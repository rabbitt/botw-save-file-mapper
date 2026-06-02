# AUTO-GENERATED from botwsave/data/effectmap.yaml — do not edit by hand.
# Regenerate with: python tools/gen_layout.py
# fmt: off

from __future__ import annotations
import construct as cs

# ── Shrines ─────────────────────────────────────────────────────────────────

SHRINES_LAYOUT = cs.Struct(
    "akhvaquot" / cs.Struct(
        "active"   / cs.Pointer(51264, cs.Int32ub),
        "complete" / cs.Pointer(814200, cs.Int32ub),
        "found"    / cs.Pointer(854832, cs.Int32ub),
        "pedestal" / cs.Pointer(844040, cs.Int32ub),
    ),
    "bareedanaag" / cs.Struct(
        "active"    / cs.Pointer(512568, cs.Int32ub),
        "complete"  / cs.Pointer(1016392, cs.Int32ub),
        "found"     / cs.Pointer(553296, cs.Int32ub),
        "pedestal"  / cs.Pointer(813256, cs.Int32ub),
        "unearthed" / cs.Pointer(5416, cs.Int32ub),
    ),
    "boshkala" / cs.Struct(
        "active"   / cs.Pointer(923384, cs.Int32ub),
        "complete" / cs.Pointer(462848, cs.Int32ub),
        "found"    / cs.Pointer(2128, cs.Int32ub),
        "pedestal" / cs.Pointer(48776, cs.Int32ub),
    ),
    "chaasqeta" / cs.Struct(
        "active"   / cs.Pointer(448696, cs.Int32ub),
        "complete" / cs.Pointer(891992, cs.Int32ub),
        "found"    / cs.Pointer(832080, cs.Int32ub),
        "pedestal" / cs.Pointer(893160, cs.Int32ub),
    ),
    "daagchokah" / cs.Struct(
        "active"   / cs.Pointer(805424, cs.Int32ub),
        "complete" / cs.Pointer(67504, cs.Int32ub),
        "found"    / cs.Pointer(336976, cs.Int32ub),
        "pedestal" / cs.Pointer(544040, cs.Int32ub),
    ),
    "dagahkeek" / cs.Struct(
        "active"    / cs.Pointer(24248, cs.Int32ub),
        "complete"  / cs.Pointer(526624, cs.Int32ub),
        "found"     / cs.Pointer(933384, cs.Int32ub),
        "pedestal"  / cs.Pointer(1023808, cs.Int32ub),
        "unearthed" / cs.Pointer(34336, cs.Int32ub),
    ),
    "dahhesho" / cs.Struct(
        "active"   / cs.Pointer(345752, cs.Int32ub),
        "complete" / cs.Pointer(860984, cs.Int32ub),
        "found"    / cs.Pointer(796608, cs.Int32ub),
        "pedestal" / cs.Pointer(858584, cs.Int32ub),
    ),
    "dahkaso" / cs.Struct(
        "active"   / cs.Pointer(901624, cs.Int32ub),
        "complete" / cs.Pointer(382712, cs.Int32ub),
        "found"    / cs.Pointer(333568, cs.Int32ub),
        "pedestal" / cs.Pointer(450000, cs.Int32ub),
    ),
    "dakatuss" / cs.Struct(
        "active"   / cs.Pointer(864920, cs.Int32ub),
        "complete" / cs.Pointer(344568, cs.Int32ub),
        "found"    / cs.Pointer(73720, cs.Int32ub),
        "pedestal" / cs.Pointer(801104, cs.Int32ub),
    ),
    "dakotah" / cs.Struct(
        "active"   / cs.Pointer(843200, cs.Int32ub),
        "complete" / cs.Pointer(302088, cs.Int32ub),
        "found"    / cs.Pointer(387552, cs.Int32ub),
        "pedestal" / cs.Pointer(468232, cs.Int32ub),
    ),
    "daqakoh" / cs.Struct(
        "active"   / cs.Pointer(66952, cs.Int32ub),
        "complete" / cs.Pointer(805736, cs.Int32ub),
        "found"    / cs.Pointer(884448, cs.Int32ub),
        "pedestal" / cs.Pointer(22656, cs.Int32ub),
    ),
    "daqochisay" / cs.Struct(
        "active"   / cs.Pointer(76320, cs.Int32ub),
        "complete" / cs.Pointer(798912, cs.Int32ub),
        "found"    / cs.Pointer(861880, cs.Int32ub),
        "pedestal" / cs.Pointer(820304, cs.Int32ub),
    ),
    "dilamaag" / cs.Struct(
        "active"   / cs.Pointer(915976, cs.Int32ub),
        "complete" / cs.Pointer(473568, cs.Int32ub),
        "found"    / cs.Pointer(11424, cs.Int32ub),
        "pedestal" / cs.Pointer(796728, cs.Int32ub),
    ),
    "downaeh" / cs.Struct(
        "active"   / cs.Pointer(39424, cs.Int32ub),
        "complete" / cs.Pointer(562752, cs.Int32ub),
        "found"    / cs.Pointer(1026720, cs.Int32ub),
        "pedestal" / cs.Pointer(461992, cs.Int32ub),
    ),
    "dunbataag" / cs.Struct(
        "active"   / cs.Pointer(482696, cs.Int32ub),
        "complete" / cs.Pointer(1018216, cs.Int32ub),
        "found"    / cs.Pointer(554296, cs.Int32ub),
        "pedestal" / cs.Pointer(1015776, cs.Int32ub),
    ),
    "etsukorima" / cs.Struct(
        "active"      / cs.Pointer(802504, cs.Int32ub),
        "complete"    / cs.Pointer(69896, cs.Int32ub),
        "found"       / cs.Pointer(340000, cs.Int32ub),
        "monsterbase" / cs.Pointer(458504, cs.Int32ub),
        "pedestal"    / cs.Pointer(50008, cs.Int32ub),
        "unearthed"   / cs.Pointer(17192, cs.Int32ub),
    ),
    "geeharah" / cs.Struct(
        "active"   / cs.Pointer(934016, cs.Int32ub),
        "complete" / cs.Pointer(456128, cs.Int32ub),
        "found"    / cs.Pointer(17880, cs.Int32ub),
        "pedestal" / cs.Pointer(849744, cs.Int32ub),
    ),
    "gomaasaagh" / cs.Struct(
        "active"   / cs.Pointer(385608, cs.Int32ub),
        "complete" / cs.Pointer(898864, cs.Int32ub),
        "found"    / cs.Pointer(846688, cs.Int32ub),
        "pedestal" / cs.Pointer(549304, cs.Int32ub),
    ),
    "goraetorr" / cs.Struct(
        "active"   / cs.Pointer(913032, cs.Int32ub),
        "complete" / cs.Pointer(361360, cs.Int32ub),
        "found"    / cs.Pointer(326192, cs.Int32ub),
        "pedestal" / cs.Pointer(381464, cs.Int32ub),
    ),
    "hadahamar" / cs.Struct(
        "active"   / cs.Pointer(471200, cs.Int32ub),
        "complete" / cs.Pointer(918920, cs.Int32ub),
        "found"    / cs.Pointer(543880, cs.Int32ub),
        "pedestal" / cs.Pointer(894664, cs.Int32ub),
    ),
    "hawakoth" / cs.Struct(
        "active"   / cs.Pointer(914216, cs.Int32ub),
        "complete" / cs.Pointer(472584, cs.Int32ub),
        "found"    / cs.Pointer(9688, cs.Int32ub),
        "pedestal" / cs.Pointer(34056, cs.Int32ub),
    ),
    "hiamiu" / cs.Struct(
        "active"   / cs.Pointer(847632, cs.Int32ub),
        "complete" / cs.Pointer(300776, cs.Int32ub),
        "found"    / cs.Pointer(386400, cs.Int32ub),
        "pedestal" / cs.Pointer(28616, cs.Int32ub),
    ),
    "hilarao" / cs.Struct(
        "active"   / cs.Pointer(302248, cs.Int32ub),
        "complete" / cs.Pointer(843064, cs.Int32ub),
        "found"    / cs.Pointer(896648, cs.Int32ub),
        "pedestal" / cs.Pointer(920384, cs.Int32ub),
    ),
    "ishtosoh" / cs.Struct(
        "active"   / cs.Pointer(382800, cs.Int32ub),
        "complete" / cs.Pointer(901584, cs.Int32ub),
        "found"    / cs.Pointer(819744, cs.Int32ub),
        "pedestal" / cs.Pointer(306568, cs.Int32ub),
    ),
    "jabaij" / cs.Struct(
        "active"   / cs.Pointer(466776, cs.Int32ub),
        "complete" / cs.Pointer(920320, cs.Int32ub),
        "found"    / cs.Pointer(544696, cs.Int32ub),
        "pedestal" / cs.Pointer(384128, cs.Int32ub),
    ),
    "jeenoh" / cs.Struct(
        "active"   / cs.Pointer(21104, cs.Int32ub),
        "complete" / cs.Pointer(525384, cs.Int32ub),
        "found"    / cs.Pointer(931592, cs.Int32ub),
        "pedestal" / cs.Pointer(2232, cs.Int32ub),
    ),
    "jitansami" / cs.Struct(
        "active"    / cs.Pointer(1026920, cs.Int32ub),
        "complete"  / cs.Pointer(477072, cs.Int32ub),
        "found"     / cs.Pointer(39600, cs.Int32ub),
        "pedestal"  / cs.Pointer(821008, cs.Int32ub),
        "unearthed" / cs.Pointer(1013136, cs.Int32ub),
    ),
    "joloonah" / cs.Struct(
        "active"    / cs.Pointer(362664, cs.Int32ub),
        "complete"  / cs.Pointer(908384, cs.Int32ub),
        "found"     / cs.Pointer(824472, cs.Int32ub),
        "pedestal"  / cs.Pointer(509336, cs.Int32ub),
        "unearthed" / cs.Pointer(519104, cs.Int32ub),
    ),
    "kaamyatak" / cs.Struct(
        "active"   / cs.Pointer(44064, cs.Int32ub),
        "complete" / cs.Pointer(557472, cs.Int32ub),
        "found"    / cs.Pointer(1019856, cs.Int32ub),
        "pedestal" / cs.Pointer(873928, cs.Int32ub),
    ),
    "kahmael" / cs.Struct(
        "active"   / cs.Pointer(857920, cs.Int32ub),
        "complete" / cs.Pointer(348672, cs.Int32ub),
        "found"    / cs.Pointer(48424, cs.Int32ub),
        "pedestal" / cs.Pointer(815072, cs.Int32ub),
    ),
    "kahokeo" / cs.Struct(
        "active"   / cs.Pointer(521608, cs.Int32ub),
        "complete" / cs.Pointer(950696, cs.Int32ub),
        "found"    / cs.Pointer(790008, cs.Int32ub),
        "pedestal" / cs.Pointer(843008, cs.Int32ub),
    ),
    "kahyah" / cs.Struct(
        "active"    / cs.Pointer(372664, cs.Int32ub),
        "complete"  / cs.Pointer(907576, cs.Int32ub),
        "found"     / cs.Pointer(822960, cs.Int32ub),
        "pedestal"  / cs.Pointer(42152, cs.Int32ub),
        "unearthed" / cs.Pointer(18768, cs.Int32ub),
    ),
    "kamiaomuna" / cs.Struct(
        "active"    / cs.Pointer(370528, cs.Int32ub),
        "complete"  / cs.Pointer(909520, cs.Int32ub),
        "found"     / cs.Pointer(826344, cs.Int32ub),
        "pedestal"  / cs.Pointer(390432, cs.Int32ub),
        "unearthed" / cs.Pointer(885752, cs.Int32ub),
    ),
    "kamurog" / cs.Struct(
        "active"    / cs.Pointer(459080, cs.Int32ub),
        "complete"  / cs.Pointer(933808, cs.Int32ub),
        "found"     / cs.Pointer(526192, cs.Int32ub),
        "pedestal"  / cs.Pointer(11824, cs.Int32ub),
        "unearthed" / cs.Pointer(821448, cs.Int32ub),
    ),
    "kaomakagh" / cs.Struct(
        "active"   / cs.Pointer(5440, cs.Int32ub),
        "complete" / cs.Pointer(547128, cs.Int32ub),
        "found"    / cs.Pointer(921296, cs.Int32ub),
        "pedestal" / cs.Pointer(899952, cs.Int32ub),
    ),
    "katahchuki" / cs.Struct(
        "active"   / cs.Pointer(817720, cs.Int32ub),
        "complete" / cs.Pointer(50768, cs.Int32ub),
        "found"    / cs.Pointer(349448, cs.Int32ub),
        "pedestal" / cs.Pointer(829776, cs.Int32ub),
    ),
    "katosaaug" / cs.Struct(
        "active"   / cs.Pointer(1016328, cs.Int32ub),
        "complete" / cs.Pointer(512616, cs.Int32ub),
        "found"    / cs.Pointer(47312, cs.Int32ub),
        "pedestal" / cs.Pointer(3416, cs.Int32ub),
    ),
    "kayawan" / cs.Struct(
        "active"   / cs.Pointer(456088, cs.Int32ub),
        "complete" / cs.Pointer(934120, cs.Int32ub),
        "found"    / cs.Pointer(531656, cs.Int32ub),
        "pedestal" / cs.Pointer(1018176, cs.Int32ub),
    ),
    "kaynoh" / cs.Struct(
        "active"   / cs.Pointer(449784, cs.Int32ub),
        "complete" / cs.Pointer(944784, cs.Int32ub),
        "found"    / cs.Pointer(536128, cs.Int32ub),
        "pedestal" / cs.Pointer(373192, cs.Int32ub),
    ),
    "kayramah" / cs.Struct(
        "active"    / cs.Pointer(329072, cs.Int32ub),
        "complete"  / cs.Pointer(826920, cs.Int32ub),
        "found"     / cs.Pointer(909464, cs.Int32ub),
        "pedestal"  / cs.Pointer(10408, cs.Int32ub),
        "unearthed" / cs.Pointer(821168, cs.Int32ub),
    ),
    "keedafunia" / cs.Struct(
        "active"    / cs.Pointer(328768, cs.Int32ub),
        "complete"  / cs.Pointer(824352, cs.Int32ub),
        "found"     / cs.Pointer(909176, cs.Int32ub),
        "pedestal"  / cs.Pointer(453800, cs.Int32ub),
        "unearthed" / cs.Pointer(449040, cs.Int32ub),
    ),
    "keehayoog" / cs.Struct(
        "active"    / cs.Pointer(513896, cs.Int32ub),
        "complete"  / cs.Pointer(1011376, cs.Int32ub),
        "found"     / cs.Pointer(794440, cs.Int32ub),
        "pedestal"  / cs.Pointer(340008, cs.Int32ub),
        "unearthed" / cs.Pointer(477304, cs.Int32ub),
    ),
    "kehnamut" / cs.Struct(
        "active"   / cs.Pointer(448176, cs.Int32ub),
        "complete" / cs.Pointer(892112, cs.Int32ub),
        "found"    / cs.Pointer(831680, cs.Int32ub),
        "pedestal" / cs.Pointer(298608, cs.Int32ub),
    ),
    "keivetala" / cs.Struct(
        "active"    / cs.Pointer(863688, cs.Int32ub),
        "complete"  / cs.Pointer(343056, cs.Int32ub),
        "found"     / cs.Pointer(72736, cs.Int32ub),
        "pedestal"  / cs.Pointer(72808, cs.Int32ub),
        "unearthed" / cs.Pointer(513176, cs.Int32ub),
    ),
    "kemakosassa" / cs.Struct(
        "active"   / cs.Pointer(850808, cs.Int32ub),
        "complete" / cs.Pointer(358280, cs.Int32ub),
        "found"    / cs.Pointer(66392, cs.Int32ub),
        "pedestal" / cs.Pointer(40064, cs.Int32ub),
    ),
    "kemazoos" / cs.Struct(
        "active"   / cs.Pointer(827232, cs.Int32ub),
        "complete" / cs.Pointer(325240, cs.Int32ub),
        "found"    / cs.Pointer(359800, cs.Int32ub),
        "pedestal" / cs.Pointer(806528, cs.Int32ub),
    ),
    "kenaishakah" / cs.Struct(
        "active"   / cs.Pointer(808016, cs.Int32ub),
        "complete" / cs.Pointer(64808, cs.Int32ub),
        "found"    / cs.Pointer(357104, cs.Int32ub),
        "pedestal" / cs.Pointer(40896, cs.Int32ub),
    ),
    "keoruug" / cs.Struct(
        "active"   / cs.Pointer(804136, cs.Int32ub),
        "complete" / cs.Pointer(71512, cs.Int32ub),
        "found"    / cs.Pointer(341016, cs.Int32ub),
        "pedestal" / cs.Pointer(798400, cs.Int32ub),
    ),
    "ketohwawai" / cs.Struct(
        "active"   / cs.Pointer(510888, cs.Int32ub),
        "complete" / cs.Pointer(1015384, cs.Int32ub),
        "found"    / cs.Pointer(551248, cs.Int32ub),
        "pedestal" / cs.Pointer(831744, cs.Int32ub),
    ),
    "kiahtoza" / cs.Struct(
        "active"    / cs.Pointer(343136, cs.Int32ub),
        "complete"  / cs.Pointer(863608, cs.Int32ub),
        "found"     / cs.Pointer(799360, cs.Int32ub),
        "pedestal"  / cs.Pointer(298408, cs.Int32ub),
        "unearthed" / cs.Pointer(459752, cs.Int32ub),
    ),
    "kihiromoh" / cs.Struct(
        "active"    / cs.Pointer(332480, cs.Int32ub),
        "complete"  / cs.Pointer(823240, cs.Int32ub),
        "found"     / cs.Pointer(907160, cs.Int32ub),
        "pedestal"  / cs.Pointer(853792, cs.Int32ub),
        "unearthed" / cs.Pointer(918120, cs.Int32ub),
    ),
    "korguchideh" / cs.Struct(
        "active"   / cs.Pointer(309296, cs.Int32ub),
        "complete" / cs.Pointer(830040, cs.Int32ub),
        "found"    / cs.Pointer(891008, cs.Int32ub),
        "pedestal" / cs.Pointer(328104, cs.Int32ub),
    ),
    "korshohu" / cs.Struct(
        "active"    / cs.Pointer(452152, cs.Int32ub),
        "complete"  / cs.Pointer(945832, cs.Int32ub),
        "found"     / cs.Pointer(538040, cs.Int32ub),
        "pedestal"  / cs.Pointer(801584, cs.Int32ub),
        "unearthed" / cs.Pointer(543032, cs.Int32ub),
    ),
    "kuhnsidajj" / cs.Struct(
        "active"    / cs.Pointer(902440, cs.Int32ub),
        "complete"  / cs.Pointer(381552, cs.Int32ub),
        "found"     / cs.Pointer(334552, cs.Int32ub),
        "pedestal"  / cs.Pointer(47096, cs.Int32ub),
        "unearthed" / cs.Pointer(13096, cs.Int32ub),
    ),
    "kuhtakkar" / cs.Struct(
        "active"   / cs.Pointer(533216, cs.Int32ub),
        "complete" / cs.Pointer(16112, cs.Int32ub),
        "found"    / cs.Pointer(452528, cs.Int32ub),
        "pedestal" / cs.Pointer(337952, cs.Int32ub),
    ),
    "laknarokee" / cs.Struct(
        "active"    / cs.Pointer(550000, cs.Int32ub),
        "complete"  / cs.Pointer(2856, cs.Int32ub),
        "found"     / cs.Pointer(462720, cs.Int32ub),
        "pedestal"  / cs.Pointer(22664, cs.Int32ub),
        "unearthed" / cs.Pointer(72912, cs.Int32ub),
    ),
    "lannokooh" / cs.Struct(
        "active"   / cs.Pointer(524272, cs.Int32ub),
        "complete" / cs.Pointer(948072, cs.Int32ub),
        "found"    / cs.Pointer(566128, cs.Int32ub),
        "pedestal" / cs.Pointer(831248, cs.Int32ub),
    ),
    "maaghalan" / cs.Struct(
        "active"   / cs.Pointer(553416, cs.Int32ub),
        "complete" / cs.Pointer(46696, cs.Int32ub),
        "found"    / cs.Pointer(512672, cs.Int32ub),
        "pedestal" / cs.Pointer(950368, cs.Int32ub),
    ),
    "maagnorah" / cs.Struct(
        "active"   / cs.Pointer(346208, cs.Int32ub),
        "complete" / cs.Pointer(860800, cs.Int32ub),
        "found"    / cs.Pointer(797064, cs.Int32ub),
        "pedestal" / cs.Pointer(844424, cs.Int32ub),
    ),
    "maheliya" / cs.Struct(
        "active"    / cs.Pointer(801568, cs.Int32ub),
        "complete"  / cs.Pointer(73704, cs.Int32ub),
        "found"     / cs.Pointer(345168, cs.Int32ub),
        "pedestal"  / cs.Pointer(514424, cs.Int32ub),
        "unearthed" / cs.Pointer(67704, cs.Int32ub),
    ),
    "makarah" / cs.Struct(
        "active"   / cs.Pointer(480504, cs.Int32ub),
        "complete" / cs.Pointer(1023488, cs.Int32ub),
        "found"    / cs.Pointer(559400, cs.Int32ub),
        "pedestal" / cs.Pointer(942152, cs.Int32ub),
    ),
    "mezzalo" / cs.Struct(
        "active"    / cs.Pointer(354104, cs.Int32ub),
        "complete"  / cs.Pointer(853088, cs.Int32ub),
        "found"     / cs.Pointer(810416, cs.Int32ub),
        "pedestal"  / cs.Pointer(808184, cs.Int32ub),
        "unearthed" / cs.Pointer(833160, cs.Int32ub),
    ),
    "mijahrokee" / cs.Struct(
        "active"   / cs.Pointer(325168, cs.Int32ub),
        "complete" / cs.Pointer(827312, cs.Int32ub),
        "found"    / cs.Pointer(911984, cs.Int32ub),
        "pedestal" / cs.Pointer(538952, cs.Int32ub),
    ),
    "mirroshaz" / cs.Struct(
        "active"   / cs.Pointer(943080, cs.Int32ub),
        "complete" / cs.Pointer(454792, cs.Int32ub),
        "found"    / cs.Pointer(16912, cs.Int32ub),
        "pedestal" / cs.Pointer(5704, cs.Int32ub),
    ),
    "misaesuma" / cs.Struct(
        "active"   / cs.Pointer(922968, cs.Int32ub),
        "complete" / cs.Pointer(460736, cs.Int32ub),
        "found"    / cs.Pointer(1800, cs.Int32ub),
        "pedestal" / cs.Pointer(951952, cs.Int32ub),
    ),
    "moakeet" / cs.Struct(
        "active"   / cs.Pointer(63208, cs.Int32ub),
        "complete" / cs.Pointer(812176, cs.Int32ub),
        "found"    / cs.Pointer(853680, cs.Int32ub),
        "pedestal" / cs.Pointer(821656, cs.Int32ub),
    ),
    "mogglatan" / cs.Struct(
        "active"   / cs.Pointer(16168, cs.Int32ub),
        "complete" / cs.Pointer(533144, cs.Int32ub),
        "found"    / cs.Pointer(942424, cs.Int32ub),
        "pedestal" / cs.Pointer(328808, cs.Int32ub),
    ),
    "monyatoma" / cs.Struct(
        "active"   / cs.Pointer(34896, cs.Int32ub),
        "complete" / cs.Pointer(566024, cs.Int32ub),
        "found"    / cs.Pointer(948800, cs.Int32ub),
        "pedestal" / cs.Pointer(912656, cs.Int32ub),
    ),
    "mozoshenno" / cs.Struct(
        "active"   / cs.Pointer(298232, cs.Int32ub),
        "complete" / cs.Pointer(797720, cs.Int32ub),
        "found"    / cs.Pointer(862584, cs.Int32ub),
        "pedestal" / cs.Pointer(11248, cs.Int32ub),
    ),
    "muwojeem" / cs.Struct(
        "active"   / cs.Pointer(858472, cs.Int32ub),
        "complete" / cs.Pointer(348552, cs.Int32ub),
        "found"    / cs.Pointer(48896, cs.Int32ub),
        "pedestal" / cs.Pointer(852648, cs.Int32ub),
    ),
    "myahmagana" / cs.Struct(
        "active"   / cs.Pointer(71424, cs.Int32ub),
        "complete" / cs.Pointer(804184, cs.Int32ub),
        "found"    / cs.Pointer(883376, cs.Int32ub),
        "pedestal" / cs.Pointer(944552, cs.Int32ub),
    ),
    "namikaozz" / cs.Struct(
        "active"   / cs.Pointer(359336, cs.Int32ub),
        "complete" / cs.Pointer(849888, cs.Int32ub),
        "found"    / cs.Pointer(810008, cs.Int32ub),
        "pedestal" / cs.Pointer(330120, cs.Int32ub),
    ),
    "neezyohma" / cs.Struct(
        "active"   / cs.Pointer(13544, cs.Int32ub),
        "complete" / cs.Pointer(538120, cs.Int32ub),
        "found"    / cs.Pointer(945264, cs.Int32ub),
        "pedestal" / cs.Pointer(850360, cs.Int32ub),
    ),
    "noerajee" / cs.Struct(
        "active"    / cs.Pointer(897144, cs.Int32ub),
        "complete"  / cs.Pointer(387472, cs.Int32ub),
        "found"     / cs.Pointer(302688, cs.Int32ub),
        "pedestal"  / cs.Pointer(1012296, cs.Int32ub),
        "unearthed" / cs.Pointer(541592, cs.Int32ub),
    ),
    "noyaneha" / cs.Struct(
        "active"   / cs.Pointer(300280, cs.Int32ub),
        "complete" / cs.Pointer(847752, cs.Int32ub),
        "found"    / cs.Pointer(900368, cs.Int32ub),
        "pedestal" / cs.Pointer(882336, cs.Int32ub),
    ),
    "omanau" / cs.Struct(
        "active"   / cs.Pointer(390472, cs.Int32ub),
        "complete" / cs.Pointer(893112, cs.Int32ub),
        "found"    / cs.Pointer(833224, cs.Int32ub),
        "pedestal" / cs.Pointer(558544, cs.Int32ub),
    ),
    "owadaim" / cs.Struct(
        "active"   / cs.Pointer(824, cs.Int32ub),
        "complete" / cs.Pointer(548208, cs.Int32ub),
        "found"    / cs.Pointer(922880, cs.Int32ub),
        "pedestal" / cs.Pointer(305600, cs.Int32ub),
    ),
    "pumaagnitae" / cs.Struct(
        "active"   / cs.Pointer(338160, cs.Int32ub),
        "complete" / cs.Pointer(886472, cs.Int32ub),
        "found"    / cs.Pointer(806504, cs.Int32ub),
        "pedestal" / cs.Pointer(10288, cs.Int32ub),
    ),
    "qazatokki" / cs.Struct(
        "active"   / cs.Pointer(540480, cs.Int32ub),
        "complete" / cs.Pointer(9152, cs.Int32ub),
        "found"    / cs.Pointer(472904, cs.Int32ub),
        "pedestal" / cs.Pointer(553304, cs.Int32ub),
    ),
    "quaraym" / cs.Struct(
        "active"   / cs.Pointer(820176, cs.Int32ub),
        "complete" / cs.Pointer(335696, cs.Int32ub),
        "found"    / cs.Pointer(383392, cs.Int32ub),
        "pedestal" / cs.Pointer(474896, cs.Int32ub),
    ),
    "qukahnata" / cs.Struct(
        "active"   / cs.Pointer(339008, cs.Int32ub),
        "complete" / cs.Pointer(885280, cs.Int32ub),
        "found"    / cs.Pointer(807384, cs.Int32ub),
        "pedestal" / cs.Pointer(330144, cs.Int32ub),
    ),
    "raqazunzo" / cs.Struct(
        "active"    / cs.Pointer(300928, cs.Int32ub),
        "complete"  / cs.Pointer(847480, cs.Int32ub),
        "found"     / cs.Pointer(900864, cs.Int32ub),
        "pedestal"  / cs.Pointer(358120, cs.Int32ub),
        "unearthed" / cs.Pointer(910472, cs.Int32ub),
    ),
    "reedahee" / cs.Struct(
        "active"   / cs.Pointer(532432, cs.Int32ub),
        "complete" / cs.Pointer(20104, cs.Int32ub),
        "found"    / cs.Pointer(457016, cs.Int32ub),
        "pedestal" / cs.Pointer(455752, cs.Int32ub),
    ),
    "resurrection" / cs.Struct(
        "active"   / cs.Pointer(51112, cs.Int32ub),
        "door"     / cs.Pointer(27240, cs.Int32ub),
        "pedestal" / cs.Pointer(852816, cs.Int32ub),
    ),
    "rinoyaa" / cs.Struct(
        "active"   / cs.Pointer(950848, cs.Int32ub),
        "complete" / cs.Pointer(521504, cs.Int32ub),
        "found"    / cs.Pointer(31976, cs.Int32ub),
        "pedestal" / cs.Pointer(828192, cs.Int32ub),
    ),
    "rinuhonika" / cs.Struct(
        "active"    / cs.Pointer(62240, cs.Int32ub),
        "complete"  / cs.Pointer(810464, cs.Int32ub),
        "found"     / cs.Pointer(852696, cs.Int32ub),
        "pedestal"  / cs.Pointer(856816, cs.Int32ub),
        "unearthed" / cs.Pointer(535752, cs.Int32ub),
    ),
    "ritaagzumo" / cs.Struct(
        "active"    / cs.Pointer(2704, cs.Int32ub),
        "complete"  / cs.Pointer(550128, cs.Int32ub),
        "found"     / cs.Pointer(923896, cs.Int32ub),
        "pedestal"  / cs.Pointer(907872, cs.Int32ub),
        "unearthed" / cs.Pointer(481344, cs.Int32ub),
    ),
    "rohtachigah" / cs.Struct(
        "active"      / cs.Pointer(895248, cs.Int32ub),
        "complete"    / cs.Pointer(391640, cs.Int32ub),
        "found"       / cs.Pointer(307336, cs.Int32ub),
        "monsterbase" / cs.Pointer(854416, cs.Int32ub),
        "pedestal"    / cs.Pointer(1015616, cs.Int32ub),
        "unearthed"   / cs.Pointer(520136, cs.Int32ub),
    ),
    "rokuwog" / cs.Struct(
        "active"   / cs.Pointer(472704, cs.Int32ub),
        "complete" / cs.Pointer(914120, cs.Int32ub),
        "found"    / cs.Pointer(540248, cs.Int32ub),
        "pedestal" / cs.Pointer(38400, cs.Int32ub),
    ),
    "ronakachta" / cs.Struct(
        "active"   / cs.Pointer(27136, cs.Int32ub),
        "complete" / cs.Pointer(794920, cs.Int32ub),
        "found"    / cs.Pointer(1013112, cs.Int32ub),
        "pedestal" / cs.Pointer(477376, cs.Int32ub),
    ),
    "rotaooh" / cs.Struct(
        "active"   / cs.Pointer(897520, cs.Int32ub),
        "complete" / cs.Pointer(389712, cs.Int32ub),
        "found"    / cs.Pointer(303088, cs.Int32ub),
        "pedestal" / cs.Pointer(328440, cs.Int32ub),
    ),
    "ruccomaag" / cs.Struct(
        "active"   / cs.Pointer(540872, cs.Int32ub),
        "complete" / cs.Pointer(11640, cs.Int32ub),
        "found"    / cs.Pointer(473176, cs.Int32ub),
        "pedestal" / cs.Pointer(944392, cs.Int32ub),
    ),
    "ruvokorbah" / cs.Struct(
        "active"      / cs.Pointer(61384, cs.Int32ub),
        "complete"    / cs.Pointer(814512, cs.Int32ub),
        "found"       / cs.Pointer(857224, cs.Int32ub),
        "monsterbase" / cs.Pointer(825256, cs.Int32ub),
        "pedestal"    / cs.Pointer(390632, cs.Int32ub),
        "unearthed"   / cs.Pointer(474480, cs.Int32ub),
    ),
    "saaskosah" / cs.Struct(
        "active"    / cs.Pointer(860856, cs.Int32ub),
        "complete"  / cs.Pointer(346168, cs.Int32ub),
        "found"     / cs.Pointer(75120, cs.Int32ub),
        "pedestal"  / cs.Pointer(362184, cs.Int32ub),
        "unearthed" / cs.Pointer(522584, cs.Int32ub),
    ),
    "sahdahaj" / cs.Struct(
        "active"   / cs.Pointer(562848, cs.Int32ub),
        "complete" / cs.Pointer(39360, cs.Int32ub),
        "found"    / cs.Pointer(477656, cs.Int32ub),
        "pedestal" / cs.Pointer(952272, cs.Int32ub),
    ),
    "sasakai" / cs.Struct(
        "active"    / cs.Pointer(912568, cs.Int32ub),
        "complete"  / cs.Pointer(361536, cs.Int32ub),
        "found"     / cs.Pointer(325752, cs.Int32ub),
        "pedestal"  / cs.Pointer(346008, cs.Int32ub),
        "unearthed" / cs.Pointer(448608, cs.Int32ub),
    ),
    "satokoda" / cs.Struct(
        "active"    / cs.Pointer(356600, cs.Int32ub),
        "complete"  / cs.Pointer(853520, cs.Int32ub),
        "found"     / cs.Pointer(812864, cs.Int32ub),
        "pedestal"  / cs.Pointer(884624, cs.Int32ub),
        "unearthed" / cs.Pointer(858672, cs.Int32ub),
    ),
    "shadanaw" / cs.Struct(
        "active"   / cs.Pointer(1008152, cs.Int32ub),
        "complete" / cs.Pointer(516632, cs.Int32ub),
        "found"    / cs.Pointer(28120, cs.Int32ub),
        "pedestal" / cs.Pointer(477080, cs.Int32ub),
    ),
    "shaekatha" / cs.Struct(
        "active"   / cs.Pointer(1015296, cs.Int32ub),
        "complete" / cs.Pointer(510968, cs.Int32ub),
        "found"    / cs.Pointer(46216, cs.Int32ub),
        "pedestal" / cs.Pointer(33456, cs.Int32ub),
    ),
    "shaeloya" / cs.Struct(
        "active"   / cs.Pointer(873808, cs.Int32ub),
        "complete" / cs.Pointer(340448, cs.Int32ub),
        "found"    / cs.Pointer(69672, cs.Int32ub),
        "pedestal" / cs.Pointer(547840, cs.Int32ub),
    ),
    "shaemosah" / cs.Struct(
        "active"   / cs.Pointer(799144, cs.Int32ub),
        "complete" / cs.Pointer(73328, cs.Int32ub),
        "found"    / cs.Pointer(342832, cs.Int32ub),
        "pedestal" / cs.Pointer(67808, cs.Int32ub),
    ),
    "shagehma" / cs.Struct(
        "active"   / cs.Pointer(849768, cs.Int32ub),
        "complete" / cs.Pointer(359432, cs.Int32ub),
        "found"    / cs.Pointer(65584, cs.Int32ub),
        "pedestal" / cs.Pointer(342760, cs.Int32ub),
    ),
    "shaiutoh" / cs.Struct(
        "active"   / cs.Pointer(6328, cs.Int32ub),
        "complete" / cs.Pointer(543336, cs.Int32ub),
        "found"    / cs.Pointer(916504, cs.Int32ub),
        "pedestal" / cs.Pointer(47064, cs.Int32ub),
    ),
    "shaiyota" / cs.Struct(
        "active"    / cs.Pointer(458664, cs.Int32ub),
        "complete"  / cs.Pointer(931064, cs.Int32ub),
        "found"     / cs.Pointer(525632, cs.Int32ub),
        "pedestal"  / cs.Pointer(483360, cs.Int32ub),
        "unearthed" / cs.Pointer(942952, cs.Int32ub),
    ),
    "sharolun" / cs.Struct(
        "active"    / cs.Pointer(845000, cs.Int32ub),
        "complete"  / cs.Pointer(303936, cs.Int32ub),
        "found"     / cs.Pointer(389200, cs.Int32ub),
        "pedestal"  / cs.Pointer(940712, cs.Int32ub),
        "unearthed" / cs.Pointer(460864, cs.Int32ub),
    ),
    "shawarvo" / cs.Struct(
        "active"   / cs.Pointer(792384, cs.Int32ub),
        "complete" / cs.Pointer(30128, cs.Int32ub),
        "found"    / cs.Pointer(517184, cs.Int32ub),
        "pedestal" / cs.Pointer(26560, cs.Int32ub),
    ),
    "sheemdagoze" / cs.Struct(
        "active"    / cs.Pointer(352680, cs.Int32ub),
        "complete"  / cs.Pointer(856912, cs.Int32ub),
        "found"     / cs.Pointer(814720, cs.Int32ub),
        "pedestal"  / cs.Pointer(345824, cs.Int32ub),
        "unearthed" / cs.Pointer(796536, cs.Int32ub),
    ),
    "sheevaneer" / cs.Struct(
        "active"   / cs.Pointer(1023800, cs.Int32ub),
        "complete" / cs.Pointer(476744, cs.Int32ub),
        "found"    / cs.Pointer(37176, cs.Int32ub),
        "pedestal" / cs.Pointer(383168, cs.Int32ub),
    ),
    "sheevenath" / cs.Struct(
        "active"   / cs.Pointer(40400, cs.Int32ub),
        "complete" / cs.Pointer(558656, cs.Int32ub),
        "found"    / cs.Pointer(1021656, cs.Int32ub),
        "pedestal" / cs.Pointer(522472, cs.Int32ub),
    ),
    "shehrata" / cs.Struct(
        "active"   / cs.Pointer(893000, cs.Int32ub),
        "complete" / cs.Pointer(390576, cs.Int32ub),
        "found"    / cs.Pointer(305640, cs.Int32ub),
        "pedestal" / cs.Pointer(346384, cs.Int32ub),
    ),
    "shiragomar" / cs.Struct(
        "active"    / cs.Pointer(304048, cs.Int32ub),
        "complete"  / cs.Pointer(873408, cs.Int32ub),
        "found"     / cs.Pointer(897720, cs.Int32ub),
        "pedestal"  / cs.Pointer(849632, cs.Int32ub),
        "unearthed" / cs.Pointer(25392, cs.Int32ub),
    ),
    "shodantu" / cs.Struct(
        "active"    / cs.Pointer(834112, cs.Int32ub),
        "complete"  / cs.Pointer(307784, cs.Int32ub),
        "found"     / cs.Pointer(391352, cs.Int32ub),
        "pedestal"  / cs.Pointer(908280, cs.Int32ub),
        "unearthed" / cs.Pointer(910800, cs.Int32ub),
    ),
    "shodasah" / cs.Struct(
        "active"   / cs.Pointer(384696, cs.Int32ub),
        "complete" / cs.Pointer(899936, cs.Int32ub),
        "found"    / cs.Pointer(845872, cs.Int32ub),
        "pedestal" / cs.Pointer(858216, cs.Int32ub),
    ),
    "shoqatatone" / cs.Struct(
        "active"    / cs.Pointer(820688, cs.Int32ub),
        "complete"  / cs.Pointer(335488, cs.Int32ub),
        "found"     / cs.Pointer(383912, cs.Int32ub),
        "pedestal"  / cs.Pointer(845488, cs.Int32ub),
        "unearthed" / cs.Pointer(849144, cs.Int32ub),
    ),
    "shorahah" / cs.Struct(
        "active"   / cs.Pointer(344640, cs.Int32ub),
        "complete" / cs.Pointer(864840, cs.Int32ub),
        "found"    / cs.Pointer(801080, cs.Int32ub),
        "pedestal" / cs.Pointer(901768, cs.Int32ub),
    ),
    "sohkofi" / cs.Struct(
        "active"   / cs.Pointer(308264, cs.Int32ub),
        "complete" / cs.Pointer(831088, cs.Int32ub),
        "found"    / cs.Pointer(886768, cs.Int32ub),
        "pedestal" / cs.Pointer(552544, cs.Int32ub),
    ),
    "sumasahma" / cs.Struct(
        "active"    / cs.Pointer(808520, cs.Int32ub),
        "complete"  / cs.Pointer(64584, cs.Int32ub),
        "found"     / cs.Pointer(357648, cs.Int32ub),
        "pedestal"  / cs.Pointer(814608, cs.Int32ub),
        "unearthed" / cs.Pointer(812968, cs.Int32ub),
    ),
    "tahmuhl" / cs.Struct(
        "active"   / cs.Pointer(515040, cs.Int32ub),
        "complete" / cs.Pointer(1012864, cs.Int32ub),
        "found"    / cs.Pointer(795392, cs.Int32ub),
        "pedestal" / cs.Pointer(459296, cs.Int32ub),
    ),
    "tahnooah" / cs.Struct(
        "active"   / cs.Pointer(37712, cs.Int32ub),
        "complete" / cs.Pointer(561624, cs.Int32ub),
        "found"    / cs.Pointer(1024208, cs.Int32ub),
        "pedestal" / cs.Pointer(797536, cs.Int32ub),
    ),
    "takamashiri" / cs.Struct(
        "active"    / cs.Pointer(372336, cs.Int32ub),
        "complete"  / cs.Pointer(904272, cs.Int32ub),
        "found"     / cs.Pointer(822608, cs.Int32ub),
        "pedestal"  / cs.Pointer(845480, cs.Int32ub),
        "unearthed" / cs.Pointer(19512, cs.Int32ub),
    ),
    "talohnaeg" / cs.Struct(
        "active"   / cs.Pointer(891864, cs.Int32ub),
        "complete" / cs.Pointer(448848, cs.Int32ub),
        "found"    / cs.Pointer(310184, cs.Int32ub),
        "pedestal" / cs.Pointer(905720, cs.Int32ub),
    ),
    "tawajinn" / cs.Struct(
        "active"    / cs.Pointer(33912, cs.Int32ub),
        "complete"  / cs.Pointer(564280, cs.Int32ub),
        "found"     / cs.Pointer(947632, cs.Int32ub),
        "pedestal"  / cs.Pointer(950672, cs.Int32ub),
        "unearthed" / cs.Pointer(31336, cs.Int32ub),
    ),
    "tenakosah" / cs.Struct(
        "active"   / cs.Pointer(67464, cs.Int32ub),
        "complete" / cs.Pointer(805504, cs.Int32ub),
        "found"    / cs.Pointer(884944, cs.Int32ub),
        "pedestal" / cs.Pointer(381624, cs.Int32ub),
    ),
    "thokayu" / cs.Struct(
        "active"    / cs.Pointer(818424, cs.Int32ub),
        "complete"  / cs.Pointer(49424, cs.Int32ub),
        "found"     / cs.Pointer(350288, cs.Int32ub),
        "pedestal"  / cs.Pointer(949936, cs.Int32ub),
        "unearthed" / cs.Pointer(343296, cs.Int32ub),
    ),
    "tohyahsa" / cs.Struct(
        "active"    / cs.Pointer(330584, cs.Int32ub),
        "complete"  / cs.Pointer(822176, cs.Int32ub),
        "found"     / cs.Pointer(904472, cs.Int32ub),
        "pedestal"  / cs.Pointer(4408, cs.Int32ub),
        "unearthed" / cs.Pointer(308528, cs.Int32ub),
    ),
    "toquomo" / cs.Struct(
        "active"   / cs.Pointer(473664, cs.Int32ub),
        "complete" / cs.Pointer(915896, cs.Int32ub),
        "found"    / cs.Pointer(541344, cs.Int32ub),
        "pedestal" / cs.Pointer(796056, cs.Int32ub),
    ),
    "totosah" / cs.Struct(
        "active"    / cs.Pointer(24752, cs.Int32ub),
        "complete"  / cs.Pointer(794632, cs.Int32ub),
        "found"     / cs.Pointer(1010240, cs.Int32ub),
        "pedestal"  / cs.Pointer(547864, cs.Int32ub),
        "unearthed" / cs.Pointer(21504, cs.Int32ub),
    ),
    "tukaloh" / cs.Struct(
        "active"   / cs.Pointer(13136, cs.Int32ub),
        "complete" / cs.Pointer(535512, cs.Int32ub),
        "found"    / cs.Pointer(944968, cs.Int32ub),
        "pedestal" / cs.Pointer(331648, cs.Int32ub),
    ),
    "tutsuwanima" / cs.Struct(
        "active"    / cs.Pointer(828328, cs.Int32ub),
        "complete"  / cs.Pointer(311064, cs.Int32ub),
        "found"     / cs.Pointer(360672, cs.Int32ub),
        "pedestal"  / cs.Pointer(924208, cs.Int32ub),
        "unearthed" / cs.Pointer(816144, cs.Int32ub),
    ),
    "voolota" / cs.Struct(
        "active"    / cs.Pointer(548024, cs.Int32ub),
        "complete"  / cs.Pointer(1736, cs.Int32ub),
        "found"     / cs.Pointer(461216, cs.Int32ub),
        "pedestal"  / cs.Pointer(806848, cs.Int32ub),
        "unearthed" / cs.Pointer(19528, cs.Int32ub),
    ),
    "wahgokatta" / cs.Struct(
        "active"   / cs.Pointer(566888, cs.Int32ub),
        "complete" / cs.Pointer(31520, cs.Int32ub),
        "found"    / cs.Pointer(519856, cs.Int32ub),
        "pedestal" / cs.Pointer(6576, cs.Int32ub),
    ),
    "yahrin" / cs.Struct(
        "active"   / cs.Pointer(550736, cs.Int32ub),
        "complete" / cs.Pointer(46328, cs.Int32ub),
        "found"    / cs.Pointer(510352, cs.Int32ub),
        "pedestal" / cs.Pointer(390216, cs.Int32ub),
    ),
    "yanaga" / cs.Struct(
        "active"   / cs.Pointer(50872, cs.Int32ub),
        "complete" / cs.Pointer(817568, cs.Int32ub),
        "found"    / cs.Pointer(860184, cs.Int32ub),
        "pedestal" / cs.Pointer(482656, cs.Int32ub),
    ),
    "yowakaita" / cs.Struct(
        "active"      / cs.Pointer(351592, cs.Int32ub),
        "complete"    / cs.Pointer(855104, cs.Int32ub),
        "found"       / cs.Pointer(813640, cs.Int32ub),
        "monsterbase" / cs.Pointer(388296, cs.Int32ub),
        "pedestal"    / cs.Pointer(565304, cs.Int32ub),
    ),
    "zaltawa" / cs.Struct(
        "active"   / cs.Pointer(521968, cs.Int32ub),
        "complete" / cs.Pointer(947656, cs.Int32ub),
        "found"    / cs.Pointer(563632, cs.Int32ub),
        "pedestal" / cs.Pointer(883728, cs.Int32ub),
    ),
    "zekasho" / cs.Struct(
        "active"   / cs.Pointer(29984, cs.Int32ub),
        "complete" / cs.Pointer(792488, cs.Int32ub),
        "found"    / cs.Pointer(1009880, cs.Int32ub),
        "pedestal" / cs.Pointer(304056, cs.Int32ub),
    ),
    "zunakai" / cs.Struct(
        "active"   / cs.Pointer(561688, cs.Int32ub),
        "complete" / cs.Pointer(37648, cs.Int32ub),
        "found"    / cs.Pointer(476432, cs.Int32ub),
        "pedestal" / cs.Pointer(816000, cs.Int32ub),
    ),
)

