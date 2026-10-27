package com.lojjkli.aconite;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.format.NamedTextColor;
import org.bukkit.Material;
import org.bukkit.NamespacedKey;
import org.bukkit.configuration.ConfigurationSection;
import org.bukkit.configuration.file.YamlConfiguration;
import org.bukkit.entity.Player;
import org.bukkit.inventory.EquipmentSlot;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.Damageable;
import org.bukkit.inventory.meta.ItemMeta;
import org.bukkit.inventory.meta.components.EquippableComponent;
import org.bukkit.persistence.PersistentDataType;

/**
 * Loads cosmetics.yml (plus any extra models found in the pack) and turns helmets into cosmetics and back.
 * A cosmetic is a look on the worn helmet: the helmet keeps its stats, and the original is stored inside it
 * so it can be given back unchanged when it leaves the head slot.
 */
public final class Cosmetics {

    public static final String NEW_CATEGORY = "New";

    /** Pack models that are part of the flower, not cosmetics. */
    private static final Set<String> FLOWER_MODELS = Set.of(
            "aconite", "wolfsbane", "aconite_stage0", "aconite_stage1", "aconite_stage2",
            "aconite_stage3", "aconite_stage4", "aconite_stage5");
    private static final Pattern PACK_ITEM = Pattern.compile("assets/aconite/items/([a-z0-9_]+)\\.json");

    private final AconitePlugin plugin;
    private final NamespacedKey idKey;
    private final NamespacedKey originalKey;
    private final NamespacedKey selectedKey;
    private final Map<String, Cosmetic> byId = new LinkedHashMap<>();
    private boolean anyAnimated;

    public Cosmetics(AconitePlugin plugin) {
        this.plugin = plugin;
        this.idKey = new NamespacedKey(plugin, "id");
        this.originalKey = new NamespacedKey(plugin, "original");
        this.selectedKey = new NamespacedKey(plugin, "selected");
    }

    public void load() {
        byId.clear();
        File file = new File(plugin.getDataFolder(), "cosmetics.yml");
        if (!file.exists()) {
            plugin.saveResource("cosmetics.yml", false);
        }
        YamlConfiguration yml = YamlConfiguration.loadConfiguration(file);
        for (String id : yml.getKeys(false)) {
            ConfigurationSection s = yml.getConfigurationSection(id);
            if (s == null) {
                continue;
            }
            List<String> frames = new ArrayList<>(s.getStringList("frames"));
            if (frames.isEmpty()) {
                frames.add(s.getString("model", "aconite:" + id));
            }
            add(id, s.getString("name", prettyName(id)), s.getString("category", NEW_CATEGORY),
                    frames, s.getInt("frame-ticks", 4));
        }
        if (plugin.getConfig().getBoolean("auto-add-from-pack", true)) {
            addFromPack(plugin.packFile());
        }
        anyAnimated = byId.values().stream().anyMatch(Cosmetic::animated);
        plugin.getLogger().info("Loaded " + byId.size() + " cosmetics.");
    }

    private void add(String id, String name, String category, List<String> frames, int frameTicks) {
        List<NamespacedKey> keys = new ArrayList<>();
        for (String frame : frames) {
            NamespacedKey key = NamespacedKey.fromString(frame.toLowerCase(Locale.ROOT));
            if (key == null) {
                plugin.getLogger().warning("Bad model '" + frame + "' for cosmetic " + id);
                return;
            }
            keys.add(key);
        }
        byId.put(id, new Cosmetic(id, name, category, List.copyOf(keys), Math.max(1, frameTicks)));
    }

    private void addFromPack(File pack) {
        if (!pack.isFile()) {
            return;
        }
        try (ZipFile zip = new ZipFile(pack)) {
            for (ZipEntry entry : zip.stream().toList()) {
                Matcher m = PACK_ITEM.matcher(entry.getName());
                if (m.matches() && !FLOWER_MODELS.contains(m.group(1)) && !byId.containsKey(m.group(1))) {
                    String id = m.group(1);
                    add(id, prettyName(id), NEW_CATEGORY, List.of("aconite:" + id), 4);
                }
            }
        } catch (IOException e) {
            plugin.getLogger().warning("Could not read pack: " + e.getMessage());
        }
    }

    private static String prettyName(String id) {
        StringBuilder sb = new StringBuilder();
        for (String word : id.split("_")) {
            if (!word.isEmpty()) {
                sb.append(sb.isEmpty() ? "" : " ").append(Character.toUpperCase(word.charAt(0))).append(word.substring(1));
            }
        }
        return sb.toString();
    }

    public Collection<Cosmetic> all() {
        return byId.values();
    }

    public Cosmetic get(String id) {
        return id == null ? null : byId.get(id);
    }

