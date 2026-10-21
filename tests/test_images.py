import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import icons
from icon_concepts import badge


class Images(unittest.TestCase):
    def test_deployed_icons_use_selected_badges(self):
        for region, motif in (("latium", "laurel"), ("albion", "triskele")):
            emblem = badge(motif, region)
            expected = icons.icon(emblem.crop(emblem.getbbox()))
            with Image.open(icons.ICON_DIR / f"folder_{region}.png") as actual:
                self.assertEqual(actual.tobytes(), expected.tobytes())

    def test_cover_proposals_are_full_hd(self):
        for name in ("a-dark", "b-parchment", "c-regional"):
            with Image.open(ROOT / "media" / "cover-proposals" / f"{name}.png") as image:
                self.assertEqual(image.size, (1920, 1080))

    def test_supplied_artwork_has_transparent_background_holes(self):
        for region, seeds in icons.BACKGROUND_SEEDS.items():
            result = icons.matte(icons.SOURCES / f"{region}.jpg")
            for point in seeds:
                with self.subTest(region=region, point=point):
                    self.assertLess(result.getpixel(point)[3], 25)

    def test_latium_white_details_survive_but_faded_wood_border_is_removed(self):
        result = icons.matte(icons.SOURCES / "latium.jpg")
        self.assertEqual(result.getpixel((500, 475))[3], 255)
        self.assertEqual(result.getpixel((420, 649))[3], 0)

    def test_albion_preserves_horn_highlight_and_board_pieces(self):
        result = icons.matte(icons.SOURCES / "albion.jpg")
        for point in ((432, 200), (535, 264), (390, 270)):
            with self.subTest(point=point):
                self.assertEqual(result.getpixel(point)[3], 255)

    def test_cutout_preserves_enclosed_white_details(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Image.new("RGB", (80, 80), "white")
            draw = ImageDraw.Draw(source)
            draw.rectangle((15, 15, 64, 64), fill=(70, 40, 20))
            draw.rectangle((30, 30, 49, 49), fill="white")
            path = Path(directory) / "source.png"
            source.save(path)
            result = icons.icon(icons.cutout(path))
            self.assertEqual(result.getpixel((0, 0))[3], 0)
            self.assertEqual(result.getpixel((256, 256)), (255, 255, 255, 255))

    def test_deployed_icons_have_transparent_margins_and_visible_art(self):
        for region in icons.REGIONS:
            with self.subTest(region=region):
                with Image.open(icons.ICON_DIR / f"folder_{region}.png") as image:
                    self.assertEqual(image.size, (512, 512))
                    self.assertEqual(image.mode, "RGBA")
                    alpha = image.getchannel("A")
                    self.assertEqual(alpha.getextrema(), (0, 255))
                    x0, y0, x1, y1 = alpha.getbbox()
                    self.assertGreater(x0, 0)
                    self.assertGreater(y0, 0)
                    self.assertLess(x1, 512)
                    self.assertLess(y1, 512)
                    self.assertGreater(max(x1 - x0, y1 - y0), 470)

    def test_cover_dimensions(self):
        with Image.open(ROOT / "media" / "modio-cover.png") as image:
            self.assertEqual(image.size, (1920, 1080))
            with Image.open(ROOT / "media" / "cover-proposals" / "b-parchment.png") as selected:
                self.assertEqual(image.tobytes(), selected.tobytes())


if __name__ == "__main__":
    unittest.main()