SHRINES_NAMES: list[str] = ["akhvaquot", "bareedanaag", "boshkala", "chaasqeta", "daagchokah", "dagahkeek", "dahhesho", "dahkaso", "dakatuss", "dakotah", "daqakoh", "daqochisay", "dilamaag", "downaeh", "dunbataag", "etsukorima", "geeharah", "gomaasaagh", "goraetorr", "hadahamar", "hawakoth", "hiamiu", "hilarao", "ishtosoh", "jabaij", "jeenoh", "jitansami", "joloonah", "kaamyatak", "kahmael", "kahokeo", "kahyah", "kamiaomuna", "kamurog", "kaomakagh", "katahchuki", "katosaaug", "kayawan", "kaynoh", "kayramah", "keedafunia", "keehayoog", "kehnamut", "keivetala", "kemakosassa", "kemazoos", "kenaishakah", "keoruug", "ketohwawai", "kiahtoza", "kihiromoh", "korguchideh", "korshohu", "kuhnsidajj", "kuhtakkar", "laknarokee", "lannokooh", "maaghalan", "maagnorah", "maheliya", "makarah", "mezzalo", "mijahrokee", "mirroshaz", "misaesuma", "moakeet", "mogglatan", "monyatoma", "mozoshenno", "muwojeem", "myahmagana", "namikaozz", "neezyohma", "noerajee", "noyaneha", "omanau", "owadaim", "pumaagnitae", "qazatokki", "quaraym", "qukahnata", "raqazunzo", "reedahee", "resurrection", "rinoyaa", "rinuhonika", "ritaagzumo", "rohtachigah", "rokuwog", "ronakachta", "rotaooh", "ruccomaag", "ruvokorbah", "saaskosah", "sahdahaj", "sasakai", "satokoda", "shadanaw", "shaekatha", "shaeloya", "shaemosah", "shagehma", "shaiutoh", "shaiyota", "sharolun", "shawarvo", "sheemdagoze", "sheevaneer", "sheevenath", "shehrata", "shiragomar", "shodantu", "shodasah", "shoqatatone", "shorahah", "sohkofi", "sumasahma", "tahmuhl", "tahnooah", "takamashiri", "talohnaeg", "tawajinn", "tenakosah", "thokayu", "tohyahsa", "toquomo", "totosah", "tukaloh", "tutsuwanima", "voolota", "wahgokatta", "yahrin", "yanaga", "yowakaita", "zaltawa", "zekasho", "zunakai"]

