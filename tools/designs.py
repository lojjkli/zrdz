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


# ======================================================================
# Froggie v2: the real vanilla frog model (FrogModel geometry + box UVs) wearing Froggie's own
# 48x48 frog texture from the animation, made girly with a bow, lashes and blush.
# ======================================================================
from mclib import Tex
import os as _os
FROG_TEX = _os.path.join(_os.path.dirname(__file__), "textures", "froggie_frog.png")
BOW, BOW_D, BOW_L, LASH, BLUSH = '#ff8fc2', '#e0609c', '#ffd0e6', '#2a1a12', '#ff9fb4'

def vanilla_frog(m, x0=0.0, y0=4.6, z0=0.0, s=0.8, girly=True, tongue=False, tex=FROG_TEX, bow=True):
    """Vanilla frog at scale s (head pixels per frog pixel). Java model space (Y down, feet at Y=24,
    face toward -Z, X mirrored) -> head pixels. y0 = where the feet touch."""
    def J(X, Y, Z, w, h, d, c, rot=None):
        m.box(x0 - (X + w) * s, y0 + (24 - Y - h) * s, z0 + Z * s, x0 - X * s, y0 + (24 - Y) * s, z0 + (Z + d) * s, c, rot=rot)
    T = lambda u, v, w, h, d, skip=(): Tex(tex, u, v, w, h, d, skip, "frog")
    J(-3.5, 20, -4, 7, 3, 9, T(3, 1, 7, 3, 9))            # body / lower jaw
    J(-3.5, 21, -4, 7, 0, 9, T(23, 22, 7, 0, 9))          # mouth plane (dark)
    J(-3.5, 18, -4, 7, 3, 9, T(0, 13, 7, 3, 9))           # head
    J(-3.5, 19, -4, 7, 0, 9, T(23, 13, 7, 0, 9))          # inner mouth plane
    big = 1.25 if girly else 1.0                          # cute Froggie: bigger, glossier eyes
    ew, eh, ed, ez = 3 * big, 2 * big, 3 * big, -3 - 0.2 * (big > 1)
    eyes = []
    for X0, uv in ((-3.5, (0, 0)), (0.5, (0, 5))):
        cx = X0 + 1.5; eyes.append(cx)
        J(cx - ew / 2, 18 - eh, ez, ew, eh, ed, T(uv[0], uv[1], 3, 2, 3))
    J(3, 21, -3.5, 2, 3, 3, T(0, 32, 2, 3, 3))            # left arm
    J(-5, 21, -3.5, 2, 3, 3, T(0, 38, 2, 3, 3))           # right arm
    J(2.5, 21, 2, 3, 3, 4, T(14, 25, 3, 3, 4))            # left leg
    J(-5.5, 21, 2, 3, 3, 4, T(0, 25, 3, 3, 4))            # right leg
    J(0, 23.98, -7.5, 8, 0, 8, T(18, 40, 8, 0, 8))        # webbed hands / feet (flat planes)
    J(-8, 23.98, -7.5, 8, 0, 8, T(2, 40, 8, 0, 8))
    J(1.5, 23.98, 0, 8, 0, 8, T(2, 32, 8, 0, 8))
    J(-9.5, 23.98, 0, 8, 0, 8, T(18, 32, 8, 0, 8))
    if tongue:   # little blep
        J(-1, 20.4, -5.4, 2, 0.4, 1.6, FTONGUE)
    if girly:
        top = 18 - eh
        for cx in eyes:
            o = -1 if cx < 0 else 1                                       # outward along Java X
            J(cx - 1.35, top + 0.35, ez - 0.08, 2.7, eh - 0.4, 0.08, '#1d1222')          # big glossy pupil
            J(cx - 1.1, top + 0.55, ez - 0.13, 0.75, 0.75, 0.05, '#ffffff')              # big sparkle (top-left)
            J(cx + 0.45, top + 1.55, ez - 0.13, 0.4, 0.4, 0.05, '#ffffff')               # small sparkle
            outer = cx + o * ew / 2
            for k in range(2):                                                          # two lashes on the outer corner
                lx = outer - o * (0.15 + 0.65 * k) - 0.15
                J(lx, top - 0.6 + 0.15 * k, ez - 0.05, 0.3, 0.6 - 0.15 * k, 0.3, LASH)
            J(min(outer, outer + o * 0.55), top - 0.05, ez - 0.05, 0.55, 0.35, 0.3, LASH)  # wing flick
        for X in (-3.45, 2.15):                                                           # rosy cheeks
            J(X, 18.35, -4.12, 1.3, 0.6, 0.12, BLUSH)
    if girly and bow:
        top = 18 - eh
        # little bow sitting on top of her left eye
        bx, bt, bz = eyes[1], top, ez + 1.1
        J(bx - 0.45, bt - 0.9, bz, 0.9, 0.9, 0.8, BOW_D)                                 # knot
        for sx in (-1, 1):
            x1 = bx + 0.45 if sx > 0 else bx - 1.95
            J(x1, bt - 1.35, bz + 0.05, 1.5, 1.4, 0.7, BOW)                               # loops
            J(x1 + 0.3, bt - 1.15, bz - 0.01, 0.7, 0.35, 0.06, BOW_L)                     # shine
    return J

@redesign("froggie_buddy")
def _(m):
    vanilla_frog(m, 0, 4.6, -0.2, s=0.8)

@design("froggie_hat", "Froggie Hat", "custom")
def _(m):
    vanilla_frog(m, 0, 4.6, -0.6, s=1.05, tongue=True)

@redesign("froglight_crown")
def _(m):
    band(m, 3.6, 4.4, FGD, 4.6)
    for (x, c, cl) in [(-3.0, '#f3d27a', '#fff2c2'), (0.0, '#e9c8e8', '#fff0ff'), (3.0, '#b8e6a6', '#effff0')]:
        rbox(m, x - 1.1, 4.4, -5.1, x + 1.1, 6.6, -2.9, c, r=0.3)
        m.box(x - 0.6, 4.9, -5.15, x + 0.6, 6.1, -5.1, cl)
    GLOW.update({'#fff2c2', '#fff0ff', '#effff0'})
    vanilla_frog(m, 0, 4.6, 1.4, s=0.5)

@redesign("taggy_froggie_duo")
def _(m):
    taggy(m, -2.2, 4.0, 0.8, s=4.6)
    vanilla_frog(m, 2.1, 4.6, 0.0, s=0.5)

@redesign("taggy_buddy")
def _(m):
    taggy(m, 0, 4.0, -1.8, s=5.8)          # perched on the front edge, feet over the brow
    name_tag(m, -2.2, 6.6, -0.6)

@design("taggy_rides_froggie", "Taggy Rides Froggie", "custom")
def _(m):
    vanilla_frog(m, 0, 4.6, 0.0, s=0.75, girly=True)
    taggy(m, 0, 4.6 + 6.0 * 0.75, 2.6, s=4.4)

@design("taggy_peek", "Taggy Peekaboo", "custom")
def _(m):
    # Taggy hanging over the front of the head: head + hands gripping the brow
    s = 5.8
    hx1, hx2 = -0.312 * s, 0.312 * s
    m.box(hx1, 2.2, -4.9 - 0.5 * s * 0.56, hx2, 2.2 + 0.5 * s, -4.9, TAGGY_P)          # head peeking over
    m.box(-0.133 * s, 2.2 + 0.068 * s, -5.0 - 0.28 * s, 0.133 * s, 2.2 + 0.14 * s, -4.95 - 0.28 * s, TAGGY_BAR)
    for sd in (-1, 1):
        m.box(min(sd * 0.133 * s, sd * 0.205 * s), 2.2 + 0.14 * s, -5.0 - 0.28 * s,
              max(sd * 0.133 * s, sd * 0.205 * s), 2.2 + 0.212 * s, -4.95 - 0.28 * s, TAGGY_EYE)
        m.box(sd * 2.6 - 0.45, 3.4, -5.4, sd * 2.6 + 0.45, 4.9, -3.2, TAGGY_P)            # hands over the edge
    m.box(-1.4, 4.0, -4.9, 1.4, 4.9, -2.6, TAGGY_P)                                     # body lying on top
    for sd in (-1, 1):
        m.box(sd * 0.9 - 0.6, 4.0, -2.6, sd * 0.9 + 0.6, 4.8, 0.2, TAGGY_P)             # legs stretched back

@design("taggy_headphones", "Taggy Headphones", "custom")
def _(m):
    m.box(-4.9, 4.6, -0.45, 4.9, 5.3, 0.45, '#2b2340')                                     # band over the top
    m.box(-4.2, 4.5, -0.5, 4.2, 4.65, 0.5, '#4b3a6a')                                      # cushion
    for sd in (-1, 1):
        m.box(min(sd * 4.6, sd * 5.2), 1.4, -0.45, max(sd * 4.6, sd * 5.2), 5.3, 0.45, '#2b2340')   # arms down the sides
        rbox(m, min(sd * 4.6, sd * 6.4), -2.4, -2.1, max(sd * 4.6, sd * 6.4), 1.8, 2.1, TAGGY_P, r=0.4)  # Taggy-head cups
        f = sd * 6.4; o = sd * 0.06
        m.box(min(f, f + o), -0.7, -0.9, max(f, f + o), -0.3, 0.9, TAGGY_BAR)                  # glowing smile
        for e in (-1, 1):
            m.box(min(f, f + o), -0.3, min(e * 0.9, e * 1.3), max(f, f + o), 0.1, max(e * 0.9, e * 1.3), TAGGY_EYE)

# ======================================================================
# TRENDY 2025-26 batch (6-7, Italian brainrot, matcha, Dubai chocolate, clanker, aura)
# ======================================================================
SIX, SEVEN = '#ff5ab4', '#4fe3ff'
GLOW.update({SIX, SEVEN, '#ffe14f'})
DIGITS = {'6': ["###", "#..", "###", "#.#", "###"], '7': ["###", "..#", "..#", ".#.", ".#."]}

def digits(m, text, cx, top, z, cell, cols, t=0.6, shadow='#2a1640'):
    n = len(text) * 4 - 1
    for i, ch in enumerate(text):                       # each digit its own colour
        sub = [("." * (i * 4)) + DIGITS[ch][r] + ("." * (n - i * 4 - 3)) for r in range(5)]
        relief(m, sub, z, {'#': (cols[i], t)}, cell=cell, top=top, cx=cx)
        relief(m, sub, z + 0.5, {'#': (shadow, 0.5)}, cell=cell, top=top - 0.25, cx=cx - 0.25)

@design("six_seven", "6-7", "trend")
def _(m):
    digits(m, "67", 0, 10.2, 0.0, 0.9, (SIX, SEVEN))
    for x, y in ((-4.6, 9.4), (4.4, 6.0), (3.6, 10.6)):
        star(m, x, y, -0.3, 0.45, '#ffe14f')

@design("six_seven_hands", "6-7 Hands", "trend")
def _(m):
    SKIN, CUFF = '#e8b58e', '#2b2b33'
    for sd, y, d, col in ((1, 5.2, "6", SIX), (-1, 6.6, "7", SEVEN)):   # +x is the wearer's right = viewer's left
        x = sd * 6.0
        m.box(x - 0.9, y - 2.6, -0.9, x + 0.9, y - 0.6, 0.9, CUFF)                       # sleeve
        rbox(m, x - 1.4, y - 0.6, -1.5, x + 1.4, y, 1.5, SKIN, r=0.3)                    # palm up
        for f in (-1.05, -0.35, 0.35, 1.05):
            m.box(x + f - 0.28, y - 0.4, -2.4, x + f + 0.28, y + 0.2, -1.5, SKIN)        # fingers
        m.box(x - sd * 1.4 - 0.3 * sd, y - 0.5, -0.6, x - sd * 1.4, y + 0.1, 0.6, SKIN)  # thumb
        digits(m, d, x, y + 4.2, 0.0, 0.6, (col,), t=0.45)

@design("tralalero", "Tralalero Shark", "trend")
def _(m):
    SH, SHD, BELLY, SHOE, SOLE = '#6f8fb2', '#4f6b8c', '#e9eef2', '#2f6fe0', '#ffffff'
    y0 = 4.6
    for x, z in ((-1.3, -1.6), (1.3, -1.6), (0, 2.2)):                                  # 3 legs in blue sneakers
        m.box(x - 0.7, y0, z - 1.3, x + 0.7, y0 + 0.4, z + 0.9, SOLE)
        m.box(x - 0.7, y0 + 0.4, z - 1.2, x + 0.7, y0 + 1.1, z + 0.9, SHOE)
        m.box(x - 0.72, y0 + 0.55, z - 0.6, x + 0.72, y0 + 0.75, z + 0.4, SOLE)          # side stripe
        m.box(x - 0.35, y0 + 1.1, z - 0.3, x + 0.35, y0 + 1.9, z + 0.3, BELLY)           # ankles
    yb = y0 + 1.9
    rbox(m, -1.9, yb, -3.6, 1.9, yb + 2.6, 3.0, SH, r=0.6)                              # body
    m.box(-1.6, yb - 0.05, -3.4, 1.6, yb + 0.9, 2.6, BELLY)                             # white belly
    rbox(m, -1.4, yb + 0.2, -5.2, 1.4, yb + 2.2, -3.6, SH, r=0.4)                       # snout
    m.box(-1.2, yb + 0.15, -5.25, 1.2, yb + 0.85, -3.6, BELLY)
    for x in (-0.8, -0.27, 0.27, 0.8):
        m.box(x - 0.18, yb + 0.85, -5.3, x + 0.18, yb + 1.15, -5.2, '#ffffff')          # teeth
    m.box(-1.1, yb + 0.85, -5.22, 1.1, yb + 0.95, -4.0, '#3a1d22')                      # mouth line
    for sd in (-1, 1):
        m.box(min(sd * 1.9, sd * 2.0), yb + 1.5, -3.2, max(sd * 1.9, sd * 2.0), yb + 2.0, -2.6, '#101418')  # eyes
        m.box(min(sd * 1.6, sd * 3.2), yb + 0.6, -1.2, max(sd * 1.6, sd * 3.2), yb + 0.9, 0.4, SHD)  # side fins
    steps(m, 0, 0.4, yb + 2.6, [2.2, 1.6, 1.0, 0.5], SHD, depth=None, h=0.8, dz=0.5)    # dorsal fin
    m.box(-0.3, yb + 0.8, 3.0, 0.3, yb + 2.0, 4.2, SH)                                  # tail stock
    m.box(-0.25, yb + 0.2, 4.0, 0.25, yb + 3.4, 4.9, SHD)                               # tail fin

@design("tung_tung", "Tung Tung Buddy", "trend")
def _(m):
    WOOD, WOOD_D, RING, BAT = '#c79a62', '#a57a45', '#e2c08c', '#8a5a2b'
    y0 = 4.6
    for sd in (-1, 1):
        m.box(sd * 0.7 - 0.35, y0, -0.35, sd * 0.7 + 0.35, y0 + 1.6, 0.35, WOOD_D)      # legs
    rbox(m, -1.4, y0 + 1.6, -1.4, 1.4, y0 + 7.0, 1.4, WOOD, r=0.45, top=False)          # log body
    m.box(-1.0, y0 + 7.0, -1.0, 1.0, y0 + 7.1, 1.0, RING)                               # cut top
    m.box(-0.5, y0 + 7.0, -0.5, 0.5, y0 + 7.15, 0.5, WOOD_D)
    for y in (y0 + 2.4, y0 + 3.6, y0 + 4.2):
        m.box(-1.45, y, -1.0, -1.4, y + 0.15, 0.6, WOOD_D)                              # bark grain
        m.box(1.4, y + 0.3, -0.6, 1.45, y + 0.45, 1.0, WOOD_D)
    for sd in (-1, 1):                                                                  # big eyes + brows
        m.box(sd * 0.65 - 0.5, y0 + 5.0, -1.55, sd * 0.65 + 0.5, y0 + 6.0, -1.4, '#ffffff')
        m.box(sd * 0.65 - 0.2, y0 + 5.2, -1.6, sd * 0.65 + 0.2, y0 + 5.6, -1.55, '#111111')
        m.box(sd * 0.65 - 0.55, y0 + 6.2, -1.55, sd * 0.65 + 0.55, y0 + 6.45, -1.4, '#3a2410')
    m.box(-0.5, y0 + 4.2, -1.55, 0.5, y0 + 4.5, -1.4, '#3a2410')                        # mouth
    m.box(-1.9, y0 + 3.4, -0.3, -1.4, y0 + 4.0, 0.3, WOOD_D)                            # left arm
    m.box(1.4, y0 + 3.4, -0.3, 2.3, y0 + 4.0, 0.3, WOOD_D)                              # right arm out
    m.box(2.0, y0 + 2.4, -0.35, 2.6, y0 + 7.2, 0.35, BAT, rot=('z', -22.5, (2.3, y0 + 3.7, 0)))  # baseball bat
    m.box(1.85, y0 + 5.6, -0.5, 2.75, y0 + 7.6, 0.5, BAT, rot=('z', -22.5, (2.3, y0 + 3.7, 0)))

@design("ballerina_cappuccina", "Ballerina Cappuccina", "trend")
def _(m):
    CUP, CUPD, COF, FOAM, TUTU, TUTU_L = '#f4efe8', '#d9d1c6', '#6b3f22', '#e8cfa8', '#ff9cc8', '#ffd1e6'
    y0 = 4.6
    for sd in (-1, 1):
        m.box(sd * 0.6 - 0.3, y0, -0.3, sd * 0.6 + 0.3, y0 + 1.4, 0.3, '#f6dccb')       # legs
        m.box(sd * 0.6 - 0.35, y0, -0.6, sd * 0.6 + 0.35, y0 + 0.35, 0.35, TUTU)        # pointe shoes
    for i, (r, c) in enumerate(((3.4, TUTU), (2.9, TUTU_L), (2.5, TUTU))):              # layered tutu
        rbox(m, -r, y0 + 1.3 + i * 0.3, -r, r, y0 + 1.6 + i * 0.3, r, c, r=r / 3, top=False)
    rbox(m, -1.9, y0 + 1.4, -1.9, 1.9, y0 + 5.0, 1.9, CUP, r=0.6, top=False)            # cup head
    m.box(-1.95, y0 + 1.4, -1.95, 1.95, y0 + 1.9, 1.95, CUPD)
    rbox(m, -1.6, y0 + 4.8, -1.6, 1.6, y0 + 5.1, 1.6, COF, r=0.5, top=False)            # coffee
    heart(m, 0, y0 + 5.1, 0.0, 0.25, FOAM, t=0.05)
    m.box(-0.6, y0 + 5.12, -0.4, 0.6, y0 + 5.17, 0.4, FOAM)                             # latte art
    rbox(m, 1.9, y0 + 2.4, -0.6, 2.9, y0 + 4.0, 0.6, CUP, r=0.3)                        # mug handle
    m.box(2.0, y0 + 2.8, -0.2, 2.5, y0 + 3.6, 0.2, CUPD)
    for sd in (-1, 1):                                                                  # face
        m.box(sd * 0.7 - 0.25, y0 + 3.4, -1.95, sd * 0.7 + 0.25, y0 + 3.9, -1.9, '#1d1b22')
        m.box(sd * 1.1 - 0.3, y0 + 2.9, -1.95, sd * 1.1 + 0.3, y0 + 3.2, -1.9, '#ffb3c6')
    m.box(-0.35, y0 + 2.9, -1.95, 0.35, y0 + 3.1, -1.9, '#c0475e')
    m.box(-2.9, y0 + 4.6, -0.25, -1.8, y0 + 5.0, 0.25, '#f6dccb', rot=('z', 22.5, (-1.9, y0 + 4.6, 0)))   # arms up
    m.box(-2.9, y0 + 5.0, -0.25, -2.5, y0 + 6.4, 0.25, '#f6dccb', rot=('z', 22.5, (-1.9, y0 + 4.6, 0)))

@design("bombardiro", "Bombardiro Croc", "trend")
def _(m):
    BODY, BODYD, CROC, CROCD, GLASS = '#7c8a6a', '#5d6a4e', '#4f8a3a', '#3a6a2a', '#9fd6ff99'
    y = 7.2
    rbox(m, -1.3, y, -2.4, 1.3, y + 2.2, 4.0, BODY, r=0.5)                              # fuselage
    m.box(-0.8, y + 2.2, -1.6, 0.8, y + 2.8, 0.6, GLASS)                                # cockpit
    rbox(m, -1.2, y + 0.1, -5.6, 1.2, y + 1.4, -2.4, CROC, r=0.3)                       # croc snout (lower)
    rbox(m, -1.3, y + 1.0, -5.4, 1.3, y + 2.3, -2.2, CROC, r=0.3)                       # croc head top
    for x in (-1.0, -0.4, 0.4, 1.0):
        m.box(x - 0.15, y + 0.9, -5.5, x + 0.15, y + 1.15, -5.3, '#ffffff')             # teeth
    for sd in (-1, 1):
        m.box(sd * 0.7 - 0.3, y + 2.3, -3.6, sd * 0.7 + 0.3, y + 2.8, -3.0, CROCD)     # eye bumps
        m.box(sd * 0.7 - 0.2, y + 2.45, -3.65, sd * 0.7 + 0.2, y + 2.7, -3.6, '#ffe14f')
        m.box(min(sd * 1.3, sd * 6.2), y + 0.9, -0.6, max(sd * 1.3, sd * 6.2), y + 1.3, 1.6, BODYD)   # wings
        m.box(min(sd * 5.6, sd * 6.2), y + 0.8, -0.4, max(sd * 5.6, sd * 6.2), y + 1.4, 1.4, '#c8312d')  # wing tips
        m.box(sd * 2.8 - 0.5, y - 0.2, -0.3, sd * 2.8 + 0.5, y + 0.9, 0.9, '#555a50')   # engines
        m.box(min(sd * 0.4, sd * 2.4), y + 1.4, 3.4, max(sd * 0.4, sd * 2.4), y + 1.7, 4.4, BODYD)  # tailplane
    m.box(-0.2, y + 2.2, 3.0, 0.2, y + 3.8, 4.2, BODYD)                                 # tail fin
    m.box(-0.4, y - 0.6, 0.6, 0.4, y, 1.8, '#3a3d36')                                   # little bomb
    for sd in (-1, 1):
        m.box(sd * 0.3 - 0.15, 4.6, -0.15, sd * 0.3 + 0.15, y, 0.15, '#3a3d36')         # landing struts

@design("matcha_latte", "Matcha Latte", "trend")
def _(m):
    CUPA, MATCHA, MILK, LID, STRAW = '#e8f4ff55', '#7fb84a', '#f2f0e4', '#f4fbff88', '#2fae6a'
    y0, k = 4.6, 1.3
    rbox(m, -1.4 * k, y0, -1.4 * k, 1.4 * k, y0 + 1.6 * k, 1.4 * k, MATCHA, r=0.5, top=False)   # green bottom
    rbox(m, -1.5 * k, y0 + 1.6 * k, -1.5 * k, 1.5 * k, y0 + 2.2 * k, 1.5 * k, '#b9d98a', r=0.5, top=False)
    rbox(m, -1.6 * k, y0 + 2.2 * k, -1.6 * k, 1.6 * k, y0 + 3.6 * k, 1.6 * k, MILK, r=0.55, top=False)
    for zz in (-0.7, 0.6):
        m.box(-0.9, y0 + 2.6 * k, zz - 0.4, -0.1, y0 + 3.3 * k, zz + 0.4, '#dff5ff')      # ice cubes
    rbox(m, -1.8 * k, y0 - 0.05, -1.8 * k, 1.8 * k, y0 + 4.0 * k, 1.8 * k, CUPA, r=0.6, top=False)  # clear cup
    rbox(m, -1.9 * k, y0 + 4.0 * k, -1.9 * k, 1.9 * k, y0 + 4.3 * k, 1.9 * k, LID, r=0.6, top=False)
    rbox(m, -1.3 * k, y0 + 4.3 * k, -1.3 * k, 1.3 * k, y0 + 4.9 * k, 1.3 * k, LID, r=0.5)
    m.box(0.3, y0 + 1.0, 0.0, 0.8, y0 + 9.2, 0.5, STRAW, rot=('z', -22.5, (0.5, y0 + 5.5, 0.2)))

@design("clanker_helmet", "Clanker Helmet", "trend")
def _(m):
    MET, MET_D, VIS, EYE = '#9ea2ad', '#6f7682', '#1a1d24', '#ff4a2a'
    shell(m, 5.0, MET, r=0.7)
    m.box(-4.0, 0.4, -5.3, 4.0, 2.8, -5.0, VIS)                                         # visor
    for x in (-2.0, 2.0):
        m.box(x - 0.9, 1.1, -5.4, x + 0.9, 2.1, -5.3, EYE)                              # glowing eyes
    for x in (-2.4, -1.2, 0.0, 1.2, 2.4):
        m.box(x - 0.25, -3.4, -5.25, x + 0.25, -1.6, -5.0, MET_D)                       # mouth grille
    for x, y in ((-4.2, 4.2), (4.2, 4.2), (-4.2, -4.2), (4.2, -4.2)):
        m.box(x - 0.3, y - 0.3, -5.25, x + 0.3, y + 0.3, -5.0, '#c9ced8')               # bolts
    for sd in (-1, 1):
        rbox(m, min(sd * 5.0, sd * 5.8), -1.6, -1.6, max(sd * 5.0, sd * 5.8), 1.6, 1.6, MET_D, r=0.4)  # ear bolts
    m.box(-0.2, 5.0, -0.2, 0.2, 7.6, 0.2, MET_D)                                        # antenna
    rbox(m, -0.5, 7.6, -0.5, 0.5, 8.6, 0.5, EYE, r=0.2)

@design("dubai_chocolate", "Dubai Chocolate", "trend")
def _(m):
    CH, CHL, PIST, KUN = '#5a3420', '#74472c', '#8fbf4f', '#d8b25a'
    y0 = 4.6
    m.box(-3.6, y0, -1.9, 0.3, y0 + 1.0, 1.9, CH)                                       # bar half on the head
    for x in (-3.0, -1.5):
        for z in (-0.95, 0.95):
            rbox(m, x - 0.6, y0 + 1.0, z - 0.75, x + 0.6, y0 + 1.3, z + 0.75, CHL, r=0.2)
    m.box(0.3, y0 + 0.2, -1.8, 0.35, y0 + 0.75, 1.8, PIST)                              # green filling at the snap
    for z in (-1.2, -0.2, 0.9):
        m.box(0.32, y0 + 0.3, z - 0.25, 0.4, y0 + 0.6, z + 0.25, KUN)                   # crunchy kunafa strands
    r = ('z', 22.5, (0.8, y0, 0))                                                       # other half leaning on it
    m.box(0.8, y0, -1.9, 4.6, y0 + 1.0, 1.9, CH, rot=r)
    m.box(0.75, y0 + 0.2, -1.8, 0.8, y0 + 0.75, 1.8, PIST, rot=r)
    for x in (2.0, 3.6):
        for z in (-0.95, 0.95):
            rbox(m, x - 0.6, y0 + 1.0, z - 0.75, x + 0.6, y0 + 1.3, z + 0.75, CHL, r=0.2, rot=r)

@design("aura_farmer", "Aura Farmer", "trend")
def _(m):
    A1, A2, A3 = '#c45cffcc', '#9be7ffcc', '#ff7ad1cc'
    GLOW.update({A1, A2, A3})
    import math as _m
    for i in range(12):
        a = i * _m.pi / 6
        x, z = 5.4 * _m.cos(a), 5.4 * _m.sin(a)
        if z < -4.0 and abs(x) < 3.0:
            continue                                                                    # keep the face clear
        c = (A1, A2, A3)[i % 3]
        h = (6.0, 8.0, 7.0, 9.0)[i % 4]
        steps(m, x, z, -3.5, [1.4, 1.2, 1.0, 0.8, 0.6, 0.4], c, h=h / 6, smooth=1)       # flames of aura rising
    for x, y, z in ((-2.6, 7.6, -2.0), (2.8, 8.8, 1.4), (0.4, 9.8, -0.6), (-3.2, 9.0, 2.6)):
        star(m, x, y, z, 0.5, '#9be7ff')

@design("googly_eyes", "Googly Eyes", "goofy")
def _(m):
    for sd, (px, py) in ((-1, (-0.7, -0.8)), (1, (0.8, 0.6))):
        cx = sd * 2.2
        rbox(m, cx - 1.9, 0.0, -5.6, cx + 1.9, 3.8, -4.6, '#ffffff', r=0.6)            # big white eye
        rbox(m, cx + px - 0.8, 1.9 + py - 0.8, -5.75, cx + px + 0.8, 1.9 + py + 0.8, -5.55, '#111111', r=0.3)

@design("plunger", "Plunger", "goofy")
def _(m):
    dome(m, 4.0, [(2.6, 0.8), (2.2, 0.6), (1.6, 0.5), (0.9, 0.4)], '#c8312d')
    m.box(-0.35, 6.2, -0.35, 0.35, 12.0, 0.35, '#b07a40')
    m.box(-0.45, 11.8, -0.45, 0.45, 12.2, 0.45, '#8a5a2b')

@design("arrow_head", "Arrow Through Head", "goofy")
def _(m):
    SH, HEAD, FL = '#8a6a3a', '#c9ced8', '#f4f2ee'
    m.box(-8.4, 1.6, -0.3, -4.6, 2.2, 0.3, SH); m.box(4.6, 1.6, -0.3, 7.0, 2.2, 0.3, SH)   # shaft out both sides
    for i, w in enumerate((1.8, 1.3, 0.8, 0.35)):                                       # arrowhead on the right
        m.box(7.0 + i * 0.45, 1.9 - w / 2, -0.25, 7.45 + i * 0.45, 1.9 + w / 2, 0.25, HEAD)
    for i, w in enumerate((0.6, 0.9, 1.2, 1.4)):                                        # fletching on the left
        m.box(-8.4 + i * 0.5, 2.2, -0.12, -7.9 + i * 0.5, 2.2 + w, 0.12, FL)
        m.box(-8.4 + i * 0.5, 1.6 - w, -0.12, -7.9 + i * 0.5, 1.6, 0.12, FL)

@design("banana_peel", "Banana Peel", "goofy")
def _(m):
    Y, YD, IN, TIP = '#f7dc3c', '#d9b52a', '#fff4c2', '#5a3a1e'
    rbox(m, -1.4, 4.0, -1.4, 1.4, 6.2, 1.4, Y, r=0.5)                                   # stalk end standing up
    m.box(-0.5, 6.2, -0.5, 0.5, 6.9, 0.5, YD); m.box(-0.35, 6.9, -0.35, 0.35, 7.2, 0.35, TIP)
    for ang in range(4):                                                                # 4 peels draped over the sides
        for i, w in enumerate((2.6, 2.4, 2.0, 1.6, 1.1)):
            if i < 2:   # lying on top
                a1, a2 = 1.2 + i * 1.7, 1.2 + (i + 1) * 1.7
                box = (-w / 2, 4.0, -a2, w / 2, 4.55, -a1)
            else:       # hanging down the side
                y2 = 4.55 - (i - 2) * 1.6
                box = (-w / 2, y2 - 1.6, -4.85, w / 2, y2, -4.6)
            x1, y1, z1, x2, y2_, z2 = box
            # rotate the north flap to each side
            pts = {0: (x1, z1, x2, z2), 1: (-z2, x1, -z1, x2), 2: (x1, -z2, x2, -z1), 3: (z1, x1, z2, x2)}[ang]
            m.box(pts[0], y1, pts[1], pts[2], y2_, pts[3], Y if i < 4 else TIP)
        m.box(*({0: (-0.9, 4.55, -4.2, 0.9, 4.6, -1.4), 1: (1.4, 4.55, -0.9, 4.2, 4.6, 0.9),
                 2: (-0.9, 4.55, 1.4, 0.9, 4.6, 4.2), 3: (-4.2, 4.55, -0.9, -1.4, 4.6, 0.9)}[ang]), IN)
    for x, y in ((-0.6, 2.4), (0.7, 1.2)):
        m.box(x - 0.25, y - 0.25, -4.9, x + 0.25, y + 0.25, -4.85, YD)                  # brown spots

@design("dizzy_stars", "Dizzy Stars", "goofy")
def _(m):
    import math as _m
    for i in range(6):
        a = i * _m.pi / 3 + 0.3
        x, z = 5.8 * _m.cos(a), 5.8 * _m.sin(a)
        y = 6.6 + 0.8 * _m.sin(a * 2)
        if i % 2 == 0:
            star(m, x, y, z, 0.9, '#ffe14f')
        else:   # little yellow birdie
            rbox(m, x - 0.9, y - 0.8, z - 0.8, x + 0.9, y + 0.8, z + 0.8, '#ffd34a', r=0.3)
            m.box(x - 0.35, y - 0.2, z - 1.3, x + 0.35, y + 0.25, z - 0.8, ORANGE)
            for e in (-1, 1):
                m.box(x + e * 0.45 - 0.18, y + 0.15, z - 0.85, x + e * 0.45 + 0.18, y + 0.5, z - 0.8, '#111111')
            m.box(x - 1.3, y - 0.1, z - 0.3, x + 1.3, y + 0.2, z + 0.4, '#f2bb2a')       # wings
    GLOW.add('#ffe14f')

@design("cheese_hat", "Cheese Wedge Hat", "goofy")
def _(m):
    C, CD, RIND = '#ffcf3a', '#e0a91e', '#f3b62a'
    n = 12
    for i in range(n):                                                                  # wedge: thick at the back
        z1 = -4.4 + i * 8.8 / n
        m.box(-4.4, 4.0, z1, 4.4, 4.5 + (i + 1) * 0.36, 4.4, C)
    m.box(-4.45, 4.0, 4.4, 4.45, 8.85, 4.5, RIND)
    for x, y in ((-2.4, 6.0), (1.6, 7.4), (2.8, 5.2), (-0.6, 4.8)):
        m.box(x - 0.6, y - 0.6, 4.5, x + 0.6, y + 0.6, 4.56, CD)                        # holes on the back
    for x, z in ((-2.2, -2.9), (2.2, -0.6), (-0.8, 1.7), (2.6, 2.6)):                  # holes on the slope
        i = int((z + 4.4) / (8.8 / n)); yy = 4.5 + (i + 1) * 0.36
        m.box(x - 0.6, yy, z - 0.3, x + 0.6, yy + 0.04, z + 0.3, CD)
    for sd in (-1, 1):
        for z, y in ((-1.0, 4.8), (2.2, 6.4), (0.6, 5.6)):
            x = sd * 4.4
            m.box(min(x, x + sd * 0.05), y - 0.5, z - 0.5, max(x, x + sd * 0.05), y + 0.5, z + 0.5, CD)

@design("frying_pan", "Frying Pan + Egg", "goofy")
def _(m):
    PAN, PAN_D, WH, YO = '#3a3d44', '#24262b', '#fafaf4', '#ffb71f'
    rbox(m, -4.2, 4.0, -4.2, 4.2, 4.5, 4.2, PAN_D, r=1.2, top=False)
    ring(m, 4.5, 4.4, PAN, t=0.5, h=0.7)
    m.box(4.2, 4.6, -0.5, 9.2, 5.1, 0.5, '#5a3a24')                                     # handle
    rbox(m, -2.6, 4.5, -2.4, 2.2, 4.8, 2.0, WH, r=0.9, top=False)                       # fried egg
    rbox(m, -0.9, 4.8, -0.9, 0.7, 5.3, 0.7, YO, r=0.3)

@design("toaster_hat", "Toaster Hat", "goofy")
def _(m):
    MET, MET_D, TOAST, CRUST = '#c9ced8', '#8c8f99', '#e9b46a', '#a8662c'
    rbox(m, -3.4, 4.0, -2.2, 3.4, 7.4, 2.2, MET, r=0.7)
    for x in (-1.5, 1.5):
        m.box(x - 0.9, 7.3, -1.5, x + 0.9, 7.42, 1.5, '#1d1b22')                        # slots
    for x, y in ((-1.5, 9.0), (1.5, 8.2)):                                              # toast popping up
        m.box(x - 0.7, 6.0, -1.3, x + 0.7, y, 1.3, CRUST)
        m.box(x - 0.72, 6.2, -1.1, x + 0.72, y - 0.2, 1.1, TOAST)
    m.box(3.4, 5.6, -0.4, 3.9, 6.4, 0.4, MET_D)                                         # lever
    m.box(-2.8, 4.6, -2.25, 2.8, 5.0, -2.2, MET_D)

@design("big_brain", "Big Brain", "goofy")
def _(m):
    BR, BRD, BRL = '#ff9db5', '#e06a8a', '#ffc4d3'
    dome(m, 4.0, [(4.6, 1.0)], BR)
    import random as _r
    rnd = _r.Random(7)
    for sd in (-1, 1):                                                                  # two lumpy hemispheres
        for ix in range(2):
            for iz in range(3):
                x1 = sd * (0.35 + ix * 2.1); x2 = sd * (0.35 + ix * 2.1 + 2.1)
                z1 = -4.3 + iz * 2.9
                h = 7.4 - ix * 0.7 - abs(iz - 1) * 0.5 + rnd.uniform(-0.15, 0.15)
                rbox(m, min(x1, x2), 5.0, z1, max(x1, x2), h, z1 + 2.7, (BR, BRL)[(ix + iz) % 2], r=0.8)
                m.box(min(x1, x2) + 0.5, h - 0.05, z1 + 1.2, max(x1, x2) - 0.5, h + 0.05, z1 + 1.5, BRD)   # squiggle
    m.box(-0.35, 5.0, -4.3, 0.35, 7.1, 4.3, BRD)                                        # middle split

