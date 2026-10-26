"""Tiny Minecraft model toolkit: build cuboid models in 'head pixel' space,
write Java resource-pack JSON + 16x16 textures, and render previews."""
import json, math, os, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont

S = 1.6  # 1 player-head pixel = 1.6 model units when worn (head = 1.6..14.4)

def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + ((int(h[6:8], 16),) if len(h) == 8 else (255,))

class Model:
    def __init__(self, name, title, tier="basic"):
        self.name, self.title, self.tier = name, title, tier
        self.boxes = []
        self.colors = []

    def box(self, x1, y1, z1, x2, y2, z2, c, rot=None, flat=False):
        """Box in head-pixel coords (head = -4..4 on every axis, front = north/-z).
        rot = (axis, angle, (ox, oy, oz))"""
        if c not in self.colors:
            self.colors.append(c)
        a, b = sorted((x1, x2)), (sorted((y1, y2)), sorted((z1, z2)))
        self.boxes.append(dict(f=(a[0], b[0][0], b[1][0]), t=(a[1], b[0][1], b[1][1]), c=c, rot=rot))
        return self

    # ---- export -------------------------------------------------------
    def texture(self):
        assert len(self.colors) <= 16, (self.name, len(self.colors))
        img = np.zeros((16, 16, 4), np.uint8)
        rng = np.random.default_rng(int(hashlib.md5(self.name.encode()).hexdigest()[:8], 16))
        for i, c in enumerate(self.colors):
            r, g, b, a = hex2rgb(c)
            u, v = (i % 4) * 4, (i // 4) * 4
            for y in range(4):
                for x in range(4):
                    k = 1 + rng.choice([-0.07, -0.035, 0, 0, 0.035, 0.06])
                    img[v + y, u + x] = [min(255, int(r * k)), min(255, int(g * k)), min(255, int(b * k)), a]
        return Image.fromarray(img, 'RGBA')

    def uv(self, c):
        i = self.colors.index(c)
        return [(i % 4) * 4, (i // 4) * 4, (i % 4) * 4 + 4, (i // 4) * 4 + 4]

    def to_json(self, texref):
        els = []
        for bx in self.boxes:
            f = [round(8 + S * v, 3) for v in bx['f']]
            t = [round(8 + S * v, 3) for v in bx['t']]
            e = {"from": f, "to": t,
                 "faces": {d: {"uv": self.uv(bx['c']), "texture": "#0"} for d in
                           ("north", "east", "south", "west", "up", "down")}}
            if bx['rot']:
                ax, ang, o = bx['rot']
                e["rotation"] = {"angle": ang, "axis": ax, "origin": [round(8 + S * v, 3) for v in o]}
            els.append(e)
        return {"credit": "ACONITE cosmetics", "texture_size": [16, 16],
                "textures": {"0": texref, "particle": texref},
                "elements": els,
                "display": {"head": {"rotation": [0, 180, 0], "translation": [0, 0, 0], "scale": [1, 1, 1]},
                            "gui": {"rotation": [30, 45, 0], "translation": [0, -1, 0], "scale": [0.5, 0.5, 0.5]},
                            "thirdperson_righthand": {"rotation": [75, 45, 0], "translation": [0, 2.5, 0], "scale": [0.375] * 3},
                            "firstperson_righthand": {"rotation": [0, 45, 0], "scale": [0.4] * 3},
                            "ground": {"translation": [0, 3, 0], "scale": [0.25] * 3},
                            "fixed": {"scale": [0.5] * 3}}}

    def render_elements(self, tex):
        """Elements in renderer format (model units, rgba texture, uv per face)."""
        arr = np.array(tex)
        out = []
        for bx in self.boxes:
            f = [8 + S * v for v in bx['f']]
            t = [8 + S * v for v in bx['t']]
            u = self.uv(bx['c'])
            out.append(dict(f=f, t=t, rot=bx['rot'] and (bx['rot'][0], bx['rot'][1], [8 + S * v for v in bx['rot'][2]]),
                            faces={d: (arr, u) for d in ("north", "east", "south", "west", "up", "down")}))
        return out

# ---- player head for previews ----------------------------------------
def player_head():
    sk = np.zeros((8, 8, 4), np.uint8); sk[:] = (198, 150, 116, 255)
    hair = (62, 40, 30, 255)
    face = sk.copy(); face[0:2] = hair; face[2, 0] = hair; face[2, 7] = hair
    face[4, 1] = face[4, 6] = (255, 255, 255, 255); face[4, 2] = face[4, 5] = (70, 60, 140, 255)
    face[6, 3:5] = (120, 70, 60, 255)
    side = sk.copy(); side[0:3] = hair
    back = sk.copy(); back[0:6] = hair
    top = sk.copy(); top[:] = hair
    full = [0, 0, 8, 8]
    return dict(f=[1.6] * 3, t=[14.4] * 3, rot=None,
                faces={"north": (face, full), "south": (back, full), "east": (side, full),
                       "west": (side, full), "up": (top, full), "down": (sk, full)})

# ---- renderer ---------------------------------------------------------
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

def render(elements, size=512, yaw=-32, pitch=24, bg=((40, 18, 60), (12, 6, 22)), label=None):
    ya, pa = math.radians(yaw), math.radians(pitch)
    cam = np.array([math.sin(ya) * math.cos(pa), math.sin(pa), -math.cos(ya) * math.cos(pa)])
    fwd = -cam
    right = np.cross(fwd, [0, 1, 0]); right /= np.linalg.norm(right)
    right = -right  # screen x
    up = np.cross(right, fwd) * -1
    up = np.array([0, 1, 0]) - fwd * fwd[1]; up /= np.linalg.norm(up)
    light = lambda n: abs(n[0]) * 0.62 + abs(n[2]) * 0.82 + (n[1] * 1.0 if n[1] > 0 else -n[1] * 0.5)
    quads = []
    for el in elements:
        a, b = el['f'], el['t']
        R, O = (rotmat(el['rot'][0], el['rot'][1]), np.array(el['rot'][2])) if el['rot'] else (None, None)
        tf = (lambda p: R @ (np.array(p) - O) + O) if R is not None else (lambda p: np.array(p, float))
        tn = (lambda n: R @ np.array(n, float)) if R is not None else (lambda n: np.array(n, float))
        flat = [b[i] - a[i] < 1e-6 for i in range(3)]
        for d, (n, geo) in FACES.items():
            if d not in el['faces']:
                continue
            nw = tn(n)
            twosided = any(flat)
            if not twosided and np.dot(nw, cam) <= 0:
                continue
            o, du, dv = geo(a, b)
            arr, uv = el['faces'][d]
            u0, v0, u1, v1 = uv
            nu, nv = max(1, round(abs(u1 - u0))), max(1, round(abs(v1 - v0)))
            sh = light(nw if np.dot(nw, cam) > 0 else -nw)
            o, du, dv = np.array(o, float), np.array(du, float), np.array(dv, float)
            for j in range(nv):
                for i in range(nu):
                    tx = int(u0 + (i + 0.5) * (u1 - u0) / nu)
                    ty = int(v0 + (j + 0.5) * (v1 - v0) / nv)
                    px = arr[min(ty, arr.shape[0]-1), min(tx, arr.shape[1]-1)]
                    if px[3] < 128:
                        continue
                    p = [o + du * (i / nu) + dv * (j / nv), o + du * ((i + 1) / nu) + dv * (j / nv),
                         o + du * ((i + 1) / nu) + dv * ((j + 1) / nv), o + du * (i / nu) + dv * ((j + 1) / nv)]
                    p = [tf(q) for q in p]
                    cen = sum(p) / 4
                    col = tuple(int(min(255, c * sh)) for c in px[:3])
                    quads.append((np.dot(cen, fwd) - 0.001 * np.dot(nw, cam), p, col))
    quads.sort(key=lambda q: -q[0])
    pts = np.array([[np.dot(v, right), np.dot(v, up)] for q in quads for v in q[1]])
    mn, mx = pts.min(0), pts.max(0)
    ss = 2
    W = size * ss
    sc = (W * 0.78) / max(mx - mn)
    ctr = (mn + mx) / 2
    img = Image.new('RGB', (W, W))
    g = ImageDraw.Draw(img)
    for y in range(W):
        t = y / W
        g.line([(0, y), (W, y)], fill=tuple(int(bg[0][k] * (1 - t) + bg[1][k] * t) for k in range(3)))
    off = 0.04 * W if label else 0
    for _, p, col in quads:
        poly = [((np.dot(v, right) - ctr[0]) * sc + W / 2, -(np.dot(v, up) - ctr[1]) * sc + W / 2 - off) for v in p]
        g.polygon(poly, fill=col, outline=col)
    img = img.resize((size, size), Image.LANCZOS)
    if label:
        d = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size // 18)
        except OSError:
            font = ImageFont.load_default()
        w = d.textlength(label, font=font)
        d.text(((size - w) / 2, size * 0.9), label, fill=(235, 220, 255), font=font)
    return img
