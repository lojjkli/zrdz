package com.lojjkli.aconite;

import io.papermc.paper.event.player.AsyncChatEvent;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.format.NamedTextColor;
import net.kyori.adventure.text.serializer.plain.PlainTextComponentSerializer;
import org.bukkit.Bukkit;
import org.bukkit.Material;
import org.bukkit.configuration.ConfigurationSection;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.inventory.InventoryClickEvent;
import org.bukkit.event.inventory.InventoryDragEvent;
import org.bukkit.event.player.PlayerQuitEvent;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.InventoryHolder;
import org.bukkit.inventory.ItemStack;

public final class CosmeticMenu implements Listener {

    private static final int PER_PAGE = 45;
    private static final int[] TOPIC_SLOTS = {10, 11, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23, 24, 25};
    private static final int TOPICS_SEARCH = 30, TOPICS_OFF = 32;
    private static final int PREV = 45, BACK = 47, SEARCH = 48, OFF = 50, NEXT = 53;

    private final AconitePlugin plugin;
    private final Cosmetics cosmetics;
    private final Set<UUID> searching = new HashSet<>();

    public CosmeticMenu(AconitePlugin plugin) {
        this.plugin = plugin;
        this.cosmetics = plugin.cosmetics();
    }

    private static final class Holder implements InventoryHolder {
        final List<Cosmetic> list;
        final List<String> topics;
        final int page;
        Inventory inventory;

        Holder(List<Cosmetic> list, List<String> topics, int page) {
            this.list = list;
            this.topics = topics;
            this.page = page;
        }

        @Override
        public Inventory getInventory() {
            return inventory;
        }
    }

    private Map<String, Cosmetic> topics() {
        Map<String, Cosmetic> topics = new LinkedHashMap<>();
        ConfigurationSection section = plugin.getConfig().getConfigurationSection("topics");
        if (section != null) {
            for (String topic : section.getKeys(false)) {
                topics.put(topic, cosmetics.get(section.getString(topic)));
            }
        }
        for (Cosmetic c : cosmetics.all()) {
            if (topics.get(c.category()) == null) {
                topics.put(c.category(), c);
            }
        }
        topics.keySet().removeIf(t -> cosmetics.all().stream().noneMatch(c -> c.category().equals(t)));
        return topics;
    }

    public void openTopics(Player player) {
        Map<String, Cosmetic> topics = topics();
        Holder holder = new Holder(null, new ArrayList<>(topics.keySet()), 0);
        Inventory inv = Bukkit.createInventory(holder, 36, Component.text("Cosmetics", NamedTextColor.DARK_PURPLE));
        holder.inventory = inv;
        int i = 0;
        for (Map.Entry<String, Cosmetic> topic : topics.entrySet()) {
            if (i >= TOPIC_SLOTS.length) {
                break;
            }
            ItemStack icon = cosmetics.icon(topic.getValue());
            icon.editMeta(meta -> {
                meta.itemName(Component.text(topic.getKey(), NamedTextColor.LIGHT_PURPLE));
                meta.lore(List.of(Component.text(count(topic.getKey()) + " cosmetics", NamedTextColor.GRAY)));
            });
            inv.setItem(TOPIC_SLOTS[i++], icon);
        }
        inv.setItem(TOPICS_SEARCH, button(Material.PLAYER_HEAD, "Search"));
        inv.setItem(TOPICS_OFF, button(Material.BARRIER, "Take off cosmetic"));
        player.openInventory(inv);
    }

    private long count(String topic) {
        return cosmetics.all().stream().filter(c -> c.category().equals(topic)).count();
    }

    private void openList(Player player, String title, List<Cosmetic> list, int page) {
        int pages = Math.max(1, (list.size() + PER_PAGE - 1) / PER_PAGE);
        Holder holder = new Holder(list, null, page);
        Inventory inv = Bukkit.createInventory(holder, 54,
                Component.text(title + (pages > 1 ? " " + (page + 1) + "/" + pages : ""), NamedTextColor.DARK_PURPLE));
        holder.inventory = inv;
        for (int i = 0; i < PER_PAGE && page * PER_PAGE + i < list.size(); i++) {
            inv.setItem(i, cosmetics.icon(list.get(page * PER_PAGE + i)));
        }
        if (page > 0) {
            inv.setItem(PREV, button(Material.ARROW, "Previous page"));
        }
        inv.setItem(BACK, button(Material.OAK_DOOR, "Back to topics"));
        inv.setItem(SEARCH, button(Material.PLAYER_HEAD, "Search"));
        inv.setItem(OFF, button(Material.BARRIER, "Take off cosmetic"));
        if (page < pages - 1) {
            inv.setItem(NEXT, button(Material.ARROW, "Next page"));
        }
        player.openInventory(inv);
    }

