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

    # previews: plain white, no text, no blocks
    os.makedirs(PV + "/aconite", exist_ok=True)
    frame = [dict(f=[-2, 0, 8], t=[18, 33, 8], rot=None, faces={"north": (np.zeros((1, 1, 4), np.uint8), [0, 0, 1, 1])})]
    plants = [(f"stage{i + 1}", cross(pix(lo)) + (cross(pix(hi), 16) if hi else [])) for i, (name, lo, hi, _) in enumerate(stages)]
    plants.append(("wolfsbane", cross(bot) + cross(wolf_top, 16)))
    tiles = []
    for name, els in plants:
        img = render(els + frame, size=480, yaw=-8, plain=True)   # same framing so the plants visibly grow
        img.save(f"{PV}/aconite/{name}.png"); tiles.append(img)
    strip = Image.new("RGB", (400 * len(tiles), 480), "white")
    for i, t in enumerate(tiles):
        strip.paste(t.crop((40, 0, 440, 480)), (i * 400, 0))
    strip.save(PV + "/final_flowers.png")

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

SKINS = sorted(f for f in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "skins")) if f.endswith(".png"))
SKINS.remove("lojjkli.png"); SKINS.insert(0, "lojjkli.png")
skin = lambda i: skin_head(os.path.join(os.path.dirname(SKIN), SKINS[i % len(SKINS)]))

VIEWS = [(-32, 24), (0, 8), (90, 12), (150, 24)]
HOME = {"taggy_buddy": "lojjkli", "taggy_wave": "lojjkli", "taggy_froggie_duo": "lojjkli",
        "froggie_buddy": "kaiib", "taggy_mask": "lojjkli", "froglight_crown": "Emii5287",
        "froggie_hat": "kaiib", "taggy_rides_froggie": "lojjkli", "taggy_peek": "lojjkli", "taggy_headphones": "lojjkli",
        "froggie_strawberry": "kaiib", "froggie_mushroom": "kaiib", "froggie_princess": "kaiib", "froggie_flower_crown": "kaiib"}

