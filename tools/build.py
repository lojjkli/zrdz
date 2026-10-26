"""Build the ACONITE resource pack + previews.  python tools/build.py"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
from mclib import Model, render, player_head, hex2rgb
import designs as DS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RP = os.path.join(ROOT, "resourcepack")
A = os.path.join(RP, "assets", "aconite")
PV = os.path.join(ROOT, "previews")

def w(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if isinstance(data, Image.Image):
        data.save(path)
    else:
        with open(path, "w") as f:
            json.dump(data, f, indent=1)

# ---------------- aconite plant pixel art ----------------
PAL = {'.': (0, 0, 0, 0), 's': hex2rgb(DS.STEM), 'd': hex2rgb(DS.AC_DARK), 'p': hex2rgb(DS.AC),
       'l': hex2rgb(DS.AC_LIGHT), 'g': hex2rgb(DS.AC_GLOW), 'L': hex2rgb(DS.LEAF), 'G': hex2rgb(DS.LEAF_D),
       'b': hex2rgb('#6fb04a')}
TOP = [".......gl.......",
       "......glpd......",
       "......lppd......",
       ".......s........",
       "....ddds.ddd....",
       "...dppls.lppd...",
       "...dllld.slld...",
       "....lp.s..pl....",
       ".......s........",
       "..dddd.s.dddd...",
       "..dpppls.lpppd..",
       "..dllll.s.llld..",
       "...lpp.s..ppl...",
       ".......s........",
       "....b..s..b.....",
       ".......s........"]
BOTTOM = [".......s........",
          ".......s........",
          "...L.L.s..L.L...",
          "..LGL.Ls.LGL.L..",
          "...LGLGs.GLGL...",
          ".L..LGGsGGL..L..",
          "..LL.LGsGL.LL...",
          "....LLGsGLL.....",
          ".......s........",
          "..L.L..s...L.L..",
          ".LGLGL.s.LGLGL..",
          "..LGGLGsGLGGL...",
          "...LLGGsGGLL....",
          ".....LGsGL......",
          "......LsL.......",
          ".......s........"]
SMALL = ["................",
         "................",
         ".......gg.......",
         "......glpd......",
         "......dpp.......",
         "....ddds.ddd....",
         "...dpll.sdlpd...",
         "....lp..s.lp....",
         ".......ss.......",
         "..L.L..s..L.L...",
         ".LGLGL.s.LGLGL..",
         "..LGGLGsGLGGL...",
         "...LLGGsGGLL....",
         ".....LGsGL......",
         "......LsL.......",
         ".......s........"]

def pix(rows):
    rng = np.random.default_rng(7)
    a = np.zeros((16, 16, 4), np.uint8)
    for y, r in enumerate(rows):
        assert len(r) == 16, (y, r)
        for x, ch in enumerate(r):
            c = PAL[ch]
            k = 1 + rng.choice([-0.06, 0, 0, 0.05]) if c[3] else 1
            a[y, x] = [min(255, int(v * k)) for v in c[:3]] + [c[3]]
    return Image.fromarray(a, "RGBA")

def cross(tex, y0=0.0, scale=1.0, ctr=(8, 8)):
    arr = np.array(tex); full = [0, 0, 16, 16]
    h = 16 * scale; r = 7.2 * scale
    els = []
    for ang in (45, -45):
        els.append(dict(f=[ctr[0] - r, y0, ctr[1]], t=[ctr[0] + r, y0 + h, ctr[1]], rot=('y', ang, [ctr[0], 8, ctr[1]]),
                        faces={"north": (arr, full), "south": (arr, full)}))
    return els

def solid(f, t, col, tex_noise=7):
    rng = np.random.default_rng(tex_noise)
    a = np.zeros((16, 16, 4), np.uint8)
    for y in range(16):
        for x in range(16):
            k = 1 + rng.choice([-0.08, -0.04, 0, 0.04, 0.07])
            a[y, x] = [min(255, int(c * k)) for c in col[:3]] + [255]
    full = [0, 0, 16, 16]
    return dict(f=f, t=t, rot=None, faces={d: (a, full) for d in ("north", "south", "east", "west", "up", "down")})

def grass_block(y=-16):
    g = solid([0, y, 0], [16, y + 16, 16], (122, 86, 58))
    top = solid([0, y + 15.99, 0], [16, y + 16.01, 16], (95, 168, 58), 3)
    return [g, top]

def build_aconite():
    top, bot, small = pix(TOP), pix(BOTTOM), pix(SMALL)
    T = os.path.join(A, "textures", "block")
    w(f"{T}/aconite_top.png", top); w(f"{T}/aconite_bottom.png", bot); w(f"{T}/aconite_small.png", small)
    M = os.path.join(A, "models")
    w(f"{M}/block/aconite_top.json", {"parent": "minecraft:block/cross", "textures": {"cross": "aconite:block/aconite_top"}})
    w(f"{M}/block/aconite_bottom.json", {"parent": "minecraft:block/cross", "textures": {"cross": "aconite:block/aconite_bottom"}})
    w(f"{M}/block/potted_aconite.json", {"parent": "minecraft:block/flower_pot_cross", "textures": {"plant": "aconite:block/aconite_small"}})
    w(f"{M}/item/aconite.json", {"parent": "minecraft:item/generated", "textures": {"layer0": "aconite:block/aconite_top"}})
    w(os.path.join(A, "items", "aconite.json"), {"model": {"type": "minecraft:model", "model": "aconite:item/aconite"}})
    # 3D chunky aconite (cuboid) for item frames / display entities / hats
    m = Model("aconite_3d", "Aconite (3D)")
    m.box(-0.3, -5, -0.3, 0.3, 4.5, 0.3, DS.STEM)
    for s, y in [(-1, -4.5), (1, -3.3), (-1, -2.0)]:
        m.box(min(0, s * 3.2), y, -1.2, max(0, s * 3.2), y + 0.4, 1.2, DS.LEAF)
        m.box(min(0, s * 2.4), y + 0.4, -0.5, max(0, s * 2.4), y + 0.7, 0.5, DS.LEAF_D)
    for i in range(6):
        y = -0.6 + i * 1.1; wd = 1.8 - i * 0.22; s = 1 if i % 2 else -1
        x = s * 0.8 * (1 - i / 7)
        m.box(x - wd / 2, y, -wd / 2, x + wd / 2, y + 0.8, wd / 2, DS.AC if i % 2 else DS.AC_LIGHT)
        m.box(x - wd / 2, y + 0.8, -wd / 2 - 0.2, x + wd / 3, y + 1.05, wd / 3, DS.AC_DARK)
    m.box(-0.35, 6, -0.35, 0.35, 6.8, 0.35, DS.AC_GLOW)
    tex = m.texture()
    w(f"{A}/textures/item/aconite_3d.png", tex)
    j = m.to_json("aconite:item/aconite_3d"); j["display"]["head"] = {"translation": [0, 8, 0]}
    w(f"{M}/item/aconite_3d.json", j)
    w(os.path.join(A, "items", "aconite_3d.json"), {"model": {"type": "minecraft:model", "model": "aconite:item/aconite_3d"}})

    os.makedirs(PV + "/aconite", exist_ok=True)
    render(grass_block() + cross(bot) + cross(top, 16), size=640, yaw=-8, label="Aconite (2-block flower)").save(PV + "/aconite/aconite_flower.png")
    pot = [solid([5, 0, 5], [11, 6, 11], (150, 76, 52), 5), solid([6, 5.9, 6], [10, 6, 10], (70, 45, 30), 2)]
    render(pot + cross(small, 4, 0.75, (8, 8)), size=512, label="Potted Aconite").save(PV + "/aconite/potted_aconite.png")
    render(m.render_elements(tex), size=512, label="Aconite (3D model)").save(PV + "/aconite/aconite_3d.png")
    big = Image.new("RGBA", (16 * 3 * 16 + 40, 16 * 16 + 20), (20, 10, 32, 255))
    for i, t in enumerate([top, bot, small]):
        big.paste(t.resize((256, 256), Image.NEAREST), (10 + i * 266, 10), t.resize((256, 256), Image.NEAREST))
    big.crop((0, 0, 3 * 266 + 10, 276)).save(PV + "/aconite/textures.png")

def build_heads():
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
    thumbs = []
    lines = []
    for name, title, tier, fn in DS.D:
        m = Model(name, title, tier); fn(m)
        tex = m.texture()
        w(f"{A}/textures/item/heads/{name}.png", tex)
        w(f"{A}/models/item/heads/{name}.json", m.to_json(f"aconite:item/heads/{name}"))
        w(f"{A}/items/{name}.json", {"model": {"type": "minecraft:model", "model": f"aconite:item/heads/{name}"}})
        img = render([player_head()] + m.render_elements(tex), size=384, label=title)
        img.save(f"{PV}/heads/{name}.png") if os.path.isdir(f"{PV}/heads") else (os.makedirs(f"{PV}/heads"), img.save(f"{PV}/heads/{name}.png"))
        thumbs.append((img, tier))
        lines.append(f'/give @p minecraft:carved_pumpkin[item_model="aconite:{name}",item_name="{title}",equippable={{slot:"head"}}]')
    with open(os.path.join(ROOT, "give_commands.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    # contact sheets
    cols, ts = 10, 192
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * ts, rows * ts), (10, 5, 18))
    for i, (im, tier) in enumerate(thumbs):
        t = im.resize((ts, ts), Image.LANCZOS)
        if tier == "cool":
            ImageDraw.Draw(t).rectangle([1, 1, ts - 2, ts - 2], outline=(196, 155, 255), width=3)
        sheet.paste(t, ((i % cols) * ts, (i // cols) * ts))
    sheet.save(f"{PV}/all_heads.png")
    print(len(thumbs), "heads")

if __name__ == "__main__":
    w(os.path.join(RP, "pack.mcmeta"), {"pack": {"pack_format": 46, "supported_formats": [46, 99],
                                                  "description": "§5ACONITE §7flower + custom heads"}})
    build_aconite()
    build_heads()
