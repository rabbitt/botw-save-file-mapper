"""SaveFile: high-level read/write API over the BotW Wii U binary save file."""

from __future__ import annotations

import struct
from pathlib import Path
from typing import Any

from ._binary import BinaryFile
from ._effectmap import EffectMap, EffectNode, DependencyGraph, DependencyResult


class FlagReadError(Exception):
    pass


class FlagWriteError(Exception):
    pass


class SaveFile:
    """Read and write flags in a BotW Wii U save file.

    Usage::

        with SaveFile("game_data.sav") as save:
            print(save.get_flag("shrines.akhvaquot.complete"))
            save.set_flag("shrines.akhvaquot.complete", True)
            # writes are flushed on clean __exit__
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
        self._binary: BinaryFile | None = None
        self._pending: list[tuple[int, int]] = []  # (offset, uint32_value)

    def __enter__(self) -> "SaveFile":
        self._binary = BinaryFile(self.path, readonly=self.readonly)
        self._binary.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._binary is not None:
            self._binary.__exit__(exc_type, exc_val, exc_tb)
            self._binary = None

    def _require_open(self) -> BinaryFile:
        if self._binary is None:
            raise RuntimeError("SaveFile not open — use as context manager")
        return self._binary

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_flag(self, keypath: str) -> Any:
        """Read a flag value from the save file. Returns bool, int, or float."""
        bf = self._require_open()
        node = self._effectmap.get(keypath)
        if node is None:
            raise FlagReadError(f"Unknown keypath: {keypath!r}")
        if not node.entries:
            raise FlagReadError(f"No entries for keypath: {keypath!r}")

        entry = node.entries[0]
        if isinstance(entry.value, bool):
            raw = bf.read_uint32(entry.offset)
            return raw == 1
        elif entry.value == "float":
            return bf.read_float(entry.offset)
        elif entry.value == "integer":
            return bf.read_uint32(entry.offset)
        elif entry.value == "ascii":
            return bf.read_ascii(entry.offset, 32)
        elif entry.value == "utf8":
            return bf.read_utf8(entry.offset, 64)
        else:
            return bf.read_uint32(entry.offset)

    def set_flag(self, keypath: str, value: Any, *, unsafe: bool = False) -> None:
        """Write a flag directly to the save file.

        Only writes the exact offsets for this keypath — no dependency cascade.
        Raises FlagWriteError if the keypath is a known danger key and unsafe=False.
        """
        if not unsafe:
            result = self._deps.check_safe(keypath, include_soft=False)
            if not result.is_safe:
                raise FlagWriteError(
                    f"Refused: {keypath!r} would implicate danger keys "
                    f"{result.danger_hits}. Pass unsafe=True to override."
                )

        bf = self._require_open()
        node = self._effectmap.get(keypath)
        if node is None:
            raise FlagWriteError(f"Unknown keypath: {keypath!r}")
        if not node.entries:
            return  # meta-entry, nothing to write

        for entry in node.entries:
            if self.dry_run:
                continue
            if isinstance(entry.value, bool):
                bf.write_uint32(entry.offset, 1 if value else 0)
            elif entry.value == "float":
                bf.write_float(entry.offset, float(value))
            elif entry.value == "integer":
                bf.write_uint32(entry.offset, int(value))
            elif entry.value == "ascii":
                bf.write_ascii(entry.offset, str(value), 32)
            elif entry.value == "utf8":
                bf.write_utf8(entry.offset, str(value), 64)
            else:
                bf.write_uint32(entry.offset, int(value))

    def check_safe(self, keypath: str, *, include_soft: bool = True) -> DependencyResult:
        """Return dependency analysis for keypath without writing anything."""
        return self._deps.check_safe(keypath, include_soft=include_soft)

    def get_dependencies(self, keypath: str, *, include_soft: bool = True) -> DependencyResult:
        """Alias for check_safe for readability."""
        return self.check_safe(keypath, include_soft=include_soft)

    def search_flags(self, pattern: str) -> list[str]:
        """Return all known keypaths matching a regex pattern."""
        return self._effectmap.search(pattern)

    @property
    def effectmap(self) -> EffectMap:
        return self._effectmap

    @property
    def deps(self) -> DependencyGraph:
        return self._deps
