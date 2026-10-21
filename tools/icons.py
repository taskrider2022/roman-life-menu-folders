from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "media" / "sources"
ICON_DIR = ROOT / "mod" / "data" / "roman-life-menu-folders-gammelflei" / "ui"
REGIONS = ("latium", "albion")
BACKGROUND_SEEDS = {
    "latium": ((506, 139), (558, 149), (279, 190), (620, 241), (616, 252)),
    "albion": (
        (288, 223), (375, 230), (466, 215), (486, 216), (663, 363),
        (688, 375), (125, 478), (492, 625), (470, 248), (357, 223),
    ),
}
LATIUM_LOWER_CONTOUR = (
    (90, 523), (97, 532), (128, 542), (145, 541), (157, 548),
    (192, 553), (211, 562), (242, 571), (252, 575), (300, 591),
    (350, 609), (400, 627), (450, 645), (474, 650), (476, 675),
    (499, 682), (522, 680), (538, 673), (543, 656), (575, 632),
    (600, 606), (626, 581), (650, 564), (676, 547), (683, 533),
    (695, 470),
)


def matte(path):
    image = Image.open(path).convert("RGB")
    minimum = ImageChops.darker(
        ImageChops.darker(image.getchannel("R"), image.getchannel("G")),
        image.getchannel("B"),
    )
    maximum = ImageChops.lighter(
        ImageChops.lighter(image.getchannel("R"), image.getchannel("G")),
        image.getchannel("B"),
    )
    # Flood only near-neutral white, including annotated enclosed background holes.
    pale = ImageChops.multiply(
        minimum.point(lambda value: 255 if value >= 205 else 0),
        ImageChops.subtract(maximum, minimum).point(lambda value: 255 if value <= 22 else 0),
    )
    padded = ImageOps.expand(pale, border=1, fill=255)
    ImageDraw.floodfill(padded, (0, 0), 128)
    for x, y in BACKGROUND_SEEDS.get(path.stem, ()):
        if image.size != (768, 768):
            raise ValueError(f"Background annotations require a 768x768 source: {path}")
        if padded.getpixel((x + 1, y + 1)) not in (128, 255):
            raise ValueError(f"Background seed {(x, y)} is not white in {path}")
        ImageDraw.floodfill(padded, (x + 1, y + 1), 128)
    background = padded.crop((1, 1, image.width + 1, image.height + 1))
    alpha = background.point(lambda value: 0 if value == 128 else 255)
    if path.stem == "latium":
        # The source fades its lower wooden edges into white; trace the solid wood.
        contour = Image.new("L", image.size, 0)
        ImageDraw.Draw(contour).polygon(
            [(0, 0), (768, 0), (768, 470), *reversed(LATIUM_LOWER_CONTOUR), (0, 523)],
            fill=255,
        )
        alpha = ImageChops.darker(alpha, contour)
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.35))
    result = image.convert("RGBA")
    result.putalpha(alpha)
    return result


def cutout(path):
    result = matte(path)
    alpha = result.getchannel("A")
    bbox = alpha.getbbox()
    if bbox is None:
        raise ValueError(f"No foreground found in {path}")
    return result.crop(bbox)


def icon(image, size=512):
    canvas = Image.new("RGBA", (size, size))
    fitted = ImageOps.contain(image, (round(size * 0.94), round(size * 0.94)), Image.Resampling.LANCZOS)
    canvas.alpha_composite(fitted, ((size - fitted.width) // 2, (size - fitted.height) // 2))
    return canvas


def build(ui_dir):
    ui_dir = Path(ui_dir)
    ui_dir.mkdir(parents=True, exist_ok=True)
    for region in REGIONS:
        icon(cutout(SOURCES / f"{region}.jpg")).save(ui_dir / f"folder_{region}.png")


if __name__ == "__main__":
    build(ICON_DIR)
