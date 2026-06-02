"""Construct Pointer-backed binary I/O for the BotW Wii U save file.

Reads are served from a bytearray loaded once on open — fast random access,
no seek overhead for inventory slot parsing.

Writes go through construct.Pointer(offset, subcon).build_stream() directly
to the open r+b file handle. Only the exact bytes targeted are ever written;
the rest of the file is never touched. A no-op round-trip is byte-identical
by construction, not by correctness of a full schema definition.
"""

from __future__ import annotations

import struct
from pathlib import Path
from typing import TYPE_CHECKING

import construct as cs

from .codecs import float_to_bits, bits_to_float

if TYPE_CHECKING:
    from .effectmap import EffectMap


class BinaryFile:
    def __init__(
        self,
        path: str | Path,
        effectmap: "EffectMap",  # API compat; Pointer approach is schema-free
        readonly: bool = False,
    ):
        self.path = Path(path)
        self.readonly = readonly
        self._data: bytearray | None = None
        self._fh = None  # r+b handle; None in readonly/dry-run mode

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "BinaryFile":
        raw = self.path.read_bytes()
        self._data = bytearray(raw)
        if not self.readonly:
            self._fh = self.path.open("r+b")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._fh is not None:
            self._fh.close()
            self._fh = None
        self._data = None

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _require(self) -> bytearray:
        if self._data is None:
            raise RuntimeError("BinaryFile not open — use as context manager")
        return self._data

    # ------------------------------------------------------------------
    # Reads — served from bytearray, no file I/O after open
    # ------------------------------------------------------------------

    def read_uint32(self, offset: int) -> int:
        return struct.unpack_from(">I", self._require(), offset)[0]

    def read_float(self, offset: int) -> float:
        return bits_to_float(self.read_uint32(offset))

    def read_ascii(self, offset: int, length: int) -> str:
        d = self._require()
        return d[offset:offset + length].rstrip(b"\x00").decode("ascii", errors="replace")

    def read_utf8(self, offset: int, length: int) -> str:
        d = self._require()
        return d[offset:offset + length].rstrip(b"\x00").decode("utf-8", errors="replace")

    # ------------------------------------------------------------------
    # Writes — Pointer(offset, subcon).build_stream writes only the
    # targeted bytes. Bytearray is also updated so reads stay consistent.
    # ------------------------------------------------------------------

    def write_uint32(self, offset: int, value: int) -> None:
        v = value & 0xFFFFFFFF
        d = self._require()
        if struct.unpack_from(">I", d, offset)[0] == v:
            return  # no change — preserve exact original bytes
        struct.pack_into(">I", d, offset, v)
        if self._fh is not None:
            cs.Pointer(offset, cs.Int32ub).build_stream(v, self._fh)

    def write_float(self, offset: int, value: float) -> None:
        self.write_uint32(offset, float_to_bits(value))

    def write_ascii(self, offset: int, value: str, length: int) -> None:
        encoded = value.encode("ascii", errors="replace")[:length]
        self._write_bytes(offset, encoded + b"\x00" * (length - len(encoded)))

    def write_utf8(self, offset: int, value: str, length: int) -> None:
        encoded = value.encode("utf-8", errors="replace")[:length]
        self._write_bytes(offset, encoded + b"\x00" * (length - len(encoded)))

    def _write_bytes(self, offset: int, data: bytes) -> None:
        d = self._require()
        d[offset:offset + len(data)] = data
        if self._fh is not None:
            cs.Pointer(offset, cs.Bytes(len(data))).build_stream(data, self._fh)