SHRINE_SIMPLE: frozenset[str] = frozenset({"akhvaquot", "boshkala", "chaasqeta", "daagchokah", "dahhesho", "dahkaso", "dakatuss", "dakotah", "daqakoh", "daqochisay", "dilamaag", "downaeh", "dunbataag", "geeharah", "gomaasaagh", "goraetorr", "hadahamar", "hawakoth", "hiamiu", "hilarao", "ishtosoh", "jabaij", "jeenoh", "kaamyatak", "kahmael", "kahokeo", "kaomakagh", "katahchuki", "katosaaug", "kayawan", "kaynoh", "kehnamut", "kemakosassa", "kemazoos", "kenaishakah", "keoruug", "ketohwawai", "korguchideh", "kuhtakkar", "lannokooh", "maaghalan", "maagnorah", "makarah", "mijahrokee", "mirroshaz", "misaesuma", "moakeet", "mogglatan", "monyatoma", "mozoshenno", "muwojeem", "myahmagana", "namikaozz", "neezyohma", "noyaneha", "omanau", "owadaim", "pumaagnitae", "qazatokki", "quaraym", "qukahnata", "reedahee", "rinoyaa", "rokuwog", "ronakachta", "rotaooh", "ruccomaag", "sahdahaj", "shadanaw", "shaekatha", "shaeloya", "shaemosah", "shagehma", "shaiutoh", "shawarvo", "sheevaneer", "sheevenath", "shehrata", "shodasah", "shorahah", "sohkofi", "tahmuhl", "tahnooah", "talohnaeg", "tenakosah", "toquomo", "tukaloh", "wahgokatta", "yahrin", "yanaga", "zaltawa", "zekasho", "zunakai"})

