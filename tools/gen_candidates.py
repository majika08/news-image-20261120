"""Generate 10 candidate images for make.fun news-image-20261120.

The day's stories come from the verified 2026-11-20 slate in NEWS_SLATE.md
(Reuters / AP / AFP / SCMP / Jiji and other outlets, read on the day).
No invented facts or figures. All text is drawn programmatically (PIL).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from newsart import C, font, flag, icon

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "candidates")
os.makedirs(OUT, exist_ok=True)

DATE = "FRIDAY, NOVEMBER 20, 2026"

STORIES = [
    {
        "head": "RUSSIA UNLEASHES HUGE BARRAGE ON UKRAINE",
        "body": ("More than 400 drones and over 110 missiles strike Kyiv and nine regions overnight, "
                 "hours after Putin vowed revenge for Ukraine's attacks on the Crimea bridge. Eight "
                 "people are killed and 28 injured. Three bridges over the Dnipro are hit, embassies "
                 "and St Volodymyr's Cathedral are damaged, and two missiles and a drone fall inside Poland."),
        "short": ("More than 400 drones and over 110 missiles strike Kyiv and nine regions "
                  "overnight. Eight people are killed and 28 injured; three bridges over the "
                  "Dnipro are hit, embassies and a cathedral damaged. Two missiles and a drone "
                  "fall inside Poland - PM Tusk calls it a deliberate provocation."),
    },
    {
        "head": "AI SELL-OFF ROCKS GLOBAL MARKETS",
        "body": ("Japan's Nikkei plunges 4.8% to a seven-month low as AI and chip shares are dumped. "
                 "SoftBank falls 14.6%; South Korea's Kospi drops 5.2% and Taiwan 6%. US stocks fall "
                 "for a fifth straight day after Anthropic's record debut."),
    },
    {
        "head": "AFTER SHENZHEN, EUROPE PUSHES BACK",
        "body": ("Trump tells European leaders and Zelenskyy that 'Putin wants to end the war'. "
                 "Europe and Ukraine reject a 'new Yalta' and insist Kyiv must be part of any peace deal."),
    },
    {
        "head": "HOUTHI MISSILE DAMAGES RIYADH'S TALLEST TOWER",
        "body": ("A Houthi missile blows out windows across eight floors of the PIF Tower, the Saudi "
                 "wealth fund's HQ. No injuries. On Friday, Saudi air defences down another missile "
                 "and two drones."),
    },
    {
        "head": "COP31 DRAFT DROPS FOSSIL-FUEL PHASE-OUT",
        "body": ("A revised climate draft keeps a 35% electrification target but deletes the call "
                 "to phase out fossil fuels."),
    },
    {
        "head": "KENYA DECLARES EBOLA OUTBREAK OVER",
        "body": ("Kenya discharges its last Ebola patient, 37 days after the first case, and "
                 "declares the outbreak over."),
    },
    {
        "head": "WHITE HOUSE OUSTS CYBER CHIEF AFTER OUTAGE CHAOS",
        "body": ("Cyber director Sean Cairncross is fired after a week of tech failures: a Microsoft "
                 "outage, an FAA ground stop that disrupted 18,000 flights, and bank glitches. "
                 "Officials say there is no sign of a coordinated attack."),
    },
]

FOOT = [
    "ESTONIA TO CLOSE ITS RUSSIAN BORDER FOR AT LEAST SIX MONTHS",
    "EU SENDS UKRAINE €7.9 BILLION - ITS LARGEST SINGLE PAYMENT YET",
    "UK AND EU AGREE YOUTH MOBILITY SCHEME FOR 100,000 PEOPLE A YEAR",
]

INK = (20, 18, 14)
PAPER = (247, 242, 231)
RED = (179, 35, 42)
GREY = (92, 88, 80)


def save(c, name):
    path = os.path.join(OUT, name)
    c.finish(path)
    print("wrote", name)


def _column(c, x, top, width, sections):
    """A stack of tagged sections; returns the y below the last body."""
    y = top
    for i, (tag, head, body) in enumerate(sections):
        if i:
            y += 12
        c.text(x, y, tag, "sans_b", 19, RED)
        y = c.para(x, y + 24, head, "sans_xb", 26, width, INK, leading=1.14)
        y = c.para(x, y + 3, body, "serif", 20, width, INK, leading=1.26)
    return y


# ================================================================ cand 01
def cand01():
    """Classic broadsheet front page."""
    c = C(PAPER)
    c.rect(28, 22, 968, 3, fill=INK)
    c.rect(28, 31, 968, 1, fill=INK)
    c.text(512, 42, "THE WORLD TODAY", "serif_blk", 82, INK, anchor="ma")
    c.text(512, 138, "THE DAY'S NEWS IN ONE PICTURE", "sans_b", 23, GREY, anchor="ma")
    c.rect(28, 176, 968, 48, fill=INK)
    c.text(512, 186, DATE, "sans_b", 32, (255, 255, 255), anchor="ma")
    # hero
    c.text(48, 236, "KYIV, UKRAINE - ONE OF THE LARGEST ATTACKS OF THE WAR", "sans_b", 22, RED)
    y = c.para(48, 260, STORIES[0]["head"], "serif_xb", 38, 928, INK, leading=1.12)
    fx = 48
    for nm in ("ua", "ru", "pl"):
        flag(c, nm, fx, y + 4, 152, 92)
        fx += 172
    for label, dy in (("UKRAINE", 10), ("RUSSIA", 38), ("POLAND", 66)):
        c.text(fx + 4, y + dy, label, "sans_b", 21, GREY)
    y = c.para(48, y + 106, STORIES[0]["body"], "serif", 21, 928, INK, leading=1.28)
    c.rect(28, y + 6, 968, 2, fill=INK)
    # two columns
    top = y + 22
    m1 = ("Japan's Nikkei plunges 4.8% to a seven-month low as AI and chip shares are "
          "dumped. SoftBank falls 14.6%; Kospi drops 5.2%, Taiwan 6%.")
    m2 = ("A Houthi missile blows out windows across eight floors of the PIF Tower, the "
          "Saudi wealth fund's HQ. No injuries; another missile is downed on Friday.")
    left = _column(c, 48, top, 452, [
        ("MARKETS", STORIES[1]["head"], m1),
        ("CLIMATE", STORIES[4]["head"], STORIES[4]["body"]),
    ])
    right = _column(c, 524, top, 452, [
        ("MIDDLE EAST", STORIES[3]["head"], m2),
        ("AFRICA", STORIES[5]["head"], STORIES[5]["body"]),
    ])
    c.line([(512, top), (512, max(left, right))], GREY, 1)
    # bottom strip
    by = max(left, right) + 14
    c.rect(28, by, 968, 2, fill=INK)
    c.text(48, by + 10, "ALSO TODAY:", "sans_b", 21, RED)
    c.para(206, by + 10, STORIES[2]["head"] + "  ·  " + STORIES[6]["head"] + "  ·  EU SENDS UKRAINE €7.9 BILLION",
           "sans", 20, 774, INK, leading=1.28)
    save(c, "cand01.png")


# ================================================================ cand 02
def cand02():
    """Dark magazine cover."""
    BG = (13, 21, 38)
    CYAN = (55, 200, 232)
    YEL = (255, 210, 63)
    WHITE = (245, 247, 250)
    MUT = (168, 182, 200)
    c = C(BG)
    c.text(48, 36, "ONE DAY", "disp_blk", 74, WHITE)
    c.text(48, 122, "THE WORLD IN ONE PICTURE", "sans_b", 26, CYAN)
    c.rrect(48, 168, 620, 56, 8, fill=YEL)
    c.text(68, 180, DATE, "sans_b", 33, (13, 21, 38))
    # hero
    c.rrect(48, 248, 928, 300, 14, fill=(22, 34, 58), outline=(55, 200, 232), ow=2)
    for k, nm in enumerate(("ua", "ru", "pl")):
        flag(c, nm, 76 + k * 190, 276, 170, 112)
    c.text(692, 292, "8 DEAD", "disp_blk", 44, YEL)
    c.text(692, 340, "IN KYIV", "disp_blk", 44, YEL)
    c.para(76, 408, STORIES[0]["head"], "disp_xb", 32, 872, WHITE, leading=1.12)
    c.para(76, 488, "400+ drones and 110+ missiles hit Kyiv and nine regions; three bridges "
                    "damaged, embassies hit, and Russian missiles fall inside Poland.",
           "sans", 22, 872, MUT, leading=1.3)
    # 2x2 chips
    chips = [
        ("downchart", (255, 77, 94), STORIES[1]["head"], "Nikkei -4.8% as AI shares are dumped; SoftBank -14.6%"),
        ("tower", CYAN, STORIES[3]["head"], "PIF Tower windows blown out; another missile downed Friday"),
        ("handshake", (80, 220, 140), STORIES[2]["head"], "Trump: 'Putin wants to end the war'; Europe rejects a 'new Yalta'"),
        ("leaf", (200, 120, 255), STORIES[4]["head"], "Revised draft keeps 35% electrification goal, drops phase-out call"),
    ]
    pos = [(48, 572), (512, 572), (48, 756), (512, 756)]
    for (ic, colr, h, b), (px, py) in zip(chips, pos):
        c.rrect(px, py, 464, 168, 12, fill=(22, 34, 58))
        icon(c, ic, px + 26, py + 44, 76, colr)
        c.rect(px, py + 10, 8, 148, fill=colr)
        hend = c.para(px + 122, py + 16, h, "sans_b", 23, 326, WHITE, leading=1.14)
        c.para(px + 122, max(py + 84, hend + 4), b, "sans", 20, 326, MUT, leading=1.25)
    c.para(48, 946, "ALSO: " + STORIES[5]["head"] + "  ·  " + STORIES[6]["head"] + "  ·  " + FOOT[0],
           "sans_b", 20, 928, CYAN, leading=1.25)
    save(c, "cand02.png")


# ================================================================ cand 03
def cand03():
    """Panel grid with hero."""
    BG = (238, 241, 245)
    SLATE = (30, 41, 59)
    c = C(BG)
    c.rect(0, 0, 1024, 118, fill=SLATE)
    c.text(40, 22, "THE WORLD ON", "disp_b", 30, (148, 184, 220))
    c.text(40, 52, DATE, "disp_xb", 42, (255, 255, 255))
    c.text(984, 40, "ONE DAY\nONE PICTURE", "sans_b", 22, (148, 184, 220), anchor="ra")
    # hero panel
    c.rrect(32, 138, 960, 252, 12, fill=(255, 255, 255))
    c.rect(32, 138, 960, 10, fill=(197, 48, 49))
    for k, nm in enumerate(("ua", "ru", "pl")):
        flag(c, nm, 60 + k * 148, 168, 132, 88)
    c.text(524, 178, "KYIV · OVERNIGHT BARRAGE", "sans_b", 21, (197, 48, 49))
    c.para(524, 204, STORIES[0]["head"], "disp_xb", 31, 440, SLATE, leading=1.12)
    c.para(60, 278, STORIES[0]["short"], "sans", 21, 904, (51, 65, 85), leading=1.28)
    panels = [
        ("downchart", (197, 48, 49), 1, "The Nikkei plunges 4.8% to a seven-month low; SoftBank -14.6%, Kospi -5.2%, Taiwan -6%. US stocks fall a fifth straight day."),
        ("handshake", (217, 119, 6), 2, "Trump tells allies 'Putin wants to end the war'. Europe and Ukraine reject a 'new Yalta'; Kyiv must be in any deal."),
        ("tower", (37, 99, 235), 3, "A Houthi missile blows out windows on eight floors of the PIF Tower. No injuries; another missile is downed on Friday."),
        ("leaf", (5, 150, 105), 4, "A revised climate draft keeps a 35% electrification target but deletes the call to phase out fossil fuels."),
        ("cross", (124, 58, 237), 5, "Kenya discharges its last Ebola patient, 37 days after the first case, and declares the outbreak over."),
        ("shield", (13, 148, 136), 6, "Cyber director Sean Cairncross is fired after a week of outages hit Microsoft, the FAA and banks. No sign of an attack."),
    ]
    pw, ph = 468, 168
    for i, (ic, colr, si, b) in enumerate(panels):
        px = 32 + (i % 2) * (pw + 24)
        py = 410 + (i // 2) * (ph + 16)
        c.rrect(px, py, pw, ph, 10, fill=(255, 255, 255))
        icon(c, ic, px + 20, py + 52, 62, colr)
        c.rect(px, py, pw, 8, fill=colr)
        c.para(px + 100, py + 18, STORIES[si]["head"], "sans_b", 22, 348, SLATE, leading=1.14)
        c.para(px + 100, py + 82, b, "sans", 18, 348, (71, 85, 105), leading=1.24)
    fy = 410 + 3 * (ph + 16) + 2
    c.para(32, fy, "ALSO TODAY:  " + FOOT[0] + "  ·  " + FOOT[1], "sans_b", 20, 960, SLATE, leading=1.25)
    save(c, "cand03.png")


# ================================================================ cand 04
def cand04():
    """Ranked timeline."""
    BG = (250, 246, 238)
    c = C(BG)
    c.text(56, 34, "20 NOVEMBER 2026", "disp_blk", 76, (26, 26, 26))
    c.text(58, 124, "FRIDAY - THE DAY'S BIGGEST STORIES, RANKED", "sans_b", 26, RED)
    c.rect(56, 168, 912, 3, fill=(26, 26, 26))
    items = [
        ("KYIV", STORIES[0]["head"], "400+ drones and 110+ missiles; 8 killed, 28 injured. Bridges, embassies and a cathedral hit; missiles fall in Poland."),
        ("TOKYO", STORIES[1]["head"], "Nikkei -4.8% to a seven-month low; SoftBank -14.6%. Kospi -5.2%, Taiwan -6%; US stocks fall a fifth day."),
        ("SHENZHEN", STORIES[2]["head"], "Trump tells allies 'Putin wants to end the war'; Europe and Ukraine reject a 'new Yalta'."),
        ("RIYADH", STORIES[3]["head"], "Houthi missile damages the PIF Tower; no injuries. Another missile downed on Friday."),
        ("CLIMATE TALKS", STORIES[4]["head"], "Revised draft keeps a 35% electrification target, deletes the fossil-fuel phase-out call."),
        ("NAIROBI", STORIES[5]["head"], "Last Ebola patient discharged, 37 days after the first case; outbreak declared over."),
        ("WASHINGTON", STORIES[6]["head"], "Cyber chief fired after outages at Microsoft, the FAA and banks; no sign of an attack."),
        ("TALLINN", "ESTONIA TO CLOSE RUSSIAN BORDER FOR SIX MONTHS", "Moscow denounces the move as a new 'Iron Curtain'."),
    ]
    y = 190
    x0 = 108
    tx, tw = 168, 800
    ys = []
    for i, (tag, h, b) in enumerate(items):
        ys.append(y)
        c.text(tx, y - 2, tag, "sans_b", 18, RED)
        c.para(tx, y + 19, h, "sans_xb", 24, tw, (26, 26, 26), leading=1.1)
        y = c.para(tx, y + 50, b, "sans", 19, tw, (80, 74, 66), leading=1.2) + 13
    c.line([(x0, ys[0] + 12), (x0, ys[-1] + 12)], (200, 190, 170), 3)
    for i, yy in enumerate(ys):
        c.ellipse(x0 - 21, yy + 2, 42, 42, fill=RED if i == 0 else (26, 26, 26))
        c.text(x0, yy + 9, str(i + 1), "sans_b", 24, (255, 255, 255), anchor="ma")
    c.rect(56, y + 2, 912, 2, fill=(26, 26, 26))
    c.para(56, y + 12, "ALSO: " + FOOT[1] + "  ·  " + FOOT[2], "sans_b", 18, 912, (80, 74, 66), leading=1.25)
    save(c, "cand04.png")


# ================================================================ cand 05
def _pairs(text):
    pts = []
    for pair in text.split():
        a, b = pair.split(",")
        pts.append((float(a), float(b)))
    return pts


def _quads(text):
    out = []
    for quad in text.split():
        a, b, c, d = quad.split(",")
        out.append((float(a), float(b), float(c), float(d)))
    return out


# Rough continent outlines as "lon,lat" pairs, parsed at run time.
NA = _pairs("-168,66 -140,70 -125,72 -108,73 -95,79 -86,70 -80,73 -77,68 -85,66 "
            "-93,66 -95,60 -90,58 -82,55 -79,51 -65,50 -60,46 -70,44 -74,40 -76,35 "
            "-81,31 -80,26 -84,30 -90,29 -97,26 -97,22 -94,18 -90,15 -83,9 -79,9 "
            "-86,13 -92,15 -97,16 -102,18 -105,20 -110,23 -114,29 -120,34 -124,40 "
            "-124,47 -130,54 -140,60 -155,60 -166,60")
SA = _pairs("-79,9 -72,12 -64,10 -55,6 -50,0 -44,-3 -35,-8 -39,-13 -40,-20 -48,-26 "
            "-56,-35 -62,-39 -65,-41 -67,-46 -69,-50 -68,-54 -71,-54 -73,-46 -73,-37 "
            "-71,-30 -70,-20 -75,-15 -79,-8 -81,-4 -80,1 -77,4")
AF = _pairs("-6,35 0,36 10,37 20,32 30,31 33,27 35,24 38,22 40,15 43,12 48,11 51,12 "
            "48,5 42,-2 40,-10 39,-18 36,-22 33,-26 28,-33 20,-35 17,-32 15,-27 13,-18 "
            "12,-10 13,-5 9,-1 9,4 4,6 -3,5 -8,5 -13,8 -17,12 -17,15 -16,20 -15,25 "
            "-13,28 -10,31")
EU = _pairs("-9,37 -9,43 -2,48 0,51 5,53 8,55 8,57 5,59 5,61 11,65 16,68 25,71 35,69 "
            "45,68 60,69 75,72 90,75 105,77 120,73 135,72 150,70 165,70 178,66 178,63 "
            "168,60 160,56 156,51 150,45 142,42 140,38 135,34 129,33 126,35 122,30 "
            "120,24 114,22 108,17 106,9 104,6 100,7 98,13 94,17 91,22 88,21 85,19 "
            "80,14 77,8 74,13 72,19 67,24 61,25 57,26 54,26 51,28 49,30 50,26 55,24 "
            "59,22 55,17 52,15 45,12 43,12 40,15 39,20 36,24 34,28 35,31 36,36 30,36 "
            "27,37 23,36 19,40 16,40 12,44 8,44 3,43 0,39 -2,37")
AU = _pairs("113,-22 114,-28 115,-34 118,-35 124,-33 129,-32 132,-32 135,-35 138,-35 "
            "140,-38 145,-38 147,-39 150,-37 153,-32 153,-27 151,-24 149,-20 146,-19 "
            "145,-15 143,-11 142,-11 141,-13 140,-18 139,-20 136,-15 135,-12 132,-11 "
            "129,-14 126,-14 122,-17 118,-20 114,-22")
ISLANDS = _quads("138,37,7,5 -2,54,3.5,4 113,-1,15,3 122,13,3.5,4.5 172,-42,3.5,5 "
                 "47,-19,3,6 102,0,4,3 95,5,3,3 129,33,3,2.5 23,65,4,3")
HOLES = _quads("51,43,5.5,4 35,43.5,6,2.8 -86,60,7,5 48,29,4,2.5")


def _in_poly(lon, lat, poly):
    inside = False
    prev = poly[-1]
    for cur in poly:
        xi, yi = cur
        xj, yj = prev
        if (yi > lat) != (yj > lat) and lon < (xj - xi) * (lat - yi) / (yj - yi) + xi:
            inside = not inside
        prev = cur
    return inside


def _in_ellipse(lon, lat, clon, clat, rx, ry):
    dx = (lon - clon) / rx
    dy = (lat - clat) / ry
    return dx * dx + dy * dy <= 1.0


def _land(lon, lat):
    for hole in HOLES:
        if _in_ellipse(lon, lat, *hole):
            return False
    if any(_in_poly(lon, lat, poly) for poly in (NA, SA, AF, EU, AU)):
        return True
    return any(_in_ellipse(lon, lat, *spot) for spot in ISLANDS)


def cand05():
    """World map with numbered pins + legend."""
    c = C((234, 243, 251))
    c.rect(0, 0, 1024, 116, fill=(23, 58, 94))
    c.text(40, 18, DATE, "disp_xb", 40, (255, 255, 255))
    c.text(40, 68, "THE DAY ON THE MAP - THE WORLD'S NEWS, WHERE IT HAPPENED", "sans_b", 22, (150, 197, 240))
    mx0, my0, mw, mh = 24, 132, 976, 470
    step = 15.5
    cols = int(mw / step)
    rows = int(mh / step)
    for r in range(rows):
        lat = 80 - (r + 0.5) * (140 / rows)
        for col in range(cols):
            lon = -180 + (col + 0.5) * (360 / cols)
            if _land(lon, lat):
                cx = mx0 + (col + 0.5) * step
                cy = my0 + (r + 0.5) * step
                c.ellipse(cx - 4.4, cy - 4.4, 8.8, 8.8, fill=(47, 107, 178))

    def pin(num, lon, lat):
        x = mx0 + (lon + 180) / 360 * mw
        y = my0 + (80 - lat) / 140 * mh
        c.ellipse(x - 17, y - 17, 34, 34, fill=(197, 48, 49), outline=(255, 255, 255), ow=3)
        c.text(x, y - 13, str(num), "sans_b", 22, (255, 255, 255), anchor="ma")

    for num, lon, lat in ((1, 30.5, 50.4), (2, 139.7, 35.7), (3, 114.1, 22.5),
                          (4, 46.7, 24.6), (5, 36.8, -1.3), (6, -77.0, 38.9)):
        pin(num, lon, lat)
    leg = [
        ("1", "KYIV - Russia's huge barrage: 400+ drones, 110+ missiles; 8 killed; missiles fall in Poland"),
        ("2", "TOKYO - Nikkei plunges 4.8% as the AI sell-off spreads across Asia"),
        ("3", "SHENZHEN - After the summit, Europe rejects a 'new Yalta' on Ukraine"),
        ("4", "RIYADH - Houthi missile damages the PIF Tower, the city's tallest"),
        ("5", "NAIROBI - Kenya declares its Ebola outbreak over; last patient discharged"),
        ("6", "WASHINGTON - White House ousts its cyber chief after a week of tech outages"),
    ]
    y = 622
    for num, txt in leg:
        c.ellipse(40, y, 30, 30, fill=(197, 48, 49))
        c.text(55, y + 3, num, "sans_b", 19, (255, 255, 255), anchor="ma")
        y = c.para(84, y + 2, txt, "sans_b", 21, 900, (23, 43, 66), leading=1.18) + 7
    c.rrect(32, y + 2, 960, 52, 8, fill=(23, 58, 94))
    c.text_fit(512, y + 15, "ALSO: COP31 DRAFT DROPS FOSSIL-FUEL PHASE-OUT  ·  ESTONIA TO SHUT RUSSIAN BORDER",
               "sans_b", 22, 920, (255, 255, 255), anchor="ma")
    save(c, "cand05.png")


# ================================================================ cand 06
def cand06():
    """Tabloid."""
    c = C((255, 255, 255))
    c.rect(0, 0, 1024, 14, fill=(208, 2, 27))
    c.text(40, 26, "WORLD DAILY", "disp_blk", 88, (208, 2, 27))
    c.rrect(770, 40, 214, 52, 6, fill=(208, 2, 27))
    c.text(877, 52, "EXTRA! EXTRA!", "sans_b", 26, (255, 255, 255), anchor="ma")
    c.rect(0, 132, 1024, 58, fill=(255, 221, 0))
    c.text(512, 143, DATE, "sans_b", 36, (10, 10, 10), anchor="ma")
    c.text(40, 204, "KYIV, UKRAINE", "sans_b", 24, (208, 2, 27))
    hs = c.fit_size("400 DRONES. 110 MISSILES.", "disp_blk", 64, 944)
    c.text(40, 234, "400 DRONES. 110 MISSILES.", "disp_blk", hs, (10, 10, 10))
    for k, nm in enumerate(("ua", "ru", "pl")):
        flag(c, nm, 40 + k * 192, 316, 170, 112)
    c.para(630, 322, "Russia fires 400+ drones and 110+ missiles at Ukraine. Eight die in "
                     "Kyiv and Lviv; bridges and embassies are hit, and missiles fall in Poland.",
           "sans", 22, 354, (40, 40, 40), leading=1.3)
    chips = [("-4.8%", "NIKKEI PLUNGES AS AI SELL-OFF SPREADS"),
             ("8 DEAD", "IN RUSSIA'S HUGE BARRAGE ON UKRAINE"),
             ("€7.9BN", "EU'S LARGEST SINGLE PAYMENT TO UKRAINE")]
    for k, (big, cap) in enumerate(chips):
        cx = 40 + k * 324
        c.rrect(cx, 476, 296, 126, 10, fill=(16, 16, 16))
        c.text(cx + 148, 488, big, "disp_blk", 50, (255, 221, 0), anchor="ma")
        c.para(cx + 14, 546, cap, "sans_b", 16, 268, (255, 255, 255), leading=1.2, align="center")
    for sx, head, body in (
        (40, STORIES[1]["head"], "AI and chip shares are dumped across Asia: SoftBank -14.6%, Kospi -5.2%, "
         "Taiwan -6%. US stocks fall for a fifth straight day."),
        (532, STORIES[3]["head"], "A Houthi missile blows out windows on eight floors of the PIF Tower. "
         "No injuries; another missile is downed on Friday."),
    ):
        c.rect(sx, 622, 452, 6, fill=(208, 2, 27))
        c.para(sx, 640, head, "disp_xb", 28, 452, (10, 10, 10), leading=1.12)
        c.para(sx, 716, body, "sans", 21, 452, (50, 50, 50), leading=1.28)
    c.rect(40, 856, 944, 108, fill=(240, 240, 240))
    c.para(56, 872, "ALSO TODAY: " + STORIES[2]["head"] + "  ·  " + STORIES[4]["head"] + "  ·  " + STORIES[5]["head"] + "  ·  " + STORIES[6]["head"],
           "sans_b", 21, 912, (10, 10, 10), leading=1.3)
    save(c, "cand06.png")


# ================================================================ cand 07
def cand07():
    """Swiss minimal."""
    c = C((255, 255, 255))
    INK2 = (17, 17, 17)
    ACC = (226, 0, 26)
    c.text(44, 8, "20", "disp_blk", 300, INK2)
    c.text(470, 66, "NOVEMBER", "disp_blk", 74, INK2)
    c.text(470, 148, "2026", "disp_blk", 74, INK2)
    c.text(472, 236, "FRIDAY", "disp_xb", 44, ACC)
    c.text(44, 330, DATE, "sans_b", 30, INK2)
    c.rect(44, 378, 936, 6, fill=ACC)
    rows = [
        (0, "400+ drones and 110+ missiles; 8 killed, 28 injured. Bridges and embassies hit; missiles fall in Poland."),
        (1, "Nikkei -4.8% to a seven-month low; SoftBank -14.6%. Kospi -5.2%, Taiwan -6%; US stocks fall a fifth day."),
        (2, "Trump: 'Putin wants to end the war'. Europe and Ukraine reject a 'new Yalta'."),
        (3, "Houthi missile damages the PIF Tower; no injuries. Another missile downed Friday."),
        (4, "Revised draft keeps a 35% electrification target, deletes the phase-out call."),
        (5, "Last Ebola patient discharged, 37 days after the first case."),
        (6, "Cyber chief fired after outages at Microsoft, the FAA and banks."),
    ]
    y = 404
    for si, b in rows:
        c.rect(44, y + 6, 16, 16, fill=ACC)
        c.para(80, y, STORIES[si]["head"], "sans_b", 25, 900, INK2, leading=1.1)
        y = c.para(80, y + 32, b, "sans", 21, 900, (90, 90, 90), leading=1.22) + 13
    c.rect(44, y + 2, 936, 2, fill=INK2)
    c.para(44, y + 12, FOOT[0] + "  ·  " + FOOT[1], "sans", 20, 936, (90, 90, 90), leading=1.3)
    save(c, "cand07.png")


# ================================================================ cand 08
def cand08():
    """TV news broadcast."""
    c = C((8, 26, 56))
    for i in range(1024):  # vertical gradient
        t = i / 1024
        col = (int(10 + 6 * t), int(34 + 10 * t), int(74 + 26 * t))
        c.line([(0, i), (1024, i)], col, 1)
    c.rect(0, 0, 330, 92, fill=(200, 16, 46))
    c.text(24, 16, "WORLD NEWS", "disp_blk", 44, (255, 255, 255))
    c.text(24, 64, "ONE DAY IN ONE PICTURE", "sans_b", 17, (255, 190, 200))
    c.text_fit(984, 18, DATE, "sans_b", 30, 620, (255, 255, 255), anchor="ra")
    c.rrect(880, 56, 104, 30, 4, fill=(255, 255, 255))
    c.text(932, 61, "LIVE", "sans_b", 20, (200, 16, 46), anchor="ma")
    # main panel
    c.rrect(32, 116, 640, 560, 10, fill=(255, 255, 255, 22), outline=(120, 170, 230), ow=2)
    c.rect(32, 116, 640, 54, fill=(200, 16, 46))
    c.text(52, 128, "BREAKING NEWS", "disp_xb", 32, (255, 255, 255))
    for k, nm in enumerate(("ua", "ru", "pl")):
        flag(c, nm, 56 + k * 170, 192, 150, 100)
    c.para(56, 312, "RUSSIA'S HUGE BARRAGE ON UKRAINE KILLS EIGHT", "disp_xb", 36,
           592, (255, 255, 255), leading=1.14)
    c.para(56, 428, "More than 400 drones and 110 missiles hit Kyiv and nine regions. Three "
                    "bridges and two embassies are damaged, and Russian missiles fall inside "
                    "Poland. Putin had vowed revenge for the Crimea bridge attacks.",
           "sans", 23, 592, (205, 222, 245), leading=1.32)
    c.text(56, 622, "KYIV, UKRAINE", "sans_b", 21, (255, 210, 63))
    # right rail
    rail = [
        ((255, 77, 94), 1, "Nikkei -4.8%; SoftBank -14.6%; Kospi -5.2%, Taiwan -6%."),
        ((255, 170, 60), 3, "PIF Tower windows blown out; no injuries reported."),
        ((90, 200, 250), 2, "Trump: 'Putin wants a deal'; Europe rejects a 'new Yalta'."),
    ]
    for k, (colr, si, b) in enumerate(rail):
        ry = 116 + k * 192
        c.rrect(696, ry, 296, 176, 10, fill=(255, 255, 255, 22))
        c.rect(696, ry, 296, 8, fill=colr)
        c.para(714, ry + 20, STORIES[si]["head"], "sans_b", 21, 262, (255, 255, 255), leading=1.15)
        c.para(714, ry + 92, b, "sans", 19, 262, (190, 208, 235), leading=1.25)
    # ticker
    c.rect(0, 692, 1024, 196, fill=(5, 5, 8))
    c.rect(0, 692, 170, 196, fill=(255, 210, 63))
    c.text(85, 742, "THE", "disp_blk", 30, (5, 5, 8), anchor="ma")
    c.text(85, 778, "LATEST", "disp_blk", 30, (5, 5, 8), anchor="ma")
    tick = ("COP31 DRAFT DROPS FOSSIL-FUEL PHASE-OUT  +++  KENYA DECLARES EBOLA OUTBREAK OVER  "
            "+++  WHITE HOUSE OUSTS CYBER CHIEF AFTER OUTAGE CHAOS  +++  ESTONIA TO CLOSE "
            "RUSSIAN BORDER FOR SIX MONTHS  +++  EU SENDS UKRAINE €7.9 BILLION")
    c.para(192, 710, tick, "sans_b", 22, 800, (255, 255, 255), leading=1.3)
    c.para(32, 906, "PLUS: UK AND EU AGREE A YOUTH MOBILITY SCHEME FOR 100,000 PEOPLE A YEAR",
           "sans", 20, 960, (160, 190, 225), leading=1.3)
    save(c, "cand08.png")


# ================================================================ cand 09
def cand09():
    """Poster: hero barrage + ALSO ON FRIDAY list."""
    c = C((16, 28, 48))
    c.rect(0, 0, 1024, 84, fill=(8, 8, 10))
    c.text(512, 20, DATE, "disp_xb", 40, (255, 255, 255), anchor="ma")
    for k, nm in enumerate(("ua", "ru", "pl")):
        flag(c, nm, 232 + k * 200, 104, 170, 108)
    c.text(512, 232, "A NIGHT OF FIRE", "disp_blk", 58, (255, 255, 255), anchor="ma")
    c.text(512, 298, "OVER KYIV", "disp_blk", 58, (255, 210, 63), anchor="ma")
    c.para(112, 368, "Russia fires more than 400 drones and 110 missiles at Ukraine in one of "
                     "the largest attacks of the war. Eight people are killed; bridges, "
                     "embassies and a cathedral are hit in Kyiv, and missiles fall in Poland.",
           "sans", 21, 800, (200, 214, 235), leading=1.32, align="center")
    # bottom cream zone
    c.rect(0, 492, 1024, 532, fill=(247, 242, 231))
    c.text(48, 510, "ALSO ON FRIDAY", "disp_xb", 30, (179, 35, 42))
    items = [
        (1, "Nikkei -4.8% to a seven-month low; SoftBank -14.6%; Kospi -5.2%, Taiwan -6%."),
        (2, "Trump: 'Putin wants to end the war'; Europe rejects a 'new Yalta'."),
        (3, "PIF Tower damaged in Riyadh; no injuries; another missile downed Friday."),
        (4, "Revised draft keeps 35% electrification goal, drops the phase-out call."),
        (5, "Last Ebola patient discharged, 37 days after the first case."),
        (6, "Cyber chief fired after outages at Microsoft, the FAA and banks."),
    ]
    y = 556
    for si, b in items:
        c.text(48, y, str(si + 1), "disp_blk", 27, (179, 35, 42))
        c.para(92, y + 1, STORIES[si]["head"], "sans_b", 22, 884, (20, 18, 14), leading=1.1)
        c.para(92, y + 28, b, "sans", 19, 884, (92, 88, 80), leading=1.2)
        y += 57
    c.rect(48, y + 4, 928, 2, fill=(179, 35, 42))
    c.para(48, y + 14, "PLUS: " + FOOT[0] + "  ·  " + FOOT[1], "sans_b", 18, 928, (92, 88, 80), leading=1.25)
    save(c, "cand09.png")


# ================================================================ cand 10
def _mini_tile(c, x, y, w, h, bg, ic, icol, head, body, bcol):
    c.rect(x, y, w, h, fill=bg)
    icon(c, ic, x + 24, y + 34, 74, icol)
    hend = c.para(x + 112, y + 20, head, "sans_b", 21, 216, (255, 255, 255), leading=1.15)
    c.para(x + 112, hend + 5, body, "sans", 18, 216, bcol, leading=1.25)


def cand10():
    """Mondrian mosaic of colour tiles."""
    c = C((24, 24, 24))
    W_ = (255, 255, 255)
    c.rect(0, 0, 1024, 118, fill=(10, 10, 10))
    c.text(36, 22, DATE, "disp_xb", 42, W_)
    c.text(36, 74, "THE DAY'S WORLD NEWS IN ONE PICTURE", "sans_b", 21, (255, 210, 63))
    # hero tile
    c.rect(0, 118, 648, 296, fill=(23, 58, 94))
    for k, nm in enumerate(("ua", "ru", "pl")):
        flag(c, nm, 30 + k * 124, 142, 108, 72)
    c.text(426, 152, "BARRAGE", "disp_blk", 34, (255, 210, 63))
    c.text(426, 190, "KYIV", "sans_b", 19, W_)
    c.para(30, 232, STORIES[0]["head"], "disp_xb", 30, 590, W_, leading=1.12)
    c.para(30, 306, "400+ drones and 110+ missiles; 8 killed. Bridges hit - and missiles fall in Poland.",
           "sans", 20, 590, (190, 214, 240), leading=1.25)
    # markets tile
    c.rect(648, 118, 376, 296, fill=(150, 20, 30))
    c.text(836, 140, "-4.8%", "disp_blk", 84, W_, anchor="ma")
    c.para(678, 240, "NIKKEI PLUNGES IN AI SELL-OFF", "sans_b", 25, 316, W_, leading=1.15, align="center")
    c.para(678, 306, "SoftBank -14.6%, Kospi -5.2%, Taiwan -6% as AI shares are dumped",
           "sans", 20, 316, (255, 205, 210), leading=1.25, align="center")
    # riyadh tile
    c.rect(0, 414, 512, 216, fill=(0, 105, 62))
    icon(c, "tower", 28, 470, 92, W_, (255, 235, 150))
    hend = c.para(140, 436, STORIES[3]["head"], "sans_b", 25, 348, W_, leading=1.14)
    c.para(140, hend + 8, "PIF Tower windows blown out across eight floors; no injuries.",
           "sans", 20, 348, (205, 245, 220), leading=1.25)
    # diplomacy tile
    c.rect(512, 414, 512, 216, fill=(194, 102, 10))
    icon(c, "handshake", 540, 470, 92, W_, (255, 230, 120))
    hend = c.para(652, 436, STORIES[2]["head"], "sans_b", 25, 348, W_, leading=1.14)
    c.para(652, hend + 8, "Trump: 'Putin wants to end the war'. Europe rejects a 'new Yalta'.",
           "sans", 20, 348, (255, 232, 205), leading=1.25)
    # small tiles
    _mini_tile(c, 0, 630, 341, 216, (10, 116, 116), "leaf", W_,
               "COP31 DROPS PHASE-OUT CALL",
               "Draft keeps 35% electrification goal, deletes fossil-fuel phase-out.",
               (200, 240, 240))
    _mini_tile(c, 341, 630, 342, 216, (88, 50, 160), "cross", W_,
               "KENYA: EBOLA OVER",
               "Last patient discharged, 37 days after the first case.",
               (220, 205, 250))
    _mini_tile(c, 683, 630, 341, 216, (40, 40, 46), "shield", (255, 210, 63),
               "CYBER CHIEF OUSTED",
               "Fired after a week of outages at Microsoft, the FAA and banks.",
               (210, 210, 215))
    # bottom strip
    c.rect(0, 846, 1024, 178, fill=(52, 52, 56))
    c.para(30, 862, FOOT[0], "sans_b", 23, 964, W_, leading=1.12)
    c.para(30, 900, "ALSO: " + FOOT[1] + "  ·  " + FOOT[2],
           "sans", 20, 964, (205, 205, 210), leading=1.3)
    save(c, "cand10.png")


if __name__ == "__main__":
    for make in (cand01, cand02, cand03, cand04, cand05,
                 cand06, cand07, cand08, cand09, cand10):
        make()
    print("done")
