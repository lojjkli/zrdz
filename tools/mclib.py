"""Tiny Minecraft model toolkit: build cuboid models in 'head pixel' space,
write Java resource-pack JSON + 16x16 textures, and render previews."""
import json, math, os, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HAT_CLEAR = 4.6
S = 1.6  # 1 player-head pixel = 1.6 model units when worn (head = 1.6..14.4)

def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + ((int(h[6:8], 16),) if len(h) == 8 else (255,))

class Tex:
    """Box faces copied 1:1 from a Java entity texture: cube at texOffs(u, v) with size (w, h, d),
    using the standard box UV layout. Faces in `skip` (or with zero area) are left transparent."""
    def __init__(self, img, u, v, w, h, d, skip=(), name=""):
        self.a = img if isinstance(img, np.ndarray) else np.array(Image.open(img).convert('RGBA'))
        self.u, self.v, self.w, self.h, self.d, self.skip = u, v, w, h, d, set(skip)
        self.key = (name, u, v, w, h, d, tuple(sorted(skip)))

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, o):
        return isinstance(o, Tex) and o.key == self.key

    def patch(self, face, pw, ph):
        u, v, w, h, d = self.u, self.v, self.w, self.h, self.d
        x, y, rw, rh = {"north": (u + d, v + d, w, h), "east": (u, v + d, d, h), "west": (u + d + w, v + d, d, h),
                        "south": (u + 2 * d + w, v + d, w, h), "up": (u + d, v, w, d), "down": (u + d + w, v, w, d)}[face]
        if face in self.skip or rw <= 0 or rh <= 0:
            return np.zeros((ph, pw, 4), np.uint8)
        p = self.a[int(y):int(y + rh), int(x):int(x + rw)]
        if face in ("up", "down"):
            p = p[::-1, ::-1]
        return np.array(Image.fromarray(np.ascontiguousarray(p)).resize((pw, ph), Image.NEAREST))


