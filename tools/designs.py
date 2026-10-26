"""All ACONITE head cosmetics. Coords are player-head pixels: head spans -4..4,
top of head is y=4, face is -z (north)."""
from mclib import Model, GLOW

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


# ======================================================================
# Quality pass: richer versions of the simpler accessories (replace originals)
# ======================================================================
def redesign(name):
    def deco(fn):
        for i, (n, t, tier, _) in enumerate(D):
            if n == name:
                D[i] = (n, t, tier, fn)
                return fn
        raise KeyError(name)
    return deco

def rbox(m, x1, y1, z1, x2, y2, z2, c, r=0.5, top=True, rot=None):
    """Soft box: chamfered vertical edges and an inset top, so shapes read as rounded."""
    r = min(r, (x2 - x1) / 3, (z2 - z1) / 3, (y2 - y1) / 2)
    m.box(x1 + r, y1, z1, x2 - r, y2 - (r if top else 0), z2, c, rot=rot)
    m.box(x1, y1, z1 + r, x2, y2 - (r if top else 0), z2 - r, c, rot=rot)
    if top:
        m.box(x1 + r, y2 - r, z1 + r, x2 - r, y2, z2 - r, c, rot=rot)

def dome(m, y, layers, c, cz=0.0):
    """Rounded crown from soft layers: layers = [(half_width, height), ...] bottom to top."""
    for hw, h in layers:
        rbox(m, -hw, y, cz - hw, hw, y + h, cz + hw, c, r=min(1.0, hw / 3), top=False)
        y += h
    return y

def flower(m, x, y, z, petal, centre=YELLOW, s=1.0, face='n'):
    """5-part flower facing outward: centre + 4 petals."""
    t = 0.3 * s
    if face == 'n':
        m.box(x - 0.35 * s, y - 0.35 * s, z - t, x + 0.35 * s, y + 0.35 * s, z, centre)
        for dx, dy in ((-0.7, 0), (0.7, 0), (0, -0.7), (0, 0.7)):
            m.box(x + dx * s - 0.38 * s, y + dy * s - 0.38 * s, z - t * 0.6, x + dx * s + 0.38 * s, y + dy * s + 0.38 * s, z + 0.05, petal)
    else:  # facing up
        m.box(x - 0.35 * s, y, z - 0.35 * s, x + 0.35 * s, y + t, z + 0.35 * s, centre)
        for dx, dz in ((-0.7, 0), (0.7, 0), (0, -0.7), (0, 0.7)):
            m.box(x + dx * s - 0.38 * s, y - 0.05, z + dz * s - 0.38 * s, x + dx * s + 0.38 * s, y + t * 0.6, z + dz * s + 0.38 * s, petal)

@redesign("bear_ears")
def _(m):
    for s in (-1, 1):
        x = s * 3.0
        rbox(m, x - 1.6, 3.8, -0.8, x + 1.6, 7.0, 0.8, BROWN, r=0.7)
        rbox(m, x - 0.9, 4.4, -1.0, x + 0.9, 6.3, -0.8, '#d9a46f', r=0.4, top=False)
    m.box(-4.6, 3.6, -0.8, 4.6, 4.3, 0.8, BROWN_D)

@redesign("panda_ears")
def _(m):
    for s in (-1, 1):
        x = s * 3.0
        rbox(m, x - 1.5, 3.8, -0.8, x + 1.5, 6.8, 0.8, '#1f1d24', r=0.7)
        rbox(m, x - 0.8, 4.4, -1.0, x + 0.8, 6.1, -0.8, '#3a3742', r=0.35, top=False)
    m.box(-4.6, 3.6, -0.8, 4.6, 4.3, 0.8, WHITE)

@redesign("bee_antennae")
def _(m):
    for i, x in enumerate([-4.6, -2.3, 0, 2.3]):
        m.box(x, 3.4, -4.6, x + 2.3, 4.4, 4.6, YELLOW if i % 2 == 0 else BLACK)
    m.box(-4.6, 3.4, 4.6, 4.6, 4.4, 4.7, YELLOW)
    for s in (-1, 1):
        r = ('z', -22.5 * s, (s * 1.5, 4.4, -2))
        m.box(s * 1.5 - 0.25, 4.4, -2.25, s * 1.5 + 0.25, 7.6, -1.75, BLACK, rot=r)
        m.box(s * 2.6 - 0.8, 7.0, -2.8, s * 2.6 + 0.8, 8.6, -1.2, YELLOW)
        m.box(s * 2.6 - 0.5, 8.6, -2.5, s * 2.6 + 0.5, 8.9, -1.5, '#fff08a')
    for s in (-1, 1):  # little wings at the back
        m.box(s * 0.6, 2.0, 4.7, s * 3.6, 5.2, 5.0, '#cfeaff', rot=('y', 22.5 * s, (s * 0.6, 3.6, 4.85)))

@redesign("devil_horns")
def _(m):
    for s in (-1, 1):
        x = s * 2.5
        rbox(m, x - 1.0, 4.0, -2.4, x + 1.0, 5.4, -0.6, '#8e1c1a', r=0.4)
        m.box(x - 0.75 + s * 0.3, 5.4, -2.2, x + 0.75 + s * 0.3, 6.6, -0.8, '#b82623')
        m.box(x - 0.55 + s * 0.7, 6.6, -2.0, x + 0.55 + s * 0.7, 7.6, -1.0, RED)
        m.box(x - 0.35 + s * 1.2, 7.6, -1.8, x + 0.35 + s * 1.2, 8.4, -1.2, '#ff5a3d')
        m.box(x - 0.2 + s * 1.6, 8.4, -1.65, x + 0.2 + s * 1.6, 8.9, -1.35, '#ffb199')

@redesign("halo")
def _(m):
    ring(m, 6.6, 3.6, GOLD, t=0.9, h=0.7)
    ring(m, 6.75, 3.0, '#fff1a0', t=0.3, h=0.45)
    for x, z, y in [(-3.9, -3.9, 7.6), (3.9, 3.9, 7.4), (3.9, -3.9, 7.8), (-3.9, 3.9, 7.5)]:
        m.box(x - 0.25, y, z - 0.25, x + 0.25, y + 0.8, z + 0.25, '#fff4b0')
        m.box(x - 0.5, y + 0.15, z - 0.1, x + 0.5, y + 0.65, z + 0.1, '#fff4b0')

@redesign("tiara")
def _(m):
    m.box(-4.0, 4.0, -3.0, 4.0, 4.6, -2.2, SILVER)
    for x, h in [(-3.2, 1.0), (-2.0, 1.6), (-0.8, 2.4), (0.8, 2.4), (2.0, 1.6), (3.2, 1.0)]:
        m.box(x - 0.25, 4.6, -2.9, x + 0.25, 4.6 + h, -2.3, SILVER)
        m.box(x - 0.35, 4.6 + h, -3.0, x + 0.35, 5.0 + h, -2.2, '#e8f4ff')
    m.box(-1.0, 4.6, -2.9, 1.0, 6.6, -2.3, SILVER)
    m.box(-0.7, 5.3, -3.1, 0.7, 6.5, -2.9, '#ff6fae'); m.box(-0.35, 6.6, -2.9, 0.35, 7.3, -2.3, '#ffd0e6')
    for x in (-2.6, 2.6):
        m.box(x - 0.35, 4.75, -3.1, x + 0.35, 5.35, -2.9, '#8fd8ff')
    for s in (-1, 1):
        m.box(s * 4.0, 4.0, -3.0, s * 4.6, 4.6, -1.0, SILVER)

@redesign("laurel_wreath")
def _(m):
    band(m, 3.4, 3.9, GOLD_D, 4.5)
    for s in (-1, 1):
        for i, z in enumerate([-3.6, -2.4, -1.2, 0, 1.2, 2.4]):
            y = 3.9 + 0.12 * i
            r = ('x', 22.5, (s * 4.6, y, z))
            m.box(s * 4.6 - 0.35, y, z - 0.6, s * 4.6 + 0.35, y + 0.5, z + 0.6, GOLD, rot=r)
            m.box(s * 5.0 - 0.3, y - 0.4, z - 0.4, s * 5.0 + 0.3, y + 0.1, z + 0.6, '#ffd95a', rot=r)
    m.box(-0.8, 3.2, 4.6, 0.8, 4.0, 5.0, RED)
    for s in (-1, 1):
        m.box(s * 0.4 - 0.3, 1.6, 4.7, s * 0.4 + 0.3, 3.2, 4.9, RED, rot=('z', 22.5 * s, (s * 0.4, 3.2, 4.8)))

@redesign("aconite_hairpin")
def _(m):
    m.box(4.6, 1.6, -2.4, 5.0, 2.2, 2.0, SILVER); m.box(4.6, 1.0, 1.6, 5.0, 2.2, 2.0, SILVER)
    for z, h, sc in [(-0.6, 5, 1.1), (1.0, 3, 0.85)]:
        aconite_spike(m, 5.3, 2.2, z, h=h, s=sc)
    for z in (-1.8, 0.2):
        m.box(4.9, 2.0, z - 0.9, 6.4, 2.4, z + 0.9, LEAF, rot=('x', 22.5, (5.6, 2.2, z)))
        m.box(5.0, 2.4, z - 0.4, 6.2, 2.6, z + 0.4, LEAF_D, rot=('x', 22.5, (5.6, 2.2, z)))

@redesign("flower_crown")
def _(m):
    band(m, 3.7, 4.3, LEAF_D, 4.6)
    cols = ['#ff6b9a', YELLOW, '#9ad0ff', '#ffffff', '#c49bff', '#ff9d5c']
    k = 0
    for x in (-3.2, -1.1, 1.1, 3.2):
        flower(m, x, 4.0, -4.6, cols[k % 6], s=0.9); k += 1
    for z in (-2.2, 0.0, 2.2):
        for s in (-1, 1):
            m.box(s * 4.6 - 0.3 * (s < 0) , 3.6, z - 0.8, s * 4.6 + 0.3 * (s > 0), 4.4, z + 0.8, cols[k % 6]); k += 1
            m.box(s * 4.9 - 0.15, 3.85, z - 0.3, s * 4.9 + 0.15, 4.15, z + 0.3, YELLOW)
    for x, z in [(-2.2, -4.7), (0, -4.7), (2.2, -4.7)]:
        m.box(x - 0.5, 4.2, z - 0.2, x + 0.5, 4.6, z + 0.2, LEAF, rot=('z', 22.5, (x, 4.4, z)))
    for x in (-2.5, 0, 2.5):
        flower(m, x, 4.3, 4.7, cols[(k := k + 1) % 6], s=0.7)

@redesign("sprout")
def _(m):
    m.box(-1.2, 4.0, -1.2, 1.2, 4.6, 1.2, '#6b4a2e'); m.box(-0.8, 4.6, -0.8, 0.8, 4.8, 0.8, '#7d5a39')
    m.box(-0.25, 4.6, -0.25, 0.25, 7.2, 0.25, STEM)
    r1, r2 = ('z', -22.5, (-0.25, 6.8, 0)), ('z', 22.5, (0.25, 7.0, 0))
    m.box(-3.4, 6.6, -1.0, -0.25, 7.1, 1.0, LEAF, rot=r1); m.box(-3.0, 7.1, -0.2, -0.6, 7.2, 0.2, '#7fd36b', rot=r1)
    m.box(0.25, 6.8, -1.0, 3.6, 7.3, 1.0, GREEN, rot=r2); m.box(0.6, 7.3, -0.2, 3.2, 7.4, 0.2, '#9be27a', rot=r2)
    m.box(-0.4, 7.2, -0.4, 0.4, 7.9, 0.4, '#b6ff6b')

@redesign("mushroom_red")
def _(m):
    rbox(m, -1.3, 4, -1.3, 1.3, 6.2, 1.3, '#efe6d6', r=0.4, top=False)
    m.box(-1.6, 5.0, -1.6, 1.6, 5.5, 1.6, '#e2d6c0')
    m.box(-4.4, 5.8, -4.4, 4.4, 6.2, 4.4, '#f0d9c8')  # gills underside
    y = dome(m, 6.2, [(4.8, 1.0), (4.4, 0.9), (3.6, 0.7), (2.4, 0.5)], RED)
    for x, z, yy in [(-2.6, -2.2, 8.0), (1.6, -1.4, 8.3), (0.2, 2.0, 8.3), (-2.0, 2.4, 7.9), (2.8, 2.5, 7.8), (0, -0.2, 8.8)]:
        m.box(x - 0.6, yy, z - 0.6, x + 0.6, yy + 0.25, z + 0.6, WHITE)
    for x in (-3.0, 0.6, 3.4):
        m.box(x - 0.6, 6.6, -4.9, x + 0.6, 7.6, -4.75, WHITE)
    m.box(-4.9, 6.8, -1.2, -4.75, 7.6, 0.2, WHITE); m.box(4.75, 6.6, 0.6, 4.9, 7.4, 1.8, WHITE)

@redesign("mushroom_brown")
def _(m):
    rbox(m, -0.9, 4, -0.9, 0.9, 5.6, 0.9, '#e8dcc6', r=0.3, top=False)
    m.box(-3.6, 5.4, -3.6, 3.6, 5.7, 3.6, '#d9c3a3')
    dome(m, 5.7, [(4.0, 0.8), (3.5, 0.6), (2.6, 0.4)], '#9a6a45')
    for x, z in [(-1.8, -1.5), (1.4, 0.8), (-0.6, 2.0)]:
        m.box(x - 0.5, 7.5, z - 0.5, x + 0.5, 7.6, z + 0.5, '#b88a5f')

