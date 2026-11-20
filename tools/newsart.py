"""Programmatic drawing kit for the 20 November 2026 news image.

The picture is painted in code: a 1024x1024 canvas rendered at twice the
size with PIL, then downscaled, so text and pictograms stay sharp. No part
of the image comes from a generative model.
"""
from PIL import Image, ImageDraw, ImageFont

SS = 2
W = 1024

_NOTO = "/usr/share/fonts/truetype/noto/"
_LIB = "/usr/share/fonts/truetype/liberation/"

_FONT_TABLE = (
    ("sans", _NOTO, "NotoSans-Regular.ttf"),
    ("sans_b", _NOTO, "NotoSans-Bold.ttf"),
    ("sans_xb", _NOTO, "NotoSans-ExtraBold.ttf"),
    ("sans_blk", _NOTO, "NotoSans-Black.ttf"),
    ("disp_blk", _NOTO, "NotoSansDisplay-Black.ttf"),
    ("disp_xb", _NOTO, "NotoSansDisplay-ExtraBold.ttf"),
    ("disp_b", _NOTO, "NotoSansDisplay-Bold.ttf"),
    ("serif", _NOTO, "NotoSerif-Regular.ttf"),
    ("serif_b", _NOTO, "NotoSerif-Bold.ttf"),
    ("serif_blk", _NOTO, "NotoSerifDisplay-Black.ttf"),
    ("serif_xb", _NOTO, "NotoSerifDisplay-ExtraBold.ttf"),
    ("lib_sans", _LIB, "LiberationSans-Regular.ttf"),
    ("lib_sans_b", _LIB, "LiberationSans-Bold.ttf"),
    ("lib_serif", _LIB, "LiberationSerif-Regular.ttf"),
    ("lib_serif_b", _LIB, "LiberationSerif-Bold.ttf"),
)
FONTS = {name: folder + fname for name, folder, fname in _FONT_TABLE}

_cache = {}


def font(kind, size):
    """A font at ``size`` final pixels (rendered at 2x)."""
    key = (kind, size)
    got = _cache.get(key)
    if got is None:
        got = ImageFont.truetype(FONTS[kind], int(size * SS))
        _cache[key] = got
    return got


def _scale(v):
    return v * SS


