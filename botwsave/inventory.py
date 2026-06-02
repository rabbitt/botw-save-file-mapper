"""Slot-based inventory read/write for BotW Wii U save files.

Items are stored in a single contiguous array of 128-byte slots starting at
SLOTS_BASE. Categories are ordered: weapons → bows → arrows → shields →
armor → materials → food → keyitems. Category boundaries are detected by
matching slot entry patterns against the item catalog YAMLs.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .binary import BinaryFile
from .catalog import (
    CATEGORIES, get_catalog, get_item_def, match_slot_entries, write_entries_for,
)
from .codecs import (
    bits_to_float, bits_to_int, float_to_bits, int_to_bits,
    encode_duration, decode_duration,
)
from . import offsets as O


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class WeaponBonus(str, Enum):
    ATTACK = "attack"
    DURABILITY = "durability"
    CRITICAL = "critical"
    LONGTHROW = "longthrow"
    ATTACK_PLUS = "attackplus"
    DURABILITY_PLUS = "durabilityplus"
    CRITICAL_PLUS = "criticalplus"
    LONGTHROW_PLUS = "longthrowplus"


class BowBonus(str, Enum):
    ATTACK = "attack"
    DURABILITY = "durability"
    FIVESHOTS = "fiveshots"
    THREESHOTS = "threeshots"
    QUICKSHOT = "quickshot"
    ATTACK_PLUS = "attackplus"
    DURABILITY_PLUS = "durabilityplus"
    FIVESHOTS_PLUS = "fiveshotsplus"
    THREESHOTS_PLUS = "threeshotsplus"
    QUICKSHOT_PLUS = "quickshotplus"


class ShieldBonus(str, Enum):
    DURABILITY = "durability"
    SHIELDSURF = "shieldsurf"
    SHIELDGUARD = "shieldguard"
    DURABILITY_PLUS = "durabilityplus"
    SHIELDSURF_PLUS = "shieldsurfplus"
    SHIELDGUARD_PLUS = "shieldguardplus"


class FoodBonusType(str, Enum):
    HEARTY = "hearty"
    CHILLY = "chilly"
    SPICY = "spicy"
    ELECTRO = "electro"
    MIGHTY = "mighty"
    TOUGH = "tough"
    SNEAKY = "sneaky"
    HASTY = "hasty"
    ENERGIZING = "energizing"
    ENDURING = "enduring"
    FIREPROOF = "fireproof"


class DyeColor(str, Enum):
    ORIGINAL = "original"
    BLUE = "blue"
    RED = "red"
    YELLOW = "yellow"
    WHITE = "white"
    BLACK = "black"
    PURPLE = "purple"
    GREEN = "green"
    LIGHTBLUE = "lightblue"
    NAVY = "navy"
    ORANGE = "orange"
    PEACH = "peach"
    CRIMSON = "crimson"
    LIGHTYELLOW = "lightyellow"
    BROWN = "brown"
    GRAY = "gray"


# ---------------------------------------------------------------------------
# Bonus type ↔ uint32 mappings
# ---------------------------------------------------------------------------

_WEAPON_BONUS_ENCODE: dict[str, int] = {
    "attack": 0x1, "durability": 0x2, "critical": 0x4, "longthrow": 0x8,
    "attackplus": 0x80000001, "durabilityplus": 0x80000002,
    "criticalplus": 0x80000004, "longthrowplus": 0x80000008,
}
_WEAPON_BONUS_DECODE = {v: k for k, v in _WEAPON_BONUS_ENCODE.items()}

_BOW_BONUS_ENCODE: dict[str, int] = {
    "attack": 0x1, "durability": 0x2, "fiveshots": 0x10, "threeshots": 0x20,
    "quickshot": 0x40, "attackplus": 0x80000001, "durabilityplus": 0x80000002,
    "fiveshotsplus": 0x80000010, "threeshotsplus": 0x80000020,
    "quickshotplus": 0x80000040,
}
_BOW_BONUS_DECODE = {v: k for k, v in _BOW_BONUS_ENCODE.items()}

_SHIELD_BONUS_ENCODE: dict[str, int] = {
    "durability": 0x2, "shieldsurf": 0x80, "shieldguard": 0x100,
    "durabilityplus": 0x80000002, "shieldsurfplus": 0x80000080,
    "shieldguardplus": 0x80000100,
}
_SHIELD_BONUS_DECODE = {v: k for k, v in _SHIELD_BONUS_ENCODE.items()}

_FOOD_TYPE_ENCODE: dict[str, int] = {
    "none": 0xBF800000,
    "hearty": 0x40000000, "chilly": 0x40800000, "spicy": 0x40A00000,
    "electro": 0x40C00000, "mighty": 0x41200000, "tough": 0x41300000,
    "sneaky": 0x41400000, "hasty": 0x41500000, "energizing": 0x41600000,
    "enduring": 0x41700000, "fireproof": 0x41800000,
}
_FOOD_TYPE_DECODE = {v: k for k, v in _FOOD_TYPE_ENCODE.items()}

_FOOD_AMOUNT_ENCODE: dict[int, int] = {0: 0, 1: 0x3F800000, 2: 0x40000000, 3: 0x40400000}
_FOOD_AMOUNT_DECODE = {v: k for k, v in _FOOD_AMOUNT_ENCODE.items()}

_DYE_ENCODE: dict[str, int] = {c.value: i for i, c in enumerate(DyeColor)}
_DYE_DECODE: dict[int, str] = {i: c.value for i, c in enumerate(DyeColor)}

# Champion abilities that must never be written through the key items slot
_UNWRITEABLE_KEY_ITEMS = frozenset({
    "daruksprotection", "miphasgrace", "revalisgale", "urbosasfury",
})

# Stackable hearts placeholder value (for stackable food items)
_STACKABLE_HEARTS_BITS = 0xBF800000


# ---------------------------------------------------------------------------
# Item dataclasses
# ---------------------------------------------------------------------------

@dataclass
class ItemBonus:
    type: str
    amount: int | float


@dataclass
class FoodBonus:
    type: str
    amount: int | float
    duration: str | None = None  # 'MM:SS' or 'HH:MM:SS'; absent for hearty/energizing/enduring


@dataclass
class WeaponItem:
    name: str
    equipped: bool = False
    durability: int = 0
    bonus: ItemBonus | None = None


@dataclass
class BowItem:
    name: str
    equipped: bool = False
    durability: int = 0
    bonus: ItemBonus | None = None


@dataclass
class ArrowItem:
    name: str
    equipped: bool = False
    quantity: int = 1


@dataclass
class ShieldItem:
    name: str
    equipped: bool = False
    durability: int = 0
    bonus: ItemBonus | None = None


@dataclass
class ArmorItem:
    name: str
    equipped: bool = False
    color: str = "original"


@dataclass
class MaterialItem:
    name: str
    quantity: int = 1


@dataclass
class FoodItem:
    name: str
    stackable: bool = True
    quantity: int = 1
    hearts: float | str = 0.0  # float or 'fullrecovery'
    bonus: FoodBonus | None = None


@dataclass
class KeyItem:
    name: str
    unique: bool = False
    stackable: bool = False
    quantity: int = 1


@dataclass
class Inventory:
    stash_weapons: int = 0
    stash_bows: int = 0
    stash_shields: int = 0
    weapons: list[WeaponItem] = field(default_factory=list)
    bows: list[BowItem] = field(default_factory=list)
    arrows: list[ArrowItem] = field(default_factory=list)
    shields: list[ShieldItem] = field(default_factory=list)
    armor: list[ArmorItem] = field(default_factory=list)
    materials: list[MaterialItem] = field(default_factory=list)
    food: list[FoodItem] = field(default_factory=list)
    keyitems: list[KeyItem] = field(default_factory=list)

    def to_dict(self) -> dict:
        import dataclasses
        def _convert(obj: Any) -> Any:
            if dataclasses.is_dataclass(obj):
                return {k: _convert(v) for k, v in dataclasses.asdict(obj).items() if v is not None}
            if isinstance(obj, list):
                return [_convert(i) for i in obj]
            return obj
        return _convert(self)


# ---------------------------------------------------------------------------
# Slot entry reading
# ---------------------------------------------------------------------------

def _read_slot_entries(bf: BinaryFile, slot: int) -> list[dict]:
    """Read the 16 uint32 values from a slot as relative-offset entry dicts."""
    base = O.slot_offset(slot)
    return [
        {"offset": i * 8, "value": bf.read_uint32(base + i * 8)}
        for i in range(O.SLOT_UINT32S)
    ]


def _write_slot_entries(bf: BinaryFile, slot: int, entries: list[dict]) -> None:
    """Write an item's entry pattern to a slot, zero-filling unused positions."""
    base = O.slot_offset(slot)
    data = {e["offset"]: e["value"] for e in entries}
    for i in range(O.SLOT_UINT32S):
        bf.write_uint32(base + i * 8, data.get(i * 8, 0))


