"""Per-entity proxy and collection subclasses for each save section.

Each section has:
  - A *Proxy class: wraps a single entity container with type-correct field access.
  - A *Collection class: wraps the full section container and yields proxies.

Horse string fields (name, type, saddle, reins, mane) use stride-8 encoding not
yet implemented and raise NotImplementedError on get and set.
"""

from __future__ import annotations

import construct as cs

from .base import EntityProxy, EntityCollection
from ._layout import (
    SHRINES_NAMES, SHRINE_SIMPLE, SHRINE_EXTRA_KEYS,
    TOWERS_NAMES,
    MEMORIES_NAMES,
    DIVINEBEASTS_NAMES,
    FAIRYFOUNTAINS_NAMES,
    ANCIENTTECHLABS_NAMES,
    CUTSCENES_NAMES,
    HORSES_NAMES,
    NPCS_NAMES,
    RUNES_NAMES,
    SHEIKAHSLATE_NAMES,
    QUICKTIPS_NAMES,
    SIDEQUESTS_NAMES,
    MAINQUESTS_NAMES,
    CHAMPIONPOWERS_NAMES,
    TOWNS_NAMES,
    MASTERSWORD_NAMES,
)


# ---------------------------------------------------------------------------
# FlagProxy — base for sections where all non-integer fields are boolean
# ---------------------------------------------------------------------------

class FlagProxy(EntityProxy):
    """Proxy where non-integer int fields are bool-converted (uint32 != 0 → True)."""

    _integer_fields: frozenset[str] = frozenset()

    def __getattr__(self, name: str):
        val = super().__getattr__(name)
        if isinstance(val, int) and name not in type(self)._integer_fields:
            return bool(val)
        return val


# ---------------------------------------------------------------------------
# Shrines
# ---------------------------------------------------------------------------

class ShrineProxy(FlagProxy):
    """Proxy for a single shrine entity. All fields are boolean."""

    @property
    def is_simple(self) -> bool:
        """True if this shrine has only the standard {active, complete, found, pedestal} fields."""
        c = object.__getattribute__(self, '_c')
        # We can't know the name directly, but we check fields against SHRINE_SIMPLE
        # Use the container's keys minus underscore-prefixed ones
        fields = frozenset(k for k in c.keys() if not k.startswith('_'))
        standard = frozenset({"active", "complete", "found", "pedestal"})
        return (fields - standard) == frozenset()

    @property
    def extra_keys(self) -> frozenset[str]:
        """Extra field names beyond the standard shrine set."""
        c = object.__getattribute__(self, '_c')
        fields = frozenset(k for k in c.keys() if not k.startswith('_'))
        standard = frozenset({"active", "complete", "found", "pedestal"})
        return fields - standard


class ShrineCollection(EntityCollection):
    """Collection of shrine entities."""

    proxy_class = ShrineProxy
    _section_names: list[str] = SHRINES_NAMES

    def simple(self):
        """Yield (name, proxy) for shrines with only standard flags."""
        c = object.__getattribute__(self, '_c')
        for name in SHRINE_SIMPLE:
            if name in c:
                yield name, ShrineProxy(c[name])

    def with_extras(self):
        """Yield (name, proxy, extra_keys) for shrines with non-standard flags."""
        c = object.__getattribute__(self, '_c')
        for name, extra_keys in SHRINE_EXTRA_KEYS.items():
            if name in c:
                yield name, ShrineProxy(c[name]), extra_keys


# ---------------------------------------------------------------------------
# Towers
# ---------------------------------------------------------------------------

class TowerProxy(FlagProxy):
    """Proxy for a single tower entity. All fields are boolean."""
    pass


class TowerCollection(EntityCollection):
    """Collection of tower entities."""

    proxy_class = TowerProxy
    _section_names: list[str] = TOWERS_NAMES


# ---------------------------------------------------------------------------
# Memories
# ---------------------------------------------------------------------------

class MemoryProxy(FlagProxy):
    """Proxy for a single memory entity."""
    pass


class MemoryCollection(EntityCollection):
    """Collection of memory entities."""

    proxy_class = MemoryProxy
    _section_names: list[str] = MEMORIES_NAMES