SHRINE_EXTRA_KEYS: dict[str, frozenset[str]] = {
    "bareedanaag": frozenset({"unearthed"}),
    "dagahkeek": frozenset({"unearthed"}),
    "etsukorima": frozenset({"monsterbase", "unearthed"}),
    "jitansami": frozenset({"unearthed"}),
    "joloonah": frozenset({"unearthed"}),
    "kahyah": frozenset({"unearthed"}),
    "kamiaomuna": frozenset({"unearthed"}),
    "kamurog": frozenset({"unearthed"}),
    "kayramah": frozenset({"unearthed"}),
    "keedafunia": frozenset({"unearthed"}),
    "keehayoog": frozenset({"unearthed"}),
    "keivetala": frozenset({"unearthed"}),
    "kiahtoza": frozenset({"unearthed"}),
    "kihiromoh": frozenset({"unearthed"}),
    "korshohu": frozenset({"unearthed"}),
    "kuhnsidajj": frozenset({"unearthed"}),
    "laknarokee": frozenset({"unearthed"}),
    "maheliya": frozenset({"unearthed"}),
    "mezzalo": frozenset({"unearthed"}),
    "noerajee": frozenset({"unearthed"}),
    "raqazunzo": frozenset({"unearthed"}),
    "resurrection": frozenset({"door"}),
    "rinuhonika": frozenset({"unearthed"}),
    "ritaagzumo": frozenset({"unearthed"}),
    "rohtachigah": frozenset({"monsterbase", "unearthed"}),
    "ruvokorbah": frozenset({"monsterbase", "unearthed"}),
    "saaskosah": frozenset({"unearthed"}),
    "sasakai": frozenset({"unearthed"}),
    "satokoda": frozenset({"unearthed"}),
    "shaiyota": frozenset({"unearthed"}),
    "sharolun": frozenset({"unearthed"}),
    "sheemdagoze": frozenset({"unearthed"}),
    "shiragomar": frozenset({"unearthed"}),
    "shodantu": frozenset({"unearthed"}),
    "shoqatatone": frozenset({"unearthed"}),
    "sumasahma": frozenset({"unearthed"}),
    "takamashiri": frozenset({"unearthed"}),
    "tawajinn": frozenset({"unearthed"}),
    "thokayu": frozenset({"unearthed"}),
    "tohyahsa": frozenset({"unearthed"}),
    "totosah": frozenset({"unearthed"}),
    "tutsuwanima": frozenset({"unearthed"}),
    "voolota": frozenset({"unearthed"}),
    "yowakaita": frozenset({"monsterbase"}),
}