# ---------------------------------------------------------------------------
# Category boundary detection
# ---------------------------------------------------------------------------

def _detect_slot_ranges(bf: BinaryFile) -> dict[str, tuple[int, int]]:
    """Return {category: (first_slot, last_slot)} by scanning the save binary."""
    weapon_stash = bf.read_uint32(O.WEAPON_STASH_OFFSET)
    bow_stash = bf.read_uint32(O.BOW_STASH_OFFSET)
    shield_stash = bf.read_uint32(O.SHIELD_STASH_OFFSET)

    # Weapons: scan up to stash limit, check for weapon type marker at offset +8
    weapon_first = 0
    weapon_count = 0
    for i in range(weapon_stash):
        marker = bf.read_uint32(O.slot_offset(weapon_first + i) + 8)
        if marker not in (O.ITEM_TYPE_TWOHANDED, O.ITEM_TYPE_MELEE_OTHER):
            break
        weapon_count += 1

    bow_first = weapon_first + weapon_count
    bow_count = 0
    for i in range(bow_stash):
        marker = bf.read_uint32(O.slot_offset(bow_first + i) + 8)
        if marker != O.ITEM_TYPE_BOW:
            break
        bow_count += 1

    # Arrows: detect by catalog matching
    arrow_first = bow_first + bow_count
    arrow_catalog = get_catalog("arrows")
    arrow_names = list(arrow_catalog.keys())
    arrow_count = 0
    for name in arrow_names:
        entries = arrow_catalog[name].get("entries", [])
        if not entries:
            continue
        slot_entries = _read_slot_entries(bf, arrow_first + arrow_count)
        matched = match_slot_entries(slot_entries, "arrows")
        if matched:
            arrow_count += 1

    shield_first = arrow_first + arrow_count
    shield_count = 0
    for i in range(shield_stash):
        marker = bf.read_uint32(O.slot_offset(shield_first + i))
        if marker != O.ITEM_TYPE_STASHABLE:
            break
        shield_count += 1

    armor_first = shield_first + shield_count
    armor_count = 0
    while bf.read_uint32(O.slot_offset(armor_first + armor_count)) == O.ITEM_TYPE_ARMOR:
        armor_count += 1

    material_first = armor_first + armor_count
    material_count = _count_by_catalog(bf, material_first, "materials")

    food_first = material_first + material_count
    food_count = _count_by_catalog(bf, food_first, "food")

    keyitem_first = food_first + food_count
    keyitem_count = _count_by_catalog(bf, keyitem_first, "keyitems")

    def _range(first: int, count: int) -> tuple[int, int]:
        last = first + count - 1 if count > 0 else first
        return first, last

    return {
        "weapons": _range(weapon_first, weapon_count),
        "bows": _range(bow_first, bow_count),
        "arrows": _range(arrow_first, arrow_count),
        "shields": _range(shield_first, shield_count),
        "armor": _range(armor_first, armor_count),
        "materials": _range(material_first, material_count),
        "food": _range(food_first, food_count),
        "keyitems": _range(keyitem_first, keyitem_count),
    }


