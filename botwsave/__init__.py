"""botwsave — BotW Wii U save file reader/writer.

Quick start::

    from botwsave import SaveFile

    with SaveFile("game_data.sav") as save:
        print(save.get_flag("shrines.akhvaquot.complete"))
        save.set_flag("shrines.akhvaquot.found", True)
        save.set_flag("shrines.akhvaquot.active", True)
        save.set_flag("shrines.akhvaquot.complete", True)
        save.set_flag("shrines.akhvaquot.pedestal.on", True)
"""

from ._save import SaveFile, FlagReadError, FlagWriteError
from ._effectmap import EffectMap, DependencyGraph, DependencyResult, EffectNode, Entry
from ._config import Config

__all__ = [
    "SaveFile",
    "FlagReadError",
    "FlagWriteError",
    "EffectMap",
    "DependencyGraph",
    "DependencyResult",
    "EffectNode",
    "Entry",
    "Config",
]
