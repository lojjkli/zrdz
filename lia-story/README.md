# LIA – a Murder Mystery 2 love story (Remotion)

A ~2:20 fictional story video styled like a Roblox mobile screen recording, set in
Murder Mystery 2. Built on the REQ trailer project: 3D scenes are three.js (via
`@remotion/three`), UI is HTML/CSS, all music and sound effects are synthesized,
voices are Kokoro TTS (kli's voice is pitched way down on purpose).

Story: Lia plays MM2 with REQ, Mikey and Ade, meets kli (everyone thinks kli is a girl
until he turns on his mic), kli brings YF who is mean and leaves, Lia is alone and sad,
BoompjeJunior shows up, they fall in love, have 67 kids, REQ farts and the world explodes.

```bash
npm install
# voices (needs kokoro-v1.0.onnx + voices-v1.0.bin from the kokoro-onnx releases)
python3 scripts/gen_voices.py kokoro-v1.0.onnx voices-v1.0.bin
python3 scripts/gen_audio.py          # music + sfx
npx remotion studio                   # preview
npx remotion render src/index.ts LIA out/lia_story.mp4
```

Timing for scenes, voice lines, sound effects and chat lives in `src/timeline.ts`.
Scenes are in `src/scenes/`, the MM2 lobby / mansion / planet are in `src/three/MM2World.tsx`.
