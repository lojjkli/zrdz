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
LIA = ("af_heart", "en-us", 1.0)
REQ = ("am_puck", "en-us", 1.0)
BOOMP = ("am_adam", "en-us", 0.88)
MIKEY = ("am_liam", "en-us", 1.0)
ADE = ("am_eric", "en-us", 1.0)
KIDS = ("af_sky", "en-us", 1.0)
KID = ("af_nicole", "en-us", 1.05)
KLI = ("am_onyx", "en-us", 0.92)
MYN = ("am_echo", "en-us", 1.0)
DONUT = ("am_michael", "en-us", 0.95)
CROWD = ("am_fenrir", "en-us", 1.05)
PIGEON = ("am_onyx", "en-us", 0.8)
CUBE = ("am_adam", "en-us", 0.9)
MACHINE = ("af_bella", "en-us", 0.85)
HAMSTER = ("af_sky", "en-us", 1.1)

# id, (voice, lang, speed), text, fx, caption (if different from the spoken text)
LINES = [
    ("n_prev", NARR, "Previously... REQ won a pigeon, got rich for eleven seconds, and lost it all.", "narr", None),
    ("n_night", NARR, "That night, REQ came back. Alone.", "narr", None),
    ("r_one", REQ, "Okay. Just one more. For real this time.", "vc", None),
    ("v_closer", MACHINE, "Come closer, REQ...", "vc_machine", None),
    ("r_closer", REQ, "...Okay.", "vc", None),
    ("n_pulled", NARR, "And then... the machine pulled him in.", "narr", None),
    ("r_where", REQ, "Bro. Where am I?", "vc", None),
    ("n_inside", NARR, "He was inside the Lucky Spin.", "narr", None),
    ("v_welcome", MACHINE, "Welcome, REQ. You have spun me four thousand times.", "vc_machine", None),
    ("r_alot", REQ, "That's... actually a lot.", "vc", None),
    ("n_curtain", NARR, "But behind the curtain, he found the truth.", "narr", None),
    ("n_hamster", NARR, "The whole machine was powered by... one hamster.", "narr", None),
    ("h_tired", HAMSTER, "I'm so tired, bro.", "vc_squeak", None),
    ("r_you", REQ, "Wait. YOU'RE the Lucky Spin?", "vc_loud", None),
    ("h_every", HAMSTER, "Every spin. Every time. Me.", "vc_squeak", None),
    ("r_break", REQ, "Bro, take a break. I'll run for you.", "vc", None),
    ("n_run", NARR, "So REQ ran. And ran. And ran.", "narr", None),
    ("k_scream", KLI, "Why is the machine screaming?", "vc_deep", None),
    ("p_coo", PIGEON, "Coo.", "vc_pigeon", None),
    ("n_peck", NARR, "The pigeon pecked the machine. Again.", "narr", None),
    ("h_free", HAMSTER, "I'm free! I'm FREE!", "vc_squeak", None),
    ("r_hard", REQ, "Running is so hard. How did you do this?", "vc", None),
    ("h_cardio", HAMSTER, "Cardio, bro.", "vc_squeak", None),
    ("n_quit", NARR, "REQ quit gambling that day. For real this time.", "narr", None),
    ("r_probably", REQ, "...Probably.", "vc", None),
    ("n_end", NARR, "REQ. Part three. The end.", "narr", None),
    ("h_best", HAMSTER, "Best. Day. Ever.", "vc_squeak", None),
]

FX = {
    "vc_machine": "asetrate=24000*0.9,aresample=24000,flanger=delay=2:depth=4:speed=0.5,aecho=0.8:0.7:90|180:0.4|0.3,volume=1.4,alimiter=limit=0.9",
    # 66 kids at once: pitched up, doubled with echo
    "vc_kids": "asetrate=24000*1.35,aresample=24000,atempo=0.8,aecho=0.8:0.7:23|41|67:0.6|0.5|0.4,chorus=0.5:0.9:40|55|70:0.5|0.4|0.3:0.3|0.5|0.7:2|3|4,volume=1.4,alimiter=limit=0.9",
    # one kid
    "vc_kid": "asetrate=24000*1.3,aresample=24000,atempo=0.82,highpass=f=250,lowpass=f=7000,acompressor=threshold=-22dB:ratio=4:attack=3:release=80,volume=1.2",
    "vc_girl": "asetrate=24000*1.1,aresample=24000,atempo=0.96,highpass=f=200,lowpass=f=6500,acompressor=threshold=-22dB:ratio=4:attack=3:release=80,volume=1.2",
    "vc_girl_loud": "asetrate=24000*1.16,aresample=24000,atempo=0.9,highpass=f=220,lowpass=f=6000,acompressor=threshold=-25dB:ratio=8:attack=2:release=60,volume=1.7,alimiter=limit=0.9",
    # the giant pigeon: huge and slow
    "vc_pigeon": "asetrate=24000*0.66,aresample=24000,atempo=1.05,lowpass=f=3800,bass=g=6:f=100,aecho=0.8:0.6:80|160:0.3|0.2,volume=1.6,alimiter=limit=0.9",
    # the default cube: flat robot
    "vc_cube": "asetrate=24000*1.05,aresample=24000,flanger=delay=3:depth=5:speed=2,highpass=f=200,lowpass=f=5000,aecho=0.6:0.5:30:0.4,volume=1.3",
    # the donut: slightly low, wobbly chorus, a bit theatrical
    "vc_donut": "asetrate=24000*0.84,aresample=24000,atempo=1.08,chorus=0.6:0.9:50|60:0.4|0.32:0.25|0.4:2|2.3,highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,aecho=0.8:0.5:40:0.18,volume=1.5",
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
