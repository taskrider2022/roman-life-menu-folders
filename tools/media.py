"""Build mod.io cover and menu-size previews from the supplied regional artwork."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

from icons import REGIONS, ROOT, SOURCES, build, cutout, matte

MEDIA = ROOT / "media"


def font(size):
    candidates = (
        Path("C:\\Windows\\Fonts\\georgiab.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"),
    )
    for candidate in candidates:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size)
    raise FileNotFoundError("Cover requires Georgia Bold or DejaVu Serif Bold.")


def centered(draw, text, y, size, fill):
    draw.text((960, y), text, font=font(size), fill=fill, anchor="mt")


def cover():
    image = Image.new("RGB", (1920, 1080))
    draw = ImageDraw.Draw(image)
    for y in range(1080):
        t = y / 1079
        draw.line((0, y, 1919, y), fill=tuple(round(a * (1 - t) + b * t) for a, b in zip((34, 46, 56), (13, 24, 30))))
    gold = (209, 176, 112)
    draw.rectangle((28, 28, 1891, 1051), outline=gold, width=2)
    draw.line((280, 234, 1640, 234), fill=gold, width=2)
    centered(draw, "ROMAN LIFE", 58, 90, (245, 230, 195))
    centered(draw, "MENU FOLDERS", 161, 42, gold)
    for region, cx in zip(REGIONS, (510, 1410)):
        art = ImageOps.contain(cutout(SOURCES / f"{region}.jpg"), (740, 650), Image.Resampling.LANCZOS)
        image.paste(art, (cx - art.width // 2, 284 + (650 - art.height) // 2), art)
    centered(draw, "LATIUM  |  ALBION  |  IMPERIAL BLENDS", 956, 30, (235, 221, 194))
    centered(draw, "Construction menu organization  |  by Gammelflei", 1008, 23, gold)
    image.save(MEDIA / "modio-cover.png")


def preview():
    image = Image.new("RGB", (1080, 480), (36, 48, 64))
    draw = ImageDraw.Draw(image)
    for row, region in enumerate(REGIONS):
        draw.text((24, row * 230 + 16), region.upper(), font=font(21), fill=(240, 220, 182))
        for size, x in ((128, 215), (64, 435), (48, 620), (32, 805)):
            # Downsample the actual deployed 512px icon, as the game would.
            source = Image.open(ROOT / "mod" / "data" / "roman-life-menu-folders-gammelflei" / "ui" / f"folder_{region}.png")
            art = source.resize((size, size), Image.Resampling.LANCZOS)
            y = row * 230 + 57
            draw.rounded_rectangle((x - 8, y - 8, x + size + 8, y + size + 8), radius=5, fill=(52, 68, 87), outline=(114, 125, 138))
            image.paste(art, (x, y), art)
            draw.text((x, y + size + 18), f"{size}px", font=font(17), fill=(220, 218, 204))
    image.save(MEDIA / "icon-size-preview.png")


def detail_preview():
    regions = (
        ("latium", (100, 100, 640, 320)),
        ("albion", (220, 175, 590, 325)),
        ("albion", (75, 440, 535, 735)),
    )
    panels = []
    for region, box in regions:
        art = matte(SOURCES / f"{region}.jpg").crop(box)
        row = Image.new("RGB", (art.width * 4, art.height * 2), (45, 45, 45))
        for index, color in enumerate(((20, 30, 40), (215, 215, 215))):
            background = Image.new("RGBA", art.size, color + (255,))
            background.alpha_composite(art)
            row.paste(background.resize((art.width * 2, art.height * 2)), (index * art.width * 2, 0))
        panels.append(row)
    image = Image.new("RGB", (max(p.width for p in panels), sum(p.height for p in panels)), (45, 45, 45))
    y = 0
    for panel in panels:
        image.paste(panel, (0, y))
        y += panel.height
    image.save(MEDIA / "cutout-detail-preview.png")


if __name__ == "__main__":
    build(ROOT / "mod" / "data" / "roman-life-menu-folders-gammelflei" / "ui")
    cover()
    preview()
    detail_preview()
