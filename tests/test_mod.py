"""Static checks for the mod. They prove the files are well-formed and consistent; they do NOT
prove the game accepts the mod. See README "In-game test checklist".
"""
import json
import re
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOD = ROOT / "mod"
ASSETS = MOD / "data/base/config/export/assets.xml"
GUI = MOD / "data/base/config/gui"
sys.path.insert(0, str(ROOT / "tools"))
import guidrange  # noqa: E402
import package  # noqa: E402
from localization import DESCRIPTION_ID, TITLE, TRANSLATIONS, IMPERIAL_MOD, description_without_imperial

CATEGORIES = {"41327", "41328", "41329", "41330", "41331", "41362", "41363", "41364", "41365"}
REQUIRED_LOAD_AFTER = {"rl-latium-khayi", "rl-albion-khayi", "rl-shared-khayi"}
ICON_DIR = MOD / "data/roman-life-menu-folders-gammelflei/ui"


def modinfo():
    return json.loads((MOD / "modinfo.json").read_text(encoding="utf-8"))


def assets():
    return ET.parse(ASSETS).getroot()


def folder_assets():
    return [a for a in assets().iter("Asset") if a.findtext("Template") == "ConstructionCategory"]


def folder_guids():
    return {a.findtext("Values/Standard/GUID") for a in folder_assets()}


class ModInfo(unittest.TestCase):
    def test_required_fields(self):
        m = modinfo()
        for key in ("Version", "Anno", "ModID", "Difficulty", "GameSetup", "Dependencies", "ModName", "Description"):
            self.assertIn(key, m)
        self.assertEqual(m["Anno"], 8)
        self.assertEqual(m["ModID"], "roman-life-menu-folders-gammelflei")
        self.assertRegex(m["Version"], r"^\d+\.\d+\.\d+$")
        self.assertEqual(m["Difficulty"], "unchanged")

    def test_menu_only_mod_is_safe_to_remove(self):
        self.assertTrue(modinfo()["GameSetup"]["SafeToRemove"])

    def test_load_after_covers_roman_life(self):
        load_after = set(modinfo()["Dependencies"]["LoadAfter"])
        self.assertLessEqual(REQUIRED_LOAD_AFTER, load_after)
        self.assertTrue(all(i.startswith("rl-") or i.endswith("-khayi") for i in load_after), "only Roman Life mods")
        self.assertNotIn(modinfo()["ModID"], load_after)

    def test_no_requires_or_incompatibles(self):
        d = modinfo()["Dependencies"]
        self.assertEqual(d.get("Require", []), [])
        self.assertEqual(d.get("Incompatible", []), [])


class Assets(unittest.TestCase):
    def test_well_formed(self):
        self.assertEqual(assets().tag, "ModOps")

    def test_every_modop_is_guid_scoped(self):
        for op in assets().iter("ModOp"):
            self.assertIn("GUID", op.attrib, ET.tostring(op, encoding="unicode")[:120])

    def test_folder_guids_in_registered_range(self):
        folders = folder_assets()
        self.assertEqual(len(folders), 9)
        guids = [int(a.findtext("Values/Standard/GUID")) for a in folders]
        self.assertEqual(len(set(guids)), len(guids))
        for g in guids:
            self.assertTrue(guidrange.RANGE_START <= g <= guidrange.RANGE_END, g)

    def test_folders_sit_next_to_known_categories(self):
        ops = [op for op in assets().iter("ModOp") if op.get("Type") == "addNextSibling" and op.find("Asset") is not None]
        self.assertEqual({op.get("GUID") for op in ops}, CATEGORIES)

    def test_folder_entry_added_to_each_category(self):
        added = {op.findtext("Item/Building") for op in assets().iter("ModOp")
                 if op.get("Type") == "add" and op.get("GUID") in CATEGORIES and "BuildingList" in op.get("Path", "")}
        self.assertEqual(added, folder_guids())

    def test_moved_buildings_are_mod_buildings(self):
        adds = [op for op in assets().iter("ModOp") if op.get("Type") == "add" and op.get("GUID") in folder_guids()]
        self.assertGreaterEqual(len(adds), 120)
        for op in adds:
            b = op.findtext("Item/Building")
            self.assertTrue(b and b.isdigit() and int(b) >= 1_000_000, b)

    def test_conditions_only_reference_mods_or_properties(self):
        for el in assets().iter():
            c = el.get("Condition")
            if c:
                self.assertRegex(c, r"^!?[#$]", c)
                self.assertNotIn("celtic", c)

    def test_icons_exist_and_are_referenced(self):
        self.assertFalse((MOD / "data/roman-life-menu-folders-taskr").exists())
        self.assertNotIn("roman-life-menu-folders-taskr", ASSETS.read_text(encoding="utf-8"))
        refs = set(re.findall(r"data/roman-life-menu-folders-gammelflei/ui/(folder_\w+\.png)", ASSETS.read_text(encoding="utf-8")))
        self.assertEqual(refs, {"folder_albion.png", "folder_latium.png"})
        for r in refs:
            self.assertTrue((ICON_DIR / r).is_file(), r)


