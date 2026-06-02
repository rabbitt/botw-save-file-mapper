"""Per-entity proxy and collection subclasses for each save section.

Each section has:
  - A *Proxy class: wraps a single entity with type-correct field access.
  - A *Collection class: yields proxies for every entity in the section.

All field access routes through the shared flat FLAT_LAYOUT container;
no nested per-entity sub-containers exist.

Horse string fields (name, type, saddle, reins, mane) use stride-8 encoding
not yet implemented and raise NotImplementedError on get and set.
"""

from __future__ import annotations

import construct as cs

from .base import EntityProxy, EntityCollection
from ._layout import NAMES, SHRINE_SIMPLE, SHRINE_EXTRA_KEYS


# ---------------------------------------------------------------------------
# Shrines
# ---------------------------------------------------------------------------

class ShrineProxy(EntityProxy):
    """Proxy for a single shrine entity. All fields are boolean flags."""

    @property
    def is_simple(self) -> bool:
        """True when the shrine has only the standard {active, complete, found, pedestal} fields."""
        flds = object.__getattribute__(self, '_flds')
        standard = frozenset({"active", "complete", "found", "pedestal"})
        return frozenset(flds) <= standard

    @property
    def extra_keys(self) -> frozenset[str]:
        """Field names beyond the standard shrine set."""
        flds = object.__getattribute__(self, '_flds')
        standard = frozenset({"active", "complete", "found", "pedestal"})
        return frozenset(flds) - standard


class ShrineCollection(EntityCollection):
    proxy_class = ShrineProxy
    _section_names: list[str] = NAMES["shrines"]

    def simple(self):
        """Yield (name, proxy) for shrines with only standard flags."""
        info = object.__getattribute__(self, '_info')
        flat = object.__getattribute__(self, '_flat')
        for name in SHRINE_SIMPLE:
            if name in info:
                yield name, ShrineProxy(flat, info[name])

    def with_extras(self):
        """Yield (name, proxy, extra_keys) for shrines with non-standard flags."""
        info = object.__getattribute__(self, '_info')
        flat = object.__getattribute__(self, '_flat')
        for name, extra_keys in SHRINE_EXTRA_KEYS.items():
            if name in info:
                yield name, ShrineProxy(flat, info[name]), extra_keys


# ---------------------------------------------------------------------------
# Towers
# ---------------------------------------------------------------------------

class TowerProxy(EntityProxy):
    pass


class TowerCollection(EntityCollection):
    proxy_class = TowerProxy
    _section_names: list[str] = NAMES["towers"]


# ---------------------------------------------------------------------------
# Memories
# ---------------------------------------------------------------------------

class MemoryProxy(EntityProxy):
    pass


class MemoryCollection(EntityCollection):
    proxy_class = MemoryProxy
    _section_names: list[str] = NAMES["memories"]


# ---------------------------------------------------------------------------
# Divine Beasts
# ---------------------------------------------------------------------------

class DivineBeastProxy(EntityProxy):
    pass


class DivineBeastCollection(EntityCollection):
    proxy_class = DivineBeastProxy
    _section_names: list[str] = NAMES["divinebeasts"]


# ---------------------------------------------------------------------------
# Fairy Fountains
# ---------------------------------------------------------------------------

class FairyFountainProxy(EntityProxy):
    pass


class FairyFountainCollection(EntityCollection):
    proxy_class = FairyFountainProxy
    _section_names: list[str] = NAMES["fairyfountains"]


# ---------------------------------------------------------------------------
# Ancient Tech Labs
# ---------------------------------------------------------------------------

class AncientTechLabProxy(EntityProxy):
    pass


class AncientTechLabCollection(EntityCollection):
    proxy_class = AncientTechLabProxy
    _section_names: list[str] = NAMES["ancienttechlabs"]


# ---------------------------------------------------------------------------
# Cutscenes
# ---------------------------------------------------------------------------

class CutsceneProxy(EntityProxy):
    pass


class CutsceneCollection(EntityCollection):
    proxy_class = CutsceneProxy
    _section_names: list[str] = NAMES["cutscenes"]


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

    _float_fields: frozenset[str] = frozenset({"bond"})

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
    proxy_class = HorseProxy
    _section_names: list[str] = NAMES["horses"]


# ---------------------------------------------------------------------------
# NPCs
# ---------------------------------------------------------------------------

class NpcProxy(EntityProxy):
    pass


class NpcCollection(EntityCollection):
    proxy_class = NpcProxy
    _section_names: list[str] = NAMES["npcs"]


# ---------------------------------------------------------------------------
# Runes
# ---------------------------------------------------------------------------

class RuneProxy(EntityProxy):
    pass


class RuneCollection(EntityCollection):
    proxy_class = RuneProxy
    _section_names: list[str] = NAMES["runes"]


# ---------------------------------------------------------------------------
# Sheikah Slate
# ---------------------------------------------------------------------------

class SheikahSlateProxy(EntityProxy):
    pass


class SheikahSlateCollection(EntityCollection):
    proxy_class = SheikahSlateProxy
    _section_names: list[str] = NAMES["sheikahslate"]


# ---------------------------------------------------------------------------
# Quick Tips
# ---------------------------------------------------------------------------

class QuickTipProxy(EntityProxy):
    pass


class QuickTipCollection(EntityCollection):
    proxy_class = QuickTipProxy
    _section_names: list[str] = NAMES["quicktips"]


# ---------------------------------------------------------------------------
# Side Quests
# ---------------------------------------------------------------------------

class SideQuestProxy(EntityProxy):
    pass


class SideQuestCollection(EntityCollection):
    proxy_class = SideQuestProxy
    _section_names: list[str] = NAMES["sidequests"]


# ---------------------------------------------------------------------------
# Main Quests
# ---------------------------------------------------------------------------

class MainQuestProxy(EntityProxy):
    pass


class MainQuestCollection(EntityCollection):
    proxy_class = MainQuestProxy
    _section_names: list[str] = NAMES["mainquests"]


# ---------------------------------------------------------------------------
# Champion Powers
# ---------------------------------------------------------------------------

class ChampionPowerProxy(EntityProxy):
    """Proxy for a single champion power entity.

    readytimer is a float32; uses is an integer count; plus is boolean.
    """

    _float_fields: frozenset[str] = frozenset({"readytimer"})


class ChampionPowerCollection(EntityCollection):
    proxy_class = ChampionPowerProxy
    _section_names: list[str] = NAMES["championpowers"]


# ---------------------------------------------------------------------------
# Towns
# ---------------------------------------------------------------------------

class TownProxy(EntityProxy):
    pass


class TownCollection(EntityCollection):
    proxy_class = TownProxy
    _section_names: list[str] = NAMES["towns"]


# ---------------------------------------------------------------------------
# Master Sword
# ---------------------------------------------------------------------------

class MasterSwordProxy(EntityProxy):
    pass


class MasterSwordCollection(EntityCollection):
    proxy_class = MasterSwordProxy
    _section_names: list[str] = NAMES["mastersword"]