def _count_by_catalog(bf: BinaryFile, first_slot: int, category: str) -> int:
    count = 0
    while True:
        entries = _read_slot_entries(bf, first_slot + count)
        if not match_slot_entries(entries, category):
            break
        count += 1
    return count


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------

def read_inventory(bf: BinaryFile) -> Inventory:
    """Read the full inventory from an open BinaryFile."""
    ranges = _detect_slot_ranges(bf)

    inv = Inventory(
        stash_weapons=bf.read_uint32(O.WEAPON_STASH_OFFSET),
        stash_bows=bf.read_uint32(O.BOW_STASH_OFFSET),
        stash_shields=bf.read_uint32(O.SHIELD_STASH_OFFSET),
    )

    first, last = ranges["weapons"]
    for slot in range(first, last + 1):
        entries = _read_slot_entries(bf, slot)
        name = match_slot_entries(entries, "weapons")
        if not name:
            break
        idx = slot - first
        inv.weapons.append(WeaponItem(
            name=name,
            equipped=bool(bf.read_uint32(O.equipped_offset(slot))),
            durability=bf.read_uint32(O.quantity_offset(slot)),
            bonus=_read_weapon_bonus(bf, idx, "weapons", _WEAPON_BONUS_DECODE),
        ))

    first, last = ranges["bows"]
    for slot in range(first, last + 1):
        entries = _read_slot_entries(bf, slot)
        name = match_slot_entries(entries, "bows")
        if not name:
            break
        idx = slot - first
        inv.bows.append(BowItem(
            name=name,
            equipped=bool(bf.read_uint32(O.equipped_offset(slot))),
            durability=bf.read_uint32(O.quantity_offset(slot)),
            bonus=_read_weapon_bonus(bf, idx, "bows", _BOW_BONUS_DECODE),
        ))

    first, last = ranges["arrows"]
    for slot in range(first, last + 1):
        entries = _read_slot_entries(bf, slot)
        name = match_slot_entries(entries, "arrows")
        if not name:
            break
        inv.arrows.append(ArrowItem(
            name=name,
            equipped=bool(bf.read_uint32(O.equipped_offset(slot))),
            quantity=bf.read_uint32(O.quantity_offset(slot)),
        ))

    first, last = ranges["shields"]
    for slot in range(first, last + 1):
        entries = _read_slot_entries(bf, slot)
        name = match_slot_entries(entries, "shields")
        if not name:
            break
        idx = slot - first
        inv.shields.append(ShieldItem(
            name=name,
            equipped=bool(bf.read_uint32(O.equipped_offset(slot))),
            durability=bf.read_uint32(O.quantity_offset(slot)),
            bonus=_read_weapon_bonus(bf, idx, "shields", _SHIELD_BONUS_DECODE),
        ))

    first, last = ranges["armor"]
    for slot in range(first, last + 1):
        entries = _read_slot_entries(bf, slot)
        name = match_slot_entries(entries, "armor")
        if not name:
            break
        color_val = bf.read_uint32(O.quantity_offset(slot))
        color = _DYE_DECODE.get(color_val, "original")
        item = ArmorItem(
            name=name,
            equipped=bool(bf.read_uint32(O.equipped_offset(slot))),
        )
        if color != "original":
            item.color = color
        inv.armor.append(item)

    first, last = ranges["materials"]
    for slot in range(first, last + 1):
        entries = _read_slot_entries(bf, slot)
        name = match_slot_entries(entries, "materials")
        if not name:
            break
        inv.materials.append(MaterialItem(
            name=name,
            quantity=bf.read_uint32(O.quantity_offset(slot)),
        ))

    first, last = ranges["food"]
    for slot in range(first, last + 1):
        entries = _read_slot_entries(bf, slot)
        name = match_slot_entries(entries, "food")
        if not name:
            break
        idx = slot - first
        item_def = get_item_def(name, "food") or {}
        stackable = item_def.get("stackable", True)
        inv.food.append(_read_food_item(bf, name, slot, idx, stackable))

    first, last = ranges["keyitems"]
    for slot in range(first, last + 1):
        entries = _read_slot_entries(bf, slot)
        name = match_slot_entries(entries, "keyitems")
        if not name:
            break
        item_def = get_item_def(name, "keyitems") or {}
        inv.keyitems.append(KeyItem(
            name=name,
            unique=item_def.get("unique", False),
            stackable=item_def.get("stackable", False),
            quantity=bf.read_uint32(O.quantity_offset(slot)),
        ))

    return inv