    private static ItemStack button(Material material, String name) {
        ItemStack item = new ItemStack(material);
        item.editMeta(meta -> meta.itemName(Component.text(name, NamedTextColor.YELLOW)));
        return item;
    }

    private String title(Holder holder) {
        Cosmetic first = holder.list.isEmpty() ? null : holder.list.get(0);
        boolean oneTopic = first != null && holder.list.stream().allMatch(c -> c.category().equals(first.category()));
        return oneTopic ? first.category() : "Search";
    }

    @EventHandler
    public void onClick(InventoryClickEvent event) {
        if (!(event.getInventory().getHolder(false) instanceof Holder holder)) {
            return;
        }
        event.setCancelled(true);
        int slot = event.getRawSlot();
        if (!(event.getWhoClicked() instanceof Player player) || slot < 0 || slot >= event.getInventory().getSize()) {
            return;
        }
        if (holder.list == null) {
            for (int i = 0; i < TOPIC_SLOTS.length && i < holder.topics.size(); i++) {
                if (TOPIC_SLOTS[i] == slot) {
                    String topic = holder.topics.get(i);
                    openList(player, topic, cosmetics.all().stream().filter(c -> c.category().equals(topic)).toList(), 0);
                    return;
                }
            }
            if (slot == TOPICS_SEARCH) {
                askSearch(player);
            } else if (slot == TOPICS_OFF) {
                takeOff(player);
            }
            return;
        }
        if (slot == PREV && holder.page > 0) {
            openList(player, title(holder), holder.list, holder.page - 1);
        } else if (slot == NEXT && (holder.page + 1) * PER_PAGE < holder.list.size()) {
            openList(player, title(holder), holder.list, holder.page + 1);
        } else if (slot == BACK) {
            openTopics(player);
        } else if (slot == SEARCH) {
            askSearch(player);
        } else if (slot == OFF) {
            takeOff(player);
        } else if (slot < PER_PAGE && holder.page * PER_PAGE + slot < holder.list.size()) {
            wear(player, holder.list.get(holder.page * PER_PAGE + slot));
        }
    }

    @EventHandler
    public void onDrag(InventoryDragEvent event) {
        if (event.getInventory().getHolder(false) instanceof Holder) {
            event.setCancelled(true);
        }
    }

    private void askSearch(Player player) {
        player.closeInventory();
        searching.add(player.getUniqueId());
        player.sendMessage(Component.text("Type what you want to search for in chat, or 'cancel'.", NamedTextColor.LIGHT_PURPLE));
    }

    @EventHandler(priority = EventPriority.LOWEST)
    public void onChat(AsyncChatEvent event) {
        Player player = event.getPlayer();
        if (!searching.remove(player.getUniqueId())) {
            return;
        }
        event.setCancelled(true);
        String query = PlainTextComponentSerializer.plainText().serialize(event.message()).trim().toLowerCase(Locale.ROOT);
        if (query.equals("cancel")) {
            return;
        }
        Bukkit.getScheduler().runTask(plugin, () -> {
            List<Cosmetic> found = cosmetics.all().stream()
                    .filter(c -> c.id().replace('_', ' ').contains(query) || c.name().toLowerCase(Locale.ROOT).contains(query))
                    .toList();
            if (found.isEmpty()) {
                player.sendMessage(Component.text("Nothing found for '" + query + "'.", NamedTextColor.RED));
                openTopics(player);
            } else {
                openList(player, "Search", found, 0);
            }
        });
    }

    @EventHandler
    public void onQuit(PlayerQuitEvent event) {
        searching.remove(event.getPlayer().getUniqueId());
    }

    public void wear(Player player, Cosmetic c) {
        cosmetics.select(player, c);
        player.getInventory().setHelmet(cosmetics.apply(player.getInventory().getHelmet(), c));
        player.sendMessage(Component.text("Now wearing " + c.name(), NamedTextColor.LIGHT_PURPLE));
    }

    public void takeOff(Player player) {
        cosmetics.select(player, null);
        player.getInventory().setHelmet(cosmetics.restore(player.getInventory().getHelmet()));
        player.closeInventory();
        player.sendMessage(Component.text("Cosmetic taken off.", NamedTextColor.GRAY));
    }
}