# ── Towers ──────────────────────────────────────────────────────────────────

TOWERS_LAYOUT = cs.Struct(
    "akkala" / cs.Struct(
        "active" / cs.Pointer(453824, cs.Int32ub),
        "found"  / cs.Pointer(387080, cs.Int32ub),
    ),
    "all" / cs.Struct(
        "unearthed" / cs.Pointer(806592, cs.Int32ub),
    ),
    "central" / cs.Struct(
        "active" / cs.Pointer(921400, cs.Int32ub),
        "found"  / cs.Pointer(911504, cs.Int32ub),
    ),
    "duelingpeaks" / cs.Struct(
        "active" / cs.Pointer(3648, cs.Int32ub),
        "found"  / cs.Pointer(325584, cs.Int32ub),
    ),
    "eldin" / cs.Struct(
        "active" / cs.Pointer(32976, cs.Int32ub),
        "found"  / cs.Pointer(75896, cs.Int32ub),
    ),
    "faron" / cs.Struct(
        "active" / cs.Pointer(28256, cs.Int32ub),
        "found"  / cs.Pointer(68664, cs.Int32ub),
    ),
    "gerudo" / cs.Struct(
        "active" / cs.Pointer(560768, cs.Int32ub),
        "found"  / cs.Pointer(817288, cs.Int32ub),
    ),
    "greatplateau" / cs.Struct(
        "active" / cs.Pointer(554480, cs.Int32ub),
        "found"  / cs.Pointer(809560, cs.Int32ub),
    ),
    "hateno" / cs.Struct(
        "active" / cs.Pointer(545944, cs.Int32ub),
        "found"  / cs.Pointer(829768, cs.Int32ub),
    ),
    "hebra" / cs.Struct(
        "active" / cs.Pointer(519096, cs.Int32ub),
        "found"  / cs.Pointer(337768, cs.Int32ub),
    ),
    "lake" / cs.Struct(
        "active" / cs.Pointer(509408, cs.Int32ub),
        "found"  / cs.Pointer(356928, cs.Int32ub),
    ),
    "lanayru" / cs.Struct(
        "active" / cs.Pointer(1021096, cs.Int32ub),
        "found"  / cs.Pointer(849408, cs.Int32ub),
    ),
    "ridgeland" / cs.Struct(
        "active" / cs.Pointer(457128, cs.Int32ub),
        "found"  / cs.Pointer(393216, cs.Int32ub),
    ),
    "tabantha" / cs.Struct(
        "active" / cs.Pointer(917928, cs.Int32ub),
        "found"  / cs.Pointer(904048, cs.Int32ub),
    ),
    "wasteland" / cs.Struct(
        "active" / cs.Pointer(17136, cs.Int32ub),
        "found"  / cs.Pointer(299272, cs.Int32ub),
    ),
    "woodland" / cs.Struct(
        "active" / cs.Pointer(520016, cs.Int32ub),
        "found"  / cs.Pointer(347376, cs.Int32ub),
    ),
)

TOWERS_NAMES: list[str] = ["akkala", "all", "central", "duelingpeaks", "eldin", "faron", "gerudo", "greatplateau", "hateno", "hebra", "lake", "lanayru", "ridgeland", "tabantha", "wasteland", "woodland"]

# ── Memories ────────────────────────────────────────────────────────────────