class Model:
    def __init__(self, name, title, tier="basic"):
        self.name, self.title, self.tier = name, title, tier
        self.boxes = []
        self.colors = []
        self.anim = None

    def animate(self, *fx, frames=16, frametime=2, interpolate=True):
        """Animated texture: fx are (kind, colours, ...) tuples applied per frame - see frame_tint()."""
        self.anim = dict(fx=fx, frames=frames, frametime=frametime, interpolate=interpolate)
        return self

    def frame_tint(self, c, f):
        """RGBA a colour should be painted with on frame f, or None to keep it."""
        import colorsys
        if not self.anim or not isinstance(c, str):
            return None
        N = self.anim['frames']
        rgba = list(hex2rgb(c)); out = None
        for fx in self.anim['fx']:
            kind, cols = fx[0], fx[1]
            if c not in cols:
                continue
            i = list(cols).index(c)
            if kind == 'seq':                         # explicit colour per frame: {colour: [c0, c1, ...]}
                seq = cols[c]
                rgba = list(hex2rgb(seq[f % len(seq)]))[:3] + [rgba[3]]
            elif kind == 'cycle':                       # each colour steps to the next one in the list
                step = fx[2] if len(fx) > 2 else 1
                rgba = list(hex2rgb(cols[(i + f // step) % len(cols)]))[:3] + [rgba[3]]
            elif kind == 'blink':                     # swap to another colour on the listed frames
                if f in fx[3]:
                    rgba = list(hex2rgb(fx[2]))[:3] + [rgba[3]]
            elif kind == 'hue':                       # rotate the hue a full turn over the loop
                h, l, sat = colorsys.rgb_to_hls(*(v / 255 for v in rgba[:3]))
                r, g, b = colorsys.hls_to_rgb((h + f / N) % 1, l, sat)
                rgba[:3] = [int(v * 255) for v in (r, g, b)]
            else:                                     # pulse / twinkle / flicker: brightness changes
                amp = fx[2] if len(fx) > 2 else 0.35
                if kind == 'pulse':
                    k = math.sin(2 * math.pi * f / N)
                elif kind == 'twinkle':
                    k = math.sin(2 * math.pi * (f / N + i / max(1, len(cols))))
                else:
                    k = (int(hashlib.md5(f'{c}{f}'.encode()).hexdigest()[:6], 16) % 1000) / 500.0 - 1
                if k >= 0:
                    rgba[:3] = [v + (255 - v) * amp * k for v in rgba[:3]]
                else:
                    rgba[:3] = [v * (1 + amp * k) for v in rgba[:3]]
            out = tuple(int(max(0, min(255, v))) for v in rgba)
        return out

    def box(self, x1, y1, z1, x2, y2, z2, c, rot=None, flat=False):
        """Box in head-pixel coords (head = -4..4 on every axis, front = north/-z).
        rot = (axis, angle, (ox, oy, oz))"""
        if c not in self.colors:
            self.colors.append(c)
        a, b = sorted((x1, x2)), (sorted((y1, y2)), sorted((z1, z2)))
        # fit: the skin's hat layer sits 0.5px outside the head (+-4.5). Any outer surface that would land
        # inside that shell is pushed to +-4.6 so hair/hat pixels never poke through the cosmetic.
        def clear(lo, hi):
            if 4 < hi < HAT_CLEAR:
                hi = HAT_CLEAR
            if -HAT_CLEAR < lo < -4:
                lo = -HAT_CLEAR
            return [lo, hi]
        if b[0][0] < 4.5:   # pieces sitting fully above the hat layer can't clip it, so they keep their exact size
            a, b = clear(*a), (clear(*b[0]), clear(*b[1]))
        self.boxes.append(dict(f=(a[0], b[0][0], b[1][0]), t=(a[1], b[0][1], b[1][1]), c=c, rot=rot))
        return self

    # ---- export -------------------------------------------------------
    DENS = 2  # texels per head pixel (2x the player-skin resolution)

    def _face_size(self, bx, d):
        if isinstance(bx['c'], Tex):   # textured faces keep their native pixels (crisp, 1:1 with the entity texture)
            t = bx['c']; w, h, dd = t.w, t.h, t.d
            fw, fh = {"north": (w, h), "south": (w, h), "east": (dd, h), "west": (dd, h), "up": (w, dd), "down": (w, dd)}[d]
            return max(1, int(round(fw))), max(1, int(round(fh)))
        dx, dy, dz = (bx['t'][i] - bx['f'][i] for i in range(3))
        w, h = {"north": (dx, dy), "south": (dx, dy), "east": (dz, dy), "west": (dz, dy),
                "up": (dx, dz), "down": (dx, dz)}[d]
        return max(1, round(w * self.DENS)), max(1, round(h * self.DENS))

    def bake(self):
        """Paint every face its own shaded patch and shelf-pack them into one atlas."""
        if hasattr(self, '_atlas'):
            return self._atlas
        rng = np.random.default_rng(int(hashlib.md5(self.name.encode()).hexdigest()[:8], 16))
        cache, patches = {}, []
        self.face_uv = []
        for bx in self.boxes:
            fu = {}
            for d in DIRS:
                w, h = self._face_size(bx, d)
                key = (w, h, bx['c'], d)
                if key not in cache:
                    cache[key] = len(patches)
                    c = bx['c']
                    patches.append((key, c.patch(d, w, h) if isinstance(c, Tex) else paint(w, h, c, d, rng)))
                    self._paint_order = getattr(self, '_paint_order', []) + [key]
                fu[d] = cache[key]
            self.face_uv.append(fu)
        order = sorted(range(len(patches)), key=lambda i: -patches[i][1].shape[0])
        total = sum(p.shape[0] * p.shape[1] for _, p in patches)
        W = 16
        while W * W < total * 1.3 or W < max(p.shape[1] for _, p in patches):
            W *= 2
        while True:
            pos, x, y, rowh, ok = {}, 0, 0, 0, True
            for i in order:
                ph, pw = patches[i][1].shape[:2]
                if x + pw > W:
                    x, y, rowh = 0, y + rowh, 0
                pos[i] = (x, y); x += pw; rowh = max(rowh, ph)
            H = y + rowh
            if H <= W:
                break
            W *= 2
        H = W
        atlas = np.zeros((H, W, 4), np.uint8)
        for i, (x, y) in pos.items():
            p = patches[i][1]; atlas[y:y + p.shape[0], x:x + p.shape[1]] = p
        self.rects = {i: (x, y, x + patches[i][1].shape[1], y + patches[i][1].shape[0]) for i, (x, y) in pos.items()}
        self._atlas = Image.fromarray(atlas, 'RGBA')
        self._pos = pos
        return self._atlas

    def frame_atlas(self, f):
        """The atlas repainted for animation frame f (same layout and noise, tinted colours)."""
        base = np.array(self.bake())
        rng = np.random.default_rng(int(hashlib.md5(self.name.encode()).hexdigest()[:8], 16))
        out = base.copy()
        for i, (w, h, c, d) in enumerate(self._paint_order):
            if isinstance(c, Tex):
                continue
            t = self.frame_tint(c, f)
            p = paint(w, h, c, d, rng, tint=t)
            if t is not None:
                x, y = self._pos[i]
                out[y:y + h, x:x + w] = p
        return out

    def anim_strip(self):
        """Vertical strip of all frames, for an animated .png + .mcmeta."""
        return Image.fromarray(np.concatenate([self.frame_atlas(f) for f in range(self.anim['frames'])], 0), 'RGBA')

    def texture(self):
        return self.bake()

    def to_json(self, texref):
        W, H = self.bake().size
        els = []
        for bx, fu in zip(self.boxes, self.face_uv):
            f = [round(8 + S * v, 3) for v in bx['f']]
            t = [round(8 + S * v, 3) for v in bx['t']]
            faces = {}
            for d in DIRS:
                x0, y0, x1, y1 = self.rects[fu[d]]
                faces[d] = {"uv": [round(x0 * 16 / W, 4), round(y0 * 16 / H, 4), round(x1 * 16 / W, 4), round(y1 * 16 / H, 4)],
                            "texture": "#0"}
            e = {"from": f, "to": t, "faces": faces}
            if bx['rot']:
                ax, ang, o = bx['rot']
                e["rotation"] = {"angle": ang, "axis": ax, "origin": [round(8 + S * v, 3) for v in o]}
            els.append(e)
        return {"credit": "ACONITE cosmetics", "texture_size": [W, H],
                "textures": {"0": texref, "particle": texref},
                "elements": els,
                "display": {"head": {"rotation": [0, 0, 0], "translation": [0, 0, 0], "scale": [1, 1, 1]},
                            "gui": {"rotation": [30, 45, 0], "translation": [0, -1, 0], "scale": [0.5, 0.5, 0.5]},
                            "thirdperson_righthand": {"rotation": [75, 45, 0], "translation": [0, 2.5, 0], "scale": [0.375] * 3},
                            "firstperson_righthand": {"rotation": [0, 45, 0], "scale": [0.4] * 3},
                            "ground": {"translation": [0, 3, 0], "scale": [0.25] * 3},
                            "fixed": {"scale": [0.5] * 3}}}

    def render_elements(self, tex=None):
        arr = np.array(self.bake()) if tex is None else tex
        out = []
        for bx, fu in zip(self.boxes, self.face_uv):
            f = [8 + S * v for v in bx['f']]
            t = [8 + S * v for v in bx['t']]
            out.append(dict(f=f, t=t, rot=bx['rot'] and (bx['rot'][0], bx['rot'][1], [8 + S * v for v in bx['rot'][2]]),
                            faces={d: (arr, list(self.rects[fu[d]])) for d in DIRS}, glow=bx['c'] in GLOW))
        return out

DIRS = ("north", "east", "south", "west", "up", "down")
SPECKLE = {'#3a2d78', '#2e2366', '#4b3a8f'}  # amethyst-like speckled surfaces
FLAT = {'#a172d0'}  # flat-shaded materials copied 1:1 from the animation (Taggy)
GLOW = {'#c49bff', '#38f6ff', '#5fe3f0', '#ff4a2a', '#fff6b0', '#ffd34a', '#c45cff', '#38d6b8', '#7cfba5',
        '#b6ffd0', '#b6ff6b', '#fff4b0', '#ff7ad1', '#8affc8', '#d4ffff', '#fff1a0', '#9be7ff'}
METAL = {'#f2c33a', '#b8861c', '#c9ced8', '#a9adb8', '#9ea2ad', '#8c8f99', '#7c808b', '#9aa1ad', '#6f7682',
         '#bfeff2', '#4ee6e6', '#e0a833', '#fff1a0'}

def _adj(c, k):
    return np.clip(np.array(c[:3], float) * k, 0, 255)

def paint(w, h, color, d, rng, tint=None):
    """Hand-painted look: noise, light-from-top gradient, darker rim, top-left highlight,
    metal sheen and soft glow cores."""
    base = tint or hex2rgb(color)
    img = np.zeros((h, w, 4), np.uint8)
    metal, glow = color in METAL, color in GLOW
    if color in FLAT:
        img[:, :, :3] = base[:3]; img[:, :, 3] = base[3]
        return img
    for y in range(h):
        for x in range(w):
            k = 1 + rng.choice([-0.06, -0.03, 0, 0, 0.03, 0.05])
            if d not in ("up", "down") and h > 2:
                k *= 1.08 - 0.2 * (y / (h - 1))          # top lit, bottom shaded
            if metal and ((x + y) % 7 in (0, 1)):
                k *= 1.22                                   # diagonal sheen
            if glow:
                cx, cy = (w - 1) / 2, (h - 1) / 2
                k *= 1.12 - 0.25 * (abs(x - cx) / max(cx, 1) + abs(y - cy) / max(cy, 1)) / 2
            if color in SPECKLE:
                k *= rng.choice([1, 1, 1, 1, 1, 1.22, 0.84, 1.1])
            if w > 2 and h > 2:
                if x == 0 or y == 0:
                    k *= 1.14                               # bevel highlight
                elif x == w - 1 or y == h - 1:
                    k *= 0.78                               # rim shade
            img[y, x, :3] = _adj(base, k)
            img[y, x, 3] = base[3]
    return img

# ---- player head for previews (16px per face) ------------------------
def player_head():
    rng = np.random.default_rng(3)
    def base(c):
        a = np.zeros((16, 16, 4), np.uint8)
        for y in range(16):
            for x in range(16):
                k = 1 + rng.choice([-0.05, 0, 0, 0.04])
                a[y, x] = [min(255, int(v * k)) for v in c] + [255]
        return a
    SK, HR, HRD = (214, 166, 128), (74, 48, 34), (52, 33, 24, 255)
    face = base(SK)
    face[0:4] = base(HR)[0:4]; face[4, :] = base(HRD[:3])[4]; face[4:6, 0:2] = HRD; face[4:6, 14:16] = HRD
    face[5, 6:10] = (196, 150, 114, 255)
    for ex in (3, 10):
        face[8:10, ex:ex + 3] = (250, 250, 250, 255)
        face[8:10, ex + (1 if ex == 3 else 0):ex + (3 if ex == 3 else 2)] = (60, 70, 160, 255)
        face[8, ex + (2 if ex == 3 else 0)] = (110, 125, 220, 255)
        face[7, ex:ex + 3] = HRD
    face[10:12, 7:9] = (190, 140, 104, 255)
    face[12, 5:11] = (150, 84, 70, 255); face[13, 6:10] = (196, 120, 106, 255)
    face[11, 3:5] = face[11, 11:13] = (226, 150, 130, 255)
    side = base(SK); side[0:6] = base(HR)[0:6]; side[6, 0:10] = HRD
    side[9:11, 6:8] = (190, 140, 104, 255)
    back = base(HR); back[13:16] = base(SK)[13:16]
    top = base(HR); bot = base((190, 146, 110))
    full = [0, 0, 16, 16]
    return dict(f=[1.6] * 3, t=[14.4] * 3, rot=None,
                faces={"north": (face, full), "south": (back, full), "east": (side, full),
                       "west": (side[:, ::-1], full), "up": (top, full), "down": (bot, full)})

def skin_head(path):
    """Real Minecraft head (base + hat layer) from a standard 64x64 skin."""
    a = np.array(Image.open(path).convert('RGBA'))
    def faces(ox):
        g = lambda x, y: a[y:y + 8, ox + x:ox + x + 8]
        full = [0, 0, 8, 8]
        return {"north": (g(8, 8), full), "east": (g(0, 8), full), "west": (g(16, 8), full),
                "south": (g(24, 8), full), "up": (g(8, 0)[::-1, ::-1].copy(), full), "down": (g(16, 0)[::-1, ::-1].copy(), full)}
    base = faces(0)
    for k, (arr, uv) in base.items():   # head base is opaque in-game
        arr = arr.copy(); arr[..., 3] = 255; base[k] = (arr, uv)
    return [dict(f=[1.6] * 3, t=[14.4] * 3, rot=None, faces=base),
            dict(f=[0.8] * 3, t=[15.2] * 3, rot=None, faces=faces(32))]

# ---- renderer (orthographic z-buffer) ---------------------------------
FACES = {
    "north": ((0, 0, -1), lambda a, b: ((b[0], b[1], a[2]), (-(b[0]-a[0]), 0, 0), (0, -(b[1]-a[1]), 0))),
    "south": ((0, 0, 1),  lambda a, b: ((a[0], b[1], b[2]), (b[0]-a[0], 0, 0), (0, -(b[1]-a[1]), 0))),
    "east":  ((1, 0, 0),  lambda a, b: ((b[0], b[1], b[2]), (0, 0, -(b[2]-a[2])), (0, -(b[1]-a[1]), 0))),
    "west":  ((-1, 0, 0), lambda a, b: ((a[0], b[1], a[2]), (0, 0, b[2]-a[2]), (0, -(b[1]-a[1]), 0))),
    "up":    ((0, 1, 0),  lambda a, b: ((a[0], b[1], a[2]), (b[0]-a[0], 0, 0), (0, 0, b[2]-a[2]))),
    "down":  ((0, -1, 0), lambda a, b: ((a[0], a[1], b[2]), (b[0]-a[0], 0, 0), (0, 0, -(b[2]-a[2])))),
}

def rotmat(axis, ang):
    r = math.radians(ang); c, s = math.cos(r), math.sin(r)
    return {"x": np.array([[1, 0, 0], [0, c, -s], [0, s, c]]),
            "y": np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]]),
            "z": np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])}[axis]

