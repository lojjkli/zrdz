"""Generate all voice lines with Kokoro TTS -> public/voice/*.wav + src/voices.json.
Usage: python3 scripts/gen_voices.py /path/kokoro-v1.0.onnx /path/voices-v1.0.bin
"""
import json, os, subprocess, sys, tempfile
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public", "voice")

NARR = ("bm_george", "en-gb", 0.92)
KLI = ("am_puck", "en-us", 1.0)
DEEP = ("am_onyx", "en-us", 0.92)
MYN = ("am_echo", "en-us", 1.0)

# id, (voice, lang, speed), text, fx, caption (if different from the spoken text)
LINES = [
    ("n_intro", NARR, "This is kli.", "narr", None),
    ("n_problem", NARR, "Before he was a legend... he had a problem.", "narr", None),
    ("k_hi", KLI, "Hiii guys! Wanna be friends?", "vc_squeak", None),
    ("n_squeak", NARR, "His voice was... very high.", "narr", None),
    ("k_please", KLI, "Guys, wait! Please don't leave!", "vc_squeak", None),
    ("c_ew", ("af_nicole", "en-us", 1.1), "Ew, it's the squeaky kid!", "vc_far", None),
    ("n_hated", NARR, "Everyone hated him.", "narr", None),
    ("n_poor", NARR, "He was poor. So poor... he couldn't even afford a face.", "narr", None),
    ("n_sell", NARR, "He even tried to sell his hair.", "narr", None),
    ("k_hair", KLI, "Hair for sale! Only one Robux!", "vc_squeak", None),
    ("k_bread", KLI, "At least I still have my bread.", "vc_squeak", None),
    ("n_pigeon", NARR, "Then a pigeon stole his bread.", "narr", None),
    ("k_why", KLI, "WHY?!", "vc_squeak", None),
    ("n_lowest", NARR, "It was the lowest point of his life.", "narr", None),
    ("n_then", NARR, "But then, his friend myninn showed up.", "narr", None),
    ("m_box", MYN, "Bro. Why are you living in a box?", "vc", None),
    ("k_poor", KLI, "Because I'm poor.", "vc_squeak", None),
    ("m_studio", MYN, "Have you ever heard of... Roblox Studio?", "vc", None),
    ("k_whats", KLI, "What's that?", "vc_squeak", None),
    ("m_make", MYN, "You make games. You make money. You get rich.", "vc", None),
    ("k_lets", KLI, "Let's gooo!", "vc_squeak", None),
    ("n_started", NARR, "So he started developing.", "narr", None),
    ("n_bad", NARR, "He was... really bad.", "narr", None),
    ("k_oops", KLI, "Oops.", "vc_squeak", None),
    ("n_dislike", NARR, "His first game got one player. And one dislike.", "narr", None),
    ("s_oof", ("am_echo", "en-us", 1.0), "Oof!", "vc_far", None),
    ("n_baseplate", NARR, "Even the baseplate left.", "narr", None),
    ("k_giveup", KLI, "I give up.", "vc_squeak_sad", None),
    ("n_met", NARR, "And then... he met Blender.", "narr", None),
    ("k_cube", KLI, "Bye bye, cube.", "vc_squeak", None),
    ("n_love", NARR, "It was love at first sight.", "narr", None),
    ("n_changed", NARR, "And at that very moment... his voice... changed.", "narr", None),
    ("k_wsg", DEEP, "What's good.", "vc_deep", "wsg."),
    ("n_deepest", NARR, "It was the deepest voice the world had ever heard.", "narr", None),
    ("n_glaze", NARR, "Smart. Strong. The coolest dev alive.", "narr", None),
    ("n_donut", NARR, "He made a donut.", "narr", None),
    ("n_models", NARR, "Then he made models for every game on Roblox.", "narr", None),
    ("k_rich", DEEP, "I'm kind of rich now.", "vc_deep", None),
    ("c_please", ("af_bella", "en-us", 1.1), "Kli, please be our friend!", "vc_far", None),
    ("k_nah", DEEP, "Nah.", "vc_deep", None),
    ("n_richest", NARR, "Kli became the richest developer in Roblox history.", "narr", None),
    ("m_welcome", MYN, "You're welcome, by the way.", "vc", None),
    ("k_thanks", DEEP, "Thanks, myninn.", "vc_deep", None),
    ("n_forgot", NARR, "But he forgot one thing.", "narr", None),
    ("n_physics", NARR, "He never turned off the donut's physics.", "narr", None),
    ("k_bro", DEEP, "Bro.", "vc_deep", None),
    ("s_aah1", ("am_fenrir", "en-us", 1.0), "Aaaaaah!", "vc_far", None),
    ("s_aah2", ("af_sky", "en-us", 1.0), "Aaaaaaah! The donut!", "vc_far", None),
    ("n_soon", NARR, "Kli. Coming soon.", "narr", None),
    ("k_post", KLI, "...hi.", "vc_squeak", None),
    ("k_jk", DEEP, "Just kidding.", "vc_deep", None),
]

