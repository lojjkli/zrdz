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
KLI = ("am_onyx", "en-us", 0.92)
YF = ("am_eric", "en-us", 1.08)
BOOMP = ("am_adam", "en-us", 0.88)

# id, (voice, lang, speed), text, fx, caption (if different from the spoken text)
LINES = [
    ("n_intro", NARR, "This is Lia.", "narr", None),
    ("n_loved", NARR, "She loved one thing... more than anything in the world.", "narr", None),
    ("n_mm2", NARR, "Murder Mystery Two.", "narr", "Murder Mystery 2."),
    ("n_friends", NARR, "Every day, she played with her best friends.", "narr", None),
    ("n_req", NARR, "Req.", "narr", "REQ."),
    ("n_mikey", NARR, "Mikey.", "narr", None),
    ("n_ade", NARR, "And Ade.", "narr", None),
    ("l_round", LIA, "Okay guys, one more round. I'm so gonna be murderer this time!", "vc_girl", None),
    ("r_bring", REQ, "Wait, wait. I'm bringing someone.", "vc", None),
    ("n_met", NARR, "And that's the day Lia met... kli.", "narr", None),
    ("l_cute", LIA, "Omg, hiii! Your avatar is so cute! Are you a girl?", "vc_girl", None),
    ("n_thought", NARR, "Everyone thought kli was a girl.", "narr", None),
    ("n_mic", NARR, "Until... he turned on his mic.", "narr", None),
    ("k_wsg", KLI, "What's good.", "vc_deep", "wsg."),
    ("k_girl", KLI, "Nah. I'm not a girl.", "vc_deep", None),
    ("l_what", LIA, "WHAT?!", "vc_girl_loud", None),
    ("n_eboy", NARR, "Kli had the deepest e boy voice... in Roblox history.", "narr", "Kli had the deepest e-boy voice... in Roblox history."),
    ("k_yf", KLI, "Yo. This is my friend, Y F.", "vc_deep", "Yo. This is my friend, YF."),
    ("y_trash", YF, "Bro, you guys are trash at this game.", "vc_loud", None),
    ("y_lia", YF, "And Lia? Nobody even likes you.", "vc_loud", None),
    ("n_mean", NARR, "Y F was... not a nice guy.", "narr", "YF was... not a nice guy."),
    ("y_out", YF, "This game is mid. I'm out.", "vc", None),
    ("n_gone", NARR, "And just like that... everyone was gone.", "narr", None),
    ("l_cry", LIA, "Nobody loves me...", "vc_sad", None),
    ("n_nolove", NARR, "No friends. No love. Nothing.", "narr", None),
    ("n_but", NARR, "But then...", "narr", None),
    ("n_boomp", NARR, "Boompje Junior. Tall. Strong. Dutch.", "narr", "BoompjeJunior. Tall. Strong. Dutch."),
    ("n_lives", NARR, "And he lived... like, twenty minutes away.", "narr", None),
    ("b_hoi", BOOMP, "Hoi, Lia. Why are you crying?", "vc_smooth", None),
    ("l_oh", LIA, "Oh. My. Gosh.", "vc_girl", None),
    ("n_love", NARR, "They fell in love. Instantly.", "narr", None),
    ("l_kids", LIA, "I want kids.", "vc_girl", None),
    ("b_many", BOOMP, "How many?", "vc_smooth", None),
    ("l_67", LIA, "Sixty... seven.", "vc_girl", "Sixty... seven. 🤲"),
    ("c_67", ("am_liam", "en-us", 1.15), "SIX SEVEN!", "vc_far", None),
    ("c_67b", ("af_nicole", "en-us", 1.15), "Six seveeen!", "vc_far", None),
    ("n_67", NARR, "And so... they had sixty seven kids.", "narr", "And so... they had 67 kids."),
    ("n_perfect", NARR, "Everything was perfect.", "narr", None),
    ("r_feel", REQ, "Guys... I don't feel so good.", "vc", None),
    ("k_bro", KLI, "Bro.", "vc_deep", None),
    ("n_fart", NARR, "And then... Req farted.", "narr", "And then... REQ farted."),
    ("n_explode", NARR, "And the world... exploded.", "narr", None),
    ("s_aah1", ("am_fenrir", "en-us", 1.0), "Aaaaaah!", "vc_far", None),
    ("s_aah2", ("af_sky", "en-us", 1.0), "Aaaaaaah! Help!", "vc_far", None),
    ("s_noo", ("am_michael", "en-us", 1.0), "Nooooo!", "vc_far", None),
    ("s_ew", ("af_nicole", "en-us", 1.1), "Ewww! REQ!", "vc_far", None),
    ("r_mybad", REQ, "...my bad.", "vc_sad", None),
    ("n_soon", NARR, "Lia. Coming soon.", "narr", None),
    ("k_post", KLI, "What's good.", "vc_deep", "wsg."),
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