@design("duck_floatie", "Duck Floatie", "goofy")
def _(m):
    Y, YL, OR = '#ffd84a', '#fff2a8', '#ff8a2a'
    for (x1, z1, x2, z2) in ((-6.2, -6.2, 6.2, -4.6), (-6.2, 4.6, 6.2, 6.2), (-6.2, -4.6, -4.6, 4.6), (4.6, -4.6, 6.2, 4.6)):
        rbox(m, x1 - (0.4 if x1 < -6 else 0), 0.8, z1 - (0.4 if z1 < -6 else 0), x2 + (0.4 if x2 > 6 else 0), 3.0, z2 + (0.4 if z2 > 6 else 0), Y, r=0.8)
    ring(m, 2.8, 6.0, YL, t=0.6, h=0.15)
    rbox(m, -1.4, 2.8, -6.8, 1.4, 5.6, -4.4, Y, r=0.6)                                  # duck head at the front
    m.box(-1.0, 3.4, -7.8, 1.0, 4.1, -6.8, OR)                                          # beak
    for sd in (-1, 1):
        m.box(sd * 0.8 - 0.3, 4.5, -6.85, sd * 0.8 + 0.3, 5.0, -6.8, '#111111')
    steps(m, 0, 5.4, 1.6, [2.2, 1.4, 0.6], Y, h=0.8)                                    # little tail at the back


# ======================================================================
# Requested: Create mod style engineer's goggles (brass, round lenses, leather strap, a little cog)
# ======================================================================
@design("engineer_goggles", "Engineer's Goggles", "cool")
def _(m):
    BRASS, BRASS_D, BRASS_L, LEATHER, LEATHER_D, LENS = '#e0a833', '#b8861c', '#f6d27a', '#6b4326', '#4a2e1a', '#bfeff2aa'
    band(m, -1.5, 0.3, LEATHER, 4.75)                                                   # leather strap
    m.box(-4.8, -1.2, 4.75, 4.8, 0.0, 4.85, LEATHER_D)
    for sd in (-1, 1):
        cx = sd * 2.05
        rbox(m, cx - 1.75, -2.25, -5.9, cx + 1.75, 1.25, -4.6, BRASS_D, r=0.6)         # lens housing
        rbox(m, cx - 1.6, -2.1, -6.3, cx + 1.6, 1.1, -5.9, BRASS, r=0.55)              # front rim
        m.box(cx - 1.05, -1.55, -6.35, cx + 1.05, 0.55, -6.3, LENS)                     # glass
        m.box(cx - 0.75, 0.05, -6.37, cx - 0.25, 0.4, -6.35, '#ffffffcc')               # glint
        for rx, ry in ((-1.25, 0.75), (1.25, 0.75), (-1.25, -1.75), (1.25, -1.75)):
            m.box(cx + rx - 0.15, ry - 0.15, -6.4, cx + rx + 0.15, ry + 0.15, -6.3, BRASS_L)   # rivets
        m.box(min(sd * 3.8, sd * 4.85), -1.2, -4.9, max(sd * 3.8, sd * 4.85), 0.0, -4.5, BRASS_D)   # strap clips
    m.box(-0.3, -0.6, -5.6, 0.3, 0.2, -4.6, BRASS)                                      # nose bridge
    # little Create-style cog on the side of the strap
    x = 4.9
    rbox(m, x, -2.0, -1.4, x + 0.5, 0.8, 1.4, BRASS, r=0.0)
    for (y1, y2, z1, z2) in ((-2.5, 1.3, -0.4, 0.4), (-1.0, -0.2, -1.9, 1.9)):
        m.box(x + 0.05, y1, z1, x + 0.45, y2, z2, BRASS_D)
    m.box(x + 0.5, -0.9, -0.3, x + 0.6, -0.3, 0.3, LEATHER_D)


# ======================================================================
# BIG BATCH 2: Froggie outfits, cute buddies, Minecraft cool, more brainrot, goofy food + gags
# ======================================================================
def fbox(J, x1, y_top, z1, w, h, d, c):
    """Frog-space box helper (Java units: y_top is the top edge, h grows downward)."""
    J(x1, y_top, z1, w, h, d, c)

@design("froggie_strawberry", "Froggie Strawberry Hat", "custom")
def _(m):
    J = vanilla_frog(m, 0, 4.6, -0.2, s=0.8, bow=False)
    R, RD, SEED, LV, ST = '#e8343f', '#c2242f', '#ffe27a', '#4cae3a', '#3a7a2c'
    cz, base = -1.2, 15.5                                       # perched on top of her eyes
    for hw, yt, yb in ((2.4, base - 1.4, base), (2.0, base - 2.4, base - 1.4), (1.3, base - 3.1, base - 2.4)):
        J(-hw, yt, cz - hw, 2 * hw, yb - yt, 2 * hw, R)
    J(-2.45, base - 0.4, cz - 2.45, 4.9, 0.4, 4.9, RD)
    for x, y in ((-1.5, base - 1.1), (0.1, base - 0.8), (1.3, base - 1.2), (-0.6, base - 1.9), (0.8, base - 2.1)):
        J(x, y, cz - 2.46, 0.4, 0.4, 0.06, SEED)
    for x, z in ((-2.46, cz - 0.8), (-2.46, cz + 0.9), (2.4, cz - 0.3), (2.4, cz + 1.1)):
        J(x, base - 1.2, z, 0.06, 0.4, 0.4, SEED)
    J(-1.8, base - 3.3, cz - 0.45, 3.6, 0.2, 0.9, LV)                                 # leaf star on top
    J(-0.45, base - 3.3, cz - 1.8, 0.9, 0.2, 3.6, LV)
    J(-0.2, base - 4.2, cz - 0.2, 0.4, 0.9, 0.4, ST)                                  # stem

@design("froggie_mushroom", "Froggie Mushroom Cap", "custom")
def _(m):
    J = vanilla_frog(m, 0, 4.6, -0.2, s=0.8, bow=False)
    R, RD, GILL, SP = '#d8322e', '#b0241f', '#efe0c6', '#fbf7ef'
    cz, base = -1.0, 15.6
    J(-0.6, base - 0.3, cz - 0.6, 1.2, 0.4, 1.2, GILL)                                # little stem
    J(-3.2, base - 0.8, cz - 3.2, 6.4, 0.5, 6.4, GILL)                                # gills underneath
    for hw, h in ((3.3, 0.7), (2.8, 0.6), (2.1, 0.5), (1.2, 0.35)):
        yt = base - 0.8 - h - sum(hh for _hw, hh in ((3.3, 0.7), (2.8, 0.6), (2.1, 0.5), (1.2, 0.35)) if _hw > hw)
        J(-hw, yt, cz - hw, 2 * hw, h, 2 * hw, R)
    top = base - 0.8 - 2.15
    for x, z in ((-1.6, cz - 1.4), (0.8, cz - 0.5), (-0.4, cz + 0.9), (1.4, cz + 1.6), (-2.2, cz + 1.4)):
        J(x, top - 0.05, z, 0.75, 0.1, 0.75, SP)
    for x, y in ((-2.4, base - 1.2), (1.0, base - 1.6), (-0.6, base - 1.1)):
        J(x, y, cz - 3.33, 0.75, 0.5, 0.05, SP)
    J(-3.3, base - 0.95, cz - 3.32, 6.6, 0.2, 0.04, RD)

@design("froggie_princess", "Froggie Princess", "custom")
def _(m):
    J = vanilla_frog(m, 0, 4.6, -0.2, s=0.8, bow=False)
    G, GD, GEM, GEM2 = '#f2c33a', '#b8861c', '#ff6fb5', '#7fd6ff'
    cz, hw, base = -1.3, 2.0, 15.5
    J(-hw, base - 1.2, cz - hw, 2 * hw, 1.2, 0.35, G); J(-hw, base - 1.2, cz + hw - 0.35, 2 * hw, 1.2, 0.35, G)   # crown band
    J(-hw, base - 1.2, cz - hw, 0.35, 1.2, 2 * hw, G); J(hw - 0.35, base - 1.2, cz - hw, 0.35, 1.2, 2 * hw, G)
    for x, z in ((-hw, cz - hw), (hw - 0.45, cz - hw), (-hw, cz + hw - 0.45), (hw - 0.45, cz + hw - 0.45), (-0.225, cz - hw),
                 (-0.225, cz + hw - 0.45), (-hw, cz - 0.225), (hw - 0.45, cz - 0.225)):
        J(x, base - 2.1, z, 0.45, 0.9, 0.45, G)                                        # prongs
        J(x + 0.05, base - 2.45, z + 0.05, 0.35, 0.35, 0.35, GD)
    J(-0.4, base - 0.95, cz - hw - 0.07, 0.8, 0.6, 0.07, GEM)                          # front gem
    for x in (-1.45, 0.95):
        J(x, base - 0.9, cz - hw - 0.06, 0.5, 0.45, 0.06, GEM2)
    J(-hw + 0.35, base - 0.3, cz - hw + 0.35, 2 * hw - 0.7, 0.3, 2 * hw - 0.7, '#e0609c')   # velvet cushion

@design("froggie_flower_crown", "Froggie Flower Crown", "custom")
def _(m):
    J = vanilla_frog(m, 0, 4.6, -0.2, s=0.8, bow=False)
    LV = '#4cae3a'
    base = 15.5
    def fl(x, z, petal, centre='#ffe14f'):
        J(x - 0.3, base - 0.55, z - 0.3, 0.6, 0.55, 0.6, centre)
        for dx, dz in ((-0.6, 0), (0.6, 0), (0, -0.6), (0, 0.6)):
            J(x + dx - 0.33, base - 0.45, z + dz - 0.33, 0.66, 0.45, 0.66, petal)
    J(-3.6, base - 0.25, -3.0, 7.2, 0.25, 0.7, LV)                                     # leafy band over her eyes
    J(-3.6, base - 0.25, 0.0, 7.2, 0.25, 0.7, LV)
    spots = [(-3.0, -2.7), (-1.0, -2.7), (1.0, -2.7), (3.0, -2.7), (-2.0, 0.35), (0.0, 0.35), (2.0, 0.35)]
    cols = ['#ff9cc8', '#ffffff', '#c49bff', '#ff9cc8', '#ffffff', '#ffb3cf', '#c49bff']
    for (x, z), c in zip(spots, cols):
        fl(x, z, c)
    for x, z in ((-2.0, -2.9), (0.0, -2.9), (2.0, -2.9)):
        J(x - 0.3, base - 0.35, z - 0.5, 0.6, 0.3, 0.7, LV)                             # leaves between the flowers

# ---------------- cute buddies ----------------
@design("axolotl_buddy", "Axolotl Buddy", "cute")
def _(m):
    P, PD, GILL, EYE = '#f6a8c8', '#e58bb0', '#d4458a', '#1a1018'
    y0 = 4.6
    rbox(m, -1.3, y0, -1.4, 1.3, y0 + 1.6, 3.2, P, r=0.4)                               # body
    m.box(-0.15, y0 + 1.6, -0.8, 0.15, y0 + 2.0, 3.0, PD)                               # back fin
    rbox(m, -2.1, y0, -4.2, 2.1, y0 + 2.2, -1.2, P, r=0.5)                              # big head
    for sd in (-1, 1):
        for k in range(3):                                                              # three fluffy gills per side
            y = y0 + 0.5 + 0.6 * k
            m.box(min(sd * 2.1, sd * (3.0 - 0.15 * k)), y, -2.6 + 0.3 * k, max(sd * 2.1, sd * (3.0 - 0.15 * k)), y + 0.45, -2.1 + 0.3 * k, GILL)
        m.box(sd * 1.0 - 0.25, y0 + 2.2, -2.4, sd * 1.0 + 0.25, y0 + 2.9, -1.9, GILL)   # top gills
        m.box(sd * 1.3 - 0.3, y0 + 1.2, -4.27, sd * 1.3 + 0.3, y0 + 1.7, -4.2, EYE)       # eyes
        m.box(sd * 1.3 - 0.2 + 0.1 * sd, y0 + 1.45, -4.3, sd * 1.3 + 0.0 + 0.1 * sd, y0 + 1.65, -4.27, '#ffffff')
        m.box(sd * 1.6 - 0.3, y0 + 0.75, -4.25, sd * 1.6 + 0.3, y0 + 1.0, -4.2, '#ff7fa8')  # blush
        for z in (-0.8, 2.2):                                                            # little legs
            m.box(min(sd * 1.3, sd * 1.9), y0, z - 0.3, max(sd * 1.3, sd * 1.9), y0 + 0.5, z + 0.3, PD)
    m.box(-0.5, y0 + 0.55, -4.27, 0.5, y0 + 0.7, -4.2, '#a43a6a')                        # smile
    m.box(-0.15, y0 + 0.2, 3.2, 0.15, y0 + 1.6, 4.6, PD)                                # tail fin
    m.box(-0.12, y0 + 0.5, 4.6, 0.12, y0 + 1.3, 5.4, PD)

@design("bee_buddy", "Bee Buddy", "cute")
def _(m):
    Y, BR, WING, EYE = '#f2c23a', '#3d2a1c', '#eef8ffaa', '#1a1418'
    y0 = 5.0
    rbox(m, -1.75, y0, -2.5, 1.75, y0 + 3.5, 2.5, Y, r=0.3)                             # body
    for z1 in (-0.5, 1.1):
        m.box(-1.78, y0 + 0.05, z1, 1.78, y0 + 3.47, z1 + 0.6, BR)                      # stripes
    for sd in (-1, 1):
        m.box(sd * 0.95 - 0.5, y0 + 1.3, -2.56, sd * 0.95 + 0.5, y0 + 2.6, -2.5, EYE)     # eyes
        m.box(sd * 0.95 - 0.35 + 0.15, y0 + 2.1, -2.6, sd * 0.95 - 0.05 + 0.15, y0 + 2.4, -2.56, '#ffffff')
        m.box(sd * 0.7 - 0.12, y0 + 3.5, -2.5, sd * 0.7 + 0.12, y0 + 4.3, -2.25, BR)       # antennae
        m.box(sd * 0.7 - 0.12, y0 + 4.05, -3.0, sd * 0.7 + 0.12, y0 + 4.3, -2.5, BR)
        m.box(min(sd * 0.2, sd * 2.6), y0 + 3.5, -0.4, max(sd * 0.2, sd * 2.6), y0 + 3.56, 1.8, WING,
              rot=('z', 22.5 * sd, (sd * 0.2, y0 + 3.5, 0)))                              # wings
        for z in (-1.2, 0.0, 1.2):
            m.box(sd * 0.8 - 0.12, y0 - 0.4, z - 0.12, sd * 0.8 + 0.12, y0, z + 0.12, BR)  # tiny legs
    m.box(-0.45, y0 + 0.6, -2.55, 0.45, y0 + 0.8, -2.5, BR)                               # little mouth
    m.box(-0.2, y0 + 1.5, 2.5, 0.2, y0 + 1.9, 3.1, '#c9ced8')                             # stinger

@design("sleepy_fox", "Sleepy Fox", "cute")
def _(m):
    O, OD, W, K = '#e2832e', '#c06a22', '#f5efe6', '#3a2a22'
    y0 = 4.6
    rbox(m, -1.9, y0, -0.8, 1.9, y0 + 2.0, 3.2, O, r=0.6)                               # curled body
    rbox(m, -0.2, y0, -3.3, 2.7, y0 + 1.9, -0.6, O, r=0.4)                              # head resting at the front
    m.box(0.5, y0, -4.0, 2.0, y0 + 0.8, -3.3, W)                                        # white muzzle
    m.box(1.0, y0 + 0.5, -4.08, 1.5, y0 + 0.85, -3.95, K)                               # nose
    for x in (0.0, 2.0):
        m.box(x, y0 + 1.9, -2.0, x + 0.7, y0 + 2.5, -1.4, O)                             # ears
        m.box(x + 0.15, y0 + 2.5, -1.9, x + 0.55, y0 + 2.8, -1.5, K)
        m.box(x + 0.1, y0 + 1.15, -3.36, x + 0.65, y0 + 1.3, -3.3, K)                    # closed eyes
    m.box(-0.1, y0 + 0.75, -3.36, 0.2, y0 + 1.05, -3.3, W); m.box(2.4, y0 + 0.75, -3.36, 2.7, y0 + 1.05, -3.3, W)
    rbox(m, -2.9, y0, -3.6, -0.3, y0 + 1.5, -0.2, O, r=0.5)                              # fluffy tail wrapped in front
    rbox(m, -2.9, y0, -3.6, -1.4, y0 + 1.5, -2.3, W, r=0.4)                              # white tail tip
    for x, z in ((-1.2, 1.8), (1.2, 2.6)):
        m.box(x - 0.2, y0 + 2.0, z - 0.2, x + 0.2, y0 + 2.05, z + 0.2, OD)
    for i, (x, y) in enumerate(((2.8, 8.0), (3.5, 9.0), (4.3, 10.1))):                  # z z z
        sz = 0.35 + 0.15 * i
        m.box(x - sz, y + sz - 0.12, -1.0, x + sz, y + sz, -0.9, '#ffffff')
        m.box(x - sz, y - sz, -1.0, x + sz, y - sz + 0.12, -0.9, '#ffffff')
        m.box(x - 0.08, y - sz, -1.0, x + 0.08, y + sz, -0.9, '#ffffff', rot=('z', -45, (x, y, -0.95)))

@design("cat_loaf", "Cat Loaf", "cute")
def _(m):
    G, GD, PINK, K, W = '#a3a3aa', '#6e6e76', '#f2a0b0', '#2a2a30', '#f4f2ee'
    y0 = 4.6
    rbox(m, -2.2, y0, -1.4, 2.2, y0 + 2.4, 3.0, G, r=0.7)                               # loaf
    rbox(m, -1.7, y0 + 0.5, -3.3, 1.7, y0 + 3.1, -0.9, G, r=0.5)                        # head
    for sd in (-1, 1):
        steps(m, sd * 1.1, -1.8, y0 + 3.1, [1.0, 0.7, 0.4], G, depth=0.5, h=0.75, smooth=1)   # ears
        m.box(sd * 1.1 - 0.25, y0 + 3.1, -2.1, sd * 1.1 + 0.25, y0 + 3.5, -2.05, PINK)
        cx = sd * 0.8                                                                   # happy closed eyes ^ ^
        m.box(cx - 0.4, y0 + 1.9, -3.36, cx - 0.15, y0 + 2.1, -3.3, K)
        m.box(cx - 0.15, y0 + 2.1, -3.36, cx + 0.15, y0 + 2.3, -3.3, K)
        m.box(cx + 0.15, y0 + 1.9, -3.36, cx + 0.4, y0 + 2.1, -3.3, K)
        m.box(sd * 1.2 - 0.3, y0 + 1.35, -3.35, sd * 1.2 + 0.3, y0 + 1.6, -3.3, '#ffb3c6')   # blush
        for k in range(2):
            m.box(min(sd * 1.7, sd * 2.4), y0 + 1.2 + 0.3 * k, -3.0, max(sd * 1.7, sd * 2.4), y0 + 1.27 + 0.3 * k, -2.95, W)  # whiskers
    m.box(-0.2, y0 + 1.5, -3.37, 0.2, y0 + 1.75, -3.3, PINK)                             # nose
    m.box(-0.45, y0 + 1.25, -3.36, -0.05, y0 + 1.37, -3.3, K); m.box(0.05, y0 + 1.25, -3.36, 0.45, y0 + 1.37, -3.3, K)
    for z in (0.0, 1.0, 2.0):
        m.box(-1.6, y0 + 2.4, z, 1.6, y0 + 2.46, z + 0.35, GD)                           # tabby stripes
    for x in (-0.5, 0.5):
        m.box(x - 0.15, y0 + 3.1, -2.6, x + 0.15, y0 + 3.15, -1.2, GD)
    m.box(-2.6, y0, -1.2, -2.2, y0 + 0.6, 2.8, G)                                       # tail tucked along the side
    for z in (-0.6, 0.6, 1.8):
        m.box(-2.62, y0 + 0.05, z, -2.18, y0 + 0.62, z + 0.35, GD)
    for x in (-0.9, 0.9):
        m.box(x - 0.4, y0, -1.75, x + 0.4, y0 + 0.4, -1.3, W)                           # front paws

@design("penguin_buddy", "Penguin Buddy", "cute")
def _(m):
    K, W, OR = '#1f2330', '#f4f2ee', '#f2a03a'
    y0 = 4.6
    for sd in (-1, 1):
        m.box(sd * 0.6 - 0.45, y0, -1.5, sd * 0.6 + 0.45, y0 + 0.3, -0.2, OR)            # feet
    rbox(m, -1.4, y0 + 0.3, -1.1, 1.4, y0 + 3.6, 1.3, K, r=0.5)                         # body
    m.box(-1.0, y0 + 0.5, -1.16, 1.0, y0 + 3.0, -1.1, W)                                # belly
    rbox(m, -1.25, y0 + 3.4, -1.0, 1.25, y0 + 5.5, 1.2, K, r=0.45)                      # head
    m.box(-0.95, y0 + 3.6, -1.06, 0.95, y0 + 5.0, -1.0, W)                              # face
    for sd in (-1, 1):
        m.box(sd * 0.5 - 0.2, y0 + 4.3, -1.1, sd * 0.5 + 0.2, y0 + 4.8, -1.06, K)          # eyes
        m.box(sd * 0.5 - 0.12 + 0.05, y0 + 4.6, -1.12, sd * 0.5 + 0.05, y0 + 4.75, -1.1, W)
        m.box(sd * 0.8 - 0.22, y0 + 3.85, -1.08, sd * 0.8 + 0.22, y0 + 4.05, -1.06, '#ffb3c6')
        m.box(min(sd * 1.4, sd * 1.75), y0 + 1.2, -0.6, max(sd * 1.4, sd * 1.75), y0 + 3.0, 0.7, K,
              rot=('z', 22.5 * sd, (sd * 1.4, y0 + 3.0, 0)))                              # flippers
    m.box(-0.35, y0 + 3.95, -1.6, 0.35, y0 + 4.35, -1.0, OR)                            # beak
    rbox(m, -0.9, y0 + 5.5, -0.9, 0.9, y0 + 5.9, 0.9, '#e8343f', r=0.3)                 # tiny beanie
    m.box(-0.25, y0 + 5.9, -0.25, 0.25, y0 + 6.3, 0.25, W)

@design("baby_hippo", "Baby Hippo", "cute")
def _(m):
    G, GL, PINK, K = '#8f8796', '#b4a9b8', '#e7a3b2', '#3a3340'
    y0 = 4.6
    rbox(m, -2.0, y0, -1.0, 2.0, y0 + 2.4, 3.4, G, r=0.7)                               # chunky body
    rbox(m, -1.8, y0 + 0.4, -3.6, 1.8, y0 + 2.9, -0.6, G, r=0.5)                        # head
    rbox(m, -1.9, y0 + 0.2, -4.5, 1.9, y0 + 1.6, -3.0, GL, r=0.4)                       # wide snout
    for sd in (-1, 1):
        m.box(sd * 0.7 - 0.2, y0 + 1.6, -4.1, sd * 0.7 + 0.2, y0 + 1.65, -3.7, K)          # nostrils
        m.box(sd * 1.0 - 0.25, y0 + 2.0, -3.66, sd * 1.0 + 0.25, y0 + 2.5, -3.6, K)        # eyes
        m.box(sd * 1.0 - 0.12 + 0.05, y0 + 2.3, -3.68, sd * 1.0 + 0.05, y0 + 2.45, -3.66, '#ffffff')
        m.box(sd * 1.3 - 0.35, y0 + 2.9, -1.5, sd * 1.3 + 0.35, y0 + 3.4, -0.9, G)        # ears
        m.box(sd * 1.3 - 0.2, y0 + 3.0, -1.55, sd * 1.3 + 0.2, y0 + 3.3, -1.5, PINK)
        m.box(sd * 1.5 - 0.35, y0 + 0.6, -4.55, sd * 1.5 + 0.35, y0 + 1.0, -4.5, PINK)    # rosy cheeks
        for z in (-0.4, 2.6):
            m.box(min(sd * 1.4, sd * 2.1), y0, z - 0.4, max(sd * 1.4, sd * 2.1), y0 + 0.6, z + 0.4, GL)
    m.box(-0.8, y0 + 0.45, -4.55, 0.8, y0 + 0.6, -4.5, K)                                # smile
    m.box(-0.2, y0 + 1.0, 3.4, 0.2, y0 + 1.6, 3.8, G)                                   # tiny tail

@design("hamster_buddy", "Hamster Buddy", "cute")
def _(m):
    O, W, PINK, K = '#e8a35a', '#f6efe4', '#f2a0b0', '#1d1418'
    y0 = 4.6
    rbox(m, -1.8, y0, -1.4, 1.8, y0 + 2.6, 1.8, O, r=0.7)                               # round body
    m.box(-1.0, y0, -1.46, 1.0, y0 + 1.2, -1.4, W)                                      # belly
    for sd in (-1, 1):
        rbox(m, min(sd * 1.3, sd * 2.3), y0 + 0.8, -1.6, max(sd * 1.3, sd * 2.3), y0 + 1.8, -0.3, W, r=0.3)  # stuffed cheeks
        m.box(sd * 1.8 - 0.3, y0 + 1.1, -1.66, sd * 1.8 + 0.3, y0 + 1.4, -1.6, PINK)
        m.box(sd * 0.75 - 0.25, y0 + 1.8, -1.46, sd * 0.75 + 0.25, y0 + 2.3, -1.4, K)      # eyes
        m.box(sd * 0.75 - 0.15 + 0.05, y0 + 2.1, -1.48, sd * 0.75 + 0.05, y0 + 2.25, -1.46, '#ffffff')
        m.box(sd * 1.1 - 0.35, y0 + 2.5, -0.6, sd * 1.1 + 0.35, y0 + 3.1, -0.1, O)        # ears
        m.box(sd * 1.1 - 0.2, y0 + 2.6, -0.65, sd * 1.1 + 0.2, y0 + 3.0, -0.6, PINK)
        m.box(sd * 0.45 - 0.25, y0 + 0.6, -1.75, sd * 0.45 + 0.25, y0 + 0.95, -1.4, PINK)  # little paws
    m.box(-0.15, y0 + 1.45, -1.47, 0.15, y0 + 1.65, -1.4, PINK)                          # nose
    m.box(-0.25, y0 + 0.5, -2.0, 0.25, y0 + 1.3, -1.7, '#4a4a52')                        # sunflower seed
    m.box(-0.08, y0 + 0.55, -2.02, 0.08, y0 + 1.25, -2.0, '#e8e6e0')

@design("raccoon_buddy", "Raccoon Buddy", "cute")
def _(m):
    G, GD, W, K = '#8a8a92', '#55555e', '#e8e6e0', '#1d1b22'
    y0 = 4.6
    for sd in (-1, 1):
        m.box(sd * 0.6 - 0.35, y0, -0.6, sd * 0.6 + 0.35, y0 + 0.4, 0.4, K)              # feet
        m.box(sd * 0.6 - 0.3, y0 + 0.4, -0.4, sd * 0.6 + 0.3, y0 + 1.0, 0.3, GD)          # legs
    rbox(m, -1.3, y0 + 1.0, -0.9, 1.3, y0 + 3.2, 1.0, G, r=0.4)                         # body
    m.box(-0.8, y0 + 1.2, -0.95, 0.8, y0 + 2.8, -0.9, '#b8b8be')                        # belly
    rbox(m, -1.6, y0 + 3.1, -1.3, 1.6, y0 + 5.1, 1.2, G, r=0.45)                        # head
    m.box(-1.6, y0 + 3.9, -1.36, 1.6, y0 + 4.5, -1.3, K)                                # bandit mask
    for sd in (-1, 1):
        m.box(sd * 0.75 - 0.22, y0 + 4.0, -1.4, sd * 0.75 + 0.22, y0 + 4.4, -1.36, W)     # eye shine
        m.box(sd * 0.75 - 0.4, y0 + 4.55, -1.34, sd * 0.75 + 0.4, y0 + 4.75, -1.3, W)    # white brows
        steps(m, sd * 1.05, 0.0, y0 + 5.1, [0.9, 0.6, 0.3], G, depth=0.4, h=0.6, smooth=1)  # ears
        m.box(sd * 1.05 - 0.2, y0 + 5.1, -0.22, sd * 1.05 + 0.2, y0 + 5.4, -0.2, W)
    m.box(-0.6, y0 + 3.15, -1.7, 0.6, y0 + 3.85, -1.3, W)                               # muzzle
    m.box(-0.2, y0 + 3.6, -1.75, 0.2, y0 + 3.9, -1.7, K)                                # nose
    m.box(1.3, y0 + 2.6, -0.3, 2.6, y0 + 3.0, 0.3, G)                                   # waving arm
    m.box(2.2, y0 + 3.0, -0.3, 2.6, y0 + 4.0, 0.3, G)
    m.box(-2.2, y0 + 1.8, -0.3, -1.3, y0 + 2.2, 0.3, G)
    for i in range(5):                                                                  # striped tail curling up
        z = 1.0 + i * 0.6; y = y0 + 0.8 + i * 0.45
        m.box(-0.45, y, z, 0.45, y + 0.8, z + 0.6, (G, K)[i % 2])

# ---------- cool (Minecraft) ----------
GLOW.update({'#29dfeb', '#d77bff', '#fff4a0', '#ffc21f'})

@design("warden_tendrils", "Warden Tendrils", "cool")
def _(m):
    D1, D2, GL = '#0f2a33', '#173d47', '#29dfeb'
    dome(m, 4.0, [(4.5, 0.8), (3.6, 0.5)], D1)
    for x, z in ((-1.5, -2.0), (1.8, 1.0), (-0.5, 2.2), (2.2, -2.6)):
        m.box(x - 0.3, 5.25, z - 0.3, x + 0.3, 5.4, z + 0.3, GL)                       # soul specks
    for sd in (-1, 1):
        x = sd * 3.0; r = ('z', -22.5 * sd, (x, 4.8, 0))
        m.box(x - 1.1, 4.8, -0.45, x + 1.1, 9.8, 0.45, D2, rot=r)                       # big tendril
        m.box(x - 0.55, 5.3, -0.55, x + 0.55, 9.3, -0.45, GL, rot=r)                    # glowing front
        m.box(x - 0.55, 5.3, 0.45, x + 0.55, 9.3, 0.55, GL, rot=r)
        m.box(x - 0.8, 9.8, -0.35, x + 0.8, 10.4, 0.35, D1, rot=r)

@design("totem_halo", "Totem Halo", "cool")
def _(m):
    GD, GDD, EM, HALO = '#f2c33a', '#b8861c', '#2fd06a', '#ffe45c'
    y0 = 4.6
    m.box(-0.8, y0, -0.6, 0.8, y0 + 1.8, 0.6, GD)                                       # robe
    m.box(-0.8, y0, -0.65, 0.8, y0 + 0.3, -0.6, GDD)
    m.box(-2.4, y0 + 1.2, -0.4, 2.4, y0 + 1.7, 0.4, GD)                                 # arms out
    m.box(-0.9, y0 + 1.8, -0.9, 0.9, y0 + 3.6, 0.9, GD)                                 # head
    for sd in (-1, 1):
        m.box(sd * 0.45 - 0.25, y0 + 2.5, -0.95, sd * 0.45 + 0.25, y0 + 2.8, -0.9, EM)    # emerald eyes
    m.box(-0.3, y0 + 2.0, -0.95, 0.3, y0 + 2.2, -0.9, GDD)
    m.box(-0.5, y0 + 0.9, -0.66, 0.5, y0 + 1.2, -0.6, EM)                               # belt gem
    for (x1, z1, x2, z2) in ((-3.6, -3.6, 3.6, -3.0), (-3.6, 3.0, 3.6, 3.6), (-3.6, -3.0, -3.0, 3.0), (3.0, -3.0, 3.6, 3.0)):
        m.box(x1, y0 + 4.4, z1, x2, y0 + 4.8, z2, HALO)                                # floating halo
    for x, y in ((-3.0, 6.6), (3.2, 7.4), (-2.2, 9.6)):
        star(m, x, y, -1.0, 0.35, HALO)

@design("end_crystal_hat", "End Crystal Hat", "cool")
def _(m):
    BR, BRD = '#3b3b3e', '#232326'
    rbox(m, -2.2, 4.6, -2.2, 2.2, 5.6, 2.2, BR, r=0.3)                                  # bedrock base
    for x, z in ((-1.4, -2.25), (0.6, -2.25), (-0.4, 2.2), (2.2, 0.4)):
        m.box(x, 4.8, z - 0.05, x + 0.7, 5.3, z + 0.05, BRD)
    c = (0, 8.0, 0)
    m.box(-0.75, 7.25, -0.75, 0.75, 8.75, 0.75, '#ff5ce1', rot=('x', 45, c))            # pink core
    m.box(-1.3, 6.7, -1.3, 1.3, 9.3, 1.3, '#b48cff70', rot=('z', 45, c))                 # inner glass
    m.box(-1.8, 6.2, -1.8, 1.8, 9.8, 1.8, '#e6d8ff50', rot=('y', 45, c))                 # outer glass
    m.box(-0.2, 9.8, -0.2, 0.2, 13.0, 0.2, '#ff9fd290')                                  # beam

@design("wither_crown", "Wither Crown", "cool")
def _(m):
    K, KD, EY = '#2b2b2f', '#18181b', '#c9ced8'
    m.box(-4.4, 4.6, -0.5, 4.4, 5.2, 0.5, K)                                            # shoulder bar
    for i in range(4):
        m.box(-1.6 + 0.2 * i, 5.0 - 0.0, 0.6 + i * 0.8, 1.6 - 0.2 * i, 5.4, 1.0 + i * 0.8, K)   # ribs/spine
    for cx, s, cz in ((0, 1.35, -0.6), (-3.0, 1.0, 0.0), (3.0, 1.0, 0.0)):
        y1 = 5.2 if cx == 0 else 5.0
        rbox(m, cx - s, y1, cz - s, cx + s, y1 + 2 * s, cz + s, K, r=0.15)
        for sd in (-1, 1):
            m.box(cx + sd * 0.5 * s - 0.3 * s, y1 + 1.0 * s, cz - s - 0.06, cx + sd * 0.5 * s + 0.3 * s, y1 + 1.4 * s, cz - s, EY)
        m.box(cx - 0.6 * s, y1 + 0.35 * s, cz - s - 0.06, cx + 0.6 * s, y1 + 0.55 * s, cz - s, KD)
        m.box(cx - 0.6 * s, y1 + 0.55 * s, cz - s - 0.06, cx - 0.4 * s, y1 + 0.75 * s, cz - s, EY)
        m.box(cx + 0.4 * s, y1 + 0.55 * s, cz - s - 0.06, cx + 0.6 * s, y1 + 0.75 * s, cz - s, EY)

@design("blaze_halo", "Blaze Halo", "cool")
def _(m):
    import math
    ROD, ROD_D, BY, BYD = '#ffc21f', '#d9861a', '#f5c542', '#c98a1c'
    for i in range(8):
        a = i * math.pi / 4; x, z = 5.4 * math.cos(a), 5.4 * math.sin(a)
        y = 0.5 if i % 2 else 3.0
        m.box(x - 0.4, y, z - 0.4, x + 0.4, y + 3.6, z + 0.4, ROD)                      # orbiting rods
        m.box(x - 0.42, y + 1.2, z - 0.42, x + 0.42, y + 1.5, z + 0.42, ROD_D)
    rbox(m, -1.2, 4.6, -1.2, 1.2, 7.0, 1.2, BY, r=0.15)                                 # mini blaze head
    m.box(-1.25, 4.6, -1.25, 1.25, 5.2, 1.25, BYD)
    for sd in (-1, 1):
        m.box(sd * 0.55 - 0.3, 5.9, -1.26, sd * 0.55 + 0.3, 6.3, -1.2, '#3a1a0a')
        m.box(sd * 0.55 - 0.3, 6.3, -1.26, sd * 0.55 + 0.3, 6.45, -1.2, '#fff2a8')
    for x, y, z in ((-2.0, 7.6, 0.4), (1.6, 8.2, -0.6), (0.2, 9.0, 0.8)):
        m.box(x - 0.3, y, z - 0.3, x + 0.3, y + 0.6, z + 0.3, '#5a5a62a0')              # smoke puffs