MEMORIES_LAYOUT = cs.Struct(
    "apremonition" / cs.Struct(
        "remembered" / cs.Pointer(796864, cs.Int32ub),
    ),
    "bladesoftheyiga" / cs.Struct(
        "remembered" / cs.Pointer(36968, cs.Int32ub),
    ),
    "championdarukssong" / cs.Struct(
        "remembered" / cs.Pointer(62448, cs.Int32ub),
    ),
    "championmiphassong" / cs.Struct(
        "remembered" / cs.Pointer(65304, cs.Int32ub),
    ),
    "championrevalissong" / cs.Struct(
        "remembered" / cs.Pointer(63384, cs.Int32ub),
    ),
    "championurbosassong" / cs.Struct(
        "remembered" / cs.Pointer(65640, cs.Int32ub),
    ),
    "daruksmettle" / cs.Struct(
        "remembered" / cs.Pointer(535400, cs.Int32ub),
    ),
    "despair" / cs.Struct(
        "remembered" / cs.Pointer(804576, cs.Int32ub),
    ),
    "fatheranddaughter" / cs.Struct(
        "remembered" / cs.Pointer(807008, cs.Int32ub),
    ),
    "miphastouch" / cs.Struct(
        "remembered" / cs.Pointer(536064, cs.Int32ub),
    ),
    "resolveandgrief" / cs.Struct(
        "remembered" / cs.Pointer(44504, cs.Int32ub),
    ),
    "returnofcalamityganon" / cs.Struct(
        "remembered" / cs.Pointer(801800, cs.Int32ub),
    ),
    "revalisflap" / cs.Struct(
        "remembered" / cs.Pointer(533312, cs.Int32ub),
    ),
    "shelterfromthestorm" / cs.Struct(
        "remembered" / cs.Pointer(800136, cs.Int32ub),
    ),
    "silentprincess" / cs.Struct(
        "remembered" / cs.Pointer(797992, cs.Int32ub),
    ),
    "slumberingpower" / cs.Struct(
        "remembered" / cs.Pointer(805240, cs.Int32ub),
    ),
    "subduedceremony" / cs.Struct(
        "remembered" / cs.Pointer(43488, cs.Int32ub),
    ),
    "thechampionsballad" / cs.Struct(
        "remembered" / cs.Pointer(51592, cs.Int32ub),
    ),
    "themastersword" / cs.Struct(
        "remembered" / cs.Pointer(864224, cs.Int32ub),
    ),
    "tomountlanayru" / cs.Struct(
        "remembered" / cs.Pointer(800440, cs.Int32ub),
    ),
    "urbosashand" / cs.Struct(
        "remembered" / cs.Pointer(537944, cs.Int32ub),
    ),
    "zeldasawakening" / cs.Struct(
        "remembered" / cs.Pointer(816584, cs.Int32ub),
    ),
    "zeldasresentment" / cs.Struct(
        "remembered" / cs.Pointer(33248, cs.Int32ub),
    ),
)

MEMORIES_NAMES: list[str] = ["apremonition", "bladesoftheyiga", "championdarukssong", "championmiphassong", "championrevalissong", "championurbosassong", "daruksmettle", "despair", "fatheranddaughter", "miphastouch", "resolveandgrief", "returnofcalamityganon", "revalisflap", "shelterfromthestorm", "silentprincess", "slumberingpower", "subduedceremony", "thechampionsballad", "themastersword", "tomountlanayru", "urbosashand", "zeldasawakening", "zeldasresentment"]

# ── Divine Beasts ───────────────────────────────────────────────────────────

DIVINEBEASTS_LAYOUT = cs.Struct(
    "finaltrial" / cs.Struct(
        "allterminals"       / cs.Pointer(458632, cs.Int32ub),
        "complete"           / cs.Pointer(526568, cs.Int32ub),
        "map"                / cs.Pointer(863160, cs.Int32ub),
        "terminal1"          / cs.Pointer(384520, cs.Int32ub),
        "terminal2"          / cs.Pointer(50416, cs.Int32ub),
        "terminal3"          / cs.Pointer(792192, cs.Int32ub),
        "terminal4"          / cs.Pointer(897688, cs.Int32ub),
        "terminalsremaining" / cs.Pointer(893088, cs.Int32ub),
    ),
    "vahmedoh" / cs.Struct(
        "active"             / cs.Pointer(1022888, cs.Int32ub),
        "allterminals"       / cs.Pointer(850456, cs.Int32ub),
        "bossdefeated"       / cs.Pointer(914304, cs.Int32ub),
        "complete"           / cs.Pointer(327216, cs.Int32ub),
        "found"              / cs.Pointer(950680, cs.Int32ub),
        "heartcontainer"     / cs.Pointer(7200, cs.Int32ub),
        "map"                / cs.Pointer(792264, cs.Int32ub),
        "pedestal"           / cs.Pointer(353688, cs.Int32ub),
        "targeting"          / cs.Pointer(526576, cs.Int32ub),
        "terminal1"          / cs.Pointer(1015280, cs.Int32ub),
        "terminal2"          / cs.Pointer(948280, cs.Int32ub),
        "terminal3"          / cs.Pointer(362408, cs.Int32ub),
        "terminal4"          / cs.Pointer(547760, cs.Int32ub),
        "terminal5"          / cs.Pointer(526424, cs.Int32ub),
        "terminalsremaining" / cs.Pointer(562912, cs.Int32ub),
    ),
    "vahnaboris" / cs.Struct(
        "active"             / cs.Pointer(940352, cs.Int32ub),
        "allterminals"       / cs.Pointer(457192, cs.Int32ub),
        "bossdefeated"       / cs.Pointer(860200, cs.Int32ub),
        "complete"           / cs.Pointer(38168, cs.Int32ub),
        "found"              / cs.Pointer(38432, cs.Int32ub),
        "heartcontainer"     / cs.Pointer(46928, cs.Int32ub),
        "map"                / cs.Pointer(18424, cs.Int32ub),
        "pedestal"           / cs.Pointer(42792, cs.Int32ub),
        "terminal1"          / cs.Pointer(544096, cs.Int32ub),
        "terminal2"          / cs.Pointer(950888, cs.Int32ub),
        "terminal3"          / cs.Pointer(794808, cs.Int32ub),
        "terminal4"          / cs.Pointer(913192, cs.Int32ub),
        "terminal5"          / cs.Pointer(819656, cs.Int32ub),
        "terminalsremaining" / cs.Pointer(354080, cs.Int32ub),
    ),
    "vahrudania" / cs.Struct(
        "active"             / cs.Pointer(533944, cs.Int32ub),
        "allterminals"       / cs.Pointer(830256, cs.Int32ub),
        "bossdefeated"       / cs.Pointer(565496, cs.Int32ub),
        "complete"           / cs.Pointer(336264, cs.Int32ub),
        "found"              / cs.Pointer(543264, cs.Int32ub),
        "heartcontainer"     / cs.Pointer(18096, cs.Int32ub),
        "map"                / cs.Pointer(509440, cs.Int32ub),
        "pedestal"           / cs.Pointer(941976, cs.Int32ub),
        "shutters"           / cs.Pointer(449024, cs.Int32ub),
        "terminal1"          / cs.Pointer(325000, cs.Int32ub),
        "terminal2"          / cs.Pointer(534696, cs.Int32ub),
        "terminal3"          / cs.Pointer(477040, cs.Int32ub),
        "terminal4"          / cs.Pointer(309824, cs.Int32ub),
        "terminal5"          / cs.Pointer(949696, cs.Int32ub),
        "terminalsremaining" / cs.Pointer(944344, cs.Int32ub),
    ),
    "vahruta" / cs.Struct(
        "active"             / cs.Pointer(817632, cs.Int32ub),
        "allterminals"       / cs.Pointer(845656, cs.Int32ub),
        "beginningenemies"   / cs.Pointer(1009432, cs.Int32ub),
        "bossdefeated"       / cs.Pointer(892144, cs.Int32ub),
        "complete"           / cs.Pointer(828976, cs.Int32ub),
        "found"              / cs.Pointer(458016, cs.Int32ub),
        "heartcontainer"     / cs.Pointer(39808, cs.Int32ub),
        "map"                / cs.Pointer(509352, cs.Int32ub),
        "pedestal"           / cs.Pointer(950168, cs.Int32ub),
        "shortcutwaterfall"  / cs.Pointer(468496, cs.Int32ub),
        "terminal1"          / cs.Pointer(32888, cs.Int32ub),
        "terminal2"          / cs.Pointer(477296, cs.Int32ub),
        "terminal3"          / cs.Pointer(832616, cs.Int32ub),
        "terminal4"          / cs.Pointer(338744, cs.Int32ub),
        "terminal5"          / cs.Pointer(43576, cs.Int32ub),
        "terminalsremaining" / cs.Pointer(884248, cs.Int32ub),
    ),
)

DIVINEBEASTS_NAMES: list[str] = ["finaltrial", "vahmedoh", "vahnaboris", "vahrudania", "vahruta"]

# ── Fairy Fountains ─────────────────────────────────────────────────────────

FAIRYFOUNTAINS_LAYOUT = cs.Struct(
    "cotera" / cs.Struct(
        "unlocked" / cs.Pointer(1017248, cs.Int32ub),
    ),
    "kaysa" / cs.Struct(
        "unlocked" / cs.Pointer(37008, cs.Int32ub),
    ),
    "malanya" / cs.Struct(
        "unlocked" / cs.Pointer(1024512, cs.Int32ub),
    ),
    "mija" / cs.Struct(
        "unlocked" / cs.Pointer(450496, cs.Int32ub),
    ),
    "tera" / cs.Struct(
        "unlocked" / cs.Pointer(541632, cs.Int32ub),
    ),
)

FAIRYFOUNTAINS_NAMES: list[str] = ["cotera", "kaysa", "malanya", "mija", "tera"]

# ── Ancient Tech Labs ───────────────────────────────────────────────────────

ANCIENTTECHLABS_LAYOUT = cs.Struct(
    "akkala" / cs.Struct(
        "active" / cs.Pointer(523656, cs.Int32ub),
        "found"  / cs.Pointer(913952, cs.Int32ub),
    ),
    "hateno" / cs.Struct(
        "active" / cs.Pointer(561184, cs.Int32ub),
        "found"  / cs.Pointer(474704, cs.Int32ub),
    ),
)

ANCIENTTECHLABS_NAMES: list[str] = ["akkala", "hateno"]

# ── Cutscenes ───────────────────────────────────────────────────────────────

CUTSCENES_LAYOUT = cs.Struct(
    "boardingvahnaboris" / cs.Struct(
        "viewed" / cs.Pointer(384560, cs.Int32ub),
    ),
    "collectedonespiritorb" / cs.Struct(
        "viewed" / cs.Pointer(918856, cs.Int32ub),
    ),
    "enteringhyrulecastle" / cs.Struct(
        "viewed" / cs.Pointer(332240, cs.Int32ub),
    ),
    "findingthemastersword" / cs.Struct(
        "viewed" / cs.Pointer(469736, cs.Int32ub),
    ),
    "firstspiritorb" / cs.Struct(
        "viewed" / cs.Pointer(29400, cs.Int32ub),
    ),
    "leavingtheshrineofresurrection" / cs.Struct(
        "viewed" / cs.Pointer(819160, cs.Int32ub),
    ),
    "masterkohgaintro" / cs.Struct(
        "viewed" / cs.Pointer(340384, cs.Int32ub),
    ),
    "meetingimpa" / cs.Struct(
        "viewed" / cs.Pointer(351664, cs.Int32ub),
    ),
    "meetingriju" / cs.Struct(
        "viewed" / cs.Pointer(71272, cs.Int32ub),
    ),
    "meetingteba" / cs.Struct(
        "viewed" / cs.Pointer(67784, cs.Int32ub),
    ),
    "meetingyunobo" / cs.Struct(
        "viewed" / cs.Pointer(68168, cs.Int32ub),
    ),
    "rescueyunoboagain" / cs.Struct(
        "viewed" / cs.Pointer(339432, cs.Int32ub),
    ),
    "takethesheikahslate" / cs.Struct(
        "viewed" / cs.Pointer(1008160, cs.Int32ub),
    ),
    "tryingtotakethemastersword" / cs.Struct(
        "viewed" / cs.Pointer(825888, cs.Int32ub),
    ),
    "vahmedohintro" / cs.Struct(
        "viewed" / cs.Pointer(334072, cs.Int32ub),
    ),
    "vahnaborisintro" / cs.Struct(
        "viewed" / cs.Pointer(344808, cs.Int32ub),
    ),
    "vahrudaniaintro" / cs.Struct(
        "viewed" / cs.Pointer(328496, cs.Int32ub),
    ),
)