class Texts(unittest.TestCase):
    def test_all_twelve_languages_exist(self):
        expected = {"brazilian", "english", "french", "german", "italian", "japanese",
                    "korean", "polish", "russian", "simplified_chinese", "spanish",
                    "traditional_chinese"}
        self.assertEqual(set(TRANSLATIONS), expected)
        self.assertEqual({p.stem.removeprefix("texts_") for p in GUI.glob("texts_*.xml")}, expected)

    def test_every_folder_references_shared_description(self):
        self.assertTrue(guidrange.RANGE_START <= DESCRIPTION_ID <= guidrange.RANGE_END)
        self.assertNotIn(str(DESCRIPTION_ID), folder_guids())
        for asset in folder_assets():
            self.assertEqual(asset.findtext("Values/ConstructionCategory/CategoryDescription"), str(DESCRIPTION_ID))
            self.assertIsNone(asset.find("Values/Standard/InfoDescription"))

    def test_localized_metadata(self):
        info = modinfo()
        for key, name, _, description in TRANSLATIONS.values():
            self.assertEqual(info["ModName"][key], name)
            self.assertEqual(info["Description"][key], description)
        self.assertEqual(info["ModName"]["English"], "Roman Life - Menu Folders")

    def test_every_folder_has_a_line_id(self):
        for lang, (_, _, description, _) in TRANSLATIONS.items():
            root = ET.parse(GUI / f"texts_{lang}.xml").getroot()
            self.assertEqual({op.get("Condition") for op in root},
                             {None, f"#{IMPERIAL_MOD}", f"!#{IMPERIAL_MOD}"})
            for loaded in (False, True):
                condition = f"#{IMPERIAL_MOD}" if loaded else f"!#{IMPERIAL_MOD}"
                entries = [t for op in root if op.get("Condition") in (None, condition)
                           for t in op.findall("Text")]
                self.assertEqual(len(entries), len(folder_guids()) + 1, (lang, loaded))
                self.assertEqual({t.findtext("LineId") for t in entries},
                                 folder_guids() | {str(DESCRIPTION_ID)}, lang)
                for t in entries:
                    content = t.findtext("Text")
                    if t.findtext("LineId") == str(DESCRIPTION_ID):
                        self.assertEqual(content, description if loaded else description_without_imperial(lang, description))
                        self.assertEqual("Imperial Blends" in content, loaded)
                    else:
                        self.assertEqual(content, TITLE)


class GuidRange(unittest.TestCase):
    def test_range_is_safe_and_sized(self):
        self.assertTrue(guidrange.SAFE_START <= guidrange.RANGE_START <= guidrange.RANGE_END <= guidrange.SAFE_END)
        self.assertLessEqual(guidrange.RANGE_END - guidrange.RANGE_START + 1, 100_000)

    def test_registry_row(self):
        self.assertEqual(guidrange.our_row(), "| gammelflei      | 2.110.000.000 | 2.110.000.999 |")

    def test_overlap_detected(self):
        table = "| someone | 2.109.999.000 | 2.110.000.100 |"
        self.assertTrue(any("overlaps" in p for p in guidrange.check(table)))

    def test_free_range_passes(self):
        self.assertEqual(guidrange.check("| someone | 2.100.000.000 | 2.100.009.999 |"), [])


class Package(unittest.TestCase):
    def test_zip_is_reproducible_and_layout_matches_loader(self):
        with tempfile.TemporaryDirectory() as t:
            a = package.build(Path(t) / "a").read_bytes()
            out = package.build(Path(t) / "b")
            self.assertEqual(out.name, f"roman-life-menu-folders-gammelflei-{modinfo()['Version']}.zip")
            self.assertEqual(a, out.read_bytes())
            with zipfile.ZipFile(out) as zf:
                names = zf.namelist()
            info = modinfo()
            folder = f"[{info['Category']['English']}] {info['ModName']['English']} (Gammelflei)"
            self.assertEqual({n.split("/")[0] for n in names}, {folder})
            self.assertIn(f"{folder}/modinfo.json", names)


if __name__ == "__main__":
    unittest.main()
