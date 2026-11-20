"""Shared drawing helpers for the 2026-11-20 news-image candidates.

Everything is drawn programmatically with PIL at 2x supersampling and
downscaled to 1024x1024, so text stays crisp. No AI-generated imagery.
Adapted from the 2026-11-19 entry's library, with new flags and icons
for the 20 November stories (Ukraine, Poland, Saudi Arabia, Kenya,
Estonia, markets, climate, health).
"""
from PIL import Image, ImageDraw, ImageFont

SS = 2  # supersampling factor
W = 1024

NOTO = "/usr/share/fonts/truetype/noto/"
LIB = "/usr/share/fonts/truetype/liberation/"

FONTS = {
    "sans": NOTO + "NotoSans-Regular.ttf",
    "sans_b": NOTO + "NotoSans-Bold.ttf",
    "sans_xb": NOTO + "NotoSans-ExtraBold.ttf",
    "sans_blk": NOTO + "NotoSans-Black.ttf",
    "disp_blk": NOTO + "NotoSansDisplay-Black.ttf",
    "disp_xb": NOTO + "NotoSansDisplay-ExtraBold.ttf",
    "disp_b": NOTO + "NotoSansDisplay-Bold.ttf",
    "serif": NOTO + "NotoSerif-Regular.ttf",
    "serif_b": NOTO + "NotoSerif-Bold.ttf",
    "serif_blk": NOTO + "NotoSerifDisplay-Black.ttf",
    "serif_xb": NOTO + "NotoSerifDisplay-ExtraBold.ttf",
    "lib_sans": LIB + "LiberationSans-Regular.ttf",
    "lib_sans_b": LIB + "LiberationSans-Bold.ttf",
    "lib_serif": LIB + "LiberationSerif-Regular.ttf",
    "lib_serif_b": LIB + "LiberationSerif-Bold.ttf",
}

_cache = {}


def font(kind, size):
    """size is in final (1024-space) pixels."""
    key = (kind, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FONTS[kind], int(size * SS))
    return _cache[key]


class C:
    """Canvas in 1024-space coordinates, rendered at 2x."""

    def __init__(self, bg):
        self.img = Image.new("RGB", (W * SS, W * SS), bg)
        self.d = ImageDraw.Draw(self.img, "RGBA")

    def s(self, v):
        return v * SS

    def rect(self, x, y, w, h, fill=None, outline=None, ow=1):
        self.d.rectangle([self.s(x), self.s(y), self.s(x + w), self.s(y + h)],
                         fill=fill, outline=outline, width=max(1, int(ow * SS)))

    def rrect(self, x, y, w, h, r, fill=None, outline=None, ow=1):
        self.d.rounded_rectangle([self.s(x), self.s(y), self.s(x + w), self.s(y + h)],
                                 radius=self.s(r), fill=fill, outline=outline,
                                 width=max(1, int(ow * SS)))

    def line(self, pts, fill, wdt=1):
        self.d.line([(self.s(a), self.s(b)) for a, b in pts], fill=fill,
                    width=max(1, int(wdt * SS)), joint="curve")

    def poly(self, pts, fill=None, outline=None, ow=1):
        p = [(self.s(a), self.s(b)) for a, b in pts]
        self.d.polygon(p, fill=fill, outline=outline)
        if outline and ow > 1:
            self.d.line(p + [p[0]], fill=outline, width=int(ow * SS), joint="curve")

    def ellipse(self, x, y, w, h, fill=None, outline=None, ow=1):
        self.d.ellipse([self.s(x), self.s(y), self.s(x + w), self.s(y + h)],
                       fill=fill, outline=outline, width=max(1, int(ow * SS)))

    def arc(self, x, y, w, h, a0, a1, fill, wdt=2):
        self.d.arc([self.s(x), self.s(y), self.s(x + w), self.s(y + h)],
                   a0, a1, fill=fill, width=max(1, int(wdt * SS)))

    def text_w(self, txt, kind, size):
        f = font(kind, size)
        return self.d.textlength(txt, font=f) / SS

    def text(self, x, y, txt, kind, size, fill, anchor="la", spacing=4):
        self.d.text((self.s(x), self.s(y)), txt, font=font(kind, size),
                    fill=fill, anchor=anchor, spacing=self.s(spacing))

    def fit_size(self, txt, kind, size, max_w):
        """Shrink font size until txt fits max_w (1024-space)."""
        while size > 8 and self.text_w(txt, kind, size) > max_w:
            size -= 1
        return size

    def text_fit(self, x, y, txt, kind, size, max_w, fill, anchor="la"):
        size = self.fit_size(txt, kind, size, max_w)
        self.text(x, y, txt, kind, size, fill, anchor=anchor)
        return size

    def wrap(self, txt, kind, size, max_w):
        words, lines, cur = txt.split(), [], ""
        for wd in words:
            t = (cur + " " + wd).strip()
            if self.text_w(t, kind, size) <= max_w or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines

    def para(self, x, y, txt, kind, size, max_w, fill, leading=1.28, align="left"):
        lines = self.wrap(txt, kind, size, max_w)
        for ln in lines:
            if align == "center":
                self.text(x + max_w / 2, y, ln, kind, size, fill, anchor="ma")
            elif align == "right":
                self.text(x + max_w, y, ln, kind, size, fill, anchor="ra")
            else:
                self.text(x, y, ln, kind, size, fill)
            y += size * leading
        return y

    def finish(self, path):
        out = self.img.resize((W, W), Image.LANCZOS)
        out.save(path, "PNG", optimize=True)
        return path