class C:
    """A canvas in 1024-space, painted at 2x and shrunk on finish."""

    def __init__(self, bg):
        self.img = Image.new("RGB", (W * SS, W * SS), bg)
        self.d = ImageDraw.Draw(self.img, "RGBA")

    def s(self, v):
        return _scale(v)

    def _box(self, x, y, w, h):
        return [_scale(x), _scale(y), _scale(x + w), _scale(y + h)]

    def _pts(self, pts):
        return [(_scale(a), _scale(b)) for a, b in pts]

    def _w(self, ow):
        return max(1, int(ow * SS))

    def rect(self, x, y, w, h, fill=None, outline=None, ow=1):
        self.d.rectangle(self._box(x, y, w, h), fill=fill, outline=outline,
                         width=self._w(ow))

    def rrect(self, x, y, w, h, r, fill=None, outline=None, ow=1):
        self.d.rounded_rectangle(self._box(x, y, w, h), radius=_scale(r),
                                 fill=fill, outline=outline, width=self._w(ow))

    def line(self, pts, fill, wdt=1):
        self.d.line(self._pts(pts), fill=fill, width=self._w(wdt), joint="curve")

    def poly(self, pts, fill=None, outline=None, ow=1):
        p = self._pts(pts)
        self.d.polygon(p, fill=fill, outline=outline)
        if outline and ow > 1:
            self.d.line(p + [p[0]], fill=outline, width=int(ow * SS), joint="curve")

    def ellipse(self, x, y, w, h, fill=None, outline=None, ow=1):
        self.d.ellipse(self._box(x, y, w, h), fill=fill, outline=outline,
                       width=self._w(ow))

    def arc(self, x, y, w, h, a0, a1, fill, wdt=2):
        self.d.arc(self._box(x, y, w, h), a0, a1, fill=fill, width=self._w(wdt))

    def text_w(self, txt, kind, size):
        return self.d.textlength(txt, font=font(kind, size)) / SS

    def text(self, x, y, txt, kind, size, fill, anchor="la", spacing=4):
        self.d.text((_scale(x), _scale(y)), txt, font=font(kind, size),
                    fill=fill, anchor=anchor, spacing=_scale(spacing))

    def fit_size(self, txt, kind, size, max_w):
        while size > 8 and self.text_w(txt, kind, size) > max_w:
            size -= 1
        return size

    def text_fit(self, x, y, txt, kind, size, max_w, fill, anchor="la"):
        size = self.fit_size(txt, kind, size, max_w)
        self.text(x, y, txt, kind, size, fill, anchor=anchor)
        return size

    def wrap(self, txt, kind, size, max_w):
        lines = []
        cur = ""
        for wd in txt.split():
            t = (cur + " " + wd).strip()
            if not cur or self.text_w(t, kind, size) <= max_w:
                cur = t
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines

    def para(self, x, y, txt, kind, size, max_w, fill, leading=1.28, align="left"):
        for ln in self.wrap(txt, kind, size, max_w):
            anchor = {"center": "ma", "right": "ra"}.get(align, "la")
            if align == "center":
                xx = x + max_w / 2
            elif align == "right":
                xx = x + max_w
            else:
                xx = x
            self.text(xx, y, ln, kind, size, fill, anchor=anchor)
            y += size * leading
        return y

    def finish(self, path):
        out = self.img.resize((W, W), Image.LANCZOS)
        out.save(path, "PNG", optimize=True)
        return path


# ---------------------------------------------------------------- flags
def _star_points(cx, cy, r, rot=-90, points=10, inner=0.42):
    import math
    pts = []
    for i in range(points):
        rr = r if i % 2 == 0 else r * inner
        a = math.radians(rot + i * (360 / points))
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts


def _hstripes(d, w, h, colors):
    n = len(colors)
    for i, col in enumerate(colors):
        d.rectangle([0, h * i / n, w, h * (i + 1) / n], fill=col)


# name -> equal horizontal bands, top to bottom
_BANDS = {
    "ru": ((245, 245, 245), (0, 57, 166), (213, 0, 50)),
    "ua": ((0, 91, 187), (255, 213, 0)),
    "pl": ((245, 245, 245), (220, 20, 60)),
    "ee": ((0, 114, 206), (20, 20, 20), (245, 245, 245)),
}


def _flag_bands(d, w, h, name):
    _hstripes(d, w, h, _BANDS[name])


def _flag_us(d, w, h):
    sh = h / 7
    for i in range(7):
        d.rectangle([0, 2 * i * sh, w, (2 * i + 1) * sh], fill=(178, 34, 52))
    d.rectangle([0, 0, w * 0.45, sh * 4], fill=(60, 59, 110))
    r = h * 0.045
    dots = [(w * 0.05 + col * w * 0.09, sh * 0.5 + row * sh)
            for row in range(4) for col in range(5)]
    for cx, cy in dots:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255))


def _flag_cn(d, w, h):
    d.rectangle([0, 0, w, h], fill=(222, 41, 16))
    d.polygon(_star_points(w * 0.17, h * 0.28, h * 0.17), fill=(255, 222, 0))
    for sx, sy in ((0.36, 0.12), (0.40, 0.30), (0.40, 0.48), (0.36, 0.64)):
        d.polygon(_star_points(w * sx, h * sy, h * 0.055), fill=(255, 222, 0))


