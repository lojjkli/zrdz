"""All ACONITE head cosmetics. Coords are player-head pixels: head spans -4..4,
top of head is y=4, face is -z (north)."""
from mclib import Model

# ACONITE palette
AC_DARK, AC, AC_LIGHT, AC_GLOW = '#2a0f4a', '#5b2a9e', '#8a55d6', '#c49bff'
LEAF, LEAF_D, STEM = '#3f8f3a', '#255a26', '#2f6b2a'
GOLD, GOLD_D, SILVER, WHITE, BLACK = '#f2c33a', '#b8861c', '#c9ced8', '#f4f2ee', '#1d1b22'
RED, PINK, ORANGE, YELLOW, BLUE, CYAN = '#c8312d', '#f2a0c0', '#e97a24', '#f7dc3c', '#2f5fd0', '#5fe3f0'
BROWN, BROWN_D, GREY, GREEN = '#7a4a26', '#4b2d17', '#7d7f86', '#4cc34a'

D = []
def design(name, title, tier="basic"):
    def deco(fn):
        D.append((name, title, tier, fn))
        return fn
    return deco

# ---------- helpers ----------
def steps(m, cx, cz, y, widths, c, depth=None, h=1, dx=0.0, dz=0.0, smooth=2):
    """Stacked shrinking squares (cones / ears), interpolated `smooth`x finer."""
    ws = []
    for i, w in enumerate(widths):
        nxt = widths[i + 1] if i + 1 < len(widths) else w * 0.5
        ws += [w + (nxt - w) * k / smooth for k in range(smooth)]
    hh = h / smooth
    for i, w in enumerate(ws):
        dd = w if depth is None else depth
        ox, oz = cx + dx * i / smooth, cz + dz * i / smooth
        m.box(ox - w / 2, y + i * hh, oz - dd / 2, ox + w / 2, y + (i + 1) * hh, oz + dd / 2, c)

def band(m, y1, y2, c, r=4.25):
    m.box(-r, y1, -r, r, y2, -4, c); m.box(-r, y1, 4, r, y2, r, c)
    m.box(-r, y1, -4, -4, y2, 4, c); m.box(4, y1, -4, r, y2, 4, c)

def brim(m, r, y, c, t=0.5):
    m.box(-r, y, -r, r, y + t, r, c)

def cap(m, c, h=1.0):
    m.box(-4.25, 4, -4.25, 4.25, 4 + h, 4.25, c)

def ears(m, outer, inner, widths=(4, 3, 2, 1), x=2.6, tilt=0, depth=1, tuft=None):
    """Smooth triangular ears: half-pixel steps, angled outward, inner colour + fluffy tuft."""
    ws = []
    for i, w in enumerate(widths):
        nxt = widths[i + 1] if i + 1 < len(widths) else 0.3
        ws += [w, (w + nxt) / 2]
    for s in (-1, 1):
        cx = s * x
        r = ('z', -22.5 * s * 0.0 if tilt == 0 else -22.5 * s, (cx, 4, 0))
        r = r if tilt else None
        for i, w in enumerate(ws):
            off = 0 if tilt else s * 0.1 * i
            m.box(cx - w / 2 + off, 4 + i * 0.5, -depth / 2, cx + w / 2 + off, 4.5 + i * 0.5, depth / 2, outer, rot=r)
        if inner:
            for i, w in enumerate(ws[:-3]):
                iw = max(0.5, w - 1.4); off = 0 if tilt else s * 0.1 * i
                m.box(cx - iw / 2 + off, 4 + i * 0.5, -depth / 2 - 0.25, cx + iw / 2 + off, 4.5 + i * 0.5, -depth / 2, inner, rot=r)
        if tuft:
            m.box(cx - 0.6, 4, -depth / 2 - 0.5, cx + 0.6, 5.2, -depth / 2 - 0.2, tuft, rot=r)

def ring(m, y, r, c, t=0.6, h=0.6):
    m.box(-r, y, -r, r, y + h, -r + t, c); m.box(-r, y, r - t, r, y + h, r, c)
    m.box(-r, y, -r + t, -r + t, y + h, r - t, c); m.box(r - t, y, -r + t, r, y + h, r - t, c)

def aconite_spike(m, x, y, z, h=4, s=1.0):
    """Monkshood raceme: stem, then hooded blooms (helmet + lip + two side petals), smaller toward the tip."""
    m.box(x - 0.2 * s, y, z - 0.2 * s, x + 0.2 * s, y + (h + 0.6) * s, z + 0.2 * s, STEM)
    for i in range(h):
        k = (1 - 0.5 * i / h) * s
        yy = y + (0.3 + i * 1.05) * s
        m.box(x - 0.7 * k, yy, z - 0.7 * k, x + 0.7 * k, yy + 0.5 * k, z + 0.5 * k, AC_LIGHT)          # lip / lower petals
        m.box(x - 0.55 * k, yy + 0.5 * k, z - 0.85 * k, x + 0.55 * k, yy + 1.15 * k, z + 0.35 * k, AC)  # helmet
        m.box(x - 0.4 * k, yy + 1.15 * k, z - 0.75 * k, x + 0.4 * k, yy + 1.35 * k, z + 0.1 * k, AC_DARK)  # hood crest
        for sd in (-1, 1):
            m.box(x + sd * 0.55 * k, yy + 0.3 * k, z - 0.4 * k, x + sd * 0.85 * k, yy + 0.9 * k, z + 0.3 * k, AC_LIGHT)
    m.box(x - 0.3 * s, y + (h + 0.4) * s, z - 0.3 * s, x + 0.3 * s, y + (h + 0.9) * s, z + 0.3 * s, AC_GLOW)

def leaf(m, x, y, z, c=LEAF, rot=0):
    m.box(x - 0.9, y, z - 0.35, x + 0.9, y + 0.5, z + 0.35, c, rot=('y', rot, (x, y, z)) if rot else None)

# ================= ANIMAL EARS =================
for key, title, outer, inner in [("cat_ears_black", "Cat Ears (Black)", BLACK, PINK),
                                 ("cat_ears_white", "Cat Ears (White)", WHITE, PINK),
                                 ("cat_ears_ginger", "Cat Ears (Ginger)", ORANGE, '#ffd2a8'),
                                 ("cat_ears_aconite", "Cat Ears (Aconite)", AC, AC_GLOW)]:
    def f(m, o=outer, i=inner):
        ears(m, o, i, widths=(4.4, 3.6, 2.8, 2.0, 1.2), tilt=0, tuft='#f4f2ee' if o != WHITE else '#ffd6e6')
    design(key, title, "basic")(f)

@design("cat_ears_bell", "Kitty Ears + Bell", "cool")
def _(m):
    ears(m, '#3a3a40', PINK)
    band(m, 3.2, 3.8, RED, 4.2)
    m.box(-0.8, 2.0, -5.0, 0.8, 3.6, -4.2, GOLD); m.box(-0.3, 1.8, -5.1, 0.3, 2.3, -4.9, GOLD_D)

@design("fox_ears", "Fox Ears", "basic")
def _(m):
    ears(m, ORANGE, WHITE, widths=(4, 3.4, 2.6, 1.8, 1), x=2.5)
    for s in (-1, 1):
        m.box(s * 2.5 - 0.5, 9, -0.5, s * 2.5 + 0.5, 9.6, 0.5, BLACK)

@design("wolf_ears", "Wolf Ears", "basic")
def _(m):
    ears(m, GREY, '#d8d8dc', widths=(3.6, 2.8, 2, 1.2), x=2.6, tilt=0.3)

@design("bunny_ears", "Bunny Ears", "cool")
def _(m):
    m.box(-2.6, 4, -0.5, -1.0, 11, 0.5, WHITE); m.box(-2.2, 4.4, -0.7, -1.4, 10.4, -0.5, PINK)
    r = ('x', 45, (2, 8, 0))
    m.box(1.0, 4, -0.5, 2.6, 8, 0.5, WHITE)
    m.box(1.0, 8, -0.5, 2.6, 11, 0.5, WHITE, rot=r); m.box(1.4, 8, -0.7, 2.2, 10.4, -0.5, PINK, rot=r)
    m.box(1.4, 4.4, -0.7, 2.2, 8, -0.5, PINK)

