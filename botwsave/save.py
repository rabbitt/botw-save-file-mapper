"""SaveFile: unified read/write API over the BotW Wii U binary save file.

Covers individual flags (get_flag/set_flag), model-level reads (read_stats,
read_inventory, etc.), and full-save YAML export/import — all without the
soft-dependency cascade that corrupts the Node tool's import-json path.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import construct as cs
from ruamel.yaml import YAML

from .effectmap import EffectMap, DependencyGraph, DependencyResult
from .codecs import (
    encode_time_of_day, decode_time_of_day,
    encode_hms, decode_hms,
    bits_to_float, float_to_bits,
)
from .inventory import Inventory, read_inventory, write_inventory, inventory_from_dict
from ._layout import FLAT_LAYOUT, ENTITY_FIELD_INFO
from . import offsets as O
from .entities import (
    ShrineCollection,
    TowerCollection,
    MemoryCollection,
    DivineBeastCollection,
    FairyFountainCollection,
    AncientTechLabCollection,
    CutsceneCollection,
    HorseCollection,
    NpcCollection,
    RuneCollection,
    SheikahSlateCollection,
    QuickTipCollection,
    SideQuestCollection,
    MainQuestCollection,
    ChampionPowerCollection,
    TownCollection,
    MasterSwordCollection,
)


def _populate_inventory_flat(fh, flat: "cs.Container") -> None:
    """Read all inventory arrays into the shared flat dict via construct Pointer reads.

    Uses the same fh that FLAT_LAYOUT just parsed — no extra open().
    Every value lands at flat[f"off{absolute_offset}"], identical to the
    effectmap entries, so the snapshot-comparison write-back in __exit__
    covers inventory changes automatically.
    """
    ROW8  = cs.Struct("v" / cs.Int32ub, cs.Padding(4))
    # 16 bytes per food entry: two uint32s separated by 4 bytes each
    ROW16 = cs.Struct("v" / cs.Int32ub, cs.Padding(4), "w" / cs.Int32ub, cs.Padding(4))

    # Slot entries: MAX_INV_SLOTS slots × SLOT_UINT32S uint32s, stride-8 each
    slot_arr = cs.Pointer(O.SLOTS_BASE, cs.Array(O.MAX_INV_SLOTS * O.SLOT_UINT32S, ROW8)).parse_stream(fh)
    for idx, row in enumerate(slot_arr):
        slot, entry = divmod(idx, O.SLOT_UINT32S)
        flat[f"off{O.SLOTS_BASE + slot * O.SLOT_WIDTH + entry * 8}"] = row.v

    # Quantities and equipped flags (both stride-8 arrays of MAX_INV_SLOTS)
    qty_arr = cs.Pointer(O.QUANTITIES_BASE, cs.Array(O.MAX_INV_SLOTS, ROW8)).parse_stream(fh)
    for i, row in enumerate(qty_arr):
        flat[f"off{O.QUANTITIES_BASE + i * O.QUANTITIES_WIDTH}"] = row.v

    eq_arr = cs.Pointer(O.EQUIPPED_BASE, cs.Array(O.MAX_INV_SLOTS, ROW8)).parse_stream(fh)
    for i, row in enumerate(eq_arr):
        flat[f"off{O.EQUIPPED_BASE + i * O.EQUIPPED_WIDTH}"] = row.v

    # Weapon / bow / shield bonus type + amount arrays (all stride-8)
    for base, count in (
        (O.WEAPON_BONUS_TYPE_BASE,   O.MAX_WEAPON_BONUS),
        (O.WEAPON_BONUS_AMOUNT_BASE, O.MAX_WEAPON_BONUS),
        (O.BOW_BONUS_TYPE_BASE,      O.MAX_BOW_BONUS),
        (O.BOW_BONUS_AMOUNT_BASE,    O.MAX_BOW_BONUS),
        (O.SHIELD_BONUS_TYPE_BASE,   O.MAX_SHIELD_BONUS),
        (O.SHIELD_BONUS_AMOUNT_BASE, O.MAX_SHIELD_BONUS),
    ):
        arr = cs.Pointer(base, cs.Array(count, ROW8)).parse_stream(fh)
        for i, row in enumerate(arr):
            flat[f"off{base + i * O.BONUS_TYPE_WIDTH}"] = row.v

    # Food arrays: two interleaved ROW16 arrays (hearts+duration, bonustype+amount)
    # FOOD_HEARTS_BASE[i]      = hearts,      FOOD_DURATION_BASE[i]      = duration
    # FOOD_BONUS_TYPE_BASE[i]  = bonus type,  FOOD_BONUS_AMOUNT_BASE[i]  = bonus amount
    hd_arr = cs.Pointer(O.FOOD_HEARTS_BASE, cs.Array(O.MAX_FOOD_ITEMS, ROW16)).parse_stream(fh)
    for i, row in enumerate(hd_arr):
        flat[f"off{O.FOOD_HEARTS_BASE   + i * O.FOOD_WIDTH}"] = row.v
        flat[f"off{O.FOOD_DURATION_BASE + i * O.FOOD_WIDTH}"] = row.w

    ba_arr = cs.Pointer(O.FOOD_BONUS_TYPE_BASE, cs.Array(O.MAX_FOOD_ITEMS, ROW16)).parse_stream(fh)
    for i, row in enumerate(ba_arr):
        flat[f"off{O.FOOD_BONUS_TYPE_BASE   + i * O.FOOD_WIDTH}"] = row.v
        flat[f"off{O.FOOD_BONUS_AMOUNT_BASE + i * O.FOOD_WIDTH}"] = row.w

    # Stash size counters (one uint32 each)
    for off in (O.WEAPON_STASH_OFFSET, O.BOW_STASH_OFFSET, O.SHIELD_STASH_OFFSET):
        flat[f"off{off}"] = cs.Pointer(off, cs.Int32ub).parse_stream(fh)


class FlagReadError(Exception):
    pass


class FlagWriteError(Exception):
    pass


# ---------------------------------------------------------------------------
# Model dataclasses for non-inventory save data
# ---------------------------------------------------------------------------

@dataclass
class Stats:
    shrinescompleted: int = 0
    staminavessels: float = 0.0   # e.g. 3.0 = 3 extra stamina vessels
    heartcontainers: float = 3.0  # e.g. 3.0 = 3 hearts
    heartsfilled: float = 3.0
    rupees: int = 0


@dataclass
class BloodMoon:
    counter: float = 0.0   # raw seconds (float32 stored in save)
    tonight: bool = False


@dataclass
class Clock:
    time: float = 120.0     # raw quarter-hour units (float32 stored in save)
    bloodmoon: BloodMoon = field(default_factory=BloodMoon)


@dataclass
class RuneState:
    enabled: bool = False
    plus: bool = False


@dataclass
class Runes:
    enabled: bool = True
    selected_index: int = 0
    bombs: RuneState = field(default_factory=RuneState)
    stasis: RuneState = field(default_factory=RuneState)
    sheikah_sensor: RuneState = field(default_factory=RuneState)
    magnesis: bool = False
    cryonis: bool = False
    camera: bool = False
    master_cycle_zero: bool = False


@dataclass
class FairyFountain:
    unlocked: bool = False


@dataclass
class FairyFountains:
    cotera: FairyFountain = field(default_factory=FairyFountain)
    kaysa: FairyFountain = field(default_factory=FairyFountain)
    malanya: FairyFountain = field(default_factory=FairyFountain)
    mija: FairyFountain = field(default_factory=FairyFountain)
    tera: FairyFountain = field(default_factory=FairyFountain)
    powerlevel: int = 0


@dataclass
class HorseData:
    name: str | None = None
    type: int | None = None
    saddle: int | None = None
    reins: int | None = None
    mane: int | None = None
    color: int | None = None
    bond: float = 0.0


@dataclass
class Horses:
    selected_slot: int | None = None
    wild: HorseData | None = None
    slot1: HorseData | None = None
    slot2: HorseData | None = None
    slot3: HorseData | None = None
    slot4: HorseData | None = None
    slot5: HorseData | None = None


# ---------------------------------------------------------------------------
# SaveFile
# ---------------------------------------------------------------------------

class SaveFile:
    """Read and write a BotW Wii U save file.

    Usage::

        with SaveFile("game_data.sav") as save:
            print(save.get_flag("shrines.akhvaquot.complete"))
            save.set_flag("shrines.akhvaquot.complete", True)

            stats = save.read_stats()
            stats.rupees = 9999
            save.write_stats(stats)

            inv = save.read_inventory()
            # modify inv ...
            save.write_inventory(inv)

            save.export_json("backup.json")   # full save → JSON
    """

    def __init__(
        self,
        path: str | Path,
        *,
        effectmap: EffectMap | None = None,
        readonly: bool = False,
        dry_run: bool = False,
    ):
        self.path = Path(path)
        self._effectmap = effectmap or EffectMap()
        self._deps = DependencyGraph(self._effectmap)
        self.readonly = readonly or dry_run
        self.dry_run = dry_run
        # _flat: the single parsed container for all flag + inventory offsets.
        self._flat: cs.Container | None = None

        # Proxy collection attributes (populated in __enter__)
        self.shrines: ShrineCollection | None = None
        self.towers: TowerCollection | None = None
        self.memories: MemoryCollection | None = None
        self.divinebeasts: DivineBeastCollection | None = None
        self.fairyfountains: FairyFountainCollection | None = None
        self.ancienttechlabs: AncientTechLabCollection | None = None
        self.cutscenes: CutsceneCollection | None = None
        self.horses: HorseCollection | None = None
        self.npcs: NpcCollection | None = None
        self.runes_collection: RuneCollection | None = None
        self.sheikahslate_collection: SheikahSlateCollection | None = None
        self.quicktips: QuickTipCollection | None = None
        self.sidequests: SideQuestCollection | None = None
        self.mainquests: MainQuestCollection | None = None
        self.championpowers: ChampionPowerCollection | None = None
        self.towns: TownCollection | None = None
        self.mastersword: MasterSwordCollection | None = None

    def __enter__(self) -> "SaveFile":
        with self.path.open('rb') as fh:
            self._flat = FLAT_LAYOUT.parse_stream(fh)
            _populate_inventory_flat(fh, self._flat)
        # Snapshot: only offsets whose value changed are written back on exit.
        self._flat_orig: dict = {k: v for k, v in self._flat.items() if not k.startswith('_')}

        # Wire entity collections — all share the same _flat container.
        def _info(key: str) -> dict:
            return ENTITY_FIELD_INFO.get(key, {})

        self.shrines            = ShrineCollection(self._flat, _info("shrines"))
        self.towers             = TowerCollection(self._flat, _info("towers"))
        self.memories           = MemoryCollection(self._flat, _info("memories"))
        self.divinebeasts       = DivineBeastCollection(self._flat, _info("divinebeasts"))
        self.fairyfountains     = FairyFountainCollection(self._flat, _info("fairyfountains"))
        self.ancienttechlabs    = AncientTechLabCollection(self._flat, _info("ancienttechlabs"))
        self.cutscenes          = CutsceneCollection(self._flat, _info("cutscenes"))
        self.horses             = HorseCollection(self._flat, _info("horses"))
        self.npcs               = NpcCollection(self._flat, _info("npcs"))
        self.runes_collection        = RuneCollection(self._flat, _info("runes"))
        self.sheikahslate_collection = SheikahSlateCollection(self._flat, _info("sheikahslate"))
        self.quicktips          = QuickTipCollection(self._flat, _info("quicktips"))
        self.sidequests         = SideQuestCollection(self._flat, _info("sidequests"))
        self.mainquests         = MainQuestCollection(self._flat, _info("mainquests"))
        self.championpowers     = ChampionPowerCollection(self._flat, _info("championpowers"))
        self.towns              = TownCollection(self._flat, _info("towns"))
        self.mastersword        = MasterSwordCollection(self._flat, _info("mastersword"))

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        # Write only the offsets whose value actually changed (surgical Pointer writes).
        if not self.readonly and not self.dry_run and self._flat is not None:
            changed = {
                key: val
                for key, val in self._flat.items()
                if not key.startswith('_') and val != self._flat_orig.get(key)
            }
            if changed:
                try:
                    with self.path.open('r+b') as fh:
                        for key, val in changed.items():
                            offset = int(key[3:])  # "off{offset}" → offset
                            cs.Pointer(offset, cs.Int32ub).build_stream(val, fh)
                except Exception:
                    pass  # don't suppress the original exception

        self._flat = None

    def _require_flat(self) -> cs.Container:
        if self._flat is None:
            raise RuntimeError("SaveFile not open — use as context manager")
        return self._flat

    # ------------------------------------------------------------------
    # Flag-level API
    # ------------------------------------------------------------------

    def get_flag(self, keypath: str) -> Any:
        """Read a single flag from the save file. Returns bool, int, or float."""
        flat = self._require_flat()
        node = self._effectmap.get(keypath)
        if node is None:
            raise FlagReadError(f"Unknown keypath: {keypath!r}")
        if not node.entries:
            raise FlagReadError(f"No entries for keypath: {keypath!r}")
        entry = node.entries[0]
        raw = flat[f"off{entry.offset}"]
        if isinstance(entry.value, bool):
            # entry.value=True  → active when raw != 0
            # entry.value=False → active when raw == 0 (inverse alias)
            return (raw != 0) if entry.value else (raw == 0)
        elif entry.value == "float":
            return bits_to_float(raw)
        elif entry.value == "integer":
            return raw
        elif entry.value == "ascii":
            return raw.rstrip(b'\x00').decode('ascii', errors='replace') if isinstance(raw, (bytes, bytearray)) else raw
        elif entry.value == "utf8":
            return raw.rstrip(b'\x00').decode('utf-8', errors='replace') if isinstance(raw, (bytes, bytearray)) else raw
        else:
            return raw  # sentinel integer literal

    def set_flag(self, keypath: str, value: Any, *, unsafe: bool = False) -> None:
        """Write a flag into the in-memory flat container.

        Changes reach disk only when the SaveFile context manager exits
        (via FLAT_LAYOUT.build_stream).  Raises FlagWriteError if keypath
        is a danger key and unsafe=False.
        """
        if not unsafe:
            result = self._deps.check_safe(keypath, include_soft=False)
            if not result.is_safe:
                raise FlagWriteError(
                    f"Refused: {keypath!r} implicates danger keys "
                    f"{result.danger_hits}. Pass unsafe=True to override."
                )
        flat = self._require_flat()
        node = self._effectmap.get(keypath)
        if node is None:
            raise FlagWriteError(f"Unknown keypath: {keypath!r}")
        if not node.entries:
            return
        # For bool keypaths: check primary entry (entries[0]) first.
        # Only write any entry if the primary needs to change.  This preserves
        # secondary entries the game left in inconsistent states (e.g. shrine-quest
        # secondaries at 0 even when the quest is complete).
        if node.entries and isinstance(node.entries[0].value, bool):
            desired = bool(value)
            primary = node.entries[0]
            primary_raw = flat[f"off{primary.offset}"]
            primary_logical = bool(primary_raw) if primary.value else (primary_raw == 0)
            if primary_logical != desired:
                for entry in node.entries:
                    if entry.value:
                        flat[f"off{entry.offset}"] = 1 if desired else 0
                    else:
                        flat[f"off{entry.offset}"] = 0 if desired else 1
            return

        for entry in node.entries:
            key = f"off{entry.offset}"
            if entry.value == "float":
                flat[key] = float_to_bits(float(value))
            elif entry.value == "integer":
                flat[key] = int(value)
            elif entry.value == "ascii":
                n = entry.length or 32
                encoded = str(value).encode('ascii', errors='replace')[:n]
                flat[key] = encoded + b'\x00' * (n - len(encoded))
            elif entry.value == "utf8":
                n = entry.length or 64
                encoded = str(value).encode('utf-8', errors='replace')[:n]
                flat[key] = encoded + b'\x00' * (n - len(encoded))
            else:
                # Integer sentinel: skip if logical bool state already matches.
                current = flat[key]
                desired_int = int(value)
                if bool(current) == bool(desired_int):
                    continue
                flat[key] = desired_int

    def check_safe(self, keypath: str, *, include_soft: bool = True) -> DependencyResult:
        return self._deps.check_safe(keypath, include_soft=include_soft)

    def get_dependencies(self, keypath: str, *, include_soft: bool = True) -> DependencyResult:
        return self.check_safe(keypath, include_soft=include_soft)

    def search_flags(self, pattern: str) -> list[str]:
        return self._effectmap.search(pattern)

    # ------------------------------------------------------------------
    # Model-level API: stats
    # ------------------------------------------------------------------

    def read_stats(self) -> Stats:
        g = self._get_flags(
            "stats.shrinescompleted", "stats.staminagauge",
            "stats.heartcontainers", "stats.heartsfilled", "stats.rupees",
        )
        return Stats(
            shrinescompleted=g["stats.shrinescompleted"],
            staminavessels=(g["stats.staminagauge"] / 200) - 5,
            heartcontainers=g["stats.heartcontainers"] / 4.0,
            heartsfilled=g["stats.heartsfilled"] / 4.0,
            rupees=g["stats.rupees"],
        )

    def write_stats(self, stats: Stats) -> None:
        if stats.shrinescompleted is not None:
            self.set_flag(f"stats.shrinescompleted", stats.shrinescompleted, unsafe=True)
        if stats.staminavessels is not None:
            self.set_flag("stats.staminagauge", int((stats.staminavessels + 5) * 200), unsafe=True)
        if stats.heartcontainers is not None:
            self.set_flag("stats.heartcontainers", int(stats.heartcontainers * 4), unsafe=True)
        if stats.heartsfilled is not None:
            self.set_flag("stats.heartsfilled", int(stats.heartsfilled * 4), unsafe=True)
        if stats.rupees is not None:
            self.set_flag("stats.rupees", stats.rupees, unsafe=True)

    # ------------------------------------------------------------------
    # Model-level API: clock
    # ------------------------------------------------------------------

    def read_clock(self) -> Clock:
        g = self._get_flags("time.specific", "bloodmoon.counter", "bloodmoon.tonight.set")
        return Clock(
            time=g["time.specific"],         # raw float32 quarter-hours; preserves exact bits
            bloodmoon=BloodMoon(
                counter=g["bloodmoon.counter"],  # raw float32 seconds; preserves exact bits
                tonight=bool(g["bloodmoon.tonight.set"]),
            ),
        )

    def write_clock(self, clock: Clock) -> None:
        # Pass raw floats directly — float_to_bits will reconstruct original bit patterns.
        self.set_flag("time.specific", float(clock.time), unsafe=True)
        self.set_flag("bloodmoon.counter", float(clock.bloodmoon.counter), unsafe=True)
        kp = "bloodmoon.tonight.set" if clock.bloodmoon.tonight else "bloodmoon.tonight.unset"
        self.set_flag(kp, True, unsafe=True)

    # ------------------------------------------------------------------
    # Model-level API: runes
    # ------------------------------------------------------------------

    def read_runes(self) -> Runes:
        g = self._get_flags(
            "runes.alldisabled", "runes.selected",
            "runes.bombs.enabled", "runes.bombs.plus.enabled",
            "runes.stasis.enabled", "runes.stasis.plus.enabled",
            "sheikahslate.sensor.enabled", "sheikahslate.sensor.plus.enabled",
            "runes.magnesis.enabled", "runes.cryonis.enabled",
            "runes.camera.enabled", "runes.mastercyclezero.enabled",
        )
        return Runes(
            enabled=not bool(g["runes.alldisabled"]),
            selected_index=g["runes.selected"],
            bombs=RuneState(enabled=bool(g["runes.bombs.enabled"]), plus=bool(g["runes.bombs.plus.enabled"])),
            stasis=RuneState(enabled=bool(g["runes.stasis.enabled"]), plus=bool(g["runes.stasis.plus.enabled"])),
            sheikah_sensor=RuneState(enabled=bool(g["sheikahslate.sensor.enabled"]), plus=bool(g["sheikahslate.sensor.plus.enabled"])),
            magnesis=bool(g["runes.magnesis.enabled"]),
            cryonis=bool(g["runes.cryonis.enabled"]),
            camera=bool(g["runes.camera.enabled"]),
            master_cycle_zero=bool(g["runes.mastercyclezero.enabled"]),
        )

    def write_runes(self, runes: Runes) -> None:
        if runes.enabled:
            self.set_flag("runes.selected", runes.selected_index, unsafe=True)
        else:
            self.set_flag("runes.alldisabled", True, unsafe=True)

        def _rune(flag_base: str, enabled: bool, plus: bool | None = None) -> None:
            kp = f"{flag_base}.{'enabled' if enabled else 'disabled'}"
            self.set_flag(kp, True, unsafe=True)
            if plus is not None:
                pkp = f"{flag_base}.plus.{'enabled' if plus else 'disabled'}"
                self.set_flag(pkp, True, unsafe=True)

        _rune("runes.bombs", runes.bombs.enabled, runes.bombs.plus)
        _rune("runes.stasis", runes.stasis.enabled, runes.stasis.plus)
        _rune("sheikahslate.sensor", runes.sheikah_sensor.enabled, runes.sheikah_sensor.plus)
        _rune("runes.magnesis", runes.magnesis)
        _rune("runes.cryonis", runes.cryonis)
        _rune("runes.camera", runes.camera)
        _rune("runes.mastercyclezero", runes.master_cycle_zero)

    # ------------------------------------------------------------------
    # Model-level API: fairy fountains
    # ------------------------------------------------------------------

    def read_fairy_fountains(self) -> FairyFountains:
        g = self._get_flags(
            "fairyfountains.cotera.unlocked", "fairyfountains.kaysa.unlocked",
            "fairyfountains.malanya.unlocked", "fairyfountains.mija.unlocked",
            "fairyfountains.tera.unlocked", "fairyfountains.powerlevel",
        )
        return FairyFountains(
            cotera=FairyFountain(unlocked=bool(g["fairyfountains.cotera.unlocked"])),
            kaysa=FairyFountain(unlocked=bool(g["fairyfountains.kaysa.unlocked"])),
            malanya=FairyFountain(unlocked=bool(g["fairyfountains.malanya.unlocked"])),
            mija=FairyFountain(unlocked=bool(g["fairyfountains.mija.unlocked"])),
            tera=FairyFountain(unlocked=bool(g["fairyfountains.tera.unlocked"])),
            powerlevel=g["fairyfountains.powerlevel"],
        )

    def write_fairy_fountains(self, ff: FairyFountains) -> None:
        self.set_flag("fairyfountains.powerlevel", ff.powerlevel, unsafe=True)
        for name, fountain in [
            ("cotera", ff.cotera), ("kaysa", ff.kaysa), ("malanya", ff.malanya),
            ("mija", ff.mija), ("tera", ff.tera),
        ]:
            kp = f"fairyfountains.{name}.{'unlocked' if fountain.unlocked else 'locked'}"
            self.set_flag(kp, True, unsafe=True)

    # ------------------------------------------------------------------
    # Model-level API: horses
    # ------------------------------------------------------------------

    def read_horses(self) -> Horses:
        selected_raw = self._get_flags("horses.selected.slot")["horses.selected.slot"]
        selected = None if selected_raw == 0xFFFFFFFF else selected_raw

        def _horse(key: str) -> HorseData | None:
            keys = [f"horses.{key}.type", f"horses.{key}.saddle", f"horses.{key}.reins",
                    f"horses.{key}.mane", f"horses.{key}.color", f"horses.{key}.bond"]
            if key != "wild":
                keys.append(f"horses.{key}.name")
            try:
                g = self._get_flags(*keys)
            except Exception:
                return None
            if not g.get(f"horses.{key}.type"):
                return None
            bond_raw = g.get(f"horses.{key}.bond", 0)
            return HorseData(
                name=g.get(f"horses.{key}.name"),
                type=g.get(f"horses.{key}.type"),
                saddle=g.get(f"horses.{key}.saddle"),
                reins=g.get(f"horses.{key}.reins"),
                mane=g.get(f"horses.{key}.mane"),
                color=g.get(f"horses.{key}.color"),
                bond=float(bond_raw) * 100.0 if bond_raw else 0.0,
            )

        return Horses(
            selected_slot=selected,
            wild=_horse("wild"),
            slot1=_horse("slot1"),
            slot2=_horse("slot2"),
            slot3=_horse("slot3"),
            slot4=_horse("slot4"),
            slot5=_horse("slot5"),
        )

    def write_horses(self, horses: Horses) -> None:
        slot_val = horses.selected_slot if horses.selected_slot is not None else 0xFFFFFFFF
        self.set_flag("horses.selected.slot", slot_val, unsafe=True)

        def _horse(key: str, h: HorseData | None) -> None:
            if h is None:
                return
            # color and bond are plain integer/float — safe to round-trip.
            # name/type/saddle/reins/mane use a stride-8 packed ASCII format
            # we don't yet encode; skip them on write to avoid corrupting those offsets.
            if h.color is not None:
                self.set_flag(f"horses.{key}.color", h.color, unsafe=True)
            if h.bond is not None:
                self.set_flag(f"horses.{key}.bond", h.bond / 100.0, unsafe=True)

        for key, h in [("wild", horses.wild), ("slot1", horses.slot1), ("slot2", horses.slot2),
                       ("slot3", horses.slot3), ("slot4", horses.slot4), ("slot5", horses.slot5)]:
            _horse(key, h)

    # ------------------------------------------------------------------
    # Model-level API: inventory
    # ------------------------------------------------------------------

    def read_inventory(self) -> Inventory:
        return read_inventory(self._require_flat())

    def write_inventory(self, inv: Inventory) -> None:
        if not self.dry_run:
            write_inventory(self._require_flat(), inv)

    # ------------------------------------------------------------------
    # World map: towers, shrines, divine beasts — all effectmap flags
    # ------------------------------------------------------------------

    def read_worldmap(self) -> dict:
        """Read all tower, shrine, and divine beast flags as a nested dict."""
        em = self._effectmap._raw
        result: dict = {}
        for top_key in ("towers", "shrines", "divinebeasts", "ancienttechlabs"):
            result[top_key] = self._read_subtree(top_key, em.get(top_key, {}))
        return result

    def write_worldmap(self, data: dict) -> None:
        self._write_subtree_flags(data)

    def read_adventure_log(self) -> dict:
        """Read all quest and memory flags as a nested dict."""
        em = self._effectmap._raw
        result: dict = {}
        for top_key in ("mainquests", "shrinequests", "sidequests", "memories"):
            result[top_key] = self._read_subtree(top_key, em.get(top_key, {}))
        return result

    def write_adventure_log(self, data: dict) -> None:
        self._write_subtree_flags(data)

    # ------------------------------------------------------------------
    # Full save export / import
    # ------------------------------------------------------------------

    def export_yaml(self, output: str | Path | None = None) -> dict:
        """Export the full save to a dict (and optionally write to a YAML file)."""
        # Build the map section from proxy collections when available
        map_section: dict = {}
        for section_name in ("shrines", "towers", "divinebeasts", "ancienttechlabs"):
            collection = getattr(self, section_name, None)
            if collection is not None:
                map_section[section_name] = collection.to_dict()
        # Fall back to read_worldmap() if no collections are available
        if not map_section:
            map_section = self.read_worldmap()

        data = {
            "inventory": self.read_inventory().to_dict(),
            "stats": _dataclass_to_dict(self.read_stats()),
            "clock": _dataclass_to_dict(self.read_clock()),
            "runes": _dataclass_to_dict(self.read_runes()),
            "fairyfountains": _dataclass_to_dict(self.read_fairy_fountains()),
            "horses": _dataclass_to_dict(self.read_horses()),
            "map": map_section,
            "adventurelog": self.read_adventure_log(),
        }
        if output:
            yaml = YAML()
            yaml.default_flow_style = False
            with Path(output).open("w") as f:
                yaml.dump(data, f)
        return data

    def import_yaml(self, source: str | Path | dict) -> None:
        """Import a save YAML. Writes only the exact offsets specified — no cascade."""
        if isinstance(source, (str, Path)):
            yaml = YAML()
            data = yaml.load(Path(source).read_text())
        else:
            data = source

        if "inventory" in data:
            self.write_inventory(inventory_from_dict(data["inventory"]))
        if "stats" in data:
            self.write_stats(_stats_from_dict(data["stats"]))
        if "clock" in data:
            self.write_clock(_clock_from_dict(data["clock"]))
        if "runes" in data:
            self.write_runes(_runes_from_dict(data["runes"]))
        if "fairyfountains" in data:
            self.write_fairy_fountains(_ff_from_dict(data["fairyfountains"]))
        if "horses" in data:
            self.write_horses(_horses_from_dict(data["horses"]))
        if "map" in data:
            for section_name, section_data in data["map"].items():
                collection = getattr(self, section_name, None)
                if collection is None or not isinstance(section_data, dict):
                    # Fall back to old subtree writer for sections not wired as collections
                    self._write_subtree_flags({section_name: section_data})
                    continue
                for entity_name, fields in section_data.items():
                    if entity_name not in collection or not isinstance(fields, dict):
                        continue
                    proxy = collection[entity_name]
                    for field_name, value in fields.items():
                        try:
                            setattr(proxy, field_name, value)
                        except (AttributeError, NotImplementedError):
                            pass
        if "adventurelog" in data:
            self.write_adventure_log(data["adventurelog"])

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_flags(self, *keypaths: str) -> dict[str, Any]:
        return {kp: self.get_flag(kp) for kp in keypaths}

    def _read_subtree(self, prefix: str, node: Any) -> Any:
        """Recursively read all leaf effectmap flags under a subtree."""
        if not isinstance(node, dict):
            return None
        if "entries" in node:
            try:
                return self.get_flag(prefix)
            except Exception:
                return None
        return {
            k: self._read_subtree(f"{prefix}.{k}", v)
            for k, v in node.items()
        }

    def _write_subtree_flags(self, data: Any, prefix: str = "") -> None:
        """Recursively write flag values from a nested dict."""
        if not isinstance(data, dict):
            return
        for k, v in data.items():
            kp = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                self._write_subtree_flags(v, kp)
            elif v is not None:
                try:
                    self.set_flag(kp, v, unsafe=True)
                except Exception:
                    pass

    @property
    def effectmap(self) -> EffectMap:
        return self._effectmap

    @property
    def deps(self) -> DependencyGraph:
        return self._deps


# ---------------------------------------------------------------------------
# Dict ↔ dataclass helpers for JSON import
# ---------------------------------------------------------------------------

def _dataclass_to_dict(obj: Any) -> dict:
    import dataclasses
    def _conv(o: Any) -> Any:
        if dataclasses.is_dataclass(o):
            return {k: _conv(v) for k, v in dataclasses.asdict(o).items()}
        if isinstance(o, list):
            return [_conv(i) for i in o]
        return o
    return _conv(obj)


def _stats_from_dict(d: dict) -> Stats:
    return Stats(**{k: v for k, v in d.items() if k in Stats.__dataclass_fields__})


def _clock_from_dict(d: dict) -> Clock:
    bm = d.get("bloodmoon", {})
    raw_counter = bm.get("counter", 0.0)
    if isinstance(raw_counter, str):
        # Legacy YAML exports used HH:MM:SS; convert to seconds.
        counter = float(encode_hms(raw_counter))
    else:
        counter = float(raw_counter)
    return Clock(
        time=d.get("time", 120.0),
        bloodmoon=BloodMoon(counter=counter, tonight=bm.get("tonight", False)),
    )


def _runes_from_dict(d: dict) -> Runes:
    def _rs(x: dict | None) -> RuneState:
        if not x:
            return RuneState()
        return RuneState(enabled=x.get("enabled", False), plus=x.get("plus", False))
    return Runes(
        enabled=d.get("enabled", True),
        selected_index=d.get("selected_index", 0),
        bombs=_rs(d.get("bombs")),
        stasis=_rs(d.get("stasis")),
        sheikah_sensor=_rs(d.get("sheikah_sensor")),
        magnesis=d.get("magnesis", False),
        cryonis=d.get("cryonis", False),
        camera=d.get("camera", False),
        master_cycle_zero=d.get("master_cycle_zero", False),
    )


def _ff_from_dict(d: dict) -> FairyFountains:
    def _f(x: dict | None) -> FairyFountain:
        return FairyFountain(unlocked=bool((x or {}).get("unlocked", False)))
    return FairyFountains(
        cotera=_f(d.get("cotera")), kaysa=_f(d.get("kaysa")),
        malanya=_f(d.get("malanya")), mija=_f(d.get("mija")),
        tera=_f(d.get("tera")), powerlevel=d.get("powerlevel", 0),
    )


def _horses_from_dict(d: dict) -> Horses:
    def _h(x: dict | None) -> HorseData | None:
        if not x:
            return None
        return HorseData(**{k: v for k, v in x.items() if k in HorseData.__dataclass_fields__})
    return Horses(
        selected_slot=d.get("selected_slot"),
        wild=_h(d.get("wild")), slot1=_h(d.get("slot1")),
        slot2=_h(d.get("slot2")), slot3=_h(d.get("slot3")),
        slot4=_h(d.get("slot4")), slot5=_h(d.get("slot5")),
    )
