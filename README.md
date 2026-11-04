# zrdz
## ACONITE Minecraft pack

Minecraft-style **Aconite (monkshood) flower** + **136 custom head cosmetics** (incl. 13 memes and 6 Taggy & Froggie pieces) (incl. a 21-piece trendy batch: coquette bow, kitsune mask, Happy Ghast, copper golem, shark hood, boba, capybara...) (cat ears, crowns, horns, hats, buddies...), all in the ACONITE purple/green palette where it fits.

- `resourcepack/` — drop into `.minecraft/resourcepacks` (made for Java 1.21.4+). Every model is a Blockbench-compatible Java JSON with its own hand-shaded texture atlas (2x player-skin pixel density, per-face shading, edge highlights, metal sheen).
- `give_commands.txt` — one `/give` per head, e.g. `/give @p minecraft:paper[item_model="aconite:cat_ears_black",equippable={slot:"head"}]`
- `previews/all_heads.png` — every head, each shown on a different test head (8 skins in `tools/skins/`). `previews/fit_check.png` puts the trickiest fits on all 8 heads. Single renders in `previews/heads/`, flowers in `previews/final_flowers.png`.
- `tools/build.py` — regenerates everything (`python tools/build.py`, needs numpy + pillow). Designs live in `tools/designs.py`.

Aconite growth: 6 stages (sprout, leaves, yellow buds, buds turning purple, 2 blocks tall, full bloom) as `aconite:block/aconite_stage0..5`, plus a yellow **wolfsbane** variant. `previews/final_flowers.png` shows them all.
- `addon_aconite_crop/` (optional, load above the main pack) re-skins the vanilla **pitcher crop** (age 0-4, grows 2 blocks tall) as aconite, so planting pitcher pods grows a real aconite in survival.

Head previews use lojjkli's real skin (`tools/skins/lojjkli.png`).

Aconite flower: `aconite:block/aconite_top|bottom` (2-block cross plant like lilac), `aconite:block/potted_aconite`, item `aconite:aconite`. A real placeable block needs a mod/datapack; the pack supplies the models and textures.

Fit: models use the vanilla `head` display (face = north, 1 head pixel = 1.6 model units). Every outer surface clears the skin's hat layer (0.5px out), so hair/hat pixels never poke through.