@redesign("grass_block_hat")
def _(m):
    m.box(-2.6, 4, -2.6, 2.6, 8.6, 2.6, '#866043')
    m.box(-2.7, 7.6, -2.7, 2.7, 8.8, 2.7, '#5fa83a')
    for x, z, d in [(-2.2, -2.75, 1.2), (-0.6, -2.75, 0.6), (1.2, -2.75, 1.0), (-2.75, 0.4, 0.8), (2.75, -1.0, 1.1)]:
        m.box(x - 0.45, 7.6 - d, z - 0.05, x + 0.45, 7.6, z + 0.05, '#4f9030')
    m.box(-0.2, 8.8, 0.6, 0.2, 10.0, 1.0, '#3f8f3a'); flower(m, 0, 10.0, 0.8, '#ff6b9a', s=0.6, face='u')
    m.box(1.2, 8.8, -1.6, 1.4, 9.6, -1.4, '#76c84a'); m.box(-1.6, 8.8, -0.8, -1.4, 9.4, -0.6, '#76c84a')

@redesign("pumpkin_hat")
def _(m):
    rbox(m, -2.8, 4, -2.8, 2.8, 7.8, 2.8, ORANGE, r=0.7)
    for x in (-1.4, 0, 1.4):
        m.box(x - 0.15, 4.2, -2.85, x + 0.15, 7.4, -2.75, '#c8621a')
        m.box(x - 0.15, 4.2, 2.75, x + 0.15, 7.4, 2.85, '#c8621a')
    m.box(-1.9, 5.6, -2.95, -0.8, 6.6, -2.8, '#ffd34a'); m.box(0.8, 5.6, -2.95, 1.9, 6.6, -2.8, '#ffd34a')
    m.box(-1.6, 4.5, -2.95, 1.6, 5.0, -2.8, '#ffd34a'); m.box(-0.5, 5.0, -2.95, 0.5, 5.3, -2.8, '#ffd34a')
    m.box(-0.4, 7.8, -0.4, 0.4, 9.0, 0.4, '#4d7a26'); m.box(0.4, 8.6, -0.3, 1.4, 8.9, 0.3, '#4d7a26')
    m.box(0.4, 7.8, -0.4, 2.2, 8.1, 1.2, LEAF, rot=('y', 22.5, (0.4, 8, 0)))

@redesign("cowboy_hat")
def _(m):
    m.box(-4.6, 4.0, -6.2, 4.6, 4.6, 6.2, BROWN)
    for s in (-1, 1):
        m.box(s * 4.6, 4.3, -6.2, s * 6.0, 4.9, 6.2, BROWN)
        m.box(s * 6.0, 4.9, -6.2, s * 6.8, 6.2, 6.2, '#8a5630')
    m.box(-4.6, 3.7, -6.8, 4.6, 4.3, -6.2, '#8a5630'); m.box(-4.6, 4.3, 6.2, 4.6, 4.9, 6.8, '#8a5630')
    rbox(m, -3.8, 4.6, -3.8, 3.8, 8.0, 3.8, BROWN, r=0.8, top=False)
    m.box(-2.8, 8.0, -3.2, -0.4, 8.5, 3.2, BROWN); m.box(0.4, 8.0, -3.2, 2.8, 8.5, 3.2, BROWN)
    m.box(-3.9, 4.6, -3.9, 3.9, 5.5, 3.9, '#3b2414')
    m.box(-0.6, 4.7, -4.05, 0.6, 5.4, -3.9, SILVER)

@redesign("beanie")
def _(m):
    for i, x in enumerate([-4.6 + 0.92 * k for k in range(10)]):
        m.box(x, 1.4, -4.6, x + 0.92, 3.0, 4.6, '#e8dccb' if i % 2 else '#f6efe3')
    y = dome(m, 3.0, [(4.6, 1.6), (4.3, 1.0), (3.6, 0.7), (2.6, 0.4)], '#c2363c')
    for x in (-3.0, -1.0, 1.0, 3.0):
        m.box(x - 0.15, 3.1, -4.75, x + 0.15, 5.4, -4.6, '#a32a30')
    rbox(m, -1.5, y, -1.5, 1.5, y + 2.4, 1.5, WHITE, r=0.6)
    m.box(-2.0, 1.8, -4.75, -0.6, 2.6, -4.6, AC); m.box(-1.6, 2.0, -4.85, -1.0, 2.4, -4.75, AC_GLOW)

def _cap(m, col, dark, back=False):
    dome(m, 4.0, [(4.6, 1.2), (4.2, 0.7), (3.3, 0.5)], col)
    for x in (-1.6, 1.6):
        m.box(x - 0.1, 4.2, -4.7 if not back else 4.6, x + 0.1, 6.2, -4.6 if not back else 4.7, dark)
    m.box(-0.5, 6.4, -0.5, 0.5, 6.8, 0.5, dark)
    zs = (-4.6, -6.6, -7.6) if not back else (4.6, 6.6, 7.6)
    sg = -1 if not back else 1
    m.box(-4.0, 4.0, min(zs[0], zs[1]), 4.0, 4.4, max(zs[0], zs[1]), dark)
    m.box(-3.2, 3.85, min(zs[1], zs[2]), 3.2, 4.25, max(zs[1], zs[2]), dark)
    m.box(-3.6, 4.05, min(zs[0], zs[1]) + (0.6 if back else 0), 3.6, 4.15, max(zs[0], zs[1]) - (0 if back else 0.6), '#202020')
    if not back:
        m.box(-1.0, 4.6, -4.8, 1.0, 5.8, -4.6, WHITE); m.box(-0.4, 4.8, -4.9, 0.4, 5.6, -4.8, AC)
    else:
        m.box(-1.3, 4.1, -4.75, 1.3, 5.0, -4.6, WHITE); m.box(-0.4, 4.3, -4.85, 0.4, 4.8, -4.75, AC)
        m.box(-1.2, 4.0, 4.6, 1.2, 4.6, 4.7, dark)

@redesign("baseball_cap")
def _(m):
    _cap(m, RED, '#9a1f1c')

@redesign("backwards_cap")
def _(m):
    _cap(m, BLUE, '#1d3f99', back=True)

@redesign("chef_hat")
def _(m):
    band(m, 2.8, 5.0, '#f4f4ee', 4.6)
    m.box(-4.0, 5.0, -4.0, 4.0, 6.0, 4.0, '#fbfbf7')
    for x, z, h in [(-2.5, -2.5, 3.0), (2.5, -2.5, 2.6), (-2.5, 2.5, 2.7), (2.5, 2.5, 3.2), (0, 0, 3.8)]:
        rbox(m, x - 2.4, 6.0, z - 2.4, x + 2.4, 6.0 + h, z + 2.4, '#ffffff', r=0.9)
    for x in (-3, -1, 1, 3):
        m.box(x - 0.1, 3.0, -4.75, x + 0.1, 4.8, -4.6, '#dcdcd4')

@redesign("santa_hat")
def _(m):
    for i, x in enumerate([-4.8 + 1.2 * k for k in range(9)]):
        m.box(x, 2.8 + (i % 2) * 0.2, -4.8, x + 1.2, 4.6 + (i % 2) * 0.2, 4.8, WHITE if i % 2 else '#eef0f4')
    y = dome(m, 4.6, [(4.2, 1.4), (3.6, 1.0)], RED)
    rbox(m, -2.6, y, -2.0, 2.6, y + 1.2, 3.0, RED, r=0.7)
    rbox(m, -1.8, y + 1.0, 0.6, 1.8, y + 1.9, 4.4, '#b8262a', r=0.5)
    rbox(m, -1.2, y - 0.2, 4.2, 1.2, y + 1.4, 5.6, '#b8262a', r=0.4)
    rbox(m, -1.3, y - 1.8, 4.6, 1.3, y + 0.0, 6.6, WHITE, r=0.6)

@redesign("party_hat")
def _(m):
    cols = ['#ff5ab4', '#5ad1ff', '#ffe25a', '#7cfba5', '#ff5ab4', '#5ad1ff']
    r = ('z', 22.5, (0, 4, 0))
    for i, w in enumerate([5.0, 4.2, 3.4, 2.6, 1.8, 1.1]):
        m.box(-w / 2, 4 + i * 1.1, -w / 2, w / 2, 5.1 + i * 1.1, w / 2, cols[i], rot=r)
    for dx, dz in ((-0.9, 0), (0.9, 0), (0, -0.9), (0, 0.9), (0, 0)):
        m.box(dx - 0.5, 10.6, dz - 0.5, dx + 0.5, 11.6, dz + 0.5, '#ffffff', rot=r)
    m.box(-2.5, 4.0, -2.5, 2.5, 4.4, 2.5, '#ffe25a', rot=r)
    for x, z, c in [(-1.8, -2.6, YELLOW), (1.0, -2.0, '#ff5ab4'), (0.2, -1.4, '#5ad1ff')]:
        m.box(x - 0.2, 5.4, z - 0.2, x + 0.2, 5.8, z, c, rot=r)

@redesign("fez")
def _(m):
    rbox(m, -2.6, 4, -2.6, 2.6, 7.2, 2.6, '#b51d2a', r=0.6, top=False)
    m.box(-2.2, 7.2, -2.2, 2.2, 7.4, 2.2, '#9c1622')
    m.box(-2.65, 4, -2.65, 2.65, 4.6, 2.65, '#7d111b')
    m.box(-0.25, 7.4, -0.25, 0.25, 7.8, 0.25, GOLD_D)
    m.box(-0.15, 7.6, -0.15, 2.8, 7.8, 0.15, GOLD)
    m.box(2.6, 4.6, -0.5, 3.0, 7.8, 0.5, GOLD); m.box(2.5, 4.2, -0.6, 3.1, 4.8, 0.6, GOLD_D)

@redesign("beret")
def _(m):
    r = ('z', 22.5, (0, 4, 0))
    m.box(-4.7, 4.0, -4.7, 4.7, 4.6, 4.7, '#2b2840', rot=r)
    m.box(-5.4, 4.6, -4.8, 4.6, 5.6, 4.8, '#34304e', rot=r)
    m.box(-4.8, 5.6, -4.2, 4.0, 6.1, 4.2, '#34304e', rot=r)
    m.box(-0.25, 6.1, -0.25, 0.25, 6.8, 0.25, '#2b2840', rot=r)
    m.box(-4.7, 4.0, -4.75, 4.7, 4.3, -4.65, '#1d1b2b', rot=r)
    m.box(-3.6, 4.8, -4.9, -2.6, 5.6, -4.8, AC_GLOW, rot=r)

@redesign("bucket_hat")
def _(m):
    m.box(-5.8, 3.0, -5.8, 5.8, 3.4, 5.8, '#5e8a4e')
    m.box(-5.0, 3.4, -5.0, 5.0, 3.9, 5.0, '#5e8a4e')
    dome(m, 3.9, [(4.6, 1.8), (4.2, 0.6), (3.6, 0.3)], '#6f9d5d')
    m.box(-4.65, 3.9, -4.65, 4.65, 4.5, 4.65, '#4b7340')
    for x in (-3, 3):
        m.box(x - 0.2, 5.2, -4.75, x + 0.2, 5.6, -4.6, SILVER)
    for i in range(6):
        x = -5.4 + i * 2.1
        m.box(x, 3.0, -5.85, x + 0.8, 3.1, -5.8, '#4b7340')

@redesign("sailor_cap")
def _(m):
    m.box(-4.6, 4.0, -4.6, 4.6, 4.8, 4.6, '#213a8f')
    dome(m, 4.8, [(4.6, 0.8), (5.2, 0.6), (4.8, 0.3)], WHITE)
    m.box(-3.4, 4.0, -6.0, 3.4, 4.3, -4.6, BLACK)
    m.box(-0.6, 4.1, -4.75, 0.6, 4.7, -4.6, GOLD); m.box(-0.15, 4.0, -4.8, 0.15, 4.8, -4.75, GOLD)
    m.box(-0.4, 6.5, -0.4, 0.4, 6.8, 0.4, RED)
    for s in (-1, 1):
        m.box(s * 0.6, 3.0, 4.6, s * 1.4, 4.4, 4.75, '#213a8f')

@redesign("straw_hat")
def _(m):
    for i, r in enumerate([6.8, 6.0, 5.2]):
        m.box(-r, 4.0, -r, r, 4.5, r, '#e8c86a' if i % 2 == 0 else '#d9b354')
    for i, y in enumerate([4.5, 5.2, 5.9, 6.6]):
        rbox(m, -4.1 + 0.15 * i, y, -4.1 + 0.15 * i, 4.1 - 0.15 * i, y + 0.7, 4.1 - 0.15 * i,
             '#e8c86a' if i % 2 == 0 else '#d9b354', r=0.7, top=(i == 3))
    m.box(-4.25, 4.5, -4.25, 4.25, 5.4, 4.25, RED)
    m.box(-1.6, 4.4, -4.6, -0.4, 5.6, -4.25, '#a32020'); m.box(0.4, 4.4, -4.6, 1.6, 5.6, -4.25, '#a32020')
    m.box(-0.4, 4.7, -4.7, 0.4, 5.3, -4.25, RED)

@redesign("miner_helmet")
def _(m):
    m.box(-5.0, 3.6, -5.0, 5.0, 4.2, 5.0, '#d6b72a')
    dome(m, 4.2, [(4.6, 1.2), (4.2, 0.8), (3.4, 0.6), (2.2, 0.3)], YELLOW)
    m.box(-0.4, 4.2, -4.7, 0.4, 7.0, 4.7, '#e3c22e')
    rbox(m, -1.4, 4.4, -5.6, 1.4, 6.6, -4.6, GREY, r=0.4)
    m.box(-1.0, 4.8, -5.8, 1.0, 6.2, -5.6, '#fff6b0')
    m.box(-0.5, 5.2, -5.9, 0.5, 5.8, -5.8, '#ffffff')