@design("bear_ears", "Bear Ears", "basic")
def _(m):
    for s in (-1, 1):
        m.box(s * 3 - 1.3, 3.8, -0.6, s * 3 + 1.3, 6.4, 0.6, BROWN)
        m.box(s * 3 - 0.6, 4.3, -0.8, s * 3 + 0.6, 5.7, -0.6, '#c58a5a')

@design("panda_ears", "Panda Ears", "basic")
def _(m):
    for s in (-1, 1):
        m.box(s * 3 - 1.2, 3.8, -0.6, s * 3 + 1.2, 6.2, 0.6, BLACK)

@design("mouse_ears", "Mouse Ears", "basic")
def _(m):
    for s in (-1, 1):
        cx = s * 3.6
        m.box(cx - 2, 4.5, -0.3, cx + 2, 8.5, 0.3, '#3b3940')
        m.box(cx - 2.5, 5.0, -0.3, cx + 2.5, 8.0, 0.3, '#3b3940')
        m.box(cx - 1.4, 5.2, -0.5, cx + 1.4, 7.8, -0.3, PINK)

@design("deer_antlers", "Deer Antlers", "cool")
def _(m):
    for s in (-1, 1):
        x = s * 2.5
        m.box(x - 0.4, 4, -0.4, x + 0.4, 7, 0.4, '#d9c39a')
        m.box(x - 0.4, 6.5, -0.4, x + 0.4 + s * 2.6, 7.3, 0.4, '#d9c39a')
        m.box(x + s * 2.2 - 0.4, 7, -0.4, x + s * 2.2 + 0.4, 10, 0.4, '#d9c39a')
        m.box(x + s * 1.0 - 0.4, 7, -0.4, x + s * 1.0 + 0.4, 9, 0.4, '#d9c39a')
        m.box(x - 0.4, 7, -0.4, x + 0.4, 11, 0.4, '#d9c39a')
        m.box(x + s * 3.0 - 0.4, 6.9, -0.4, x + s * 3.0 + 0.4, 8.2, 0.4, '#d9c39a')

@design("axolotl_gills", "Axolotl Gills", "cool")
def _(m):
    for s in (-1, 1):
        for i, (dy, ln) in enumerate([(2.8, 3.0), (1.0, 3.6), (-0.8, 3.0)]):
            m.box(s * 4, dy, -0.5, s * (4 + ln), dy + 1, 0.5, '#e2588b')
            m.box(s * (3.6 + ln), dy + 1, -0.5, s * (4 + ln), dy + 1.6, 0.5, '#ff8ab4')

@design("bee_antennae", "Bee Antennae", "basic")
def _(m):
    for s in (-1, 1):
        m.box(s * 1.5 - 0.3, 4, -2.3, s * 1.5 + 0.3, 7, -1.7, BLACK, rot=('z', -22.5 * s, (s * 1.5, 4, -2)))
        m.box(s * 2.7 - 0.6, 6.6, -2.6, s * 2.7 + 0.6, 7.8, -1.4, YELLOW)

@design("alien_antennae", "Alien Antennae", "basic")
def _(m):
    for s in (-1, 1):
        m.box(s * 1.6 - 0.3, 4, -0.3, s * 1.6 + 0.3, 8, 0.3, GREEN)
        m.box(s * 1.6 - 0.8, 8, -0.8, s * 1.6 + 0.8, 9.6, 0.8, '#b6ff6b')

# ================= HORNS =================
@design("devil_horns", "Devil Horns", "basic")
def _(m):
    for s in (-1, 1):
        steps(m, s * 2.6, -1.5, 4, [1.6, 1.2, 0.8], RED, dx=s * 0.4)

@design("demon_horns", "Demon Horns", "cool")
def _(m):
    for s in (-1, 1):
        x = s * 4
        m.box(x - 0.9, 1.5, -1.2, x + s * 2.6, 3.3, 0.6, '#26222b')
        m.box(x + s * 1.6 - 0.8, 3.3, -1.0, x + s * 1.6 + 0.8, 5.3, 0.4, '#26222b')
        m.box(x + s * 1.5 - 0.6, 5.3, -0.8, x + s * 1.5 + 0.6, 7.0, 0.2, '#3a3440')
        m.box(x + s * 1.2 - 0.35, 7.0, -0.6, x + s * 1.2 + 0.35, 8.4, 0.0, '#ff4a2a')

@design("ram_horns", "Ram Horns", "cool")
def _(m):
    for s in (-1, 1):
        x = s * 4
        m.box(x, 1.5, -1.5, x + s * 1.4, 4.5, 2.5, '#cdb98f')
        m.box(x + s * 1.4, 0, -1.5, x + s * 2.6, 4.5, 1.5, '#cdb98f')
        m.box(x + s * 1.4, -1.5, -3.5, x + s * 2.6, 0.5, -1.0, '#a8925f')
        m.box(x + s * 0.4, -1.5, -4.2, x + s * 1.8, -0.3, -2.6, '#a8925f')

@design("oni_horns", "Oni Horns", "cool")
def _(m):
    for s in (-1, 1):
        steps(m, s * 2.2, -2.2, 4, [1.8, 1.4, 1.0, 0.6], '#f2ead6', dx=s * 0.2, dz=-0.2)
    band(m, 3.0, 3.8, RED)

@design("dragon_horns", "Dragon Horns", "cool")
def _(m):
    for s in (-1, 1):
        x = s * 2.6
        m.box(x - 0.9, 4, -1, x + 0.9, 5.4, 1, '#1f4a2c')
        m.box(x - 0.7, 4.6, 1, x + 0.7, 5.8, 3.4, '#1f4a2c')
        m.box(x - 0.5, 5.2, 3.4, x + 0.5, 6.2, 5.6, '#2d6b3e')
        m.box(x - 0.3, 5.8, 5.6, x + 0.3, 6.6, 7.2, '#d8c88a')
    for i, z in enumerate([-2, 0, 2, 4.2]):
        m.box(-0.3, 4, z - 0.5, 0.3, 4.8 + 0.3 * (i % 2), z + 0.5, '#7fd18a')

@design("unicorn_horn", "Unicorn Horn", "cool")
def _(m):
    cols = [GOLD, '#fff3b0', GOLD, '#fff3b0', GOLD]
    for i, w in enumerate([1.8, 1.5, 1.2, 0.9, 0.5]):
        m.box(-w / 2, 4 + i, -3.2 - w / 2 - 0.4 * i, w / 2, 5 + i, -3.2 + w / 2 - 0.4 * i, cols[i])
    for i, c in enumerate(['#ff9ad5', '#b49bff', '#8fd8ff']):
        m.box(-0.8, 4, -1.5 + i * 2, 0.8, 4.8, 0.5 + i * 2, c)

@design("crystal_horns", "Amethyst Horns", "cool")
def _(m):
    for s in (-1, 1):
        r = ('z', -22.5 * s, (s * 2.5, 4, 0))
        m.box(s * 2.5 - 0.8, 4, -0.8, s * 2.5 + 0.8, 8, 0.8, AC_LIGHT, rot=r)
        m.box(s * 2.5 - 0.5, 8, -0.5, s * 2.5 + 0.5, 9.5, 0.5, AC_GLOW, rot=r)
        m.box(s * 1.2 - 0.5, 4, -1.4, s * 1.2 + 0.5, 6, -0.4, AC, rot=('z', 22.5 * s, (s * 1.2, 4, -1)))
        m.box(s * 3.4 - 0.4, 4, 0.8, s * 3.4 + 0.4, 5.6, 1.6, AC, rot=('x', 22.5, (s * 3.4, 4, 1.2)))