@design("baby_dragon", "Baby Ender Dragon", "cool")
def _(m):
    K, KL, WG, EYE = '#1b1620', '#3a3340', '#4a3a58', '#d77bff'
    y0 = 4.6
    rbox(m, -1.4, y0 + 0.4, -1.0, 1.4, y0 + 2.4, 2.6, K, r=0.4)                         # body
    for sd in (-1, 1):
        for z in (-0.6, 2.0):
            m.box(sd * 0.9 - 0.35, y0, z - 0.35, sd * 0.9 + 0.35, y0 + 0.6, z + 0.35, K)  # legs
        r = ('z', 22.5 * sd, (sd * 1.4, y0 + 2.0, 0))
        m.box(min(sd * 1.4, sd * 4.6), y0 + 1.9, -0.6, max(sd * 1.4, sd * 4.6), y0 + 2.1, 2.2, WG, rot=r)   # wings
        m.box(min(sd * 1.4, sd * 4.8), y0 + 2.1, -0.7, max(sd * 1.4, sd * 4.8), y0 + 2.4, -0.4, KL, rot=r)
        m.box(sd * 0.55 - 0.3, y0 + 3.6, -3.06, sd * 0.55 + 0.3, y0 + 3.9, -3.0, EYE)     # purple eyes
        m.box(sd * 0.45 - 0.12, y0 + 4.0, -2.4, sd * 0.45 + 0.12, y0 + 4.6, -1.9, KL)     # horns
    rbox(m, -1.0, y0 + 2.4, -3.0, 1.0, y0 + 4.0, -0.8, K, r=0.3)                        # head
    m.box(-0.7, y0 + 2.5, -4.0, 0.7, y0 + 3.3, -3.0, K)                                 # snout
    for sd in (-1, 1):
        m.box(sd * 0.35 - 0.12, y0 + 3.0, -4.05, sd * 0.35 + 0.12, y0 + 3.2, -4.0, KL)
    for i in range(4):                                                                  # tail with spikes
        z = 2.6 + i * 0.8; w = 0.6 - 0.1 * i
        m.box(-w, y0 + 0.6, z, w, y0 + 1.6 - 0.15 * i, z + 0.8, K)
        m.box(-0.12, y0 + 1.6 - 0.15 * i, z + 0.2, 0.12, y0 + 2.0 - 0.15 * i, z + 0.6, KL)
    for z in (-0.2, 0.8, 1.8):
        m.box(-0.15, y0 + 2.4, z, 0.15, y0 + 2.9, z + 0.4, KL)                          # back spikes

@design("turtle_helmet", "Turtle Shell Helmet", "cool")
def _(m):
    TG, TD, TL = '#4f9a3a', '#2f6b2a', '#7cc35c'
    m.box(-4.6, 1.2, 4.0, 4.6, 4.0, 4.6, TG)                                            # back flap
    for sd in (-1, 1):
        m.box(min(sd * 4.0, sd * 4.6), 1.2, -4.0, max(sd * 4.0, sd * 4.6), 4.0, 4.0, TG)   # side flaps
    m.box(-4.6, 3.2, -4.6, 4.6, 4.0, -4.0, TG)                                          # front brim
    m.box(-4.6, 3.2, -4.7, 4.6, 3.4, -4.6, TD)
    y = dome(m, 4.0, [(4.6, 0.9), (3.8, 0.7), (2.6, 0.5)], TG)
    for x, z in ((-2.2, -2.2), (2.2, -2.2), (-2.2, 2.2), (2.2, 2.2)):                   # scutes
        m.box(x - 1.1, 4.95, z - 1.1, x + 1.1, 5.0, z + 1.1, TD)
    m.box(-1.2, y - 0.05, -1.2, 1.2, y + 0.05, 1.2, TD)
    m.box(-0.7, y, -0.7, 0.7, y + 0.1, 0.7, TL)
    for sd in (-1, 1):
        m.box(sd * 4.6 - 0.05, 1.6, -3.0, sd * 4.6 + 0.05, 3.6, -1.0, TD)
        m.box(sd * 4.6 - 0.05, 1.6, 1.0, sd * 4.6 + 0.05, 3.6, 3.0, TD)

@design("armadillo_buddy", "Armadillo Buddy", "cool")
def _(m):
    SH, SHD, SK, K, PK = '#a8625a', '#7c4440', '#e2a894', '#2a1a1a', '#f2a0b0'
    y0 = 4.6
    for sd in (-1, 1):
        for z in (-1.0, 1.8):
            m.box(sd * 1.1 - 0.35, y0, z - 0.35, sd * 1.1 + 0.35, y0 + 0.6, z + 0.35, SK)
    rbox(m, -1.8, y0 + 0.5, -1.6, 1.8, y0 + 2.9, 2.4, SH, r=0.6)                         # shell
    for z in (-0.9, 0.1, 1.1):
        m.box(-1.84, y0 + 0.55, z, 1.84, y0 + 2.92, z + 0.3, SHD)                        # bands
    rbox(m, -0.9, y0 + 0.5, -3.4, 0.9, y0 + 2.0, -1.4, SK, r=0.3)                       # head
    m.box(-0.5, y0 + 0.6, -4.0, 0.5, y0 + 1.3, -3.4, SK)                                # snout
    m.box(-0.2, y0 + 0.95, -4.05, 0.2, y0 + 1.25, -4.0, PK)
    for sd in (-1, 1):
        m.box(sd * 0.55 - 0.25, y0 + 2.0, -2.3, sd * 0.55 + 0.25, y0 + 2.8, -2.0, SK)     # ears
        m.box(sd * 0.55 - 0.15, y0 + 2.1, -2.35, sd * 0.55 + 0.15, y0 + 2.6, -2.3, PK)
        m.box(sd * 0.45 - 0.2, y0 + 1.4, -3.46, sd * 0.45 + 0.2, y0 + 1.75, -3.4, K)      # eyes
        m.box(sd * 0.45 - 0.08 + 0.05, y0 + 1.6, -3.48, sd * 0.45 + 0.05, y0 + 1.72, -3.46, '#ffffff')
    m.box(-0.25, y0 + 0.4, 2.4, 0.25, y0 + 0.8, 3.6, SHD)                               # tail

@design("breeze_buddy", "Breeze Buddy", "cool")
def _(m):
    W1, W2, HD, FC = '#b9c8ffb0', '#d6c8ff90', '#d6e0ff', '#3b3b8a'
    y0 = 4.6
    for i, w in enumerate((1.2, 2.4, 3.6)):
        m.box(-w / 2, y0 + i * 1.1, -w / 2, w / 2, y0 + i * 1.1 + 0.9, w / 2, (W1, W2)[i % 2], rot=('y', (22.5, -22.5, 45)[i], (0, 0, 0)))
    rbox(m, -1.7, y0 + 3.2, -1.7, 1.7, y0 + 6.2, 1.7, HD, r=0.4)                        # head
    for sd in (-1, 1):
        m.box(sd * 0.75 - 0.35, y0 + 4.5, -1.76, sd * 0.75 + 0.35, y0 + 5.3, -1.7, FC)
        m.box(sd * 0.75 - 0.18 + 0.08, y0 + 5.0, -1.78, sd * 0.75 + 0.08, y0 + 5.25, -1.76, '#ffffff')
    m.box(-0.4, y0 + 3.8, -1.76, 0.4, y0 + 4.05, -1.7, FC)
    m.box(-0.6, y0 + 6.2, -0.6, 0.6, y0 + 7.3, 0.6, '#b9c8ff', rot=('y', 45, (0, 0, 0)))
    for x, y, z in ((-4.0, 1.0, -0.6), (2.4, 2.0, 0.4), (-3.2, 3.4, 1.4)):
        m.box(x, y0 + y, z - 0.1, x + 1.8, y0 + y + 0.2, z + 0.1, '#e6eeffb0')          # wind streaks

@design("planet_orbit", "Planet Orbit", "cool")
def _(m):
    P, PD, RG, MN = '#e6b86a', '#c98e4a', '#f2dca0', '#c9ced8'
    rbox(m, -1.7, 6.0, -1.7, 1.7, 9.4, 1.7, P, r=0.8)                                   # planet
    rbox(m, -1.4, 5.7, -1.4, 1.4, 9.7, 1.4, P, r=0.6)
    m.box(-1.75, 7.0, -1.75, 1.75, 7.35, 1.75, PD)
    m.box(-1.75, 8.2, -1.75, 1.75, 8.45, 1.75, PD)
    r = ('z', 22.5, (0, 7.7, 0))
    for (x1, z1, x2, z2) in ((-3.4, -3.4, 3.4, -2.6), (-3.4, 2.6, 3.4, 3.4), (-3.4, -2.6, -2.6, 2.6), (2.6, -2.6, 3.4, 2.6)):
        m.box(x1, 7.6, z1, x2, 7.8, z2, RG, rot=r)                                      # ring
    rbox(m, 3.4, 9.6, -0.5, 4.4, 10.6, 0.5, MN, r=0.3)                                  # moon
    m.box(-0.05, 4.6, -0.05, 0.05, 5.7, 0.05, '#ffffff00')
    for x, y in ((-3.6, 10.0), (-2.6, 5.4), (3.6, 5.6)):
        star(m, x, y, -0.5, 0.35, '#ffe45c')

# ---------- more brainrot ----------
@design("chimpanzini_bananini", "Chimpanzini Bananini", "trend")
def _(m):
    Y, YL, BRN, FACE, K = '#f5d43a', '#fff3b0', '#6b4326', '#d9a77a', '#1d1418'
    y0 = 4.6
    rbox(m, -1.6, y0, -1.6, 1.6, y0 + 2.0, 1.6, Y, r=0.5)                               # banana cup
    m.box(-0.4, y0, -0.4, 0.4, y0 + 0.1, 0.4, '#4b2d17')
    rbox(m, -1.2, y0 + 1.6, -1.2, 1.2, y0 + 3.6, 1.2, BRN, r=0.4)                       # monkey head
    m.box(-0.9, y0 + 1.7, -1.26, 0.9, y0 + 3.2, -1.2, FACE)
    m.box(-0.6, y0 + 1.7, -1.6, 0.6, y0 + 2.3, -1.26, FACE)                             # muzzle
    m.box(-0.3, y0 + 1.85, -1.62, 0.3, y0 + 1.95, -1.6, K)
    for sd in (-1, 1):
        m.box(sd * 0.45 - 0.2, y0 + 2.5, -1.28, sd * 0.45 + 0.2, y0 + 2.9, -1.26, K)
        m.box(min(sd * 1.2, sd * 1.7), y0 + 2.4, -0.3, max(sd * 1.2, sd * 1.7), y0 + 3.1, 0.3, FACE)   # ears
    for (x1, z1, x2, z2, ax, a) in ((-1.1, -1.8, 1.1, -1.4, 'x', -22.5), (-1.1, 1.4, 1.1, 1.8, 'x', 22.5),
                                    (1.4, -1.1, 1.8, 1.1, 'z', -22.5), (-1.8, -1.1, -1.4, 1.1, 'z', 22.5)):
        o = ((x1 + x2) / 2, y0 + 1.6, (z1 + z2) / 2)
        m.box(x1, y0 + 1.4, z1, x2, y0 + 4.0, z2, Y, rot=(ax, a, o))                    # peel flaps
    m.box(-0.2, y0 + 1.6, -1.85, 0.2, y0 + 3.8, -1.75, YL, rot=('x', -22.5, (0, y0 + 1.6, -1.6)))

@design("lirili_larila", "Lirili Larila", "trend")
def _(m):
    CG, CGD, GR, GRD, SAN, K = '#4f9a3a', '#2f6b2a', '#9a9aa6', '#6e6e7a', '#8a5a2a', '#1d1b22'
    y0 = 4.6
    for sd in (-1, 1):
        m.box(sd * 0.8 - 0.45, y0, -1.4, sd * 0.8 + 0.45, y0 + 0.25, 0.6, SAN)          # sandals
        m.box(sd * 0.8 - 0.45, y0 + 0.25, -0.9, sd * 0.8 + 0.45, y0 + 0.45, -0.7, SAN)
        m.box(sd * 0.8 - 0.3, y0 + 0.25, -0.5, sd * 0.8 + 0.3, y0 + 1.0, 0.3, CG)       # legs
        m.box(min(sd * 1.3, sd * 2.4), y0 + 2.0, -0.3, max(sd * 1.3, sd * 2.4), y0 + 2.5, 0.3, CG)   # cactus arms
        m.box(sd * 2.0, y0 + 2.0, -0.3, sd * 2.0 + sd * 0.4, y0 + 3.2, 0.3, CG) if sd > 0 else \
            m.box(sd * 2.4, y0 + 2.0, -0.3, sd * 2.0, y0 + 3.2, 0.3, CG)
    rbox(m, -1.3, y0 + 0.9, -1.0, 1.3, y0 + 3.6, 1.2, CG, r=0.4)                        # cactus body
    for x, y in ((-0.8, 1.4), (0.6, 2.0), (-0.2, 2.8), (0.9, 3.2), (-0.9, 2.4)):
        m.box(x - 0.08, y0 + y - 0.08, -1.12, x + 0.08, y0 + y + 0.08, -1.0, '#e8e6c8')  # spines
    rbox(m, -1.5, y0 + 3.4, -1.5, 1.5, y0 + 5.4, 1.3, GR, r=0.4)                        # elephant head
    for sd in (-1, 1):
        m.box(min(sd * 1.4, sd * 2.9), y0 + 3.3, -0.5, max(sd * 1.4, sd * 2.9), y0 + 5.3, -0.1, GR)   # ears
        m.box(min(sd * 1.6, sd * 2.6), y0 + 3.6, -0.55, max(sd * 1.6, sd * 2.6), y0 + 5.0, -0.5, GRD)
        m.box(sd * 0.6 - 0.2, y0 + 4.5, -1.56, sd * 0.6 + 0.2, y0 + 4.9, -1.5, K)
        m.box(sd * 0.55 - 0.1, y0 + 3.4, -1.9, sd * 0.55 + 0.1, y0 + 3.7, -1.5, '#f4f2ee')   # tusks
    m.box(-0.35, y0 + 2.8, -2.0, 0.35, y0 + 4.4, -1.5, GR)                              # trunk
    m.box(-0.35, y0 + 2.8, -2.5, 0.35, y0 + 3.2, -2.0, GR)

@design("brr_patapim", "Brr Brr Patapim", "trend")
def _(m):
    BK, BKD, MOSS, NOSE, K, W = '#6b4a2b', '#4b2d17', '#5c9e3a', '#e9a08a', '#1d1418', '#f4f2ee'
    y0 = 4.6
    rbox(m, -2.4, y0, -2.4, 2.4, y0 + 3.6, 2.4, BK, r=0.6)                               # tree stump
    for x in (-1.8, -0.4, 1.2):
        m.box(x, y0 + 0.2, -2.46, x + 0.2, y0 + 1.0, -2.4, BKD)
    dome(m, y0 + 3.4, [(2.6, 0.5), (2.0, 0.5), (1.2, 0.4)], MOSS)                        # mossy top
    for sd in (-1, 1):
        m.box(sd * 1.0 - 0.5, y0 + 2.2, -2.46, sd * 1.0 + 0.5, y0 + 3.0, -2.4, W)        # eyes
        m.box(sd * 1.0 - 0.2, y0 + 2.3, -2.5, sd * 1.0 + 0.2, y0 + 2.7, -2.46, K)
        m.box(sd * 1.4 - 0.45, y0, -4.0, sd * 1.4 + 0.45, y0 + 0.5, -2.4, NOSE)          # big feet
        m.box(min(sd * 2.4, sd * 3.8), y0 + 1.6, -0.15, max(sd * 2.4, sd * 3.8), y0 + 1.9, 0.15, BKD,
              rot=('z', 22.5 * sd, (sd * 2.4, y0 + 1.6, 0)))                              # twig arms
    rbox(m, -0.7, y0 + 1.0, -3.8, 0.7, y0 + 2.3, -2.4, NOSE, r=0.3)                      # big nose
    m.box(-0.8, y0 + 0.5, -2.46, 0.8, y0 + 0.7, -2.4, K)

@design("cappuccino_assassino", "Cappuccino Assassino", "trend")
def _(m):
    CUP, COF, FOAM, K, RD = '#f4f2ee', '#7a4a26', '#f0d9b5', '#1d1b22', '#c8312d'
    y0 = 4.6
    for sd in (-1, 1):                                                                  # crossed katanas on the back
        r = ('z', 45 * sd, (0, y0 + 2.0, 2.1))
        m.box(-0.15, y0 - 0.6, 1.95, 0.15, y0 + 3.2, 2.15, '#d8dde6', rot=r)
        m.box(-0.2, y0 + 3.2, 1.95, 0.2, y0 + 4.6, 2.15, '#3a1f2b', rot=r)
        m.box(-0.45, y0 + 3.0, 1.9, 0.45, y0 + 3.2, 2.2, GOLD, rot=r)
    rbox(m, -1.8, y0, -1.8, 1.8, y0 + 3.0, 1.8, CUP, r=0.4)                             # cup
    m.box(-1.5, y0 + 2.95, -1.5, 1.5, y0 + 3.05, 1.5, COF)
    m.box(-0.5, y0 + 3.05, -0.5, 0.5, y0 + 3.1, 0.5, FOAM)
    m.box(-1.86, y0 + 1.4, -1.86, 1.86, y0 + 2.4, 1.86, K)                              # ninja mask
    for sd in (-1, 1):
        m.box(sd * 0.7 - 0.4, y0 + 1.6, -1.92, sd * 0.7 + 0.4, y0 + 1.95, -1.86, W)     # eyes
        m.box(sd * 0.7 - 0.12, y0 + 1.6, -1.94, sd * 0.7 + 0.12, y0 + 1.9, -1.92, K)
        m.box(sd * 0.25, y0 + 2.05, -1.93, sd * 1.15, y0 + 2.2, -1.86, RD, rot=('z', -22.5 * sd, (sd * 0.25, y0 + 2.1, -1.9)))   # angry brows
        m.box(sd * 0.3 - 0.2, y0 + 1.8, 1.86, sd * 0.3 + 0.2, y0 + 2.2, 3.4, RD)        # headband tails
    rbox(m, 1.8, y0 + 0.6, -0.3, 2.6, y0 + 2.4, 0.3, CUP, r=0.2)                        # handle
    m.box(-0.5, y0, -1.86, 0.5, y0 + 0.25, -1.8, '#e0d8cc')
W = WHITE

# ---------- more goofy ----------
@design("lightbulb_idea", "Lightbulb Idea", "goofy")
def _(m):
    import math
    BULB, GR = '#fff4a0', '#9a9ca6'
    m.box(-0.9, 6.2, -0.9, 0.9, 7.2, 0.9, GR)                                           # screw base
    for y in (6.4, 6.8):
        m.box(-0.95, y, -0.95, 0.95, y + 0.15, 0.95, '#6e7078')
    rbox(m, -1.5, 7.1, -1.5, 1.5, 9.8, 1.5, BULB, r=0.6)
    rbox(m, -1.0, 9.6, -1.0, 1.0, 10.3, 1.0, BULB, r=0.3)
    m.box(-0.5, 8.0, -1.55, 0.5, 8.15, -1.5, '#ffb71f')                                 # filament
    for k in range(7):                                                                  # rays
        a = math.pi * (0.1 + 0.8 * k / 6); x, y = 2.6 * math.cos(a), 8.6 + 2.6 * math.sin(a) * 0.8
        m.box(x - 0.18, y - 0.18, -0.2, x + 0.18, y + 0.18, 0.2, '#ffe45c')

@design("fishbowl_helmet", "Fishbowl Helmet", "goofy")
def _(m):
    m.box(-4.6, 4.6, -4.6, 4.6, 6.0, 4.6, '#5fb8f060')                                  # water on top
    for (x, z, c) in ((-1.6, -2.0, '#ff8a2a'), (1.8, 1.4, '#ffd84a')):                  # fish
        m.box(x - 0.8, 6.2, z - 0.35, x + 0.6, 7.0, z + 0.35, c)
        m.box(x + 0.6, 6.3, z - 0.2, x + 1.2, 6.9, z + 0.2, c)
        m.box(x - 0.55, 6.6, z - 0.4, x - 0.35, 6.8, z - 0.35, '#1d1b22')
    for x, y in ((-2.6, 7.6), (-2.2, 8.4), (2.4, 7.9)):
        m.box(x - 0.2, y, -1.0, x + 0.2, y + 0.4, -0.6, '#e6f6ffb0')                    # bubbles
    m.box(-0.5, 4.6, 0.4, 0.5, 5.6, 1.4, '#4cc34a')                                     # seaweed
    m.box(-0.3, 5.6, 0.6, 0.3, 6.4, 1.2, '#4cc34a')
    m.box(-5.0, -5.0, -5.0, 5.0, 8.6, 5.0, '#cfeeff38')                                 # glass bowl
    ring(m, 8.6, 4.4, '#e6f6ffc0', t=0.6, h=0.4)

@design("ice_cream_splat", "Ice Cream Splat", "goofy")
def _(m):
    PK, PKD, CONE, CONED = '#ffb3cf', '#f08cb0', '#e3a85a', '#b87a34'
    dome(m, 4.0, [(4.5, 0.8), (3.6, 0.6)], PK)                                          # squished scoop
    for x, y2 in ((-2.6, 1.6), (0.6, 2.8), (2.8, 2.0)):                                 # drips on forehead
        m.box(x - 0.45, y2, -4.6, x + 0.45, 4.6, -4.2, PK)
        m.box(x - 0.55, y2 - 0.4, -4.65, x + 0.55, y2 + 0.2, -4.2, PK)
    for sd in (-1, 1):
        for z, y2 in ((-1.6, 0.4), (2.0, 1.8)):
            m.box(min(sd * 4.2, sd * 4.6), y2, z - 0.45, max(sd * 4.2, sd * 4.6), 4.6, z + 0.45, PK)
    steps(m, 0, 0, 5.3, [3.0, 2.6, 2.2, 1.8, 1.4, 1.0, 0.6], CONE, h=0.8, smooth=1)    # upside-down cone
    for y in (5.9, 7.1, 8.3):
        m.box(-1.6, y, -1.6, 1.6, y + 0.12, 1.6, CONED)
    for x, z, c in ((-2.8, -2.0, '#4cc3ff'), (2.4, -2.6, '#ffe45c'), (-1.6, 2.6, '#7af08a'), (3.0, 1.4, '#ff5c5c'), (-3.4, 0.8, '#ffe45c')):
        m.box(x - 0.3, 5.4, z - 0.1, x + 0.3, 5.5, z + 0.1, c)                          # sprinkles

@design("spaghetti_hair", "Spaghetti Hair", "goofy")
def _(m):
    PL, ND, NDD, SC, MB = '#f4f2ee', '#f0d27a', '#d9b45a', '#c8312d', '#6b3a22'
    rbox(m, -4.4, 4.0, -4.4, 4.4, 4.6, 4.4, PL, r=1.2, top=False)                       # plate
    dome(m, 4.6, [(3.2, 0.8), (2.4, 0.7), (1.4, 0.5)], ND)                              # pasta pile
    for x, z in ((-2.0, -1.0), (1.0, 1.8), (0.4, -2.4)):
        m.box(x - 0.8, 5.4, z - 0.08, x + 0.8, 5.48, z + 0.08, NDD)
    dome(m, 6.1, [(1.6, 0.4), (0.9, 0.3)], SC)                                          # sauce
    for x, y, z in ((-0.5, 6.5, -0.5), (1.6, 5.4, -1.6), (-1.9, 5.3, 1.2)):
        rbox(m, x - 0.6, y, z - 0.6, x + 0.6, y + 1.1, z + 0.6, MB, r=0.3)              # meatballs
    m.box(0.2, 6.85, 0.2, 1.0, 6.95, 0.7, '#3f8f3a')                                    # basil
    for x, y1 in ((-3.0, 1.2), (-1.0, 2.4), (2.4, 0.8)):                                # noodles dangling in the face
        m.box(x - 0.15, y1, -4.75, x + 0.15, 4.6, -4.45, ND)
        m.box(x - 0.15 + 0.3, y1 - 0.6, -4.75, x + 0.15 + 0.3, y1 + 0.3, -4.45, ND)
    for sd in (-1, 1):
        for z, y1 in ((-2.0, -1.6), (1.2, 0.0), (3.2, -0.8)):
            m.box(min(sd * 4.45, sd * 4.75), y1, z - 0.15, max(sd * 4.45, sd * 4.75), 4.6, z + 0.15, ND)

@design("lampshade", "Lampshade", "goofy")
def _(m):
    SH, SHD, TS = '#f3e3b8', '#d9c48e', '#c9a96a'
    steps(m, 0, 0, 2.2, [10.4, 9.6, 8.8, 8.0, 7.2, 6.4], SH, h=1.0, smooth=2)
    m.box(-5.25, 2.2, -5.25, 5.25, 2.5, 5.25, SHD)
    for i in range(10):                                                                 # tassel fringe
        t = -4.6 + i * 1.0
        for (x, z) in ((t, -5.25), (t, 5.25), (-5.25, t), (5.25, t)):
            m.box(x - 0.15, 1.4, z - 0.15, x + 0.15, 2.2, z + 0.15, TS)
    m.box(-2.8, 8.0, -2.8, 2.8, 8.3, 2.8, SHD)
    m.box(-0.4, 8.3, -0.4, 0.4, 9.0, 0.4, '#b8861c')                                    # finial

@design("rubber_chicken", "Rubber Chicken", "goofy")
def _(m):
    Y, YD, K = '#f7dc3c', '#d9b821', '#1d1b22'
    r = ('y', 22.5, (0, 0, 0))
    rbox(m, -3.4, 4.6, -0.9, 1.8, 6.0, 0.9, Y, r=0.4, rot=r)                            # body
    m.box(1.6, 5.0, -0.4, 4.0, 5.6, 0.4, Y, rot=r)                                      # floppy neck
    rbox(m, 3.8, 4.8, -0.7, 5.4, 6.4, 0.7, Y, r=0.3, rot=r)                             # head
    m.box(5.4, 5.3, -0.3, 6.4, 5.8, 0.3, ORANGE, rot=r)                                 # beak
    m.box(4.2, 6.4, -0.15, 5.2, 7.1, 0.15, RED, rot=r)                                  # comb
    m.box(4.6, 4.5, -0.15, 5.0, 4.9, 0.15, RED, rot=r)
    for sd in (-1, 1):
        z = sd * 0.72
        m.box(4.4, 5.6, z - 0.03, 5.0, 5.75, z + 0.03, K, rot=r)                        # X eyes
        m.box(4.625, 5.375, z - 0.03, 4.775, 5.975, z + 0.03, K, rot=r)
        m.box(-0.9, 5.2, sd * 0.9 - 0.05, 0.6, 5.7, sd * 0.9 + 0.05, YD, rot=r)          # wings
    for z in (-0.4, 0.4):
        m.box(-2.6, 6.0, z - 0.15, -2.3, 7.4, z + 0.15, ORANGE, rot=r)                   # legs up
        m.box(-2.9, 7.4, z - 0.3, -2.0, 7.6, z + 0.3, ORANGE, rot=r)
    m.box(-4.2, 5.4, -0.5, -3.4, 6.4, 0.5, YD, rot=r)                                   # tail

@design("cone_of_shame", "Cone of Shame", "goofy")
def _(m):
    for i in range(5):
        h = 4.75 + 0.5 * i; t = 0.5; z2 = 1.0 - 0.8 * i; z1 = z2 - 0.8; cy = -0.5
        c = '#eef4ff90' if i < 4 else '#cfd8e6'
        m.box(-h, cy + h - t, z1, h, cy + h, z2, c); m.box(-h, cy - h, z1, h, cy - h + t, z2, c)
        m.box(-h, cy - h + t, z1, -h + t, cy + h - t, z2, c); m.box(h - t, cy - h + t, z1, h, cy + h - t, z2, c)
    for x in (-3.0, 3.0):
        m.box(x - 0.4, -0.5 + 4.75 - 0.6, 0.95, x + 0.4, -0.5 + 4.75, 1.05, '#9aa6b8')

@design("pancake_stack", "Pancake Stack", "goofy")
def _(m):
    PC, PCL, SY, BT = '#d9954a', '#f0c27a', '#8b3f0e', '#fff0a0'
    y = 4.6
    for i, off in enumerate((0.0, 0.3, -0.25, 0.15)):
        rbox(m, -3.0 + off, y, -3.0 - off, 3.0 + off, y + 0.7, 3.0 - off, PC, r=1.0)
        m.box(-2.4 + off, y + 0.1, -3.05 - off, 2.4 + off, y + 0.25, 3.05 - off, PCL)
        y += 0.7
    rbox(m, -2.4, y - 0.05, -2.4, 2.4, y + 0.08, 2.4, SY, r=0.8)                        # syrup
    for x, z, d in ((-1.8, -2.95, 1.2), (1.2, -2.85, 2.0), (2.9, 0.8, 1.4)):
        m.box(x - 0.3, y - d, z - 0.1, x + 0.3, y, z + 0.1, SY)                          # drips
    m.box(-0.7, y, -0.7, 0.7, y + 0.6, 0.7, BT)                                          # butter
    m.box(1.6, y - 0.3, 0.8, 1.8, y + 3.6, 1.0, SILVER, rot=('z', -22.5, (1.7, y, 0.9)))  # fork stuck in
    for dx in (-0.25, 0.0, 0.25):
        m.box(1.65 + dx, y + 3.6, 0.82, 1.75 + dx, y + 4.4, 0.98, SILVER, rot=('z', -22.5, (1.7, y, 0.9)))

@design("bird_nest", "Bird Nest", "goofy")
def _(m):
    HAY, BL, BLD, OR = '#c9a96a', '#4a8fd8', '#2f63a8', '#f2a03a'
    m.box(-2.6, 4.6, -2.6, 2.6, 4.9, 2.6, HAY)
    ring(m, 4.6, 3.6, BROWN, t=1.2, h=0.9)
    ring(m, 5.3, 3.3, BROWN_D, t=0.9, h=0.6)
    for (x, z, ax, a) in ((-3.6, -1.0, 'z', 22.5), (3.4, 1.6, 'z', -45), (1.0, 3.6, 'x', 22.5), (-1.4, 3.4, 'x', -45)):
        m.box(x - 0.12, 5.2, z - 0.12, x + 0.12, 6.6, z + 0.12, BROWN, rot=(ax, a, (x, 5.2, z)))   # loose twigs
    for x, z in ((-0.9, 0.6), (0.9, 0.9), (0.1, 1.8)):
        rbox(m, x - 0.5, 4.9, z - 0.45, x + 0.5, 6.0, z + 0.45, '#a8d8e8', r=0.2)        # eggs
        m.box(x - 0.2, 5.6, z - 0.47, x - 0.05, 5.75, z - 0.45, '#6a9aa8')
    # little bluebird on the front rim
    rbox(m, -0.9, 6.1, -3.7, 0.9, 7.6, -1.9, BL, r=0.4)
    rbox(m, -0.7, 7.4, -3.6, 0.7, 8.6, -2.3, BL, r=0.3)
    m.box(-0.6, 6.3, -3.76, 0.6, 7.3, -3.7, '#ffd9b0')                                  # chest
    m.box(-0.25, 7.8, -4.1, 0.25, 8.1, -3.6, OR)
    for sd in (-1, 1):
        m.box(sd * 0.35 - 0.12, 8.1, -3.66, sd * 0.35 + 0.12, 8.35, -3.6, BLACK)
        m.box(min(sd * 0.9, sd * 1.05), 6.4, -3.4, max(sd * 0.9, sd * 1.05), 7.4, -2.0, BLD)
    m.box(-0.5, 6.6, -1.9, 0.5, 7.0, -1.0, BLD)                                         # tail

@design("hot_dog_hat", "Hot Dog Hat", "goofy")
def _(m):
    BUN, BUND, DOG, MU = '#e9b46a', '#c98a3e', '#c4553a', '#f7d21f'
    for z1, z2 in ((-1.8, -0.3), (0.3, 1.8)):
        rbox(m, -4.2, 4.6, z1, 4.2, 6.0, z2, BUN, r=0.5)
        m.box(-3.8, 5.95, z1 + 0.2, 3.8, 6.05, z2 - 0.2, BUND)
    rbox(m, -5.2, 5.2, -0.7, 5.2, 6.5, 0.7, DOG, r=0.5)                                 # sausage
    for i in range(9):                                                                  # mustard zigzag
        x = -4.0 + i * 1.0; z = -0.3 if i % 2 else 0.1
        m.box(x - 0.1, 6.5, z, x + 1.0, 6.65, z + 0.2, MU)

@design("pizza_slice", "Pizza Slice", "goofy")
def _(m):
    CH, CHD, SC, CR, PEP = '#f6c94a', '#e0a93a', '#c8312d', '#d99a4a', '#b8352d'
    n = 16
    for k in range(n):
        w = 7.2 - 6.6 * k / (n - 1); z2 = 2.6 - 0.5 * k
        m.box(-w / 2, 4.6, z2 - 0.5, w / 2, 4.75, z2, SC)
        m.box(-w / 2 + 0.1, 4.75, z2 - 0.5, w / 2 - 0.1, 5.0, z2, CH)
    rbox(m, -3.8, 4.6, 2.6, 3.8, 5.6, 3.6, CR, r=0.4)                                   # crust
    for x, z in ((-1.6, 1.2), (1.4, 0.8), (0.0, -1.2), (-0.3, -3.4), (1.6, 2.0)):
        m.box(x - 0.55, 5.0, z - 0.55, x + 0.55, 5.1, z + 0.55, PEP)
    m.box(-0.3, 2.4, -5.2, 0.3, 4.75, -4.9, CH)                                         # cheese drip off the tip
    m.box(-0.4, 2.0, -5.25, 0.4, 2.6, -4.85, CHD)

@design("snorkel_mask", "Snorkel Mask", "goofy")
def _(m):
    FR, LN, ST, TB = '#1f6f8b', '#bfeff2a0', '#24262b', '#ff8a2a'
    m.box(-4.6, -0.8, -4.0, -4.0, 0.2, 4.6, ST); m.box(4.0, -0.8, -4.0, 4.6, 0.2, 4.6, ST)   # strap
    m.box(-4.6, -0.8, 4.0, 4.6, 0.2, 4.6, ST)
    m.box(-3.6, 0.8, -5.2, 3.6, 1.4, -4.0, FR); m.box(-3.6, -2.2, -5.2, 3.6, -1.6, -4.0, FR)   # frame
    for sd in (-1, 1):
        m.box(min(sd * 3.0, sd * 3.6), -1.6, -5.2, max(sd * 3.0, sd * 3.6), 0.8, -4.0, FR)
    m.box(-0.6, -2.6, -5.2, 0.6, -1.6, -4.0, FR)                                        # nose pocket
    m.box(-3.0, -1.6, -4.9, 3.0, 0.8, -4.8, LN)                                         # lens
    m.box(-2.6, 0.1, -4.95, -1.6, 0.5, -4.9, '#ffffffcc')
    m.box(4.6, -2.6, -1.0, 5.4, 7.0, -0.2, TB)                                          # tube
    m.box(4.55, 6.0, -1.05, 5.45, 7.0, -0.15, '#e8343f')
    m.box(1.0, -3.0, -4.9, 5.4, -2.2, -4.1, TB)                                         # bend to mouth
    m.box(4.6, -3.0, -4.1, 5.4, -2.2, -1.0, TB)
    m.box(0.2, -3.4, -5.1, 1.2, -1.8, -4.1, ST)                                         # mouthpiece

@design("angler_light", "Angler Light", "goofy")
def _(m):
    ST, FIN, GL = '#3a5a6b', '#2a4250', '#a6ffef'
    m.box(-0.15, 4.6, 0.6, 0.15, 6.2, 3.6, FIN)                                         # head fin
    for z in (1.2, 2.2, 3.0):
        m.box(-0.1, 6.2, z, 0.1, 6.8, z + 0.25, FIN)
    m.box(-0.2, 4.6, -0.2, 0.2, 7.8, 0.2, ST)                                           # lure stalk
    m.box(-0.2, 7.4, -4.4, 0.2, 7.8, -0.2, ST)
    m.box(-0.2, 6.4, -4.6, 0.2, 7.8, -4.2, ST)
    rbox(m, -0.8, 4.8, -5.2, 0.8, 6.4, -3.6, GL, r=0.4)                                 # glowing bulb
    m.box(-1.2, 4.4, -5.6, 1.2, 6.8, -3.2, '#a6ffef40')