    public boolean anyAnimated() {
        return anyAnimated;
    }

    // Player selection

    public Cosmetic selected(Player player) {
        return get(player.getPersistentDataContainer().get(selectedKey, PersistentDataType.STRING));
    }

    public void select(Player player, Cosmetic c) {
        if (c == null) {
            player.getPersistentDataContainer().remove(selectedKey);
        } else {
            player.getPersistentDataContainer().set(selectedKey, PersistentDataType.STRING, c.id());
        }
    }

    // Cosmetic items

    public boolean isCosmetic(ItemStack item) {
        return item != null && item.hasItemMeta()
                && item.getItemMeta().getPersistentDataContainer().has(idKey, PersistentDataType.STRING);
    }

    /** The cosmetic this item shows, or null. */
    public Cosmetic of(ItemStack item) {
        if (!isCosmetic(item)) {
            return null;
        }
        return byId.get(item.getItemMeta().getPersistentDataContainer().get(idKey, PersistentDataType.STRING));
    }

    /** Puts the cosmetic look on a helmet. With no helmet, makes a look-only item that disappears when taken off. */
    public ItemStack apply(ItemStack head, Cosmetic c) {
        ItemStack base = restore(head);
        ItemStack item = base == null ? new ItemStack(Material.PAPER) : base.clone();
        item.editMeta(meta -> {
            if (base == null) {
                meta.itemName(Component.text(c.name(), NamedTextColor.LIGHT_PURPLE));
            } else {
                meta.getPersistentDataContainer().set(originalKey, PersistentDataType.BYTE_ARRAY, base.serializeAsBytes());
                meta.lore(List.of(Component.text("Cosmetic: " + c.name(), NamedTextColor.LIGHT_PURPLE)));
            }
            meta.setItemModel(c.model());
            // No armor texture and no pumpkin overlay, so the cosmetic model is what shows on the head.
            EquippableComponent equippable = meta.getEquippable();
            equippable.setSlot(EquipmentSlot.HEAD);
            equippable.setModel(null);
            equippable.setCameraOverlay(null);
            meta.setEquippable(equippable);
            meta.getPersistentDataContainer().set(idKey, PersistentDataType.STRING, c.id());
        });
        return item;
    }

    /** Turns a cosmetic back into the normal helmet (keeping its wear), or null if it had no helmet. */
    public ItemStack restore(ItemStack item) {
        if (item == null || item.isEmpty()) {
            return null;
        }
        if (!isCosmetic(item)) {
            return item;
        }
        ItemMeta meta = item.getItemMeta();
        byte[] bytes = meta.getPersistentDataContainer().get(originalKey, PersistentDataType.BYTE_ARRAY);
        if (bytes == null) {
            return null;
        }
        ItemStack original = ItemStack.deserializeBytes(bytes);
        if (meta instanceof Damageable worn) {
            original.editMeta(Damageable.class, d -> d.setDamage(worn.getDamage()));
        }
        original.setAmount(item.getAmount());
        return original;
    }

    /** Menu icon. Not a cosmetic item itself. */
    public ItemStack icon(Cosmetic c) {
        ItemStack item = new ItemStack(Material.PAPER);
        item.editMeta(meta -> {
            meta.itemName(Component.text(c.name(), NamedTextColor.LIGHT_PURPLE));
            meta.setItemModel(c.model());
            meta.lore(List.of(Component.text("Click to wear", NamedTextColor.GRAY)));
        });
        return item;
    }

    // Flower items

    public ItemStack aconite() {
        return flowerItem("aconite:aconite", "Aconite");
    }

    public ItemStack wolfsbane() {
        return flowerItem("aconite:wolfsbane", "Wolfsbane");
    }

    /** Pitcher pods that look like aconite. Planted, they grow into aconite (the pack reskins the pitcher crop). */
    public ItemStack seeds() {
        ItemStack item = new ItemStack(Material.PITCHER_POD);
        item.editMeta(meta -> {
            meta.itemName(Component.text("Aconite Seeds", NamedTextColor.DARK_PURPLE));
            meta.setItemModel(NamespacedKey.fromString("aconite:aconite_stage0"));
        });
        return item;
    }

    public ItemStack flowerByName(String id) {
        return switch (id) {
            case "aconite" -> aconite();
            case "wolfsbane" -> wolfsbane();
            case "aconite_seeds" -> seeds();
            default -> null;
        };
    }

    private static ItemStack flowerItem(String model, String name) {
        ItemStack item = new ItemStack(Material.PAPER);
        item.editMeta(meta -> {
            meta.itemName(Component.text(name, NamedTextColor.DARK_PURPLE));
            meta.setItemModel(NamespacedKey.fromString(model));
        });
        return item;
    }
}