def _read_weapon_bonus(
    bf: BinaryFile, idx: int, category: str, decode_map: dict
) -> ItemBonus | None:
    type_bits = bf.read_uint32(O.bonus_type_offset(idx, category))
    bonus_type = decode_map.get(type_bits)
    if bonus_type is None:
        return None
    amount = bf.read_uint32(O.bonus_amount_offset(idx, category))
    return ItemBonus(type=bonus_type, amount=amount)


def _read_food_item(
    bf: BinaryFile, name: str, slot: int, idx: int, stackable: bool
) -> FoodItem:
    hearts_bits = bf.read_uint32(O.food_hearts_offset(idx))
    quarter_hearts = bits_to_int(hearts_bits)
    full_hearts = quarter_hearts / 4.0

    is_frozen = name.startswith("frozen") or name.startswith("icy")
    if is_frozen:
        return FoodItem(
            name=name, stackable=stackable,
            quantity=bf.read_uint32(O.quantity_offset(slot)),
            hearts=full_hearts,
            bonus=FoodBonus(type="chilly", amount=1, duration="01:00"),
        )

    type_bits = bf.read_uint32(O.food_bonus_type_offset(idx))
    bonus_type = _FOOD_TYPE_DECODE.get(type_bits)

    bonus: FoodBonus | None = None
    hearts: float | str = full_hearts

    if bonus_type == "hearty":
        hearts = "fullrecovery"
        bonus = FoodBonus(type="hearty", amount=full_hearts)
    elif bonus_type == "energizing":
        raw = bits_to_float(bf.read_uint32(O.food_bonus_amount_offset(idx)))
        bonus = FoodBonus(type="energizing", amount=raw / 1000.0)
    elif bonus_type == "enduring":
        raw = bits_to_float(bf.read_uint32(O.food_bonus_amount_offset(idx)))
        bonus = FoodBonus(type="enduring", amount=raw / 5.0)
    elif bonus_type is not None:
        amount = _FOOD_AMOUNT_DECODE.get(bf.read_uint32(O.food_bonus_amount_offset(idx)), 0)
        duration = decode_duration(bf.read_uint32(O.food_duration_offset(idx)))
        bonus = FoodBonus(type=bonus_type, amount=amount, duration=duration)

    return FoodItem(
        name=name, stackable=stackable,
        quantity=bf.read_uint32(O.quantity_offset(slot)),
        hearts=hearts,
        bonus=bonus,
    )


