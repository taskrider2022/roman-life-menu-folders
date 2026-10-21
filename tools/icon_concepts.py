"""Generate selection previews only; never replace deployed menu icons."""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "media" / "icon-concepts"
S = 512


def arc_points(cx, cy, rx, ry, start, end, count=70):
    return [(cx + rx * math.cos(t), cy + ry * math.sin(t))
            for t in (math.radians(start + (end - start) * i / (count - 1))
                      for i in range(count))]


def symbol(name):
    mask = Image.new("L", (S, S))
    d = ImageDraw.Draw(mask)
    if name == "temple":
        d.polygon([(115, 210), (397, 210), (256, 118)], fill=255)
        d.polygon([(163, 193), (349, 193), (256, 145)], fill=0)
        d.rectangle((130, 219, 382, 235), fill=255)
        for x in (146, 209, 272, 335):
            d.rectangle((x, 245, x + 30, 351), fill=255)
        d.rectangle((129, 355, 383, 372), fill=255)
        d.rectangle((111, 382, 401, 399), fill=255)
    elif name == "carnyx":
        pts = [(164, 381), (207, 365), (253, 335), (287, 285),
               (302, 220), (311, 151)]
        d.line(pts, fill=255, width=39, joint="curve")
        d.polygon([(287, 164), (292, 123), (311, 101), (333, 122),
                   (362, 125), (388, 148), (378, 174), (350, 163),
                   (332, 181), (304, 180)], fill=255)
        d.ellipse((334, 134, 344, 144), fill=0)
        d.polygon([(297, 128), (285, 95), (313, 110)], fill=255)
        d.line((147, 393, 179, 370), fill=255, width=17)
        for x, y in ((273, 303), (296, 248), (306, 200)):
            d.line((x - 22, y - 7, x + 18, y + 6), fill=0, width=6)
    elif name == "laurel":
        for side in (-1, 1):
            points = [(256 + side * x, y) for x, y in
                      ((8, 396), (73, 362), (113, 308), (122, 243), (103, 180), (76, 141))]
            d.line(points, fill=255, width=12, joint="curve")
            for x, y, angle in ((67, 354, 35), (99, 314, 15),
                                (118, 270, -5), (118, 222, -20), (98, 181, -35)):
                for direction in (-1, 1):
                    leaf = Image.new("L", (100, 100))
                    ImageDraw.Draw(leaf).ellipse((37, 10, 63, 86), fill=255)
                    leaf = leaf.rotate(side * angle + direction * 35, Image.Resampling.BICUBIC)
                    mask.paste(255, (int(256 + side * x + direction * 15 - 50), y - 50), leaf)
        d = ImageDraw.Draw(mask)
        d.text((211, 207), "R", font=font(110), fill=255)
    elif name == "triskele":
        for rotation in (0, 120, 240):
            pts = []
            for i in range(130):
                t = i / 129
                angle = math.radians(-140 + t * 360)
                radius = 64 * (1 - t) + 6
                x = 0 + radius * math.cos(angle)
                y = -100 + radius * math.sin(angle)
                a = math.radians(rotation)
                pts.append((256 + x * math.cos(a) - y * math.sin(a),
                            256 + x * math.sin(a) + y * math.cos(a)))
            d.line([(256, 256), *pts], fill=255, width=25, joint="curve")
        d.ellipse((239, 239, 273, 273), fill=255)
    elif name == "amphora":
        d.ellipse((155, 168, 227, 283), outline=255, width=21)
        d.ellipse((285, 168, 357, 283), outline=255, width=21)
        d.polygon([(222, 145), (290, 145), (286, 211), (324, 269),
                   (318, 328), (291, 363), (266, 391), (246, 391),
                   (221, 363), (194, 328), (188, 269), (226, 211)], fill=255)
        d.ellipse((211, 131, 301, 159), fill=255)
        d.line((207, 299, 305, 299), fill=0, width=12)
    elif name == "torc":
        d.line(arc_points(256, 256, 123, 132, 38, 322), fill=255, width=34)
        for x in (351,):
            d.ellipse((x - 29, 311, x + 29, 369), fill=255)
            d.ellipse((x - 29, 143, x + 29, 201), fill=255)
        for angle in range(65, 300, 24):
            a = math.radians(angle)
            x, y = 256 + 123 * math.cos(a), 256 + 132 * math.sin(a)
            d.line((x - 13, y - 7, x + 13, y + 7), fill=0, width=5)
    else:
        raise ValueError(name)
    return mask


def font(size):
    for p in (Path("C:\\Windows\\Fonts\\georgiab.ttf"),
              Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf")):
        if p.is_file():
            return ImageFont.truetype(str(p), size)
    raise FileNotFoundError("Georgia Bold or DejaVu Serif Bold required")


def badge(name, region):
    image = Image.new("RGBA", (S, S))
    d = ImageDraw.Draw(image)
    shield = [(66, 92), (256, 54), (446, 92), (431, 362), (256, 458), (81, 362)]
    d.polygon(shield, fill=(34, 41, 46), outline=(170, 140, 77), width=13)
    inner = [(87, 110), (256, 76), (425, 110), (411, 349), (256, 432), (101, 349)]
    d.polygon(inner, fill=(75, 40, 43) if region == "latium" else (34, 65, 59),
              outline=(92, 80, 54), width=5)
    mask = symbol(name)
    shadow = Image.new("RGBA", (S, S))
    shadow.paste((9, 13, 18, 220), (0, 0, S, S), mask.filter(ImageFilter.GaussianBlur(6)))
    image.alpha_composite(shadow, (3, 6))
    gold = Image.new("RGBA", (S, S))
    gd = ImageDraw.Draw(gold)
    for y in range(S):
        t = y / (S - 1)
        gd.line((0, y, S, y), fill=(int(255 - 63 * t), int(244 - 89 * t), int(188 - 105 * t), 255))
    image.paste(gold, (0, 0), mask)
    return image


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    sheet = Image.new("RGB", (1500, 1050), (28, 39, 51))
    d = ImageDraw.Draw(sheet)
    d.text((40, 22), "ROMAN LIFE - ICON CONCEPTS", font=font(30), fill=(244, 227, 187))
    pairs = (("A - Architektur / Carnyx", "temple", "carnyx"),
             ("B - Lorbeer / Triskele", "laurel", "triskele"),
             ("C - Amphore / Torques", "amphora", "torc"))
    for row, (label, left, right) in enumerate(pairs):
        y = 90 + row * 310
        d.text((40, y + 10), label, font=font(24), fill=(226, 196, 137))
        for column, (region, motif) in enumerate((("latium", left), ("albion", right))):
            x = 520 + column * 490
            art = badge(motif, region)
            art.save(OUT / f"{chr(97 + row)}-{region}.png")
            sheet.paste(art.resize((190, 190), Image.Resampling.LANCZOS), (x, y), art.resize((190, 190), Image.Resampling.LANCZOS))
            d.text((x, y + 196), region.upper(), font=font(19), fill=(230, 224, 206))
            for index, size in enumerate((48, 36, 28)):
                bx = x + 220 + index * 76
                by = y + 60
                d.rectangle((bx - 4, by - 5, bx + size + 4, by + 60), fill=(51, 67, 87), outline=(111, 122, 136))
                small = art.resize((size, size), Image.Resampling.LANCZOS)
                sheet.paste(small, (bx, by), small)
                d.text((bx, by + 77), str(size), font=font(15), fill=(214, 210, 194))
    sheet.save(OUT / "comparison.png")


if __name__ == "__main__":
    build()