CUTSCENES_NAMES: list[str] = ["boardingvahnaboris", "collectedonespiritorb", "enteringhyrulecastle", "findingthemastersword", "firstspiritorb", "leavingtheshrineofresurrection", "masterkohgaintro", "meetingimpa", "meetingriju", "meetingteba", "meetingyunobo", "rescueyunoboagain", "takethesheikahslate", "tryingtotakethemastersword", "vahmedohintro", "vahnaborisintro", "vahrudaniaintro"]

# ── Horses ──────────────────────────────────────────────────────────────────
# NOTE: stride-8 string fields (name/type/saddle/reins/mane) are excluded.
# Only bond (float), color (integer), and selected.slot are mapped here.
# Stub: HorseProxy.name / .type / .saddle / .reins / .mane raise NotImplementedError.


HORSES_LAYOUT = cs.Struct(
    "selected" / cs.Struct(
        "position" / cs.Pointer(1016640, cs.Int32ub),
        "slot"     / cs.Pointer(847024, cs.Int32ub),
    ),
    "slot1" / cs.Struct(
        "bond"  / cs.Pointer(915808, cs.Int32ub),
        "color" / cs.Pointer(525960, cs.Int32ub),
    ),
    "slot2" / cs.Struct(
        "bond"  / cs.Pointer(915816, cs.Int32ub),
        "color" / cs.Pointer(525968, cs.Int32ub),
    ),
    "slot3" / cs.Struct(
        "bond"  / cs.Pointer(915824, cs.Int32ub),
        "color" / cs.Pointer(525976, cs.Int32ub),
    ),
    "slot4" / cs.Struct(
        "bond"  / cs.Pointer(915832, cs.Int32ub),
        "color" / cs.Pointer(525984, cs.Int32ub),
    ),
    "slot5" / cs.Struct(
        "bond"  / cs.Pointer(915840, cs.Int32ub),
        "color" / cs.Pointer(525992, cs.Int32ub),
    ),
    "wild" / cs.Struct(
        "bond"     / cs.Pointer(915848, cs.Int32ub),
        "color"    / cs.Pointer(526000, cs.Int32ub),
        "position" / cs.Pointer(362720, cs.Int32ub),
    ),
)

HORSES_NAMES: list[str] = ["selected", "slot1", "slot2", "slot3", "slot4", "slot5", "wild"]

# ── NPCs ────────────────────────────────────────────────────────────────────

NPCS_LAYOUT = cs.Struct(
    "kass" / cs.Struct(
        "introduced" / cs.Pointer(65152, cs.Int32ub),
    ),
    "traysi" / cs.Struct(
        "introduced" / cs.Pointer(69144, cs.Int32ub),
    ),
)

NPCS_NAMES: list[str] = ["kass", "traysi"]

# ── Runes ───────────────────────────────────────────────────────────────────

RUNES_LAYOUT = cs.Struct(
    "bombs" / cs.Struct(
        "enabled" / cs.Pointer(38648, cs.Int32ub),
        "plus"    / cs.Pointer(449632, cs.Int32ub),
    ),
    "camera" / cs.Struct(
        "enabled" / cs.Pointer(1013160, cs.Int32ub),
    ),
    "cryonis" / cs.Struct(
        "enabled" / cs.Pointer(386608, cs.Int32ub),
    ),
    "magnesis" / cs.Struct(
        "enabled" / cs.Pointer(514936, cs.Int32ub),
    ),
    "mastercyclezero" / cs.Struct(
        "enabled" / cs.Pointer(861792, cs.Int32ub),
    ),
    "stasis" / cs.Struct(
        "enabled" / cs.Pointer(483584, cs.Int32ub),
        "plus"    / cs.Pointer(791896, cs.Int32ub),
    ),
)

RUNES_NAMES: list[str] = ["bombs", "camera", "cryonis", "magnesis", "mastercyclezero", "stasis"]

# ── Sheikah Slate ───────────────────────────────────────────────────────────

SHEIKAHSLATE_LAYOUT = cs.Struct(
    "album" / cs.Struct(
        "enabled" / cs.Pointer(942184, cs.Int32ub),
    ),
    "hyrulecompendium" / cs.Struct(
        "enabled" / cs.Pointer(348488, cs.Int32ub),
    ),
    "sensor" / cs.Struct(
        "enabled" / cs.Pointer(863256, cs.Int32ub),
        "plus"    / cs.Pointer(814808, cs.Int32ub),
    ),
)

SHEIKAHSLATE_NAMES: list[str] = ["album", "hyrulecompendium", "sensor"]

# ── Quick Tips ──────────────────────────────────────────────────────────────

QUICKTIPS_LAYOUT = cs.Struct(
    "switcharrows" / cs.Struct(
        "viewed" / cs.Pointer(448208, cs.Int32ub),
    ),
    "switchbows" / cs.Struct(
        "viewed" / cs.Pointer(830368, cs.Int32ub),
    ),
    "switchshields" / cs.Struct(
        "viewed" / cs.Pointer(802776, cs.Int32ub),
    ),
    "switchweapons" / cs.Struct(
        "viewed" / cs.Pointer(44720, cs.Int32ub),
    ),
    "throwweapon" / cs.Struct(
        "viewed" / cs.Pointer(355024, cs.Int32ub),
    ),
)

QUICKTIPS_NAMES: list[str] = ["switcharrows", "switchbows", "switchshields", "switchweapons", "throwweapon"]

# ── Side Quests ─────────────────────────────────────────────────────────────

SIDEQUESTS_LAYOUT = cs.Struct(
    "agiftfromthemonks" / cs.Struct(
        "complete"     / cs.Pointer(922064, cs.Int32ub),
        "tookcap"      / cs.Pointer(349112, cs.Int32ub),
        "tooktrousers" / cs.Pointer(537960, cs.Int32ub),
        "tooktunic"    / cs.Pointer(28064, cs.Int32ub),
    ),
    "byfireflyslight" / cs.Struct(
        "begun"    / cs.Pointer(45048, cs.Int32ub),
        "complete" / cs.Pointer(308088, cs.Int32ub),
    ),
    "findkheel" / cs.Struct(
        "available"   / cs.Pointer(932472, cs.Int32ub),
        "begun"       / cs.Pointer(335976, cs.Int32ub),
        "complete"    / cs.Pointer(862048, cs.Int32ub),
        "talktokheel" / cs.Pointer(452792, cs.Int32ub),
    ),
    "flownthecoop" / cs.Struct(
        "begun"           / cs.Pointer(562264, cs.Int32ub),
        "complete"        / cs.Pointer(801928, cs.Int32ub),
        "returnthecuccos" / cs.Pointer(357624, cs.Int32ub),
    ),
    "robbiesresearch" / cs.Struct(
        "begun"              / cs.Pointer(38720, cs.Int32ub),
        "blueflamefurnace"   / cs.Pointer(516328, cs.Int32ub),
        "complete"           / cs.Pointer(332936, cs.Int32ub),
        "introducedtojerrin" / cs.Pointer(371704, cs.Int32ub),
    ),
    "slatedforupgrades" / cs.Struct(
        "askforsomethinggood" / cs.Pointer(20176, cs.Int32ub),
        "begun"               / cs.Pointer(828160, cs.Int32ub),
        "complete"            / cs.Pointer(833704, cs.Int32ub),
    ),
    "thepricelessmaracas" / cs.Struct(
        "begun"    / cs.Pointer(561976, cs.Int32ub),
        "complete" / cs.Pointer(801488, cs.Int32ub),
    ),
    "trialofthesword" / cs.Struct(
        "begun"          / cs.Pointer(325528, cs.Int32ub),
        "complete"       / cs.Pointer(899608, cs.Int32ub),
        "talktodekutree" / cs.Pointer(298960, cs.Int32ub),
    ),
)

SIDEQUESTS_NAMES: list[str] = ["agiftfromthemonks", "byfireflyslight", "findkheel", "flownthecoop", "robbiesresearch", "slatedforupgrades", "thepricelessmaracas", "trialofthesword"]

# ── Main Quests ─────────────────────────────────────────────────────────────