# ---------------------------------------------------------------------------
# Write
# ---------------------------------------------------------------------------

def write_inventory(bf: BinaryFile, inv: Inventory) -> None:
    """Write the full inventory to an open BinaryFile."""
    slot = 0

    slot = _write_weapons(bf, inv, slot)
    slot = _write_bows(bf, inv, slot)
    slot = _write_arrows(bf, inv, slot)
    slot = _write_shields(bf, inv, slot)
    slot = _write_armor(bf, inv, slot)
    slot = _write_materials(bf, inv, slot)
    slot = _write_food(bf, inv, slot)
    _write_keyitems(bf, inv, slot)


def _condense(items: list, category: str) -> list:
    """Stack stackable duplicates and drop excess unique items (mirrors Node behaviour)."""
    catalog = get_catalog(category)
    counts: dict[str, int] = {}
    seen_unique: set[str] = set()
    result = []

    for item in items:
        item_def = catalog.get(item.name, {})
        unique = item_def.get("unique", getattr(item, "unique", False))
        stackable = item_def.get("stackable", getattr(item, "stackable", False))

        if unique and item.name in seen_unique:
            continue
        seen_unique.add(item.name)

        qty = getattr(item, "quantity", 1)
        if stackable:
            if item.name not in counts:
                counts[item.name] = 0
                result.append(item)
            counts[item.name] = min(counts[item.name] + qty, 999)
        else:
            counts[item.name] = qty
            result.append(item)

    for item in result:
        item_def = catalog.get(item.name, {})
        if item_def.get("stackable", getattr(item, "stackable", False)):
            item.quantity = counts[item.name]

    return result


def _write_weapons(bf: BinaryFile, inv: Inventory, first_slot: int) -> int:
    items = _condense(list(inv.weapons), "weapons")
    bf.write_uint32(O.WEAPON_STASH_OFFSET, inv.stash_weapons)
    for i, item in enumerate(items):
        slot = first_slot + i
        _write_slot_entries(bf, slot, write_entries_for(item.name, "weapons"))
        bf.write_uint32(O.equipped_offset(slot), 1 if item.equipped else 0)
        bf.write_uint32(O.quantity_offset(slot), item.durability)
        bt = _WEAPON_BONUS_ENCODE.get(item.bonus.type, 0) if item.bonus else 0
        ba = item.bonus.amount if item.bonus else 0
        bf.write_uint32(O.bonus_type_offset(i, "weapons"), bt)
        bf.write_uint32(O.bonus_amount_offset(i, "weapons"), ba)
    return first_slot + len(items)