def _flag_sa(d, w, h):
    # stylised shahada strokes and sword line (abstract, no real script)
    d.rectangle([0, 0, w, h], fill=(0, 108, 53))
    bars = [(ww, 0.22 + i * 0.11, 0.27 + i * 0.11)
            for i, ww in enumerate((0.52, 0.40, 0.58, 0.34))]
    for ww, y0, y1 in bars:
        x0 = w * (0.5 - ww / 2)
        d.rectangle([x0, h * y0, x0 + w * ww, h * y1], fill=(255, 255, 255))
    d.rectangle([w * 0.16, h * 0.74, w * 0.84, h * 0.79], fill=(255, 255, 255))
    tip = [(w * 0.84, h * 0.715), (w * 0.92, h * 0.765), (w * 0.84, h * 0.815)]
    d.polygon(tip, fill=(255, 255, 255))


def _flag_ke(d, w, h):
    band = h / 3
    for i, col in enumerate(((20, 20, 20), (187, 0, 0), (0, 105, 62))):
        d.rectangle([0, band * i, w, band * (i + 1)], fill=col)
    for edge in (band, 2 * band):
        d.rectangle([0, edge - h * 0.035, w, edge + h * 0.035], fill=(255, 255, 255))
    d.ellipse([w * 0.40, h * 0.10, w * 0.60, h * 0.90], fill=(187, 0, 0),
              outline=(255, 255, 255))
    d.ellipse([w * 0.465, h * 0.22, w * 0.535, h * 0.78], fill=(20, 20, 20))
    d.ellipse([w * 0.482, h * 0.30, w * 0.518, h * 0.70], fill=(255, 255, 255))


def _flag_jp(d, w, h):
    d.rectangle([0, 0, w, h], fill=(255, 255, 255))
    disc = (w * 0.36, h * 0.22, w * 0.64, h * 0.78)
    d.ellipse(disc, fill=(188, 0, 45))


_SPECIAL_FLAGS = {
    "us": _flag_us,
    "cn": _flag_cn,
    "sa": _flag_sa,
    "ke": _flag_ke,
    "jp": _flag_jp,
}


def _flag_mask(w, h):
    mask = Image.new("L", (int(w * SS), int(h * SS)), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, int(w * SS), int(h * SS)], radius=int(6 * SS), fill=255)
    return mask


def paste_flag(c, draw_fn, x, y, w, h):
    layer = Image.new("RGB", (int(w * SS), int(h * SS)), (255, 255, 255))
    draw_fn(ImageDraw.Draw(layer), w * SS, h * SS)
    c.img.paste(layer, (int(x * SS), int(y * SS)), _flag_mask(w, h))
    c.d = ImageDraw.Draw(c.img, "RGBA")
    c.rrect(x, y, w, h, 6, outline=(0, 0, 0, 90), ow=1)


def flag(c, name, x, y, w, h):
    if name in _BANDS:
        fn = lambda d, ww, hh: _flag_bands(d, ww, hh, name)
    else:
        fn = _SPECIAL_FLAGS[name]
    paste_flag(c, fn, x, y, w, h)


# ---------------------------------------------------------------- icons
def _icon_missile(c, x, y, size, col, col2):
    u = size
    body = (x + u * .20, y + u * .38, u * .50, u * .24)
    c.rrect(body[0], body[1], body[2], body[3], u * .10, fill=col)
    nose = [(x + u * .70, y + u * .34), (x + u * .96, y + u * .50),
            (x + u * .70, y + u * .66)]
    c.poly(nose, fill=col)
    for fy in (.38, .62):
        tip = .18 if fy < .5 else .82
        fin = [(x + u * .24, y + u * fy), (x + u * .40, y + u * fy),
               (x + u * .30, y + u * tip)]
        c.poly(fin, fill=col)
    flame = [(x + u * .20, y + u * .42), (x + u * .04, y + u * .50),
             (x + u * .20, y + u * .58)]
    c.poly(flame, fill=col2 or (240, 140, 40))


def _icon_burst(c, x, y, size, col, col2):
    cx, cy = x + size / 2, y + size / 2
    pts = _star_points(cx, cy, size * 0.48, rot=0, points=16, inner=0.5)
    c.poly(pts, fill=col)
    r = size * .12
    c.ellipse(cx - r, cy - r, r * 2, r * 2, fill=col2 or (255, 220, 90))


