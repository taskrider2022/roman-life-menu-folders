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
    cover_proposals()
    with Image.open(MEDIA / "cover-proposals" / "b-parchment.png") as image:
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


def cover_proposals():
    from icon_concepts import badge

    destination = MEDIA / "cover-proposals"
    destination.mkdir(parents=True, exist_ok=True)
    palettes = (
        ("a-dark", (31, 44, 54), (12, 25, 31), (244, 225, 185), (205, 170, 100)),
        ("b-parchment", (242, 231, 203), (210, 189, 148), (84, 51, 31), (143, 100, 49)),
        ("c-regional", (88, 47, 48), (30, 66, 58), (248, 231, 192), (214, 178, 108)),
    )
    thumbs = Image.new("RGB", (960, 3 * 580), (25, 33, 41))
    for index, (name, top, bottom, ink, gold) in enumerate(palettes):
        image = Image.new("RGB", (1920, 1080))
        draw = ImageDraw.Draw(image)
        for y in range(1080):
            t = y / 1079
            draw.line((0, y, 1919, y), fill=tuple(round(a * (1 - t) + b * t) for a, b in zip(top, bottom)))
        draw.rectangle((28, 28, 1891, 1051), outline=gold, width=2)
        # Offset lettering gives the title a restrained engraved look.
        draw.text((960, 56), "ROMAN LIFE", font=font(102), anchor="mt", fill=gold)
        centered(draw, "ROMAN LIFE", 53, 102, ink)
        centered(draw, "MENU FOLDERS", 170, 44, gold)
        draw.line((340, 239, 1580, 239), fill=gold, width=2)
        for region, motif, cx in zip(REGIONS, ("laurel", "triskele"), (505, 1415)):
            art = ImageOps.contain(cutout(SOURCES / f"{region}.jpg"), (720, 610), Image.Resampling.LANCZOS)
            image.paste(art, (cx - art.width // 2, 295 + (610 - art.height) // 2), art)
            emblem = badge(motif, region).resize((166, 166), Image.Resampling.LANCZOS)
            image.paste(emblem, (cx - 83, 235), emblem)
        centered(draw, "LATIUM  |  ALBION  |  IMPERIAL BLENDS", 948, 30, ink)
        centered(draw, "Construction menu organization  |  by Gammelflei", 1003, 23, gold)
        image.save(destination / f"{name}.png")
        thumbs.paste(image.resize((960, 540), Image.Resampling.LANCZOS), (0, index * 580 + 40))
        ImageDraw.Draw(thumbs).text((20, index * 580 + 8), name.upper(), font=font(22), fill=(238, 220, 182))
    thumbs.save(destination / "comparison.png")


if __name__ == "__main__":
    build(ROOT / "mod" / "data" / "roman-life-menu-folders-gammelflei" / "ui")
    cover()
    preview()
    detail_preview()