@design("bone_crown", "Bone Crown", "cool")
def _(m):
    band(m, 3.0, 4.2, '#e9e1cf')
    for x, h in [(-3.5, 2.5), (-1.5, 3.5), (0.5, 4.5), (2.5, 3), (4, 2)]:
        m.box(x - 0.5, 4, -4.6, x + 0.5, 4 + h, -3.8, '#efe8d8')
        m.box(x - 0.8, 4 + h - 0.6, -4.8, x + 0.8, 4 + h, -3.6, '#d9cfb8')
    m.box(-1, 1.8, -4.9, 1, 3.6, -4.25, '#efe8d8'); m.box(-0.7, 2.4, -5.0, -0.2, 3.0, -4.85, BLACK); m.box(0.2, 2.4, -5.0, 0.7, 3.0, -4.85, BLACK)

# ================= HALOS / CROWNS =================
@design("halo", "Halo", "basic")
def _(m):
    ring(m, 6.5, 3.4, GOLD, t=0.7, h=0.5)

@design("angel_set", "Angel Halo + Wings", "cool")
def _(m):
    ring(m, 6.5, 3.4, '#fff1a0', t=0.7, h=0.5)
    for s in (-1, 1):
        m.box(s * 1.5, 0, 4.2, s * 7.5, 3, 4.8, WHITE, rot=('y', -22.5 * s, (s * 1.5, 0, 4.5)))
        m.box(s * 1.5, -2.5, 4.2, s * 6, 0, 4.8, '#e6ecf5', rot=('y', -22.5 * s, (s * 1.5, 0, 4.5)))
        m.box(s * 1.5, 3, 4.2, s * 6.5, 4.5, 4.8, '#e6ecf5', rot=('y', -22.5 * s, (s * 1.5, 0, 4.5)))

@design("ender_halo", "Ender Halo", "cool")
def _(m):
    ring(m, 6.0, 3.6, '#16101e', t=0.6, h=0.6)
    for x, z, y in [(-3.6, -3.6, 7), (3.6, 3.6, 7.5), (3.6, -3.6, 6.8), (-3.6, 3.6, 7.3)]:
        m.box(x - 0.6, y, z - 0.6, x + 0.6, y + 1.2, z + 0.6, '#c45cff')
    m.box(-0.6, 8, -0.6, 0.6, 9.2, 0.6, '#38d6b8')

@design("gold_crown", "Royal Crown", "cool")
def _(m):
    band(m, 4, 5.5, GOLD, 4.4)
    for x in (-3.9, 0, 3.9):
        for z in (-3.9, 3.9):
            m.box(x - 0.6, 5.5, z - 0.5, x + 0.6, 7, z + 0.5, GOLD)
            m.box(x - 0.35, 7, z - 0.35, x + 0.35, 7.6, z + 0.35, GOLD_D)
    for z in (0,):
        for x in (-3.9, 3.9):
            m.box(x - 0.5, 5.5, z - 0.6, x + 0.5, 7, z + 0.6, GOLD)
    m.box(-0.7, 4.3, -4.7, 0.7, 5.2, -4.4, RED)
    m.box(-2.9, 4.4, -4.6, -2.1, 5.1, -4.4, '#2fb3e0'); m.box(2.1, 4.4, -4.6, 2.9, 5.1, -4.4, '#2ed06b')
    m.box(-3.9, 4, -3.9, 3.9, 4.9, 3.9, '#7a1730')

@design("diamond_crown", "Diamond Crown", "cool")
def _(m):
    band(m, 4, 5, '#bfeff2', 4.4)
    for i, x in enumerate((-3.2, -1.6, 0, 1.6, 3.2)):
        h = [1.5, 2.2, 3.2, 2.2, 1.5][i]
        m.box(x - 0.55, 5, -4.4, x + 0.55, 5 + h, -3.6, '#4ee6e6')
        m.box(x - 0.3, 5 + h, -4.2, x + 0.3, 5.6 + h, -3.8, '#d4ffff')
    m.box(-4.4, 5, -3.6, -3.6, 6.5, 4.4, '#4ee6e6'); m.box(3.6, 5, -3.6, 4.4, 6.5, 4.4, '#4ee6e6')

