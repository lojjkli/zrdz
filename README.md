# AconiteCosmetics

Paper plugin with all 468 aconite cosmetics and the aconite flower.

## Install

1. Put `AconiteCosmetics-1.0.0.jar` in your server's `plugins` folder and start the server.
2. The plugin sends the resource pack to players when they join. It hosts the pack itself on port `8164`,
   so open that port and set `resource-pack.public-address` in `plugins/AconiteCosmetics/config.yml`
   to your server's IP or domain. Or upload the pack somewhere and put the link in `resource-pack.url`.

## Use

- `/cosmetics` opens the menu. Pick a topic, then click a cosmetic to wear it.
  Click the search head and type a word in chat to search.
- The cosmetic shows on whatever helmet you wear, and the helmet keeps its protection.
  Take the helmet off and it is a normal helmet again. With no helmet on, the cosmetic is worn on its own.
- Cosmetics can't be renamed in an anvil, upgraded in a smithing table or used in a grindstone.
- The aconite flower: plant **Aconite Seeds** on farmland. Fully grown, it drops an aconite and more seeds.
  Breaking grass sometimes drops seeds.
- Admin: `/aconite give <player> <aconite|wolfsbane|aconite_seeds> [amount]` and `/aconite reload`.

## Add new cosmetics

1. Add the model to the resource pack (`assets/aconite/items/<id>.json` and its model and texture).
2. Copy the new pack over `plugins/AconiteCosmetics/aconite_server_pack.zip` and run `/aconite reload`.
   New models show up in the menu by themselves. To give one a nicer name, add it to `cosmetics.yml`:

```yaml
my_new_hat:
  name: "My New Hat"
  category: "Hats & Caps"
```

New models without an entry go in the "New" topic. Topics and their icons are set in `config.yml`.

**Animated cosmetics** work two ways:
- Animated texture: add a `.png.mcmeta` next to the texture in the pack. Nothing to change in the plugin.
- Model frames: list the models and the plugin swaps them while it is worn.

```yaml
spinning_hat:
  name: "Spinning Hat"
  category: "Hats & Caps"
  frames: [aconite:spinning_hat_1, aconite:spinning_hat_2, aconite:spinning_hat_3]
  frame-ticks: 4   # 20 ticks = 1 second
```

## Build

`mvn package -Dpaper.version=<paper api version>`. GitHub Actions builds it against the newest Paper API
and puts the jar on the `dev-build` release.
