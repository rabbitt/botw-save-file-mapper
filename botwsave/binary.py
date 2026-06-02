"""Big-endian binary I/O for Wii U BotW save files (PowerPC, big-endian uint32)."""

import struct
from pathlib import Path


UINT32 = struct.Struct(">I")
FLOAT32 = struct.Struct(">f")
SAVE_SIZE = 1_027_200


class BinaryFile:
    def __init__(self, path: str | Path, readonly: bool = False):
        self.path = Path(path)
        self.readonly = readonly
        self._data: bytearray | None = None

    def __enter__(self):
        raw = self.path.read_bytes()
        self._data = bytearray(raw)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None and not self.readonly and self._data is not None:
            self.path.write_bytes(self._data)
        self._data = None

    def _check(self, offset: int) -> None:
        if self._data is None:
            raise RuntimeError("BinaryFile not open — use as context manager")
        if offset < 0 or offset + 4 > len(self._data):
            raise ValueError(f"Offset 0x{offset:08x} out of range (file size {len(self._data)})")

    def read_uint32(self, offset: int) -> int:
        self._check(offset)
        return UINT32.unpack_from(self._data, offset)[0]

    def write_uint32(self, offset: int, value: int) -> None:
        self._check(offset)
        UINT32.pack_into(self._data, offset, value & 0xFFFFFFFF)

    def read_float(self, offset: int) -> float:
        self._check(offset)
        return FLOAT32.unpack_from(self._data, offset)[0]

    def write_float(self, offset: int, value: float) -> None:
        self._check(offset)
        FLOAT32.pack_into(self._data, offset, value)

    def read_ascii(self, offset: int, length: int) -> str:
        if self._data is None:
            raise RuntimeError("BinaryFile not open")
        raw = self._data[offset : offset + length]
        return raw.rstrip(b"\x00").decode("ascii", errors="replace")

    def write_ascii(self, offset: int, value: str, length: int) -> None:
        if self._data is None:
            raise RuntimeError("BinaryFile not open")
        encoded = value.encode("ascii")[:length]
        self._data[offset : offset + length] = encoded.ljust(length, b"\x00")

    def read_utf8(self, offset: int, length: int) -> str:
        if self._data is None:
            raise RuntimeError("BinaryFile not open")
        raw = self._data[offset : offset + length]
        return raw.rstrip(b"\x00").decode("utf-8", errors="replace")

    def write_utf8(self, offset: int, value: str, length: int) -> None:
        if self._data is None:
            raise RuntimeError("BinaryFile not open")
        encoded = value.encode("utf-8")[:length]
        self._data[offset : offset + length] = encoded.ljust(length, b"\x00")