MAINQUESTS_LAYOUT = cs.Struct(
    "capturedmemories" / cs.Struct(
        "12memoriescomplete"  / cs.Pointer(478288, cs.Int32ub),
        "begun"               / cs.Pointer(42352, cs.Int32ub),
        "championstunictaken" / cs.Pointer(358448, cs.Int32ub),
        "complete"            / cs.Pointer(809744, cs.Int32ub),
        "memoriesremaining"   / cs.Pointer(481944, cs.Int32ub),
    ),
    "championdarukssong" / cs.Struct(
        "begun"                       / cs.Pointer(830752, cs.Int32ub),
        "complete"                    / cs.Pointer(44512, cs.Int32ub),
        "illusoryrealmbattleunlocked" / cs.Pointer(43656, cs.Int32ub),
    ),
    "championmiphassong" / cs.Struct(
        "begun"                       / cs.Pointer(382360, cs.Int32ub),
        "complete"                    / cs.Pointer(384256, cs.Int32ub),
        "illusoryrealmbattleunlocked" / cs.Pointer(62320, cs.Int32ub),
    ),
    "championrevalissong" / cs.Struct(
        "begun"                       / cs.Pointer(886040, cs.Int32ub),
        "complete"                    / cs.Pointer(798888, cs.Int32ub),
        "illusoryrealmbattleunlocked" / cs.Pointer(802736, cs.Int32ub),
    ),
    "championurbosassong" / cs.Struct(
        "begun"                       / cs.Pointer(50320, cs.Int32ub),
        "complete"                    / cs.Pointer(337680, cs.Int32ub),
        "illusoryrealmbattleunlocked" / cs.Pointer(844056, cs.Int32ub),
    ),
    "destroyganon" / cs.Struct(
        "begun"    / cs.Pointer(523120, cs.Int32ub),
        "selected" / cs.Pointer(393768, cs.Int32ub),
    ),
    "divinebeastvahmedoh" / cs.Struct(
        "begun"          / cs.Pointer(942480, cs.Int32ub),
        "boardvahmedoh"  / cs.Pointer(480976, cs.Int32ub),
        "complete"       / cs.Pointer(810544, cs.Int32ub),
        "impressteba"    / cs.Pointer(813208, cs.Int32ub),
        "talktosaki"     / cs.Pointer(947048, cs.Int32ub),
        "theflightrange" / cs.Pointer(802808, cs.Int32ub),
    ),
    "divinebeastvahnaboris" / cs.Struct(
        "begun"                   / cs.Pointer(381240, cs.Int32ub),
        "boardvahnaboris"         / cs.Pointer(10232, cs.Int32ub),
        "complete"                / cs.Pointer(911144, cs.Int32ub),
        "defeatmasterkohga"       / cs.Pointer(807448, cs.Int32ub),
        "entertheyigahideout"     / cs.Pointer(353728, cs.Int32ub),
        "meetrijuatlookout"       / cs.Pointer(469664, cs.Int32ub),
        "obtainthethunderhelm"    / cs.Pointer(518808, cs.Int32ub),
        "retreatedfromvahnaboris" / cs.Pointer(34992, cs.Int32ub),
        "returnthethunderhelm"    / cs.Pointer(346144, cs.Int32ub),
        "talktoteake"             / cs.Pointer(516344, cs.Int32ub),
    ),
    "divinebeastvahrudania" / cs.Struct(
        "begun"           / cs.Pointer(908472, cs.Int32ub),
        "boardvahrudania" / cs.Pointer(393664, cs.Int32ub),
        "bridgeofeldin"   / cs.Pointer(850872, cs.Int32ub),
        "complete"        / cs.Pointer(340304, cs.Int32ub),
        "rescueyunobo"    / cs.Pointer(901304, cs.Int32ub),
        "talktobludo"     / cs.Pointer(567288, cs.Int32ub),
    ),
    "divinebeastvahruta" / cs.Struct(
        "begun"              / cs.Pointer(454152, cs.Int32ub),
        "boardvahruta"       / cs.Pointer(904416, cs.Int32ub),
        "collectshockarrows" / cs.Pointer(453624, cs.Int32ub),
        "complete"           / cs.Pointer(334496, cs.Int32ub),
        "talktomuzu"         / cs.Pointer(810240, cs.Int32ub),
        "wearzoraarmor"      / cs.Pointer(1020832, cs.Int32ub),
    ),
    "findthefairyfountain" / cs.Struct(
        "begun"    / cs.Pointer(306768, cs.Int32ub),
        "complete" / cs.Pointer(1023032, cs.Int32ub),
    ),
    "followthesheikahslate" / cs.Struct(
        "begun"    / cs.Pointer(931768, cs.Int32ub),
        "complete" / cs.Pointer(551072, cs.Int32ub),
    ),
    "forbiddencityentry" / cs.Struct(
        "begun"            / cs.Pointer(75552, cs.Int32ub),
        "buygerudoclothes" / cs.Pointer(805392, cs.Int32ub),
        "complete"         / cs.Pointer(389096, cs.Int32ub),
    ),
    "freethedivinebeasts" / cs.Struct(
        "begun"    / cs.Pointer(1007840, cs.Int32ub),
        "complete" / cs.Pointer(478264, cs.Int32ub),
    ),
    "lockedmementos" / cs.Struct(
        "begun"            / cs.Pointer(883504, cs.Int32ub),
        "complete"         / cs.Pointer(895872, cs.Int32ub),
        "lightthefurnace"  / cs.Pointer(521184, cs.Int32ub),
        "returntoimpa"     / cs.Pointer(481112, cs.Int32ub),
        "takeasnapofpurah" / cs.Pointer(550120, cs.Int32ub),
        "talktopurah"      / cs.Pointer(455496, cs.Int32ub),
    ),
    "reachzorasdomain" / cs.Struct(
        "begun"               / cs.Pointer(18608, cs.Int32ub),
        "complete"            / cs.Pointer(943064, cs.Int32ub),
        "sidonrivercutscene1" / cs.Pointer(852424, cs.Int32ub),
        "sidonrivercutscene2" / cs.Pointer(388912, cs.Int32ub),
        "sidonrivercutscene3" / cs.Pointer(72464, cs.Int32ub),
        "sidonrivercutscene4" / cs.Pointer(821544, cs.Int32ub),
        "sidonrivercutscene5" / cs.Pointer(942584, cs.Int32ub),
    ),
    "seekoutimpa" / cs.Struct(
        "begun"    / cs.Pointer(47360, cs.Int32ub),
        "complete" / cs.Pointer(342936, cs.Int32ub),
        "selected" / cs.Pointer(393768, cs.Int32ub),
    ),
    "thechampionsballad" / cs.Struct(
        "begun"                                / cs.Pointer(805208, cs.Int32ub),
        "complete"                             / cs.Pointer(334296, cs.Int32ub),
        "completethechampionsongs"             / cs.Pointer(540304, cs.Int32ub),
        "conquerthemonsterbases"               / cs.Pointer(452296, cs.Int32ub),
        "findthenewmonuments"                  / cs.Pointer(1025168, cs.Int32ub),
        "kassisontheplateau"                   / cs.Pointer(850320, cs.Int32ub),
        "returntotheshrineofresurrection"      / cs.Pointer(352576, cs.Int32ub),
        "returntotheshrineofresurrectionagain" / cs.Pointer(549800, cs.Int32ub),
    ),
    "theherossword" / cs.Struct(
        "begun"    / cs.Pointer(860848, cs.Int32ub),
        "complete" / cs.Pointer(32688, cs.Int32ub),
    ),
    "theisolatedplateau" / cs.Struct(
        "begun"                   / cs.Pointer(44624, cs.Int32ub),
        "collectedfourspiritorbs" / cs.Pointer(71744, cs.Int32ub),
        "collectedonespiritorb"   / cs.Pointer(1016504, cs.Int32ub),
        "complete"                / cs.Pointer(456704, cs.Int32ub),
    ),
)

MAINQUESTS_NAMES: list[str] = ["capturedmemories", "championdarukssong", "championmiphassong", "championrevalissong", "championurbosassong", "destroyganon", "divinebeastvahmedoh", "divinebeastvahnaboris", "divinebeastvahrudania", "divinebeastvahruta", "findthefairyfountain", "followthesheikahslate", "forbiddencityentry", "freethedivinebeasts", "lockedmementos", "reachzorasdomain", "seekoutimpa", "thechampionsballad", "theherossword", "theisolatedplateau"]

# ── Champion Powers ─────────────────────────────────────────────────────────

CHAMPIONPOWERS_LAYOUT = cs.Struct(
    "daruksprotection" / cs.Struct(
        "plus"       / cs.Pointer(885256, cs.Int32ub),
        "readytimer" / cs.Pointer(470264, cs.Int32ub),
        "uses"       / cs.Pointer(949152, cs.Int32ub),
    ),
    "miphasgrace" / cs.Struct(
        "plus"       / cs.Pointer(1012400, cs.Int32ub),
        "readytimer" / cs.Pointer(797104, cs.Int32ub),
    ),
    "revalisgale" / cs.Struct(
        "plus"       / cs.Pointer(538312, cs.Int32ub),
        "readytimer" / cs.Pointer(9624, cs.Int32ub),
        "uses"       / cs.Pointer(1023176, cs.Int32ub),
    ),
    "urbosasfury" / cs.Struct(
        "plus"       / cs.Pointer(913760, cs.Int32ub),
        "readytimer" / cs.Pointer(27648, cs.Int32ub),
        "uses"       / cs.Pointer(563560, cs.Int32ub),
    ),
)

CHAMPIONPOWERS_NAMES: list[str] = ["daruksprotection", "miphasgrace", "revalisgale", "urbosasfury"]

# ── Towns ───────────────────────────────────────────────────────────────────

TOWNS_LAYOUT = cs.Struct(
    "kakarikovillage" / cs.Struct(
        "found" / cs.Pointer(902192, cs.Int32ub),
    ),
    "lurelinvillage" / cs.Struct(
        "found" / cs.Pointer(346048, cs.Int32ub),
    ),
)

TOWNS_NAMES: list[str] = ["kakarikovillage", "lurelinvillage"]

# ── Master Sword ────────────────────────────────────────────────────────────

MASTERSWORD_LAYOUT = cs.Struct(
    "fullyunlocked" / cs.Struct(
        "set" / cs.Pointer(550296, cs.Int32ub),
    ),
)

MASTERSWORD_NAMES: list[str] = ["fullyunlocked"]

# ── Registry ────────────────────────────────────────────────────────────────

LAYOUTS: dict[str, cs.Struct] = {
    "shrines": SHRINES_LAYOUT,
    "towers": TOWERS_LAYOUT,
    "memories": MEMORIES_LAYOUT,
    "divinebeasts": DIVINEBEASTS_LAYOUT,
    "fairyfountains": FAIRYFOUNTAINS_LAYOUT,
    "ancienttechlabs": ANCIENTTECHLABS_LAYOUT,
    "cutscenes": CUTSCENES_LAYOUT,
    "horses": HORSES_LAYOUT,
    "npcs": NPCS_LAYOUT,
    "runes": RUNES_LAYOUT,
    "sheikahslate": SHEIKAHSLATE_LAYOUT,
    "quicktips": QUICKTIPS_LAYOUT,
    "sidequests": SIDEQUESTS_LAYOUT,
    "mainquests": MAINQUESTS_LAYOUT,
    "championpowers": CHAMPIONPOWERS_LAYOUT,
    "towns": TOWNS_LAYOUT,
    "mastersword": MASTERSWORD_LAYOUT,
}

NAMES: dict[str, list[str]] = {
    "shrines": SHRINES_NAMES,
    "towers": TOWERS_NAMES,
    "memories": MEMORIES_NAMES,
    "divinebeasts": DIVINEBEASTS_NAMES,
    "fairyfountains": FAIRYFOUNTAINS_NAMES,
    "ancienttechlabs": ANCIENTTECHLABS_NAMES,
    "cutscenes": CUTSCENES_NAMES,
    "horses": HORSES_NAMES,
    "npcs": NPCS_NAMES,
    "runes": RUNES_NAMES,
    "sheikahslate": SHEIKAHSLATE_NAMES,
    "quicktips": QUICKTIPS_NAMES,
    "sidequests": SIDEQUESTS_NAMES,
    "mainquests": MAINQUESTS_NAMES,
    "championpowers": CHAMPIONPOWERS_NAMES,
    "towns": TOWNS_NAMES,
    "mastersword": MASTERSWORD_NAMES,
}

# ── Compatibility aliases (singular / short form) ────────────────────────────

SHRINE_LAYOUT = SHRINES_LAYOUT
SHRINE_NAMES: list[str] = SHRINES_NAMES
TOWER_LAYOUT = TOWERS_LAYOUT
TOWER_NAMES: list[str] = TOWERS_NAMES
MEMORY_LAYOUT = MEMORIES_LAYOUT
MEMORY_NAMES: list[str] = MEMORIES_NAMES
DIVINEBEAST_LAYOUT = DIVINEBEASTS_LAYOUT
DIVINEBEAST_NAMES: list[str] = DIVINEBEASTS_NAMES
FAIRYFOUNTAIN_LAYOUT = FAIRYFOUNTAINS_LAYOUT
FAIRYFOUNTAIN_NAMES: list[str] = FAIRYFOUNTAINS_NAMES
ANCIENTTECHLAB_LAYOUT = ANCIENTTECHLABS_LAYOUT
ANCIENTTECHLAB_NAMES: list[str] = ANCIENTTECHLABS_NAMES
CUTSCENE_LAYOUT = CUTSCENES_LAYOUT
CUTSCENE_NAMES: list[str] = CUTSCENES_NAMES
HORSE_LAYOUT = HORSES_LAYOUT
HORSE_NAMES: list[str] = HORSES_NAMES
NPC_LAYOUT = NPCS_LAYOUT
NPC_NAMES: list[str] = NPCS_NAMES
RUNE_LAYOUT = RUNES_LAYOUT
RUNE_NAMES: list[str] = RUNES_NAMES
QUICKTIP_LAYOUT = QUICKTIPS_LAYOUT
QUICKTIP_NAMES: list[str] = QUICKTIPS_NAMES
SIDEQUEST_LAYOUT = SIDEQUESTS_LAYOUT
SIDEQUEST_NAMES: list[str] = SIDEQUESTS_NAMES
MAINQUEST_LAYOUT = MAINQUESTS_LAYOUT
MAINQUEST_NAMES: list[str] = MAINQUESTS_NAMES
CHAMPIONPOWER_LAYOUT = CHAMPIONPOWERS_LAYOUT
CHAMPIONPOWER_NAMES: list[str] = CHAMPIONPOWERS_NAMES
TOWN_LAYOUT = TOWNS_LAYOUT
TOWN_NAMES: list[str] = TOWNS_NAMES