def _write_bows(bf: BinaryFile, inv: Inventory, first_slot: int) -> int:
    items = _condense(list(inv.bows), "bows")
    bf.write_uint32(O.BOW_STASH_OFFSET, inv.stash_bows)
    for i, item in enumerate(items):
        slot = first_slot + i
        _write_slot_entries(bf, slot, write_entries_for(item.name, "bows"))
        bf.write_uint32(O.equipped_offset(slot), 1 if item.equipped else 0)
        bf.write_uint32(O.quantity_offset(slot), item.durability)
        bt = _BOW_BONUS_ENCODE.get(item.bonus.type, 0) if item.bonus else 0
        ba = item.bonus.amount if item.bonus else 0
        bf.write_uint32(O.bonus_type_offset(i, "bows"), bt)
        bf.write_uint32(O.bonus_amount_offset(i, "bows"), ba)
    return first_slot + len(items)


def _write_arrows(bf: BinaryFile, inv: Inventory, first_slot: int) -> int:
    items = _condense(list(inv.arrows), "arrows")
    for i, item in enumerate(items):
        slot = first_slot + i
        _write_slot_entries(bf, slot, write_entries_for(item.name, "arrows"))
        bf.write_uint32(O.equipped_offset(slot), 1 if item.equipped else 0)
        bf.write_uint32(O.quantity_offset(slot), item.quantity)
    return first_slot + len(items)


def _write_shields(bf: BinaryFile, inv: Inventory, first_slot: int) -> int:
    items = _condense(list(inv.shields), "shields")
    bf.write_uint32(O.SHIELD_STASH_OFFSET, inv.stash_shields)
    for i, item in enumerate(items):
        slot = first_slot + i
        _write_slot_entries(bf, slot, write_entries_for(item.name, "shields"))
        bf.write_uint32(O.equipped_offset(slot), 1 if item.equipped else 0)
        bf.write_uint32(O.quantity_offset(slot), item.durability)
        bt = _SHIELD_BONUS_ENCODE.get(item.bonus.type, 0) if item.bonus else 0
        ba = item.bonus.amount if item.bonus else 0
        bf.write_uint32(O.bonus_type_offset(i, "shields"), bt)
        bf.write_uint32(O.bonus_amount_offset(i, "shields"), ba)
    return first_slot + len(items)


def _write_armor(bf: BinaryFile, inv: Inventory, first_slot: int) -> int:
    items = _condense(list(inv.armor), "armor")
    for i, item in enumerate(items):
        slot = first_slot + i
        _write_slot_entries(bf, slot, write_entries_for(item.name, "armor"))
        bf.write_uint32(O.equipped_offset(slot), 1 if item.equipped else 0)
        bf.write_uint32(O.quantity_offset(slot), _DYE_ENCODE.get(item.color, 0))
    return first_slot + len(items)


def _write_materials(bf: BinaryFile, inv: Inventory, first_slot: int) -> int:
    items = _condense(list(inv.materials), "materials")
    for i, item in enumerate(items):
        slot = first_slot + i
        _write_slot_entries(bf, slot, write_entries_for(item.name, "materials"))
        bf.write_uint32(O.equipped_offset(slot), 0)
        bf.write_uint32(O.quantity_offset(slot), item.quantity)
    return first_slot + len(items)


def _write_food(bf: BinaryFile, inv: Inventory, first_slot: int) -> int:
    items = _condense(list(inv.food), "food")
    for i, item in enumerate(items):
        slot = first_slot + i
        _write_slot_entries(bf, slot, write_entries_for(item.name, "food"))
        bf.write_uint32(O.equipped_offset(slot), 0)
        bf.write_uint32(O.quantity_offset(slot), item.quantity if item.stackable else 1)

        full_hearts = (
            item.bonus.amount if item.bonus and item.bonus.type == "hearty"
            else (item.hearts if isinstance(item.hearts, (int, float)) else 0)
        )
        quarter_hearts = int(full_hearts * 4)
        hearts_bits = _STACKABLE_HEARTS_BITS if item.stackable else int_to_bits(quarter_hearts)
        bf.write_uint32(O.food_hearts_offset(i), hearts_bits)

        if item.bonus and item.bonus.type:
            bt = _FOOD_TYPE_ENCODE.get(item.bonus.type, _FOOD_TYPE_ENCODE["none"])
            bf.write_uint32(O.food_bonus_type_offset(i), bt)
            if item.bonus.type == "energizing":
                bf.write_uint32(O.food_bonus_amount_offset(i), float_to_bits(item.bonus.amount * 1000))
                bf.write_uint32(O.food_duration_offset(i), 0)
            elif item.bonus.type == "enduring":
                bf.write_uint32(O.food_bonus_amount_offset(i), float_to_bits(item.bonus.amount * 5.0))
                bf.write_uint32(O.food_duration_offset(i), 0)
            elif item.bonus.type == "hearty":
                bf.write_uint32(O.food_bonus_amount_offset(i), int_to_bits(quarter_hearts))
                bf.write_uint32(O.food_duration_offset(i), 0)
            elif item.bonus.duration:
                bf.write_uint32(O.food_bonus_amount_offset(i), _FOOD_AMOUNT_ENCODE.get(int(item.bonus.amount), 0))
                bf.write_uint32(O.food_duration_offset(i), encode_duration(item.bonus.duration))
            else:
                bf.write_uint32(O.food_bonus_amount_offset(i), 0)
                bf.write_uint32(O.food_duration_offset(i), 0)
        else:
            bf.write_uint32(O.food_bonus_type_offset(i), _FOOD_TYPE_ENCODE["none"])
            bf.write_uint32(O.food_bonus_amount_offset(i), 0)
            bf.write_uint32(O.food_duration_offset(i), 0)

    return first_slot + len(items)