def _icon_chart(c, x, y, size, col, col2):
    u = size
    axes = [(x + u * .12, y + u * .10), (x + u * .12, y + u * .88),
            (x + u * .92, y + u * .88)]
    c.line(axes, col, 4)
    trend = [(x + u * .20, y + u * .68), (x + u * .42, y + u * .50),
             (x + u * .55, y + u * .60), (x + u * .82, y + u * .26)]
    c.line(trend, col2 or col, 5)
    head = [(x + u * .82, y + u * .14), (x + u * .90, y + u * .34),
            (x + u * .68, y + u * .32)]
    c.poly(head, fill=col2 or col)


def _icon_downchart(c, x, y, size, col, col2):
    u = size
    axes = [(x + u * .12, y + u * .10), (x + u * .12, y + u * .88),
            (x + u * .92, y + u * .88)]
    c.line(axes, col, 4)
    trend = [(x + u * .20, y + u * .26), (x + u * .42, y + u * .44),
             (x + u * .55, y + u * .36), (x + u * .80, y + u * .68)]
    c.line(trend, col2 or col, 5)
    head = [(x + u * .82, y + u * .52), (x + u * .88, y + u * .76),
            (x + u * .64, y + u * .70)]
    c.poly(head, fill=col2 or col)


def _icon_dome(c, x, y, size, col, col2):
    u = size
    c.arc(x + u * .28, y + u * .02, u * .44, u * .44, 180, 360, col, 5)
    roof = [(x + u * .28, y + u * .24), (x + u * .72, y + u * .24),
            (x + u * .66, y + u * .34), (x + u * .34, y + u * .34)]
    c.poly(roof, fill=col)
    c.rect(x + u * .46, y + u * .0, u * .08, u * .10, fill=col)
    cols = [x + u * (.22 + i * .15) for i in range(4)]
    for cx in cols:
        c.rect(cx, y + u * .40, u * .07, u * .36, fill=col)
    for bx, bw, by, bh in ((.12, .76, .78, .09), (.08, .84, .90, .08)):
        c.rect(x + u * bx, y + u * by, u * bw, u * bh, fill=col)


def _icon_globe(c, x, y, size, col, col2):
    u = size
    cx, cy = x + u / 2, y + u / 2
    outer = (x + u * .06, y + u * .06, u * .88, u * .88)
    c.ellipse(*outer, outline=col, ow=4)
    inner = (cx - u * .18, y + u * .06, u * .36, u * .88)
    c.ellipse(*inner, outline=col, ow=3)
    c.line([(x + u * .08, cy), (x + u * .92, cy)], col, 3)
    for yy in (.26, .74):
        c.line([(x + u * .16, y + u * yy), (x + u * .84, y + u * yy)], col, 2)


def _icon_handshake(c, x, y, size, col, col2):
    import math
    cx, cy = x + size / 2, y + size / 2
    for a0 in (-90, 30, 150):
        a = math.radians(a0)
        sx = cx + size * .30 * math.cos(a)
        sy = cy + size * .30 * math.sin(a)
        c.poly(_star_points(sx, sy, size * 0.13, inner=0.055 / 0.13), fill=col)


def _icon_tower(c, x, y, size, col, col2):
    u = size
    c.rect(x + u * .30, y + u * .06, u * .40, u * .86, fill=col)
    roof = [(x + u * .30, y + u * .06), (x + u * .50, y - u * .0),
            (x + u * .70, y + u * .06)]
    c.poly(roof, fill=col)
    wins = [(x + u * (.37 + q * .17), y + u * (.18 + r * .14))
            for r in range(5) for q in range(2)]
    for wx, wy in wins:
        c.rect(wx, wy, u * .09, u * .08, fill=col2 or (255, 235, 150))
    c.rect(x + u * .16, y + u * .92, u * .68, u * .05, fill=col)