def sheet(images, cols, ts, path):
    rows = (len(images) + cols - 1) // cols
    out = Image.new("RGB", (cols * ts, rows * ts), "white")
    for i, im in enumerate(images):
        out.paste(im.resize((ts, ts), Image.LANCZOS), ((i % cols) * ts, (i // cols) * ts))
    out.save(path)

_NAMES = [d[0] for d in DS.D]
NEW_BATCH = _NAMES[_NAMES.index('creeper_buddy'):]   # batch 5: the 250 added after the batch-4 crowns/medals

def build_heads():
    thumbs, lines, models, angle_strips = [], [], {}, []
    os.makedirs(f"{PV}/heads", exist_ok=True)
    for i, (name, title, tier, fn) in enumerate(DS.D):
        m = Model(name, title, tier); fn(m)
        tex = m.texture(); models[name] = m
        w(f"{A}/textures/item/heads/{name}.png", tex)
        w(f"{A}/models/item/heads/{name}.json", m.to_json(f"aconite:item/heads/{name}"))
        w(f"{A}/items/{name}.json", {"model": {"type": "minecraft:model", "model": f"aconite:item/heads/{name}"}})
        base = SKINS.index(HOME[name] + ".png") if name in HOME else i   # Taggy/Froggie start on their own rider
        img = render(skin(base) + m.render_elements(), size=384, plain=True)   # each accessory on a different head
        thumbs.append(img)
        # multiple photos: 3/4 front, straight front, side, 3/4 back - each on a different head
        views = [render(skin(base + k) + m.render_elements(), size=300, yaw=yaw, pitch=pitch, plain=True)
                 for k, (yaw, pitch) in enumerate(VIEWS)]
        strip = Image.new("RGB", (300 * len(views), 300), "white")
        for k, v in enumerate(views):
            strip.paste(v, (300 * k, 0))
        strip.save(f"{PV}/heads/{name}.png"); angle_strips.append(strip)
        lines.append(f'/give @p minecraft:paper[item_model="aconite:{name}",item_name="{title}",equippable={{slot:"head"}}]')
    with open(os.path.join(ROOT, "give_commands.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    sheet(thumbs, 12, 200, f"{PV}/all_heads.png")
    # big overview pages: 36 accessories each (6x6)
    for k in range(0, len(thumbs), 36):
        sheet(thumbs[k:k + 36], 6, 280, f"{PV}/all_cosmetics_{k // 36 + 1}.png")
    # angle sheets: 12 accessories per page, 4 photos each
    for page in range(0, len(angle_strips), 12):
        group = angle_strips[page:page + 12]
        out = Image.new("RGB", (1000, 250 * len(group)), "white")
        for r, st in enumerate(group):
            out.paste(st.resize((1000, 250), Image.LANCZOS), (0, 250 * r))
        out.save(f"{PV}/angles_{page // 12 + 1}.png")
    # trendy batch on its own sheets
    for tier, label in (("trend", "trendy"), ("meme", "meme"), ("custom", "taggy_froggie"), ("goofy", "goofy"), ("cute", "cute"), ("cool", "cool"), ("lunar", "headbands"), ("hair", "hair"),
                        ("mob", "mob"), ("food", "food"), ("hats", "hats"), ("face", "face"), ("fantasy", "fantasy"), ("holiday", "holiday")):
        idx = [i for i, d in enumerate(DS.D) if d[2] == tier]
        if not idx:
            continue
        sheet([thumbs[i] for i in idx], min(7, len(idx)), 260, f"{PV}/{label}_heads.png")
        out = Image.new("RGB", (1000 * 2 + 60, 250 * ((len(idx) + 1) // 2)), "white")
        for k, i in enumerate(idx):
            out.paste(angle_strips[i].resize((1000, 250), Image.LANCZOS), ((k % 2) * 1060, 250 * (k // 2)))
        out.save(f"{PV}/{label}_photos.png")
    # latest batch (new trends, goofy, Froggie v2 + Taggy updates): hero shots and 4-angle photos
    new = [i for i, d in enumerate(DS.D) if d[0] in NEW_BATCH]
    for k in range(0, len(new), 36):
        sheet([thumbs[i] for i in new[k:k + 36]], 6, 280, f"{PV}/new_batch_heads_{k // 36 + 1}.png")
    for k in range(0, len(new), 14):
        grp = new[k:k + 14]
        out = Image.new("RGB", (1000 * 2 + 60, 250 * ((len(grp) + 1) // 2)), "white")
        for j, i in enumerate(grp):
            out.paste(angle_strips[i].resize((1000, 250), Image.LANCZOS), ((j % 2) * 1060, 250 * (j // 2)))
        out.save(f"{PV}/new_batch_photos_{k // 14 + 1}.png")
    # fit test: the trickiest fits (tight bands, full helmets, brims, side pieces) on all 8 heads
    test = ["cat_ears_black", "top_hat", "gold_crown", "knight_helmet", "headphones", "aviator_goggles",
            "beanie", "sunglasses", "viking_helmet", "flower_crown"]
    fit = [render(skin(j) + models[n].render_elements(), size=300, plain=True) for n in test for j in range(len(SKINS))]
    sheet(fit, len(SKINS), 200, f"{PV}/fit_check.png")
    # bare heads, for reference
    sheet([render(skin(j), size=300, plain=True) for j in range(len(SKINS))], len(SKINS), 200, f"{PV}/test_heads.png")
    print(len(thumbs), "heads")

if __name__ == "__main__":
    w(os.path.join(RP, "pack.mcmeta"), {"pack": {"pack_format": 46, "supported_formats": [46, 99],
                                                  "description": "§5ACONITE §7flower + custom heads"}})
    build_aconite()
    build_heads()
