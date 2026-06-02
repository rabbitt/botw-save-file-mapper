"""Construct-backed binary I/O for the BotW Wii U save file.

The entire file is parsed into a construct Container on open. Named fields
map to effectmap-documented offsets; all gaps are Bytes that round-trip
verbatim. Arbitrary offset reads/writes (used by inventory parsing) locate the
covering gap field via binary search and mutate its bytes in-place, so every
change — named or raw — flows through the single Container that build() uses.
"""

from __future__ import annotations

import bisect
import struct
from pathlib import Path
from typing import TYPE_CHECKING

from .codecs import float_to_bits, bits_to_float
from .layout import get_file_struct, build_file_struct, FILE_SIZE

if TYPE_CHECKING:
    from .effectmap import EffectMap

_UINT32_BE = struct.Struct(">I")


class BinaryFile:
    def __init__(
        self,
        path: str | Path,
        effectmap: "EffectMap",
        readonly: bool = False,
    ):
        self.path = Path(path)
        self.readonly = readonly
        self._effectmap_raw = effectmap._raw
        self._schema = get_file_struct(effectmap._raw)
        self._container = None
        self._named: dict[int, str] = {}    # offset → field name for named fields
        self._gap_starts: list[int] = []    # sorted gap start offsets
        self._gap_info: list[tuple[int, int, str]] = []  # (start, end, name) per gap

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "BinaryFile":
        raw = self.path.read_bytes()
        if len(raw) != FILE_SIZE:
            self._schema = build_file_struct(self._effectmap_raw, file_size=len(raw))
        self._container = self._schema.parse(raw)
        self._build_layout()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None and not self.readonly and self._container is not None:
            data = self._schema.build(self._container)
            self.path.write_bytes(data)
        self._container = None
        self._named = {}
        self._gap_starts = []
        self._gap_info = []

    # ------------------------------------------------------------------
    # Layout index — built once per open()
    # ------------------------------------------------------------------

    def _build_layout(self) -> None:
        """Index all subcons so we can find any offset in O(log n)."""
        named: dict[int, str] = {}
        gaps: list[tuple[int, int, str]] = []

        for sc in self._schema.subcons:
            name = sc.name
            size = sc.subcon.length  # Int32ub=4, Float32b=4, Bytes(n)=n
            if name.startswith("f") and len(name) == 9:
                off = int(name[1:], 16)
                named[off] = name
            elif name.startswith("_g"):
                off = int(name[2:], 16)
                gaps.append((off, off + size, name))

        self._named = named
        self._gap_info = gaps
        self._gap_starts = [g[0] for g in gaps]

    def _find_gap(self, offset: int) -> tuple[int, int, str]:
        """Return the (start, end, name) gap field that contains offset."""
        idx = bisect.bisect_right(self._gap_starts, offset) - 1
        if idx >= 0:
            g = self._gap_info[idx]
            if g[0] <= offset < g[1]:
                return g
        raise KeyError(f"Offset 0x{offset:08x} not covered by schema")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _require(self):
        if self._container is None:
            raise RuntimeError("BinaryFile not open — use as context manager")
        return self._container

    # ------------------------------------------------------------------
    # Typed field access
    # ------------------------------------------------------------------

    def read_uint32(self, offset: int) -> int:
        c = self._require()
        if offset in self._named:
            return int(c[self._named[offset]])
        # offset is inside a gap Bytes field
        start, _, name = self._find_gap(offset)
        return _UINT32_BE.unpack_from(c[name], offset - start)[0]

    def write_uint32(self, offset: int, value: int) -> None:
        c = self._require()
        if offset in self._named:
            c[self._named[offset]] = value & 0xFFFFFFFF
            return
        start, _, name = self._find_gap(offset)
        ba = bytearray(c[name])
        _UINT32_BE.pack_into(ba, offset - start, value & 0xFFFFFFFF)
        c[name] = bytes(ba)

    def read_float(self, offset: int) -> float:
        return bits_to_float(self.read_uint32(offset))

    def write_float(self, offset: int, value: float) -> None:
        self.write_uint32(offset, float_to_bits(value))

    def read_ascii(self, offset: int, length: int) -> str:
        raw = self._read_bytes(offset, length)
        return raw.rstrip(b"\x00").decode("ascii", errors="replace")

    def write_ascii(self, offset: int, value: str, length: int) -> None:
        encoded = value.encode("ascii", errors="replace")[:length]
        self._write_bytes(offset, encoded.ljust(length, b"\x00"))

    def read_utf8(self, offset: int, length: int) -> str:
        raw = self._read_bytes(offset, length)
        return raw.rstrip(b"\x00").decode("utf-8", errors="replace")

    def write_utf8(self, offset: int, value: str, length: int) -> None:
        encoded = value.encode("utf-8", errors="replace")[:length]
        self._write_bytes(offset, encoded.ljust(length, b"\x00"))

    # ------------------------------------------------------------------
    # Raw byte access (used by string fields and inventory parsing)
    # ------------------------------------------------------------------

    def _read_bytes(self, offset: int, length: int) -> bytes:
        c = self._require()
        if offset in self._named:
            raw = c[self._named[offset]]
            if isinstance(raw, int):
                raw = raw.to_bytes(4, "big")
            return bytes(raw)
        start, _, name = self._find_gap(offset)
        return bytes(c[name][offset - start : offset - start + length])

    def _write_bytes(self, offset: int, data: bytes) -> None:
        c = self._require()
        if offset in self._named:
            c[self._named[offset]] = data
            return
        start, _, name = self._find_gap(offset)
        ba = bytearray(c[name])
        local = offset - start
        ba[local : local + len(data)] = data
        c[name] = bytes(ba)
