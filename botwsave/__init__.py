"""botwsave — BotW Wii U save file reader/writer.

Quick start::

    from botwsave import SaveFile

    with SaveFile("game_data.sav") as save:
        # Individual flag access
        print(save.get_flag("shrines.akhvaquot.complete"))
        save.set_flag("shrines.akhvaquot.complete", True)

        # Model-level access
        stats = save.read_stats()
        stats.rupees = 9999
        save.write_stats(stats)

        inv = save.read_inventory()
        print(inv.weapons)

        # Full save JSON export/import (safe — no soft-dep cascade)
        save.export_json("backup.json")
        save.import_json("backup.json")
"""

from .save import (
    SaveFile,
    FlagReadError,
    FlagWriteError,
    Stats,
    Clock,
    BloodMoon,
    Runes,
    RuneState,
    FairyFountains,
    FairyFountain,
    Horses,
    HorseData,
)
from .effectmap import EffectMap, DependencyGraph, DependencyResult, EffectNode, Entry
from .inventory import (
    Inventory,
    WeaponItem,
    BowItem,
    ArrowItem,
    ShieldItem,
    ArmorItem,
    MaterialItem,
    FoodItem,
    KeyItem,
    FoodBonus,
    ItemBonus,
    WeaponBonus,
    BowBonus,
    ShieldBonus,
    FoodBonusType,
    DyeColor,
    read_inventory,
    write_inventory,
    inventory_from_dict,
)
from .config import Config

__all__ = [
    # Core
    "SaveFile", "FlagReadError", "FlagWriteError",
    # Model objects
    "Stats", "Clock", "BloodMoon", "Runes", "RuneState",
    "FairyFountains", "FairyFountain", "Horses", "HorseData",
    # Inventory
    "Inventory", "WeaponItem", "BowItem", "ArrowItem", "ShieldItem",
    "ArmorItem", "MaterialItem", "FoodItem", "KeyItem",
    "FoodBonus", "ItemBonus",
    "WeaponBonus", "BowBonus", "ShieldBonus", "FoodBonusType", "DyeColor",
    "read_inventory", "write_inventory", "inventory_from_dict",
    # Effectmap
    "EffectMap", "DependencyGraph", "DependencyResult", "EffectNode", "Entry",
    # Config
    "Config",
]
