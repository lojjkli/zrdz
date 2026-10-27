package com.lojjkli.aconite;

import com.sun.net.httpserver.HttpServer;
import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.URI;
import java.nio.file.Files;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.HexFormat;
import java.util.List;
import java.util.UUID;
import net.kyori.adventure.resource.ResourcePackInfo;
import net.kyori.adventure.resource.ResourcePackRequest;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.format.NamedTextColor;
import org.bukkit.Bukkit;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.inventory.ItemStack;
import org.bukkit.plugin.java.JavaPlugin;

public final class AconitePlugin extends JavaPlugin implements Listener {

    private static final String PACK = "aconite_server_pack.zip";
    private static final UUID PACK_ID = UUID.nameUUIDFromBytes("aconite".getBytes());

    private Cosmetics cosmetics;
    private CosmeticMenu menu;
    private CosmeticListener cosmeticListener;
    private HttpServer packServer;
    private ResourcePackRequest packRequest;

    @Override
    public void onEnable() {
        saveDefaultConfig();
        if (!packFile().exists()) {
            saveResource(PACK, false);
        }
        cosmetics = new Cosmetics(this);
        cosmetics.load();
        menu = new CosmeticMenu(this);
        cosmeticListener = new CosmeticListener(cosmetics);

        getServer().getPluginManager().registerEvents(this, this);
        getServer().getPluginManager().registerEvents(menu, this);
        getServer().getPluginManager().registerEvents(cosmeticListener, this);
        getServer().getPluginManager().registerEvents(new FlowerListener(this), this);
        getServer().getScheduler().runTaskTimer(this, cosmeticListener::tick, 1, 1);
        setupPack();
    }

    @Override
    public void onDisable() {
        if (cosmeticListener != null) {
            cosmeticListener.restoreOnline();
        }
        stopPackServer();
    }

    public Cosmetics cosmetics() {
        return cosmetics;
    }

    public File packFile() {
        return new File(getDataFolder(), PACK);
    }

    private void setupPack() {
        stopPackServer();
        packRequest = null;
        if (!getConfig().getBoolean("resource-pack.enabled", true)) {
            return;
        }
        try {
            byte[] bytes = Files.readAllBytes(packFile().toPath());
            String hash = HexFormat.of().formatHex(MessageDigest.getInstance("SHA-1").digest(bytes));
            String url = getConfig().getString("resource-pack.url", "");
            if (url.isBlank()) {
                url = startPackServer(bytes, hash);
            }
            packRequest = ResourcePackRequest.resourcePackRequest()
                    .packs(ResourcePackInfo.resourcePackInfo(PACK_ID, URI.create(url), hash))
                    .required(getConfig().getBoolean("resource-pack.required", false))
                    .prompt(Component.text(getConfig().getString("resource-pack.prompt", "Aconite"), NamedTextColor.LIGHT_PURPLE))
                    .replace(false)
                    .build();
            getLogger().info("Resource pack: " + url);
        } catch (Exception e) {
            getLogger().warning("Resource pack not set up: " + e.getMessage());
        }
    }

    private String startPackServer(byte[] bytes, String hash) throws IOException {
        int port = getConfig().getInt("resource-pack.host-port", 8164);
        packServer = HttpServer.create(new InetSocketAddress(port), 0);
        packServer.createContext("/", exchange -> {
            exchange.getResponseHeaders().add("Content-Type", "application/zip");
            exchange.sendResponseHeaders(200, bytes.length);
            try (OutputStream out = exchange.getResponseBody()) {
                out.write(bytes);
            }
        });
        packServer.start();
        String address = getConfig().getString("resource-pack.public-address", "");
        if (address.isBlank()) {
            address = Bukkit.getIp().isBlank() ? "localhost" : Bukkit.getIp();
            if (address.equals("localhost")) {
                getLogger().warning("Set resource-pack.public-address in config.yml so other players can download the pack.");
            }
        }
        return "http://" + address + ":" + port + "/" + hash + ".zip";
    }

    private void stopPackServer() {
        if (packServer != null) {
            packServer.stop(0);
            packServer = null;
        }
    }

    @EventHandler
    public void onJoin(PlayerJoinEvent event) {
        if (packRequest != null) {
            event.getPlayer().sendResourcePacks(packRequest);
        }
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command, String label, String[] args) {
        if (command.getName().equals("cosmetics")) {
            if (sender instanceof Player player) {
                menu.openTopics(player);
            } else {
                sender.sendMessage("Only players can use this.");
            }
            return true;
        }

        if (args.length >= 1 && args[0].equalsIgnoreCase("reload")) {
            reloadConfig();
            cosmetics.load();
            setupPack();
            for (Player player : Bukkit.getOnlinePlayers()) {
                if (packRequest != null) {
                    player.sendResourcePacks(packRequest);
                }
            }
            sender.sendMessage(Component.text("Reloaded. " + cosmetics.all().size() + " cosmetics.", NamedTextColor.GREEN));
            return true;
        }
        if (args.length >= 3 && args[0].equalsIgnoreCase("give")) {
            Player target = Bukkit.getPlayerExact(args[1]);
            ItemStack item = cosmetics.flowerByName(args[2].toLowerCase());
            if (target == null || item == null) {
                sender.sendMessage(Component.text("Unknown player or item.", NamedTextColor.RED));
                return true;
            }
            int amount = 1;
            if (args.length >= 4) {
                try {
                    amount = Math.max(1, Math.min(64, Integer.parseInt(args[3])));
                } catch (NumberFormatException ignored) {
                }
            }
            item.setAmount(amount);
            target.getInventory().addItem(item).values()
                    .forEach(left -> target.getWorld().dropItemNaturally(target.getLocation(), left));
            sender.sendMessage(Component.text("Gave " + args[2] + " to " + target.getName(), NamedTextColor.GREEN));
            return true;
        }
        sender.sendMessage(Component.text("/aconite give <player> <item> [amount]  |  /aconite reload", NamedTextColor.YELLOW));
        return true;
    }

    @Override
    public List<String> onTabComplete(CommandSender sender, Command command, String alias, String[] args) {
        List<String> options = new ArrayList<>();
        if (command.getName().equals("cosmetics")) {
            return options;
        }
        if (args.length == 1) {
            options.addAll(List.of("give", "reload"));
        } else if (args.length == 2 && args[0].equalsIgnoreCase("give")) {
            Bukkit.getOnlinePlayers().forEach(p -> options.add(p.getName()));
        } else if (args.length == 3 && args[0].equalsIgnoreCase("give")) {
            options.addAll(List.of("aconite", "wolfsbane", "aconite_seeds"));
        }
        String last = args.length == 0 ? "" : args[args.length - 1].toLowerCase();
        return options.stream().filter(o -> o.toLowerCase().startsWith(last)).toList();
    }
}
