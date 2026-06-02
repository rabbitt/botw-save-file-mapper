"""Encoders and decoders for BotW save file values.

All float encoding writes into the big-endian uint32 slot that BinaryFile
already manages. The helpers here convert between Python values and the
uint32 patterns the save file expects.
"""

from __future__ import annotations

import struct


# ---------------------------------------------------------------------------
# Float32 ↔ uint32
# ---------------------------------------------------------------------------

def float_to_bits(value: float) -> int:
    """Pack a float32 into its big-endian uint32 bit pattern."""
    return struct.unpack(">I", struct.pack(">f", float(value)))[0]


def bits_to_float(bits: int) -> float:
    """Unpack a uint32 bit pattern as a float32."""
    return struct.unpack(">f", struct.pack(">I", bits & 0xFFFFFFFF))[0]


def bits_to_int(bits: int) -> int:
    """Decode a uint32 float32 bit pattern to its nearest integer value."""
    return int(bits_to_float(bits))


def int_to_bits(value: int) -> int:
    """Encode an integer as float32 bit pattern (used for quarter-hearts, etc.)."""
    return float_to_bits(float(value))


# ---------------------------------------------------------------------------
# Time of day  ("HH:MM AM/PM" ↔ quarter-hour count stored as uint32)
# ---------------------------------------------------------------------------

def encode_time_of_day(time_str: str) -> int:
    """Convert '08:00 AM' style string to the quarter-hour integer the save uses."""
    if ":" not in str(time_str):
        return int(time_str)
    parts = str(time_str).strip().split()
    ampm = parts[1].upper() if len(parts) > 1 else "AM"
    h, m = (int(x) for x in parts[0].split(":"))
    if ampm == "PM" and h != 12:
        h += 12
    elif ampm == "AM" and h == 12:
        h = 0
    return round((h * 60 + m) / 4.0)


def decode_time_of_day(value: int | float) -> str:
    """Convert the quarter-hour integer to '08:00 AM' style string."""
    raw_minutes = int(value) * 4
    minutes = round((raw_minutes % 60 - 1) / 5) * 5 if raw_minutes % 60 else 0
    raw_hours = raw_minutes // 60
    if raw_hours == 12:
        hours, ampm = 12, "PM"
    elif raw_hours > 12:
        hours, ampm = raw_hours - 12, "PM"
    elif raw_hours == 0:
        hours, ampm = 12, "AM"
    else:
        hours, ampm = raw_hours, "AM"
    return f"{hours:02d}:{minutes:02d} {ampm}"


# ---------------------------------------------------------------------------
# Duration  ("MM:SS" or "HH:MM:SS" ↔ float32 bits encoding total seconds)
# ---------------------------------------------------------------------------

def encode_duration(time_str: str) -> int:
    """Convert 'MM:SS' or 'HH:MM:SS' to float32-bits encoding total seconds."""
    if ":" not in str(time_str):
        return int_to_bits(int(time_str))
    parts = list(reversed([int(x) for x in str(time_str).split(":")]))
    total = (parts[0] if len(parts) > 0 else 0) \
          + (parts[1] if len(parts) > 1 else 0) * 60 \
          + (parts[2] if len(parts) > 2 else 0) * 3600
    return int_to_bits(total)


def decode_duration(bits: int) -> str:
    """Convert float32-bits encoding total seconds to 'MM:SS' or 'HH:MM:SS'."""
    total = bits_to_int(bits)
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


# ---------------------------------------------------------------------------
# Blood moon counter  (HH:MM:SS integer seconds ↔ uint32)
# Plain integer, no float encoding needed.
# ---------------------------------------------------------------------------

def encode_hms(time_str: str) -> int:
    """Convert 'HH:MM:SS' or 'MM:SS' to total seconds (plain uint32)."""
    if ":" not in str(time_str):
        return int(time_str)
    parts = list(reversed([int(x) for x in str(time_str).split(":")]))
    return (parts[0] if len(parts) > 0 else 0) \
         + (parts[1] if len(parts) > 1 else 0) * 60 \
         + (parts[2] if len(parts) > 2 else 0) * 3600


def decode_hms(total_seconds: int | float) -> str:
    """Convert total seconds to 'HH:MM:SS' or 'MM:SS'."""
    total_seconds = int(total_seconds)
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"
