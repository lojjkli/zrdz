package com.lojjkli.aconite;

import java.util.ListIterator;
import java.util.function.Consumer;
import org.bukkit.Bukkit;
import org.bukkit.entity.Item;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.PlayerDeathEvent;
import org.bukkit.event.inventory.InventoryCloseEvent;
import org.bukkit.event.inventory.PrepareAnvilEvent;
import org.bukkit.event.inventory.PrepareGrindstoneEvent;
import org.bukkit.event.inventory.PrepareSmithingEvent;
import org.bukkit.event.player.PlayerDropItemEvent;
import org.bukkit.event.player.PlayerQuitEvent;
import org.bukkit.inventory.Inventory;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.PlayerInventory;

public final class CosmeticListener implements Listener {

    private final Cosmetics cosmetics;
    private long tick;

    public CosmeticListener(Cosmetics cosmetics) {
        this.cosmetics = cosmetics;
    }

    public void tick() {
        tick++;
        for (Player player : Bukkit.getOnlinePlayers()) {
            if (tick % 2 == 0) {
                update(player);
            }
            animate(player);
        }
    }

    private void update(Player player) {
        PlayerInventory inv = player.getInventory();
        ItemStack head = inv.getHelmet();
        Cosmetic selected = cosmetics.selected(player);
        if (selected != null && !selected.equals(cosmetics.of(head))) {
            inv.setHelmet(cosmetics.apply(head, selected));
        } else if (selected == null && cosmetics.isCosmetic(head)) {
            inv.setHelmet(cosmetics.restore(head));
        }

        restoreAll(inv.getStorageContents(), inv::setStorageContents);
        restoreAll(inv.getExtraContents(), inv::setExtraContents);
        ItemStack cursor = player.getItemOnCursor();
        if (cosmetics.isCosmetic(cursor)) {
            player.setItemOnCursor(cosmetics.restore(cursor));
        }
        Inventory top = player.getOpenInventory().getTopInventory();
        if (top != inv) {
            restoreAll(top);
        }
    }

    private void restoreAll(ItemStack[] items, Consumer<ItemStack[]> setter) {
        boolean changed = false;
        for (int i = 0; i < items.length; i++) {
            if (cosmetics.isCosmetic(items[i])) {
                items[i] = cosmetics.restore(items[i]);
                changed = true;
            }
        }
        if (changed) {
            setter.accept(items);
        }
    }

    private void restoreAll(Inventory inventory) {
        ListIterator<ItemStack> it = inventory.iterator();
        while (it.hasNext()) {
            ItemStack item = it.next();
            if (cosmetics.isCosmetic(item)) {
                it.set(cosmetics.restore(item));
            }
        }
    }

    private void animate(Player player) {
        if (!cosmetics.anyAnimated()) {
            return;
        }
        ItemStack head = player.getInventory().getHelmet();
        Cosmetic c = cosmetics.of(head);
        if (c == null || !c.animated() || tick % c.frameTicks() != 0) {
            return;
        }
        int frame = (int) ((tick / c.frameTicks()) % c.frames().size());
        head.editMeta(meta -> meta.setItemModel(c.frames().get(frame)));
        player.getInventory().setHelmet(head);
    }

    @EventHandler
    public void onDrop(PlayerDropItemEvent event) {
        Item drop = event.getItemDrop();
        if (cosmetics.isCosmetic(drop.getItemStack())) {
            ItemStack normal = cosmetics.restore(drop.getItemStack());
            if (normal == null) {
                drop.remove();
            } else {
                drop.setItemStack(normal);
            }
        }
    }

    @EventHandler
    public void onDeath(PlayerDeathEvent event) {
        ListIterator<ItemStack> it = event.getDrops().listIterator();
        while (it.hasNext()) {
            ItemStack item = it.next();
            if (cosmetics.isCosmetic(item)) {
                ItemStack normal = cosmetics.restore(item);
                if (normal == null) {
                    it.remove();
                } else {
                    it.set(normal);
                }
            }
        }
    }

    @EventHandler
    public void onClose(InventoryCloseEvent event) {
        if (event.getInventory() != event.getPlayer().getInventory()) {
            restoreAll(event.getInventory());
        }
    }

    @EventHandler
    public void onQuit(PlayerQuitEvent event) {
        PlayerInventory inv = event.getPlayer().getInventory();
        inv.setHelmet(cosmetics.restore(inv.getHelmet()));
    }

    public void restoreOnline() {
        for (Player player : Bukkit.getOnlinePlayers()) {
            PlayerInventory inv = player.getInventory();
            inv.setHelmet(cosmetics.restore(inv.getHelmet()));
        }
    }

    @EventHandler
    public void onAnvil(PrepareAnvilEvent event) {
        if (hasCosmetic(event.getInventory())) {
            event.setResult(null);
        }
    }

    @EventHandler
    public void onSmithing(PrepareSmithingEvent event) {
        if (hasCosmetic(event.getInventory())) {
            event.setResult(null);
        }
    }

    @EventHandler
    public void onGrindstone(PrepareGrindstoneEvent event) {
        if (hasCosmetic(event.getInventory())) {
            event.setResult(null);
        }
    }

    private boolean hasCosmetic(Inventory inventory) {
        for (ItemStack item : inventory.getContents()) {
            if (cosmetics.isCosmetic(item)) {
                return true;
            }
        }
        return false;
    }
}