@design("silly_goose", "Silly Goose", "goofy")
def _(m):
    OR, K, MO, GY = '#ff8a2a', '#1d1b22', '#e85a6a', '#d0d0d6'
    for sd in (-1, 1):
        m.box(sd * 0.8 - 0.5, 4.6, -1.8, sd * 0.8 + 0.5, 4.85, -0.6, OR)                # feet
    rbox(m, -1.8, 4.6, -1.0, 1.8, 6.8, 3.4, WHITE, r=0.7)                               # body
    steps(m, 0, 3.0, 6.4, [1.6, 1.0, 0.5], WHITE, h=0.7, smooth=1, dz=0.4)              # tail up
    for sd in (-1, 1):
        m.box(min(sd * 1.8, sd * 1.9), 5.4, -0.2, max(sd * 1.8, sd * 1.9), 6.4, 2.8, GY)  # wings
    m.box(-0.6, 6.4, -1.4, 0.6, 9.2, -0.2, WHITE)                                       # long neck
    rbox(m, -0.8, 8.8, -2.6, 0.8, 10.0, -0.2, WHITE, r=0.3)                             # head
    m.box(-0.4, 9.3, -3.9, 0.4, 9.7, -2.6, OR)                                          # open beak (HONK)
    m.box(-0.35, 8.8, -3.6, 0.35, 9.05, -2.6, OR)
    m.box(-0.3, 9.05, -3.2, 0.3, 9.3, -2.6, MO)
    for sd in (-1, 1):
        m.box(sd * 0.45 - 0.22, 9.45, -2.66, sd * 0.45 + 0.22, 9.85, -2.6, K)           # wide eyes
        m.box(sd * 0.45 - 0.1 + 0.05, 9.7, -2.68, sd * 0.45 + 0.05, 9.82, -2.66, WHITE)
    for x, y in ((-1.4, 9.8), (1.4, 9.8), (0.0, 10.6)):
        m.box(x - 0.1, y, -4.2, x + 0.1, y + 0.5, -4.0, '#ffe45c')                      # honk lines