# ---------------------------------------------------------------------------
# Divine Beasts
# ---------------------------------------------------------------------------

class DivineBeastProxy(FlagProxy):
    """Proxy for a single divine beast entity.

    terminalsremaining is an integer count, not a boolean.
    """

    _integer_fields: frozenset[str] = frozenset({"terminalsremaining"})


class DivineBeastCollection(EntityCollection):
    """Collection of divine beast entities."""

    proxy_class = DivineBeastProxy
    _section_names: list[str] = DIVINEBEASTS_NAMES


# ---------------------------------------------------------------------------
# Fairy Fountains
# ---------------------------------------------------------------------------

class FairyFountainProxy(FlagProxy):
    """Proxy for a single fairy fountain entity."""
    pass


class FairyFountainCollection(EntityCollection):
    """Collection of fairy fountain entities."""

    proxy_class = FairyFountainProxy
    _section_names: list[str] = FAIRYFOUNTAINS_NAMES


# ---------------------------------------------------------------------------
# Ancient Tech Labs
# ---------------------------------------------------------------------------

class AncientTechLabProxy(FlagProxy):
    """Proxy for a single ancient tech lab entity."""
    pass


class AncientTechLabCollection(EntityCollection):
    """Collection of ancient tech lab entities."""

    proxy_class = AncientTechLabProxy
    _section_names: list[str] = ANCIENTTECHLABS_NAMES


# ---------------------------------------------------------------------------
# Cutscenes
# ---------------------------------------------------------------------------

class CutsceneProxy(FlagProxy):
    """Proxy for a single cutscene entity."""
    pass


class CutsceneCollection(EntityCollection):
    """Collection of cutscene entities."""

    proxy_class = CutsceneProxy
    _section_names: list[str] = CUTSCENES_NAMES


# ---------------------------------------------------------------------------
# Horses
# ---------------------------------------------------------------------------

_HORSE_STRING_FIELDS = frozenset({"name", "type", "saddle", "reins", "mane"})


class HorseProxy(EntityProxy):
    """Proxy for a single horse slot entity.

    bond is stored as a float32 bit pattern.
    color and slot are plain integers.
    The stride-8 string fields (name, type, saddle, reins, mane) are not
    mapped in the layout and raise NotImplementedError on access.
    """

    _float_fields: frozenset[str] = frozenset({"bond", "position"})

    def __getattr__(self, name: str):
        if name in _HORSE_STRING_FIELDS:
            raise NotImplementedError("stride-8 encoding not yet implemented")
        return super().__getattr__(name)

    def __setattr__(self, name: str, value) -> None:
        if name in _HORSE_STRING_FIELDS:
            raise NotImplementedError("stride-8 encoding not yet implemented")
        super().__setattr__(name, value)

    @property
    def name(self) -> str:  # type: ignore[override]
        raise NotImplementedError("stride-8 encoding not yet implemented")

    @name.setter
    def name(self, value: str) -> None:
        raise NotImplementedError("stride-8 encoding not yet implemented")

    @property
    def type(self) -> int:  # type: ignore[override]
        raise NotImplementedError("stride-8 encoding not yet implemented")

    @type.setter
    def type(self, value: int) -> None:
        raise NotImplementedError("stride-8 encoding not yet implemented")

    @property
    def saddle(self) -> int:  # type: ignore[override]
        raise NotImplementedError("stride-8 encoding not yet implemented")

    @saddle.setter
    def saddle(self, value: int) -> None:
        raise NotImplementedError("stride-8 encoding not yet implemented")

    @property
    def reins(self) -> int:  # type: ignore[override]
        raise NotImplementedError("stride-8 encoding not yet implemented")

    @reins.setter
    def reins(self, value: int) -> None:
        raise NotImplementedError("stride-8 encoding not yet implemented")

    @property
    def mane(self) -> int:  # type: ignore[override]
        raise NotImplementedError("stride-8 encoding not yet implemented")

    @mane.setter
    def mane(self, value: int) -> None:
        raise NotImplementedError("stride-8 encoding not yet implemented")


