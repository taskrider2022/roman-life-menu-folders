import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

S = 1024
INK = (58, 40, 28)
rng = np.random.default_rng(7)


def noise(scale, amp=1.0):
    n = rng.random((S // scale + 2, S // scale + 2)).astype("float32")
    im = Image.fromarray((n * 255).astype("uint8")).resize((S, S), Image.BICUBIC)
    return (np.asarray(im).astype("float32") / 255 - 0.5) * 2 * amp


def blank():
    return Image.new("L", (S, S), 0)


class Canvas:
    def __init__(self):
        self.rgb = np.zeros((S, S, 3), "float32")
        self.a = np.zeros((S, S), "float32")
        self.grain = noise(3, 0.5) + noise(24, 0.8) + noise(90, 0.8)

    def paint(self, mask, color, shade=0.0, hatch=None, outline=True, wet=True):
        m = np.asarray(mask).astype("float32") / 255
        col = np.array(color, "float32")
        yy, xx = np.mgrid[0:S, 0:S].astype("float32")
        bb = np.argwhere(m > 0.5)
        if len(bb) == 0:
            return
        y0, x0 = bb.min(0)
        y1, x1 = bb.max(0)
        gx = (xx - x0) / max(1, x1 - x0)
        gy = (yy - y0) / max(1, y1 - y0)
        light = 1.0 - shade * (0.55 * gx + 0.45 * gy)
        tex = 1.0 + self.grain * 0.07
        base = col[None, None, :] * (light * tex)[..., None]
        if wet:
            er = np.asarray(mask.filter(ImageFilter.MinFilter(9)).filter(ImageFilter.GaussianBlur(5))).astype("float32") / 255
            edge = np.clip(m - er, 0, 1)
            base *= (1 - 0.22 * edge)[..., None]
        self.rgb = self.rgb * (1 - m[..., None]) + base * m[..., None]
        self.a = np.maximum(self.a, m)
        if hatch:
            dx, sp, st = hatch
            h = blank()
            hd = ImageDraw.Draw(h)
            for k in range(-S, S * 2, sp):
                jit = int(rng.integers(-3, 4))
                hd.line((k + jit, 0, k + dx + jit, S), fill=255, width=3)
            inner = mask.filter(ImageFilter.MinFilter(15))
            sh = np.clip((gx + gy) - 0.95, 0, 1)
            hm = (np.asarray(h).astype("float32") / 255) * (np.asarray(inner).astype("float32") / 255) * np.clip(sh * 2.2, 0, 1)
            self.rgb = self.rgb * (1 - hm[..., None] * st) + np.array(INK, "float32") * hm[..., None] * st
        if outline:
            self.line_from_mask(mask)

    def line_from_mask(self, mask, width=11):
        er = mask.filter(ImageFilter.MinFilter(width))
        edge = ImageChops.subtract(mask, er)
        e = np.asarray(edge).astype("float32") / 255
        e *= 0.78 + 0.22 * np.clip(self.grain, -1, 1)
        e = np.clip(e, 0, 1)
        self.rgb = self.rgb * (1 - e[..., None]) + np.array(INK, "float32") * e[..., None]
        self.a = np.maximum(self.a, e)

    def stroke(self, fn, alpha=0.85):
        m = blank()
        fn(ImageDraw.Draw(m))
        e = np.asarray(m).astype("float32") / 255 * alpha * (0.8 + 0.2 * np.clip(self.grain, -1, 1))
        self.rgb = self.rgb * (1 - e[..., None]) + np.array(INK, "float32") * e[..., None]
        self.a = np.maximum(self.a, e)

    def finish(self):
        # slight wobble so lines look hand drawn
        dx = noise(40, 1.0) * 3.2
        dy = noise(40, 1.0) * 3.2
        yy, xx = np.mgrid[0:S, 0:S]
        sx = np.clip(xx + dx, 0, S - 1).astype(int)
        sy = np.clip(yy + dy, 0, S - 1).astype(int)
        rgb = self.rgb[sy, sx]
        a = self.a[sy, sx]
        out = np.dstack([np.clip(rgb, 0, 255), np.clip(a, 0, 1) * 255]).astype("uint8")
        im = Image.fromarray(out, "RGBA")
        return im.filter(ImageFilter.GaussianBlur(0.8)).resize((512, 512), Image.LANCZOS)


def poly(pts):
    m = blank()
    ImageDraw.Draw(m).polygon(pts, fill=255)
    return m


def rect(x0, y0, x1, y1, r=0):
    m = blank()
    d = ImageDraw.Draw(m)
    if r:
        d.rounded_rectangle((x0, y0, x1, y1), r, fill=255)
    else:
        d.rectangle((x0, y0, x1, y1), fill=255)
    return m


def ell(x0, y0, x1, y1):
    m = blank()
    ImageDraw.Draw(m).ellipse((x0, y0, x1, y1), fill=255)
    return m


def wash(cv, color, cx=512, cy=800, rx=420, ry=120):
    # uneven paper stain below the motif, like the linen icon
    m = blank()
    d = ImageDraw.Draw(m)
    for _ in range(14):
        ox, oy = int(rng.integers(-rx // 3, rx // 3)), int(rng.integers(-ry // 3, ry // 3))
        w, h = int(rng.integers(rx // 2, rx)), int(rng.integers(ry // 2, ry))
        d.ellipse((cx + ox - w // 2, cy + oy - h // 2, cx + ox + w // 2, cy + oy + h // 2), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(10))
    mm = np.asarray(m).astype("float32") / 255
    mm = np.clip((mm - 0.4) * 3, 0, 1) * 0.9
    col = np.array(color, "float32")
    cv.rgb = cv.rgb * (1 - mm[..., None]) + (col * (1 + cv.grain[..., None] * 0.05)) * mm[..., None]
    cv.a = np.maximum(cv.a, mm)


def latium():
    cv = Canvas()
    wash(cv, (232, 214, 176), 512, 850, 440, 130)
    stone = (236, 222, 190)
    stone_d = (214, 196, 158)
    for i, (x0, x1, y0) in enumerate([(170, 854, 790), (205, 819, 750), (240, 784, 710)]):
        cv.paint(rect(x0, y0, x1, y0 + 44), stone if i % 2 == 0 else stone_d, shade=0.25, hatch=(40, 18, 0.35))
    for k in range(5):
        x = 285 + k * 112
        cv.paint(rect(x - 6, 690, x + 62, 712), stone_d, shade=0.2)
        cv.paint(rect(x, 430, x + 56, 690), stone, shade=0.4, hatch=(60, 14, 0.4))
        cv.paint(rect(x - 12, 408, x + 68, 436, 6), stone_d, shade=0.3)
        for fx in (14, 28, 42):
            cv.stroke(lambda d, fx=fx, x=x: d.line((x + fx, 450, x + fx, 680), fill=255, width=3), alpha=0.35)
    cv.paint(rect(235, 352, 789, 412), stone, shade=0.5, hatch=(30, 16, 0.4))
    for k in range(9):
        x = 262 + k * 62
        cv.paint(rect(x, 368, x + 30, 396), stone_d, shade=0.2, outline=False)
    cv.paint(poly([(205, 352), (819, 352), (512, 190)]), (196, 104, 66), shade=0.6, hatch=(50, 16, 0.5))
    cv.paint(poly([(300, 336), (724, 336), (512, 236)]), (226, 150, 104), shade=0.4)
    cv.paint(ell(478, 262, 546, 330), (238, 210, 130), shade=0.5)
    cv.paint(poly([(492, 196), (532, 196), (512, 150)]), (214, 172, 90), shade=0.4)
    for sx in (-1, 1):
        for j in range(6):
            x = 512 + sx * (60 + j * 30)
            y = 888 - j * 8
            cv.paint(ell(x - 20, y - 9, x + 20, y + 9), (96, 128, 64), shade=0.5)
    return cv.finish()


def albion():
    cv = Canvas()
    wash(cv, (214, 226, 200), 512, 850, 440, 130)
    for i, x in enumerate(range(90, 930, 56)):
        top = 560 + (i * 17 % 5) * 9
        cv.paint(poly([(x, top + 40), (x + 22, top), (x + 44, top + 40), (x + 44, 790), (x, 790)]), (126, 92, 60), shade=0.8, hatch=(36, 14, 0.5))
    cv.paint(rect(742, 400, 830, 600), (118, 84, 56), shade=0.7, hatch=(40, 14, 0.5))
    cv.paint(rect(722, 372, 850, 410), (140, 104, 68), shade=0.5)
    cv.paint(poly([(716, 372), (856, 372), (786, 290)]), (196, 160, 84), shade=0.6, hatch=(40, 14, 0.5))
    cv.paint(ell(60, 760, 964, 900), (124, 156, 88), shade=0.6, hatch=(30, 22, 0.3))
    cv.paint(rect(260, 560, 764, 790, 12), (188, 152, 112), shade=0.8, hatch=(50, 14, 0.5))
    for x in range(290, 750, 46):
        cv.stroke(lambda d, x=x: d.line((x, 575, x + 4, 785), fill=255, width=4), alpha=0.4)
    cv.paint(poly([(200, 590), (824, 590), (512, 250)]), (214, 176, 92), shade=0.7, hatch=(55, 15, 0.6))
    for k in range(8):
        y = 590 - k * 42
        w = (824 - 200) / 2 * (y - 250) / 340
        cv.stroke(lambda d, y=y, w=w: d.line((512 - w + 10, y, 512 + w - 10, y + 8), fill=255, width=4), alpha=0.5)
    for k in range(-5, 6):
        cv.stroke(lambda d, k=k: d.line((512 + k * 12, 270 + abs(k) * 6, 512 + k * 58, 588), fill=255, width=3), alpha=0.3)
    cv.paint(poly([(498, 250), (526, 250), (512, 200)]), (196, 160, 84), shade=0.4)
    cv.paint(rect(452, 650, 572, 790, 50), (62, 42, 30), shade=0.2)
    for x, y, r in [(572, 230, 28), (606, 172, 36), (648, 104, 46)]:
        cv.paint(ell(x - r, y - r, x + r, y + r), (238, 238, 232), shade=0.2)
    for sx in (-1, 1):
        for j in range(5):
            x = 512 + sx * (240 + j * 26)
            y = 880 - j * 14
            cv.paint(ell(x - 20, y - 9, x + 20, y + 9), (82, 124, 64), shade=0.5)
    return cv.finish()


def build(ui_dir):
    os.makedirs(ui_dir, exist_ok=True)
    latium().save(os.path.join(ui_dir, "folder_latium.png"))
    albion().save(os.path.join(ui_dir, "folder_albion.png"))


if __name__ == "__main__":
    build(os.path.join(os.path.dirname(os.path.abspath(__file__)), "prev"))