@redesign("chick_buddy")
def _(m):
    rbox(m, -2.2, 4, -2.2, 2.2, 7.8, 2.2, '#ffe14a', r=0.8)
    m.box(-1.0, 5.6, -3.4, 1.0, 6.2, -2.2, ORANGE); m.box(-0.7, 5.2, -3.0, 0.7, 5.6, -2.2, '#d9661a')
    m.box(-1.6, 6.6, -2.3, -0.8, 7.4, -2.2, BLACK); m.box(0.8, 6.6, -2.3, 1.6, 7.4, -2.2, BLACK)
    m.box(-1.4, 7.1, -2.35, -1.2, 7.3, -2.3, WHITE); m.box(1.0, 7.1, -2.35, 1.2, 7.3, -2.3, WHITE)
    m.box(-2.0, 6.0, -2.35, -1.4, 6.4, -2.2, '#ffb0a0'); m.box(1.4, 6.0, -2.35, 2.0, 6.4, -2.2, '#ffb0a0')
    for s in (-1, 1):
        rbox(m, min(s * 2.2, s * 2.8), 4.8, -1.0, max(s * 2.2, s * 2.8), 6.6, 1.4, '#f5cf2e', r=0.25)
    m.box(-0.2, 7.8, -0.2, 0.2, 8.6, 0.2, '#ffd21a'); m.box(-0.2, 8.4, -0.2, 0.8, 8.8, 0.2, '#ffd21a')
    for s in (-1, 1):
        m.box(s * 1.0 - 0.4, 4.0, -2.8, s * 1.0 + 0.4, 4.2, -1.8, ORANGE)

@redesign("sunglasses")
def _(m):
    for s in (-1, 1):
        rbox(m, s * 2.3 - 1.9, 0.0, -4.85, s * 2.3 + 1.9, 2.0, -4.6, '#15151b', r=0.4, top=False)
        m.box(s * 2.3 - 1.5, 0.3, -4.95, s * 2.3 + 1.5, 1.8, -4.85, '#2a2440')
        m.box(s * 2.3 - 1.2 + 0.3, 1.2, -5.0, s * 2.3 - 0.6 + 0.3, 1.6, -4.95, '#9a8ad6')
        m.box(s * 4.6, 1.3, -4.85, s * 4.75, 1.7, 2.5, '#15151b')
    m.box(-0.5, 1.4, -4.85, 0.5, 1.8, -4.6, '#15151b')
    m.box(-4.2, 1.8, -4.9, 4.2, 2.1, -4.6, GOLD)

@redesign("ninja_headband")
def _(m):
    band(m, 2.4, 3.8, '#1e2a4a', 4.6)
    rbox(m, -1.6, 2.2, -4.85, 1.6, 4.0, -4.6, SILVER, r=0.3, top=False)
    m.box(-1.0, 2.8, -4.95, 1.0, 3.4, -4.85, '#4a4f5c'); m.box(-0.2, 2.6, -4.95, 0.2, 3.6, -4.85, '#4a4f5c')
    for x in (-1.3, 1.3):
        m.box(x - 0.15, 2.4, -4.95, x + 0.15, 2.7, -4.85, '#8a8f9c'); m.box(x - 0.15, 3.5, -4.95, x + 0.15, 3.8, -4.85, '#8a8f9c')
    m.box(-0.7, 2.4, 4.6, 0.7, 3.8, 5.2, '#1e2a4a')
    m.box(-1.2, 2.0, 5.0, -0.2, 3.0, 8.4, '#1e2a4a', rot=('x', -22.5, (0, 3, 5.0)))
    m.box(0.2, 1.8, 5.0, 1.2, 2.8, 7.6, '#2a3a63', rot=('x', -45, (0, 3, 5.0)))

@redesign("pirate_bandana")
def _(m):
    dome(m, 2.4, [(4.6, 1.6), (4.4, 0.6), (3.8, 0.4)], RED)
    for x, y, z in [(-3, 3.0, -4.7), (-0.5, 3.6, -4.7), (2, 2.8, -4.7), (3.5, 3.6, -4.7)]:
        m.box(x, y, z, x + 0.6, y + 0.5, z + 0.1, WHITE)
    for x, z in [(-2, -1), (1, 1.5), (2.5, -2)]:
        m.box(x, 5.0, z, x + 0.5, 5.1, z + 0.5, WHITE)
    rbox(m, -1.0, 1.6, 4.6, 1.0, 3.2, 5.6, '#a82522', r=0.3)
    m.box(-1.4, -0.6, 5.0, -0.4, 1.8, 5.4, RED, rot=('z', 22.5, (-0.9, 1.8, 5.2)))
    m.box(0.4, -0.2, 5.0, 1.4, 1.8, 5.4, RED, rot=('z', -22.5, (0.9, 1.8, 5.2)))

@redesign("headphones")
def _(m):
    m.box(-4.0, 4.6, -0.7, 4.0, 5.3, 0.7, '#2a2a33')
    m.box(-3.0, 4.6, -0.5, 3.0, 4.8, 0.5, '#5a5a66')
    for s in (-1, 1):
        m.box(min(s * 4.0, s * 4.7), 2.0, -0.5, max(s * 4.0, s * 4.7), 5.3, 0.5, '#2a2a33')
        m.box(min(s * 4.6, s * 5.0), 1.6, -0.4, max(s * 4.6, s * 5.0), 3.2, 0.4, SILVER)
        rbox(m, min(s * 4.6, s * 5.9), -1.8, -2.0, max(s * 4.6, s * 5.9), 2.0, 2.0, '#34343e', r=0.6, top=False)
        m.box(min(s * 4.6, s * 4.9), -1.6, -1.8, max(s * 4.6, s * 4.9), 1.8, 1.8, '#1a1a20')
        m.box(min(s * 5.9, s * 6.1), -0.9, -1.1, max(s * 5.9, s * 6.1), 1.1, 1.1, '#ff3d7f')
        m.box(min(s * 6.1, s * 6.2), -0.4, -0.5, max(s * 6.1, s * 6.2), 0.6, 0.5, '#ffd0e0')

@redesign("knight_plume")
def _(m):
    band(m, 3.3, 4.2, SILVER, 4.6)
    m.box(-0.8, 3.2, -4.85, 0.8, 4.4, -4.6, '#3a7bf0')
    rbox(m, -0.6, 4.2, 3.4, 0.6, 5.4, 4.8, SILVER, r=0.2)
    r = ('x', -22.5, (0, 5.2, 4.1))
    for i, (c, dz, h) in enumerate([('#2a6de0', 0, 5.0), ('#4b8bff', 0.6, 4.2), (WHITE, 1.2, 3.2)]):
        m.box(-0.7 + 0.1 * i, 5.2, 3.6 + dz, 0.7 - 0.1 * i, 5.2 + h, 4.6 + dz, c, rot=r)
    m.box(-0.5, 9.6, 3.8, 0.5, 10.6, 4.4, '#9cc2ff', rot=r)

@redesign("snail_shell")
def _(m):
    rbox(m, -2.6, 4, -2.8, 2.6, 9.4, 2.8, '#c98b4a', r=0.9)
    rbox(m, -2.7, 5.0, -2.0, 2.7, 8.4, 2.0, '#a96c33', r=0.7, top=False)
    rbox(m, -2.8, 5.8, -1.2, 2.8, 7.6, 1.2, '#e2b07a', r=0.4, top=False)
    m.box(-2.9, 6.4, -0.4, 2.9, 7.0, 0.4, '#7a4a20')
    for s in (-1, 1):
        m.box(s * 1 - 0.2, 4, -3.6, s * 1 + 0.2, 6.4, -3.2, '#a7b56a')
        m.box(s * 1 - 0.4, 6.4, -3.8, s * 1 + 0.4, 7.1, -3.0, '#a7b56a'); m.box(s * 1 - 0.2, 6.6, -3.9, s * 1 + 0.2, 7.0, -3.8, BLACK)

@redesign("alien_antennae")
def _(m):
    m.box(-4.6, 3.6, -0.6, 4.6, 4.3, 0.6, '#3a3f4a')
    for s in (-1, 1):
        x = s * 2.0
        for i in range(5):
            m.box(x - 0.3 + s * 0.15 * (i % 2), 4.3 + i * 0.8, -0.3, x + 0.3 + s * 0.15 * (i % 2), 5.1 + i * 0.8, 0.3, '#8a93a6' if i % 2 else '#c2cad8')
        rbox(m, x - 1.0, 8.3, -1.0, x + 1.0, 10.3, 1.0, '#b6ff6b', r=0.4)
        m.box(x - 0.5, 8.8, -1.1, x + 0.5, 9.8, -1.0, '#eaffd0')

@redesign("laurel_wreath")
def _(m):
    band(m, 3.5, 4.0, '#3c6e2a', 4.6)
    for s in (-1, 1):
        for i, z in enumerate([-3.8, -2.6, -1.4, -0.2, 1.0, 2.2, 3.4]):
            for up in (0, 1):
                r = ('x', 22.5 if up else -22.5, (s * 4.7, 3.75, z))
                m.box(s * 4.6 - 0.3 * (s < 0), 3.75 + (0.1 if up else -0.6), z - 0.2, s * 4.6 + 0.3 * (s > 0), 4.25 + (0.1 if up else -0.6), z + 1.0,
                      '#5aa83f' if (i + up) % 2 else '#3f8a2e', rot=r)
            if i % 2:
                m.box(s * 4.95 - 0.2, 3.5, z + 0.2, s * 4.95 + 0.2, 3.9, z + 0.6, GOLD)
    m.box(-4.6, 3.5, 4.6, 4.6, 4.0, 4.7, '#3c6e2a')
    m.box(-0.8, 3.2, 4.65, 0.8, 4.2, 5.1, GOLD)
    for s in (-1, 1):
        m.box(s * 0.4 - 0.3, 1.4, 4.75, s * 0.4 + 0.3, 3.2, 4.95, GOLD_D, rot=('z', 22.5 * s, (s * 0.4, 3.2, 4.85)))

@redesign("pirate_tricorn")
def _(m):
    dome(m, 4.0, [(4.6, 1.5), (4.2, 1.2), (3.6, 0.6)], BLACK)
    m.box(-5.6, 5.0, -5.4, 5.6, 7.2, -4.6, '#25222b')
    for s in (-1, 1):
        m.box(min(s * 4.6, s * 5.6), 5.0, -5.4, max(s * 4.6, s * 5.6), 7.2, 5.4, '#25222b')
    m.box(-5.6, 5.0, 4.6, 5.6, 7.2, 5.4, '#25222b')
    for z1, z2 in ((-5.45, -4.6), (4.6, 5.45)):
        m.box(-5.65, 7.0, z1, 5.65, 7.35, z2, GOLD)
    for s in (-1, 1):
        m.box(min(s * 4.6, s * 5.65), 7.0, -5.4, max(s * 4.6, s * 5.65), 7.35, 5.4, GOLD)
    m.box(-1.0, 5.6, -5.55, 1.0, 6.9, -5.4, WHITE); m.box(-0.6, 5.2, -5.55, 0.6, 5.6, -5.4, WHITE)
    m.box(-0.6, 6.0, -5.6, -0.2, 6.4, -5.55, BLACK); m.box(0.2, 6.0, -5.6, 0.6, 6.4, -5.55, BLACK)
    m.box(-1.6, 4.9, -5.5, 1.6, 5.1, -5.4, WHITE, rot=('z', 22.5, (0, 5, -5.45)))
    m.box(-1.6, 4.9, -5.5, 1.6, 5.1, -5.4, WHITE, rot=('z', -22.5, (0, 5, -5.45)))
    m.box(-4.4, 0.9, -4.75, -0.9, 2.6, -4.6, BLACK)
    m.box(-4.6, 2.2, -4.7, 4.6, 2.5, 4.7, '#3a3540')


# ======================================================================
# Full-head pieces with real depth: rounded shells, carved/raised relief
# ======================================================================
def relief(m, rows, z, spec, cell=1.0, top=5.0, width=None, cx=0.0):
    """Pixel relief on the front (-z) face. rows are read as seen from the front, top row first.
    spec: char -> (colour, thickness). Thickness 0/None = carved hole (nothing drawn)."""
    n = len(rows[0]); width = width or n * cell
    xl = cx + width / 2  # viewer's left edge is +x
    for r, row in enumerate(rows):
        y2 = top - r * cell; y1 = y2 - cell
        c = 0
        while c < n:
            ch = row[c]; e = c
            while e + 1 < n and row[e + 1] == ch:
                e += 1
            col, t = spec.get(ch, (None, 0))
            if t:
                m.box(xl - (e + 1) * cell, y1, z - t, xl - c * cell, y2, z, col)
            c = e + 1

def shell(m, h, c, r=1.0, y1=-5.1, y2=5.1, dome_top=True):
    """Rounded full-head shell, kept outside the skin's hat layer."""
    m.box(-4.6, -4.6, -4.6, 4.6, 4.6, 4.6, c)   # core: hides the head + hat layer inside the rounded corners
    rbox(m, -h, y1, -h, h, y2 - (0.6 if dome_top else 0), h, c, r=r, top=False)
    if dome_top:
        rbox(m, -h + r, y2 - 0.6, -h + r, h - r, y2, h - r, c, r=0.5, top=False)

@redesign("creeper_mask")
def _(m):
    G, GL, GD, K = '#5ec04a', '#8ee07a', '#45a036', '#101410'
    shell(m, 5.0, G, r=0.8)
    # front: creeper face carved in, lighter pixels raised
    m.box(-3.0, -4.0, -5.05, 3.0, 2.0, -5.0, K)   # dark cavity behind the carved face
    relief(m, ["gLggggLggg",
               "ggggLggggg",
               "gKKKggKKKg",
               "gKKKggKKKg",
               "ggggKKgggd",
               "gggKKKKggg",
               "gLgKKKKggg",
               "gggKggKgLg",
               "dggggggggg",
               "gggLgggggg"], -5.0,
           {'g': (G, 0.35), 'L': (GL, 0.6), 'd': (GD, 0.2), 'K': (None, 0)})
    for x, y, zz in [(-5.0, 2.5, -2), (-5.0, -1.5, 1.5), (5.0, 1.0, -1), (5.0, -3, 2.5)]:
        m.box(x - 0.3 if x < 0 else x, y, zz, x if x < 0 else x + 0.3, y + 1.0, zz + 1.0, GL)
    for x, zz in [(-2, -2), (1.5, 1.5), (-1, 2.5)]:
        m.box(x, 5.1, zz, x + 1.0, 5.4, zz + 1.0, GL)