class HorseCollection(EntityCollection):
    """Collection of horse slot entities."""

    proxy_class = HorseProxy
    _section_names: list[str] = HORSES_NAMES


# ---------------------------------------------------------------------------
# NPCs
# ---------------------------------------------------------------------------

class NpcProxy(FlagProxy):
    """Proxy for a single NPC entity."""
    pass


class NpcCollection(EntityCollection):
    """Collection of NPC entities."""

    proxy_class = NpcProxy
    _section_names: list[str] = NPCS_NAMES


# ---------------------------------------------------------------------------
# Runes
# ---------------------------------------------------------------------------

class RuneProxy(FlagProxy):
    """Proxy for a single rune entity."""
    pass


class RuneCollection(EntityCollection):
    """Collection of rune entities."""

    proxy_class = RuneProxy
    _section_names: list[str] = RUNES_NAMES


# ---------------------------------------------------------------------------
# Sheikah Slate
# ---------------------------------------------------------------------------

class SheikahSlateProxy(FlagProxy):
    """Proxy for a single Sheikah Slate feature entity."""
    pass


class SheikahSlateCollection(EntityCollection):
    """Collection of Sheikah Slate feature entities."""

    proxy_class = SheikahSlateProxy
    _section_names: list[str] = SHEIKAHSLATE_NAMES


# ---------------------------------------------------------------------------
# Quick Tips
# ---------------------------------------------------------------------------

class QuickTipProxy(FlagProxy):
    """Proxy for a single quick tip entity."""
    pass


class QuickTipCollection(EntityCollection):
    """Collection of quick tip entities."""

    proxy_class = QuickTipProxy
    _section_names: list[str] = QUICKTIPS_NAMES


# ---------------------------------------------------------------------------
# Side Quests
# ---------------------------------------------------------------------------

class SideQuestProxy(FlagProxy):
    """Proxy for a single side quest entity."""
    pass


class SideQuestCollection(EntityCollection):
    """Collection of side quest entities."""

    proxy_class = SideQuestProxy
    _section_names: list[str] = SIDEQUESTS_NAMES


# ---------------------------------------------------------------------------
# Main Quests
# ---------------------------------------------------------------------------

class MainQuestProxy(FlagProxy):
    """Proxy for a single main quest entity.

    memoriesremaining and selected are integer counts, not booleans.
    findthenewmonuments is also an integer counter.
    """

    _integer_fields: frozenset[str] = frozenset({
        "memoriesremaining",
        "selected",
        "findthenewmonuments",
    })


class MainQuestCollection(EntityCollection):
    """Collection of main quest entities."""

    proxy_class = MainQuestProxy
    _section_names: list[str] = MAINQUESTS_NAMES


# ---------------------------------------------------------------------------
# Champion Powers
# ---------------------------------------------------------------------------

class ChampionPowerProxy(EntityProxy):
    """Proxy for a single champion power entity.

    readytimer is a float32.
    uses is an integer count.
    plus is boolean.
    """

    _float_fields: frozenset[str] = frozenset({"readytimer"})

    def __getattr__(self, name: str):
        val = super().__getattr__(name)
        # bool-convert boolean fields (plus)
        if isinstance(val, int) and name not in ("uses",):
            # readytimer is already decoded as float by EntityProxy
            return bool(val)
        return val


class ChampionPowerCollection(EntityCollection):
    """Collection of champion power entities."""

    proxy_class = ChampionPowerProxy
    _section_names: list[str] = CHAMPIONPOWERS_NAMES


# ---------------------------------------------------------------------------
# Towns
# ---------------------------------------------------------------------------

class TownProxy(FlagProxy):
    """Proxy for a single town entity."""
    pass


class TownCollection(EntityCollection):
    """Collection of town entities."""

    proxy_class = TownProxy
    _section_names: list[str] = TOWNS_NAMES


# ---------------------------------------------------------------------------
# Master Sword
# ---------------------------------------------------------------------------

class MasterSwordProxy(FlagProxy):
    """Proxy for a single master sword state entity."""
    pass


class MasterSwordCollection(EntityCollection):
    """Collection of master sword state entities."""

    proxy_class = MasterSwordProxy
    _section_names: list[str] = MASTERSWORD_NAMES