def _write_keyitems(bf: BinaryFile, inv: Inventory, first_slot: int) -> None:
    writeable = [i for i in inv.keyitems if i.name not in _UNWRITEABLE_KEY_ITEMS]
    items = _condense(writeable, "keyitems")
    for i, item in enumerate(items):
        slot = first_slot + i
        _write_slot_entries(bf, slot, write_entries_for(item.name, "keyitems"))
        bf.write_uint32(O.equipped_offset(slot), 0)
        bf.write_uint32(O.quantity_offset(slot), item.quantity or 1)
    # Write a zeroed terminator slot after the last key item
    terminator_slot = first_slot + len(items)
    _write_slot_entries(bf, terminator_slot, [{"offset": i * 8, "value": 0} for i in range(O.SLOT_UINT32S)])


# ---------------------------------------------------------------------------
# JSON round-trip helpers
# ---------------------------------------------------------------------------

def inventory_from_dict(data: dict) -> Inventory:
    """Reconstruct an Inventory from a plain dict (e.g. loaded from JSON)."""
    def _bonus(d: dict | None) -> ItemBonus | None:
        if not d:
            return None
        return ItemBonus(type=d["type"], amount=d["amount"])

    def _food_bonus(d: dict | None) -> FoodBonus | None:
        if not d:
            return None
        return FoodBonus(type=d["type"], amount=d["amount"], duration=d.get("duration"))

    return Inventory(
        stash_weapons=data.get("stash_weapons", 0),
        stash_bows=data.get("stash_bows", 0),
        stash_shields=data.get("stash_shields", 0),
        weapons=[WeaponItem(name=w["name"], equipped=w.get("equipped", False),
                            durability=w.get("durability", 0), bonus=_bonus(w.get("bonus")))
                 for w in data.get("weapons", [])],
        bows=[BowItem(name=b["name"], equipped=b.get("equipped", False),
                      durability=b.get("durability", 0), bonus=_bonus(b.get("bonus")))
              for b in data.get("bows", [])],
        arrows=[ArrowItem(name=a["name"], equipped=a.get("equipped", False),
                          quantity=a.get("quantity", 1))
                for a in data.get("arrows", [])],
        shields=[ShieldItem(name=s["name"], equipped=s.get("equipped", False),
                            durability=s.get("durability", 0), bonus=_bonus(s.get("bonus")))
                 for s in data.get("shields", [])],
        armor=[ArmorItem(name=a["name"], equipped=a.get("equipped", False),
                         color=a.get("color", "original"))
               for a in data.get("armor", [])],
        materials=[MaterialItem(name=m["name"], quantity=m.get("quantity", 1))
                   for m in data.get("materials", [])],
        food=[FoodItem(name=f["name"], stackable=f.get("stackable", True),
                       quantity=f.get("quantity", 1), hearts=f.get("hearts", 0.0),
                       bonus=_food_bonus(f.get("bonus")))
              for f in data.get("food", [])],
        keyitems=[KeyItem(name=k["name"], unique=k.get("unique", False),
                          stackable=k.get("stackable", False), quantity=k.get("quantity", 1))
                  for k in data.get("keyitems", [])],
    )
