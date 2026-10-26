"""Build the ACONITE resource pack + previews.  python tools/build.py"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
from mclib import Model, render, player_head, skin_head, hex2rgb
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
       'b': hex2rgb('#6fb04a'), 'y': hex2rgb('#f2d43a'), 'Y': hex2rgb('#fff08a'), 'o': hex2rgb('#c9d84a'),
       'O': hex2rgb('#c9a227')}
SKIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skins", "lojjkli.png")

# growth stages: sprout -> leaves -> yellow buds -> buds turn purple -> 2 blocks tall -> full bloom
STAGE0 = ["................"] * 11 + [
          "....LL...LL.....",
          "...LGLL.LLGL....",
          ".....LGsGL......",
          ".......s........",
          ".......s........"]
STAGE1 = ["................"] * 7 + [
          "...L.L....L.L...",
          "..LGLGL..LGLGL..",
          "...LGGLsLGGL....",
          ".L..LGGsGGL..L..",
          "..LL.LGsGL.LL...",
          "....LLGsGLL.....",
          "......LsL.......",
          ".......s........"]
STAGE2 = ["................",
          "................",
          ".......Y........",
          "......yYy.......",
          ".......s.oy.....",
          "....yo.s........",
          ".......s.yo.....",
          "....oy.s........",
          ".......s........",
          "...L.L.s..L.L...",
          "..LGLGLs.LGLGL..",
          "...LGGLsLGGL....",
          ".L..LGGsGGL..L..",
          "..LL.LGsGL.LL...",
          "....LLGsGLL.....",
          ".......s........"]
STAGE3 = [".......Y........",
          "......yYy.......",
          ".......s.oy.....",
          "....yy.s........",
          ".......s.ddd....",
          "...ddd.sdlpd....",
          "..dppl.s.lp.....",
          "...lp..s........",
          ".......s........",
          "...L.L.s..L.L...",
          "..LGLGLs.LGLGL..",
          "...LGGLsLGGL....",
          ".L..LGGsGGL..L..",
          "..LL.LGsGL.LL...",
          "....LLGsGLL.....",
          ".......s........"]
STAGE4_TOP = ["................",
              "................",
              ".......Y........",
              "......yYy.......",
              ".......s.yo.....",
              "....oy.s........",
              ".......s.ddd....",
              "...ddd.sdlppd...",
              "..dppl.s.llld...",
              "..dlll.s..lp....",
              "...lp..s........",
              ".......s.ddd....",
              "...ddd.sdlppd...",
              "..dppl.s.lll....",
              "...lp..s..lp....",
              ".......s........"]
WOLFSBANE = str.maketrans({'p': 'y', 'l': 'Y', 'd': 'O', 'g': 'Y'})
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

def grass_block(y=-16, x=0, z=0, seed=1):
    """Vanilla-style grass block: tinted grass top, dirt sides with a ragged grass lip."""
    rng = np.random.default_rng(seed)
    GR = [(76, 128, 44), (89, 145, 52), (99, 160, 58), (110, 172, 64), (121, 184, 72)]
    DI = [(89, 61, 41), (105, 74, 51), (121, 85, 58), (134, 96, 67), (150, 108, 75)]
    pick = lambda pal, wts: pal[rng.choice(len(pal), p=wts)]
    top = np.zeros((16, 16, 4), np.uint8); side = np.zeros((16, 16, 4), np.uint8); dirt = np.zeros((16, 16, 4), np.uint8)
    for yy in range(16):
        for xx in range(16):
            top[yy, xx] = pick(GR, [.12, .25, .3, .23, .1]) + (255,)
            dirt[yy, xx] = pick(DI, [.1, .2, .35, .25, .1]) + (255,)
    side[:] = dirt
    for xx in range(16):
        drip = rng.choice([1, 2, 2, 3, 3, 4])
        for yy in range(drip):
            side[yy, xx] = tuple(int(c * 0.92) for c in pick(GR, [.15, .3, .3, .2, .05])) + (255,)
    full = [0, 0, 16, 16]
    return [dict(f=[x, y, z], t=[x + 16, y + 16, z + 16], rot=None,
                 faces={"north": (side, full), "south": (side, full), "east": (side, full), "west": (side, full),
                        "up": (top, full), "down": (dirt, full)})]

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
    # growth stages + yellow wolfsbane
    stages = [("aconite_stage0", STAGE0, None, "Sprout"), ("aconite_stage1", STAGE1, None, "Leaves"),
              ("aconite_stage2", STAGE2, None, "Yellow buds"), ("aconite_stage3", STAGE3, None, "Buds turning"),
              ("aconite_stage4", BOTTOM, STAGE4_TOP, "2 blocks tall"), ("aconite_stage5", BOTTOM, TOP, "Full bloom")]
    for name, lo, hi, _ in stages:
        if hi is None:
            w(f"{T}/{name}.png", pix(lo))
            w(f"{M}/block/{name}.json", {"parent": "minecraft:block/cross", "textures": {"cross": f"aconite:block/{name}"}})
            tex_item = name
        else:
            w(f"{T}/{name}_bottom.png", pix(lo)); w(f"{T}/{name}_top.png", pix(hi))
            for half in ("bottom", "top"):
                w(f"{M}/block/{name}_{half}.json", {"parent": "minecraft:block/cross", "textures": {"cross": f"aconite:block/{name}_{half}"}})
            tex_item = f"{name}_top"
        w(f"{M}/item/{name}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"aconite:block/{tex_item}"}})
        w(os.path.join(A, "items", f"{name}.json"), {"model": {"type": "minecraft:model", "model": f"aconite:item/{name}"}})
    wolf_top = pix([r.translate(WOLFSBANE) for r in TOP])
    w(f"{T}/wolfsbane_top.png", wolf_top); w(f"{T}/wolfsbane_bottom.png", bot)
    for half in ("bottom", "top"):
        w(f"{M}/block/wolfsbane_{half}.json", {"parent": "minecraft:block/cross", "textures": {"cross": f"aconite:block/wolfsbane_{half}"}})
    w(f"{M}/item/wolfsbane.json", {"parent": "minecraft:item/generated", "textures": {"layer0": "aconite:block/wolfsbane_top"}})
    w(os.path.join(A, "items", "wolfsbane.json"), {"model": {"type": "minecraft:model", "model": "aconite:item/wolfsbane"}})
    build_crop_addon(stages)

    os.makedirs(PV + "/aconite", exist_ok=True)
    tiles = []
    for i, (name, lo, hi, label) in enumerate(stages):
        els = cross(pix(lo)) + (cross(pix(hi), 16) if hi else [])
        # fixed framing so the plants visibly grow
        els += [dict(f=[-2, 0, 8], t=[18, 33, 8], rot=None, faces={"north": (np.zeros((1, 1, 4), np.uint8), [0, 0, 1, 1])})]
        tiles.append(render(els, size=480, yaw=-8, label=f"{i + 1}. {label}", bg=SKY))
    frame = [dict(f=[-2, 0, 8], t=[18, 33, 8], rot=None, faces={"north": (np.zeros((1, 1, 4), np.uint8), [0, 0, 1, 1])})]
    tiles.append(render(cross(bot) + cross(pix([r.translate(WOLFSBANE) for r in TOP]), 16) + frame, size=480, yaw=-8,
                        label="7. Yellow Wolfsbane", bg=SKY))
    strip = Image.new("RGB", (480 * 4, 480 * 2), SKY[1])
    for i, t in enumerate(tiles):
        strip.paste(t, ((i % 4) * 480, (i // 4) * 480))
    strip.save(PV + "/aconite/growth_stages.png")
    globals()["_flower_tiles"] = strip
    render(cross(bot) + cross(wolf_top, 16), size=512, yaw=-8, label="Yellow Wolfsbane", bg=SKY).save(PV + "/aconite/wolfsbane.png")

    # 3D chunky aconite (cuboid) for item frames / display entities / hats
    m = Model("aconite_3d", "Aconite (3D)")
    m.box(-0.35, -5, -0.35, 0.35, 0, 0.35, DS.STEM)
    for (lx, lz, ly, rot) in [(-1, 0, -4.6, 0), (1, 0, -3.6, 0), (0, -1, -2.6, 0), (0, 1, -1.6, 0)]:
        # deeply-cut palmate leaves: three fingers each
        for f, (fx, fz) in enumerate([(lx, lz), (lx + lz * 0.7, lz + lx * 0.7), (lx - lz * 0.7, lz - lx * 0.7)]):
            ex, ez = fx * 3.2, fz * 3.2
            m.box(min(0, ex) - 0.45, ly, min(0, ez) - 0.45, max(0, ex) + 0.45, ly + 0.4, max(0, ez) + 0.45, DS.LEAF if f else DS.LEAF_D)
    DS.aconite_spike(m, 0, -1, 0, h=6, s=1.7)
    tex = m.texture()
    w(f"{A}/textures/item/aconite_3d.png", tex)
    j = m.to_json("aconite:item/aconite_3d"); j["display"]["head"] = {"translation": [0, 8, 0]}
    w(f"{M}/item/aconite_3d.json", j)
    w(os.path.join(A, "items", "aconite_3d.json"), {"model": {"type": "minecraft:model", "model": "aconite:item/aconite_3d"}})

    os.makedirs(PV + "/aconite", exist_ok=True)
    render(cross(bot) + cross(top, 16), size=640, yaw=-8, label="Aconite (2-block flower)", bg=SKY).save(PV + "/aconite/aconite_flower.png")
    pot = [solid([5, 0, 5], [11, 6, 11], (150, 76, 52), 5), solid([6, 5.9, 6], [10, 6, 10], (70, 45, 30), 2)]
    render(pot + cross(small, 4, 0.75, (8, 8)), size=512, label="Potted Aconite").save(PV + "/aconite/potted_aconite.png")
    render(m.render_elements(tex), size=512, label="Aconite (3D model)").save(PV + "/aconite/aconite_3d.png")
    final = globals()["_flower_tiles"]
    final.paste(render(m.render_elements(tex), size=480, label="8. Aconite 3D model", bg=SKY), (3 * 480, 480))
    final.save(PV + "/final_flowers.png")
    big = Image.new("RGBA", (16 * 3 * 16 + 40, 16 * 16 + 20), (20, 10, 32, 255))
    for i, t in enumerate([top, bot, small]):
        big.paste(t.resize((256, 256), Image.NEAREST), (10 + i * 266, 10), t.resize((256, 256), Image.NEAREST))
    big.crop((0, 0, 3 * 266 + 10, 276)).save(PV + "/aconite/textures.png")

SKY = ((121, 166, 255), (196, 222, 255))

def build_crop_addon(stages):
    """Optional add-on: re-skins the vanilla pitcher crop (age 0-4, grows 2 blocks tall)
    as a growing aconite. Plant pitcher pods and watch it grow."""
    C = os.path.join(ROOT, "addon_aconite_crop")
    w(os.path.join(C, "pack.mcmeta"), {"pack": {"pack_format": 46, "supported_formats": [46, 99],
                                                 "description": "\u00a75ACONITE \u00a77crop: pitcher crop grows as aconite (needs main pack)"}})
    w(os.path.join(C, "assets/aconite/models/block/empty.json"), {"textures": {"particle": "aconite:block/aconite_bottom"}, "elements": []})
    lower = ["aconite_stage0", "aconite_stage1", "aconite_stage2", "aconite_stage4_bottom", "aconite_stage5_bottom"]
    upper = ["empty", "empty", "empty", "aconite_stage4_top", "aconite_stage5_top"]
    v = {}
    for age in range(5):
        v[f"age={age},half=lower"] = {"model": f"aconite:block/{lower[age]}"}
        v[f"age={age},half=upper"] = {"model": f"aconite:block/{upper[age]}"}
    w(os.path.join(C, "assets/minecraft/blockstates/pitcher_crop.json"), {"variants": v})

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
        img = render(skin_head(SKIN) + m.render_elements(tex), size=384, label=title)
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