def _icon_leaf(c, x, y, size, col, col2):
    u = size
    blade = [(x + u * .18, y + u * .82), (x + u * .22, y + u * .38),
             (x + u * .52, y + u * .16), (x + u * .84, y + u * .20),
             (x + u * .80, y + u * .54), (x + u * .54, y + u * .80),
             (x + u * .30, y + u * .86)]
    c.poly(blade, fill=col)
    c.line([(x + u * .24, y + u * .80), (x + u * .72, y + u * .30)],
           col2 or (255, 255, 255), 4)
    c.line([(x + u * .18, y + u * .86), (x + u * .10, y + u * .94)], col, 4)


def _icon_cross(c, x, y, size, col, col2):
    u = size
    cx, cy = x + u / 2, y + u / 2
    ring = (x + u * .06, y + u * .06, u * .88, u * .88)
    c.ellipse(*ring, outline=col, ow=5)
    bars = ((cx - u * .09, y + u * .26, u * .18, u * .48),
            (x + u * .26, cy - u * .09, u * .48, u * .18))
    for bx, by, bw, bh in bars:
        c.rect(bx, by, bw, bh, fill=col)


def _icon_shield(c, x, y, size, col, col2):
    u = size
    cx = x + u / 2
    outline = [(cx, y + u * .04), (x + u * .84, y + u * .14),
               (x + u * .84, y + u * .52), (cx, y + u * .96),
               (x + u * .16, y + u * .52), (x + u * .16, y + u * .14)]
    c.poly(outline, fill=col)
    # NB: a polygon with no fill and no outline still inks its edge in
    # PIL (white here), and the entry image was rendered with it: keep it.
    c.poly([(x + u * .30, y + u * .48), (x + u * .44, y + u * .62),
            (x + u * .72, y + u * .28)], outline=None, fill=None)
    tick = [(x + u * .31, y + u * .50), (x + u * .45, y + u * .63),
            (x + u * .71, y + u * .30)]
    c.line(tick, col2 or (255, 255, 255), 6)


def _icon_people(c, x, y, size, col, col2):
    u = size
    for px in (0.22, 0.5, 0.78):
        hx = x + u * (px - .09)
        c.ellipse(hx, y + u * .14, u * .18, u * .18, fill=col)
        bx = x + u * (px - .11)
        c.rrect(bx, y + u * .36, u * .22, u * .34, u * .08, fill=col)
    c.line([(x + u * .10, y + u * .88), (x + u * .90, y + u * .88)], col, 3)


def _icon_bridge(c, x, y, size, col, col2):
    u = size
    deck = [(x + u * .06, y + u * .66), (x + u * .94, y + u * .66)]
    c.line(deck, col, 6)
    for px in (0.24, 0.5, 0.76):
        c.line([(x + u * px, y + u * .16), (x + u * px, y + u * .66)], col, 4)
    arch = [(x + u * .06, y + u * .66), (x + u * .24, y + u * .16),
            (x + u * .5, y + u * .16), (x + u * .76, y + u * .16),
            (x + u * .94, y + u * .66)]
    c.line(arch, col, 3)
    c.line([(x + u * .06, y + u * .84), (x + u * .94, y + u * .84)],
           col2 or col, 3)


_ICONS = {
    "missile": _icon_missile,
    "burst": _icon_burst,
    "chart": _icon_chart,
    "downchart": _icon_downchart,
    "dome": _icon_dome,
    "globe": _icon_globe,
    "handshake": _icon_handshake,
    "tower": _icon_tower,
    "leaf": _icon_leaf,
    "cross": _icon_cross,
    "shield": _icon_shield,
    "people": _icon_people,
    "bridge": _icon_bridge,
}


def icon(c, name, x, y, size, col, col2=None):
    """A flat pictogram drawn inside a size x size box at (x, y)."""
    _ICONS[name](c, x, y, size, col, col2)
