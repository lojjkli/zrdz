package com.lojjkli.aconite;

import java.util.List;
import org.bukkit.NamespacedKey;

/** One cosmetic. More than one frame means it is animated. */
public record Cosmetic(String id, String name, String category, List<NamespacedKey> frames, int frameTicks) {

    public NamespacedKey model() {
        return frames.get(0);
    }

    public boolean animated() {
        return frames.size() > 1;
    }
}