# ======================================================================
# BATCH 4: Lunar-style headbands, dreads, cuter turtles, more buddies
# ======================================================================
def wrap(m, u, du, y1, y2, c, r=4.6, t=0.06):
    """Paint a patch on the outside of a ring at perimeter position u (0 = front-left corner, clockwise seen from above)."""
    L = 2 * r
    seg, s = int(u // L) % 4, u % L
    a, b = -r + s, min(r, -r + s + du)
    if seg == 0:   m.box(a, y1, -r - t, b, y2, -r, c)
    elif seg == 1: m.box(r, y1, a, r + t, y2, b, c)
    elif seg == 2: m.box(-b, y1, r, -a, y2, r + t, c)
    else:          m.box(-r - t, y1, -b, -r, y2, -a, c)

def headband(m, base, tail=None, y1=1.5, y2=2.9, tails=True):
    band(m, y1, y2, base, 4.6)
    if tails:
        tail = tail or base
        kx = 1.6
        m.box(kx - 0.65, y1 - 0.1, 4.6, kx + 0.65, y2 + 0.1, 5.25, tail)                  # knot at the back
        for dx, a, ln in ((-0.35, -22.5, 3.2), (0.45, -45, 3.6)):                        # two tails flowing back
            x = kx + dx
            m.box(x - 0.38, y1 - ln, 5.0, x + 0.38, y1 + 0.3, 5.28, tail, rot=('x', a, (x, y1 + 0.3, 5.1)))

def hb_dots(m, cols, y1, y2, step, w, seed, h=None):
    import random as _r
    rnd = _r.Random(seed); u = 0.2
    while u < 36.6:
        yy = rnd.uniform(y1, y2 - (h or w))
        wrap(m, u, w, yy, yy + (h or w), rnd.choice(cols))
        u += step * rnd.uniform(0.7, 1.3)

@design("headband_red", "Red Headband", "lunar")
def _(m):
    headband(m, '#c8312d', '#a8231f')
    for u in range(0, 36, 1):
        wrap(m, u + 0.2, 0.5, 1.65, 1.75, '#f4f2ee'); wrap(m, u + 0.2, 0.5, 2.65, 2.75, '#f4f2ee')   # stitching

@design("headband_black", "Black Headband", "lunar")
def _(m):
    headband(m, '#1d1b22', '#2c2a33')
    for u in range(0, 36, 1):
        wrap(m, u + 0.2, 0.5, 1.65, 1.75, '#5a5862'); wrap(m, u + 0.2, 0.5, 2.65, 2.75, '#5a5862')
    m.box(-0.5, 1.9, -4.7, 0.5, 2.5, -4.6, '#c9ced8', rot=('z', 45, (0, 2.2, -4.65)))   # small diamond badge

@design("headband_aconite", "Aconite Headband", "lunar")
def _(m):
    headband(m, AC, AC_DARK)
    hb_dots(m, [AC_LIGHT, AC_GLOW], 1.7, 2.7, 1.4, 0.25, 3)
    m.box(-1.0, 1.6, -4.72, 1.0, 2.8, -4.6, AC_DARK)
    aconite_spike(m, 0, 1.75, -4.9, h=2, s=0.45)

@design("headband_rainbow", "Rainbow Headband", "lunar")
def _(m):
    cols = ['#e8343f', '#f2a03a', '#f7dc3c', '#4cc34a', '#2f8fe0', '#8a55d6']
    for i, c in enumerate(cols):
        band(m, 2.9 - (i + 1) * 0.233, 2.9 - i * 0.233, c, 4.6)
    headband(m, '#8a55d6', '#e8343f', tails=True) if False else None
    kx = 1.6
    m.box(kx - 0.65, 1.4, 4.6, kx + 0.65, 3.0, 5.25, '#f7dc3c')
    for (dx, a, ln, c) in ((-0.35, -22.5, 3.2, '#e8343f'), (0.45, -45, 3.6, '#2f8fe0')):
        x = kx + dx
        m.box(x - 0.38, 1.5 - ln, 5.0, x + 0.38, 1.8, 5.28, c, rot=('x', a, (x, 1.8, 5.1)))

@design("headband_flame", "Flame Headband", "lunar")
def _(m):
    headband(m, '#1d1b22', '#ff8a1f')
    u = 0.1
    while u < 36.6:
        h = 0.55 if int(u * 2) % 2 else 0.95
        wrap(m, u, 0.5, 1.5, 1.5 + h, '#ff5a1f')
        wrap(m, u + 0.1, 0.3, 1.5, 1.5 + h * 0.55, '#ffc21f', t=0.1)
        u += 0.6

@design("headband_galaxy", "Galaxy Headband", "lunar")
def _(m):
    headband(m, '#1a1240', '#2a1a5a')
    hb_dots(m, ['#3a2a8a', '#4a2a7a'], 1.5, 2.9, 1.1, 0.9, 9, h=0.6)
    hb_dots(m, ['#ffffff', '#ff9fd2', '#7af7ff', '#ffe45c'], 1.6, 2.8, 0.7, 0.15, 5)
    star(m, 0, 2.2, -4.6, 0.32, '#ffe45c')

@design("headband_camo", "Camo Headband", "lunar")
def _(m):
    headband(m, '#5a6b3a', '#4a5a30')
    hb_dots(m, ['#3d4a28', '#8a8a5a', '#2e3520'], 1.5, 2.9, 0.9, 0.8, 11, h=0.55)

@design("headband_checker", "Checker Headband", "lunar")
def _(m):
    headband(m, '#f4f2ee', '#1d1b22')
    for k in range(int(36.8 / 0.7)):
        for row in range(2):
            if (k + row) % 2:
                wrap(m, k * 0.7, 0.7, 1.5 + row * 0.7, 2.2 + row * 0.7, '#1d1b22')

@design("headband_hearts", "Heart Headband", "lunar")
def _(m):
    headband(m, '#f7a8c8', '#f08cb0')
    for x in (-3.0, -0.0, 3.0):
        heart(m, x, 1.75, -4.6, 0.2, '#e8345f', t=0.08)
    for z in (-2.0, 1.0):
        for sd in (-1, 1):
            m.box(sd * 4.6 - 0.04, 1.95, z - 0.25, sd * 4.6 + 0.04, 2.45, z + 0.25, '#e8345f')

@design("headband_sakura", "Sakura Headband", "lunar")
def _(m):
    headband(m, '#fff4f7', '#f7c8d8')
    for x in (-3.2, -1.1, 1.1, 3.2):
        flower(m, x, 2.2, -4.6, '#f7a8c8', '#fff0a0', s=0.45)
    for sd in (-1, 1):
        for z in (-2.2, 0.4, 2.8):
            m.box(sd * 4.6 - 0.05, 2.0, z - 0.3, sd * 4.6 + 0.05, 2.4, z + 0.3, '#f7a8c8')

@design("headband_ninja", "Ninja Plate Headband", "lunar")
def _(m):
    headband(m, '#22283a', '#1a1f2e')
    m.box(-1.9, 1.55, -4.75, 1.9, 2.85, -4.6, '#c9ced8')                               # metal plate
    m.box(-1.9, 1.55, -4.77, 1.9, 1.65, -4.75, '#8c8f99'); m.box(-1.9, 2.75, -4.77, 1.9, 2.85, -4.75, '#8c8f99')
    for (x1, y1, x2, y2) in ((-0.8, 1.85, 0.8, 1.95), (0.7, 1.85, 0.8, 2.55), (-0.5, 2.45, 0.8, 2.55),
                             (-0.5, 2.1, -0.4, 2.55), (-0.5, 2.1, 0.4, 2.2)):
        m.box(x1, y1, -4.79, x2, y2, -4.75, '#5a5d66')                                 # engraved swirl
    for x in (-1.6, 1.6):
        m.box(x - 0.1, 2.1, -4.79, x + 0.1, 2.3, -4.75, '#5a5d66')

@design("sweatband", "Retro Sweatband", "lunar")
def _(m):
    band(m, 1.4, 3.0, '#f4f2ee', 4.6)
    band(m, 1.75, 1.95, '#e8343f', 4.68); band(m, 2.45, 2.65, '#2f5fd0', 4.68)
    hb_dots(m, ['#e6e2da'], 1.45, 2.95, 0.5, 0.12, 4)

# ear / bopper headbands (thin band over the top)
def top_band(m, c, z=-1.0, t=0.6):
    m.box(-4.6, 4.0, z - t / 2, 4.6, 4.5, z + t / 2, c)
    for sd in (-1, 1):
        m.box(min(sd * 4.0, sd * 4.6), 0.4, z - t / 2, max(sd * 4.0, sd * 4.6), 4.5, z + t / 2, c)

@design("cat_ear_headband", "Cat Ear Headband", "lunar")
def _(m):
    top_band(m, '#1d1b22')
    for sd in (-1, 1):
        steps(m, sd * 2.6, -1.0, 4.6, [2.4, 1.8, 1.2, 0.6], '#1d1b22', depth=0.7, h=0.8, dx=sd * 0.2)
        steps(m, sd * 2.6, -1.4, 4.6, [1.4, 0.9, 0.4], '#f7a8c8', depth=0.1, h=0.7, dx=sd * 0.2)

@design("bunny_ear_headband", "Bunny Ear Headband", "lunar")
def _(m):
    W, P = '#f4f2ee', '#f7a8c8'
    top_band(m, W)
    for sd in (-1, 1):
        r = ('z', -22.5 * sd, (sd * 1.6, 4.6, -1.0))
        rbox(m, sd * 1.6 - 0.8, 4.6, -1.35, sd * 1.6 + 0.8, 10.0, -0.65, W, r=0.3, rot=r)
        m.box(sd * 1.6 - 0.4, 5.2, -1.4, sd * 1.6 + 0.4, 9.4, -1.35, P, rot=r)
    m.box(-0.8, 4.5, -1.5, 0.8, 5.3, -0.5, P)                                           # little bow
    m.box(-0.25, 4.6, -1.55, 0.25, 5.2, -0.45, '#e8789a')

@design("devil_headband", "Devil Horn Headband", "lunar")
def _(m):
    R, RD = '#d62828', '#8a1414'
    top_band(m, '#1d1b22')
    for sd in (-1, 1):
        steps(m, sd * 2.5, -1.0, 4.6, [1.6, 1.2, 0.8, 0.4], R, h=0.8, dx=sd * 0.5)
        m.box(sd * 2.5 + sd * 0.35 - 0.3, 4.6, -1.65, sd * 2.5 + sd * 0.35 + 0.3, 5.0, -1.55, RD)

@design("heart_boppers", "Heart Boppers", "lunar")
def _(m):
    top_band(m, '#f7a8c8')
    for sd in (-1, 1):
        x = sd * 2.2
        for k in range(5):                                                              # springy stalk
            m.box(x + (0.15 if k % 2 else -0.15) - 0.12, 4.6 + k * 0.6, -1.12, x + (0.15 if k % 2 else -0.15) + 0.12, 5.2 + k * 0.6, -0.88, '#c9ced8')
        heart(m, x, 7.5, -0.7, 0.32, '#e8345f', t=0.6, hi='#ffffff')

# face bandanas
def face_bandana(m, base, dot):
    m.box(-4.6, -4.4, -4.6, 4.6, -1.3, -4.0, base)                                      # over nose + mouth
    for i, w in enumerate((8.0, 6.0, 4.0, 2.0)):                                        # triangle point below chin
        m.box(-w / 2, -4.4 - (i + 1) * 0.5, -4.6, w / 2, -4.4 - i * 0.5, -4.1, base)
    for sd in (-1, 1):
        m.box(min(sd * 4.0, sd * 4.6), -2.6, -4.6, max(sd * 4.0, sd * 4.6), -1.3, 4.6, base)
    m.box(-4.6, -2.6, 4.0, 4.6, -1.3, 4.6, base)
    m.box(-0.6, -3.0, 4.6, 0.6, -1.0, 5.2, base)                                        # knot
    m.box(-0.5, -4.6, 4.9, 0.0, -2.8, 5.15, base); m.box(0.1, -4.4, 4.9, 0.55, -2.8, 5.15, base)
    import random as _r
    rnd = _r.Random(2)
    for _ in range(14):
        x, y = rnd.uniform(-4.2, 3.8), rnd.uniform(-4.2, -1.8)
        m.box(x, y, -4.66, x + 0.3, y + 0.3, -4.6, dot)
    for x in (-1.2, 0.0, 1.2):
        m.box(x - 0.15, -5.5, -4.66, x + 0.15, -5.2, -4.6, dot)

@design("bandana_mask_red", "Red Bandana Mask", "lunar")
def _(m): face_bandana(m, '#c8312d', '#f4f2ee')

@design("bandana_mask_black", "Black Bandana Mask", "lunar")
def _(m): face_bandana(m, '#1d1b22', '#c9ced8')

# ---------- dreads ----------
def dreads(m, c1, c2, tip=None, bead=None, seed=1, length=1.0, updo=False):
    import random as _r
    rnd = _r.Random(seed)
    dome(m, 4.0, [(4.6, 0.5)], c1)                                                      # hair cap
    m.box(-4.6, 3.4, -4.6, 4.6, 4.6, -4.0, c1)                                          # hairline
    dome(m, 4.5, [(4.1, 0.35), (3.2, 0.3)], c2)
    for _ in range(9):                                                                  # a few loose root lumps
        x, z = rnd.uniform(-3.4, 3.4), rnd.uniform(-3.4, 3.4)
        rbox(m, x - 0.6, 4.6, z - 0.6, x + 0.6, 5.35, z + 0.6, rnd.choice((c1, c2)), r=0.3)
    def strand(cx, cz, y_top, y_bot, w=0.7, ax=None):
        h = w / 2
        x1, x2, z1, z2 = cx - h, cx + h, cz - h, cz + h
        col = rnd.choice((c1, c1, c2))
        m.box(x1, y_bot + 0.6, z1, x2, y_top, z2, col, rot=ax)
        m.box(x1 + 0.1, y_bot, z1 + 0.1, x2 - 0.1, y_bot + 0.6, z2 - 0.1, tip or col, rot=ax)   # tapered end
        if tip:
            m.box(x1 - 0.02, y_bot + 0.6, z1 - 0.02, x2 + 0.02, y_bot + 1.3, z2 + 0.02, tip, rot=ax)
        for _ in range(2):
            y = rnd.uniform(y_bot + 1.4, y_top - 1.0)
            m.box(x1 - 0.05, y, z1 - 0.05, x2 + 0.05, y + 0.35, z2 + 0.05, c2 if col == c1 else c1, rot=ax)   # twist bumps
        if bead and rnd.random() < 0.4:
            yb = rnd.uniform(y_bot + 1.0, y_top - 2.0)
            m.box(x1 - 0.12, yb, z1 - 0.12, x2 + 0.12, yb + 0.5, z2 + 0.12, bead, rot=ax)
    if updo:                                                                            # high ponytail that falls down the back
        for ix in range(3):
            for iz in range(3):
                x, z = -0.8 + ix * 0.8, -0.4 + iz * 0.8
                strand(x, z, 7.8 + rnd.uniform(-0.2, 0.3), 4.8, w=0.75)
        m.box(-1.45, 5.4, -1.05, 1.45, 6.0, 1.85, bead or c2)                            # hair tie
        for i in range(6):
            x = -1.75 + i * 0.7
            strand(x, 0.6, 7.8, 7.8 - 5.6, w=0.7, ax=('x', -45, (x, 7.8, 0.6)))
            strand(x + 0.3, 4.95, 4.4, -2.6 + rnd.uniform(-0.8, 0.8), w=0.7)
        return
    for i in range(9):                                                                  # back
        strand(-4.0 + i * 1.0 + rnd.uniform(-0.1, 0.1), 5.0, 4.6, (-6.6 + rnd.uniform(-1.4, 1.4)) * length, w=0.82)
    for i in range(8):                                                                  # back outer layer
        strand(-3.5 + i * 1.0, 5.8, 4.2, (-5.4 + rnd.uniform(-1.4, 1.4)) * length, w=0.82)
    for sd in (-1, 1):
        for i in range(8):                                                              # sides
            strand(sd * 5.0, -3.5 + i * 1.08, 4.6, (-4.8 + rnd.uniform(-1.4, 1.4) - 0.15 * i) * length, w=0.82)
        for k, x in enumerate((3.9, 3.05)):                                             # face-framing locks
            strand(sd * x, -4.98, 4.6, (-3.4 - 1.2 * k + rnd.uniform(-0.4, 0.4)) * length)

@design("dreads_black", "Black Dreads", "hair")
def _(m): dreads(m, '#2a2222', '#45393a', seed=1)

@design("dreads_brown", "Brown Dreads", "hair")
def _(m): dreads(m, '#5a3720', '#7a4e2e', seed=2)

@design("dreads_blonde", "Blonde Tip Dreads", "hair")
def _(m): dreads(m, '#3a2818', '#55402a', tip='#e8c25a', seed=3)

@design("dreads_purple", "Purple Ombre Dreads", "hair")
def _(m): dreads(m, '#2a2230', '#433650', tip=AC_LIGHT, seed=4)

@design("dreads_beaded", "Beaded Dreads", "hair")
def _(m): dreads(m, '#3a2818', '#55402a', bead=GOLD, seed=5)

@design("dreads_updo", "Dread Updo", "hair")
def _(m): dreads(m, '#2a2222', '#45393a', bead=GOLD, seed=6, updo=True)

# ---------- cuter turtles ----------
T_SH, T_SHL, T_SK, T_BEL = '#3b8a3a', '#6cbd4b', '#a6d873', '#e9dca0'
def turtle(m, cx, y0, cz, s=1.0):
    def B(x1, y1, z1, x2, y2, z2, c):
        m.box(cx + x1 * s, y0 + y1 * s, cz + z1 * s, cx + x2 * s, y0 + y2 * s, cz + z2 * s, c)
    def R(x1, y1, z1, x2, y2, z2, c, r):
        rbox(m, cx + x1 * s, y0 + y1 * s, cz + z1 * s, cx + x2 * s, y0 + y2 * s, cz + z2 * s, c, r=r * s)
    for sd in (-1, 1):
        B(min(sd * 1.6, sd * 3.0), 0.0, -1.9, max(sd * 1.6, sd * 3.0), 0.4, -0.9, T_SK)   # front flippers
        B(min(sd * 1.5, sd * 2.5), 0.0, 1.5, max(sd * 1.5, sd * 2.5), 0.4, 2.4, T_SK)     # back flippers
    B(-2.0, 0.2, -1.8, 2.0, 0.6, 2.2, T_BEL)                                            # belly
    R(-2.2, 0.5, -2.0, 2.2, 1.9, 2.4, T_SH, 0.6)                                        # shell
    R(-1.6, 1.9, -1.4, 1.6, 2.5, 1.8, T_SH, 0.5)
    B(-2.25, 0.5, -2.05, 2.25, 0.75, 2.45, T_SHL)                                       # light rim
    B(-0.7, 2.5, -0.4, 0.7, 2.56, 0.8, T_SHL)                                           # scutes
    for x, z in ((-1.2, -0.9), (1.2, -0.9), (-1.2, 1.3), (1.2, 1.3)):
        B(x - 0.35, 1.9, z - 0.35, x + 0.35, 1.96, z + 0.35, T_SHL)
    R(-1.15, 0.5, -3.9, 1.15, 2.5, -1.7, T_SK, 0.45)                                    # big round head
    for sd in (-1, 1):
        B(sd * 0.5 - 0.28, 1.4, -3.96, sd * 0.5 + 0.28, 2.1, -3.9, '#1a1418')             # big eyes
        B(sd * 0.5 - 0.2 + 0.06, 1.8, -3.98, sd * 0.5 + 0.06, 2.02, -3.96, '#ffffff')
        B(sd * 0.88 - 0.2, 1.05, -3.95, sd * 0.88 + 0.2, 1.28, -3.9, '#ff9fb8')          # blush
    B(-0.3, 0.9, -3.95, 0.3, 1.02, -3.9, '#3a5a2a')                                     # smile
    B(-0.25, 0.5, 2.4, 0.25, 0.9, 3.0, T_SK)                                            # tail

@design("turtle_buddy", "Turtle Buddy", "cute")
def _(m): turtle(m, 0, 4.6, 0.2, 1.25)

@design("turtle_stack", "Turtle Stack", "cute")
def _(m):
    turtle(m, 0, 4.6, 0.2, 1.1)
    turtle(m, 0, 4.6 + 2.75, 0.4, 0.75)
    turtle(m, 0, 4.6 + 2.75 + 1.9, 0.5, 0.5)

@design("turtle_egg_hat", "Turtle Egg Nest", "cute")
def _(m):
    SAND, SANDD, EGG, SPOT = '#e8d9a0', '#d4c27f', '#f2efdc', '#6cbd4b'
    rbox(m, -3.4, 4.0, -3.4, 3.4, 5.2, 3.4, SAND, r=1.0)
    for x, z in ((-2.2, 1.6), (2.4, -1.8), (0.8, 2.4)):
        m.box(x - 0.3, 5.2, z - 0.3, x + 0.3, 5.26, z + 0.3, SANDD)
    for x, z in ((-1.6, -1.2), (1.4, 0.8), (-0.6, 1.8)):
        rbox(m, x - 0.7, 5.2, z - 0.7, x + 0.7, 6.8, z + 0.7, EGG, r=0.3)
        m.box(x - 0.2, 6.0, z - 0.72, x + 0.1, 6.3, z - 0.7, SPOT)
        m.box(x + 0.25, 5.6, z - 0.72, x + 0.5, 5.85, z - 0.7, SPOT)
    m.box(1.0, 5.2, -2.6, 2.6, 5.6, -1.2, EGG)                                          # cracked shell
    turtle(m, 1.8, 5.2, -1.4, 0.5)                                                      # baby hatching

@redesign("turtle_helmet")
def _(m):
    TG, TD, TL = '#4fa83e', '#2f7a2a', '#8fd06a'
    m.box(-4.6, 1.2, 4.0, 4.6, 4.0, 4.6, TG)
    for sd in (-1, 1):
        m.box(min(sd * 4.0, sd * 4.6), 1.2, -4.0, max(sd * 4.0, sd * 4.6), 4.0, 4.0, TG)
    m.box(-4.6, 3.2, -4.6, 4.6, 4.0, -4.0, TG)
    m.box(-4.6, 3.2, -4.7, 4.6, 3.4, -4.6, TL)
    y = dome(m, 4.0, [(4.6, 0.9), (3.8, 0.7), (2.6, 0.5)], TG)
    for x, z in ((-2.2, -2.2), (2.2, -2.2), (-2.2, 2.2), (2.2, 2.2)):
        m.box(x - 1.1, 4.95, z - 1.1, x + 1.1, 5.0, z + 1.1, TL)
    for sd in (-1, 1):
        m.box(sd * 4.6 - 0.05, 1.6, -3.0, sd * 4.6 + 0.05, 3.6, -1.0, TL)
        m.box(sd * 4.6 - 0.05, 1.6, 1.0, sd * 4.6 + 0.05, 3.6, 3.0, TL)
    turtle(m, 0, y, 0.3, 0.6)                                                           # baby turtle riding on top

# ---------- more buddies ----------
@design("baby_sniffer", "Baby Sniffer", "cute")
def _(m):
    R, RD, MOSS, NOSE, K = '#b2493a', '#8a3328', '#5fae46', '#e2b44a', '#1a1418'
    y0 = 4.6
    for sd in (-1, 1):
        for z in (-1.0, 0.6, 2.2):
            m.box(sd * 1.4 - 0.35, y0, z - 0.35, sd * 1.4 + 0.35, y0 + 0.7, z + 0.35, RD)
    rbox(m, -2.0, y0 + 0.6, -1.6, 2.0, y0 + 2.8, 2.8, R, r=0.5)                          # body
    m.box(-1.8, y0 + 2.75, -1.2, 1.8, y0 + 3.1, 2.4, MOSS)                               # mossy back
    for x, z, c in ((-1.0, 0.0, '#ffe45c'), (0.8, 1.4, '#f7a8c8'), (0.2, -0.6, '#ffffff')):
        m.box(x - 0.2, y0 + 3.1, z - 0.2, x + 0.2, y0 + 3.3, z + 0.2, c)
    rbox(m, -1.4, y0 + 0.8, -3.4, 1.4, y0 + 2.9, -1.4, R, r=0.4)                         # head
    rbox(m, -0.9, y0 + 0.5, -4.4, 0.9, y0 + 1.5, -3.2, NOSE, r=0.3)                      # big sniffer nose
    for sd in (-1, 1):
        m.box(sd * 0.4 - 0.15, y0 + 0.9, -4.45, sd * 0.4 + 0.15, y0 + 1.15, -4.4, '#8a5a1a')
        m.box(sd * 0.75 - 0.3, y0 + 1.9, -3.46, sd * 0.75 + 0.3, y0 + 2.5, -3.4, K)       # cute eyes
        m.box(sd * 0.75 - 0.18 + 0.06, y0 + 2.25, -3.48, sd * 0.75 + 0.06, y0 + 2.45, -3.46, '#ffffff')
        m.box(min(sd * 1.4, sd * 1.8), y0 + 1.4, -2.6, max(sd * 1.4, sd * 1.8), y0 + 2.5, -1.8, RD)   # floppy ears
    m.box(-1.0, y0 + 2.9, -3.0, 1.0, y0 + 3.15, -1.8, MOSS)

@design("allay_cookie", "Allay with Cookie", "cute")
def _(m):
    B1, B2, WG = '#5fd3f5', '#3aa8d8', '#d8f4ffa0'
    GLOW.update({B1})
    y0 = 5.6
    m.box(-0.7, y0, -0.5, 0.7, y0 + 1.4, 0.5, B2)                                       # body
    rbox(m, -1.1, y0 + 1.3, -1.1, 1.1, y0 + 3.3, 1.1, B1, r=0.3)                        # head
    for sd in (-1, 1):
        m.box(sd * 0.45 - 0.22, y0 + 2.0, -1.16, sd * 0.45 + 0.22, y0 + 2.6, -1.1, '#1a3a5a')
        m.box(sd * 0.45 - 0.12 + 0.05, y0 + 2.35, -1.18, sd * 0.45 + 0.05, y0 + 2.55, -1.16, '#ffffff')
        m.box(min(sd * 0.3, sd * 2.4), y0 + 0.8, 0.5, max(sd * 0.3, sd * 2.4), y0 + 2.4, 0.6, WG,
              rot=('y', 22.5 * sd, (sd * 0.3, 0, 0.5)))                                  # wings
        m.box(min(sd * 0.7, sd * 1.0), y0 + 0.4, -0.3, max(sd * 0.7, sd * 1.0), y0 + 1.2, 0.3, B2)
    m.box(-0.5, y0 + 0.2, -1.1, 0.5, y0 + 1.0, -0.6, '#f2c33a')                         # holding a cookie
    m.box(-0.2, y0 + 0.5, -1.15, 0.0, y0 + 0.7, -1.1, '#7a4a26')
    m.box(-0.15, 4.6, -0.15, 0.15, y0, 0.15, '#5fd3f540')                               # sparkle trail
    for x, y in ((-1.8, 6.0), (1.6, 9.4)):
        star(m, x, y, -0.5, 0.3, '#a6ffef')

@design("jelly_slime", "Jelly Slime", "cute")
def _(m):
    y0 = 4.6
    m.box(-1.2, y0 + 0.6, -1.2, 1.2, y0 + 3.0, 1.2, '#4fa83e')                          # core
    for sd in (-1, 1):
        m.box(sd * 0.75 - 0.35, y0 + 1.9, -1.26, sd * 0.75 + 0.35, y0 + 2.6, -1.2, '#1e3a1a')
        m.box(sd * 0.75 - 0.2 + 0.08, y0 + 2.3, -1.28, sd * 0.75 + 0.08, y0 + 2.52, -1.26, '#ffffff')
        m.box(sd * 1.0 - 0.25, y0 + 1.4, -1.25, sd * 1.0 + 0.25, y0 + 1.6, -1.2, '#ff9fb8')
    m.box(-0.35, y0 + 1.1, -1.26, 0.35, y0 + 1.3, -1.2, '#1e3a1a')
    rbox(m, -2.0, y0, -2.0, 2.0, y0 + 3.8, 2.0, '#7ad35a90', r=0.4)                      # jelly shell
    m.box(-1.6, y0 + 3.0, -2.06, -0.9, y0 + 3.4, -2.0, '#e6ffd8c0')                      # shine

@design("bunny_buddy", "Bunny Buddy", "cute")
def _(m):
    W, P, BR, K = '#f4f2ee', '#f7a8c8', '#c49a6c', '#1a1418'
    y0 = 4.6
    rbox(m, -1.6, y0, -1.0, 1.6, y0 + 2.2, 2.2, W, r=0.6)                               # body
    rbox(m, -0.5, y0 + 0.6, 2.2, 0.5, y0 + 1.6, 2.8, W, r=0.3)                          # cotton tail
    rbox(m, -1.3, y0 + 1.2, -2.6, 1.3, y0 + 3.4, -0.4, W, r=0.45)                       # head
    for sd in (-1, 1):
        r = ('z', -22.5 * sd, (sd * 0.6, y0 + 3.4, -1.4))
        rbox(m, sd * 0.6 - 0.45, y0 + 3.3, -1.7, sd * 0.6 + 0.45, y0 + 6.0, -1.1, W, r=0.2, rot=r)   # ears
        m.box(sd * 0.6 - 0.22, y0 + 3.6, -1.75, sd * 0.6 + 0.22, y0 + 5.6, -1.7, P, rot=r)
        m.box(sd * 0.55 - 0.25, y0 + 2.2, -2.66, sd * 0.55 + 0.25, y0 + 2.8, -2.6, K)
        m.box(sd * 0.55 - 0.14 + 0.06, y0 + 2.55, -2.68, sd * 0.55 + 0.06, y0 + 2.75, -2.66, W)
        m.box(sd * 0.9 - 0.2, y0 + 1.75, -2.65, sd * 0.9 + 0.2, y0 + 1.95, -2.6, P)
        m.box(sd * 0.6 - 0.35, y0, -1.6, sd * 0.6 + 0.35, y0 + 0.5, -0.8, W)            # paws
    m.box(-0.18, y0 + 1.95, -2.67, 0.18, y0 + 2.15, -2.6, P)                             # nose
    m.box(-1.2, y0 + 2.2, 0.2, -0.2, y0 + 2.25, 1.2, BR)                                # brown spot

# ---------- pirates ----------
def eye_patch(m, c='#1d1b22', rim='#3a3540'):
    rbox(m, 0.6, -1.7, -4.78, 3.4, 0.7, -4.6, c, r=0.5)                                  # patch over one eye
    m.box(0.9, -1.4, -4.8, 3.1, -1.25, -4.78, rim)
    m.box(1.8, 0.3, -4.74, 2.6, 0.5, -4.62, c)
    m.box(-5.0, 0.3, -4.74, 2.6, 0.6, -4.62, c, rot=('z', -22.5, (2.2, 0.45, -4.68)))   # strap up across the forehead
    m.box(-4.7, 3.0, -4.6, -4.6, 3.4, 4.6, c)                                           # around the side,
    m.box(-5.4, -0.55, 4.6, 4.7, -0.25, 4.7, c, rot=('z', -22.5, (4.6, -0.4, 4.65)))    # the back,
    m.box(4.6, -0.55, -4.6, 4.7, -0.25, 4.6, c)                                         # and the other side

@design("eye_patch", "Eye Patch", "basic")
def _(m): eye_patch(m)

@design("pirate_head", "Pirate Head", "cool")
def _(m):
    HAT, HAT_D, BEARD, BEARD_D = '#25222b', '#2e2a35', '#3a2418', '#553624'
    band(m, 2.0, 3.7, RED, 4.6)                                                         # red bandana under the hat
    for x, y in ((-3.2, 2.6), (-0.6, 3.0), (2.4, 2.4), (3.9, 3.1)):
        m.box(x, y, -4.7, x + 0.5, y + 0.45, -4.6, WHITE)
    m.box(-4.0, 1.8, 4.6, -2.6, 3.4, 5.3, '#a82522')
    m.box(-3.8, -0.6, 4.9, -3.1, 2.0, 5.25, RED, rot=('x', -22.5, (-3.45, 2.0, 5.1)))
    dome(m, 3.7, [(4.7, 1.8), (4.2, 1.6), (3.4, 0.9)], HAT)                             # tricorn crown
    for (x1, z1, x2, z2, ax, a, o) in ((-5.6, -5.4, 5.6, -4.7, 'x', -22.5, (0, 4.4, -5.0)), (-5.6, 4.7, 5.6, 5.4, 'x', 22.5, (0, 4.4, 5.0)),
                                       (-5.4, -5.6, -4.7, 5.6, 'z', 22.5, (-5.0, 4.4, 0)), (4.7, -5.6, 5.4, 5.6, 'z', -22.5, (5.0, 4.4, 0))):
        m.box(x1, 4.4, z1, x2, 6.4, z2, HAT_D, rot=(ax, a, o))                          # flared, upturned brim
        m.box(x1 - 0.05, 6.15, z1 - 0.05, x2 + 0.05, 6.5, z2 + 0.05, GOLD, rot=(ax, a, o))
    sk = ('x', -22.5, (0, 4.4, -5.0))
    m.box(-1.0, 5.3, -5.5, 1.0, 6.5, -5.38, WHITE, rot=sk); m.box(-0.6, 5.0, -5.5, 0.6, 5.3, -5.38, WHITE, rot=sk)   # skull
    m.box(-0.6, 5.8, -5.55, -0.2, 6.2, -5.5, HAT, rot=sk); m.box(0.2, 5.8, -5.55, 0.6, 6.2, -5.5, HAT, rot=sk)
    m.box(-1.5, 4.75, -5.5, 1.5, 4.95, -5.4, WHITE, rot=sk)
    m.box(4.4, 6.2, -1.0, 4.9, 10.6, -0.4, '#e8343f', rot=('z', -22.5, (4.6, 6.2, -0.7)))   # feather
    m.box(4.2, 7.0, -1.05, 5.1, 10.2, -0.35, '#c8312d', rot=('z', -22.5, (4.6, 6.2, -0.7)))
    eye_patch(m)
    m.box(-3.6, -4.6, -4.6, 3.6, -2.5, -4.0, BEARD)                                     # beard
    for sd in (-1, 1):
        m.box(min(sd * 3.4, sd * 4.6), -4.6, -4.6, max(sd * 3.4, sd * 4.6), -0.6, -3.2, BEARD)   # sideburns
        m.box(min(sd * 0.3, sd * 2.8), -2.4, -4.8, max(sd * 0.3, sd * 2.8), -1.8, -4.6, BEARD_D)  # moustache
        m.box(min(sd * 2.6, sd * 3.2), -1.8, -4.8, max(sd * 2.6, sd * 3.2), -1.2, -4.6, BEARD_D)
    for k in range(3):                                                                  # braided beard tip
        m.box(-0.7 + 0.12 * k, -5.3 - k * 0.7, -4.6, 0.7 - 0.12 * k, -4.6 - k * 0.7, -4.0, (BEARD, BEARD_D)[k % 2])
    m.box(-0.4, -7.0, -4.65, 0.4, -6.6, -3.95, GOLD)
    m.box(-3.6, -5.0, -4.6, 3.6, -4.6, -3.6, BEARD)
    m.box(-4.8, -2.6, -1.0, -4.6, -1.0, -0.8, GOLD); m.box(-4.8, -2.6, -0.8, -4.6, -2.4, 0.0, GOLD)   # gold earring
    m.box(-4.8, -2.6, 0.0, -4.6, -1.6, 0.2, GOLD)

@design("pirate_parrot", "Pirate Parrot", "cool")
def _(m):
    R, RD, BL, YL, K = '#e8343f', '#b8232d', '#2f6fd8', '#f7d21f', '#1d1b22'
    y0 = 4.6; cx = 1.2
    for sd in (-1, 1):
        m.box(cx + sd * 0.5 - 0.25, y0, -0.8, cx + sd * 0.5 + 0.25, y0 + 0.5, 0.2, '#4a4a52')   # feet
    rbox(m, cx - 1.1, y0 + 0.4, -0.8, cx + 1.1, y0 + 3.2, 1.2, R, r=0.4)                # body
    for sd in (-1, 1):
        x1, x2 = sorted((cx + sd * 1.1, cx + sd * 1.35))
        m.box(x1, y0 + 0.8, -0.4, x2, y0 + 2.9, 1.6, BL)                               # wings
        m.box(x1, y0 + 2.2, -0.45, x2, y0 + 2.9, 0.4, YL)
    m.box(cx - 0.4, y0 - 0.6, 1.2, cx + 0.4, y0 + 1.4, 1.8, BL, rot=('x', -22.5, (cx, y0 + 1.4, 1.5)))   # tail
    rbox(m, cx - 0.9, y0 + 3.0, -1.2, cx + 0.9, y0 + 4.8, 0.6, R, r=0.3)               # head
    m.box(cx - 0.75, y0 + 3.4, -1.26, cx + 0.75, y0 + 4.4, -1.2, '#f4f2ee')            # face patch
    for sd in (-1, 1):
        m.box(cx + sd * 0.45 - 0.18, y0 + 3.85, -1.3, cx + sd * 0.45 + 0.18, y0 + 4.25, -1.26, K)
    m.box(cx - 0.35, y0 + 3.0, -1.9, cx + 0.35, y0 + 3.8, -1.2, '#e8e4d8')             # hooked beak
    m.box(cx - 0.3, y0 + 2.7, -1.9, cx + 0.3, y0 + 3.1, -1.55, '#3a3540')
    m.box(cx - 1.4, y0 + 4.8, -1.0, cx + 1.4, y0 + 5.3, 0.4, '#25222b')                 # mini tricorn
    m.box(cx - 0.8, y0 + 5.3, -0.6, cx + 0.8, y0 + 6.0, 0.0, '#25222b')
    m.box(cx - 1.45, y0 + 5.2, -1.05, cx + 1.45, y0 + 5.35, 0.45, GOLD)
    m.box(cx - 0.25, y0 + 5.4, -0.65, cx + 0.25, y0 + 5.8, -0.6, WHITE)


# ---------- cool crowns ----------
def prong(m, cx, cz, along_x, y, w, hgt, c, t=0.6, n=4):
    for k in range(n):
        ww = w * (1 - k / n)
        if along_x:
            m.box(cx - ww / 2, y + k * hgt / n, cz - t / 2, cx + ww / 2, y + (k + 1) * hgt / n, cz + t / 2, c)
        else:
            m.box(cx - t / 2, y + k * hgt / n, cz - ww / 2, cx + t / 2, y + (k + 1) * hgt / n, cz + ww / 2, c)

def crown(m, c, cd, gem, y=3.4, h=1.6, r=4.8, ph=2.2, pc=None, tip=None, gem2=None):
    band(m, y, y + h, c, r)
    band(m, y, y + 0.35, cd, r + 0.08); band(m, y + h - 0.3, y + h, cd, r + 0.08)
    pc = pc or c
    for k, u in enumerate((-3.0, 0.0, 3.0)):
        hh = ph * (1.25 if u == 0 else 0.85)
        prong(m, u, -r + 0.3, True, y + h, 2.2, hh, pc); prong(m, u, r - 0.3, True, y + h, 2.2, hh * 0.8, pc)
        prong(m, -r + 0.3, u, False, y + h, 2.2, hh * 0.9, pc); prong(m, r - 0.3, u, False, y + h, 2.2, hh * 0.9, pc)
        if tip:
            for (x, z) in ((u, -r + 0.3), (-r + 0.3, u), (r - 0.3, u)):
                m.box(x - 0.3, y + h + hh * 0.9 - 0.1, z - 0.3, x + 0.3, y + h + hh * 0.9 + 0.5, z + 0.3, tip)
    for k, u in enumerate((-3.0, 0.0, 3.0)):
        g = gem2 if (gem2 and k != 1) else gem
        rbox(m, u - 0.55, y + 0.45, -r - 0.25, u + 0.55, y + h - 0.45, -r, g, r=0.2)
        for sd in (-1, 1):
            m.box(sd * r - (0.25 if sd < 0 else 0), y + 0.5, u - 0.45, sd * r + (0.25 if sd > 0 else 0), y + h - 0.5, u + 0.45, g)

@design("netherite_crown", "Netherite Crown", "cool")
def _(m):
    GLOW.update({'#ff6a1f'})
    crown(m, '#3a3438', '#252126', '#ff6a1f', tip=GOLD, gem2='#ffb03a')
    for x in (-1.5, 1.5):
        m.box(x - 0.08, 3.6, -4.95, x + 0.08, 4.8, -4.88, '#ff6a1f')                      # lava cracks

@design("emerald_crown", "Emerald Crown", "cool")
def _(m):
    crown(m, GOLD, GOLD_D, '#2fd06a', tip='#2fd06a', gem2='#1f9a4a')

@design("soul_crown", "Soul Fire Crown", "cool")
def _(m):
    GLOW.update({'#5fe3f0', '#b8fbff'})
    crown(m, '#3a4450', '#252c36', '#5fe3f0', pc='#3a4450')
    for u in (-3.0, 0.0, 3.0):
        for (x, z) in ((u, -4.5), (-4.5, u), (4.5, u), (u, 4.5)):
            m.box(x - 0.35, 5.4, z - 0.35, x + 0.35, 7.6 + (0.6 if u == 0 else 0), z + 0.35, '#5fe3f0a0')   # soul flames
            m.box(x - 0.18, 5.4, z - 0.18, x + 0.18, 6.6, z + 0.18, '#b8fbff')

@design("imperial_crown", "Imperial Crown", "cool")
def _(m):
    VEL, FUR, SPOT = '#8a1a2a', '#f4f2ee', '#1d1b22'
    dome(m, 4.0, [(4.4, 1.6), (3.6, 1.2), (2.4, 0.8)], VEL)                             # velvet cap
    band(m, 2.6, 3.8, FUR, 4.9)                                                         # ermine fur trim
    for u in range(0, 38, 2):
        wrap(m, u + 0.5, 0.35, 3.0, 3.5, SPOT, r=4.9)
    band(m, 3.8, 4.8, GOLD, 4.7)
    for ax in ('x', 'z'):                                                               # crossing gold arches
        for k, (y1, ext) in enumerate(((4.8, 4.5), (6.4, 3.7), (7.6, 2.6))):
            if ax == 'x':
                m.box(-0.4, y1, -ext, 0.4, y1 + (1.6 if k < 2 else 0.9), -ext + 0.6, GOLD); m.box(-0.4, y1, ext - 0.6, 0.4, y1 + (1.6 if k < 2 else 0.9), ext, GOLD)
            else:
                m.box(-ext, y1, -0.4, -ext + 0.6, y1 + (1.6 if k < 2 else 0.9), 0.4, GOLD); m.box(ext - 0.6, y1, -0.4, ext, y1 + (1.6 if k < 2 else 0.9), 0.4, GOLD)
    m.box(-2.0, 8.5, -0.4, 2.0, 9.0, 0.4, GOLD); m.box(-0.4, 8.5, -2.0, 0.4, 9.0, 2.0, GOLD)
    rbox(m, -0.8, 9.0, -0.8, 0.8, 10.4, 0.8, GOLD, r=0.3)                               # orb + cross
    m.box(-0.2, 10.4, -0.2, 0.2, 11.8, 0.2, GOLD); m.box(-0.7, 10.9, -0.2, 0.7, 11.3, 0.2, GOLD)
    for x, c in ((-3.0, '#2f5fd0'), (0.0, RED), (3.0, '#2fd06a')):
        rbox(m, x - 0.5, 4.0, -4.95, x + 0.5, 4.6, -4.7, c, r=0.15)
    for x in (-1.5, 1.5):
        m.box(x - 0.2, 4.15, -4.85, x + 0.2, 4.45, -4.7, '#f4f2ee')

@design("void_crown", "Void Crown", "cool")
def _(m):
    GLOW.update({'#c49bff'})
    band(m, 3.4, 4.8, '#1a1028', 4.8)
    band(m, 3.4, 3.7, '#2a1a40', 4.88)
    import random as _r
    rnd = _r.Random(4)
    for (x, z, ax, a) in ((0, -4.4, 'x', -22.5), (-2.6, -4.4, 'z', 22.5), (2.6, -4.4, 'z', -22.5), (-4.4, 0.0, 'z', 22.5),
                          (4.4, 0.0, 'z', -22.5), (-4.4, 3.0, 'x', 22.5), (4.4, 3.0, 'x', 22.5), (0, 4.4, 'x', 22.5)):
        hgt = 3.8 if x == 0 and z < 0 else rnd.uniform(2.2, 3.0)
        o = (x, 4.8, z)
        m.box(x - 0.55, 4.6, z - 0.55, x + 0.55, 4.8 + hgt, z + 0.55, '#c49bff', rot=(ax, a, o))   # crystal shards
        m.box(x - 0.3, 4.8 + hgt, z - 0.3, x + 0.3, 5.4 + hgt, z + 0.3, '#e8d8ff', rot=(ax, a, o))
    for x, y in ((-3.6, 9.0), (3.0, 9.6), (0.4, 10.6)):
        m.box(x - 0.2, y, -0.2, x + 0.2, y + 0.4, 0.2, '#c49bff80')                     # floating particles

@design("tilted_crown", "Tilted Crown", "cool")
def _(m):
    r = ('z', 22.5, (1.4, 4.6, 0))
    cx = 1.4
    for (x1, z1, x2, z2) in ((cx - 2.4, -2.4, cx + 2.4, -1.8), (cx - 2.4, 1.8, cx + 2.4, 2.4), (cx - 2.4, -1.8, cx - 1.8, 1.8), (cx + 1.8, -1.8, cx + 2.4, 1.8)):
        m.box(x1, 4.6, z1, x2, 5.8, z2, GOLD, rot=r)
    for (x1, z1, x2, z2) in ((cx - 2.45, -2.45, cx + 2.45, -1.75), (cx - 2.45, 1.75, cx + 2.45, 2.45)):
        m.box(x1, 4.6, z1, x2, 4.85, z2, GOLD_D, rot=r)
    for x in (cx - 2.1, cx, cx + 2.1):
        for z in (-2.1, 2.1):
            for k in range(3):
                w = 0.6 - 0.18 * k
                m.box(x - w, 5.8 + k * 0.5, z - 0.3, x + w, 6.3 + k * 0.5, z + 0.3, GOLD, rot=r)
            m.box(x - 0.25, 7.3, z - 0.25, x + 0.25, 7.7, z + 0.25, RED if x == cx else '#2f5fd0', rot=r)
    rbox(m, cx - 0.5, 4.95, -2.55, cx + 0.5, 5.5, -2.4, RED, r=0.15, rot=r)

# ---------- medals + champion ----------
def medal(m, metal, dark, rib1, rib2):
    band(m, 2.4, 3.2, rib1, 4.6)
    for u in range(0, 37, 1):
        wrap(m, u + 0.3, 0.4, 2.7, 2.9, rib2)
    for sd in (-1, 1):
        m.box(sd * 0.2 - 0.35, 1.4, -4.75, sd * 0.2 + 0.35, 3.0, -4.6, rib1, rot=('z', 22.5 * sd, (sd * 0.2, 3.0, -4.68)))   # V ribbon
    rbox(m, -1.2, -0.3, -4.95, 1.2, 1.9, -4.6, metal, r=0.45)                           # medal
    m.box(-0.95, -0.05, -4.98, 0.95, 0.1, -4.95, dark)
    star(m, 0, 0.8, -4.95, 0.45, dark)
    m.box(-0.4, 1.85, -4.85, 0.4, 2.15, -4.6, dark)                                     # loop

@design("medal_gold", "Gold Medal", "cool")
def _(m): medal(m, '#f2c33a', '#b8861c', '#c8312d', '#f4f2ee')

@design("medal_silver", "Silver Medal", "cool")
def _(m): medal(m, '#d8dde6', '#8c8f99', '#2f5fd0', '#f4f2ee')

@design("medal_bronze", "Bronze Medal", "cool")
def _(m): medal(m, '#d08a4a', '#8a5226', '#2f8a4a', '#f4f2ee')

@design("golden_laurel", "Golden Laurel", "cool")
def _(m):
    band(m, 2.75, 2.95, GOLD_D, 4.6)
    u = 0.0
    while u < 36.8:
        if not (3.7 < u < 5.5):                                                         # gap in the middle of the forehead
            wrap(m, u, 0.55, 3.0, 3.6, (GOLD, '#ffe07a')[int(u * 2) % 2], t=0.25)
            wrap(m, u + 0.3, 0.55, 2.1, 2.7, (GOLD, '#ffe07a')[int(u * 2 + 1) % 2], t=0.25)
        u += 0.7
    for sd in (-1, 1):
        m.box(sd * 0.7 - 0.25, 3.0, -4.9, sd * 0.7 + 0.25, 3.9, -4.6, GOLD, rot=('z', -22.5 * sd, (sd * 0.7, 3.0, -4.75)))

@design("trophy_hat", "Trophy Hat", "cool")
def _(m):
    WD = '#5a3720'
    rbox(m, -2.2, 4.6, -2.2, 2.2, 5.6, 2.2, WD, r=0.3)                                  # wooden base
    m.box(-1.6, 5.6, -1.6, 1.6, 6.0, 1.6, GOLD_D)
    m.box(-0.8, 5.0, -2.25, 0.8, 5.3, -2.2, GOLD)                                       # plaque
    m.box(-0.4, 6.0, -0.4, 0.4, 7.4, 0.4, GOLD)                                         # stem
    steps(m, 0, 0, 7.2, [1.0, 1.8, 2.6, 3.2], GOLD, h=0.5, smooth=1)                    # cup flaring up
    m.box(-1.8, 9.2, -1.8, 1.8, 10.4, 1.8, GOLD)
    m.box(-1.85, 10.2, -1.85, 1.85, 10.5, 1.85, GOLD_D)
    m.box(-1.4, 10.3, -1.4, 1.4, 10.52, 1.4, '#b8861c')
    for sd in (-1, 1):                                                                  # handles
        x1, x2 = sorted((sd * 1.8, sd * 2.8))
        m.box(x1, 9.4, -0.25, x2, 9.7, 0.25, GOLD); m.box(x1, 8.0, -0.25, x2, 8.3, 0.25, GOLD)
        m.box(min(sd * 2.5, sd * 2.8), 8.0, -0.25, max(sd * 2.5, sd * 2.8), 9.7, 0.25, GOLD)
    star(m, 0, 9.6, -1.8, 0.4, '#fff4a0')


# ======================================================================
# BATCH 5+: 250 more. Shared helpers for chibi critters.
# ======================================================================
def eyes(m, cx, y, z, sep, w=0.5, h=0.6, c='#1a1418', shine='#ffffff', t=0.06):
    """Two cute eyes on a front face at z, with a sparkle in the upper-left of each."""
    for sd in (-1, 1):
        x = cx + sd * sep
        m.box(x - w / 2, y, z - t, x + w / 2, y + h, z, c)
        if shine:
            m.box(x + w / 2 - 0.26, y + h - 0.26, z - t - 0.02, x + w / 2 - 0.06, y + h - 0.06, z - t, shine)

def cheeks(m, cx, y, z, sep, c='#ff9fb8', w=0.45, h=0.22):
    for sd in (-1, 1):
        m.box(cx + sd * sep - w / 2, y, z - 0.05, cx + sd * sep + w / 2, y + h, z, c)

def legs4(m, c, x, z1, z2, y0, h, w=0.6, foot=None):
    for sx in (-1, 1):
        for z in (z1, z2):
            m.box(sx * x - w / 2, y0, z - w / 2, sx * x + w / 2, y0 + h, z + w / 2, c)
            if foot:
                m.box(sx * x - w / 2 - 0.02, y0, z - w / 2 - 0.02, sx * x + w / 2 + 0.02, y0 + 0.2, z + w / 2 + 0.02, foot)

def patches(m, axis, plane, out, a1, a2, y1, y2, n, cols, seed, s=0.45):
    """Random pixel patches on one flat face (axis 'z' = front/back face, 'x' = side face, 'y' = top face)."""
    import random as _r
    rnd = _r.Random(seed)
    for _ in range(n):
        a = rnd.uniform(a1, a2 - s); b = rnd.uniform(y1, y2 - s); c = rnd.choice(cols)
        p1, p2 = sorted((plane, plane + out * 0.04))
        if axis == 'z':
            m.box(a, b, p1, a + s, b + s, p2, c)
        elif axis == 'x':
            m.box(p1, b, a, p2, b + s, a + s, c)
        else:
            m.box(a, p1, b, a + s, p2, b + s, c)

def tail_curl(m, x, y, z, c, s=0.3):
    for dx, dy, dz in ((0, 0, 0), (0, s, s), (0, 2 * s, 0), (0, s, -s * 0.2)):
        m.box(x - s / 2 + dx, y + dy, z + dz, x + s / 2 + dx, y + dy + s, z + dz + s, c)

# ---------- A: mob buddies ----------
@design("creeper_buddy", "Creeper Buddy", "cute")
def _(m):
    G, GD, GL, K = '#5fae46', '#3f8a32', '#8fd06a', '#1d2a1a'
    y0 = 4.6
    for sx in (-1, 1):
        for z in (-1.0, 1.4):
            m.box(sx * 0.75 - 0.5, y0, z - 0.5, sx * 0.75 + 0.5, y0 + 0.8, z + 0.5, G)
            m.box(sx * 0.75 - 0.52, y0, z - 0.52, sx * 0.75 + 0.52, y0 + 0.2, z + 0.52, GD)
    m.box(-1.0, y0 + 0.7, -0.6, 1.0, y0 + 2.5, 1.0, G)                                  # body
    patches(m, 'z', -0.6, -1, -1.0, 1.0, y0 + 0.8, y0 + 2.4, 5, [GD, GL], 1, s=0.4)
    rbox(m, -1.7, y0 + 2.3, -1.9, 1.7, y0 + 5.7, 1.5, G, r=0.25)                         # big head
    for ax, pl, out, a1, a2 in (('x', 1.7, 1, -1.9, 1.5), ('x', -1.7, -1, -1.9, 1.5), ('z', 1.5, 1, -1.7, 1.7)):
        patches(m, ax, pl, out, a1, a2, y0 + 2.4, y0 + 5.6, 10, [GD, GL, GD], 2 + int(pl * 3), s=0.42)
    patches(m, 'y', y0 + 5.7, 1, -1.5, 1.5, -1.7, 1.3, 8, [GD, GL], 9, s=0.42)
    relief(m, ["........", "........", ".EE..EE.", ".EE..EE.", "...MM...", "..MMMM..", "..MMMM..", "..M..M.."],
           -1.9, {'E': (K, 0.06), 'M': (K, 0.06)}, cell=0.425, top=y0 + 5.7)
    for sd in (-1, 1):
        x = sd * 0.85
        m.box(x + (0.425 if sd < 0 else 0) - 0.3, y0 + 4.6, -1.98, x + (0.425 if sd < 0 else 0) - 0.12, y0 + 4.78, -1.96, '#ffffff')
    cheeks(m, 0, y0 + 3.85, -1.9, 1.35, w=0.4, h=0.3)

@design("enderman_buddy", "Enderman Buddy", "cute")
def _(m):
    K, K2, P, PL = '#141218', '#22202a', '#d77bff', '#f4c8ff'
    GLOW.update({P})
    y0 = 4.6
    for sd in (-1, 1):
        m.box(sd * 0.5 - 0.2, y0, -0.2, sd * 0.5 + 0.2, y0 + 2.6, 0.2, K)                # long legs
    m.box(-0.8, y0 + 2.5, -0.4, 0.8, y0 + 3.9, 0.4, K2)                                 # body
    for sd in (-1, 1):
        m.box(sd * 0.8 - (0.4 if sd > 0 else 0), y0 + 1.6, -0.2, sd * 0.8 + (0.4 if sd < 0 else 0), y0 + 3.9, 0.2, K)   # long arms
    rbox(m, -0.9, y0 + 1.4, -1.6, 0.9, y0 + 2.6, -0.4, '#5fae46', r=0.1)                 # holding a grass block
    m.box(-0.92, y0 + 1.4, -1.62, 0.92, y0 + 2.2, -0.38, '#7a4a26')
    patches(m, 'z', -1.62, -1, -0.9, 0.9, y0 + 1.45, y0 + 2.15, 3, ['#5e3a20', '#8a5a34'], 4, s=0.25)
    rbox(m, -1.4, y0 + 3.8, -1.4, 1.4, y0 + 6.4, 1.4, K, r=0.2)                          # head
    eyes(m, 0, y0 + 4.8, -1.4, 0.7, w=0.8, h=0.5, c=P)
    for sd in (-1, 1):
        m.box(sd * 0.7 - 0.15, y0 + 4.85, -1.47, sd * 0.7 + 0.15, y0 + 5.2, -1.46, '#7a2aa8')
    cheeks(m, 0, y0 + 4.35, -1.4, 1.0, c='#5a2a6a')
    for x, y in ((-2.2, 8.4), (2.0, 9.6), (-1.6, 11.0)):
        m.box(x - 0.15, y, -0.15, x + 0.15, y + 0.3, 0.15, PL)                            # ender particles

@design("pig_buddy", "Pig Buddy", "cute")
def _(m):
    P, PD, PL, K = '#f2a6b4', '#e08a9c', '#f9c8d2', '#1a1418'
    y0 = 4.6
    legs4(m, PD, 1.0, -0.9, 1.6, y0, 0.7, w=0.65)
    rbox(m, -1.5, y0 + 0.6, -1.3, 1.5, y0 + 2.6, 2.2, P, r=0.5)                          # body
    rbox(m, -1.4, y0 + 1.0, -3.3, 1.4, y0 + 3.6, -0.9, P, r=0.45)                        # head
    rbox(m, -0.75, y0 + 1.4, -3.75, 0.75, y0 + 2.3, -3.3, PL, r=0.15)                    # snout
    for sd in (-1, 1):
        m.box(sd * 0.32 - 0.15, y0 + 1.7, -3.8, sd * 0.32 + 0.15, y0 + 2.0, -3.75, '#c06a7c')
        m.box(sd * 0.95 - 0.45, y0 + 3.4, -2.6, sd * 0.95 + 0.45, y0 + 3.9, -1.9, PD,
              rot=('x', -22.5, (sd * 0.95, y0 + 3.4, -2.25)))                             # flop ears
    eyes(m, 0, y0 + 2.5, -3.3, 0.8, w=0.42, h=0.5)
    cheeks(m, 0, y0 + 2.0, -3.3, 1.1)
    tail_curl(m, 0, y0 + 1.8, 2.2, PD)

@design("cow_buddy", "Cow Buddy", "cute")
def _(m):
    W, K, PK, HN = '#f4f2ee', '#2a2226', '#f2b0b8', '#e8e0c8'
    y0 = 4.6
    legs4(m, W, 1.0, -0.9, 1.7, y0, 0.8, w=0.6, foot=K)
    rbox(m, -1.6, y0 + 0.7, -1.3, 1.6, y0 + 2.8, 2.4, W, r=0.45)                         # body
    for (x, z, w, d) in ((-1.62, 0.2, 0.0, 1.4), (1.62, -0.6, 0.0, 1.2)):
        x1, x2 = sorted((x, x + (0.05 if x > 0 else -0.05)))
        m.box(x1, y0 + 1.3, z, x2, y0 + 2.4, z + d, K)                                   # side spots
    m.box(-0.6, y0 + 2.8, 0.4, 0.8, y0 + 2.85, 1.6, K)
    rbox(m, -1.4, y0 + 1.1, -3.4, 1.4, y0 + 3.8, -1.0, W, r=0.4)                         # head
    m.box(0.3, y0 + 2.8, -3.46, 1.4, y0 + 3.8, -3.4, K)                                  # face patch
    rbox(m, -1.0, y0 + 1.1, -3.85, 1.0, y0 + 2.1, -3.3, PK, r=0.2)                       # muzzle
    for sd in (-1, 1):
        m.box(sd * 0.4 - 0.12, y0 + 1.5, -3.9, sd * 0.4 + 0.12, y0 + 1.75, -3.85, '#b86a78')
        m.box(min(sd * 1.4, sd * 2.0), y0 + 3.0, -2.4, max(sd * 1.4, sd * 2.0), y0 + 3.4, -1.9, W)   # ears
        m.box(sd * 0.9 - 0.18, y0 + 3.8, -2.2, sd * 0.9 + 0.18, y0 + 4.5, -1.85, HN)       # horns
    eyes(m, 0, y0 + 2.6, -3.4, 0.6, w=0.42, h=0.5)
    m.box(-0.2, y0 + 1.4, 2.4, 0.2, y0 + 2.6, 2.7, W); m.box(-0.25, y0 + 1.1, 2.45, 0.25, y0 + 1.45, 2.75, K)   # tail

@design("mooshroom_buddy", "Mooshroom Buddy", "cute")
def _(m):
    R, RD, W, PK = '#c03a2e', '#9a2a22', '#f4f2ee', '#f2b0b8'
    y0 = 4.6
    legs4(m, R, 1.0, -0.9, 1.7, y0, 0.8, w=0.6, foot=W)
    rbox(m, -1.6, y0 + 0.7, -1.3, 1.6, y0 + 2.8, 2.4, R, r=0.45)
    patches(m, 'x', 1.6, 1, -1.0, 2.0, y0 + 1.0, y0 + 2.6, 3, [W], 3, s=0.7)
    patches(m, 'x', -1.6, -1, -1.0, 2.0, y0 + 1.0, y0 + 2.6, 3, [W], 5, s=0.7)
    rbox(m, -1.4, y0 + 1.1, -3.4, 1.4, y0 + 3.8, -1.0, R, r=0.4)
    rbox(m, -1.0, y0 + 1.1, -3.85, 1.0, y0 + 2.1, -3.3, PK, r=0.2)
    for sd in (-1, 1):
        m.box(sd * 0.4 - 0.12, y0 + 1.5, -3.9, sd * 0.4 + 0.12, y0 + 1.75, -3.85, '#b86a78')
        m.box(sd * 0.9 - 0.18, y0 + 3.8, -2.2, sd * 0.9 + 0.18, y0 + 4.4, -1.85, '#e8e0c8')
    eyes(m, 0, y0 + 2.6, -3.4, 0.6, w=0.42, h=0.5)
    cheeks(m, 0, y0 + 2.2, -3.4, 1.0, c='#ff8a8a')
    for x, y, z in ((-0.7, y0 + 2.8, 0.0), (0.8, y0 + 2.8, 1.4), (0.3, y0 + 3.8, -2.4)):  # red mushrooms
        m.box(x - 0.12, y, z - 0.12, x + 0.12, y + 0.6, z + 0.12, W)
        rbox(m, x - 0.5, y + 0.5, z - 0.5, x + 0.5, y + 0.95, z + 0.5, RED, r=0.2)
        m.box(x - 0.2, y + 0.95, z - 0.2, x, y + 1.0, z, W)

@design("sheep_buddy", "Sheep Buddy", "cute")
def _(m):
    W, WS, F, FD = '#f4f2ee', '#e2ded6', '#e8cdb0', '#c9a888'
    y0 = 4.6
    legs4(m, F, 0.9, -0.8, 1.6, y0, 0.7, w=0.5)
    rbox(m, -1.9, y0 + 0.6, -1.5, 1.9, y0 + 3.0, 2.4, W, r=0.7)                          # fluffy wool body
    for x, y, z in ((-1.2, y0 + 3.0, -0.6), (0.6, y0 + 3.0, 0.8), (-0.4, y0 + 3.0, 1.8), (1.3, y0 + 2.6, -1.0)):
        rbox(m, x - 0.7, y - 0.3, z - 0.7, x + 0.7, y + 0.35, z + 0.7, (W, WS)[int(x * 10) % 2], r=0.3)
    rbox(m, -1.0, y0 + 1.4, -3.1, 1.0, y0 + 3.2, -1.3, F, r=0.35)                        # face
    rbox(m, -1.25, y0 + 2.8, -2.6, 1.25, y0 + 3.7, -1.2, W, r=0.35)                      # wool fringe
    for sd in (-1, 1):
        m.box(min(sd * 1.0, sd * 1.7), y0 + 2.2, -2.2, max(sd * 1.0, sd * 1.7), y0 + 2.6, -1.8, FD)
    eyes(m, 0, y0 + 2.2, -3.1, 0.45, w=0.38, h=0.45)
    cheeks(m, 0, y0 + 1.8, -3.1, 0.7, w=0.3)
    m.box(-0.15, y0 + 1.65, -3.15, 0.15, y0 + 1.8, -3.1, FD)

@design("hen_buddy", "Hen Buddy", "cute")
def _(m):
    W, Y, R, O = '#f4f2ee', '#f2c23a', '#e0343a', '#f29a2a'
    y0 = 4.6
    for sd in (-1, 1):
        m.box(sd * 0.5 - 0.12, y0 + 0.2, -0.12, sd * 0.5 + 0.12, y0 + 0.9, 0.12, O)
        m.box(sd * 0.5 - 0.35, y0, -0.6, sd * 0.5 + 0.35, y0 + 0.2, 0.3, O)
    rbox(m, -1.2, y0 + 0.8, -1.0, 1.2, y0 + 2.6, 1.8, W, r=0.45)                         # body
    for sd in (-1, 1):
        m.box(min(sd * 1.2, sd * 1.4), y0 + 1.2, -0.4, max(sd * 1.2, sd * 1.4), y0 + 2.2, 1.4, '#e2ded6')   # wings
    m.box(-0.5, y0 + 2.0, 1.8, 0.5, y0 + 3.0, 2.3, W)                                   # tail
    rbox(m, -0.8, y0 + 2.4, -1.3, 0.8, y0 + 4.4, 0.2, W, r=0.25)                         # tall head
    m.box(-0.5, y0 + 2.9, -1.95, 0.5, y0 + 3.4, -1.3, Y)                                # beak
    m.box(-0.25, y0 + 2.4, -1.5, 0.25, y0 + 2.95, -1.3, R)                              # wattle
    m.box(-0.2, y0 + 4.4, -1.0, 0.2, y0 + 4.9, 0.0, R)                                  # comb
    eyes(m, 0, y0 + 3.55, -1.3, 0.48, w=0.3, h=0.42)

@design("wolf_pup", "Wolf Pup", "cute")
def _(m):
    G, GD, GL, K, COL = '#d6d3d0', '#a8a49f', '#f0eeea', '#1a1418', '#d8343a'
    y0 = 4.6
    legs4(m, G, 0.8, -0.8, 1.6, y0, 0.8, w=0.55)
    rbox(m, -1.2, y0 + 0.7, -1.2, 1.2, y0 + 2.4, 2.0, G, r=0.4)
    m.box(-1.25, y0 + 1.7, -1.3, 1.25, y0 + 2.15, -0.8, COL)                            # red collar
    m.box(-0.2, y0 + 1.4, -1.35, 0.2, y0 + 1.75, -1.3, GOLD)
    rbox(m, -1.3, y0 + 1.8, -3.0, 1.3, y0 + 4.0, -0.8, G, r=0.4)                         # head
    rbox(m, -0.6, y0 + 1.8, -3.7, 0.6, y0 + 2.7, -2.9, GL, r=0.2)                        # snout
    m.box(-0.22, y0 + 2.4, -3.75, 0.22, y0 + 2.7, -3.7, K)
    for sd in (-1, 1):
        steps(m, sd * 0.8, -1.6, y0 + 4.0, [0.8, 0.55, 0.3], G, depth=0.4, h=0.3, smooth=1)   # ears
        m.box(sd * 0.8 - 0.2, y0 + 4.0, -1.83, sd * 0.8 + 0.2, y0 + 4.25, -1.8, '#f2b0b8')
    eyes(m, 0, y0 + 2.95, -3.0, 0.55, w=0.4, h=0.5)
    cheeks(m, 0, y0 + 2.6, -3.0, 0.95, w=0.35)
    m.box(-0.25, y0 + 1.8, 2.0, 0.25, y0 + 3.4, 2.5, G, rot=('x', 22.5, (0, y0 + 1.8, 2.25)))   # wagging tail
    m.box(-0.27, y0 + 2.9, 2.35, 0.27, y0 + 3.45, 2.85, GL, rot=('x', 22.5, (0, y0 + 1.8, 2.25)))

@design("parrot_buddy", "Parrot Buddy", "cute")
def _(m):
    G, GD, Y, B, BK = '#4cc34a', '#2f8a32', '#f2d23a', '#2f6fd8', '#3a3540'
    y0 = 4.6
    for sd in (-1, 1):
        m.box(sd * 0.4 - 0.25, y0, -0.5, sd * 0.4 + 0.25, y0 + 0.4, 0.3, BK)
    rbox(m, -0.9, y0 + 0.4, -0.7, 0.9, y0 + 2.8, 1.0, G, r=0.35)                         # body
    for sd in (-1, 1):
        x1, x2 = sorted((sd * 0.9, sd * 1.15))
        m.box(x1, y0 + 0.8, -0.4, x2, y0 + 2.5, 1.2, GD)
        m.box(x1, y0 + 0.8, 0.6, x2, y0 + 1.4, 1.3, B)
    m.box(-0.35, y0 - 0.4, 1.0, 0.35, y0 + 1.2, 1.5, B, rot=('x', -22.5, (0, y0 + 1.2, 1.25)))   # tail
    rbox(m, -0.8, y0 + 2.6, -1.0, 0.8, y0 + 4.2, 0.6, G, r=0.3)                          # head
    m.box(-0.6, y0 + 3.9, -0.6, 0.6, y0 + 4.5, 0.2, Y)                                  # yellow crest
    m.box(-0.3, y0 + 2.6, -1.6, 0.3, y0 + 3.3, -1.0, '#3a3540')                         # beak
    m.box(-0.3, y0 + 3.0, -1.7, 0.3, y0 + 3.3, -1.6, '#5a5560')
    eyes(m, 0, y0 + 3.4, -1.0, 0.45, w=0.3, h=0.4)

@design("bat_buddy", "Bat Buddy", "cute")
def _(m):
    BR, BRD, WG, K = '#5a4636', '#3e2f24', '#2e2420', '#1a1418'
    y0 = 4.6
    rbox(m, -0.9, y0, -0.8, 0.9, y0 + 1.8, 0.8, BR, r=0.4)                               # round body
    rbox(m, -1.0, y0 + 1.6, -1.0, 1.0, y0 + 3.3, 0.8, BR, r=0.35)                        # head
    for sd in (-1, 1):
        steps(m, sd * 0.6, -0.2, y0 + 3.3, [0.7, 0.5, 0.25], BR, depth=0.3, h=0.35, smooth=1)   # ears
        m.box(sd * 0.6 - 0.15, y0 + 3.3, -0.37, sd * 0.6 + 0.15, y0 + 3.7, -0.35, '#c08a7a')
        r = ('z', 22.5 * sd, (sd * 0.9, y0 + 1.4, 0))
        m.box(min(sd * 0.9, sd * 3.4), y0 + 1.2, -0.1, max(sd * 0.9, sd * 3.4), y0 + 1.6, 0.1, BRD, rot=r)   # wing bone
        for k, (x_end, yb) in enumerate(((1.8, y0 + 0.2), (2.6, y0 + 0.4), (3.4, y0 + 0.7))):
            x1, x2 = sorted((sd * (0.9 + 0.9 * k), sd * x_end))
            m.box(x1, yb, -0.05, x2, y0 + 1.3, 0.05, WG, rot=r)                          # scalloped wing
    eyes(m, 0, y0 + 2.4, -1.0, 0.42, w=0.35, h=0.45)
    m.box(-0.35, y0 + 2.0, -1.06, -0.15, y0 + 2.2, -1.0, '#ffffff'); m.box(0.15, y0 + 2.0, -1.06, 0.35, y0 + 2.2, -1.0, '#ffffff')   # fangs
    cheeks(m, 0, y0 + 2.05, -1.0, 0.75, w=0.3, h=0.2)

@design("strider_buddy", "Strider Buddy", "cute")
def _(m):
    R, RD, H, K = '#b8343a', '#8a2228', '#5a2a30', '#1a1418'
    y0 = 4.6
    for sd in (-1, 1):
        m.box(sd * 0.8 - 0.3, y0, -0.3, sd * 0.8 + 0.3, y0 + 1.8, 0.3, '#6a3a4a')          # wobbly legs
        m.box(sd * 0.8 - 0.35, y0 + 0.9, -0.35, sd * 0.8 + 0.35, y0 + 1.0, 0.35, '#8a4a5a')
    rbox(m, -1.6, y0 + 1.8, -1.4, 1.6, y0 + 4.0, 1.4, R, r=0.4)                          # body-head
    for i, x in enumerate((-1.2, -0.6, 0.0, 0.6, 1.2)):                                   # wavy hair strands
        h = 1.0 + 0.4 * (i % 2)
        m.box(x - 0.12, y0 + 4.0, -0.2, x + 0.12, y0 + 4.0 + h, 0.2, H, rot=('z', (-22.5, 22.5)[i % 2], (x, y0 + 4.0, 0)))
    m.box(-1.62, y0 + 1.8, -1.42, 1.62, y0 + 2.3, 1.42, RD)
    eyes(m, 0, y0 + 2.9, -1.4, 0.6, w=0.45, h=0.6)
    m.box(-0.5, y0 + 2.4, -1.46, 0.5, y0 + 2.55, -1.4, K)                               # little smile
    cheeks(m, 0, y0 + 2.5, -1.4, 1.1, c='#ff8a8a')

@design("goat_buddy", "Goat Buddy", "cute")
def _(m):
    W, WS, HN, K = '#f4f2ee', '#d8d4cc', '#a89a86', '#1a1418'
    y0 = 4.6
    legs4(m, WS, 0.85, -0.8, 1.6, y0, 0.9, w=0.5, foot='#5a4a3a')
    rbox(m, -1.3, y0 + 0.8, -1.2, 1.3, y0 + 2.6, 2.0, W, r=0.45)
    rbox(m, -1.0, y0 + 1.6, -3.0, 1.0, y0 + 3.6, -0.9, W, r=0.35)                        # head
    m.box(-0.4, y0 + 1.0, -2.8, 0.4, y0 + 1.7, -2.4, WS)                                # beard
    for sd in (-1, 1):
        r = ('x', 22.5, (sd * 0.6, y0 + 3.6, -1.6))
        m.box(sd * 0.6 - 0.2, y0 + 3.5, -1.8, sd * 0.6 + 0.2, y0 + 4.8, -1.4, HN, rot=r)    # curved horns
        m.box(sd * 0.6 - 0.18, y0 + 4.6, -1.2, sd * 0.6 + 0.18, y0 + 4.95, -0.4, HN, rot=r)
        m.box(min(sd * 1.0, sd * 1.7), y0 + 2.8, -2.0, max(sd * 1.0, sd * 1.7), y0 + 3.1, -1.6, WS)
    eyes(m, 0, y0 + 2.6, -3.0, 0.5, w=0.38, h=0.42, c='#6a4a2a')
    m.box(-0.2, y0 + 2.0, -3.06, 0.2, y0 + 2.2, -3.0, '#c9a0a0')
    cheeks(m, 0, y0 + 2.25, -3.0, 0.75, w=0.3)

@design("camel_buddy", "Camel Buddy", "cute")
def _(m):
    C, CD, K = '#d9b07a', '#b98a54', '#1a1418'
    y0 = 4.6
    legs4(m, C, 0.9, -0.8, 1.8, y0, 1.1, w=0.5, foot=CD)
    rbox(m, -1.3, y0 + 1.0, -1.2, 1.3, y0 + 2.6, 2.4, C, r=0.4)
    rbox(m, -0.9, y0 + 2.5, -0.4, 0.9, y0 + 3.6, 1.4, C, r=0.4)                          # hump
    m.box(-1.35, y0 + 2.3, -0.2, 1.35, y0 + 2.7, 1.2, '#c8312d')                         # blanket
    for x in (-1.36, 1.36):
        m.box(x - 0.02, y0 + 1.6, -0.2, x + 0.02, y0 + 2.3, 1.2, '#2f6fd8')
    m.box(-0.45, y0 + 2.2, -2.0, 0.45, y0 + 3.8, -1.2, C)                               # neck
    rbox(m, -0.75, y0 + 3.4, -3.2, 0.75, y0 + 4.6, -1.3, C, r=0.3)                       # head
    m.box(-0.5, y0 + 3.4, -3.4, 0.5, y0 + 3.9, -3.2, CD)
    for sd in (-1, 1):
        m.box(sd * 0.55 - 0.15, y0 + 4.6, -1.7, sd * 0.55 + 0.15, y0 + 4.95, -1.45, CD)
    eyes(m, 0, y0 + 4.0, -3.2, 0.38, w=0.3, h=0.36)
    m.box(-0.2, y0 + 1.0, 2.4, 0.2, y0 + 2.1, 2.7, CD)

@design("panda_buddy", "Panda Buddy", "cute")
def _(m):
    W, K, BB = '#f4f2ee', '#1d1b22', '#6cbd4b'
    y0 = 4.6
    rbox(m, -1.4, y0, -0.9, 1.4, y0 + 2.2, 1.6, W, r=0.6)                                # sitting body
    m.box(-1.45, y0 + 1.4, -0.95, 1.45, y0 + 2.0, 1.65, K)                               # shoulder band
    for sd in (-1, 1):
        rbox(m, sd * 0.8 - 0.45, y0, -1.5, sd * 0.8 + 0.45, y0 + 0.7, -0.6, K, r=0.2)      # feet
        m.box(sd * 1.0 - 0.3, y0 + 0.8, -1.3, sd * 1.0 + 0.3, y0 + 1.8, -0.8, K)           # arms
    m.box(-1.4, y0 + 1.1, -1.6, 1.4, y0 + 1.4, -1.3, BB)                                # bamboo
    m.box(-0.4, y0 + 1.1, -1.65, -0.3, y0 + 1.4, -1.25, '#4a9a3a')
    m.box(1.2, y0 + 1.4, -1.6, 1.8, y0 + 1.8, -1.45, '#8fd06a')
    rbox(m, -1.4, y0 + 2.0, -1.4, 1.4, y0 + 4.2, 1.2, W, r=0.5)                          # head
    for sd in (-1, 1):
        rbox(m, sd * 1.0 - 0.45, y0 + 4.0, -0.5, sd * 1.0 + 0.45, y0 + 4.6, 0.1, K, r=0.15)   # ears
        m.box(sd * 0.6 - 0.4, y0 + 2.8, -1.46, sd * 0.6 + 0.4, y0 + 3.6, -1.4, K)         # eye patches
    eyes(m, 0, y0 + 3.0, -1.46, 0.6, w=0.3, h=0.36)
    m.box(-0.2, y0 + 2.5, -1.47, 0.2, y0 + 2.75, -1.4, K)
    cheeks(m, 0, y0 + 2.45, -1.4, 1.0, w=0.35)

@design("polar_bear_cub", "Polar Bear Cub", "cute")
def _(m):
    W, WS, K = '#f6f4ee', '#e0dcd2', '#1a1418'
    y0 = 4.6
    legs4(m, W, 0.9, -0.8, 1.7, y0, 0.7, w=0.65)
    rbox(m, -1.4, y0 + 0.6, -1.2, 1.4, y0 + 2.6, 2.2, W, r=0.55)
    rbox(m, -1.3, y0 + 1.2, -3.1, 1.3, y0 + 3.4, -0.9, W, r=0.5)                         # head
    rbox(m, -0.6, y0 + 1.3, -3.6, 0.6, y0 + 2.2, -2.9, WS, r=0.2)                        # snout
    m.box(-0.25, y0 + 1.85, -3.65, 0.25, y0 + 2.15, -3.6, K)
    for sd in (-1, 1):
        rbox(m, sd * 0.9 - 0.35, y0 + 3.2, -2.0, sd * 0.9 + 0.35, y0 + 3.75, -1.5, W, r=0.15)
        m.box(sd * 0.9 - 0.18, y0 + 3.3, -2.03, sd * 0.9 + 0.18, y0 + 3.6, -2.0, '#c9c0b8')
    eyes(m, 0, y0 + 2.4, -3.1, 0.6, w=0.36, h=0.42)
    cheeks(m, 0, y0 + 2.05, -3.1, 0.95, w=0.32)
    rbox(m, -0.3, y0 + 1.6, 2.2, 0.3, y0 + 2.1, 2.6, W, r=0.1)

@design("glow_squid_buddy", "Glow Squid Buddy", "cute")
def _(m):
    T, TL, TD, GL = '#2fb8b0', '#7af0e0', '#1f8a86', '#a6ffef'
    GLOW.update({T, TL})
    y0 = 4.6
    for i in range(8):                                                                  # tentacles drape over the head
        import math
        a = i * math.pi / 4; x, z = 1.0 * math.cos(a), 1.0 * math.sin(a)
        m.box(x - 0.25, y0 - 0.2 - (i % 2) * 0.5, z - 0.25, x + 0.25, y0 + 1.0, z + 0.25, (T, TD)[i % 2])
        m.box(x - 0.18, y0 - 0.4 - (i % 2) * 0.5, z - 0.18, x + 0.18, y0 - 0.2 - (i % 2) * 0.5, z + 0.18, TL)
    rbox(m, -1.3, y0 + 0.8, -1.3, 1.3, y0 + 3.6, 1.3, T, r=0.4)                          # mantle
    patches(m, 'x', 1.3, 1, -1.2, 1.2, y0 + 1.0, y0 + 3.4, 6, [TL, GL], 7, s=0.3)
    patches(m, 'x', -1.3, -1, -1.2, 1.2, y0 + 1.0, y0 + 3.4, 6, [TL, GL], 8, s=0.3)
    patches(m, 'z', 1.3, 1, -1.2, 1.2, y0 + 1.0, y0 + 3.4, 6, [TL, GL], 9, s=0.3)
    eyes(m, 0, y0 + 1.6, -1.3, 0.55, w=0.45, h=0.55, c='#0f3a3a')
    cheeks(m, 0, y0 + 1.25, -1.3, 0.9, c='#ff9fd2')
    for x, y in ((-2.0, 9.4), (1.8, 10.0)):
        m.box(x - 0.2, y, -0.2, x + 0.2, y + 0.4, 0.2, '#a6ffef80')

@design("dolphin_buddy", "Dolphin Buddy", "cute")
def _(m):
    B, BL, BD = '#7d9ab8', '#d6e2ee', '#5a7898'
    y0 = 4.6
    r = ('x', 22.5, (0, y0 + 2.6, 0))
    rbox(m, -0.9, y0 + 1.6, -1.6, 0.9, y0 + 3.4, 2.0, B, r=0.4, rot=r)                   # leaping body
    m.box(-0.75, y0 + 1.6, -1.4, 0.75, y0 + 2.1, 1.6, BL, rot=r)                        # pale belly
    m.box(-0.15, y0 + 3.4, 0.0, 0.15, y0 + 4.3, 0.9, BD, rot=r)                         # dorsal fin
    m.box(-0.5, y0 + 2.0, -2.6, 0.5, y0 + 2.6, -1.6, B, rot=r)                          # beak
    m.box(-0.35, y0 + 2.0, 2.0, 0.35, y0 + 2.8, 2.8, B, rot=r)
    m.box(-1.2, y0 + 2.2, 2.6, 1.2, y0 + 2.6, 3.2, BD, rot=r)                           # tail flukes
    for sd in (-1, 1):
        m.box(min(sd * 0.9, sd * 1.5), y0 + 1.8, -0.6, max(sd * 0.9, sd * 1.5), y0 + 2.0, 0.2, BD, rot=r)
        m.box(sd * 0.92 - (0.06 if sd > 0 else 0), y0 + 2.7, -1.2, sd * 0.92 + (0.06 if sd < 0 else 0), y0 + 3.1, -0.8, '#1a1418', rot=r)
    for x, y, z in ((-0.6, y0 + 0.3, -1.6), (0.7, y0 + 0.1, 1.2), (0.0, y0 + 0.0, 0.0)):
        m.box(x - 0.25, y, z - 0.25, x + 0.25, y + 0.5, z + 0.25, '#bfe8ffb0')            # splash
    m.box(-1.6, y0, -1.6, 1.6, y0 + 0.2, 1.6, '#5fb8f080')

@design("snow_golem_buddy", "Snow Golem Buddy", "cute")
def _(m):
    S, SS, P, PD, ST = '#f6f8fa', '#dfe6ee', '#e0862a', '#b8661c', '#6b4326'
    y0 = 4.6
    rbox(m, -1.3, y0, -1.3, 1.3, y0 + 2.2, 1.3, S, r=0.4)                                # lower snowball
    rbox(m, -1.0, y0 + 2.0, -1.0, 1.0, y0 + 3.6, 1.0, S, r=0.3)                          # upper snowball
    for sd in (-1, 1):
        r = ('z', -45 * sd, (sd * 1.0, y0 + 3.0, 0))
        m.box(min(sd * 1.0, sd * 2.4), y0 + 2.9, -0.1, max(sd * 1.0, sd * 2.4), y0 + 3.1, 0.1, ST, rot=r)   # stick arms
    m.box(-1.32, y0 + 0.3, -1.32, 1.32, y0 + 0.5, 1.32, SS)
    rbox(m, -1.2, y0 + 3.5, -1.2, 1.2, y0 + 5.9, 1.2, P, r=0.2)                          # carved pumpkin head
    for x in (-0.6, 0.0, 0.6):
        m.box(x - 0.04, y0 + 3.6, -1.24, x + 0.04, y0 + 5.8, -1.2, PD)
    m.box(-0.15, y0 + 5.9, -0.15, 0.15, y0 + 6.4, 0.15, '#4a7a2a')
    relief(m, [".EE.EE.", ".EE.EE.", ".......", "..MMM..", ".M...M."], -1.2,
           {'E': ('#3a2210', 0.06), 'M': ('#3a2210', 0.06)}, cell=0.3, top=y0 + 5.4)
    m.box(-0.75, y0 + 5.05, -1.29, -0.6, y0 + 5.2, -1.26, '#ffd27a'); m.box(0.3, y0 + 5.05, -1.29, 0.45, y0 + 5.2, -1.26, '#ffd27a')

@design("iron_golem_buddy", "Iron Golem Buddy", "cute")
def _(m):
    I, ID, IL, V, K = '#d8d4cc', '#a8a49c', '#eeebe4', '#4a8a3a', '#1a1418'
    y0 = 4.6
    for sd in (-1, 1):
        m.box(sd * 0.6 - 0.4, y0, -0.4, sd * 0.6 + 0.4, y0 + 1.0, 0.4, ID)               # legs
        m.box(min(sd * 1.4, sd * 2.0), y0 + 0.2, -0.35, max(sd * 1.4, sd * 2.0), y0 + 2.6, 0.35, I)   # long arms
    rbox(m, -1.4, y0 + 0.9, -0.8, 1.4, y0 + 2.8, 0.9, I, r=0.3)                          # chest
    for (x, y) in ((-1.0, y0 + 1.0), (0.6, y0 + 2.0), (1.1, y0 + 0.6)):
        m.box(x, y, -0.86, x + 0.2, y + 1.0, -0.8, V)                                     # vines
    rbox(m, -1.0, y0 + 2.6, -1.3, 1.0, y0 + 4.4, 0.6, I, r=0.25)                         # head
    m.box(-0.25, y0 + 2.6, -1.7, 0.25, y0 + 3.5, -1.3, ID)                              # big nose
    m.box(-0.9, y0 + 3.7, -1.36, 0.9, y0 + 3.95, -1.3, ID)                              # brow
    eyes(m, 0, y0 + 3.15, -1.3, 0.55, w=0.32, h=0.4, c='#8a1a1a')
    m.box(1.75, y0 + 2.6, -0.4, 1.85, y0 + 3.8, -0.3, '#3a7a2a')                        # poppy for you
    rbox(m, 1.45, y0 + 3.7, -0.65, 2.15, y0 + 4.3, -0.05, '#d62828', r=0.15)
    m.box(1.7, y0 + 3.9, -0.7, 1.9, y0 + 4.1, -0.65, K)

@design("villager_buddy", "Villager Buddy", "cute")
def _(m):
    SK, SKD, R, RD, K = '#c9a07a', '#a87e5a', '#7a4a26', '#5a3418', '#1a1418'
    y0 = 4.6
    rbox(m, -1.0, y0, -0.8, 1.0, y0 + 2.6, 0.8, R, r=0.3)                                # robe
    m.box(-1.05, y0, -0.85, 1.05, y0 + 0.3, 0.85, RD)
    m.box(-1.3, y0 + 1.4, -1.25, 1.3, y0 + 2.0, -0.6, R)                                # crossed arms
    m.box(-1.3, y0 + 1.5, -1.3, -0.9, y0 + 1.9, -1.25, SK); m.box(0.9, y0 + 1.5, -1.3, 1.3, y0 + 1.9, -1.25, SK)
    rbox(m, -1.0, y0 + 2.5, -1.0, 1.0, y0 + 4.9, 1.0, SK, r=0.3)                          # tall head
    m.box(-0.3, y0 + 2.5, -1.8, 0.3, y0 + 3.6, -1.0, SKD)                               # the nose
    m.box(-0.85, y0 + 3.85, -1.06, 0.85, y0 + 4.05, -1.0, '#5a3a20')                    # unibrow
    eyes(m, 0, y0 + 3.4, -1.0, 0.5, w=0.32, h=0.38, c='#2f8a32')
    cheeks(m, 0, y0 + 3.0, -1.0, 0.75, w=0.28)

@design("llama_buddy", "Llama Buddy", "cute")
def _(m):
    C, CD, K = '#efe3c8', '#d8c8a4', '#1a1418'
    y0 = 4.6
    legs4(m, C, 0.85, -0.8, 1.7, y0, 1.0, w=0.5)
    rbox(m, -1.3, y0 + 0.9, -1.2, 1.3, y0 + 2.6, 2.2, C, r=0.5)
    for i, c in enumerate(('#e8343f', '#f2a03a', '#4cc34a', '#2f6fd8')):                  # festive carpet
        m.box(-1.35, y0 + 2.2, -0.6 + i * 0.5, 1.35, y0 + 2.65, -0.1 + i * 0.5, c)
    m.box(-0.5, y0 + 2.2, -1.8, 0.5, y0 + 4.0, -1.0, C)                                 # neck
    rbox(m, -0.75, y0 + 3.6, -2.6, 0.75, y0 + 4.9, -1.1, C, r=0.3)                       # head
    rbox(m, -0.5, y0 + 3.6, -3.0, 0.5, y0 + 4.2, -2.5, CD, r=0.15)                       # snout
    for sd in (-1, 1):
        m.box(sd * 0.5 - 0.15, y0 + 4.9, -1.6, sd * 0.5 + 0.15, y0 + 5.5, -1.3, C)
    eyes(m, 0, y0 + 4.3, -2.6, 0.4, w=0.3, h=0.36)
    cheeks(m, 0, y0 + 4.0, -2.6, 0.6, w=0.25, h=0.18)
    m.box(-0.35, y0 + 4.9, -2.2, 0.35, y0 + 5.2, -1.6, CD)                               # fluffy top

@design("piglin_buddy", "Piglin Buddy", "cute")
def _(m):
    P, PD, BR, K = '#e6a08a', '#c8806a', '#6b4326', '#1a1418'
    y0 = 4.6
    for sd in (-1, 1):
        m.box(sd * 0.5 - 0.35, y0, -0.35, sd * 0.5 + 0.35, y0 + 1.0, 0.35, BR)
    rbox(m, -1.0, y0 + 0.9, -0.7, 1.0, y0 + 2.6, 0.7, BR, r=0.25)                        # tunic
    m.box(-1.02, y0 + 1.6, -0.72, 1.02, y0 + 1.8, 0.72, GOLD)                            # gold belt
    m.box(0.9, y0 + 1.2, -1.3, 1.6, y0 + 1.6, -0.7, GOLD)                               # gold ingot in hand
    m.box(1.0, y0 + 1.6, -0.8, 1.4, y0 + 2.4, -0.4, P)
    rbox(m, -1.4, y0 + 2.5, -1.3, 1.4, y0 + 4.6, 1.0, P, r=0.35)                         # wide head
    rbox(m, -0.65, y0 + 2.7, -1.75, 0.65, y0 + 3.5, -1.2, PD, r=0.15)                    # snout
    for sd in (-1, 1):
        m.box(sd * 0.28 - 0.12, y0 + 3.0, -1.8, sd * 0.28 + 0.12, y0 + 3.25, -1.75, '#8a4a3a')
        m.box(sd * 0.8 - 0.1, y0 + 2.5, -1.4, sd * 0.8 + 0.1, y0 + 2.9, -1.3, '#f4f2ee')   # tusks
        m.box(min(sd * 1.4, sd * 2.0), y0 + 3.0, -0.4, max(sd * 1.4, sd * 2.0), y0 + 4.0, 0.0, P,
              rot=('z', 22.5 * sd, (sd * 1.4, y0 + 4.0, 0)))                              # floppy ears
        m.box(sd * 1.3 - 0.15, y0 + 3.2, -1.36, sd * 1.3 + 0.15, y0 + 3.6, -1.3, GOLD)    # gold earrings
    eyes(m, 0, y0 + 3.7, -1.3, 0.6, w=0.36, h=0.42)
    cheeks(m, 0, y0 + 3.3, -1.3, 1.05, w=0.3)

@design("shulker_buddy", "Shulker Buddy", "cute")
def _(m):
    S, SD, Y, K = '#9a6aa8', '#7a4e8a', '#f2e070', '#1a1418'
    y0 = 4.6
    rbox(m, -1.6, y0, -1.6, 1.6, y0 + 1.6, 1.6, S, r=0.15)                               # lower shell
    m.box(-1.62, y0 + 1.3, -1.62, 1.62, y0 + 1.6, 1.62, SD)
    rbox(m, -1.0, y0 + 1.0, -1.0, 1.0, y0 + 2.6, 1.0, Y, r=0.3)                          # little head peeking
    eyes(m, 0, y0 + 1.8, -1.0, 0.4, w=0.3, h=0.42)
    cheeks(m, 0, y0 + 1.45, -1.0, 0.65, w=0.25)
    r = ('x', 22.5, (0, y0 + 2.1, 1.6))
    rbox(m, -1.6, y0 + 2.1, -1.6, 1.6, y0 + 3.6, 1.6, S, r=0.15, rot=r)                 # lid tipped open
    m.box(-1.62, y0 + 2.1, -1.62, 1.62, y0 + 2.4, 1.62, SD, rot=r)

@design("phantom_buddy", "Phantom Buddy", "cute")
def _(m):
    B, BD, G = '#4a5a8a', '#34406a', '#7af08a'
    GLOW.update({G})
    y0 = 5.4
    rbox(m, -0.9, y0, -1.2, 0.9, y0 + 0.9, 1.8, B, r=0.3)                                # body
    rbox(m, -1.0, y0, -2.4, 1.0, y0 + 1.1, -1.1, B, r=0.25)                              # head
    eyes(m, 0, y0 + 0.35, -2.4, 0.45, w=0.4, h=0.4, c=G, shine='#e8ffe8')
    for sd in (-1, 1):
        r = ('z', 22.5 * sd, (sd * 0.9, y0 + 0.6, 0))
        m.box(min(sd * 0.9, sd * 3.6), y0 + 0.5, -0.8, max(sd * 0.9, sd * 3.6), y0 + 0.7, 1.4, BD, rot=r)   # wings
        m.box(min(sd * 0.9, sd * 3.6), y0 + 0.7, -0.85, max(sd * 0.9, sd * 3.6), y0 + 0.75, -0.6, '#8a9ac8', rot=r)
    m.box(-0.4, y0 + 0.2, 1.8, 0.4, y0 + 0.6, 3.0, BD)                                  # tail
    m.box(-0.12, 4.6, -0.12, 0.12, y0, 0.12, '#4a5a8a60')

@design("ocelot_buddy", "Ocelot Buddy", "cute")
def _(m):
    Y, YD, SP, K = '#e8c25a', '#c8a03a', '#7a5a2a', '#1a1418'
    y0 = 4.6
    rbox(m, -1.1, y0, -0.6, 1.1, y0 + 2.2, 1.6, Y, r=0.45)                               # sitting body
    for sd in (-1, 1):
        m.box(sd * 0.55 - 0.3, y0, -1.1, sd * 0.55 + 0.3, y0 + 1.2, -0.6, Y)
    patches(m, 'x', 1.1, 1, -0.4, 1.4, y0 + 0.4, y0 + 2.0, 5, [SP], 3, s=0.3)
    patches(m, 'x', -1.1, -1, -0.4, 1.4, y0 + 0.4, y0 + 2.0, 5, [SP], 4, s=0.3)
    rbox(m, -1.1, y0 + 2.0, -1.4, 1.1, y0 + 3.8, 0.6, Y, r=0.35)                         # head
    for sd in (-1, 1):
        steps(m, sd * 0.65, -0.4, y0 + 3.8, [0.6, 0.4, 0.2], Y, depth=0.3, h=0.28, smooth=1)
    eyes(m, 0, y0 + 2.9, -1.4, 0.5, w=0.36, h=0.42, c='#2f8a32')
    m.box(-0.15, y0 + 2.6, -1.46, 0.15, y0 + 2.8, -1.4, '#d87a8a')
    for sd in (-1, 1):
        m.box(min(sd * 0.6, sd * 1.4), y0 + 2.55, -1.6, max(sd * 0.6, sd * 1.4), y0 + 2.6, -1.55, '#f4f2ee')
    for k in range(4):                                                                  # striped tail wrapped round
        m.box(-1.3 + k * 0.7, y0, 1.6, -0.7 + k * 0.7, y0 + 0.5, 2.1, (Y, SP)[k % 2])

# ---------- B: mob masks ----------
def mask8(m, base, rows=None, spec=None, r=4.6, tex=None, seed=1):
    """Full-head mob mask: a cube just outside the hat layer with an 8x8 pixel face on the front."""
    m.box(-r, -r, -r, r, r, r, base)
    if rows:
        relief(m, rows, -r, {k: (c, 0.06) for k, c in spec.items()}, cell=2 * r / 8, top=r)
    if tex:
        for ax, pl, out in (('x', r, 1), ('x', -r, -1), ('z', r, 1)):
            patches(m, ax, pl, out, -r, r, -r, r, 14, tex, seed + int(pl * 7) + (3 if ax == 'z' else 0), s=2 * r / 8)
        patches(m, 'y', r, 1, -r, r, -r, r, 14, tex, seed + 50, s=2 * r / 8)

@design("enderman_mask", "Enderman Mask", "mob")
def _(m):
    GLOW.update({'#e079fa', '#cc00fa'})
    mask8(m, '#161616', ["........", "........", "........", "........", "eEe..eEe", "........", "........", "........"],
          {'e': '#e079fa', 'E': '#cc00fa'}, tex=['#0e0e0e', '#1f1f22'])
    for x, y in ((-5.6, 2.0), (5.4, -1.0), (-4.8, 6.0), (3.6, 6.8)):
        m.box(x - 0.2, y, -1.0, x + 0.2, y + 0.4, -0.6, '#e079fa')

@design("zombie_mask", "Zombie Mask", "mob")
def _(m):
    mask8(m, '#4f8a3a', ["dddddddd", "d......d", "........", "........", ".kk..kk.", "...nn...", "..mmmm..", "........"],
          {'d': '#3a6e2a', 'k': '#1d2a1a', 'n': '#3a6a2a', 'm': '#2a4a22'}, tex=['#3f7a2e', '#5f9a48'])

@design("skeleton_mask", "Skeleton Mask", "mob")
def _(m):
    mask8(m, '#c9c9c9', ["........", "........", "........", ".kk..kk.", ".kk..kk.", "...nn...", ".mmmmmm.", "........"],
          {'k': '#2a2a2a', 'n': '#6a6a6a', 'm': '#5a5a5a'}, tex=['#b4b4b4', '#d8d8d8'])
    for x in (-2.3, -1.15, 0.0, 1.15, 2.3):
        m.box(x - 0.06, -3.45, -4.68, x + 0.06, -2.3, -4.6, '#c9c9c9')                    # teeth gaps

@design("spider_mask", "Spider Mask", "mob")
def _(m):
    GLOW.update({'#ff4a3a'})
    mask8(m, '#2e2620', ["........", "........", "..r..r..", "........", ".RR..RR.", ".RR..RR.", "........", "...ff..."],
          {'r': '#ff4a3a', 'R': '#c8201a', 'f': '#5a4a3a'}, tex=['#241e1a', '#3a302a'])
    for sd in (-1, 1):
        for z in (-2.6, -0.6, 1.4, 3.2):                                                 # bent legs on each side
            x1, x2 = sorted((sd * 4.6, sd * 6.8))
            m.box(x1, 0.6, z - 0.3, x2, 1.2, z + 0.3, '#2e2620')
            x1, x2 = sorted((sd * 6.2, sd * 6.8))
            m.box(x1, -2.6, z - 0.3, x2, 0.6, z + 0.3, '#2e2620')

@design("pig_mask", "Pig Mask", "mob")
def _(m):
    mask8(m, '#f0a0b0', ["........", "........", "........", ".wk..kw.", "........", "........", "........", "........"],
          {'w': '#ffffff', 'k': '#1a1418'}, tex=['#e890a2', '#f8b8c4'])
    rbox(m, -2.3, -3.4, -5.6, 2.3, -0.9, -4.6, '#f8c0cc', r=0.4)
    for sd in (-1, 1):
        m.box(sd * 1.0 - 0.45, -2.6, -5.66, sd * 1.0 + 0.45, -1.7, -5.6, '#c06a7c')

@design("cow_mask", "Cow Mask", "mob")
def _(m):
    mask8(m, '#f4f2ee', ["KKK.....", "KKK...KK", "KK......", ".kw..wk.", "........", "........", "........", "........"],
          {'K': '#2a2226', 'k': '#1a1418', 'w': '#ffffff'}, tex=['#2a2226', '#f4f2ee', '#e8e4dc'])
    rbox(m, -2.6, -4.6, -5.5, 2.6, -1.6, -4.6, '#c9b0a4', r=0.4)
    for sd in (-1, 1):
        m.box(sd * 1.2 - 0.4, -2.8, -5.56, sd * 1.2 + 0.4, -2.2, -5.5, '#5a3a3a')
        m.box(sd * 3.4 - 0.4, 4.6, -1.2, sd * 3.4 + 0.4, 6.4, -0.4, '#e8e0c8')              # horns
        m.box(min(sd * 4.6, sd * 6.0), 1.6, -1.6, max(sd * 4.6, sd * 6.0), 2.6, -0.4, '#2a2226')   # ears

@design("sheep_hood", "Sheep Hood", "mob")
def _(m):
    W, WS, F = '#f4f2ee', '#e2ded6', '#e8cdb0'
    dome(m, 4.0, [(5.2, 1.2), (4.4, 0.6)], W)
    m.box(-5.2, -4.0, 4.0, 5.2, 4.6, 5.2, W)                                             # back
    for sd in (-1, 1):
        m.box(min(sd * 4.0, sd * 5.2), -4.0, -5.2, max(sd * 4.0, sd * 5.2), 4.6, 4.0, W)   # sides
        m.box(min(sd * 3.2, sd * 4.0), -4.0, -5.2, max(sd * 3.2, sd * 4.0), 4.6, -4.0, W)  # face frame
        m.box(min(sd * 5.2, sd * 6.6), 1.4, -1.6, max(sd * 5.2, sd * 6.6), 2.2, -0.4, F)  # ears
    m.box(-4.0, 2.8, -5.2, 4.0, 4.6, -4.0, W)
    import random as _r
    rnd = _r.Random(3)
    for _ in range(26):                                                                 # fluffy bumps
        x, y = rnd.uniform(-5.0, 4.0), rnd.uniform(-3.8, 5.4)
        z = rnd.choice((-5.4, 5.2)) if abs(x) < 3 else rnd.uniform(-4.8, 4.0)
        if abs(x) < 3.2 and y < 2.8 and z < 0:
            continue
        rbox(m, x, y, z, x + 1.0, y + 0.9, z + 0.4 if z > 5 or z < -5 else z + 1.0, (W, WS)[rnd.random() < 0.4], r=0.2)

@design("villager_nose", "Villager Nose", "mob")
def _(m):
    rbox(m, -1.15, -3.4, -6.6, 1.15, 0.2, -4.6, '#b88a64', r=0.25)                       # hmm
    m.box(-1.15, -3.4, -6.62, 1.15, -3.0, -4.6, '#a07a54')
    m.box(-3.6, 0.4, -4.8, 3.6, 1.1, -4.6, '#4a2e1a')                                    # unibrow

@design("iron_golem_mask", "Iron Golem Mask", "mob")
def _(m):
    mask8(m, '#d8d4cc', None, tex=['#c8c4bc', '#e8e4dc', '#b8b4ac'])
    m.box(-4.6, 0.4, -5.4, 4.6, 1.6, -4.6, '#c8c4bc')                                    # brow ridge
    for sd in (-1, 1):
        m.box(sd * 2.3 - 0.6, -0.6, -4.68, sd * 2.3 + 0.6, 0.4, -4.6, '#8a1a1a')
    rbox(m, -1.15, -3.6, -6.0, 1.15, 0.6, -4.6, '#c8c4bc', r=0.2)                        # golem nose
    for (x, y, h) in ((-4.0, -4.6, 6.0), (3.4, -4.6, 3.2), (-2.6, 2.0, 2.6)):
        m.box(x, y, -4.68, x + 0.5, y + h, -4.6, '#4a8a3a')                               # vines
    m.box(4.6, -2.0, -2.0, 4.66, 3.0, -1.5, '#4a8a3a'); m.box(-4.66, -4.0, 1.0, -4.6, 1.0, 1.5, '#4a8a3a')
    for x, y in ((1.8, 2.6), (-3.4, -3.0)):
        m.box(x, y, -4.66, x + 0.9, y + 0.12, -4.6, '#8c887f')                             # cracks

@design("blaze_mask", "Blaze Mask", "mob")
def _(m):
    mask8(m, '#f2c33a', ["........", "........", "........", ".kk..kk.", "........", "........", "..mmmm..", "........"],
          {'k': '#3a1a0a', 'm': '#c8781a'}, tex=['#e0a020', '#fff070', '#d89018'])
    for x, z in ((-5.8, -5.8), (5.8, -5.8), (-5.8, 5.8), (5.8, 5.8)):
        m.box(x - 0.45, -3.0, z - 0.45, x + 0.45, 2.6, z + 0.45, '#ffc21f')               # floating rods
        m.box(x - 0.47, -1.0, z - 0.47, x + 0.47, -0.6, z + 0.47, '#d9861a')
    for x, y in ((-2.0, 5.6), (1.4, 6.4), (2.8, 5.2)):
        m.box(x - 0.4, y, -0.4, x + 0.4, y + 0.8, 0.4, '#5a5a62a0')

@design("wither_skull_mask", "Wither Skull Mask", "mob")
def _(m):
    mask8(m, '#2b2b2f', ["........", "........", "........", ".ee..ee.", "........", "...nn...", ".tttttt.", ".t.tt.t."],
          {'e': '#c9ced8', 'n': '#18181b', 't': '#8c8f99'}, tex=['#232327', '#36363b'])

@design("piglin_mask", "Piglin Mask", "mob")
def _(m):
    mask8(m, '#e6a08a', ["........", "........", ".bb..bb.", ".wk..kw.", "........", "........", "........", "........"],
          {'b': '#6b4326', 'w': '#ffffff', 'k': '#1a1418'}, tex=['#d8907a', '#f2b8a0'])
    rbox(m, -2.0, -3.4, -5.8, 2.0, -0.8, -4.6, '#f2b8a0', r=0.35)
    for sd in (-1, 1):
        m.box(sd * 0.9 - 0.35, -2.4, -5.86, sd * 0.9 + 0.35, -1.7, -5.8, '#8a4a3a')
        m.box(sd * 2.6 - 0.3, -4.6, -5.2, sd * 2.6 + 0.3, -3.0, -4.6, '#f4f2ee')          # tusks
        m.box(min(sd * 4.6, sd * 6.4), 0.4, -1.6, max(sd * 4.6, sd * 6.4), 3.4, -0.4, '#e6a08a',
              rot=('z', 22.5 * sd, (sd * 4.6, 3.4, -1.0)))                               # floppy ears
        m.box(min(sd * 4.6, sd * 4.9), -1.0, -2.0, max(sd * 4.6, sd * 4.9), 0.0, -1.4, GOLD)

@design("guardian_eye_hat", "Guardian Buddy", "mob")
def _(m):
    T, TD, O, K = '#5aa89a', '#3e8a7e', '#e8803a', '#3a1a5a'
    y0 = 4.6
    rbox(m, -2.2, y0, -2.2, 2.2, y0 + 3.6, 2.2, T, r=0.3)
    patches(m, 'x', 2.2, 1, -2.0, 2.0, y0 + 0.2, y0 + 3.4, 6, [TD, '#7ac8b8'], 2, s=0.55)
    patches(m, 'x', -2.2, -1, -2.0, 2.0, y0 + 0.2, y0 + 3.4, 6, [TD, '#7ac8b8'], 3, s=0.55)
    m.box(-1.2, y0 + 1.0, -2.26, 1.2, y0 + 2.6, -2.2, '#f4f2ee')                          # big eye
    m.box(-0.4, y0 + 1.3, -2.3, 0.4, y0 + 2.2, -2.26, K)
    m.box(-0.1, y0 + 1.9, -2.32, 0.15, y0 + 2.1, -2.3, '#ffffff')
    for (x, y, z, ax) in ((0, y0 + 3.6, 0, 'y'), (-2.2, y0 + 1.8, 0, 'x'), (2.2, y0 + 1.8, 0, 'x'), (0, y0 + 1.8, 2.2, 'z'),
                          (-1.4, y0 + 3.6, -1.4, 'y'), (1.4, y0 + 3.6, 1.4, 'y'), (-2.2, y0 + 3.2, -1.6, 'x'), (2.2, y0 + 0.6, 1.4, 'x')):
        if ax == 'y':
            m.box(x - 0.2, y, z - 0.2, x + 0.2, y + 1.0, z + 0.2, O)
        elif ax == 'x':
            x1, x2 = sorted((x, x + (1.0 if x > 0 else -1.0)))
            m.box(x1, y - 0.2, z - 0.2, x2, y + 0.2, z + 0.2, O)
        else:
            m.box(x - 0.2, y - 0.2, z, x + 0.2, y + 0.2, z + 1.0, O)                      # spikes
    for k in range(3):
        m.box(-0.6 + 0.15 * k, y0 + 1.2, 2.2 + k * 0.9, 0.6 - 0.15 * k, y0 + 2.2, 3.1 + k * 0.9, (T, TD)[k % 2])
    m.box(-0.8, y0 + 1.4, 4.9, 0.8, y0 + 2.0, 5.3, O)

@design("slime_helmet", "Slime Helmet", "mob")
def _(m):
    K = '#1e3a1a'
    m.box(-5.2, -5.2, -5.2, 5.2, 5.2, 5.2, '#7ad35a70')                                  # jelly
    for sd in (-1, 1):
        m.box(sd * 2.2 - 0.9, 2.0, -5.3, sd * 2.2 + 0.9, 3.6, -5.2, K)
        m.box(sd * 2.2 + 0.1, 3.0, -5.32, sd * 2.2 + 0.6, 3.5, -5.3, '#e6ffd8')
    m.box(-0.6, 1.0, -5.3, 0.6, 1.5, -5.2, K)
    m.box(-4.6, 4.4, -5.26, -3.2, 4.8, -5.2, '#e6ffd8c0')                                # shine
    for x, z in ((-3.0, -1.0), (2.4, 2.0)):
        rbox(m, x - 0.6, 5.2, z - 0.6, x + 0.6, 6.2, z + 0.6, '#7ad35a90', r=0.2)         # baby slimes bouncing

@design("magma_cube_helmet", "Magma Cube Helmet", "mob")
def _(m):
    D, DL, O, Y = '#4a1410', '#6a2018', '#ff8a1f', '#ffd23a'
    GLOW.update({O, Y})
    m.box(-4.5, -4.5, -4.5, 4.5, 4.5, 4.5, O)                                           # glowing core
    for i, (y1, y2) in enumerate(((-4.8, -3.0), (-2.4, -0.8), (-0.2, 1.6), (2.2, 4.0), (4.0, 4.8))):
        m.box(-4.8 - 0.1 * (i % 2), y1, -4.8 - 0.1 * (i % 2), 4.8 + 0.1 * (i % 2), y2, 4.8 + 0.1 * (i % 2), D)
        patches(m, 'z', -4.8 - 0.1 * (i % 2), -1, -4.6, 4.6, y1 + 0.1, y2 - 0.1, 4, [DL, '#2a0a08'], i + 2, s=0.6)
    for sd in (-1, 1):
        m.box(sd * 1.8 - 0.9, 0.2, -5.0, sd * 1.8 + 0.9, 1.3, -4.8, Y)                   # eyes
        m.box(sd * 1.8 - 0.3, 0.2, -5.04, sd * 1.8 + 0.3, 0.9, -5.0, '#c8201a')

@design("shulker_helmet", "Shulker Helmet", "mob")
def _(m):
    S, SD, Y = '#9a6aa8', '#7a4e8a', '#f2e070'
    m.box(-5.0, -4.6, 4.0, 5.0, 2.4, 5.0, S)                                             # back
    for sd in (-1, 1):
        m.box(min(sd * 4.0, sd * 5.0), -4.6, -5.0, max(sd * 4.0, sd * 5.0), 2.4, 4.0, S)
    m.box(-5.05, -4.6, -5.05, 5.05, -3.8, 5.05, SD)
    r = ('x', 22.5, (0, 3.0, 5.0))
    m.box(-5.0, 2.6, -5.0, 5.0, 5.6, 5.0, S, rot=r)                                      # lid tipped open
    m.box(-5.05, 2.6, -5.05, 5.05, 3.2, 5.05, SD, rot=r)
    rbox(m, -1.6, 4.3, -2.6, 1.6, 5.8, 0.4, Y, r=0.3)                                    # head peeking from inside
    eyes(m, 0, 4.8, -2.6, 0.6, w=0.4, h=0.5)

@design("ghast_mask", "Ghast Mask", "mob")
def _(m):
    mask8(m, '#f0f0f0', ["........", "........", "........", ".kk..kk.", "..t..t..", "..t..t..", "...mm...", "...mm..."],
          {'k': '#3a3a3a', 't': '#9ab8d8', 'm': '#3a3a3a'}, tex=['#e4e4e4', '#fafafa'])
    import random as _r
    rnd = _r.Random(2)
    for x in (-3.4, -1.1, 1.1, 3.4):
        for z in (-3.4, 0.0, 3.4):
            if z > -1 and abs(x) < 2:
                continue
            m.box(x - 0.4, -4.6 - rnd.uniform(1.0, 2.2), z - 0.4, x + 0.4, -4.6, z + 0.4, '#e8e8e8')   # tentacles

@design("snow_golem_head", "Snowman Mask", "mob")
def _(m):
    mask8(m, '#f6f8fa', None, tex=['#e2e8ee', '#ffffff'])
    for sd in (-1, 1):
        rbox(m, sd * 1.9 - 0.55, 0.0, -5.2, sd * 1.9 + 0.55, 1.1, -4.6, '#2a2a2e', r=0.2)  # coal eyes
        r = ('z', -45 * sd, (sd * 4.6, -0.5, 0))
        m.box(min(sd * 4.6, sd * 7.4), -0.7, -0.2, max(sd * 4.6, sd * 7.4), -0.3, 0.2, '#6b4326', rot=r)   # stick arms
    steps(m, 0, 0, -1.6, [1.2, 0.9, 0.6, 0.3], ORANGE, h=0.6, smooth=1) if False else None
    for k, w in enumerate((1.1, 0.85, 0.6, 0.35)):
        m.box(-w / 2, -1.6 - w / 2 + 0.3, -5.6 - k * 0.7, w / 2, -1.6 + w / 2 + 0.3, -4.6 - k * 0.7, ORANGE)   # carrot
    for x in (-2.0, -1.0, 0.0, 1.0, 2.0):
        m.box(x - 0.3, -3.6 + abs(x) * 0.35, -4.9, x + 0.3, -3.0 + abs(x) * 0.35, -4.6, '#2a2a2e')   # coal smile

@design("drowned_mask", "Drowned Mask", "mob")
def _(m):
    GLOW.update({'#7af7ff'})
    mask8(m, '#3a8a7a', ["ssssssss", "s.....ss", "........", "........", ".ee..ee.", "........", "..mmmm..", "........"],
          {'s': '#2a5a4a', 'e': '#7af7ff', 'm': '#1a3a32'}, tex=['#2a6a5a', '#5aa898'])
    for sd in (-1, 1):
        for z, ln in ((-2.6, 4.0), (0.4, 6.4), (3.0, 3.0)):
            x1, x2 = sorted((sd * 4.6, sd * 4.95))
            m.box(x1, 4.6 - ln, z - 0.3, x2, 4.6, z + 0.3, '#3a8a3a')                        # seaweed
    for x in (-2.0, 1.0, 2.6):
        m.box(x - 0.25, 4.6, -1.0, x + 0.25, 6.6 + x * 0.3, -0.5, '#4cc34a')

@design("stray_hood", "Stray Hood", "mob")
def _(m):
    H, HD = '#4a5a5e', '#36444a'
    mask8(m, '#b8c6c8', ["........", "........", "........", ".kk..kk.", ".kk..kk.", "...nn...", ".mmmmmm.", "........"],
          {'k': '#2a3436', 'n': '#6a7a7c', 'm': '#5a6a6c'}, tex=['#a8b6b8', '#c8d6d8'])
    dome(m, 4.6, [(5.0, 0.7), (4.2, 0.5)], H)
    m.box(-5.0, -4.6, 4.6, 5.0, 4.8, 5.2, H)
    for sd in (-1, 1):
        m.box(min(sd * 4.6, sd * 5.2), -4.6, -4.4, max(sd * 4.6, sd * 5.2), 4.8, 5.2, H)
    m.box(-5.0, 2.4, -5.2, 5.0, 4.8, -4.6, H)
    for x in (-4.0, -2.0, 0.6, 2.8):
        m.box(x, 1.8, -5.25, x + 1.0, 2.4, -4.8, HD)                                      # ragged edge
    for x in (-4.8, 4.8):
        for z in (-3.0, 0.0, 3.0):
            m.box(x - 0.3, -5.6 + abs(z) * 0.2, z - 0.4, x + 0.3, -4.6, z + 0.4, HD)

@design("bee_hive_hat", "Beehive Hat", "mob")
def _(m):
    H, HD, HN = '#e8c070', '#c89a40', '#f2a01f'
    rbox(m, -2.6, 4.6, -2.6, 2.6, 8.6, 2.6, H, r=0.2)
    for y in (5.4, 6.4, 7.4):
        m.box(-2.65, y, -2.65, 2.65, y + 0.2, 2.65, HD)
    m.box(-0.8, 5.8, -2.7, 0.8, 6.8, -2.6, '#4a2e1a')                                   # entrance
    m.box(-0.4, 4.8, -2.75, 0.2, 5.8, -2.6, HN)                                         # honey drip
    m.box(-2.7, 8.4, -2.7, 2.7, 8.8, 2.7, '#a8783a')
    for (x, y, z) in ((-3.8, 7.6, -1.0), (3.6, 6.4, 0.8), (1.4, 9.6, -1.8)):             # tiny bees
        m.box(x - 0.4, y, z - 0.3, x + 0.4, y + 0.6, z + 0.3, '#f2c23a')
        m.box(x - 0.1, y - 0.01, z - 0.31, x + 0.1, y + 0.61, z + 0.31, '#3d2a1c')
        m.box(x - 0.3, y + 0.6, z - 0.1, x + 0.3, y + 0.65, z + 0.4, '#eef8ffaa')

@design("chest_mimic", "Chest Mimic", "mob")
def _(m):
    W, WD, MO, T = '#b07a3a', '#6b4a20', '#7a1a2a', '#f4f2ee'
    m.box(-4.9, -4.9, -4.9, 4.9, -1.4, 4.9, W)                                           # lower jaw
    m.box(-4.95, -2.0, -4.95, 4.95, -1.4, 4.95, WD)
    r = ('x', 22.5, (0, -1.0, 4.9))
    m.box(-4.9, -1.0, -4.9, 4.9, 4.9, 4.9, W, rot=r)                                     # lid, open
    m.box(-4.95, -1.0, -4.95, 4.95, -0.4, 4.95, WD, rot=r)
    m.box(-0.6, -1.6, -5.25, 0.6, 0.4, -4.95, GOLD, rot=r)                               # latch
    for k in range(7):
        x = -3.9 + k * 1.3
        m.box(x - 0.3, -1.4, -5.0, x + 0.3, -0.5, -4.6, T)                                # bottom teeth
        m.box(x - 0.3 + 0.6, -1.6, -5.0, x + 0.3 + 0.6, -0.8, -4.6, T, rot=r)             # top teeth
    m.box(-1.6, -1.6, -6.4, 1.6, -1.3, -4.9, '#e05a7a')                                 # tongue
    m.box(-1.0, -1.7, -6.6, 1.0, -1.3, -6.4, '#e05a7a')
    for x in (-4.95, 4.95):
        m.box(x - 0.05, -4.9, -4.95, x + 0.05, -1.4, -4.4, WD)

@design("crafting_table_hat", "Crafting Table Hat", "mob")
def _(m):
    W, WD, WL = '#b07a3a', '#6b4a20', '#c8925a'
    m.box(-2.4, 4.6, -2.4, 2.4, 9.0, 2.4, W)
    m.box(-2.45, 8.4, -2.45, 2.45, 9.0, 2.45, '#8a5a2a')
    for k in range(4):
        m.box(-2.4 + k * 1.2 + 1.15, 9.0, -2.4, -2.4 + k * 1.2 + 1.25, 9.06, 2.4, WD)         # crafting grid
        m.box(-2.4, 9.0, -2.4 + k * 1.2 + 1.15, 2.4, 9.06, -2.4 + k * 1.2 + 1.25, WD)
    m.box(-1.6, 5.4, -2.46, -0.2, 7.6, -2.4, '#8c8f99'); m.box(-1.0, 7.6, -2.46, -0.8, 8.2, -2.4, WD)   # saw
    m.box(0.6, 6.4, -2.46, 1.8, 7.0, -2.4, '#5a5d66'); m.box(1.0, 5.2, -2.46, 1.4, 6.4, -2.4, WD)     # hammer
    patches(m, 'x', 2.4, 1, -2.4, 2.4, 4.8, 8.4, 6, [WD, WL], 4, s=0.5)
    patches(m, 'x', -2.4, -1, -2.4, 2.4, 4.8, 8.4, 6, [WD, WL], 5, s=0.5)

@design("creeper_hood", "Creeper Hoodie Hood", "mob")
def _(m):
    G, GD, K = '#5fae46', '#3f8a32', '#1d2a1a'
    dome(m, 4.0, [(5.0, 1.0), (4.4, 0.5)], G)
    m.box(-5.0, -4.6, 4.0, 5.0, 4.6, 5.0, G)
    for sd in (-1, 1):
        m.box(min(sd * 4.0, sd * 5.0), -4.6, -5.0, max(sd * 4.0, sd * 5.0), 4.6, 4.0, G)
        m.box(sd * 2.4 - 0.12, -6.6, -5.1, sd * 2.4 + 0.12, -4.0, -4.9, '#e8e4dc')         # drawstrings
        m.box(sd * 2.4 - 0.2, -6.9, -5.15, sd * 2.4 + 0.2, -6.6, -4.85, '#c9ced8')
    m.box(-5.0, 2.6, -5.2, 5.0, 4.6, -4.0, G)                                            # hood brim
    m.box(-5.0, -4.6, -5.2, -3.6, 2.6, -4.0, G); m.box(3.6, -4.6, -5.2, 5.0, 2.6, -4.0, G)
    m.box(-5.0, 2.55, -5.25, 5.0, 2.75, -5.2, GD)
    relief(m, ["........", ".EE..EE.", ".EE..EE.", "...MM...", "..MMMM..", "..M..M.."], -1.0,
           {'E': (K, 0.06), 'M': (K, 0.06)}, cell=0.5, top=1.0) if False else None
    for (x1, y1, x2, y2) in ((-2.0, 5.6, -1.0, 6.4), (1.0, 5.6, 2.0, 6.4), (-0.5, 5.2, 0.5, 5.6), (-1.0, 4.6, 1.0, 5.2)):
        m.box(x1, y1, -4.72, x2, y2, -4.66, K) if False else None
    for (x1, z1, x2, z2) in ((-2.0, -3.2, -0.8, -2.0), (0.8, -3.2, 2.0, -2.0), (-0.6, -2.0, 0.6, -1.0), (-1.2, -1.0, 1.2, 0.4),
                             (-1.2, 0.4, -0.6, 1.0), (0.6, 0.4, 1.2, 1.0)):
        m.box(x1, 5.5, z1, x2, 5.56, z2, K)                                               # creeper face on top of the hood
    patches(m, 'x', 5.0, 1, -4.8, 4.8, -4.4, 4.4, 12, [GD, '#8fd06a'], 6, s=0.8)
    patches(m, 'x', -5.0, -1, -4.8, 4.8, -4.4, 4.4, 12, [GD, '#8fd06a'], 7, s=0.8)

@design("warden_mask", "Warden Mask", "mob")
def _(m):
    GLOW.update({'#29dfeb'})
    mask8(m, '#0f3a42', ["........", "........", ".kk..kk.", ".kk..kk.", "........", ".cc..cc.", "..mmmm..", "..mmmm.."],
          {'k': '#062026', 'c': '#29dfeb', 'm': '#062026'}, tex=['#1a5560', '#0a2a30'])
    for sd in (-1, 1):
        x = sd * 4.0; r = ('z', -22.5 * sd, (x, 4.6, 0))
        m.box(x - 0.8, 4.6, -0.4, x + 0.8, 7.8, 0.4, '#173d47', rot=r)
        m.box(x - 0.4, 5.0, -0.5, x + 0.4, 7.4, -0.4, '#29dfeb', rot=r)

# ---------- C: Minecraft blocks + items ----------
def note_icon(m, x, y, z, c, s=1.0):
    m.box(x - 0.35 * s, y, z - 0.08, x + 0.15 * s, y + 0.4 * s, z + 0.08, c)
    m.box(x + 0.05 * s, y + 0.3 * s, z - 0.08, x + 0.2 * s, y + 1.3 * s, z + 0.08, c)
    m.box(x + 0.05 * s, y + 1.15 * s, z - 0.08, x + 0.6 * s, y + 1.3 * s, z + 0.08, c)

@design("diamond_ore_hat", "Diamond Ore Hat", "cool")
def _(m):
    ST, STD, STL, DI, DIL = '#8a8a8a', '#6e6e6e', '#a2a2a2', '#4fd8e8', '#c8fbff'
    m.box(-2.4, 4.6, -2.4, 2.4, 9.4, 2.4, ST)
    for ax, pl, out, a1, a2 in (('z', -2.4, -1, -2.4, 2.4), ('x', 2.4, 1, -2.4, 2.4), ('x', -2.4, -1, -2.4, 2.4), ('z', 2.4, 1, -2.4, 2.4)):
        patches(m, ax, pl, out, a1, a2, 4.7, 9.3, 8, [STD, STL], int(pl * 10) + 3, s=0.6)
        patches(m, ax, pl, out * 1.5, a1 + 0.4, a2 - 0.4, 5.0, 9.0, 4, [DI, DI, DIL], int(pl * 10) + 9, s=0.6)
    patches(m, 'y', 9.4, 1, -2.2, 2.2, -2.2, 2.2, 5, [DI, STD], 11, s=0.6)
    r = ('z', 45, (0.6, 10.2, 0))                                                       # pickaxe stuck in the top
    m.box(0.45, 9.0, -0.15, 0.75, 12.4, 0.15, '#6b4326', rot=r)
    m.box(-0.8, 12.0, -0.2, 2.0, 12.5, 0.2, '#4fd8e8', rot=r)

@design("beacon_hat", "Beacon Hat", "cool")
def _(m):
    GLOW.update({'#7af7ff'})
    m.box(-3.0, 4.6, -3.0, 3.0, 5.1, 3.0, '#d8d4cc')                                     # iron base
    m.box(-3.05, 4.95, -3.05, 3.05, 5.15, 3.05, GOLD)
    m.box(-2.0, 5.1, -2.0, 2.0, 5.7, 2.0, '#1a1028')                                     # obsidian
    rbox(m, -1.1, 5.7, -1.1, 1.1, 7.9, 1.1, '#7af7ff', r=0.3)                            # core
    m.box(-2.0, 5.1, -2.0, 2.0, 9.1, 2.0, '#d8f8ff60')                                   # glass
    m.box(-0.5, 9.1, -0.5, 0.5, 16.0, 0.5, '#7af7ff70')                                  # beam

@design("jukebox_hat", "Jukebox Hat", "cool")
def _(m):
    W, WD, K = '#7a4e2e', '#4b2d17', '#1d1b22'
    m.box(-2.4, 4.6, -2.4, 2.4, 8.6, 2.4, W)
    m.box(-2.45, 8.0, -2.45, 2.45, 8.6, 2.45, WD)
    m.box(-2.45, 4.6, -2.45, 2.45, 5.0, 2.45, WD)
    m.box(-1.6, 8.6, -0.3, 1.6, 8.7, 0.3, K)                                             # slot
    rbox(m, -2.0, 8.7, -2.0, 2.0, 8.9, 2.0, K, r=0.8)                                     # spinning disc
    rbox(m, -0.6, 8.9, -0.6, 0.6, 8.95, 0.6, '#e8343f', r=0.2)
    for (x, y, c) in ((-3.0, 9.6, '#4cc3ff'), (2.6, 10.4, '#ff5ce1'), (-0.4, 11.4, '#ffe45c')):
        note_icon(m, x, y, -1.0, c)

@design("enchant_table_hat", "Enchanting Table Hat", "cool")
def _(m):
    OB, RD, DI, BK = '#1a1028', '#a81a2a', '#4fd8e8', '#7a1a1a'
    GLOW.update({'#c49bff'})
    m.box(-2.4, 4.6, -2.4, 2.4, 7.0, 2.4, OB)
    m.box(-2.45, 6.4, -2.45, 2.45, 7.05, 2.45, RD)                                        # red cloth top
    for x in (-2.1, 2.1):
        for z in (-2.1, 2.1):
            m.box(x - 0.35, 6.3, z - 0.35, x + 0.35, 7.1, z + 0.35, DI)                    # diamond corners
    for sd in (-1, 1):                                                                  # floating open book
        r = ('z', -22.5 * sd, (0, 8.4, 0))
        x1, x2 = sorted((0, sd * 1.8))
        m.box(x1, 8.3, -1.2, x2, 8.5, 1.2, BK, rot=r)
        m.box(x1, 8.5, -1.05, x2, 8.7, 1.05, '#f4ecd8', rot=r)
    for x, y, z in ((-2.6, 8.8, -1.0), (2.4, 9.4, 0.6), (-1.0, 10.2, 1.0), (1.4, 7.6, -2.2)):
        m.box(x - 0.18, y, z - 0.04, x + 0.18, y + 0.36, z + 0.04, '#c49bff')            # glyph particles

@design("anvil_hat", "Anvil Hat", "cool")
def _(m):
    A, AD, AL = '#4a4a50', '#36363b', '#6a6a72'
    m.box(-2.4, 4.6, -1.8, 2.4, 5.4, 1.8, A)                                             # foot
    m.box(-1.6, 5.4, -1.2, 1.6, 6.0, 1.2, AD)
    m.box(-1.0, 6.0, -0.8, 1.0, 7.0, 0.8, A)                                             # waist
    m.box(-2.8, 7.0, -1.3, 2.8, 8.4, 1.3, A)                                             # face
    m.box(-2.8, 8.3, -1.3, 2.8, 8.45, 1.3, AL)
    m.box(2.8, 7.4, -0.7, 3.8, 8.4, 0.7, A)                                              # horn
    for k in range(5):                                                                  # dizzy stars
        import math
        a = k * 2 * math.pi / 5
        star(m, 3.4 * math.cos(a), 6.4 + 0.4 * (k % 2), 3.4 * math.sin(a), 0.32, '#ffe45c', axis='z')

@design("bell_hat", "Village Bell Hat", "cool")
def _(m):
    W, WD, B, BD = '#7a4e2e', '#4b2d17', '#f2c33a', '#b8861c'
    for sd in (-1, 1):
        m.box(sd * 3.0 - 0.4, 4.6, -0.4, sd * 3.0 + 0.4, 10.4, 0.4, W)                   # posts
    m.box(-3.4, 10.4, -0.5, 3.4, 11.0, 0.5, WD)                                         # beam
    m.box(-0.2, 9.6, -0.2, 0.2, 10.4, 0.2, '#3a3a42')
    for k, w in enumerate((1.2, 1.6, 2.0, 2.4, 2.8)):                                    # bell flaring downward
        y = 9.6 - (k + 1) * 0.7
        m.box(-w / 2, y, -w / 2, w / 2, y + 0.7, w / 2, B)
    m.box(-1.45, 6.1, -1.45, 1.45, 6.4, 1.45, BD)
    m.box(-0.25, 5.4, -0.25, 0.25, 6.1, 0.25, '#5a5a62')                                 # clapper

@design("lantern_hat", "Lantern Hat", "cool")
def _(m):
    I, G = '#3a3a42', '#ffc85a'
    GLOW.update({G})
    m.box(-1.2, 4.6, -1.2, 1.2, 5.0, 1.2, I)
    m.box(-1.0, 5.0, -1.0, 1.0, 7.2, 1.0, G)                                             # glow
    for x in (-1.0, 1.0):
        for z in (-1.0, 1.0):
            m.box(x - 0.15, 5.0, z - 0.15, x + 0.15, 7.2, z + 0.15, I)                     # bars
    m.box(-1.2, 7.2, -1.2, 1.2, 7.6, 1.2, I)
    m.box(-0.6, 7.6, -0.6, 0.6, 7.9, 0.6, I)
    m.box(-0.5, 7.9, -0.1, -0.3, 9.0, 0.1, I); m.box(0.3, 7.9, -0.1, 0.5, 9.0, 0.1, I)   # handle
    m.box(-0.5, 8.8, -0.1, 0.5, 9.0, 0.1, I)

@design("soul_lantern_hat", "Soul Lantern Rod", "cool")
def _(m):
    I, G, W = '#2a3038', '#5fe3f0', '#5a3a20'
    GLOW.update({G})
    m.box(-0.2, 4.6, 2.0, 0.2, 9.4, 2.4, W)                                              # rod up from the back
    m.box(-0.2, 9.0, -3.8, 0.2, 9.4, 2.4, W)                                             # arching forward
    m.box(-0.08, 7.8, -3.68, 0.08, 9.0, -3.52, I)                                        # chain
    m.box(-0.9, 5.6, -4.5, 0.9, 5.9, -2.7, I)
    m.box(-0.75, 5.9, -4.35, 0.75, 7.4, -2.85, G)
    for x in (-0.75, 0.75):
        for z in (-4.35, -2.85):
            m.box(x - 0.12, 5.9, z - 0.12, x + 0.12, 7.4, z + 0.12, I)
    m.box(-0.9, 7.4, -4.5, 0.9, 7.8, -2.7, I)
    for x, y in ((-1.4, 8.0), (1.2, 7.4)):
        m.box(x - 0.15, y, -3.7, x + 0.15, y + 0.3, -3.4, '#a6ffef')

@design("campfire_hat", "Campfire Hat", "cool")
def _(m):
    LG, LGD, F1, F2 = '#6b4326', '#4b2d17', '#ff8a1f', '#ffd23a'
    GLOW.update({F1, F2})
    for (x1, z1, x2, z2) in ((-3.0, -1.6, 3.0, -0.8), (-3.0, 0.8, 3.0, 1.6)):
        m.box(x1, 4.6, z1, x2, 5.4, z2, LG)
    for (x1, z1, x2, z2) in ((-1.6, -3.0, -0.8, 3.0), (0.8, -3.0, 1.6, 3.0)):
        m.box(x1, 5.4, z1, x2, 6.2, z2, LGD)
    for x, z, h in ((-0.6, -0.4, 2.6), (0.5, 0.3, 3.2), (0.0, -0.9, 2.0), (-0.3, 0.8, 2.4)):
        m.box(x - 0.4, 5.4, z - 0.4, x + 0.4, 5.4 + h, z + 0.4, F1)
        m.box(x - 0.2, 5.4, z - 0.45, x + 0.2, 5.4 + h * 0.6, z + 0.45, F2)
    for x, y in ((0.2, 9.6), (-0.6, 10.8), (0.6, 12.0)):
        m.box(x - 0.4, y, -0.4, x + 0.4, y + 0.7, 0.4, '#8a8a92a0')

@design("honey_drip_hat", "Honey Block Hat", "cool")
def _(m):
    H, HL = '#f2a01fc0', '#ffc84a'
    m.box(-2.4, 4.6, -2.4, 2.4, 9.0, 2.4, H)
    m.box(-1.6, 5.4, -1.6, 1.6, 8.2, 1.6, '#e8901a')
    m.box(-4.6, 4.0, -4.6, 4.6, 4.6, 4.6, HL)                                           # honey puddle
    for (x, z, y2) in ((-3.0, -4.65, 1.2), (1.2, -4.65, 2.6), (3.6, -4.65, 0.6), (-1.0, 4.65, 0.4), (2.6, 4.65, 1.8)):
        m.box(x - 0.4, y2, z - 0.05, x + 0.4, 4.6, z + 0.05, HL)
        m.box(x - 0.5, y2 - 0.4, z - 0.08, x + 0.5, y2 + 0.2, z + 0.08, HL)
    for sd in (-1, 1):
        for z, y2 in ((-2.0, 0.8), (2.2, 2.0)):
            m.box(sd * 4.6 - 0.05, y2, z - 0.4, sd * 4.6 + 0.05, 4.6, z + 0.4, HL)

@design("sponge_hat", "Wet Sponge Hat", "cool")
def _(m):
    S, SD, W = '#c8c84a', '#9a9a2a', '#5fb8f0a0'
    m.box(-2.4, 4.6, -2.4, 2.4, 9.0, 2.4, S)
    for ax, pl, out, a1, a2 in (('z', -2.4, -1, -2.4, 2.4), ('x', 2.4, 1, -2.4, 2.4), ('x', -2.4, -1, -2.4, 2.4), ('z', 2.4, 1, -2.4, 2.4)):
        patches(m, ax, pl, out, a1, a2, 4.8, 8.8, 9, [SD, '#7a7a1a'], int(pl * 10) + 21, s=0.5)
    patches(m, 'y', 9.0, 1, -2.2, 2.2, -2.2, 2.2, 6, [SD], 30, s=0.5)
    for x, z, y in ((-3.4, -3.4, 2.0), (3.0, -3.6, 3.0), (0.4, -4.8, 1.0)):
        m.box(x - 0.2, y, z - 0.2, x + 0.2, y + 0.5, z + 0.2, W)                          # drips

@design("note_block_hat", "Note Block Hat", "cool")
def _(m):
    W, WD = '#7a4e2e', '#5a3820'
    m.box(-2.4, 4.6, -2.4, 2.4, 9.0, 2.4, W)
    for z in (-2.4, 2.4):
        patches(m, 'z', z, -1 if z < 0 else 1, -2.4, 2.4, 4.8, 8.8, 6, [WD], 3 + int(z), s=0.6)
    m.box(-1.0, 5.8, -2.48, 1.0, 7.8, -2.4, '#3a2210')
    note_icon(m, -0.2, 6.0, -2.5, '#1d1b22', s=1.2)
    for x, y, c in ((-3.2, 9.4, '#4cc34a'), (2.8, 10.0, '#ff5ce1'), (0.0, 11.0, '#4cc3ff'), (-1.6, 12.0, '#ffe45c')):
        note_icon(m, x, y, -0.6, c)

@design("hopper_hat", "Hopper Funnel Hat", "cool")
def _(m):
    I, ID, IL = '#4a4a50', '#36363b', '#6a6a72'
    m.box(-4.8, 4.0, -4.8, 4.8, 5.6, 4.8, I)                                             # wide rim
    m.box(-4.0, 5.55, -4.0, 4.0, 5.65, 4.0, ID)
    m.box(-2.8, 5.6, -2.8, 2.8, 7.4, 2.8, I)                                             # middle
    m.box(-1.2, 7.4, -1.2, 1.2, 9.0, 1.2, ID)                                            # spout
    m.box(-4.85, 5.2, -4.85, 4.85, 5.6, 4.85, IL)

@design("cauldron_hat", "Bubbling Cauldron", "cool")
def _(m):
    C, CD, P, PL = '#3a3a42', '#26262c', '#a84ae8', '#d8a0ff'
    GLOW.update({P})
    for sd in (-1, 1):
        m.box(sd * 2.0 - 0.5, 4.6, -2.5, sd * 2.0 + 0.5, 5.2, -1.5, CD)
        m.box(sd * 2.0 - 0.5, 4.6, 1.5, sd * 2.0 + 0.5, 5.2, 2.5, CD)
    m.box(-2.8, 5.2, -2.8, 2.8, 8.2, 2.8, C)
    m.box(-2.2, 8.0, -2.2, 2.2, 8.25, 2.2, P)                                            # potion
    for x, z, y in ((-1.0, -0.6, 8.25), (0.8, 0.8, 8.25), (0.2, -1.2, 9.0), (-0.6, 1.0, 9.8)):
        rbox(m, x - 0.35, y, z - 0.35, x + 0.35, y + 0.6, z + 0.35, PL, r=0.15)
    m.box(-2.85, 7.6, -2.85, 2.85, 8.2, 2.85, CD)

@design("brewing_hat", "Brewing Stand Hat", "cool")
def _(m):
    ST, R = '#8a8a8a', '#d8a020'
    m.box(-2.6, 4.6, -2.6, 2.6, 5.0, 2.6, ST)
    m.box(-0.3, 5.0, -0.3, 0.3, 9.4, 0.3, R)                                             # blaze rod
    for k, (x, z, c) in enumerate(((-2.0, -1.2, '#e8343f'), (2.0, -1.2, '#4cc3ff'), (0.0, 2.0, '#7af08a'))):
        m.box(min(0, x), 7.8, min(0, z) - 0.1, max(0, x), 8.0, max(0, z) + 0.1, '#5a5a62')
        rbox(m, x - 0.8, 5.0, z - 0.8, x + 0.8, 6.6, z + 0.8, c + 'd0', r=0.3)             # potion bottles
        m.box(x - 0.35, 6.6, z - 0.35, x + 0.35, 7.4, z + 0.35, '#e6f6ffb0')
        m.box(x - 0.25, 7.4, z - 0.25, x + 0.25, 7.8, z + 0.25, '#a8783a')

@design("portal_halo", "Nether Portal Halo", "cool")
def _(m):
    OB, P = '#1a1028', '#8a2ae0'
    GLOW.update({'#c49bff'})
    for (x1, z1, x2, z2) in ((-3.6, -3.6, 3.6, -2.8), (-3.6, 2.8, 3.6, 3.6), (-3.6, -2.8, -2.8, 2.8), (2.8, -2.8, 3.6, 2.8)):
        m.box(x1, 7.0, z1, x2, 7.8, z2, OB)
    m.box(-2.8, 7.3, -2.8, 2.8, 7.5, 2.8, P + '90')
    for x, z in ((-1.4, -1.0), (0.8, 1.2), (1.6, -1.6)):
        m.box(x - 0.4, 7.5, z - 0.1, x + 0.4, 7.56, z + 0.1, '#c49bff')
    for x, y in ((-3.0, 5.6), (2.8, 6.0), (0.0, 9.0)):
        m.box(x - 0.15, y, -0.15, x + 0.15, y + 0.3, 0.15, '#c49bff')

@design("end_portal_hat", "End Portal Crown", "cool")
def _(m):
    FR, FT, EY = '#d8d4a0', '#3a7a6a', '#2f8a5a'
    for u in range(8):
        import math
        a = u * math.pi / 4; x, z = 4.4 * math.cos(a), 4.4 * math.sin(a)
        m.box(x - 0.9, 3.8, z - 0.9, x + 0.9, 5.4, z + 0.9, FR)                          # frame blocks
        m.box(x - 0.92, 5.0, z - 0.92, x + 0.92, 5.4, z + 0.92, FT)
        if u % 2 == 0 or u == 3:
            rbox(m, x - 0.45, 5.4, z - 0.45, x + 0.45, 5.9, z + 0.45, EY, r=0.15)          # eyes of ender
            m.box(x - 0.15, 5.9, z - 0.15, x + 0.15, 5.95, z + 0.15, '#1a3a2a')
    m.box(-3.4, 4.62, -3.4, 3.4, 4.7, 3.4, '#061418')                                    # starry void
    patches(m, 'y', 4.7, 1, -3.2, 3.2, -3.2, 3.2, 12, ['#5fe3f0', '#c8fbff', '#2a8a7a'], 4, s=0.2)

@design("conduit_hat", "Conduit Hat", "cool")
def _(m):
    PR, PRD, W, EY = '#6ac8b8', '#3e8a7e', '#a87a4a', '#f2c33a'
    GLOW.update({EY})
    y0 = 8.0
    rbox(m, -0.9, y0 - 0.9, -0.9, 0.9, y0 + 0.9, 0.9, W, r=0.2)                          # wooden core
    m.box(-0.5, y0 - 0.3, -0.95, 0.5, y0 + 0.3, -0.9, EY)
    m.box(-0.15, y0 - 0.2, -0.98, 0.15, y0 + 0.2, -0.95, '#1d1b22')
    for (x, y, z) in ((-2.2, y0, 0), (2.2, y0, 0), (0, y0 + 2.2, 0), (0, y0 - 2.2, 0), (0, y0, 2.2), (0, y0, -2.2),
                      (-1.6, y0 + 1.6, -1.6), (1.6, y0 - 1.6, 1.6)):
        m.box(x - 0.45, y - 0.45, z - 0.45, x + 0.45, y + 0.45, z + 0.45, (PR, PRD)[int(x + z) % 2])   # prismarine cage
    for x, y in ((-3.4, 6.4), (3.2, 9.6), (-2.4, 10.4)):
        m.box(x - 0.15, y, -0.15, x + 0.15, y + 0.3, 0.15, '#bfe8ffb0')

@design("spyglass_monocle", "Spyglass", "cool")
def _(m):
    CU, CUD, AM = '#c87a4a', '#9a5a32', '#a87adf'
    m.box(0.9, -1.7, -6.8, 3.1, 0.5, -4.6, CU)                                           # tube at one eye
    m.box(1.1, -1.5, -9.4, 2.9, 0.3, -6.8, CU)
    m.box(1.05, -1.55, -7.2, 2.95, 0.35, -6.8, CUD)
    m.box(1.3, -1.3, -9.5, 2.7, 0.1, -9.4, AM)                                           # amethyst lens
    m.box(1.4, -0.4, -9.55, 1.8, 0.0, -9.5, '#e8d8ff')
    band(m, -0.6, -0.1, '#3a2a20', 4.6)                                                  # strap

@design("golden_apple_hat", "Enchanted Golden Apple", "cool")
def _(m):
    G, GD, LF = '#f2c33a', '#d8a020', '#4cc34a'
    GLOW.update({'#e8a0ff'})
    rbox(m, -2.2, 4.6, -2.2, 2.2, 8.6, 2.2, G, r=0.9)
    m.box(-0.5, 8.3, -0.5, 0.5, 8.6, 0.5, GD)
    m.box(-0.15, 8.6, -0.15, 0.15, 9.6, 0.15, '#6b4326')                                 # stem
    m.box(0.15, 9.0, -0.2, 1.4, 9.3, 0.4, LF)                                            # leaf
    m.box(-1.6, 7.0, -2.26, -0.9, 7.8, -2.2, '#fff4b0')                                  # shine
    for (x, y, z) in ((-2.25, 5.6, -0.6), (2.25, 6.6, 0.8), (-0.8, 5.2, -2.25), (1.2, 7.4, -2.25), (0.4, 8.6, 1.2)):
        x1, x2 = sorted((x, x + (0.05 if x > 0 else -0.05))) if abs(x) > 2 else (x - 0.3, x + 0.3)
        z1, z2 = sorted((z, z + (0.05 if z > 0 else -0.05))) if abs(z) > 2 else (z - 0.3, z + 0.3)
        m.box(x1, y, z1, x2, y + 0.5, z2, '#e8a0ff')                                       # enchant glint

@design("enchanted_book_hat", "Enchanted Book Hat", "cool")
def _(m):
    C, CD, PG = '#6a2a8a', '#4a1a6a', '#f4ecd8'
    GLOW.update({'#e8a0ff'})
    for sd in (-1, 1):                                                                  # book open like a roof
        r = ('z', -45 * sd, (0, 6.6, 0))
        x1, x2 = sorted((0, sd * 3.6))
        m.box(x1, 6.4, -2.4, x2, 6.7, 2.4, C, rot=r)
        m.box(x1, 6.15, -2.2, x2, 6.4, 2.2, PG, rot=r)
        m.box(x1, 6.65, -2.45, x2, 6.75, -2.3, GOLD, rot=r)
    m.box(-0.3, 6.4, -2.45, 0.3, 6.8, 2.45, CD)                                          # spine
    for (x, y) in ((-2.6, 7.6), (2.2, 8.0), (0.0, 8.6), (-1.0, 9.4)):
        m.box(x - 0.15, y, -0.15, x + 0.15, y + 0.3, 0.15, '#e8a0ff')

@design("sword_through_head", "Sword Through Head", "goofy")
def _(m):
    BL, BLD, H, GR = '#4fd8e8', '#2fa8b8', '#4a3a2a', '#2fa8b8'
    m.box(-9.4, 1.2, -0.35, -4.6, 2.2, 0.35, BL)                                         # blade sticking out one side
    m.box(-10.2, 1.45, -0.3, -9.4, 1.95, 0.3, BL)
    m.box(-9.4, 1.6, -0.38, -4.6, 1.8, 0.38, BLD)
    m.box(4.6, 0.6, -1.1, 5.2, 2.8, 1.1, GR)                                             # guard on the other side
    m.box(5.2, 1.3, -0.3, 7.6, 2.1, 0.3, H)                                              # handle
    m.box(7.6, 1.2, -0.4, 8.2, 2.2, 0.4, GR)

@design("trident_crown", "Trident Crown", "cool")
def _(m):
    T, TD, PR = '#5ac8b8', '#3e8a7e', '#f4f2ee'
    band(m, 3.0, 4.4, TD, 4.7)
    band(m, 3.6, 3.9, T, 4.78)
    for u in (-2.8, 0.0, 2.8):
        h = 3.2 if u == 0 else 2.4
        m.box(u - 0.25, 4.4, -4.7, u + 0.25, 4.4 + h, -4.2, T)                            # tines
        m.box(u - 0.55, 4.4 + h - 0.7, -4.7, u + 0.55, 4.4 + h - 0.4, -4.2, T)
        m.box(u - 0.15, 4.4 + h, -4.6, u + 0.15, 4.4 + h + 0.5, -4.3, T)
        rbox(m, u - 0.35, 3.25, -4.95, u + 0.35, 4.05, -4.7, PR, r=0.15)                 # pearls
    for sd in (-1, 1):
        for z in (-1.8, 1.8):
            m.box(sd * 4.7 - 0.25, 4.4, z - 0.25, sd * 4.7 + 0.25, 6.4, z + 0.25, T)

@design("mini_elytra", "Mini Elytra", "cool")
def _(m):
    E, ED, EL = '#8a8ab8', '#5a5a8a', '#b8b8e0'
    for sd in (-1, 1):
        r = ('y', -45 * sd, (sd * 0.3, 0, 4.7))
        x1, x2 = sorted((sd * 0.3, sd * 5.4))
        m.box(x1, -2.0, 4.7, x2, 4.4, 5.2, E, rot=r)                                     # wings flaring out behind the head
        m.box(x1, 3.4, 4.65, x2, 4.4, 5.25, EL, rot=r)
        for k in range(4):
            m.box(x1, -2.0 + k * 1.3, 5.2, x2, -1.8 + k * 1.3, 5.26, ED, rot=r)
        x1, x2 = sorted((sd * 4.4, sd * 5.4))
        m.box(x1, -3.0, 4.7, x2, -2.0, 5.2, E, rot=r)                                    # pointed tips

@design("banner_flag", "Banner Flag Hat", "cool")
def _(m):
    P, C1, C2 = '#7a4e2e', '#2f5fd0', '#f2c33a'
    m.box(-0.2, 4.6, -0.2, 0.2, 12.4, 0.2, P)                                            # pole
    m.box(-0.25, 12.2, -0.25, 0.25, 12.6, 0.25, GOLD)
    m.box(0.2, 7.0, -0.1, 4.0, 12.0, 0.1, C1)                                            # banner
    relief(m, ["...yy...", "..yyyy..", ".yyyyyy.", "..yyyy..", "...yy..."], -0.1, {'y': (C2, 0.05)}, cell=0.4, top=11.0, cx=2.1)
    for k in range(4):
        m.box(0.2 + k * 0.95, 6.4, -0.1, 0.65 + k * 0.95, 7.0, 0.1, C1)                   # notched bottom

# ---------- D: food ----------
@design("sushi_hat", "Sushi Hat", "food")
def _(m):
    RI, SA, SAL, NO = '#f6f4ee', '#f28a5a', '#fcd0b8', '#1f3a2a'
    rbox(m, -1.9, 4.6, -3.0, 1.9, 6.3, 3.0, RI, r=0.6)                                  # rice
    for x, z in ((-1.4, -2.0), (0.8, 0.6), (-0.4, 2.2), (1.3, -1.6)):
        m.box(x - 0.2, 5.4, z - 0.15, x + 0.2, 5.65, z + 0.15, '#e8e4dc')
    rbox(m, -2.1, 6.1, -3.4, 2.1, 6.9, 3.4, SA, r=0.5)                                  # salmon
    for z in (-2.4, -1.0, 0.4, 1.8):
        m.box(-2.12, 6.85, z, 2.12, 6.92, z + 0.35, SAL)
        for sd in (-1, 1):
            m.box(sd * 2.1 - 0.02, 6.3, z, sd * 2.1 + 0.02, 6.85, z + 0.35, SAL)
    m.box(-1.95, 5.2, -0.6, 1.95, 6.95, 0.6, NO)                                          # nori band
    for dx in (-0.3, 0.3):                                                              # chopsticks
        m.box(2.0 + dx, 5.6, -0.1, 2.2 + dx, 10.4, 0.1, '#c9a06a', rot=('z', -22.5, (2.1 + dx, 5.6, 0)))

@design("taco_hat", "Taco Hat", "food")
def _(m):
    SH, SHD, LE, TO, CH, ME = '#f2c86a', '#d8a84a', '#6cbd4b', '#e8343f', '#ffd23a', '#7a3a1a'
    for sd in (-1, 1):
        r = ('z', -22.5 * sd, (0, 4.6, 0))
        x1, x2 = sorted((sd * 0.2, sd * 0.6))
        m.box(x1, 4.6, -3.6, x2, 8.0, 3.6, SH, rot=r)                                    # shell walls
        m.box(x1, 7.6, -3.65, x2, 8.0, 3.65, SHD, rot=r)
    m.box(-0.6, 4.6, -3.6, 0.6, 5.0, 3.6, SH)
    m.box(-1.2, 5.0, -3.4, 1.2, 6.6, 3.4, ME)                                            # fillings
    for z in (-2.8, -1.2, 0.4, 2.0):
        m.box(-1.6, 6.4, z, 1.6, 7.1, z + 0.9, LE)
        m.box(-0.6, 6.9, z + 0.4, 0.2, 7.4, z + 1.0, TO)
    for z in (-3.0, -0.6, 1.4):
        m.box(-0.8, 7.0, z, 0.9, 7.2, z + 0.25, CH)

@design("burger_hat", "Burger Hat", "food")
def _(m):
    BUN, BUND, PAT, CH, LE, TO = '#e8a85a', '#c8803a', '#5a2e1a', '#ffd23a', '#6cbd4b', '#e8343f'
    rbox(m, -3.2, 4.6, -3.2, 3.2, 5.6, 3.2, BUN, r=0.8)                                  # bottom bun
    rbox(m, -3.4, 5.6, -3.4, 3.4, 6.6, 3.4, PAT, r=0.8)                                  # patty
    m.box(-3.6, 6.6, -3.6, 3.6, 6.8, 3.6, CH)                                            # cheese
    for (x, z) in ((-3.6, -3.6), (3.4, 3.4), (-3.6, 3.2)):
        m.box(x, 6.0, z, x + 0.3, 6.6, z + 0.3, CH)
    for k in range(9):
        x = -3.6 + k * 0.9
        m.box(x, 6.75 - 0.15 * (k % 2), -3.7, x + 0.9, 7.1, 3.7, LE)                     # lettuce
    m.box(-2.8, 7.1, -2.8, 2.8, 7.4, 2.8, TO)                                            # tomato
    dome(m, 7.4, [(3.3, 0.8), (2.8, 0.6), (1.9, 0.4)], BUN)                              # top bun
    for (x, y, z) in ((-1.6, 8.75, -1.0), (0.8, 8.75, 1.2), (1.6, 8.15, -2.4), (-2.4, 8.15, 1.8), (0.2, 9.2, -0.2), (-0.6, 8.75, 2.4)):
        m.box(x - 0.18, y, z - 0.1, x + 0.18, y + 0.1, z + 0.1, '#fff4dc')                  # sesame

@design("donut_hat", "Donut Hat", "food")
def _(m):
    D, FR = '#d9a05a', '#f7a8c8'
    ring(m, 4.6, 3.6, D, t=2.4, h=1.6)
    ring(m, 5.0, 3.7, FR, t=2.6, h=1.3)
    for (x1, z1, x2, z2) in ((-3.7, -3.7, 3.7, -2.2), (-3.7, 2.2, 3.7, 3.7), (-3.7, -2.2, -2.2, 2.2), (2.2, -2.2, 3.7, 2.2)):
        for sd in (1,):
            m.box(x1 + 0.6, 6.2, z1 + 0.4, x2 - 0.6, 6.4, z2 - 0.4, FR)
    import random as _r
    rnd = _r.Random(6)
    for _ in range(22):
        x, z = rnd.uniform(-3.2, 3.0), rnd.uniform(-3.2, 3.0)
        if abs(x) < 1.6 and abs(z) < 1.6:
            continue
        m.box(x, 6.4, z, x + rnd.choice((0.5, 0.15)), 6.5, z + 0.15, rnd.choice(('#4cc3ff', '#ffe45c', '#7af08a', '#ffffff', '#ff5c5c')))

@design("cupcake_hat", "Cupcake Hat", "food")
def _(m):
    WR, WRD, FR, FRL = '#f7a8c8', '#e888ae', '#fff4f7', '#ffd8e6'
    for k in range(3):                                                                  # wrapper flaring up
        w = 2.6 + 0.3 * k
        m.box(-w, 4.6 + k * 0.7, -w, w, 5.3 + k * 0.7, w, WR)
        for u in range(-2, 3):
            m.box(u * 1.0 - 0.15, 4.6 + k * 0.7, -w - 0.04, u * 1.0 + 0.15, 5.3 + k * 0.7, -w, WRD)
    for i, (w, h) in enumerate(((3.6, 0.9), (3.0, 0.8), (2.2, 0.8), (1.4, 0.7), (0.6, 0.6))):
        y = 6.7 + sum(hh for _, hh in ((3.6, 0.9), (3.0, 0.8), (2.2, 0.8), (1.4, 0.7))[:i])
        rbox(m, -w, y, -w, w, y + h, w, (FR, FRL)[i % 2], r=min(0.6, w / 2))
    rbox(m, -0.6, 10.2, -0.6, 0.6, 11.2, 0.6, '#d62828', r=0.3)                         # cherry
    m.box(0.0, 11.1, -0.05, 0.1, 11.8, 0.05, '#4a7a2a')
    for x, z, c in ((-2.6, -2.4, '#4cc3ff'), (2.2, -2.8, '#ffe45c'), (-1.0, -3.0, '#7af08a'), (2.8, 1.0, '#ff5c5c')):
        m.box(x - 0.25, 7.5, z - 0.08, x + 0.25, 7.6, z + 0.08, c)

@design("popcorn_bucket", "Popcorn Bucket", "food")
def _(m):
    R, W, PC, PCY = '#d62828', '#f4f2ee', '#fff4d0', '#f2d06a'
    for k in range(2):
        w = 2.2 + 0.3 * k
        m.box(-w, 4.6 + k * 1.2, -w, w, 5.8 + k * 1.2, w, W)
    for u in (-2.0, -0.6, 0.8):
        for sd in (-1, 1):
            m.box(u, 4.6, sd * 2.25 - 0.05, u + 0.7, 5.8, sd * 2.25 + 0.05, R)
            m.box(u - 0.1, 5.8, sd * 2.55 - 0.05, u + 0.7, 7.0, sd * 2.55 + 0.05, R)
    import random as _r
    rnd = _r.Random(8)
    for _ in range(26):                                                                 # popcorn overflowing
        x, z = rnd.uniform(-2.6, 2.0), rnd.uniform(-2.6, 2.0)
        y = 7.0 + rnd.uniform(0, 1.4) - 0.3 * (abs(x) + abs(z)) / 2
        rbox(m, x, y, z, x + 0.7, y + 0.6, z + 0.7, rnd.choice((PC, PC, PCY)), r=0.2)

@design("ramen_bowl", "Ramen Bowl", "food")
def _(m):
    BW, BWD, BR, ND, EG, YO = '#e8343f', '#b8232d', '#d89a4a', '#f2d88a', '#f8f6ee', '#ffa81f'
    rbox(m, -2.4, 4.6, -2.4, 2.4, 5.2, 2.4, BWD, r=0.6)
    rbox(m, -3.4, 5.2, -3.4, 3.4, 7.2, 3.4, BW, r=1.0)                                   # bowl
    m.box(-3.0, 7.0, -3.0, 3.0, 7.1, 3.0, BR)                                            # broth
    for z in (-2.0, -1.0, 0.0, 1.0):
        m.box(-2.6, 7.1, z, 0.4, 7.25, z + 0.35, ND)                                     # noodles
    rbox(m, 0.6, 7.1, -2.4, 2.2, 7.6, -0.8, EG, r=0.3)                                   # soft egg
    rbox(m, 1.0, 7.5, -2.0, 1.8, 7.65, -1.2, YO, r=0.2)
    rbox(m, 0.8, 7.1, 0.4, 2.2, 7.4, 1.8, '#f4f2ee', r=0.5)                              # naruto
    m.box(1.3, 7.4, 0.9, 1.7, 7.45, 1.3, '#f2709a')
    m.box(-2.6, 7.1, 2.0, -0.6, 8.6, 2.2, '#1f3a2a')                                     # nori
    for dx in (-0.25, 0.25):
        m.box(-0.1 + dx, 7.0, -0.1, 0.1 + dx, 11.0, 0.1, '#c9a06a', rot=('x', 22.5, (dx, 7.0, 0)))

@design("fries_hat", "Fries Hat", "food")
def _(m):
    R, RD, F, FD = '#d62828', '#a81a1a', '#ffd23a', '#e8b01f'
    m.box(-2.4, 4.6, -1.6, 2.4, 7.4, 1.6, R)                                             # carton
    m.box(-2.45, 6.8, -1.65, 2.45, 7.0, 1.65, RD)
    for x in (-1.6, -0.4, 0.8):
        m.box(x, 4.6, -1.65, x + 0.6, 6.8, -1.6, '#f4f2ee')                                # stripes
    import random as _r
    rnd = _r.Random(4)
    for i in range(11):
        x = -2.0 + i * 0.4; z = rnd.uniform(-1.2, 0.8)
        h = rnd.uniform(1.6, 3.2)
        m.box(x - 0.2, 6.6, z, x + 0.2, 7.4 + h, z + 0.4, (F, FD)[i % 2],
              rot=None if i % 3 else ('z', (-22.5, 22.5)[i % 2], (x, 7.0, z)))

@design("pineapple_hat", "Pineapple Hat", "food")
def _(m):
    Y, YD, G, GD = '#f2c23a', '#c8901a', '#4cc34a', '#2f8a32'
    rbox(m, -2.2, 4.6, -2.2, 2.2, 8.8, 2.2, Y, r=0.7)
    for y in (5.2, 6.2, 7.2, 8.2):                                                      # diamond scales
        for ax, pl, out in (('z', -2.2, -1), ('z', 2.2, 1), ('x', 2.2, 1), ('x', -2.2, -1)):
            for a in (-1.4, 0.0, 1.4):
                aa = a + (0.7 if int(y) % 2 else 0)
                if abs(aa) < 1.6:
                    p1, p2 = sorted((pl, pl + out * 0.05))
                    if ax == 'z':
                        m.box(aa - 0.35, y - 0.12, p1, aa + 0.35, y + 0.12, p2, YD)
                    else:
                        m.box(p1, y - 0.12, aa - 0.35, p2, y + 0.12, aa + 0.35, YD)
    for k, (ax, a) in enumerate((('x', -22.5), ('x', 22.5), ('z', -22.5), ('z', 22.5), ('x', 0), ('z', 45), ('z', -45))):
        h = 2.6 if a == 0 else 2.0
        rot = None if a == 0 else (ax, a, (0, 8.6, 0))
        m.box(-0.3, 8.6, -0.3, 0.3, 8.6 + h, 0.3, (G, GD)[k % 2], rot=rot)               # leafy crown

@design("avocado_hat", "Avocado Buddy", "food")
def _(m):
    SK, FL, FLL, PT, K = '#2f5a2a', '#c8e07a', '#e8f0a8', '#8a5a2a', '#1a1418'
    y0 = 4.6
    rbox(m, -2.6, y0, -1.0, 2.6, y0 + 5.2, 1.4, SK, r=1.0)                              # skin
    rbox(m, -2.6, y0 + 3.6, -1.0, 2.6, y0 + 5.6, 1.4, SK, r=1.2) if False else None
    rbox(m, -2.2, y0 + 0.4, -1.15, 2.2, y0 + 4.8, -1.0, FLL, r=0.8)                      # flesh
    rbox(m, -1.8, y0 + 0.6, -1.2, 1.8, y0 + 3.8, -1.1, FL, r=0.7)
    rbox(m, -1.2, y0 + 0.9, -1.9, 1.2, y0 + 3.1, -1.1, PT, r=0.5)                        # pit
    eyes(m, 0, y0 + 2.1, -1.9, 0.48, w=0.34, h=0.4)
    cheeks(m, 0, y0 + 1.7, -1.9, 0.82, w=0.28, h=0.2)
    m.box(-0.22, y0 + 1.5, -1.95, 0.22, y0 + 1.62, -1.9, K)
    for sd in (-1, 1):
        m.box(sd * 2.6 - 0.3, y0 + 1.6, -0.3, sd * 2.6 + 0.3, y0 + 2.4, 0.3, FL)          # little arms

@design("egg_yolk_hat", "Eggshell Helmet", "food")
def _(m):
    SH, SHD, YO = '#fbf8ee', '#e8e2d0', '#ffb31f'
    dome(m, 2.0, [(4.9, 2.6), (4.4, 1.2), (3.4, 0.8), (2.0, 0.5)], SH)
    for i in range(10):                                                                 # jagged cracked edge
        u = -4.4 + i * 0.98
        if i % 2:
            for z in (-4.95, 4.95):
                m.box(u - 0.45, 1.4, z - 0.05, u + 0.45, 2.0, z + 0.05, SH)
            for x in (-4.95, 4.95):
                m.box(x - 0.05, 1.4, u - 0.45, x + 0.05, 2.0, u + 0.45, SH)
    m.box(-4.92, 2.4, -4.95, 4.92, 2.5, -4.9, SHD)
    m.box(1.4, 0.2, -5.0, 2.2, 2.0, -4.9, YO)                                            # yolk drip
    m.box(1.2, -0.4, -5.05, 2.4, 0.4, -4.9, YO)

@design("croissant_hat", "Croissant Hat", "food")
def _(m):
    C, CD, CL = '#d9953a', '#a8682a', '#f0c070'
    import math
    for k in range(9):                                                                  # crescent of puffy segments
        a = math.pi * (0.1 + 0.8 * k / 8)
        x, z = 3.2 * math.cos(a), -0.6 + 2.0 * math.sin(a)
        s = 1.0 - abs(k - 4) * 0.17
        rbox(m, x - 0.6, 4.6, z - 0.9 * s - 0.3, x + 0.6, 4.6 + 1.8 * s + 0.2, z + 0.9 * s + 0.3, (C, CL)[k % 2], r=0.3)
        m.box(x - 0.62, 4.6 + 1.2 * s, z - 0.6, x + 0.62, 4.6 + 1.25 * s + 0.1, z + 0.6, CD)

@design("milk_carton_hat", "Milk Carton Hat", "food")
def _(m):
    W, B, BD, K = '#f4f2ee', '#4c8ad8', '#2f6ab8', '#2a2226'
    m.box(-1.8, 4.6, -1.8, 1.8, 8.6, 1.8, W)
    m.box(-1.82, 5.6, -1.82, 1.82, 7.4, 1.82, B)                                         # label band
    for sd in (-1, 1):                                                                  # gabled top
        x1, x2 = sorted((0, sd * 1.8))
        m.box(x1, 8.6, -1.8, x2, 8.9, 1.8, W, rot=('z', -22.5 * sd, (sd * 1.8, 8.6, 0)))
    m.box(-0.15, 8.6, -1.85, 0.15, 9.8, 1.85, W)
    m.box(-0.6, 6.0, -1.88, 0.6, 7.0, -1.82, W)
    m.box(-0.3, 6.2, -1.9, 0.0, 6.5, -1.88, K); m.box(0.1, 6.5, -1.9, 0.4, 6.8, -1.88, K)   # cow spots
    m.box(-1.82, 4.6, -1.82, 1.82, 4.9, 1.82, BD)

@design("sundae_hat", "Sundae Hat", "food")
def _(m):
    GL, V, ST, CO, CR, WF = '#e6f6ffa0', '#fff4dc', '#f7a8c8', '#6b3a22', '#fbfbfb', '#e8b46a'
    m.box(-1.0, 4.6, -1.0, 1.0, 5.0, 1.0, GL)
    m.box(-0.3, 5.0, -0.3, 0.3, 5.8, 0.3, GL)
    m.box(-2.4, 5.8, -2.4, 2.4, 7.4, 2.4, GL)                                            # glass cup
    rbox(m, -2.2, 6.6, -2.2, 0.0, 8.4, 0.0, ST, r=0.5)                                   # scoops
    rbox(m, 0.0, 6.6, -2.2, 2.2, 8.4, 0.0, V, r=0.5)
    rbox(m, -1.1, 6.6, 0.0, 1.1, 8.4, 2.2, CO, r=0.5)
    m.box(-1.6, 8.0, -1.6, 1.6, 8.6, 1.6, CO)                                            # fudge
    for k, w in enumerate((1.6, 1.1, 0.6)):
        rbox(m, -w, 8.4 + k * 0.5, -w, w, 8.9 + k * 0.5, w, CR, r=0.3)                   # whipped cream
    rbox(m, -0.45, 9.9, -0.45, 0.45, 10.8, 0.45, '#d62828', r=0.2)                       # cherry
    m.box(1.2, 8.4, 0.6, 1.6, 10.4, 1.4, WF, rot=('z', -22.5, (1.4, 8.4, 1.0)))           # wafer

@design("cotton_candy_hair", "Cotton Candy Hair", "food")
def _(m):
    P, PL, B, BL = '#f7a8c8', '#ffd0e4', '#a8d8ff', '#d0ecff'
    import random as _r
    rnd = _r.Random(12)
    dome(m, 4.0, [(4.8, 1.2), (4.4, 1.0), (3.6, 1.0), (2.4, 0.8)], P)
    for _ in range(30):                                                                 # puffy clumps
        x, z = rnd.uniform(-4.6, 3.6), rnd.uniform(-4.6, 3.6)
        y = 4.4 + rnd.uniform(0, 3.4) - 0.25 * max(abs(x), abs(z))
        rbox(m, x, y, z, x + 1.4, y + 1.2, z + 1.4, rnd.choice((P, PL, B, BL)), r=0.4)
    m.box(-0.2, 8.4, -0.2, 0.2, 11.2, 0.2, '#f4f2ee')                                    # paper stick poking out

@design("corn_hat", "Corn Cob Hat", "food")
def _(m):
    Y, YD, H, HD = '#ffd23a', '#e8b01f', '#8fd06a', '#5a9a3a'
    m.box(-1.2, 4.6, -1.2, 1.2, 10.0, 1.2, Y)
    for y in [4.9 + k * 0.6 for k in range(9)]:
        m.box(-1.22, y, -1.22, 1.22, y + 0.08, 1.22, YD)                                  # kernel rows
    m.box(-0.8, 10.0, -0.8, 0.8, 10.6, 0.8, Y)
    for sd in (-1, 1):                                                                  # husk leaves peeling
        m.box(min(sd * 1.2, sd * 1.5), 4.6, -1.0, max(sd * 1.2, sd * 1.5), 8.0, 1.0, H, rot=('z', -22.5 * sd, (sd * 1.2, 4.6, 0)))
        m.box(-1.0, 4.6, min(sd * 1.2, sd * 1.5), 1.0, 7.0, max(sd * 1.2, sd * 1.5), HD, rot=('x', 22.5 * sd, (0, 4.6, sd * 1.2)))

@design("broccoli_hair", "Broccoli Hair", "food")
def _(m):
    G, GD, GL = '#3f8f3a', '#2a6a2a', '#6cbd4b'
    import random as _r
    rnd = _r.Random(14)
    dome(m, 4.0, [(4.7, 1.4), (4.0, 1.2), (3.0, 1.0)], GD)
    for _ in range(40):                                                                 # floret bumps
        x, z = rnd.uniform(-5.0, 3.6), rnd.uniform(-5.0, 3.6)
        y = 4.4 + rnd.uniform(0.5, 3.2) - 0.35 * max(abs(x), abs(z))
        s = rnd.uniform(1.3, 2.1)
        rbox(m, x, y, z, x + s, y + s * 0.8, z + s, rnd.choice((G, G, GL, GD)), r=0.35)
    for x in (-3.6, 3.6):
        m.box(x - 0.6, 1.6, -0.6, x + 0.6, 4.6, 0.6, '#9ac86a') if False else None

@design("carrot_hat", "Carrot Hat", "food")
def _(m):
    O, OD, G = '#f2802a', '#c8601a', '#4cc34a'
    for k, w in enumerate((2.0, 1.7, 1.4, 1.1, 0.8, 0.5, 0.3)):
        y = 9.4 - k * 0.9
        m.box(-w / 2, y - 0.9, -w / 2, w / 2, y, w / 2, O, rot=('z', 22.5, (0, 4.6, 0)))
        m.box(-w / 2 - 0.02, y - 0.5, -w / 2 - 0.02, w / 2 + 0.02, y - 0.4, w / 2 + 0.02, OD, rot=('z', 22.5, (0, 4.6, 0)))
    for k, (ax, a) in enumerate((('x', -22.5), ('x', 22.5), ('z', 0))):
        m.box(-0.25, 9.4, -0.25, 0.25, 11.6, 0.25, G, rot=('z', 22.5, (0, 4.6, 0)) if a == 0 else ('x', a, (0, 9.4, 0)))
    m.box(-1.0, 4.6, -1.0, 1.0, 5.0, 1.0, OD) if False else None

@design("baguette_hat", "Baguette Hat", "food")
def _(m):
    B, BD, FL = '#d9953a', '#a8682a', '#f4ecd8'
    r = ('y', 22.5, (0, 0, 0))
    rbox(m, -1.0, 4.6, -6.0, 1.0, 6.4, 6.0, B, r=0.7, rot=r)
    for z in (-4.0, -1.6, 0.8, 3.2):
        m.box(-0.7, 6.35, z, 0.7, 6.45, z + 1.0, FL, rot=r)                              # scoring with flour
        m.box(-0.75, 6.3, z + 1.0, 0.75, 6.42, z + 1.15, BD, rot=r)
    rbox(m, -3.4, 4.0, -3.4, 3.4, 4.8, 3.4, '#22283a', r=1.0)                            # little beret under it
    m.box(-0.2, 4.6, -0.2, 0.2, 5.2, 0.2, '#22283a')

@design("pretzel_hat", "Pretzel Hat", "food")
def _(m):
    P, PD, S = '#a8682a', '#7a4a1a', '#ffffff'
    y0 = 4.6
    pts = [(-2.2, 0.0), (-2.6, 1.0), (-2.4, 2.0), (-1.8, 2.8), (-0.8, 3.0), (0.0, 2.2), (0.8, 3.0), (1.8, 2.8),
           (2.4, 2.0), (2.6, 1.0), (2.2, 0.0), (1.2, 0.6), (0.0, 1.4), (-1.2, 0.6)]
    pts = pts + pts[:1]
    for i in range(len(pts) - 1):                                                       # knot loop, filled in between points
        (xa, ya), (xb, yb) = pts[i], pts[i + 1]
        for k in range(3):
            t = k / 3; x, y = xa + (xb - xa) * t, ya + (yb - ya) * t
            m.box(x - 0.5, y0 + y, -0.5, x + 0.5, y0 + y + 1.0, 0.5, P)
    for x, y in ((-2.0, 2.4), (2.0, 2.4), (0.0, 1.5)):
        m.box(x - 0.52, y0 + y, -0.52, x + 0.52, y0 + y + 0.25, 0.52, PD)
    for x, y in ((-2.4, 1.8), (-0.8, 3.6), (1.2, 3.6), (2.6, 1.2), (0.0, 2.0)):
        m.box(x - 0.12, y0 + y, -0.5, x + 0.12, y0 + y + 0.12, -0.45, S)                   # salt

@design("lemon_hat", "Lemon Buddy", "food")
def _(m):
    Y, YD, G = '#fbe23a', '#e8c81f', '#4cc34a'
    y0 = 4.6
    rbox(m, -2.0, y0, -1.6, 2.0, y0 + 3.0, 1.6, Y, r=0.9)
    m.box(-2.6, y0 + 1.2, -0.5, -2.0, y0 + 1.8, 0.5, YD); m.box(2.0, y0 + 1.2, -0.5, 2.6, y0 + 1.8, 0.5, YD)   # pointy ends
    m.box(-0.1, y0 + 3.0, -0.1, 0.1, y0 + 3.5, 0.1, '#6b4326')
    m.box(0.1, y0 + 3.2, -0.25, 1.4, y0 + 3.5, 0.45, G)
    eyes(m, 0, y0 + 1.5, -1.6, 0.6, w=0.36, h=0.42)
    cheeks(m, 0, y0 + 1.15, -1.6, 1.0, w=0.32)
    m.box(-0.25, y0 + 1.05, -1.65, 0.25, y0 + 1.17, -1.6, '#1a1418')

@design("cherry_clips", "Cherry Hair Clips", "food")
def _(m):
    R, RL, ST, LF = '#d62828', '#ff6a6a', '#4a7a2a', '#4cc34a'
    for sd in (-1, 1):
        x = sd * 4.7
        x1, x2 = sorted((x, x + sd * 0.15))
        m.box(x1, 2.0, -2.6, x2, 2.4, -0.6, '#f7a8c8')                                    # clip
        for dz, h in ((-2.2, 0.0), (-1.0, 0.6)):
            rbox(m, min(x, x + sd * 1.2), 0.4 + h, -2.6 + dz * 0.2 - 0.6, max(x, x + sd * 1.2), 1.6 + h, -2.6 + dz * 0.2 + 0.6, R, r=0.35)
            m.box(min(x, x + sd * 0.4), 1.3 + h, -2.6 + dz * 0.2 - 0.4, max(x, x + sd * 0.4) if sd > 0 else max(x, x + sd * 0.4), 1.5 + h, -2.6 + dz * 0.2 - 0.2, RL)
        m.box(min(x, x + sd * 0.3), 1.6, -2.4, max(x, x + sd * 0.3), 3.0, -2.2, ST)
        m.box(min(x, x + sd * 0.2), 2.8, -2.4, max(x, x + sd * 0.2), 3.2, -1.2, LF)

@design("dumpling_hat", "Dumpling Steamer", "food")
def _(m):
    BB, BBD, DU, DUD = '#d8b070', '#a8803a', '#f6f2e6', '#e2dccc'
    m.box(-3.0, 4.6, -3.0, 3.0, 6.0, 3.0, BB)                                            # bamboo basket
    for y in (4.9, 5.5):
        m.box(-3.05, y, -3.05, 3.05, y + 0.15, 3.05, BBD)
    for (x, z) in ((-1.4, -1.4), (1.4, -1.4), (-1.4, 1.4), (1.4, 1.4)):
        rbox(m, x - 1.1, 5.9, z - 1.1, x + 1.1, 7.2, z + 1.1, DU, r=0.45)                 # dumplings
        for k in range(3):
            m.box(x - 0.6 + k * 0.5, 7.0, z - 0.1, x - 0.45 + k * 0.5, 7.5, z + 0.1, DUD)   # pleats
    r = ('x', 22.5, (0, 6.0, 3.0))
    m.box(-3.0, 7.4, -3.0, 3.0, 8.2, 3.0, BB, rot=r)                                     # lid tipped open
    m.box(-3.05, 7.6, -3.05, 3.05, 7.75, 3.05, BBD, rot=r)
    for x, y in ((-1.2, 9.0), (0.6, 9.8), (1.6, 8.8)):
        m.box(x - 0.35, y, -1.4, x + 0.35, y + 0.6, -0.8, '#f4f4f8a0')                    # steam

@design("onigiri_hat", "Onigiri Buddy", "food")
def _(m):
    RI, NO, K = '#f8f6ee', '#1f3a2a', '#1a1418'
    y0 = 4.6
    for k in range(8):                                                                  # rounded triangle
        w = 4.4 - k * 0.48
        rbox(m, -w / 2, y0 + k * 0.5, -1.0, w / 2, y0 + (k + 1) * 0.5, 1.0, RI, r=0.25)
    m.box(-1.4, y0, -1.05, 1.4, y0 + 1.6, 1.05, NO)                                       # nori
    eyes(m, 0, y0 + 2.1, -1.0, 0.55, w=0.32, h=0.38)
    cheeks(m, 0, y0 + 1.75, -1.0, 0.95, w=0.3)
    m.box(-0.2, y0 + 1.75, -1.05, 0.2, y0 + 1.85, -1.0, K)
    for x, y in ((-0.8, y0 + 3.0), (0.9, y0 + 2.6), (0.2, y0 + 3.4)):
        m.box(x - 0.1, y, -1.04, x + 0.1, y + 0.18, -1.0, '#e8e4dc')

@design("coffee_cup_hat", "Coffee To Go", "food")
def _(m):
    CUP, SL, LID, K = '#f4f2ee', '#a8783a', '#3a3540', '#1a1418'
    for k in range(4):
        w = 1.6 + 0.15 * k
        m.box(-w, 4.6 + k * 1.0, -w, w, 5.6 + k * 1.0, w, CUP)
    m.box(-1.95, 6.0, -1.95, 1.95, 7.6, 1.95, SL)                                         # sleeve
    m.box(-0.6, 6.4, -1.98, 0.6, 7.2, -1.95, '#5a3a20')
    m.box(-2.2, 8.6, -2.2, 2.2, 9.1, 2.2, LID)
    m.box(-1.7, 9.1, -1.7, 1.7, 9.5, 1.7, LID)
    m.box(-0.5, 9.5, -1.6, 0.5, 9.6, -1.0, K)
    for x, y in ((-0.4, 10.0), (0.4, 10.8), (-0.2, 11.6)):
        m.box(x - 0.3, y, -1.4, x + 0.3, y + 0.6, -0.8, '#f4f4f8a0')
