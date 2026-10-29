# KLI – from squeak to legend (Remotion)

A ~3:00 fictional story video styled like a Roblox mobile screen recording. Built on the
LIA project: 3D scenes are three.js (via `@remotion/three`), UI is HTML/CSS, music and
sound effects are synthesized, voices are Kokoro TTS (squeaky kli is pitched up, deep kli
pitched way down).

Story: kli has a squeaky voice, everyone hates him, he's broke and lives in a box (a pigeon
steals his bread). His friend myninn tells him about Roblox Studio, he's terrible at it,
then he meets a 3D app, falls in love with it, gets struck by lightning and gets the
deepest voice ever. He makes a donut, gets rich, says "nah" to the haters... and the
donut's physics were never turned off.

```bash
npm install
python3 scripts/gen_voices.py kokoro-v1.0.onnx voices-v1.0.bin
python3 scripts/gen_audio.py          # music + sfx
npx remotion studio                   # preview
# fast 720p render
npx remotion render src/index.ts KLI out/kli_720p.mp4 --scale=0.6666666666666666 --crf=24
```

Timing for scenes, voice lines, sound effects and chat lives in `src/timeline.ts`.
Scenes are in `src/scenes/` (Early, Mid, Late), props in `src/three/KliProps.tsx`,
Studio / 3D-app / game page UI in `src/ui/KliUI.tsx`.