@redesign("pumpkin_head")
def _(m):
    O, OD, OL, GLOW, IN = ORANGE, '#c8621a', '#f59a3c', '#ffd34a', '#ff9a1f'
    shell(m, 5.0, O, r=1.4)
    m.box(-4.0, -4.0, -5.05, 4.0, 3.0, -5.0, GLOW)  # candle glow inside the carving
    relief(m, ["ooRooooRoo",
               "ooRooooRoo",
               "ohhhoohhho",
               "oohhoohhoo",
               "ooRohhoRoo",
               "ooRooooRoo",
               "ohhhhhhhho",
               "oohhohhhoo",
               "ooRooooRoo",
               "ooRooooRoo"], -5.0, {'o': (O, 0.4), 'R': (OL, 0.65), 'h': (None, 0)})
    for z in (-2.5, 0, 2.5):  # ribs round the sides and back
        for s in (-1, 1):
            m.box(min(s * 5.0, s * 5.3), -4.2, z - 0.4, max(s * 5.0, s * 5.3), 4.0, z + 0.4, OL)
    for x in (-2.5, 0, 2.5):
        m.box(x - 0.4, -4.2, 5.0, x + 0.4, 4.0, 5.3, OL)
    rbox(m, -0.7, 5.1, -0.7, 0.7, 6.8, 0.7, '#4d7a26', r=0.25)
    m.box(0.7, 6.2, -0.4, 2.2, 6.6, 0.4, '#4d7a26'); m.box(1.8, 5.6, -0.4, 2.2, 6.2, 0.4, '#4d7a26')
    m.box(-0.6, 5.1, -0.6, -3.2, 5.5, 1.6, LEAF, rot=('y', 22.5, (-0.6, 5.3, 0)))
    m.box(-1.2, 5.5, -0.1, -2.8, 5.6, 0.9, LEAF_D, rot=('y', 22.5, (-0.6, 5.3, 0)))

@redesign("ghost_sheet")
def _(m):
    W, WS, K = '#f2f2f6', '#dcdce6', '#15151c'
    shell(m, 5.0, W, r=1.5, y1=-5.0, y2=5.4)
    rbox(m, -3.2, 5.4, -3.2, 3.2, 6.2, 3.2, W, r=1.0)
    # wavy hem hanging below
    hem = [(-5.0, -3.0, 1.6), (-3.0, -1.0, 0.8), (-1.0, 1.0, 1.9), (1.0, 3.0, 0.7), (3.0, 5.0, 1.5)]
    for a, b, d in hem:
        m.box(a, -5.0 - d, -5.0, b, -5.0, -4.2, W); m.box(a, -5.0 - (2.4 - d), 4.2, b, -5.0, 5.0, WS)
        m.box(-5.0, -5.0 - d, a, -4.2, -5.0, b, WS); m.box(4.2, -5.0 - (2.4 - d), a, 5.0, -5.0, b, W)
    # face: big carved eyes + mouth, cheeks puffed out
    m.box(-3.0, -2.5, -5.05, 3.0, 2.6, -5.0, K)
    relief(m, ["wwwwwwwwww",
               "wwwwwwwwww",
               "wwKKwwKKww",
               "wwKKwwKKww",
               "wwKKwwKKww",
               "wwwwwwwwww",
               "wpwwKKwwpw",
               "wwwwKKwwww",
               "wwwwwwwwww"], -5.0, {'w': (W, 0.3), 'p': ('#ffc2d6', 0.45), 'K': (None, 0)}, top=4.6, cell=1.0)
    for z in (-2.5, 0.5, 3.0):  # cloth folds
        for s in (-1, 1):
            m.box(min(s * 5.0, s * 5.25), -5.6, z - 0.3, max(s * 5.0, s * 5.25), 3.0, z + 0.3, WS)
    for s in (-1, 1):  # little arms
        rbox(m, min(s * 5.0, s * 6.2), -2.6, -1.2, max(s * 5.0, s * 6.2), -0.6, 1.2, W, r=0.4)

@redesign("knight_helmet")
def _(m):
    S1, S2, S3, K = '#b4b8c4', '#9ea2ad', '#7c808b', '#101014'
    shell(m, 5.0, S1, r=1.1)
    m.box(-0.5, 5.0, -4.6, 0.5, 6.0, 4.6, S3)                 # top ridge
    m.box(-5.4, -5.3, -5.4, 5.4, -4.4, 5.4, S3)              # flared gorget
    # visor sticks out with an eye slit and breathing holes punched through
    m.box(-4.0, -3.4, -5.05, 4.0, 2.2, -5.0, K)
    relief(m, ["vvvvvvvvvv",
               "vvvvvvvvvv",
               "SSSSSSSSSS",
               "vvvvvvvvvv",
               "vvvvvrvvvv",
               "vhvhvrvhvh",
               "vvvvvrvvvv",
               "vhvhvrvhvh",
               "vvvvvrvvvv"], -5.0,
           {'v': (S2, 0.7), 'r': (S1, 1.0), 'S': (None, 0), 'h': (None, 0)}, top=4.2, cell=0.9)
    for x, y in [(-4.0, 3.6), (4.0, 3.6), (-4.0, -3.8), (4.0, -3.8)]:
        m.box(x - 0.35, y - 0.35, -5.95, x + 0.35, y + 0.35, -5.6, '#e6e8ee')
    for s in (-1, 1):                                       # visor hinges
        rbox(m, min(s * 5.0, s * 5.6), -0.8, -1.2, max(s * 5.0, s * 5.6), 1.0, 0.6, S3, r=0.3)
    m.box(-0.8, 6.0, -2.5, 0.8, 8.0, 3.0, '#c8282c')       # plume
    m.box(-0.7, 3.4, 3.0, 0.7, 7.6, 6.4, '#e0403f', rot=('x', -22.5, (0, 7.0, 3.0)))

@redesign("astronaut")
def _(m):
    Wh, Wd, V, VL = '#f4f4f8', '#cfd3dc', '#e0a833', '#ffe08a'
    shell(m, 5.1, Wh, r=1.4, y1=-4.8, y2=5.3)
    m.box(-5.5, -5.6, -5.5, 5.5, -4.6, 5.5, '#9aa1ad')       # neck ring
    m.box(-5.1, -4.6, -5.3, 5.1, -3.9, 5.3, Wd)
    # bulging gold visor, layered so it curves out
    rbox(m, -4.2, -2.6, -5.5, 4.2, 3.6, -5.0, Wd, r=0.6, top=False)
    rbox(m, -3.7, -2.2, -5.9, 3.7, 3.2, -5.4, V, r=0.6, top=False)
    rbox(m, -2.9, -1.6, -6.2, 2.9, 2.6, -5.8, '#efbb44', r=0.6, top=False)
    m.box(1.2, 1.2, -6.3, 2.4, 2.2, -6.15, VL); m.box(1.8, 0.3, -6.3, 2.4, 1.0, -6.15, VL)
    for s in (-1, 1):                                        # side comms pods
        rbox(m, min(s * 5.1, s * 6.0), -1.6, -1.6, max(s * 5.1, s * 6.0), 1.6, 1.6, Wd, r=0.5)
        m.box(min(s * 6.0, s * 6.15), -0.6, -0.6, max(s * 6.0, s * 6.15), 0.6, 0.6, '#d23c3c' if s < 0 else '#2f6fd8')
    m.box(2.6, 5.1, 2.0, 3.0, 7.8, 2.4, GREY); m.box(2.4, 7.8, 1.8, 3.2, 8.6, 2.6, RED)
    m.box(-3.4, 3.8, 5.1, -1.4, 4.6, 5.25, '#2f6fd8'); m.box(-3.4, 3.0, 5.1, -1.4, 3.8, 5.25, Wh)

@redesign("astronaut")
def _(m):
    Wh, Wd, GLS, HI = '#f4f4f8', '#cfd3dc', '#a8dcff66', '#ffffffb0'
    # white shell: back half, top and sides, with a big opening at the front
    rbox(m, -5.1, -4.8, 0.4, 5.1, 4.7, 5.1, Wh, r=1.2, top=False)
    rbox(m, -4.0, 4.7, -3.9, 4.0, 5.4, 4.0, Wh, r=0.8, top=False)
    m.box(-5.1, 4.0, -5.1, 5.1, 4.7, 1.8, Wh)                      # brow
    for s in (-1, 1):
        m.box(min(s * 4.6, s * 5.1), -4.8, -5.1, max(s * 4.6, s * 5.1), 4.7, 1.8, Wh)   # cheeks
        m.box(min(s * 4.2, s * 4.6), -4.8, -5.1, max(s * 4.2, s * 4.6), 4.0, -4.6, Wd)  # visor rim
    m.box(-4.6, -4.8, -5.1, 4.6, -3.6, -4.6, Wd)                   # chin
    m.box(-5.5, -5.6, -5.5, 5.5, -4.8, 5.5, '#9aa1ad')             # neck ring
    # curved glass visor: deeper in the middle, the face shows through
    m.box(-2.8, -3.6, -6.1, 2.8, 4.0, -5.1, GLS)
    for s in (-1, 1):
        m.box(min(s * 2.8, s * 4.2), -3.6, -5.7, max(s * 2.8, s * 4.2), 4.0, -5.1, GLS)
    m.box(1.2, 2.2, -6.2, 2.4, 3.4, -6.1, HI); m.box(1.9, 0.9, -6.2, 2.4, 1.9, -6.1, HI)
    m.box(-3.9, 2.6, -5.8, -3.4, 3.6, -5.7, HI)
    for s in (-1, 1):                                              # comms pods
        rbox(m, min(s * 5.1, s * 6.0), -1.6, -1.6, max(s * 5.1, s * 6.0), 1.6, 1.6, Wd, r=0.5)
        m.box(min(s * 6.0, s * 6.15), -0.6, -0.6, max(s * 6.0, s * 6.15), 0.6, 0.6, '#d23c3c' if s < 0 else '#2f6fd8')
    m.box(2.6, 5.4, 2.0, 3.0, 8.0, 2.4, GREY); m.box(2.4, 8.0, 1.8, 3.2, 8.8, 2.6, RED)
    m.box(-3.4, 3.4, 5.1, -1.4, 4.2, 5.25, '#2f6fd8'); m.box(-3.4, 2.6, 5.1, -1.4, 3.4, 5.25, Wh)


# ======================================================================
# TRENDY batch: what cosmetic shops / servers push right now
# ======================================================================
GLOW.update({'#ff8a1f', '#7af7ff', '#ff5ce1', '#ffe45c', '#ff9fd2', '#a6ffef'})
GLS = '#bfe8ff70'

def heart(m, cx, cy, z, cell, col, t=0.3, hi=None):
    relief(m, ["HH.HH", "HHHHH", "HHHHH", ".HHH.", "..H.."], z, {'H': (col, t)}, cell=cell, top=cy + 2.5 * cell, cx=cx)
    if hi:
        m.box(cx + 1.2 * cell, cy + 1.2 * cell, z - t - 0.05, cx + 1.8 * cell, cy + 1.8 * cell, z - t, hi)

def star(m, x, y, z, s, col, axis='z'):
    if axis == 'z':
        m.box(x - 0.3 * s, y - 1.0 * s, z - 0.25, x + 0.3 * s, y + 1.0 * s, z, col)
        m.box(x - 1.0 * s, y - 0.3 * s, z - 0.25, x + 1.0 * s, y + 0.3 * s, z, col)
        m.box(x - 0.55 * s, y - 0.55 * s, z - 0.3, x + 0.55 * s, y + 0.55 * s, z, col)
    else:  # facing +x
        m.box(x, y - 1.0 * s, z - 0.3 * s, x + 0.25, y + 1.0 * s, z + 0.3 * s, col)
        m.box(x, y - 0.3 * s, z - 1.0 * s, x + 0.25, y + 0.3 * s, z + 1.0 * s, col)
        m.box(x, y - 0.55 * s, z - 0.55 * s, x + 0.3, y + 0.55 * s, z + 0.55 * s, col)

@design("coquette_bow", "Coquette Bow", "trend")
def _(m):
    P, PD, PL = '#ff9cc8', '#e2679f', '#ffd1e6'
    m.box(-4.7, 4.0, -0.5, 4.7, 4.7, 0.5, P)                                   # satin headband
    for s in (-1, 1):
        m.box(min(s * 4.6, s * 5.0), 0.2, -0.5, max(s * 4.6, s * 5.0), 4.7, 0.5, P)
    rbox(m, -0.8, 4.4, -1.6, 0.8, 5.8, -0.2, PD, r=0.3)                       # knot
    for s in (-1, 1):
        r = ('z', -22.5 * s, (s * 0.8, 5.1, -0.9))
        rbox(m, min(s * 0.8, s * 4.0), 4.5, -1.5, max(s * 0.8, s * 4.0), 6.9, -0.3, P, r=0.5, rot=r)
        m.box(min(s * 1.2, s * 3.2), 5.1, -1.6, max(s * 1.2, s * 3.2), 6.3, -1.5, PL, rot=r)
        rt = ('z', 22.5 * s, (s * 0.5, 4.6, -1.7))
        m.box(min(s * 0.2, s * 1.4), 2.2, -1.8, max(s * 0.2, s * 1.4), 4.6, -1.5, P, rot=rt)
        m.box(min(s * 0.2, s * 1.4), 2.0, -1.8, max(s * 0.2, s * 1.4), 2.4, -1.5, PD, rot=rt)
    m.box(-0.3, 5.2, -1.75, 0.3, 5.6, -1.6, '#ffffff')

@design("heart_shades", "Heart Shades", "trend")
def _(m):
    for s in (-1, 1):
        heart(m, s * 2.3, -0.2, -4.6, 0.75, '#ff3d7f', t=0.35, hi='#ffd1e6')
        m.box(min(s * 4.6, s * 4.8), 1.2, -4.6, max(s * 4.6, s * 4.8), 1.6, 2.5, '#ff7aa8')
    m.box(-0.6, 1.4, -4.9, 0.6, 1.8, -4.6, '#ff7aa8')

