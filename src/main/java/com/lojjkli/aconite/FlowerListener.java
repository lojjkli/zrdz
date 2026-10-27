package com.lojjkli.aconite;

import java.util.concurrent.ThreadLocalRandom;
import org.bukkit.GameMode;
import org.bukkit.Location;
import org.bukkit.Material;
import org.bukkit.block.Block;
import org.bukkit.block.data.Ageable;
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.block.BlockBreakEvent;
import org.bukkit.inventory.ItemStack;

public final class FlowerListener implements Listener {

    private final AconitePlugin plugin;

    public FlowerListener(AconitePlugin plugin) {
        this.plugin = plugin;
    }

    @EventHandler(priority = EventPriority.HIGH, ignoreCancelled = true)
    public void onBreak(BlockBreakEvent event) {
        Block block = event.getBlock();
        FileConfiguration config = plugin.getConfig();
        Cosmetics items = plugin.cosmetics();
        Location at = block.getLocation().add(0.5, 0.5, 0.5);
        boolean survival = event.getPlayer().getGameMode() != GameMode.CREATIVE;

        if (block.getType() == Material.PITCHER_CROP && block.getBlockData() instanceof Ageable crop) {
            event.setDropItems(false);
            if (!survival) {
                return;
            }
            if (crop.getAge() < crop.getMaximumAge()) {
                drop(at, items.seeds(), 1);
                return;
            }
            drop(at, items.aconite(), config.getInt("flower.flowers-per-harvest", 1));
            drop(at, items.seeds(), 1 + ThreadLocalRandom.current().nextInt(Math.max(1, config.getInt("flower.max-seeds-per-harvest", 2))));
        } else if (survival && (block.getType() == Material.SHORT_GRASS || block.getType() == Material.TALL_GRASS)
                && ThreadLocalRandom.current().nextDouble() < config.getDouble("flower.seed-chance-from-grass", 0.02)) {
            drop(at, items.seeds(), 1);
        }
    }

    private static void drop(Location at, ItemStack item, int amount) {
        if (amount > 0) {
            item.setAmount(amount);
            at.getWorld().dropItemNaturally(at, item);
        }
    }
}
