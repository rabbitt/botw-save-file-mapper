"""Binary layout constants for BotW Wii U save file (game_data.sav)."""


# Item slots: consecutive 128-byte blocks, starting at base offset
SLOTS_BASE = 0x060408
SLOT_WIDTH = 128
SLOT_UINT32S = SLOT_WIDTH // 8  # 16 uint32 values per slot

# Quantities (durability for weapons/bows/shields, quantity for consumables, dye for armor)
QUANTITIES_BASE = 0x000711C8
QUANTITIES_WIDTH = 8

# Equipped flag per slot
EQUIPPED_BASE = 0x00080D70
EQUIPPED_WIDTH = 8

# Weapon/bow/shield bonus type (category-specific bases)
WEAPON_BONUS_TYPE_BASE = 0x0005DD20
BOW_BONUS_TYPE_BASE = 0x00004990
SHIELD_BONUS_TYPE_BASE = 0x000D1038
BONUS_TYPE_WIDTH = 8

# Weapon/bow/shield bonus amount
WEAPON_BONUS_AMOUNT_BASE = 0x000C4C68
BOW_BONUS_AMOUNT_BASE = 0x0000B1E0
SHIELD_BONUS_AMOUNT_BASE = 0x00071098
BONUS_AMOUNT_WIDTH = 8

# Food properties — each array entry is 16 bytes wide
FOOD_WIDTH = 16
FOOD_HEARTS_BASE = 0x000DCD90
FOOD_DURATION_BASE = 0x000DCD98
FOOD_BONUS_TYPE_BASE = 0x000FA6B0
FOOD_BONUS_AMOUNT_BASE = 0x000FA6B8

# Stash size counters (max slots for each weapon category)
WEAPON_STASH_OFFSET = 0x00085048
BOW_STASH_OFFSET = 0x000E3348
SHIELD_STASH_OFFSET = 0x00048CD8

# Item type markers used to detect category boundaries
ITEM_TYPE_TWOHANDED = 1869504332
ITEM_TYPE_MELEE_OTHER = 1869504339
ITEM_TYPE_BOW = 1869504322
ITEM_TYPE_STASHABLE = 1466261872  # shields and most other stashable items
ITEM_TYPE_ARMOR = 1098018159


# Array bounds for construct-based flat parsing (generous upper bounds)
MAX_INV_SLOTS    = 539   # (QUANTITIES_BASE - SLOTS_BASE) // SLOT_WIDTH
MAX_WEAPON_BONUS = 120
MAX_BOW_BONUS    = 30
MAX_SHIELD_BONUS = 30
MAX_FOOD_ITEMS   = 60


_BONUS_TYPE_BASES = {
    "weapons": WEAPON_BONUS_TYPE_BASE,
    "bows": BOW_BONUS_TYPE_BASE,
    "shields": SHIELD_BONUS_TYPE_BASE,
}

_BONUS_AMOUNT_BASES = {
    "weapons": WEAPON_BONUS_AMOUNT_BASE,
    "bows": BOW_BONUS_AMOUNT_BASE,
    "shields": SHIELD_BONUS_AMOUNT_BASE,
}


def slot_offset(slot: int) -> int:
    return SLOTS_BASE + slot * SLOT_WIDTH


def quantity_offset(slot: int) -> int:
    return QUANTITIES_BASE + slot * QUANTITIES_WIDTH


def equipped_offset(slot: int) -> int:
    return EQUIPPED_BASE + slot * EQUIPPED_WIDTH


def bonus_type_offset(slot_in_category: int, category: str) -> int:
    return _BONUS_TYPE_BASES[category] + slot_in_category * BONUS_TYPE_WIDTH


def bonus_amount_offset(slot_in_category: int, category: str) -> int:
    return _BONUS_AMOUNT_BASES[category] + slot_in_category * BONUS_AMOUNT_WIDTH


def food_hearts_offset(slot_in_category: int) -> int:
    return FOOD_HEARTS_BASE + slot_in_category * FOOD_WIDTH


def food_duration_offset(slot_in_category: int) -> int:
    return FOOD_DURATION_BASE + slot_in_category * FOOD_WIDTH


def food_bonus_type_offset(slot_in_category: int) -> int:
    return FOOD_BONUS_TYPE_BASE + slot_in_category * FOOD_WIDTH


def food_bonus_amount_offset(slot_in_category: int) -> int:
    return FOOD_BONUS_AMOUNT_BASE + slot_in_category * FOOD_WIDTH