@design("kitsune_mask", "Kitsune Mask", "trend")
def _(m):
    W, R, G = '#f7f3ea', '#d8323a', '#e8b23a'
    band(m, 1.0, 1.5, R, 4.6)
    x0 = 4.6
    rbox(m, x0, -2.4, -3.0, x0 + 0.8, 3.0, 3.0, W, r=0.6, top=False)                # face plate (worn on the side)
    m.box(x0 + 0.8, -1.8, -1.0, x0 + 2.2, 0.2, 1.0, W); m.box(x0 + 2.2, -1.6, -0.6, x0 + 2.6, -0.4, 0.6, BLACK)  # snout + nose
    m.box(x0 + 0.8, -2.2, -1.4, x0 + 1.6, -1.6, 1.4, R)                          # mouth line
    for zz in (-1.6, 1.6):
        m.box(x0 + 0.8, 0.8, zz - 0.9, x0 + 0.95, 1.3, zz + 0.9, R)              # eye slits
        m.box(x0 + 0.8, 1.3, zz - 0.5, x0 + 0.95, 1.6, zz + 0.5, R)
        for i, w in enumerate([1.8, 1.2, 0.6]):                                   # ears
            m.box(x0, 3.0 + i * 0.8, zz - w / 2, x0 + 0.8, 3.8 + i * 0.8, zz + w / 2, W)
        m.box(x0 + 0.8, 3.0, zz - 0.4, x0 + 0.95, 4.4, zz + 0.4, R)
        m.box(x0 + 0.8, -0.8, zz - 0.2 * (zz < 0) - 0.9 * (zz > 0) + 0.0, x0 + 0.95, -0.4, zz + 0.9 * (zz < 0) + 0.2 * (zz > 0), R)
    m.box(x0 + 0.8, 2.0, -0.3, x0 + 0.95, 2.6, 0.3, G)
    m.box(x0 + 0.3, -3.6, 0.6, x0 + 0.6, -2.4, 1.0, R); m.box(x0 + 0.2, -4.4, 0.4, x0 + 0.7, -3.6, 1.2, G)  # tassel

@design("creaking_mask", "Creaking Mask", "trend")
def _(m):
    B, BD, BL, E, RS = '#8a7b6e', '#5c4f45', '#a89a8c', '#ff8a1f', '#ffb347'
    shell(m, 5.0, B, r=0.9)
    m.box(-3.6, -1.0, -5.05, 3.6, 2.2, -5.0, '#1a120c')
    relief(m, ["bbBbbbbBbb",
               "bBbbbBbbbB",
               "bbbbbbbbbb",
               "bEEbbbbEEb",
               "bEEbbbbEEb",
               "bbbbBBbbbb",
               "bBbbbbbbBb",
               "bbbBbbBbbb",
               "bBbbbbbbbB",
               "bbbbbBbbbb"], -5.0, {'b': (B, 0.35), 'B': (BD, 0.55), 'E': (E, 0.1)})
    for x, h, z in [(-3.5, 3.0, -2), (-1.0, 4.4, 1), (2.0, 3.6, -1), (3.6, 2.4, 2.5), (0.5, 2.0, 3.5)]:
        m.box(x - 0.35, 5.0, z - 0.35, x + 0.35, 5.0 + h, z + 0.35, BD)
        m.box(x, 5.0 + h * 0.6, z - 0.25, x + 1.4 * (1 if x < 0 else -1) * 0 + 1.2, 5.0 + h * 0.6 + 0.5, z + 0.25, BD)
    for x, y in [(-4.0, -3.6), (3.6, 3.2), (-4.4, 1.2)]:
        m.box(x, y, -5.7, x + 0.7, y + 0.7, -5.35, RS)
    for s in (-1, 1):
        m.box(min(s * 5.0, s * 5.35), -3.5, -2.5, max(s * 5.0, s * 5.35), 2.5, -1.8, BD)

@design("happy_ghast", "Happy Ghast", "trend")
def _(m):
    W, WS = '#f6f6f8', '#e2e2ea'
    rbox(m, -2.8, 5.6, -2.8, 2.8, 10.6, 2.8, W, r=0.6)
    for i, (x, z, h) in enumerate([(-1.8, -1.8, 1.4), (0, -1.8, 1.0), (1.8, -1.8, 1.6), (-1.8, 0, 1.1), (1.8, 0, 0.9),
                                   (-1.8, 1.8, 1.5), (0, 1.8, 1.2), (1.8, 1.8, 1.0), (0, 0, 1.3)]):
        m.box(x - 0.35, 5.6 - h, z - 0.35, x + 0.35, 5.6, z + 0.35, WS)
    for x in (-1.6, 1.0):                                    # happy closed eyes ^ ^
        m.box(x, 8.4, -2.95, x + 0.6, 8.8, -2.8, BLACK); m.box(x - 0.3, 8.0, -2.95, x, 8.4, -2.8, BLACK); m.box(x + 0.6, 8.0, -2.95, x + 0.9, 8.4, -2.8, BLACK)
    m.box(-0.6, 7.0, -2.95, 0.6, 7.3, -2.8, BLACK)
    m.box(-2.6, 7.3, -2.95, -1.8, 7.8, -2.8, '#ffb7cf'); m.box(1.8, 7.3, -2.95, 2.6, 7.8, -2.8, '#ffb7cf')
    m.box(-2.9, 9.6, -2.9, 2.9, 10.0, 2.9, '#7a4a26')           # harness
    m.box(-2.9, 5.8, -0.3, 2.9, 10.0, 0.3, '#7a4a26')
    rbox(m, -2.2, 10.6, -1.4, -0.2, 11.6, 0.4, '#5ad1ff', r=0.3); rbox(m, 0.2, 10.6, -1.4, 2.2, 11.6, 0.4, '#5ad1ff', r=0.3)
    m.box(-0.2, 10.8, -0.8, 0.2, 11.2, -0.2, '#7a4a26')
    m.box(-0.6, 4.0, -0.6, 0.6, 4.6, 0.6, '#7a4a26')

@design("copper_golem", "Copper Golem Buddy", "trend")
def _(m):
    C, CD, CL, OX = '#c8714b', '#9c5235', '#e59a6e', '#5fa58c'
    rbox(m, -1.4, 4.0, -1.0, 1.4, 6.2, 1.0, C, r=0.3)
    rbox(m, -1.8, 6.2, -1.6, 1.8, 8.8, 1.6, C, r=0.4)
    m.box(-0.4, 6.6, -2.4, 0.4, 7.8, -1.6, CD)                   # nose
    m.box(-1.3, 7.6, -1.65, -0.6, 8.2, -1.6, '#2a1a12'); m.box(0.6, 7.6, -1.65, 1.3, 8.2, -1.6, '#2a1a12')
    m.box(-0.3, 8.8, -0.3, 0.3, 10.2, 0.3, CL); rbox(m, -0.6, 10.2, -0.6, 0.6, 11.2, 0.6, CL, r=0.25)   # lightning rod
    for s in (-1, 1):
        m.box(min(s * 1.4, s * 2.0), 4.4, -0.4, max(s * 1.4, s * 2.0), 6.0, 0.4, CD)                     # arms
        m.box(s * 0.8 - 0.35, 4.0, -2.2, s * 0.8 + 0.35, 4.6, -0.8, CD)                                  # legs dangling
    for x, y, z in [(-1.8, 7.0, 0.2), (1.2, 8.4, 1.0), (-0.8, 4.6, 1.0), (1.4, 5.2, -1.05)]:
        m.box(x, y, z, x + 0.6, y + 0.6, z + 0.06, OX)

@design("capybara", "Capybara Buddy", "trend")
def _(m):
    Bn, BD, Bl = '#a0703f', '#7d5530', '#b9864f'
    rbox(m, -2.4, 4.0, -2.6, 2.4, 7.0, 3.6, Bn, r=0.8)
    rbox(m, -1.9, 4.8, -5.0, 1.9, 7.6, -2.2, Bl, r=0.6)
    m.box(-1.5, 4.9, -5.6, 1.5, 6.4, -4.8, BD)                   # snout
    m.box(-0.8, 5.8, -5.7, -0.4, 6.2, -5.6, '#2a1a12'); m.box(0.4, 5.8, -5.7, 0.8, 6.2, -5.6, '#2a1a12')
    m.box(-1.6, 6.8, -5.05, -0.8, 7.2, -5.0, '#2a1a12'); m.box(0.8, 6.8, -5.05, 1.6, 7.2, -5.0, '#2a1a12')
    for s in (-1, 1):
        m.box(s * 1.5 - 0.4, 7.6, -3.4, s * 1.5 + 0.4, 8.2, -2.8, BD)
        m.box(s * 1.6 - 0.5, 4.0, -2.4, s * 1.6 + 0.5, 4.6, -1.2, BD)
    rbox(m, -0.8, 7.6, -4.2, 0.8, 9.0, -2.8, ORANGE, r=0.35)     # the orange
    m.box(-0.1, 9.0, -3.6, 0.1, 9.4, -3.4, '#4d7a26'); m.box(0.1, 9.1, -3.7, 0.9, 9.3, -3.3, LEAF)

@design("shark_hood", "Shark Hood", "trend")
def _(m):
    S, SD, Wb, T = '#6f8fb3', '#56728f', '#e8eef5', '#ffffff'
    rbox(m, -5.0, -4.8, 0.2, 5.0, 4.9, 5.0, S, r=1.0, top=False)
    m.box(-5.0, 4.0, -5.0, 5.0, 5.4, 1.4, S); rbox(m, -4.0, 5.4, -4.0, 4.0, 6.0, 4.0, S, r=0.8, top=False)
    for s in (-1, 1):
        m.box(min(s * 4.6, s * 5.0), -4.8, -5.0, max(s * 4.6, s * 5.0), 4.0, 1.4, S)
        m.box(min(s * 5.0, s * 5.15), 0.6, -2.2, max(s * 5.0, s * 5.15), 1.4, -1.4, BLACK)              # eyes
        for k in range(3):
            m.box(min(s * 5.0, s * 5.15), -2.6 + k * 0.7, 0.4, max(s * 5.0, s * 5.15), -2.4 + k * 0.7, 1.8, SD)  # gills
    m.box(-4.6, 4.0, -5.0, 4.6, 4.4, -4.6, Wb)
    for i in range(8):                                            # teeth around the face opening
        x = -4.0 + i * 1.14
        m.box(x - 0.35, 3.4, -5.05, x + 0.35, 4.0, -4.7, T)
    for s in (-1, 1):
        for k in range(5):
            y = 3.0 - k * 1.5
            m.box(min(s * 4.0, s * 4.6), y - 0.35, -5.05, max(s * 4.0, s * 4.4), y + 0.35, -4.7, T)
    for i, (z, h) in enumerate([(0.5, 2.6), (1.5, 2.0), (2.5, 1.3), (3.4, 0.7)]):   # dorsal fin
        m.box(-0.35, 6.0, z - 0.5, 0.35, 6.0 + h, z + 0.5, S if i % 2 == 0 else SD)
    m.box(-4.6, -4.8, -5.0, 4.6, -4.2, -4.6, Wb)

@design("frog_bucket", "Froggy Bucket Hat", "trend")
def _(m):
    G, GD = '#7cc65a', '#5ea544'
    m.box(-5.8, 3.0, -5.8, 5.8, 3.4, 5.8, GD)
    m.box(-5.0, 3.4, -5.0, 5.0, 3.9, 5.0, GD)
    dome(m, 3.9, [(4.6, 1.8), (4.2, 0.6), (3.6, 0.3)], G)
    for s in (-1, 1):
        rbox(m, s * 2.2 - 1.3, 6.2, -3.0, s * 2.2 + 1.3, 8.0, -0.6, G, r=0.5)
        m.box(s * 2.2 - 0.8, 6.6, -3.1, s * 2.2 + 0.8, 7.7, -3.0, WHITE)
        m.box(s * 2.2 - 0.4, 6.7, -3.2, s * 2.2 + 0.4, 7.3, -3.1, BLACK)
        m.box(s * 3.2 - 0.5, 4.6, -4.75, s * 3.2 + 0.5, 5.1, -4.6, '#ff9fb5')
    m.box(-1.6, 4.4, -4.75, 1.6, 4.7, -4.6, '#e0607a')

