# zrdz
## ACONITE Minecraft pack

Minecraft-style **Aconite (monkshood) flower** + **96 custom head cosmetics** (cat ears, crowns, horns, hats, buddies...), all in the ACONITE purple/green palette where it fits.

- `resourcepack/` — drop into `.minecraft/resourcepacks` (made for Java 1.21.4+). Every model is a Blockbench-compatible Java JSON with its own hand-shaded texture atlas (2x player-skin pixel density, per-face shading, edge highlights, metal sheen).
- `give_commands.txt` — one `/give` per head, e.g. `/give @p minecraft:carved_pumpkin[item_model="aconite:cat_ears_black",equippable={slot:"head"}]`
- `previews/all_heads.png` — every head (purple frame = "cool" tier). Single renders in `previews/heads/`, flower renders in `previews/aconite/`.
- `tools/build.py` — regenerates everything (`python tools/build.py`, needs numpy + pillow). Designs live in `tools/designs.py`.

Aconite growth: 6 stages (sprout, leaves, yellow buds, buds turning purple, 2 blocks tall, full bloom) as `aconite:block/aconite_stage0..5`, plus a yellow **wolfsbane** variant. `previews/final_flowers.png` shows them all.
- `addon_aconite_crop/` (optional, load above the main pack) re-skins the vanilla **pitcher crop** (age 0-4, grows 2 blocks tall) as aconite, so planting pitcher pods grows a real aconite in survival.

Head previews use lojjkli's real skin (`tools/skins/lojjkli.png`).

Aconite flower: `aconite:block/aconite_top|bottom` (2-block cross plant like lilac), `aconite:block/potted_aconite`, item `aconite:aconite`, and a chunky 3D version `aconite:aconite_3d`. A real placeable block needs a mod/datapack; the pack supplies the models and textures.

Note: head models are built for the vanilla `head` display slot (face = north). If something sits a bit off in-game, tweak `display.head` in Blockbench.