@design("ice_crown", "Frost Crown", "cool")
def _(m):
    band(m, 4, 4.8, '#9ad9ff', 4.4)
    for x, z, h in [(-3.6, -4, 3), (-1.2, -4, 4.5), (1.2, -4, 3.6), (3.6, -4, 2.5), (-4, 0, 3.5), (4, 0, 3.2), (0, 4, 2.8), (-3, 4, 2), (3, 4, 2.2)]:
        steps(m, x, z, 4.8, [0.9, 0.6, 0.3][:max(1, int(h // 1.2))], '#cdefff', h=h / 3)
        m.box(x - 0.15, 4.8, z - 0.15, x + 0.15, 4.8 + h, z + 0.15, '#eaf9ff')

@design("fire_crown", "Blaze Crown", "cool")
def _(m):
    band(m, 4, 4.8, '#3a1a10', 4.4)
    cols = ['#ff4b1f', ORANGE, YELLOW, '#fff4b0']
    for x, z, h in [(-3.4, -4, 3), (-1, -4, 4.5), (1.4, -4, 3.6), (3.6, -4, 2.6), (-4, 1, 3.2), (4, 0, 3.6), (0, 4, 3), (-3, 4, 2.4), (3, 4, 2.8)]:
        for i in range(4):
            w = 1.2 - i * 0.25
            m.box(x - w / 2, 4.8 + i * h / 4, z - w / 2, x + w / 2, 4.8 + (i + 1) * h / 4, z + w / 2, cols[i])

@design("tiara", "Tiara", "basic")
def _(m):
    m.box(-3.5, 4, -2.6, 3.5, 4.4, -2.0, SILVER)
    for x, h in [(-2.4, 0.8), (-1.2, 1.2), (0, 2.0), (1.2, 1.2), (2.4, 0.8)]:
        m.box(x - 0.3, 4.4, -2.5, x + 0.3, 4.4 + h, -2.1, SILVER)
    m.box(-0.5, 5.0, -2.7, 0.5, 6.0, -2.4, PINK)

@design("laurel_wreath", "Laurel Wreath", "basic")
def _(m):
    band(m, 3.6, 4.1, GOLD_D, 4.3)
    for s in (-1, 1):
        for i, z in enumerate([-3, -1.5, 0, 1.5, 3]):
            m.box(s * 4.3 - 0.4, 3.4 + (i % 2) * 0.6, z - 0.7, s * 4.3 + 0.4, 4.1 + (i % 2) * 0.6, z + 0.7, GOLD)

# ================= FLOWERS / NATURE =================
@design("aconite_crown", "Aconite Crown", "cool")
def _(m):
    band(m, 3.6, 4.3, LEAF_D, 4.35)
    for x, z, h in [(-3, -4.2, 3), (0, -4.2, 4), (3, -4.2, 3), (-4.3, 0, 3), (4.3, 0, 3), (-2.2, 4.3, 2), (2.2, 4.3, 2)]:
        aconite_spike(m, x, 4.3, z, h=h, s=0.9)
    for x, z in [(-1.5, -4.4), (1.5, -4.4), (-4.4, -2), (4.4, 2), (0, 4.4)]:
        m.box(x - 0.8, 3.7, z - 0.4, x + 0.8, 4.2, z + 0.4, LEAF)

@design("aconite_hairpin", "Aconite Hairpin", "basic")
def _(m):
    m.box(3.9, 2, -1.6, 4.5, 2.6, 1.6, SILVER)
    aconite_spike(m, 4.6, 2.6, 0, h=4, s=0.9)
    m.box(4.4, 2.4, -2.4, 5.0, 3.0, -0.6, LEAF)

@design("aconite_bloom_hat", "Aconite Bloom Hat", "cool")
def _(m):
    # giant upside-down hood flower worn as a hat
    m.box(-4.6, 4, -4.6, 4.6, 6, 4.6, AC)
    m.box(-3.8, 6, -3.8, 3.8, 8, 3.8, AC_LIGHT)
    m.box(-2.8, 8, -3.2, 2.8, 9.6, 2.4, AC)
    m.box(-1.6, 9.6, -2.6, 1.6, 10.6, 0.8, AC_DARK)
    m.box(-4.6, 3, -4.9, 4.6, 4, -4.4, AC_DARK)
    for s in (-1, 1):
        m.box(s * 4.6 - 0.3, 3.5, -1, s * 4.6 + 0.3, 6.5, 2, LEAF)
    m.box(-0.25, 10.6, -0.9, 0.25, 12, -0.4, STEM)
    m.box(-0.5, 2.4, -5.0, 0.5, 3.0, -4.6, AC_GLOW)

@design("flower_crown", "Flower Crown", "basic")
def _(m):
    band(m, 3.6, 4.2, LEAF, 4.3)
    flowers = [(-3, -4.4, '#ff6b9a'), (0, -4.5, YELLOW), (3, -4.4, '#9ad0ff'), (-4.5, 1, '#ff6b9a'), (4.5, 1, YELLOW), (0, 4.5, '#ffffff')]
    for x, z, c in flowers:
        m.box(x - 0.8, 3.8, z - 0.8, x + 0.8, 4.8, z + 0.8, c)
        m.box(x - 0.3, 4.8, z - 0.3, x + 0.3, 5.0, z + 0.3, ORANGE)

@design("sprout", "Little Sprout", "basic")
def _(m):
    m.box(-0.25, 4, -0.25, 0.25, 6, 0.25, STEM)
    m.box(-2.2, 5.6, -0.6, -0.25, 6.2, 0.6, LEAF, rot=('z', -22.5, (-0.25, 5.8, 0)))
    m.box(0.25, 6.0, -0.6, 2.4, 6.6, 0.6, GREEN, rot=('z', 22.5, (0.25, 6.2, 0)))

@design("mushroom_red", "Red Mushroom Cap", "basic")
def _(m):
    m.box(-1.2, 4, -1.2, 1.2, 6, 1.2, '#efe6d6')
    m.box(-4.5, 6, -4.5, 4.5, 7.5, 4.5, RED)
    m.box(-3.4, 7.5, -3.4, 3.4, 8.6, 3.4, RED)
    for x, z in [(-2.5, -2), (1.5, -1.5), (0, 2), (-2.2, 2.2), (2.4, 2.4)]:
        m.box(x - 0.6, 8.6, z - 0.6, x + 0.6, 8.8, z + 0.6, WHITE)
    for x in (-3, 1, 3.5):
        m.box(x - 0.6, 6.4, -4.7, x + 0.6, 7.2, -4.5, WHITE)

@design("mushroom_brown", "Brown Mushroom", "basic")
def _(m):
    m.box(-0.8, 4, -0.8, 0.8, 5.4, 0.8, '#e8dcc6')
    m.box(-3.4, 5.4, -3.4, 3.4, 6.6, 3.4, '#9a6a45')
    m.box(-2, 6.6, -2, 2, 7.2, 2, '#b07c52')

@design("grass_block_hat", "Grass Block Hat", "basic")
def _(m):
    m.box(-2.5, 4, -2.5, 2.5, 7.5, 2.5, '#866043')
    m.box(-2.55, 6.5, -2.55, 2.55, 8, 2.55, '#5fa83a')
    m.box(-0.2, 8, -0.2, 0.2, 9, 0.2, '#76c84a')

@design("pumpkin_hat", "Mini Pumpkin", "basic")
def _(m):
    m.box(-2.6, 4, -2.6, 2.6, 7.6, 2.6, ORANGE)
    m.box(-1.8, 5, -2.8, -0.8, 6, -2.6, '#3b1c05'); m.box(0.8, 5, -2.8, 1.8, 6, -2.6, '#3b1c05')
    m.box(-1.5, 4.4, -2.8, 1.5, 4.8, -2.6, '#3b1c05')
    m.box(-0.4, 7.6, -0.4, 0.4, 8.6, 0.4, '#3b6b1c')

@design("cloud_hat", "Rain Cloud", "cool")
def _(m):
    m.box(-4, 8, -2.5, 4, 10, 2.5, '#eef2f8'); m.box(-2.5, 10, -2, 2.5, 11.4, 2, WHITE)
    m.box(-5, 8.3, -1.5, -4, 9.6, 1.5, '#dfe5ee'); m.box(4, 8.3, -1.5, 5, 9.6, 1.5, '#dfe5ee')
    for x, z, y in [(-3, -1, 6.5), (-1, 1, 5.2), (1.5, -1.5, 6.2), (3, 1, 5.6), (0, -0.5, 7)]:
        m.box(x - 0.2, y, z - 0.2, x + 0.2, y + 0.9, z + 0.2, '#5aa9ff')

@design("rainbow_arc", "Rainbow", "cool")
def _(m):
    cols = ['#ff4040', ORANGE, YELLOW, '#4cc34a', '#3b8cff', AC_LIGHT]
    for i, c in enumerate(cols):
        r = 6 - i * 0.6
        m.box(-r, 4 + r * 0.8 - 0.6, -0.3, r, 4 + r * 0.8, 0.3, c)
        for s in (-1, 1):
            m.box(s * r - 0.6 * s, 4, -0.3, s * r, 4 + r * 0.8, 0.3, c)
    for s in (-1, 1):
        m.box(s * 6.6 - 1.2, 3.4, -1, s * 6.6 + 1.2, 4.6, 1, WHITE)

# ================= HATS =================
@design("top_hat", "Top Hat", "basic")
def _(m):
    brim(m, 5.4, 4, BLACK); m.box(-3.6, 4.5, -3.6, 3.6, 10, 3.6, BLACK); m.box(-3.65, 4.5, -3.65, 3.65, 5.6, 3.65, RED)

@design("gentleman", "Gentleman (Hat + Monocle)", "cool")
def _(m):
    brim(m, 5.4, 4, '#3a2b55'); m.box(-3.6, 4.5, -3.6, 3.6, 9.5, 3.6, '#3a2b55'); m.box(-3.65, 4.5, -3.65, 3.65, 5.4, 3.65, GOLD)
    m.box(-3.4, 0.6, -4.5, -1.2, 0.9, -4.3, GOLD); m.box(-3.4, -1.5, -4.5, -1.2, -1.2, -4.3, GOLD)
    m.box(-3.4, -1.2, -4.5, -3.1, 0.6, -4.3, GOLD); m.box(-1.5, -1.2, -4.5, -1.2, 0.6, -4.3, GOLD)
    m.box(-1.4, -3.0, -4.45, -1.25, -1.5, -4.35, GOLD)

@design("wizard_hat", "Wizard Hat", "cool")
def _(m):
    brim(m, 5.6, 4, '#24308a')
    steps(m, 0, 0, 4.5, [7.4, 6.2, 5.0, 3.8, 2.8, 1.8, 1.0], '#2c3ea8', dz=0.45, h=1.1)
    m.box(-0.4, 12.2, 3, 0.4, 13, 3.8, YELLOW)
    for x, y, z in [(-2.5, 5.5, -3.75), (1.5, 7, -3.2), (-0.5, 9, -2.2), (2.8, 5.2, -3.75)]:
        m.box(x - 0.4, y - 0.4, z - 0.15, x + 0.4, y + 0.4, z, YELLOW)

@design("witch_hat", "Witch Hat", "cool")
def _(m):
    brim(m, 6.2, 4, '#1c1a24')
    steps(m, 0, 0, 4.5, [7.0, 5.6, 4.4, 3.2, 2.2, 1.4, 0.8], '#24212e', dx=-0.2, dz=0.5, h=1.0)
    band(m, 4.5, 5.4, AC, 3.6)
    m.box(-0.8, 4.6, -3.8, 0.8, 5.3, -3.65, '#8affc8')

@design("cowboy_hat", "Cowboy Hat", "basic")
def _(m):
    brim(m, 6.0, 4, BROWN, 0.6)
    for s in (-1, 1):
        m.box(s * 6, 4, -6, s * 4.6, 5.4, 6, BROWN)
    m.box(-3.6, 4.6, -3.6, 3.6, 7.8, 3.6, BROWN); m.box(-3.65, 4.6, -3.65, 3.65, 5.3, 3.65, BROWN_D)
    m.box(-0.8, 7.0, -3.6, 0.8, 7.81, 3.6, BROWN_D)

@design("beanie", "Beanie", "basic")
def _(m):
    m.box(-4.4, 2, -4.4, 4.4, 4, 4.4, '#b8333a'); m.box(-4.2, 4, -4.2, 4.2, 5.5, 4.2, '#d64a4a')
    m.box(-4.5, 1.6, -4.5, 4.5, 2.6, 4.5, '#f4e9d8')
    m.box(-1.2, 5.5, -1.2, 1.2, 7.2, 1.2, WHITE)

@design("propeller_cap", "Propeller Cap", "cool")
def _(m):
    m.box(-4.3, 3, -4.3, 0, 5.2, 0, RED); m.box(0, 3, -4.3, 4.3, 5.2, 0, YELLOW)
    m.box(-4.3, 3, 0, 0, 5.2, 4.3, BLUE); m.box(0, 3, 0, 4.3, 5.2, 4.3, GREEN)
    m.box(-4.3, 3, -7, 4.3, 3.5, -4.3, RED)
    m.box(-0.25, 5.2, -0.25, 0.25, 6.6, 0.25, GREY)
    m.box(-4, 6.4, -0.5, 4, 6.8, 0.5, '#3fc1ff', rot=('y', 22.5, (0, 6.6, 0)))

@design("baseball_cap", "Baseball Cap", "basic")
def _(m):
    cap(m, RED, 1.2); m.box(-3.6, 5.2, -3.6, 3.6, 5.8, 3.6, RED)
    m.box(-4.25, 4, -7.2, 4.25, 4.4, -4.25, '#a3201d')
    m.box(-0.4, 5.8, -0.4, 0.4, 6.1, 0.4, WHITE)

@design("backwards_cap", "Backwards Cap", "basic")
def _(m):
    cap(m, BLUE, 1.2); m.box(-3.6, 5.2, -3.6, 3.6, 5.8, 3.6, BLUE)
    m.box(-4.25, 4, 4.25, 4.25, 4.4, 7.2, '#1d3f99')
    m.box(-0.9, 4.2, 4.25, 0.9, 4.6, 4.4, WHITE)

@design("chef_hat", "Chef Hat", "basic")
def _(m):
    band(m, 3, 5, WHITE, 4.3)
    m.box(-4.6, 5, -4.6, 4.6, 9.5, 4.6, '#fbfbf7')
    for x, z in [(-2.5, -2.5), (2.5, -2.5), (-2.5, 2.5), (2.5, 2.5)]:
        m.box(x - 2.3, 9.5, z - 2.3, x + 2.3, 10.6, z + 2.3, '#f0f0ea')

@design("pirate_tricorn", "Pirate Captain", "cool")
def _(m):
    cap(m, BLACK, 1.5)
    m.box(-5.6, 5.5, -4.8, 5.6, 7.5, -4.0, BLACK)
    for s in (-1, 1):
        m.box(s * 5.6 - 0.8 * s, 5.5, -4.8, s * 5.6, 7.5, 4.8, BLACK)
    m.box(-5.6, 5.5, 4.0, 5.6, 7.5, 4.8, BLACK)
    m.box(-5.65, 5.5, -4.85, 5.65, 5.8, -3.9, GOLD)
    m.box(-0.9, 6.0, -4.95, 0.9, 7.2, -4.8, WHITE); m.box(-0.5, 5.6, -4.95, 0.5, 6.0, -4.8, WHITE)
    m.box(-4.3, 1.0, -4.5, -1.0, 2.5, -4.3, BLACK)

@design("viking_helmet", "Viking Helmet", "cool")
def _(m):
    band(m, 2.5, 4, '#8c8f99', 4.4); m.box(-4.4, 4, -4.4, 4.4, 5.5, 4.4, '#9ea2ad'); m.box(-3, 5.5, -3, 3, 6.5, 3, '#9ea2ad')
    m.box(-0.5, 2.5, -4.8, 0.5, 6.6, -4.3, BROWN_D); m.box(-0.5, -1.5, -4.8, 0.5, 2.5, -4.5, '#8c8f99')
    for s in (-1, 1):
        m.box(s * 4.4, 3.5, -1, s * 6.4, 5, 1, '#efe5c9'); m.box(s * 5.4, 5, -0.8, s * 6.6, 7.4, 0.8, '#efe5c9')
        m.box(s * 5.6, 7.4, -0.5, s * 6.4, 8.8, 0.5, '#d9cfa8')

@design("santa_hat", "Santa Hat", "basic")
def _(m):
    m.box(-4.5, 3, -4.5, 4.5, 4.4, 4.5, WHITE)
    m.box(-4, 4.4, -4, 4, 6.4, 4, RED); m.box(-3, 6.4, -2.5, 3, 7.8, 3.5, RED)
    m.box(-2, 7.8, 0, 2, 8.8, 4.5, RED); m.box(-1.2, 7.0, 4.5, 1.2, 8.6, 6.0, RED)
    m.box(-1.0, 5.8, 5.6, 1.0, 7.6, 7.4, WHITE)

@design("party_hat", "Party Hat", "basic")
def _(m):
    cols = ['#ff5ab4', '#5ad1ff', '#ffe25a', '#ff5ab4', '#5ad1ff', '#ffe25a']
    for i, w in enumerate([4.4, 3.6, 2.8, 2.0, 1.3, 0.7]):
        m.box(-w / 2 + 0.8, 4 + i, -w / 2, w / 2 + 0.8, 5 + i, w / 2, cols[i])
    m.box(0.3, 10, -0.5, 1.3, 11, 0.5, WHITE)

@design("fez", "Fez", "basic")
def _(m):
    m.box(-2.4, 4, -2.4, 2.4, 7, 2.4, '#b51d2a'); m.box(-2.1, 7, -2.1, 2.1, 7.2, 2.1, '#9c1622')
    m.box(-0.2, 7.2, -0.2, 0.2, 7.5, 0.2, BLACK); m.box(-0.2, 4.6, 2.4, 0.2, 7.5, 2.6, BLACK)

@design("beret", "Beret", "basic")
def _(m):
    m.box(-4.8, 4, -4.4, 4.0, 5.2, 4.4, '#20202a', rot=('z', 22.5, (0, 4, 0)))
    m.box(-0.2, 5.2, -0.2, 0.2, 5.8, 0.2, '#20202a', rot=('z', 22.5, (0, 4, 0)))

@design("grad_cap", "Graduation Cap", "basic")
def _(m):
    cap(m, BLACK, 1.4)
    m.box(-6, 5.4, -6, 6, 5.9, 6, BLACK, rot=('y', 45, (0, 5.4, 0)))
    m.box(-0.4, 5.9, -0.4, 0.4, 6.3, 0.4, GOLD)
    m.box(0, 6.0, -0.2, 5.0, 6.2, 0.2, GOLD, rot=('y', 45, (0, 6, 0)))
    m.box(3.3, 3.2, -3.7, 3.8, 6.0, -3.2, GOLD)

@design("knight_helmet", "Knight Helmet", "cool")
def _(m):
    m.box(-4.5, -4.5, -4.5, 4.5, 4.5, 4.5, '#a9adb8')
    m.box(-4.6, 0.2, -4.7, 4.6, 0.9, -4.5, BLACK); m.box(-0.3, -3, -4.7, 0.3, 0.2, -4.5, '#7c808b')
    m.box(-4.6, 4.5, -4.6, 4.6, 5.0, 4.6, '#7c808b')
    m.box(-0.8, 5.0, -2.5, 0.8, 7.5, 4.0, '#c8282c'); m.box(-0.7, 3.0, 4.0, 0.7, 7.0, 6.5, '#e0403f')
    for x in (-3, -2, -1, 1, 2, 3):
        m.box(x - 0.2, -2.0, -4.65, x + 0.2, -1.6, -4.5, BLACK)
    for x, y in [(-4, 3.8), (4, 3.8), (-4, -4), (4, -4)]:
        m.box(x - 0.35, y - 0.1, -4.75, x + 0.35, y + 0.6, -4.5, '#e6e8ee')
    m.box(-4.6, -4.6, -4.6, 4.6, -3.8, 4.6, '#7c808b')

@design("bucket_hat", "Bucket Hat", "basic")
def _(m):
    m.box(-5.5, 3.2, -5.5, 5.5, 3.7, 5.5, '#5e8a4e'); m.box(-4.4, 3.7, -4.4, 4.4, 6.2, 4.4, '#6f9d5d')

@design("sailor_cap", "Sailor Cap", "basic")
def _(m):
    m.box(-4.3, 4, -4.3, 4.3, 5.5, 4.3, WHITE); m.box(-4.35, 4, -4.35, 4.35, 4.7, 4.35, '#213a8f')
    m.box(-0.4, 5.5, -0.4, 0.4, 5.9, 0.4, RED)

@design("straw_hat", "Straw Hat", "basic")
def _(m):
    brim(m, 6.6, 4, '#e8c86a'); m.box(-4, 4.5, -4, 4, 7, 4, '#e8c86a'); m.box(-4.05, 4.5, -4.05, 4.05, 5.4, 4.05, RED)

@design("jester_hat", "Jester Hat", "cool")
def _(m):
    m.box(-4.4, 3, -4.4, 4.4, 5, 4.4, AC)
    m.box(-4.4, 4.4, -1, 0, 6.5, 1, AC); m.box(-7, 5.5, -0.8, -4, 8, 0.8, AC); m.box(-8, 4.5, -0.6, -6.8, 6, 0.6, AC)
    m.box(0, 4.4, -1, 4.4, 6.5, 1, GOLD); m.box(4, 5.5, -0.8, 7, 8, 0.8, GOLD); m.box(6.8, 4.5, -0.6, 8, 6, 0.6, GOLD)
    m.box(-8.6, 3.6, -0.6, -7.4, 4.8, 0.6, YELLOW); m.box(7.4, 3.6, -0.6, 8.6, 4.8, 0.6, AC_LIGHT)
    m.box(-0.7, 6.5, -0.7, 0.7, 7.9, 0.7, YELLOW)

@design("deerstalker", "Detective Cap", "basic")
def _(m):
    cap(m, '#8b6a45', 1.6)
    m.box(-3.4, 5.6, -3.4, 3.4, 6.2, 3.4, '#8b6a45')
    m.box(-3, 4, -6, 3, 4.4, -4.25, '#73563a'); m.box(-3, 4, 4.25, 3, 4.4, 6, '#73563a')
    for s in (-1, 1):
        m.box(s * 4.25, 1, -2, s * 4.6, 4, 2, '#73563a')
    m.box(-0.3, 6.2, -0.3, 0.3, 6.6, 0.3, '#5c3f26')

@design("miner_helmet", "Miner Helmet", "basic")
def _(m):
    cap(m, YELLOW, 1.8); m.box(-3.6, 5.8, -3.6, 3.6, 6.6, 3.6, YELLOW)
    m.box(-4.6, 3.8, -4.6, 4.6, 4.3, 4.6, '#d6b72a')
    m.box(-1.2, 4.4, -5.0, 1.2, 6.2, -4.25, GREY); m.box(-0.8, 4.8, -5.2, 0.8, 5.8, -5.0, '#fff6b0')

@design("astronaut", "Astronaut Helmet", "cool")
def _(m):
    for (a, b) in [((-4.8, -4.8), (-4.0, 4.8)), ((4.0, -4.8), (4.8, 4.8))]:
        m.box(a[0], -4.8, a[1], b[0], 4.8, b[1], WHITE)
    m.box(-4.8, 4.0, -4.8, 4.8, 4.8, 4.8, WHITE); m.box(-4.8, -4.8, 4.0, 4.8, 4.8, 4.8, WHITE)
    m.box(-4.0, -4.8, -4.8, 4.0, -2.8, -4.0, WHITE)
    m.box(-4.0, -2.8, -4.7, 4.0, 4.0, -4.2, '#e0a833')
    m.box(-4.9, -1, -1, -4.8, 1, 1, '#d23c3c'); m.box(4.8, -1, -1, 4.9, 1, 1, '#2f6fd8')
    m.box(2.5, 4.8, 2, 2.9, 7.5, 2.4, GREY); m.box(2.3, 7.5, 1.8, 3.1, 8.3, 2.6, RED)

@design("traffic_cone", "Traffic Cone", "basic")
def _(m):
    m.box(-3.6, 4, -3.6, 3.6, 4.5, 3.6, ORANGE)
    cols = [ORANGE, WHITE, ORANGE, WHITE, ORANGE]
    for i, w in enumerate([5, 4.2, 3.4, 2.6, 1.8]):
        m.box(-w / 2, 4.5 + i * 1.2, -w / 2, w / 2, 5.7 + i * 1.2, w / 2, cols[i])

@design("ufo_hat", "UFO", "cool")
def _(m):
    m.box(-0.2, 4, -0.2, 0.2, 6, 0.2, '#9cff7a')
    m.box(-5, 6, -5, 5, 7, 5, '#9aa1ad'); m.box(-3.5, 5.6, -3.5, 3.5, 6, 3.5, '#6f7682')
    m.box(-2.5, 7, -2.5, 2.5, 9, 2.5, '#7cfba5'); m.box(-1.5, 9, -1.5, 1.5, 9.6, 1.5, '#b6ffd0')
    for x, z in [(-4.2, 0), (4.2, 0), (0, -4.2), (0, 4.2)]:
        m.box(x - 0.4, 6.2, z - 0.4, x + 0.4, 6.8, z + 0.4, YELLOW) if False else m.box(x - 0.45, 6.9, z - 0.45, x + 0.45, 7.3, z + 0.45, YELLOW)

@design("cake_hat", "Birthday Cake", "cool")
def _(m):
    m.box(-3.5, 4, -3.5, 3.5, 6.5, 3.5, '#f3d6a4'); m.box(-3.6, 6.5, -3.6, 3.6, 7.3, 3.6, '#ffffff')
    for x, z in [(-3.6, -2), (-1, -3.6), (2, -3.6), (3.6, 1), (0, 3.6)]:
        m.box(x - 0.4, 5.6, z - 0.4, x + 0.4, 6.6, z + 0.4, '#ffffff')
    m.box(-0.8, 7.3, -0.8, 0.8, 7.8, 0.8, RED)
    m.box(-0.2, 7.8, -0.2, 0.2, 9.5, 0.2, '#7ac7ff'); m.box(-0.25, 9.5, -0.25, 0.25, 10.3, 0.25, ORANGE)

@design("tnt_hat", "TNT Hat", "cool")
def _(m):
    m.box(-2.6, 4, -2.6, 2.6, 9.2, 2.6, '#db2b1a')
    m.box(-2.65, 5.8, -2.65, 2.65, 7.4, 2.65, '#e8e2d2')
    m.box(-1.7, 6.2, -2.7, 1.7, 7.0, -2.65, BLACK)
    m.box(-2.6, 9.2, -2.6, 2.6, 9.3, 2.6, '#a9a29a')
    m.box(-0.2, 9.3, -0.2, 0.2, 10.4, 0.2, '#3b3b3b'); m.box(-0.3, 10.4, -0.3, 0.3, 11, 0.3, YELLOW)

@design("slime_buddy", "Slime Buddy", "cool")
def _(m):
    m.box(-3, 4, -3, 3, 9.5, 3, '#7fd36b'); m.box(-2, 5, -2, 2, 8.5, 2, '#5cad4b')
    m.box(-2.2, 7, -3.2, -0.8, 8.2, -3, '#244a1c'); m.box(0.8, 7, -3.2, 2.2, 8.2, -3, '#244a1c')
    m.box(-0.5, 5.6, -3.2, 0.5, 6.2, -3, '#244a1c')

@design("chick_buddy", "Chick Buddy", "basic")
def _(m):
    m.box(-2, 4, -2, 2, 7.5, 2, '#ffe14a'); m.box(-0.8, 5.4, -3.2, 0.8, 6.2, -2, ORANGE)
    m.box(-1.6, 6.4, -2.1, -0.8, 7.0, -2, BLACK); m.box(0.8, 6.4, -2.1, 1.6, 7.0, -2, BLACK)
    m.box(-0.6, 7.5, -0.6, 0.6, 8.2, 0.6, '#ffd21a')

@design("frog_buddy", "Frog Buddy", "cool")
def _(m):
    m.box(-3, 4, -3, 3, 6.4, 3, '#4fae3e'); m.box(-3, 4, -3.1, 3, 4.8, -3, '#e0607a')
    for s in (-1, 1):
        m.box(s * 1.9 - 1.0, 6.4, -2.5, s * 1.9 + 1.0, 7.8, -0.9, '#4fae3e')
        m.box(s * 1.9 - 0.6, 6.8, -2.6, s * 1.9 + 0.6, 7.6, -2.5, BLACK)
        m.box(s * 3 - 0.6, 4, -3.6, s * 3 + 0.6, 4.6, -2.2, '#3d8c30')

@design("creeper_mask", "Creeper Mask", "cool")
def _(m):
    m.box(-4.5, -4.5, -4.5, 4.5, 4.5, 4.5, '#5ec04a')
    m.box(-3, 0.5, -4.65, -1, 2.5, -4.5, BLACK); m.box(1, 0.5, -4.65, 3, 2.5, -4.5, BLACK)
    m.box(-1, -2.5, -4.65, 1, 0.5, -4.5, BLACK); m.box(-2, -3.5, -4.65, -1, -1.5, -4.5, BLACK); m.box(1, -3.5, -4.65, 2, -1.5, -4.5, BLACK)
    for x, y in [(-3.5, 3.5), (2, -4), (3.4, 2.2), (-2.5, -3.9)]:
        m.box(x, y, -4.6, x + 1, y + 0.6, -4.5, '#8ee07a')

@design("pumpkin_head", "Jack o' Lantern Head", "cool")
def _(m):
    m.box(-4.5, -4.5, -4.5, 4.5, 4.5, 4.5, '#e2852a')
    for x in (-4.5, -1.5, 1.5):
        m.box(x, -4.5, -4.6, x + 0.2, 4.5, -4.5, '#c26a18')
    m.box(-3, 0.5, -4.7, -1, 2.2, -4.5, '#ffd34a'); m.box(1, 0.5, -4.7, 3, 2.2, -4.5, '#ffd34a')
    m.box(-3, -3, -4.7, 3, -1.5, -4.5, '#ffd34a'); m.box(-0.5, -1.5, -4.7, 0.5, -1.0, -4.5, '#ffd34a')
    m.box(-0.5, 4.5, -0.5, 0.5, 6, 0.5, '#4d7a26')

# ================= EYEWEAR / FACE =================
@design("sunglasses", "Shades", "basic")
def _(m):
    m.box(-4.2, 0.4, -4.5, -0.6, 1.8, -4.25, BLACK); m.box(0.6, 0.4, -4.5, 4.2, 1.8, -4.25, BLACK)
    m.box(-0.6, 1.2, -4.5, 0.6, 1.6, -4.25, BLACK)
    for s in (-1, 1):
        m.box(s * 4.25, 1.2, -4.25, s * 4.5, 1.6, 2, BLACK)
    m.box(-3.6, 1.2, -4.55, -2.8, 1.6, -4.5, '#6a6a7a')

@design("3d_glasses", "3D Glasses", "basic")
def _(m):
    m.box(-4.3, 0.2, -4.5, 4.3, 2.2, -4.25, WHITE)
    m.box(-3.8, 0.6, -4.6, -0.8, 1.8, -4.5, '#e33a3a'); m.box(0.8, 0.6, -4.6, 3.8, 1.8, -4.5, '#3aa6e3')

@design("aviator_goggles", "Aviator Goggles", "cool")
def _(m):
    band(m, 3.6, 4.5, BROWN, 4.3)
    for s in (-1, 1):
        m.box(s * 2.1 - 1.6, 3.3, -5.2, s * 2.1 + 1.6, 5.4, -4.3, '#8a6b3e')
        m.box(s * 2.1 - 1.1, 3.7, -5.3, s * 2.1 + 1.1, 5.0, -5.2, '#f0a83a')

@design("vr_visor", "Cyber Visor", "cool")
def _(m):
    m.box(-4.6, -0.2, -5.4, 4.6, 2.6, -4.25, '#1a1d26')
    m.box(-4.0, 0.8, -5.5, 4.0, 1.4, -5.4, '#38f6ff')
    band(m, 0.6, 1.6, '#1a1d26', 4.4)
    m.box(4.4, 2.6, -1, 4.8, 6, -0.6, GREY); m.box(4.3, 6, -1.1, 4.9, 6.6, -0.5, '#38f6ff')

@design("ninja_headband", "Ninja Headband", "basic")
def _(m):
    band(m, 2.4, 3.6, RED, 4.3)
    m.box(-1.2, 2.5, -4.5, 1.2, 3.5, -4.3, SILVER)
    m.box(-1, 2.2, 4.3, -0.2, 3.2, 8, RED, rot=('x', -22.5, (0, 3, 4.3)))
    m.box(0.2, 2.0, 4.3, 1, 3.0, 7, RED, rot=('x', -45, (0, 3, 4.3)))

@design("pirate_bandana", "Bandana", "basic")
def _(m):
    m.box(-4.3, 2.4, -4.3, 4.3, 4.4, 4.3, RED)
    for x, y in [(-3, 3), (-0.5, 3.6), (2, 2.8), (3.5, 3.6)]:
        m.box(x, y, -4.4, x + 0.6, y + 0.5, -4.3, WHITE)
    m.box(-0.6, 1.4, 4.3, 0.6, 2.8, 5.6, RED)

@design("headphones", "Headphones", "basic")
def _(m):
    m.box(-4.6, 4, -0.6, 4.6, 4.8, 0.6, '#2a2a33')
    for s in (-1, 1):
        m.box(s * 4.2, 1, -0.6, s * 4.6, 4, 0.6, '#2a2a33')
        m.box(s * 4.3, -1.5, -1.8, s * 5.4, 2, 1.8, '#34343e')
        m.box(s * 5.4, -0.6, -1, s * 5.6, 1.2, 1, '#ff3d7f')

@design("cat_headphones", "Cat Headphones", "cool")
def _(m):
    m.box(-4.6, 4, -0.6, 4.6, 4.8, 0.6, '#f6f0ff')
    for s in (-1, 1):
        m.box(s * 4.2, 1, -0.6, s * 4.6, 4, 0.6, '#f6f0ff')
        m.box(s * 4.3, -1.5, -1.8, s * 5.4, 2, 1.8, '#f6f0ff')
        m.box(s * 5.4, -0.8, -1.2, s * 5.6, 1.4, 1.2, '#ff7ad1')
    for s in (-1, 1):
        for i, w in enumerate([3, 2, 1]):
            m.box(s * 2.8 - w / 2, 4.8 + i, -0.5, s * 2.8 + w / 2, 5.8 + i, 0.5, '#f6f0ff')
        m.box(s * 2.8 - 0.8, 4.8, -0.7, s * 2.8 + 0.8, 6.8, -0.5, '#ff7ad1')

# ================= SPECIAL / EPIC =================
@design("samurai_kabuto", "Samurai Kabuto", "cool")
def _(m):
    m.box(-4.5, 2, -4.5, 4.5, 5.5, 4.5, '#5c1a1f')
    m.box(-5.5, -1, -2, -4.5, 3, 4.6, '#7a2328'); m.box(4.5, -1, -2, 5.5, 3, 4.6, '#7a2328')
    m.box(-4.5, -1, 4.5, 4.5, 3, 5.5, '#7a2328')
    m.box(-4.6, 2, -4.8, 4.6, 2.6, -4.5, GOLD)
    for s in (-1, 1):
        m.box(s * 1.2 - 0.4, 5.5, -5, s * 1.2 + 0.4, 9.5, -4.6, GOLD, rot=('z', -22.5 * s, (s * 0.5, 5.5, -4.8)))
    m.box(-0.8, 4.6, -5.0, 0.8, 6.2, -4.5, '#e33a3a')

@design("phoenix_crest", "Phoenix Crest", "cool")
def _(m):
    band(m, 3.5, 4.3, GOLD_D, 4.35)
    cols = ['#ff3b1f', ORANGE, YELLOW]
    for i, (z, h) in enumerate([(-3, 3.5), (-1.5, 5), (0, 6.5), (1.5, 5.5), (3, 4)]):
        for j in range(3):
            m.box(-0.5 + j * 0.0, 4.3 + j * h / 3, z - 0.6, 0.5, 4.3 + (j + 1) * h / 3, z + 0.6, cols[j],
                  rot=('x', -22.5, (0, 4.3, z)))
    for s in (-1, 1):
        m.box(s * 4.35, 3, -2, s * 5.2, 6, -1, ORANGE, rot=('z', -22.5 * s, (s * 4.35, 3, 0)))

@design("knight_plume", "Plumed Circlet", "basic")
def _(m):
    band(m, 3.4, 4.2, SILVER, 4.35)
    m.box(-0.3, 4.2, 3.6, 0.3, 5, 4.4, SILVER)
    m.box(-0.6, 5, 3.4, 0.6, 9, 4.6, '#2a6de0', rot=('x', -22.5, (0, 5, 4)))
    m.box(-0.5, 8.5, 3.6, 0.5, 10.5, 4.4, WHITE, rot=('x', -22.5, (0, 5, 4)))

@design("snail_shell", "Snail Shell", "basic")
def _(m):
    m.box(-2.4, 4, -2.6, 2.4, 9, 2.6, '#c98b4a'); m.box(-2.5, 5, -1.6, 2.5, 8, 1.6, '#a96c33')
    m.box(-2.55, 6, -0.6, 2.55, 7, 0.6, '#e2b07a')
    for s in (-1, 1):
        m.box(s * 1 - 0.2, 4, -3.4, s * 1 + 0.2, 6, -3, '#a7b56a'); m.box(s * 1 - 0.35, 6, -3.55, s * 1 + 0.35, 6.6, -2.85, BLACK)

@design("star_antenna", "Shooting Star", "cool")
def _(m):
    m.box(-0.2, 4, 1.6, 0.2, 8.5, 2.0, GREY, rot=('x', 22.5, (0, 4, 1.8)))
    for (x1, y1, x2, y2) in [(-1.6, 9.0, 1.6, 10.0), (-0.5, 7.8, 0.5, 11.2), (-1.0, 8.2, 1.0, 10.6)]:
        m.box(x1, y1, 3.0, x2, y2, 3.8, YELLOW)
    m.box(-0.3, 9.2, 2.9, 0.3, 9.8, 3.0, '#fff8c8')
    m.box(-0.4, 9.2, 3.8, 0.4, 9.8, 6.5, '#ffe9a0')

@design("bubble_halo", "Bubble Orbit", "cool")
def _(m):
    for x, y, z, r in [(-4.5, 6, -2, 1.2), (3.5, 7, -3.5, 0.9), (4.5, 5.5, 3, 1.4), (-3, 7.5, 3.5, 0.8), (0, 8.5, 0, 1.0)]:
        m.box(x - r, y - r, z - r, x + r, y + r, z + r, '#9be7ff')
        m.box(x - r * 0.4, y + r * 0.3, z - r - 0.05, x, y + r * 0.7, z - r, WHITE)

@design("sky_island", "Floating Island", "cool")
def _(m):
    m.box(-3, 6, -3, 3, 7.5, 3, '#866043'); m.box(-3.05, 7.5, -3.05, 3.05, 8.2, 3.05, '#5fa83a')
    m.box(-2, 5, -2, 2, 6, 2, '#6e4d33'); m.box(-0.8, 4.3, -0.8, 0.8, 5, 0.8, '#5c4029')
    m.box(-1.8, 8.2, -0.3, -1.4, 10, 0.1, BROWN_D); m.box(-2.8, 9.6, -1.2, -0.4, 11.4, 1.0, '#3d8a2b')
    aconite_spike(m, 1.6, 8.2, 1.2, h=3, s=0.7)
    m.box(1.0, 8.2, -2.2, 2.2, 8.6, -1.0, '#9a9a9a')

@design("aconite_halo", "Aconite Halo", "cool")
def _(m):
    ring(m, 6.4, 3.6, AC_DARK, t=0.7, h=0.6)
    for x, z in [(-3.6, -3.6), (3.6, -3.6), (-3.6, 3.6), (3.6, 3.6), (0, -3.6), (0, 3.6), (-3.6, 0), (3.6, 0)]:
        m.box(x - 0.6, 7.0, z - 0.6, x + 0.6, 7.8, z + 0.6, AC_LIGHT)
        m.box(x - 0.3, 7.8, z - 0.3, x + 0.3, 8.2, z + 0.3, AC_GLOW)

@design("aconite_witch", "Aconite Witch Hat", "cool")
def _(m):
    brim(m, 6.2, 4, AC_DARK)
    steps(m, 0, 0, 4.5, [7.0, 5.6, 4.4, 3.2, 2.2, 1.4, 0.8], AC, dx=0.2, dz=0.5, h=1.0)
    band(m, 4.5, 5.4, LEAF_D, 3.6)
    aconite_spike(m, -3.2, 5.4, -3.2, h=3, s=0.8)
    aconite_spike(m, -2.0, 5.4, -3.7, h=2, s=0.7)

@design("plague_mask", "Plague Doctor Mask", "cool")
def _(m):
    m.box(-4.4, -2.5, -4.6, 4.4, 2.8, -4.25, '#2b2520')
    m.box(-1.2, -2.5, -8.5, 1.2, 0.3, -4.6, '#3a312a'); m.box(-0.8, -2.3, -10, 0.8, -0.3, -8.5, '#3a312a')
    for s in (-1, 1):
        m.box(s * 2.2 - 1, 0.4, -4.75, s * 2.2 + 1, 2.2, -4.6, '#d9a13a')
    cap(m, '#1d1a17', 1.6); brim(m, 5.4, 4, '#1d1a17')

@design("ghost_sheet", "Spooky Ghost", "cool")
def _(m):
    m.box(-4.6, -4, -4.6, 4.6, 4.8, 4.6, '#f2f2f6'); m.box(-3, 4.8, -3, 3, 5.6, 3, '#f2f2f6')
    for x in (-4.6, -1.6, 1.4):
        m.box(x, -5, -4.6, x + 1.6, -4, 4.6, '#e3e3ea')
    m.box(-2.8, 0.5, -4.75, -1.2, 2.5, -4.6, BLACK); m.box(1.2, 0.5, -4.75, 2.8, 2.5, -4.6, BLACK)
    m.box(-0.8, -2.5, -4.75, 0.8, -0.8, -4.6, BLACK)