# ---------------------------------------------------------------- flags
def _clip_flag(c, x, y, w, h):
    mask = Image.new("L", (int(w * SS), int(h * SS)), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, int(w * SS), int(h * SS)], radius=int(6 * SS), fill=255)
    return mask


def paste_flag(c, draw_fn, x, y, w, h):
    layer = Image.new("RGB", (int(w * SS), int(h * SS)), (255, 255, 255))
    ld = ImageDraw.Draw(layer)
    draw_fn(ld, w * SS, h * SS)
    mask = _clip_flag(c, x, y, w, h)
    c.img.paste(layer, (int(x * SS), int(y * SS)), mask)
    c.d = ImageDraw.Draw(c.img, "RGBA")
    c.rrect(x, y, w, h, 6, outline=(0, 0, 0, 90), ow=1)


def _star(d, cx, cy, r, fill, rot=-90):
    import math
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.42
        a = math.radians(rot + i * 36)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)


def flag_us(d, w, h):
    sh = h / 7
    for i in range(7):
        d.rectangle([0, i * 2 * sh if i else 0, w, (2 * i + 1) * sh], fill=(178, 34, 52))
    d.rectangle([0, 0, w * 0.45, sh * 4], fill=(60, 59, 110))
    r = h * 0.045
    for row in range(4):
        for col in range(5):
            cx = w * 0.05 + col * w * 0.09
            cy = sh * 0.5 + row * sh
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255))


def flag_cn(d, w, h):
    d.rectangle([0, 0, w, h], fill=(222, 41, 16))
    _star(d, w * 0.17, h * 0.28, h * 0.17, (255, 222, 0))
    for sx, sy in [(0.36, 0.12), (0.40, 0.30), (0.40, 0.48), (0.36, 0.64)]:
        _star(d, w * sx, h * sy, h * 0.055, (255, 222, 0))