FX = {
    # narrator: warm documentary, light compression + tiny room
    "narr": "highpass=f=70,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,aecho=0.8:0.5:25:0.12",
    # roblox voice chat: phone-ish band, compressed
    "vc": "asetrate=24000*1.12,aresample=24000,atempo=0.95,highpass=f=220,lowpass=f=5500,acompressor=threshold=-22dB:ratio=5:attack=3:release=80,volume=1.2",
    "vc_loud": "asetrate=24000*1.06,aresample=24000,atempo=0.97,highpass=f=250,lowpass=f=5000,acompressor=threshold=-25dB:ratio=8:attack=2:release=60,volume=1.6,alimiter=limit=0.9",
    "vc_sad": "asetrate=24000*1.08,aresample=24000,atempo=0.85,highpass=f=220,lowpass=f=5000,volume=1.1",
    "vc_far": "asetrate=24000*1.1,aresample=24000,highpass=f=300,lowpass=f=4500,aecho=0.8:0.6:40:0.25,volume=0.9",
    # Lia: a bit younger/brighter
    "vc_girl": "asetrate=24000*1.1,aresample=24000,atempo=0.96,highpass=f=200,lowpass=f=6500,acompressor=threshold=-22dB:ratio=4:attack=3:release=80,volume=1.2",
    "vc_girl_loud": "asetrate=24000*1.16,aresample=24000,atempo=0.9,highpass=f=220,lowpass=f=6000,acompressor=threshold=-25dB:ratio=8:attack=2:release=60,volume=1.7,alimiter=limit=0.9",
    # kli: absurdly deep e-boy voice (pitched way down, slowed, bass boosted)
    "vc_deep": "asetrate=24000*0.70,aresample=24000,atempo=1.12,lowpass=f=4200,bass=g=8:f=90,acompressor=threshold=-20dB:ratio=4:attack=5:release=150,aecho=0.8:0.4:30:0.15,volume=1.5,alimiter=limit=0.9",
    # young kli: chipmunk squeak
    "vc_squeak": "asetrate=24000*1.6,aresample=24000,atempo=0.72,highpass=f=300,lowpass=f=7500,acompressor=threshold=-22dB:ratio=4:attack=3:release=80,volume=1.2",
    "vc_squeak_sad": "asetrate=24000*1.5,aresample=24000,atempo=0.62,highpass=f=300,lowpass=f=7000,volume=1.1",
    # BoompjeJunior: smooth, slightly lower, a little reverb
    "vc_smooth": "asetrate=24000*0.93,aresample=24000,atempo=1.0,highpass=f=90,lowpass=f=7000,bass=g=3:f=120,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,aecho=0.8:0.5:60:0.2,volume=1.3",
}


def level(path, target_db):
    """Scale so the voiced part sits at target_db RMS (dBFS), keep peaks under -1 dBFS."""
    x, sr = sf.read(path)
    n = int(sr * 0.05)
    frames = x[: len(x) // n * n].reshape(-1, n)
    rms = np.sqrt((frames ** 2).mean(axis=1))
    voiced = rms[rms > rms.max() * 0.1]
    cur = 20 * np.log10(np.sqrt((voiced ** 2).mean()) + 1e-9)
    g = 10 ** ((target_db - cur) / 20)
    g = min(g, 0.89 / (np.abs(x).max() + 1e-9))
    sf.write(path, x * g, sr)


def main(model, voices):
    os.makedirs(OUT, exist_ok=True)
    k = Kokoro(model, voices)
    meta = {}
    for lid, (voice, lang, speed), text, fx, cap in LINES:
        s, sr = k.create(text, voice=voice, speed=speed, lang=lang)
        with tempfile.NamedTemporaryFile(suffix=".wav") as t:
            sf.write(t.name, s, sr)
            dst = os.path.join(OUT, f"{lid}.wav")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", t.name,
                            "-af", FX[fx] + ",apad=pad_dur=0.05", "-ar", "48000", "-ac", "1", dst], check=True)
        level(dst, -15.0 if fx == "vc_deep" else -21.0 if fx == "vc_far" else -17.0)
        info = sf.info(dst)
        meta[lid] = {"file": f"voice/{lid}.wav", "sec": round(info.duration, 3), "text": cap or text}
        print(f"{lid:12s} {info.duration:5.2f}s  {cap or text}")
    with open(os.path.join(ROOT, "src", "voices.json"), "w") as f:
        json.dump(meta, f, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main(*sys.argv[1:3])
