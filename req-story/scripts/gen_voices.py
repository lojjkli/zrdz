"""Generate all voice lines with Kokoro TTS -> public/voice/*.wav + src/voices.json.
Usage: python3 scripts/gen_voices.py /path/kokoro-v1.0.onnx /path/voices-v1.0.bin
"""
import json, os, subprocess, sys, tempfile
import soundfile as sf
from kokoro_onnx import Kokoro

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public", "voice")

NARR = ("bm_george", "en-gb", 0.92)
REQ = ("am_puck", "en-us", 1.0)

# id, (voice, lang, speed), text, fx
LINES = [
    ("n_intro", NARR, "This is Req.", "narr"),
    ("n_problem", NARR, "An ordinary kid... with an extraordinary problem.", "narr"),
    ("n_found", NARR, "One day, he found Pet Simulator ninety nine.", "narr"),
    ("n_had", NARR, "He had pets. He had diamonds. He had... everything.", "narr"),
    ("r_fire", REQ, "Yo, this game is actually fire.", "vc"),
    ("n_machine", NARR, "Then... he found the machine.", "narr"),
    ("r_onespin", REQ, "Okay. Just one spin.", "vc"),
    ("r_onemore1", REQ, "One more.", "vc"),
    ("n_everyday", NARR, "Every single day, he said the exact same thing.", "narr"),
    ("r_onemore2", REQ, "Just one more!", "vc"),
    ("r_onemore3", REQ, "One more! One more!", "vc"),
    ("r_99", REQ, "Bro! Ninety nine percent of gamblers quit right before the big win!", "vc"),
    ("n_gone", NARR, "His diamonds? Gone. His Robux? Gone. But his hope... was stronger than ever.", "narr"),
    ("r_onemore_sad", REQ, "...one more.", "vc_sad"),
    ("n_flying", NARR, "And then... someone came flying in.", "narr"),
    ("r_woah", REQ, "Woah... who is that?", "vc"),
    ("n_wedding", NARR, "Nobody saw it coming. But lowkey... they had a wedding.", "narr"),
    ("r_ido", REQ, "I do!", "vc"),
    ("r_after", REQ, "...after one more spin.", "vc"),
    ("c_letsgo", ("am_liam", "en-us", 1.1), "Let's gooo!", "vc_far"),
    ("c_w", ("af_bella", "en-us", 1.1), "W wedding!", "vc_far"),
    ("n_perfect", NARR, "It was perfect.", "narr"),
    ("n_collapse", NARR, "And then... the Earth collapsed.", "narr"),
    ("r_sky", REQ, "Wait... why is the sky red?", "vc"),
    ("r_run", REQ, "RUN! RUUUN!", "vc_loud"),
    ("r_pets", REQ, "WAIT! MY PETS!", "vc_loud"),
    ("s_aah1", ("am_fenrir", "en-us", 1.0), "Aaaaaah!", "vc_far"),
    ("s_aah2", ("af_sky", "en-us", 1.0), "Aaaaaaah! Help!", "vc_far"),
    ("s_noo", ("am_michael", "en-us", 1.0), "Nooooo!", "vc_far"),
    ("s_run", ("af_nicole", "en-us", 1.1), "Run! Run!", "vc_far"),
    ("s_oof", ("am_echo", "en-us", 1.0), "Oof!", "vc_far"),
    ("n_soon", NARR, "Req. Coming soon.", "narr"),
    ("r_whisper", REQ, "...one more.", "vc_sad"),
]

FX = {
    # narrator: warm documentary, light compression + tiny room
    "narr": "highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,aecho=0.8:0.5:25:0.12",
    # roblox voice chat: pitched up (younger), phone-ish band, compressed
    "vc": "asetrate=24000*1.12,aresample=24000,atempo=0.95,highpass=f=220,lowpass=f=5500,acompressor=threshold=-22dB:ratio=5:attack=3:release=80,volume=1.2",
    "vc_loud": "asetrate=24000*1.15,aresample=24000,atempo=0.94,highpass=f=250,lowpass=f=5000,acompressor=threshold=-25dB:ratio=8:attack=2:release=60,volume=1.6,alimiter=limit=0.9",
    "vc_sad": "asetrate=24000*1.08,aresample=24000,atempo=0.85,highpass=f=220,lowpass=f=5000,volume=1.1",
    "vc_far": "asetrate=24000*1.1,aresample=24000,highpass=f=300,lowpass=f=4500,aecho=0.8:0.6:40:0.25,volume=0.9",
}


def main(model, voices):
    os.makedirs(OUT, exist_ok=True)
    k = Kokoro(model, voices)
    meta = {}
    for lid, (voice, lang, speed), text, fx in LINES:
        s, sr = k.create(text, voice=voice, speed=speed, lang=lang)
        with tempfile.NamedTemporaryFile(suffix=".wav") as t:
            sf.write(t.name, s, sr)
            dst = os.path.join(OUT, f"{lid}.wav")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", t.name,
                            "-af", FX[fx] + ",apad=pad_dur=0.05", "-ar", "48000", "-ac", "1", dst], check=True)
        info = sf.info(dst)
        meta[lid] = {"file": f"voice/{lid}.wav", "sec": round(info.duration, 3), "text": text}
        print(f"{lid:16s} {info.duration:5.2f}s  {text}")
    with open(os.path.join(ROOT, "src", "voices.json"), "w") as f:
        json.dump(meta, f, indent=1)


if __name__ == "__main__":
    main(*sys.argv[1:3])