def flag_ru(d, w, h):
    d.rectangle([0, 0, w, h / 3], fill=(245, 245, 245))
    d.rectangle([0, h / 3, w, 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([0, 2 * h / 3, w, h], fill=(213, 0, 50))


def flag_ua(d, w, h):
    d.rectangle([0, 0, w, h / 2], fill=(0, 91, 187))
    d.rectangle([0, h / 2, w, h], fill=(255, 213, 0))


def flag_pl(d, w, h):
    d.rectangle([0, 0, w, h / 2], fill=(245, 245, 245))
    d.rectangle([0, h / 2, w, h], fill=(220, 20, 60))


def flag_sa(d, w, h):
    d.rectangle([0, 0, w, h], fill=(0, 108, 53))
    # stylised shahada strokes and sword line (abstract, no real script)
    for i, ww in enumerate((0.52, 0.40, 0.58, 0.34)):
        x0 = w * (0.5 - ww / 2)
        d.rectangle([x0, h * (0.22 + i * 0.11), x0 + w * ww, h * (0.27 + i * 0.11)],
                    fill=(255, 255, 255))
    d.rectangle([w * 0.16, h * 0.74, w * 0.84, h * 0.79], fill=(255, 255, 255))
    d.polygon([(w * 0.84, h * 0.715), (w * 0.92, h * 0.765), (w * 0.84, h * 0.815)],
              fill=(255, 255, 255))


def flag_ke(d, w, h):
    band = h / 3
    d.rectangle([0, 0, w, band], fill=(20, 20, 20))
    d.rectangle([0, band, w, 2 * band], fill=(187, 0, 0))
    d.rectangle([0, 2 * band, w, h], fill=(0, 105, 62))
    d.rectangle([0, band - h * 0.035, w, band + h * 0.035], fill=(255, 255, 255))
    d.rectangle([0, 2 * band - h * 0.035, w, 2 * band + h * 0.035], fill=(255, 255, 255))
    d.ellipse([w * 0.40, h * 0.10, w * 0.60, h * 0.90], fill=(187, 0, 0),
              outline=(255, 255, 255))
    d.ellipse([w * 0.465, h * 0.22, w * 0.535, h * 0.78], fill=(20, 20, 20))
    d.ellipse([w * 0.482, h * 0.30, w * 0.518, h * 0.70], fill=(255, 255, 255))


def flag_ee(d, w, h):
    d.rectangle([0, 0, w, h / 3], fill=(0, 114, 206))
    d.rectangle([0, h / 3, w, 2 * h / 3], fill=(20, 20, 20))
    d.rectangle([0, 2 * h / 3, w, h], fill=(245, 245, 245))


def flag_jp(d, w, h):
    d.rectangle([0, 0, w, h], fill=(255, 255, 255))
    d.ellipse([w * 0.36, h * 0.22, w * 0.64, h * 0.78], fill=(188, 0, 45))


FLAGS = {"us": flag_us, "cn": flag_cn, "ru": flag_ru, "ua": flag_ua,
         "pl": flag_pl, "sa": flag_sa, "ke": flag_ke, "ee": flag_ee,
         "jp": flag_jp}


def flag(c, name, x, y, w, h):
    paste_flag(c, FLAGS[name], x, y, w, h)


# ---------------------------------------------------------------- icons
def icon(c, name, x, y, size, col, col2=None):
    """Simple flat pictograms drawn inside a size x size box at (x, y)."""
    cx, cy = x + size / 2, y + size / 2
    if name == "missile":
        c.rrect(x + size * .20, y + size * .38, size * .50, size * .24, size * .10, fill=col)
        c.poly([(x + size * .70, y + size * .34), (x + size * .96, y + size * .50),
                (x + size * .70, y + size * .66)], fill=col)
        c.poly([(x + size * .24, y + size * .38), (x + size * .40, y + size * .38),
                (x + size * .30, y + size * .18)], fill=col)
        c.poly([(x + size * .24, y + size * .62), (x + size * .40, y + size * .62),
                (x + size * .30, y + size * .82)], fill=col)
        c.poly([(x + size * .20, y + size * .42), (x + size * .04, y + size * .50),
                (x + size * .20, y + size * .58)], fill=col2 or (240, 140, 40))
    elif name == "burst":
        import math
        pts = []
        for i in range(16):
            rr = size * (0.48 if i % 2 == 0 else 0.24)
            a = math.radians(i * 22.5)
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        c.poly(pts, fill=col)
        c.ellipse(cx - size * .12, cy - size * .12, size * .24, size * .24,
                  fill=col2 or (255, 220, 90))
    elif name == "chart":
        c.line([(x + size * .12, y + size * .10), (x + size * .12, y + size * .88),
                (x + size * .92, y + size * .88)], col, 4)
        c.line([(x + size * .20, y + size * .68), (x + size * .42, y + size * .50),
                (x + size * .55, y + size * .60), (x + size * .82, y + size * .26)], col2 or col, 5)
        c.poly([(x + size * .82, y + size * .14), (x + size * .90, y + size * .34),
                (x + size * .68, y + size * .32)], fill=col2 or col)
    elif name == "downchart":
        c.line([(x + size * .12, y + size * .10), (x + size * .12, y + size * .88),
                (x + size * .92, y + size * .88)], col, 4)
        c.line([(x + size * .20, y + size * .26), (x + size * .42, y + size * .44),
                (x + size * .55, y + size * .36), (x + size * .80, y + size * .68)], col2 or col, 5)
        c.poly([(x + size * .82, y + size * .52), (x + size * .88, y + size * .76),
                (x + size * .64, y + size * .70)], fill=col2 or col)
    elif name == "dome":  # capitol
        c.arc(x + size * .28, y + size * .02, size * .44, size * .44, 180, 360, col, 5)
        c.poly([(x + size * .28, y + size * .24), (x + size * .72, y + size * .24),
                (x + size * .66, y + size * .34), (x + size * .34, y + size * .34)], fill=col)
        c.rect(x + size * .46, y + size * .0, size * .08, size * .10, fill=col)
        for i in range(4):
            c.rect(x + size * (.22 + i * .15), y + size * .40, size * .07, size * .36, fill=col)
        c.rect(x + size * .12, y + size * .78, size * .76, size * .09, fill=col)
        c.rect(x + size * .08, y + size * .90, size * .84, size * .08, fill=col)
    elif name == "globe":
        c.ellipse(x + size * .06, y + size * .06, size * .88, size * .88, outline=col, ow=4)
        c.ellipse(cx - size * .18, y + size * .06, size * .36, size * .88, outline=col, ow=3)
        c.line([(x + size * .08, cy), (x + size * .92, cy)], col, 3)
        c.line([(x + size * .16, y + size * .26), (x + size * .84, y + size * .26)], col, 2)
        c.line([(x + size * .16, y + size * .74), (x + size * .84, y + size * .74)], col, 2)
    elif name == "handshake":  # three-star summit mark
        import math
        for a0 in (-90, 30, 150):
            a = math.radians(a0)
            sx, sy = cx + size * .30 * math.cos(a), cy + size * .30 * math.sin(a)
            pts = []
            for i in range(10):
                rr = size * (0.13 if i % 2 == 0 else 0.055)
                aa = math.radians(-90 + i * 36)
                pts.append((sx + rr * math.cos(aa), sy + rr * math.sin(aa)))
            c.poly(pts, fill=col)
    elif name == "tower":  # skyscraper
        c.rect(x + size * .30, y + size * .06, size * .40, size * .86, fill=col)
        c.poly([(x + size * .30, y + size * .06), (x + size * .50, y - size * .0),
                (x + size * .70, y + size * .06)], fill=col)
        for r in range(5):
            for q in range(2):
                c.rect(x + size * (.37 + q * .17), y + size * (.18 + r * .14),
                       size * .09, size * .08, fill=col2 or (255, 235, 150))
        c.rect(x + size * .16, y + size * .92, size * .68, size * .05, fill=col)
    elif name == "leaf":
        c.poly([(x + size * .18, y + size * .82), (x + size * .22, y + size * .38),
                (x + size * .52, y + size * .16), (x + size * .84, y + size * .20),
                (x + size * .80, y + size * .54), (x + size * .54, y + size * .80),
                (x + size * .30, y + size * .86)], fill=col)
        c.line([(x + size * .24, y + size * .80), (x + size * .72, y + size * .30)],
               col2 or (255, 255, 255), 4)
        c.line([(x + size * .18, y + size * .86), (x + size * .10, y + size * .94)], col, 4)
    elif name == "cross":  # medical cross in a ring
        c.ellipse(x + size * .06, y + size * .06, size * .88, size * .88, outline=col, ow=5)
        c.rect(cx - size * .09, y + size * .26, size * .18, size * .48, fill=col)
        c.rect(x + size * .26, cy - size * .09, size * .48, size * .18, fill=col)
    elif name == "shield":
        c.poly([(cx, y + size * .04), (x + size * .84, y + size * .14),
                (x + size * .84, y + size * .52), (cx, y + size * .96),
                (x + size * .16, y + size * .52), (x + size * .16, y + size * .14)], fill=col)
        c.poly([(x + size * .30, y + size * .48), (x + size * .44, y + size * .62),
                (x + size * .72, y + size * .28)], outline=None, fill=None)
        c.line([(x + size * .31, y + size * .50), (x + size * .45, y + size * .63),
                (x + size * .71, y + size * .30)], col2 or (255, 255, 255), 6)
    elif name == "people":
        for px in (0.22, 0.5, 0.78):
            c.ellipse(x + size * (px - .09), y + size * .14, size * .18, size * .18, fill=col)
            c.rrect(x + size * (px - .11), y + size * .36, size * .22, size * .34, size * .08, fill=col)
        c.line([(x + size * .10, y + size * .88), (x + size * .90, y + size * .88)], col, 3)
    elif name == "bridge":
        c.line([(x + size * .06, y + size * .66), (x + size * .94, y + size * .66)], col, 6)
        for px in (0.24, 0.5, 0.76):
            c.line([(x + size * px, y + size * .16), (x + size * px, y + size * .66)], col, 4)
        c.line([(x + size * .06, y + size * .66), (x + size * .24, y + size * .16),
                (x + size * .5, y + size * .16), (x + size * .76, y + size * .16),
                (x + size * .94, y + size * .66)], col, 3)
        c.line([(x + size * .06, y + size * .84), (x + size * .94, y + size * .84)],
               col2 or col, 3)
