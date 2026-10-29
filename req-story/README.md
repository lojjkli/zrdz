# REQ – story trailer (Remotion)

A ~1:42 fictional mini-documentary styled like a Roblox mobile screen recording.
3D scenes are three.js (via `@remotion/three`), UI is HTML/CSS, all music and sound
effects are synthesized, voices are Kokoro TTS.

```bash
npm install
# voices (needs kokoro-v1.0.onnx + voices-v1.0.bin from the kokoro-onnx releases)
python3 scripts/gen_voices.py kokoro-v1.0.onnx voices-v1.0.bin
python3 scripts/gen_audio.py          # music + sfx
npx remotion studio                   # preview
npx remotion render src/index.ts REQ out/req_story.mp4
```

Timing for scenes, voice lines, sound effects, chat and diamonds lives in `src/timeline.ts`.