@design("strawberry_hat", "Strawberry Hat", "trend")
def _(m):
    R, RD, L = '#e8343f', '#c22632', '#4fa83a'
    dome(m, 3.0, [(4.7, 2.0), (4.4, 1.0), (3.8, 0.8), (2.8, 0.6), (1.6, 0.4)], R)
    for x, y, z in [(-3.0, 3.6, -4.8), (-1.0, 4.4, -4.8), (1.2, 3.4, -4.8), (3.0, 4.2, -4.8), (-2.0, 5.4, -4.5),
                    (0.4, 5.6, -4.5), (2.2, 5.6, -4.5), (-4.8, 4.0, -1.0), (4.8, 3.6, 1.0), (-4.8, 4.6, 2.2), (4.8, 4.8, -2.4)]:
        if abs(z) > 4.6:
            m.box(x - 0.2, y - 0.25, z, x + 0.2, y + 0.25, z + 0.15, '#ffe45c')
        else:
            m.box(x - 0.15 * (x < 0), y - 0.25, z - 0.2, x + 0.15 * (x > 0), y + 0.25, z + 0.2, '#ffe45c')
    for ang in (0, 45, 90, 135):
        m.box(-2.6, 7.7, -0.5, 2.6, 8.0, 0.5, L, rot=('y', [0, 22.5, 45, -22.5][ang // 45], (0, 7.8, 0)))
    m.box(-0.3, 7.8, -0.3, 0.3, 9.2, 0.3, '#3d7d2c')

@design("boba_buddy", "Boba Tea Buddy", "trend")
def _(m):
    m.box(-1.5, 4.1, -1.5, 1.5, 7.0, 1.5, '#cfa37a')               # milk tea
    for x, z in [(-0.9, -1.0), (0.2, -1.1), (1.0, -0.6), (-0.4, -0.2)]:
        m.box(x - 0.35, 4.15, z - 0.4, x + 0.35, 4.85, z + 0.3, '#2a1a14')   # pearls
    m.box(-1.8, 4.0, -1.8, 1.8, 8.0, 1.8, GLS)                      # clear cup
    m.box(-1.9, 8.0, -1.9, 1.9, 8.3, 1.9, '#ffb7d5')               # sealed lid
    m.box(-1.2, 5.6, -1.95, 1.2, 6.8, -1.8, '#ff9cc8'); m.box(-0.6, 5.9, -2.0, 0.6, 6.5, -1.95, WHITE)  # cute label
    m.box(0.3, 8.3, -0.3, 0.9, 11.6, 0.3, '#ff5ab4', rot=('z', -22.5, (0.6, 8.3, 0)))   # straw

@design("gaming_headset", "RGB Gaming Headset", "trend")
def _(m):
    m.box(-4.0, 4.6, -0.8, 4.0, 5.4, 0.8, '#1d1d26'); m.box(-3.0, 5.4, -0.4, 3.0, 5.6, 0.4, '#ff5ce1')
    for s in (-1, 1):
        m.box(min(s * 4.0, s * 4.7), 2.0, -0.6, max(s * 4.0, s * 4.7), 5.4, 0.6, '#1d1d26')
        rbox(m, min(s * 4.6, s * 6.0), -2.0, -2.2, max(s * 4.6, s * 6.0), 2.2, 2.2, '#24242e', r=0.7, top=False)
        m.box(min(s * 6.0, s * 6.15), -1.6, -1.8, max(s * 6.0, s * 6.15), 1.8, -1.2, '#7af7ff')
        m.box(min(s * 6.0, s * 6.15), -1.6, 1.2, max(s * 6.0, s * 6.15), 1.8, 1.8, '#ff5ce1')
        m.box(min(s * 6.0, s * 6.2), -0.6, -0.6, max(s * 6.0, s * 6.2), 0.8, 0.6, '#ffe45c')
    m.box(4.8, -1.4, -2.2, 5.4, -0.8, -0.8, '#1d1d26')                       # mic boom
    m.box(2.6, -2.4, -5.4, 5.2, -1.8, -4.8, '#1d1d26', rot=('y', -22.5, (5.0, -2.1, -2.0)))
    m.box(4.8, -1.4, -4.6, 5.4, -0.8, -2.2, '#1d1d26')
    m.box(4.6, -1.6, -5.2, 5.6, -0.6, -4.4, '#ff5ce1')

@design("butterfly_clips", "Butterfly Clips", "trend")
def _(m):
    cols = [('#c49bff', '#ff9fd2'), ('#9be7ff', '#a6ffef'), ('#ffb7d5', '#ffe45c'), ('#a6ffef', '#c49bff')]
    spots = [(4.6, 2.6, -2.4, 'x'), (4.6, 0.6, -0.4, 'x'), (-2.6, 4.6, -2.0, 'y'), (1.4, 4.6, 1.6, 'y')]
    for (x, y, z, ax), (c1, c2) in zip(spots, cols):
        if ax == 'x':
            m.box(x, y - 0.15, z - 0.9, x + 0.35, y + 0.15, z + 0.9, '#2a2440')
            for s in (-1, 1):
                m.box(x, y, z + s * 0.2 if s > 0 else z - 1.6, x + 0.25, y + 1.3, z + 1.6 if s > 0 else z - 0.2, c1, rot=('x', 22.5 * s, (x, y, z)))
                m.box(x, y - 1.0, z + 0.2 if s > 0 else z - 1.1, x + 0.25, y, z + 1.1 if s > 0 else z - 0.2, c2, rot=('x', -22.5 * s, (x, y, z)))
        else:
            m.box(x - 0.15, y, z - 0.9, x + 0.15, y + 0.35, z + 0.9, '#2a2440')
            for s in (-1, 1):
                m.box(x + 0.2 if s > 0 else x - 1.6, y, z - 0.1, x + 1.6 if s > 0 else x - 0.2, y + 0.25, z + 1.3, c1, rot=('z', 22.5 * s, (x, y, z)))
                m.box(x + 0.2 if s > 0 else x - 1.1, y, z - 1.0, x + 1.1 if s > 0 else x - 0.2, y + 0.25, z, c2, rot=('z', 22.5 * s, (x, y, z)))

@design("star_clips", "Star Clips", "trend")
def _(m):
    for (y, z, sc, c) in [(3.0, -2.6, 0.9, '#ffe45c'), (1.4, -0.6, 0.6, '#ff9fd2'), (3.2, 0.9, 0.5, '#7af7ff'), (-0.2, -2.4, 0.45, '#ffe45c')]:
        star(m, 4.6, y, z, sc, c, axis='x')
    star(m, -1.5, 5.2, -4.6, 0.7, '#ffe45c')
    m.box(-1.8, 4.0, -4.7, -1.2, 4.6, -4.6, SILVER)

@design("cherry_blossom_crown", "Cherry Blossom Crown", "trend")
def _(m):
    Br = '#5a3a2e'
    band(m, 3.7, 4.2, Br, 4.6)
    pink = ['#ffb7d5', '#ff9cc8', '#ffd1e6']
    k = 0
    for x in (-3.4, -1.2, 1.0, 3.2):
        flower(m, x, 4.3, -4.6, pink[k % 3], centre='#ffe45c', s=0.8); k += 1
    for z in (-2.4, 0.2, 2.6):
        for s in (-1, 1):
            m.box(min(s * 4.6, s * 4.95), 3.6, z - 0.7, max(s * 4.6, s * 4.95), 4.4, z + 0.7, pink[k % 3]); k += 1
            m.box(min(s * 4.95, s * 5.05), 3.85, z - 0.2, max(s * 4.95, s * 5.05), 4.15, z + 0.2, '#ffe45c')
    for x in (-2.0, 0.6, 2.4):
        flower(m, x, 4.2, 4.6, pink[(k := k + 1) % 3], centre='#ffe45c', s=0.7)
    for x, y, z in [(-3.8, 6.2, -2.0), (2.6, 7.0, -3.0), (0.2, 6.6, 1.0)]:     # drifting petals
        m.box(x, y, z, x + 0.5, y + 0.15, z + 0.5, '#ffd1e6')
    m.box(2.6, 4.2, -4.8, 4.2, 4.5, -4.6, Br, rot=('z', 22.5, (2.6, 4.3, -4.7)))

@design("heart_halo", "Heart Halo", "trend")
def _(m):
    ring(m, 6.6, 3.6, '#ff9fd2', t=0.8, h=0.6)
    for (x, z, rot) in [(0, -3.6, 0), (0, 3.6, 0)]:
        heart(m, x, 8.0, z - 0.3 if z < 0 else z + 0.3, 0.45, '#ff5ab4', t=0.3, hi='#ffffff')
    for s in (-1, 1):
        m.box(min(s * 3.6, s * 3.9), 7.5, -0.5, max(s * 3.6, s * 3.9), 8.5, 0.5, '#ff5ab4')
        m.box(min(s * 3.6, s * 3.9), 8.0, -0.9, max(s * 3.6, s * 3.9), 8.5, 0.9, '#ff5ab4')

@design("allay_buddy", "Allay Buddy", "trend")
def _(m):
    A, AD = '#4fd8ff', '#2fb0e0'
    rbox(m, -1.4, 8.2, -1.4, 1.4, 10.8, 1.4, A, r=0.4)
    m.box(-0.8, 6.4, -0.7, 0.8, 8.2, 0.7, AD); m.box(-0.5, 5.6, -0.5, 0.5, 6.4, 0.5, AD)
    m.box(-1.0, 9.2, -1.5, -0.4, 9.8, -1.4, '#1d2a40'); m.box(0.4, 9.2, -1.5, 1.0, 9.8, -1.4, '#1d2a40')
    for s in (-1, 1):
        m.box(min(s * 0.8, s * 4.0), 6.6, 0.6, max(s * 0.8, s * 4.0), 8.6, 0.8, '#c6f6ff80', rot=('y', 22.5 * s, (s * 0.8, 7.6, 0.7)))
        m.box(min(s * 0.8, s * 1.4), 6.8, -0.3, max(s * 0.8, s * 1.4), 7.8, 0.3, AD)
    rbox(m, -0.5, 4.8, -1.6, 0.5, 5.8, -0.6, '#ffe45c', r=0.25)

@design("sniffer_buddy", "Sniffer Buddy", "trend")
def _(m):
    Rd, RdD, Ms, Ns = '#a4413a', '#7e2f2a', '#5d8a3a', '#e3b04a'
    rbox(m, -2.4, 4.6, -2.4, 2.4, 7.6, 3.4, Rd, r=0.6)
    rbox(m, -2.0, 7.6, -1.6, 2.0, 8.4, 3.0, Ms, r=0.6)
    for x, z in [(-1.4, 0.0), (0.6, 1.6), (1.2, -0.8)]:
        m.box(x - 0.2, 8.4, z - 0.2, x + 0.2, 9.0, z + 0.2, '#7cc65a')
    rbox(m, -1.8, 5.2, -4.6, 1.8, 7.6, -2.4, RdD, r=0.5)
    m.box(-1.0, 5.0, -6.0, 1.0, 6.4, -4.6, Ns)
    m.box(-1.4, 6.8, -4.65, -0.7, 7.3, -4.6, BLACK); m.box(0.7, 6.8, -4.65, 1.4, 7.3, -4.6, BLACK)
    for x in (-1.6, 1.6):
        for z in (-1.6, 0.6, 2.6):
            m.box(x - 0.4, 4.0, z - 0.4, x + 0.4, 4.6, z + 0.4, RdD)

@design("duck_buddy", "Duck Buddy (Shades)", "trend")
def _(m):
    Y, O = '#ffd93a', '#ff9a1f'
    rbox(m, -2.2, 4.0, -2.0, 2.2, 6.4, 3.0, Y, r=0.7)
    rbox(m, -1.6, 6.0, -2.4, 1.6, 8.8, 0.6, Y, r=0.6)
    m.box(-1.0, 6.6, -3.6, 1.0, 7.3, -2.4, O)
    m.box(-1.7, 7.6, -2.5, 1.7, 8.2, -2.4, BLACK); m.box(-1.6, 7.3, -2.5, -0.2, 7.6, -2.4, BLACK); m.box(0.2, 7.3, -2.5, 1.6, 7.6, -2.4, BLACK)
    m.box(1.0, 7.9, -2.55, 1.4, 8.1, -2.5, '#9a8ad6')
    m.box(-0.6, 5.4, 3.0, 0.6, 6.6, 3.6, Y)
    for s in (-1, 1):
        m.box(min(s * 2.2, s * 2.5), 4.6, -0.6, max(s * 2.2, s * 2.5), 5.8, 1.8, '#f5c52e')

@design("neon_horns", "Neon Cyber Horns", "trend")
def _(m):
    band(m, 3.2, 3.8, '#14141c', 4.6)
    for s in (-1, 1):
        x = s * 2.6
        r = ('z', -22.5 * s, (x, 4.0, -1.0))
        m.box(x - 0.6, 4.0, -1.6, x + 0.6, 7.4, -0.4, '#14141c', rot=r)
        m.box(x - 0.4, 7.4, -1.4, x + 0.4, 8.6, -0.6, '#14141c', rot=r)
        m.box(x - 0.65, 4.4, -1.7, x - 0.45, 8.0, -1.5, '#7af7ff', rot=r)
        m.box(x + 0.45, 4.4, -1.7, x + 0.65, 7.0, -1.5, '#ff5ce1', rot=r)
        m.box(x - 0.2, 8.6, -1.2, x + 0.2, 9.2, -0.8, '#7af7ff', rot=r)
    m.box(-1.6, 3.3, -4.75, 1.6, 3.7, -4.6, '#7af7ff')

@design("bear_beanie", "Bear Beanie", "trend")
def _(m):
    Cr, CrD, Br = '#efe2cf', '#ddcdb4', '#8a5a36'
    for i, x in enumerate([-4.6 + 0.92 * k for k in range(10)]):
        m.box(x, 1.4, -4.6, x + 0.92, 3.0, 4.6, CrD if i % 2 else Cr)
    dome(m, 3.0, [(4.6, 1.6), (4.3, 1.0), (3.6, 0.6), (2.6, 0.3)], Cr)
    for s in (-1, 1):
        rbox(m, s * 2.9 - 1.3, 5.6, -0.8, s * 2.9 + 1.3, 8.0, 0.8, Cr, r=0.6)
        rbox(m, s * 2.9 - 0.7, 6.0, -1.0, s * 2.9 + 0.7, 7.4, -0.8, Br, r=0.3, top=False)
    m.box(-1.2, 3.4, -4.75, 1.2, 4.6, -4.6, Br); m.box(-0.4, 4.0, -4.85, 0.4, 4.4, -4.75, BLACK)
    m.box(-2.0, 4.8, -4.75, -1.4, 5.4, -4.6, BLACK); m.box(1.4, 4.8, -4.75, 2.0, 5.4, -4.6, BLACK)


def mirrored(fn):
    """Same accessory on the other side of the head (so side pieces face the hero camera)."""
    def g(m):
        n0 = len(m.boxes); fn(m)
        for b in m.boxes[n0:]:
            (fx, fy, fz), (tx, ty, tz) = b['f'], b['t']
            b['f'], b['t'] = (-tx, fy, fz), (-fx, ty, tz)
            if b['rot']:
                ax, ang, (ox, oy, oz) = b['rot']
                b['rot'] = (ax, ang if ax == 'x' else -ang, (-ox, oy, oz))
    return g

for _i, (_n, _t, _tier, _fn) in enumerate(D):
    if _n in ("kitsune_mask", "butterfly_clips", "star_clips", "gaming_headset"):
        D[_i] = (_n, _t, _tier, mirrored(_fn))


# ======================================================================
# MEME batch
# ======================================================================
@design("deal_with_it", "Deal With It Shades", "meme")
def _(m):
    K, Wt = '#0d0d10', '#ffffff'
    relief(m, ["KKKKKKKKKKKKKKKKKK",
               "KKKKKKKK..KKKKKKKK",
               ".KKWKKKK...KKWKKK.",
               ".KWKKKK.....KWKKK.",
               "..KKKK.......KKK.."], -4.6, {'K': (K, 0.45), 'W': (Wt, 0.5)}, cell=0.52, top=2.4)
    for s in (-1, 1):
        m.box(min(s * 4.6, s * 4.8), 1.5, -4.6, max(s * 4.6, s * 4.8), 2.0, 2.5, K)

@design("chicken_jockey", "Chicken Jockey", "meme")
def _(m):
    W, Y, R, Z, ZD, Sh = '#f4f4f0', '#f2b33a', '#d8323a', '#5aa04a', '#3f7a35', '#3c9fd8'
    rbox(m, -2.0, 4.0, -2.4, 2.0, 7.0, 2.6, W, r=0.6)                      # chicken body
    rbox(m, -1.3, 6.4, -3.4, 1.3, 9.2, -1.2, W, r=0.4)                     # chicken head
    m.box(-0.8, 7.4, -4.4, 0.8, 8.2, -3.4, Y); m.box(-0.5, 6.6, -3.6, 0.5, 7.4, -3.4, R)
    m.box(-1.0, 8.4, -3.45, -0.5, 8.9, -3.4, BLACK); m.box(0.5, 8.4, -3.45, 1.0, 8.9, -3.4, BLACK)
    for s in (-1, 1):
        m.box(min(s * 2.0, s * 2.4), 4.6, -1.6, max(s * 2.0, s * 2.4), 6.4, 1.8, '#e4e4de')
    m.box(-0.8, 7.0, 1.2, 0.8, 7.6, 2.6, W)
    # baby zombie rider
    rbox(m, -1.2, 7.0, -0.6, 1.2, 9.2, 1.4, Sh, r=0.3)                     # shirt
    for s in (-1, 1):
        m.box(s * 0.7 - 0.45, 7.0, -1.8, s * 0.7 + 0.45, 7.6, -0.4, '#3b3f8f')   # legs
        m.box(min(s * 1.2, s * 1.9), 8.4, -2.4, max(s * 1.2, s * 1.9), 9.0, 0.2, Z)  # arms out front
    rbox(m, -1.6, 9.2, -1.2, 1.6, 12.2, 1.8, Z, r=0.3)
    m.box(-1.0, 10.4, -1.25, -0.4, 11.0, -1.2, BLACK); m.box(0.4, 10.4, -1.25, 1.0, 11.0, -1.2, BLACK)
    m.box(-0.6, 9.6, -1.25, 0.6, 9.9, -1.2, ZD)

@design("lava_chicken", "Lava Chicken", "meme")
def _(m):
    Ck, CkD, Bn, L, LD = '#c98a4a', '#9e6532', '#efe6d6', '#ff7a1f', '#ffc23a'
    m.box(-3.2, 4.0, -3.2, 3.2, 4.4, 3.2, '#d9d4cc')                       # plate
    rbox(m, -2.4, 4.4, -1.8, 2.4, 7.0, 2.2, Ck, r=0.8)                     # roast chicken
    for s in (-1, 1):
        m.box(s * 1.4 - 0.6, 5.6, -3.4, s * 1.4 + 0.6, 6.6, -1.8, CkD)
        m.box(s * 1.4 - 0.3, 5.8, -4.2, s * 1.4 + 0.3, 6.4, -3.4, Bn)
    for x, z, h in [(-1.2, -1.0, 1.2), (0.4, 0.4, 1.8), (1.4, -0.6, 0.9)]:  # lava pouring over it
        m.box(x - 0.45, 6.6, z - 0.45, x + 0.45, 7.2, z + 0.45, LD)
        m.box(x - 0.3, 7.0 - h - 1.2, -1.95, x + 0.3, 7.0, -1.8, L)
    m.box(-0.5, 8.6, -0.5, 0.5, 11.0, 0.5, L); m.box(-0.8, 7.0, -0.8, 0.8, 8.6, 0.8, LD)

@design("banana_cat", "Banana Cat", "meme")
def _(m):
    Y, YD, Br = '#ffd93a', '#e6b81c', '#5a3a1e'
    rbox(m, -5.0, -4.8, 0.2, 5.0, 4.9, 5.0, Y, r=1.0, top=False)           # banana peel hood
    m.box(-5.0, 4.0, -5.0, 5.0, 5.4, 1.4, Y); rbox(m, -4.0, 5.4, -4.0, 4.0, 6.0, 4.0, Y, r=0.8, top=False)
    for s in (-1, 1):
        m.box(min(s * 4.6, s * 5.0), -4.8, -5.0, max(s * 4.6, s * 5.0), 4.0, 1.4, Y)
        m.box(min(s * 5.0, s * 5.15), -4.8, -2.0, max(s * 5.0, s * 5.15), 4.0, -1.6, YD)          # peel seams
        for i, w in enumerate([2.4, 1.6, 0.8]):                                                   # cat ears
            m.box(s * 2.6 - w / 2, 6.0 + i * 0.7, -0.6, s * 2.6 + w / 2, 6.7 + i * 0.7, 0.6, Y)
    m.box(-0.5, 6.0, 4.0, 0.5, 8.6, 5.0, YD); m.box(-0.4, 8.6, 4.2, 0.4, 9.2, 4.8, Br)          # banana stem
    m.box(-4.6, 4.0, -5.0, 4.6, 4.4, -4.6, YD)

@design("bread_face", "Bread Face", "meme")
def _(m):
    Cr, In = '#b0672b', '#f3d9a4'
    # slice of toast with the face poking through the hole
    m.box(-5.6, -5.0, -5.4, 5.6, 4.0, -4.6, In)
    rbox(m, -6.0, 3.0, -5.4, 6.0, 7.4, -4.6, In, r=1.6, top=False)
    m.box(-6.0, -5.0, -5.4, -5.6, 4.0, -4.6, Cr); m.box(5.6, -5.0, -5.4, 6.0, 4.0, -4.6, Cr)
    m.box(-5.6, -5.4, -5.4, 5.6, -5.0, -4.6, Cr)
    rbox(m, -6.4, 3.0, -5.4, 6.4, 7.8, -4.6, Cr, r=1.8, top=False)
    m.box(-4.4, -4.0, -5.5, 4.4, 3.6, -5.35, '#ffffff00')  # (hole is just not drawn)

@redesign("bread_face")
def _(m):
    Cr, In = '#b0672b', '#f3d9a4'
    z1, z2 = -5.4, -4.6
    m.box(-6.0, -5.4, z1, 6.0, -4.2, z2, Cr)                                 # bottom crust
    m.box(-5.4, -4.2, z1, 5.4, -3.6, z2, In)
    for s in (-1, 1):
        m.box(min(s * 5.4, s * 6.0), -4.2, z1, max(s * 5.4, s * 6.0), 4.2, z2, Cr)
        m.box(min(s * 4.0, s * 5.4), -3.6, z1, max(s * 4.0, s * 5.4), 4.2, z2, In)
    # domed top of the slice
    m.box(-5.4, 4.2, z1, 5.4, 6.2, z2, In); m.box(-6.0, 4.2, z1, 6.0, 5.4, z2, Cr)
    m.box(-5.4, 6.2, z1, 5.4, 6.8, z2, Cr); m.box(-4.4, 6.8, z1, 4.4, 7.4, z2, Cr)
    m.box(-5.4, 5.4, z1, -4.4, 6.8, z2, Cr); m.box(4.4, 5.4, z1, 5.4, 6.8, z2, Cr)
    m.box(-4.4, 3.6, z1, 4.4, 4.2, z2, In)
    for x, y in [(-4.8, 1.0), (4.6, -2.0), (-2.0, 5.6), (2.6, 5.0)]:
        m.box(x, y, z1 - 0.05, x + 0.5, y + 0.4, z1, '#e2c08a')

@design("tinfoil_hat", "Tinfoil Hat", "meme")
def _(m):
    F1, F2 = '#d7dbe2', '#aeb4be'
    for i, w in enumerate([9.6, 8.0, 6.4, 4.8, 3.2, 1.8, 0.8]):
        r = ('y', 22.5 if i % 2 else 0, (0, 4, 0))
        m.box(-w / 2, 4.0 + i * 0.9, -w / 2, w / 2, 4.9 + i * 0.9, w / 2, F1 if i % 2 == 0 else F2, rot=r)
    for x, y, z in [(-3.0, 4.4, -4.85), (1.6, 5.4, -4.05), (-1.0, 6.6, -3.2), (3.4, 4.6, -4.85)]:
        m.box(x, y, z - 0.1, x + 0.6, y + 0.4, z, '#ffffff')

@design("bucket_head", "Bucket Head", "meme")
def _(m):
    I1, I2, I3 = '#c9ced8', '#a3a9b4', '#7d838e'
    rbox(m, -5.0, 0.6, -5.0, 5.0, 6.4, 5.0, I1, r=1.0, top=False)
    rbox(m, -4.0, 6.4, -4.0, 4.0, 7.2, 4.0, I2, r=0.8, top=False)
    m.box(-5.3, 0.6, -5.3, 5.3, 1.4, 5.3, I3)
    for s in (-1, 1):
        m.box(min(s * 5.0, s * 5.4), 3.2, -0.5, max(s * 5.0, s * 5.4), 4.2, 0.5, I3)
    m.box(-5.6, 0.4, -0.25, -5.4, 3.6, 0.25, I3); m.box(5.4, 0.4, -0.25, 5.6, 3.6, 0.25, I3)
    m.box(-5.6, 0.2, -0.25, 5.6, 0.6, 0.25, I3)          # handle swinging under the chin
    m.box(-3.2, 2.0, -5.15, -2.4, 2.8, -5.0, '#e6e8ee')

@design("shiba_buddy", "Shiba Buddy", "meme")
def _(m):
    O, Cr = '#e3a052', '#f6ead6'
    rbox(m, -2.2, 4.0, -1.6, 2.2, 6.6, 3.0, O, r=0.7)
    rbox(m, -2.0, 6.0, -3.2, 2.0, 8.8, -0.4, O, r=0.6)
    m.box(-1.2, 6.0, -4.2, 1.2, 7.2, -3.2, Cr); m.box(-0.4, 6.9, -4.3, 0.4, 7.3, -4.2, BLACK)
    m.box(-1.6, 7.4, -3.25, -0.8, 7.7, -3.2, BLACK); m.box(0.8, 7.4, -3.25, 1.6, 7.7, -3.2, BLACK)  # smug eyes
    m.box(-1.7, 7.9, -3.25, -1.2, 8.1, -3.2, Cr); m.box(1.2, 7.9, -3.25, 1.7, 8.1, -3.2, Cr)
    for s in (-1, 1):
        steps(m, s * 1.3, -1.8, 8.8, [1.2, 0.8, 0.4], O, depth=0.6, h=0.5)
    m.box(-0.4, 6.0, 3.0, 0.4, 7.6, 3.8, O); m.box(-0.4, 7.6, 2.2, 0.4, 8.2, 3.6, Cr)            # curly tail
    m.box(-1.6, 4.0, -1.7, 1.6, 5.4, -1.6, Cr)

@design("fish_slap", "Fish On Head", "meme")
def _(m):
    F, FD, FL = '#7fb3c8', '#5b8ea3', '#c9e6ef'
    rbox(m, -0.9, 4.0, -3.6, 0.9, 5.6, 2.4, F, r=0.4)
    m.box(-0.9, 4.0, -3.6, 0.9, 4.6, 2.4, FL)
    m.box(-0.5, 4.2, 2.4, 0.5, 5.4, 3.2, FD); m.box(-0.6, 3.8, 3.2, 0.6, 5.8, 3.8, FD)            # tail
    m.box(-0.2, 5.6, -1.6, 0.2, 6.2, 0.6, FD)
    m.box(-0.95, 4.9, -3.0, -0.9, 5.3, -2.6, BLACK); m.box(0.9, 4.9, -3.0, 0.95, 5.3, -2.6, BLACK)
    m.box(-0.5, 4.3, -3.9, 0.5, 4.8, -3.6, '#e88aa0')

@design("groucho_disguise", "Disguise Glasses", "meme")
def _(m):
    K, Sk, Mu = '#141418', '#e8a98a', '#2a1a12'
    for s in (-1, 1):
        m.box(s * 2.2 - 1.6, 0.0, -4.85, s * 2.2 + 1.6, 0.4, -4.6, K); m.box(s * 2.2 - 1.6, 1.8, -4.85, s * 2.2 + 1.6, 2.2, -4.6, K)
        m.box(s * 2.2 - 1.6, 0.4, -4.85, s * 2.2 - 1.2, 1.8, -4.6, K); m.box(s * 2.2 + 1.2, 0.4, -4.85, s * 2.2 + 1.6, 1.8, -4.6, K)
        m.box(s * 2.2 - 1.4, 2.4, -4.9, s * 2.2 + 1.4, 3.2, -4.6, K)                                   # bushy brows
        m.box(min(s * 4.6, s * 4.8), 1.6, -4.85, max(s * 4.6, s * 4.8), 2.0, 2.0, K)
    m.box(-0.6, 0.6, -4.85, 0.6, 1.0, -4.6, K)
    rbox(m, -0.8, -1.4, -6.4, 0.8, 1.0, -4.6, Sk, r=0.3)                                               # big nose
    m.box(-2.6, -2.2, -5.0, 2.6, -1.4, -4.6, Mu); m.box(-2.2, -2.6, -5.0, -1.0, -2.2, -4.6, Mu); m.box(1.0, -2.6, -5.0, 2.2, -2.2, -4.6, Mu)

@design("clown_wig", "Clown Wig", "meme")
def _(m):
    cols = ['#ff4040', ORANGE, YELLOW, '#4cc34a', '#3b8cff', '#b066ff']
    k = 0
    for x in (-4.4, -1.5, 1.5, 4.4):
        for y in (3.4, 5.8):
            for z in (-2.6, 0.2, 3.0):
                if abs(x) < 3 and y < 4 and z < 0:
                    continue
                rbox(m, x - 1.6, y - 1.4, z - 1.6, x + 1.6, y + 1.4, z + 1.6, cols[k % 6], r=0.6); k += 1
    rbox(m, -0.9, -1.0, -5.8, 0.9, 0.8, -4.6, '#e8202a', r=0.4)
    m.box(-0.3, 0.2, -5.85, 0.2, 0.6, -5.8, '#ff9a9a')

@design("herobrine_eyes", "Herobrine Eyes", "meme")
def _(m):
    for s in (-1, 1):
        m.box(s * 2.2 - 1.1, 0.0, -4.85, s * 2.2 + 1.1, 1.0, -4.6, '#ffffff')
    m.box(-4.6, 0.0, -4.7, 4.6, 1.0, -4.62, '#c9f7ff60')  # faint glow haze

@design("watermelon_helmet", "Watermelon Helmet", "meme")
def _(m):
    G, GD, Wr, R = '#3f8f3a', '#2c6b28', '#e8f2d0', '#e8343f'
    dome(m, 2.0, [(5.0, 2.4), (4.7, 1.2), (4.2, 0.8), (3.4, 0.6), (2.2, 0.4)], G)
    for x in (-3.4, -1.1, 1.1, 3.4):
        m.box(x - 0.4, 2.0, -5.05, x + 0.4, 5.4, -4.95, GD); m.box(x - 0.4, 2.0, 4.95, x + 0.4, 5.4, 5.05, GD)
    m.box(-5.0, 1.4, -5.0, 5.0, 2.0, 5.0, Wr)
    m.box(-4.7, 0.8, -4.7, 4.7, 1.4, 4.7, R)
    for x, z in [(-3.0, -4.75), (-0.8, -4.75), (1.6, -4.75), (3.4, -4.75), (-4.75, -1.0), (4.75, 1.4)]:
        m.box(x - 0.2, 1.0, z - 0.05, x + 0.2, 1.3, z + 0.05, BLACK)


# ======================================================================
# TAGGY & FROGGIE (from lojjkli's animation)
# ======================================================================
TG, TGD, TGL, SMILE = '#3a2d78', '#2e2366', '#4b3a8f', '#fdfdff'
FG, FGD, FGL, FTAN, FMOUTH, FTONGUE = '#568022', '#3a5a19', '#63902e', '#bead6a', '#2e1d10', '#ff8a8a'
GLOW.add(SMILE)

def taggy(m, x=0.0, y=4.0, z=0.0, s=1.0, wave=False):
    """Taggy: small speckled-amethyst buddy, head a bit taller than a cube, glowing pixel smile."""
    S = lambda v: v * s
    # feet dangling over the front + body
    for sd in (-1, 1):
        m.box(x + sd * S(0.7) - S(0.45), y, z - S(2.0), x + sd * S(0.7) + S(0.45), y + S(0.7), z - S(0.6), TGD)
    rbox(m, x - S(1.3), y, z - S(0.8), x + S(1.3), y + S(2.0), z + S(0.9), TG, r=S(0.3))
    for sd in (-1, 1):  # arms
        ay2 = y + S(3.4) if (wave and sd < 0) else y + S(1.8)
        m.box(min(x + sd * S(1.3), x + sd * S(1.9)), y + S(0.4) if not (wave and sd < 0) else y + S(1.4), z - S(0.35),
              max(x + sd * S(1.3), x + sd * S(1.9)), ay2, z + S(0.35), TGD)
    hy = y + S(2.0)
    rbox(m, x - S(1.8), hy, z - S(1.6), x + S(1.8), hy + S(3.6), z + S(1.6), TG, r=S(0.35))
    m.box(x - S(1.85), hy + S(3.2), z - S(1.65), x + S(1.85), hy + S(3.65), z + S(1.65), TGL)
    # glowing smile: corner pixels + bar
    f = z - S(1.6)
    px = S(0.45)
    m.box(x + S(1.1) - px, hy + S(1.6), f - 0.12, x + S(1.1), hy + S(1.6) + px, f, SMILE)
    m.box(x - S(1.1), hy + S(1.6), f - 0.12, x - S(1.1) + px, hy + S(1.6) + px, f, SMILE)
    m.box(x - S(1.1) + px, hy + S(1.6) - px, f - 0.12, x + S(1.1) - px, hy + S(1.6), f, SMILE)

def froggie(m, x=0.0, y=4.0, z=0.0, s=1.0, tongue=True):
    """Froggie: vanilla-style frog in its own texture colours (green body, tan back, dark mouth)."""
    S = lambda v: v * s
    for sd in (-1, 1):  # splayed feet + legs
        m.box(x + sd * S(2.6) - S(1.0), y, z + S(0.4), x + sd * S(2.6) + S(1.0), y + S(0.2), z + S(2.6), FGD)
        m.box(x + sd * S(1.8) - S(0.6), y, z - S(3.4), x + sd * S(1.8) + S(0.6), y + S(0.2), z - S(2.2), FGD)
        rbox(m, x + sd * S(2.4) - S(0.7), y, z + S(0.6), x + sd * S(2.4) + S(0.7), y + S(1.6), z + S(2.4), FG, r=S(0.25))
    rbox(m, x - S(2.4), y + S(0.4), z - S(3.2), x + S(2.4), y + S(1.4), z + S(2.6), FMOUTH, r=S(0.3), top=False)  # dark jaw line
    rbox(m, x - S(2.4), y + S(0.2), z - S(3.0), x + S(2.4), y + S(0.6), z + S(2.6), FG, r=S(0.3), top=False)   # lower jaw
    rbox(m, x - S(2.4), y + S(1.2), z - S(3.2), x + S(2.4), y + S(2.6), z + S(2.6), FG, r=S(0.4))             # upper head/body
    m.box(x - S(1.8), y + S(2.6), z - S(0.6), x + S(1.8), y + S(2.8), z + S(2.4), FTAN)                       # tan back
    for sd in (-1, 1):  # eyes
        rbox(m, x + sd * S(1.5) - S(0.8), y + S(2.4), z - S(2.8), x + sd * S(1.5) + S(0.8), y + S(3.6), z - S(1.2), FGL, r=S(0.2))
        m.box(x + sd * S(1.5) - S(0.6), y + S(2.8), z - S(2.9), x + sd * S(1.5) + S(0.6), y + S(3.2), z - S(2.8), FMOUTH)
    if tongue:
        m.box(x - S(0.4), y + S(0.6), z - S(4.6), x + S(0.4), y + S(0.8), z - S(3.2), FTONGUE)
        m.box(x - S(0.6), y + S(0.5), z - S(5.1), x + S(0.6), y + S(0.9), z - S(4.5), '#e55e5e')

def name_tag(m, x, y, z, col='#c9a46a'):
    """Little Minecraft name tag hanging off the side."""
    m.box(x - 0.1, y, z - 1.4, x + 0.1, y + 1.0, z + 0.6, col)
    m.box(x - 0.1, y + 0.2, z + 0.6, x + 0.1, y + 0.8, z + 1.0, col)
    m.box(x - 0.15, y + 0.4, z + 0.7, x + 0.15, y + 0.6, z + 0.9, '#5a3a1e')
    m.box(x - 0.15, y + 0.35, z - 1.1, x + 0.15, y + 0.45, z + 0.3, '#5a3a1e')
    m.box(x - 0.05, y + 0.6, z + 1.0, x + 0.05, y + 1.8, z + 1.1, '#e8e2d2')

@design("taggy_buddy", "Taggy Buddy", "custom")
def _(m):
    taggy(m, 0, 4.0, 0.4, s=1.0)
    name_tag(m, -2.0, 6.4, 1.2)

@design("taggy_wave", "Taggy Waving", "custom")
def _(m):
    taggy(m, 0.6, 4.0, 0.2, s=1.1, wave=True)

@design("taggy_mask", "Taggy Head", "custom")
def _(m):
    shell(m, 5.0, TG, r=0.9, y1=-5.0, y2=5.6)
    m.box(-5.05, 4.6, -5.05, 5.05, 5.0, 5.05, TGL)
    relief(m, ["..W....W..",
               "...WWWW..."], -5.0, {'W': (SMILE, 0.25)}, top=-0.2, cell=0.9)
    name_tag(m, -5.05, 2.0, 2.4)

@design("froggie_buddy", "Froggie Buddy", "custom")
def _(m):
    froggie(m, 0, 4.0, 0.6, s=1.0)
    name_tag(m, 2.6, 5.2, 1.6)

@design("froglight_crown", "Froglight Crown", "custom")
def _(m):
    band(m, 3.6, 4.4, FGD, 4.6)
    for (x, c, cl) in [(-3.0, '#f3d27a', '#fff2c2'), (0.0, '#e9c8e8', '#fff0ff'), (3.0, '#b8e6a6', '#effff0')]:
        rbox(m, x - 1.1, 4.4, -5.1, x + 1.1, 6.6, -2.9, c, r=0.3)
        m.box(x - 0.6, 4.9, -5.15, x + 0.6, 6.1, -5.1, cl)
    GLOW.update({'#fff2c2', '#fff0ff', '#effff0'})
    for s in (-1, 1):  # frog eyes peeking over the back
        rbox(m, s * 1.6 - 0.9, 4.4, 1.6, s * 1.6 + 0.9, 6.0, 3.4, FG, r=0.3)
        m.box(s * 1.6 - 0.6, 4.9, 1.5, s * 1.6 + 0.6, 5.5, 1.6, FMOUTH)

@design("taggy_froggie_duo", "Taggy & Froggie Duo", "custom")
def _(m):
    taggy(m, -1.9, 4.0, 0.6, s=0.75)
    froggie(m, 2.0, 4.0, 0.4, s=0.62, tongue=True)


# ---- Taggy, rebuilt from the animation's own model (taggy_model.blend / taggy_dimensions.txt) ----
TAGGY_P, TAGGY_BAR, TAGGY_EYE = '#a172d0', '#ffffff', '#f6edff'
GLOW.update({TAGGY_BAR, TAGGY_EYE})
TAGGY_HEAD_TOP = 0.952 + 0.06   # head made ~12% taller on top in the latest animation

def taggy(m, x=0.0, y=4.0, z=0.0, s=5.8, wave=False):
    """Exact Taggy proportions. Blender units (Z up, face -Y) -> head pixels (Y up, face -Z, X mirrored).
    s = head pixels per Blender unit; the feet bottom (z=-0.136) sits at y."""
    def T(x1, y1, z1, x2, y2, z2, c, rot=None):
        m.box(x - x2 * s, y + (z1 + 0.136) * s, z + y1 * s, x - x1 * s, y + (z2 + 0.136) * s, z + y2 * s, c, rot=rot)
    T(-0.312, -0.281, 0.452, 0.312, 0.281, TAGGY_HEAD_TOP, TAGGY_P)          # head
    T(-0.156, -0.125, 0.032, 0.156, 0.125, 0.452, TAGGY_P)                   # body
    for sd in (-1, 1):
        T(min(sd * 0.031, sd * 0.256), -0.359, -0.136, max(sd * 0.031, sd * 0.256), -0.134, 0.076, TAGGY_P)   # feet
        if wave and sd == -1:   # raised arm, swung up from the shoulder
            sx, sy = x - sd * 0.25 * s, y + (0.42 + 0.136) * s
            T(min(sd * 0.184, sd * 0.316), -0.066, 0.42, max(sd * 0.184, sd * 0.316), 0.066, 0.826, TAGGY_P,
              rot=('z', -22.5, (sx, sy, z)))
        else:
            T(min(sd * 0.184, sd * 0.316), -0.066, 0.014, max(sd * 0.184, sd * 0.316), 0.066, 0.42, TAGGY_P)  # arms
    T(-0.133, -0.305, 0.52, 0.133, -0.281, 0.592, TAGGY_BAR)                  # smile bar
    for sd in (-1, 1):
        T(min(sd * 0.133, sd * 0.205), -0.305, 0.592, max(sd * 0.133, sd * 0.205), -0.281, 0.664, TAGGY_EYE)  # glowing corners

@redesign("taggy_buddy")
def _(m):
    taggy(m, 0, 4.0, 0.6, s=5.8)
    name_tag(m, -2.2, 6.6, 1.6)

@redesign("taggy_wave")
def _(m):
    taggy(m, 0, 4.0, 0.6, s=6.2, wave=True)

@redesign("taggy_mask")
def _(m):
    # Taggy's head as a full mask: same 0.625 x 0.56 x 0.5 proportions and smile placement, scaled up
    shell(m, 5.0, TAGGY_P, r=0.6, y1=-5.0, y2=5.6)
    sc = 10.0 / 0.625; y0 = -5.0
    def F(x1, z1, x2, z2, c):
        m.box(-x2 * sc, y0 + (z1 - 0.452) * sc, -5.3, -x1 * sc, y0 + (z2 - 0.452) * sc, -5.0, c)
    F(-0.133, 0.52, 0.133, 0.592, TAGGY_BAR)
    for sd in (-1, 1):
        F(min(sd * 0.133, sd * 0.205), 0.592, max(sd * 0.133, sd * 0.205), 0.664, TAGGY_EYE)
    name_tag(m, -5.05, 2.0, 2.4)

@redesign("taggy_froggie_duo")
def _(m):
    taggy(m, -2.0, 4.0, 0.8, s=4.6)
    froggie(m, 2.0, 4.0, 0.4, s=0.62, tongue=True)