_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def render(elements, size=512, yaw=-32, pitch=24, bg=((126, 100, 170), (48, 30, 80)), label=None, ss=3, plain=False):
    ya, pa = math.radians(yaw), math.radians(pitch)
    cam = np.array([math.sin(ya) * math.cos(pa), math.sin(pa), -math.cos(ya) * math.cos(pa)])
    fwd = -cam
    right = np.cross(fwd, [0, 1, 0]); right /= np.linalg.norm(right)   # +x on the left when facing the front, as in-game
    up = np.array([0, 1, 0]) - fwd * fwd[1]; up /= np.linalg.norm(up)
    L = np.array([-0.35, 0.85, -0.55]); L /= np.linalg.norm(L)
    faces = []
    for el in elements:
        a, b = el['f'], el['t']
        R, O = (rotmat(el['rot'][0], el['rot'][1]), np.array(el['rot'][2], float)) if el['rot'] else (np.eye(3), np.zeros(3))
        flat = any(b[i] - a[i] < 1e-6 for i in range(3))
        for d, (n, geo) in FACES.items():
            if d not in el['faces']:
                continue
            nw = R @ np.array(n, float)
            if not flat and nw @ cam <= 1e-6:
                continue
            o, du, dv = (np.array(v, float) for v in geo(a, b))
            o = R @ (o - O) + O; du = R @ du; dv = R @ dv
            if nw @ cam < 0:
                nw = -nw
            sh = 1.0 if el.get('glow') else 0.55 + 0.5 * max(0, nw @ L) + 0.08 * nw[1]
            faces.append((o, du, dv, el['faces'][d], min(1.25, sh)))
    pts = np.array([[p @ right, p @ up] for o, du, dv, *_ in faces for p in (o, o + du, o + dv, o + du + dv)])
    mn, mx = pts.min(0), pts.max(0)
    W = size * ss
    sc = W * (0.74 if label else 0.8) / max(mx - mn)
    ctr = (mn + mx) / 2
    yoff = -0.05 * W if label else 0
    to2 = lambda p: np.array([(p @ right - ctr[0]) * sc + W / 2, -(p @ up - ctr[1]) * sc + W / 2 + yoff])
    col = np.zeros((W, W, 3), np.float32); zb = np.full((W, W), np.inf, np.float32)
    def raster(o, du, dv, arr, uv):
        P0, PU, PV = to2(o), to2(o + du) - to2(o), to2(o + dv) - to2(o)
        M = np.array([[PU[0], PV[0]], [PU[1], PV[1]]])
        if abs(np.linalg.det(M)) < 1e-6:
            return None
        Mi = np.linalg.inv(M)
        corners = np.array([P0, P0 + PU, P0 + PV, P0 + PU + PV])
        x0, y0 = np.floor(corners.min(0)).astype(int); x1, y1 = np.ceil(corners.max(0)).astype(int)
        x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, W), min(y1, W)
        if x0 >= x1 or y0 >= y1:
            return None
        X, Y = np.meshgrid(np.arange(x0, x1) + 0.5, np.arange(y0, y1) + 0.5)
        dx, dy = X - P0[0], Y - P0[1]
        s_ = Mi[0, 0] * dx + Mi[0, 1] * dy; t_ = Mi[1, 0] * dx + Mi[1, 1] * dy
        m = (s_ >= 0) & (s_ < 1) & (t_ >= 0) & (t_ < 1)
        if not m.any():
            return None
        u0, v0, u1, v1 = uv
        tx = np.clip((u0 + s_ * (u1 - u0)).astype(int), 0, arr.shape[1] - 1)
        ty = np.clip((v0 + t_ * (v1 - v0)).astype(int), 0, arr.shape[0] - 1)
        z = o @ fwd + s_ * (du @ fwd) + t_ * (dv @ fwd)
        return x0, y0, x1, y1, m, arr[ty, tx], z

    glass = []
    for o, du, dv, (arr, uv), sh in faces:
        r = raster(o, du, dv, arr, uv)
        if r is None:
            continue
        x0, y0, x1, y1, m, px, z = r
        a = px[..., 3]
        if ((a > 20) & (a < 250) & m).any():
            glass.append((float(np.mean(z[m])), r, sh))
        m = m & (a >= 250)
        sub = zb[y0:y1, x0:x1]
        m &= z < sub - 1e-4
        sub[m] = z[m]
        col[y0:y1, x0:x1][m] = px[..., :3][m] * sh + max(0.0, sh - 0.5) * 34  # lift so black skins still read in 3D
    mask = np.isfinite(zb)
    # silhouette + crease outline from depth jumps
    zf = np.where(mask, zb, 1e9)
    edge = np.zeros_like(mask)
    for sy, sx in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        nz = np.roll(np.roll(zf, sy, 0), sx, 1)
        edge |= mask & (nz - zf > 0.8)
    col[edge] *= 0.35
    # background + soft contact shadow
    t = np.linspace(0, 1, W)[:, None, None]
    bgimg = np.array(bg[0], np.float32) * (1 - t) + np.array(bg[1], np.float32) * t
    bgimg = np.broadcast_to(bgimg, (W, W, 3)).copy()
    if plain:
        bgimg[:] = 255
    ys, xs = np.nonzero(mask)
    if len(ys) and not plain:
        cy, cx = ys.max() + W * 0.01, (xs.min() + xs.max()) / 2
        rx, ry = (xs.max() - xs.min()) * 0.55, W * 0.035
        Y, X = np.mgrid[0:W, 0:W]
        dd = ((X - cx) / rx) ** 2 + ((Y - cy) / ry) ** 2
        bgimg *= (1 - 0.55 * np.clip(1 - dd, 0, 1))[..., None]
        # faint rim glow behind the model
        glow = np.zeros((W, W), np.float32); glow[mask] = 1
        g = Image.fromarray((glow * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(W * 0.03))
        bgimg += (np.array(g, np.float32) / 255)[..., None] * np.array([70, 40, 110], np.float32) * 0.6
    out = np.where(mask[..., None], col, bgimg)
    # see-through pixels (glass): blended back to front over whatever is behind them
    for _, (x0, y0, x1, y1, m, px, z), sh in sorted(glass, key=lambda g: -g[0]):
        a = px[..., 3].astype(np.float32) / 255
        m = m & (a > 0.08) & (a < 0.98) & (z < zb[y0:y1, x0:x1] - 1e-4)
        tile = out[y0:y1, x0:x1]
        tint = px[..., :3].astype(np.float32) * min(1.2, sh + 0.15)
        tile[m] = tile[m] * (1 - a[m, None]) + tint[m] * a[m, None]
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).resize((size, size), Image.LANCZOS)
    if label:
        d = ImageDraw.Draw(img)
        font = ImageFont.truetype(_FONT, size // 17)
        w = d.textlength(label, font=font)
        d.text(((size - w) / 2, size * 0.885), label, fill=(240, 228, 255), font=font, stroke_width=max(2, size // 150), stroke_fill=(28, 16, 48))
    return img
