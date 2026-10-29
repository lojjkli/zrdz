"""Synthesize all music + sound effects (no samples, everything generated).
Usage: python3 scripts/gen_audio.py   -> public/music/*.wav, public/sfx/*.wav
"""
import os
import numpy as np
import soundfile as sf
from scipy import signal

SR = 48000
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rng = np.random.default_rng(7)


# ---------------------------------------------------------------- helpers
def t_(dur):
    return np.arange(int(dur * SR)) / SR


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def note(name):
    names = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
    n = names[name[0]]
    i = 1
    if len(name) > 2 or (len(name) == 2 and name[1] in "#b"):
        n += 1 if name[1] == "#" else -1
        i = 2
    return 12 * (int(name[i:]) + 1) + n


def env(n, a=0.005, d=0.1, s=0.0, r=0.05, hold=None):
    """ADSR envelope of n samples."""
    a_n, d_n, r_n = int(a * SR), int(d * SR), int(r * SR)
    out = np.zeros(n)
    a_n = min(a_n, n)
    out[:a_n] = np.linspace(0, 1, a_n, endpoint=False)
    k = a_n
    dn = min(d_n, n - k)
    out[k:k + dn] = np.linspace(1, s, dn, endpoint=False)
    k += dn
    if hold is None:
        hold = n - k - r_n
    hn = max(0, min(int(hold * SR), n - k - r_n)) if hold != n else 0
    out[k:k + hn] = s
    k += hn
    rn = n - k
    if rn > 0:
        out[k:] = np.linspace(out[k - 1] if k > 0 else s, 0, rn)
    return out


def expdecay(n, tau):
    return np.exp(-np.arange(n) / (tau * SR))


def lp(x, f, order=2):
    b, a = signal.butter(order, min(f / (SR / 2), 0.99), "low")
    return signal.lfilter(b, a, x, axis=0)


def hp(x, f, order=2):
    b, a = signal.butter(order, min(f / (SR / 2), 0.99), "high")
    return signal.lfilter(b, a, x, axis=0)


def bp(x, lo, hi, order=2):
    b, a = signal.butter(order, [lo / (SR / 2), min(hi / (SR / 2), 0.99)], "band")
    return signal.lfilter(b, a, x, axis=0)


def saw(f, t, harmonics=24):
    out = np.zeros_like(t)
    for k in range(1, harmonics + 1):
        if f * k > SR / 2.2:
            break
        out += ((-1) ** (k + 1)) * np.sin(2 * np.pi * f * k * t) / k
    return out * 0.6


def square(f, t, harmonics=15):
    out = np.zeros_like(t)
    for k in range(1, harmonics * 2, 2):
        if f * k > SR / 2.2:
            break
        out += np.sin(2 * np.pi * f * k * t) / k
    return out * 0.8


def noise(n):
    return rng.standard_normal(n)


def stereo(x, pan=0.0):
    """pan -1..1, equal power."""
    l = np.cos((pan + 1) * np.pi / 4)
    r = np.sin((pan + 1) * np.pi / 4)
    return np.stack([x * l, x * r], axis=1)


def place(buf, x, start_sec, gain=1.0, pan=0.0):
    if x.ndim == 1:
        x = stereo(x, pan)
    s = int(start_sec * SR)
    if s >= len(buf):
        return
    e = min(len(buf), s + len(x))
    buf[s:e] += x[: e - s] * gain


_IR = {}


def reverb(x, seconds=1.8, wet=0.25, bright=6000):
    key = (seconds, bright)
    if key not in _IR:
        n = int(seconds * SR)
        ir = np.stack([noise(n), noise(n)], 1) * expdecay(n, seconds / 6.0)[:, None]
        ir = lp(ir, bright)
        ir[: int(0.012 * SR)] *= np.linspace(0, 1, int(0.012 * SR))[:, None]
        ir /= np.sqrt((ir ** 2).sum(0))
        _IR[key] = ir
    ir = _IR[key]
    if x.ndim == 1:
        x = stereo(x)
    wetsig = np.stack([signal.fftconvolve(x[:, c], ir[:, c])[: len(x)] for c in range(2)], 1)
    return x * (1 - wet) + wetsig * wet * 1.6


def norm(x, peak=0.89):
    m = np.abs(x).max()
    return x * (peak / m) if m > 0 else x


def soft_limit(x, drive=1.0):
    return np.tanh(x * drive) / np.tanh(drive)


def write(path, x, peak=0.89):
    x = norm(x, peak)
    if x.ndim == 1:
        x = stereo(x)
    # tiny fades to avoid clicks
    f = min(len(x) // 4, int(0.004 * SR))
    x[:f] *= np.linspace(0, 1, f)[:, None]
    x[-f:] *= np.linspace(1, 0, f)[:, None]
    full = os.path.join(ROOT, "public", path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    sf.write(full, x.astype(np.float32), SR, subtype="PCM_16")
    print(f"{path:28s} {len(x) / SR:6.2f}s")


# ---------------------------------------------------------------- instruments
def marimba(f, dur=0.6):
    t = t_(dur)
    x = np.sin(2 * np.pi * f * t) * expdecay(len(t), 0.35)
    x += 0.35 * np.sin(2 * np.pi * f * 3.93 * t) * expdecay(len(t), 0.06)
    x += 0.12 * np.sin(2 * np.pi * f * 9.2 * t) * expdecay(len(t), 0.02)
    x *= env(len(t), a=0.002, d=0.0, s=1.0, r=0.03)
    return x


def musicbox(f, dur=1.6):
    t = t_(dur)
    x = np.sin(2 * np.pi * f * t) * expdecay(len(t), 0.7)
    x += 0.4 * np.sin(2 * np.pi * f * 2.0 * t) * expdecay(len(t), 0.35)
    x += 0.25 * np.sin(2 * np.pi * f * 5.43 * t) * expdecay(len(t), 0.08)
    x += 0.12 * np.sin(2 * np.pi * f * 8.1 * t) * expdecay(len(t), 0.03)
    return x * env(len(t), a=0.001, d=0, s=1, r=0.05)


def bell(f, dur=4.0):
    """church bell: inharmonic partials (hum, prime, tierce, quint, nominal)."""
    t = t_(dur)
    parts = [(0.5, 0.8, 2.5), (1.0, 1.0, 1.8), (1.19, 0.6, 1.2), (1.5, 0.4, 1.0), (2.0, 0.7, 0.9),
             (2.5, 0.3, 0.5), (3.0, 0.25, 0.4), (4.07, 0.15, 0.25)]
    x = np.zeros_like(t)
    for ratio, amp, tau in parts:
        x += amp * np.sin(2 * np.pi * f * ratio * t + rng.random() * 6) * expdecay(len(t), tau)
    strike = noise(len(t)) * expdecay(len(t), 0.004) * 0.3
    return x + bp(strike, 1000, 6000)


def piano(f, dur=2.0, vel=1.0):
    t = t_(dur)
    x = np.zeros_like(t)
    B = 0.0004
    for k in range(1, 12):
        fk = f * k * np.sqrt(1 + B * k * k)
        if fk > SR / 2.2:
            break
        x += (1 / k ** 1.3) * np.sin(2 * np.pi * fk * t) * expdecay(len(t), 1.2 / (1 + 0.4 * k))
    x *= env(len(t), a=0.003, d=0, s=1, r=0.15)
    hammer = bp(noise(len(t)) * expdecay(len(t), 0.003), 2000, 8000) * 0.1
    return (x + hammer) * vel


def pluck(f, dur=0.5, bright=0.5):
    """Karplus-Strong (vectorised by period)."""
    n = int(dur * SR)
    p = max(2, int(SR / f))
    buf = noise(p) * 0.8
    buf = lp(buf, 1500 + 6000 * bright)
    out = np.zeros(n)
    k = 0
    while k < n:
        m = min(p, n - k)
        out[k:k + m] = buf[:m]
        nb = 0.5 * (buf + np.roll(buf, -1)) * 0.996
        buf = nb
        k += p
    return out * env(n, a=0.001, d=0, s=1, r=0.02)


def pad(freqs, dur, cutoff=1800, detune=0.006, a=0.6, r=0.8):
    t = t_(dur)
    x = np.zeros_like(t)
    for f in freqs:
        for d in (-detune, 0, detune):
            x += saw(f * (1 + d), t + rng.random(), 30)
    x = lp(x, cutoff, 2)
    return x * env(len(t), a=a, d=0, s=1, r=r) / (len(freqs) * 2)


def bass(f, dur=0.4):
    t = t_(dur)
    x = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t) + 0.15 * saw(f, t, 8)
    return lp(x, 900) * env(len(t), a=0.004, d=0.08, s=0.7, r=0.06)


def kick(dur=0.35, f0=130, f1=45):
    t = t_(dur)
    f = f1 + (f0 - f1) * np.exp(-t / 0.03)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * expdecay(len(t), 0.12)
    click = hp(noise(len(t)) * expdecay(len(t), 0.002), 2000) * 0.25
    return x + click


def snare(dur=0.25):
    t = t_(dur)
    tone = np.sin(2 * np.pi * 185 * t) * expdecay(len(t), 0.04)
    nz = bp(noise(len(t)), 1200, 9000) * expdecay(len(t), 0.07)
    return 0.6 * tone + 0.8 * nz


def clap(dur=0.3):
    n = int(dur * SR)
    x = np.zeros(n)
    for off in (0, 0.011, 0.022, 0.03):
        s = int(off * SR)
        seg = noise(n - s) * expdecay(n - s, 0.012 if off < 0.03 else 0.09)
        x[s:] += seg
    return bp(x, 900, 5000)


def hat(dur=0.06, open_=False):
    t = t_(0.35 if open_ else dur)
    return hp(noise(len(t)), 7000) * expdecay(len(t), 0.12 if open_ else 0.018) * 0.5


def taiko(dur=0.9, f0=110, f1=60):
    t = t_(dur)
    f = f1 + (f0 - f1) * np.exp(-t / 0.05)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * expdecay(len(t), 0.25)
    x += lp(noise(len(t)), 600) * expdecay(len(t), 0.05) * 0.6
    return x


# ---------------------------------------------------------------- music
def chord_tones(root, kind="maj"):
    iv = {"maj": [0, 4, 7], "min": [0, 3, 7], "7": [0, 4, 7, 10], "m7": [0, 3, 7, 10]}[kind]
    return [root + i for i in iv]


def song_lobby():
    """Cheerful marimba lobby tune, C - G - Am - F, 118 bpm, 16 bars."""
    bpm = 118
    beat = 60 / bpm
    bars = 16
    dur = bars * 4 * beat + 2
    buf = np.zeros((int(dur * SR), 2))
    prog = [(note("C4"), "maj"), (note("G3"), "maj"), (note("A3"), "min"), (note("F3"), "maj")]
    melody = [  # (beat offset in 4-bar phrase, midi, length beats)
        (0, 76, 1), (1, 79, 1), (2, 81, 0.5), (2.5, 79, 1.5), (4, 74, 1), (5, 76, 1), (6, 79, 2),
        (8, 76, 1), (9, 72, 1), (10, 74, 0.5), (10.5, 76, 1.5), (12, 77, 1), (13, 76, 0.5), (13.5, 74, 0.5), (14, 72, 2)]
    for bar in range(bars):
        root, kind = prog[bar % 4]
        tones = chord_tones(root, kind)
        t0 = bar * 4 * beat
        arp = [tones[0], tones[1], tones[2], tones[1] + 12, tones[2], tones[1], tones[0] + 12, tones[2]]
        for i, m in enumerate(arp):
            place(buf, marimba(midi(m)), t0 + i * beat / 2, 0.32, pan=-0.3 + 0.6 * (i % 2))
        for b in range(4):
            place(buf, bass(midi(root - 12), beat * 0.9), t0 + b * beat, 0.45 if b in (0, 2) else 0.3)
        if bar >= 2:
            place(buf, kick(), t0, 0.7)
            place(buf, kick(), t0 + 2 * beat, 0.6)
            place(buf, kick(), t0 + 2.5 * beat, 0.35)
            place(buf, clap(), t0 + beat, 0.35, 0.1)
            place(buf, clap(), t0 + 3 * beat, 0.35, 0.1)
            for h in range(8):
                place(buf, hat(), t0 + h * beat / 2, 0.22 if h % 2 else 0.12, 0.35)
        if bar >= 4 and bar % 4 == 0:
            for off, m, ln in melody:
                place(buf, musicbox(midi(m), 1.2), t0 + off * beat, 0.28, 0.15)
    return reverb(buf, 1.4, 0.18)


def song_casino():
    """Tense minor groove for the gambling machine, 124 bpm."""
    bpm = 124
    beat = 60 / bpm
    bars = 14
    dur = bars * 4 * beat + 2
    buf = np.zeros((int(dur * SR), 2))
    prog = [(note("A3"), "min"), (note("F3"), "maj"), (note("D3"), "min"), (note("E3"), "maj")]
    for bar in range(bars):
        root, kind = prog[bar % 4]
        tones = chord_tones(root, kind)
        t0 = bar * 4 * beat
        for i in range(16):
            m = tones[[0, 2, 1, 2][i % 4]] + (12 if i % 8 >= 4 else 0)
            place(buf, pluck(midi(m), 0.3, 0.6), t0 + i * beat / 4, 0.28, pan=-0.4 if i % 2 else 0.4)
        for b in range(8):
            if b % 2 == 0 or b in (3, 7):
                place(buf, bass(midi(root - 12), beat * 0.45), t0 + b * beat / 2, 0.5)
        place(buf, kick(), t0, 0.75)
        place(buf, kick(), t0 + 1.5 * beat, 0.5)
        place(buf, kick(), t0 + 2 * beat, 0.7)
        place(buf, snare(), t0 + beat, 0.38)
        place(buf, snare(), t0 + 3 * beat, 0.38)
        for h in range(16):
            place(buf, hat(), t0 + h * beat / 4, 0.16 if h % 4 == 2 else 0.08, -0.3)
        if bar % 2 == 0:
            place(buf, pad([midi(x + 12) for x in tones], 4 * beat * 2, 1400, a=0.3), t0, 0.22)
    return reverb(buf, 1.2, 0.15)


def song_sad():
    """Lonely piano: Am - F - C - G, slow."""
    beat = 60 / 68
    prog = [("A2", [57, 60, 64, 69]), ("F2", [53, 57, 60, 65]), ("C3", [55, 60, 64, 67]), ("G2", [55, 59, 62, 67])]
    dur = len(prog) * 2 * beat + 4
    buf = np.zeros((int(dur * SR), 2))
    mel = [76, 74, 72, 71]
    for i, (bn, tones) in enumerate(prog):
        t0 = i * 2 * beat
        place(buf, piano(midi(note(bn)), 3.0, 0.7), t0, 0.5)
        for j, m in enumerate(tones):
            place(buf, piano(midi(m), 2.5, 0.5), t0 + j * beat * 0.25, 0.3, pan=-0.3 + 0.2 * j)
        place(buf, piano(midi(mel[i]), 2.5, 0.8), t0 + beat, 0.35, 0.2)
    buf += np.stack([pad([midi(45), midi(57), midi(64)], dur, 900, a=1.5, r=2.0)] * 2, 1) * 0.25
    return reverb(buf, 2.6, 0.35)


def song_wedding():
    """Bridal Chorus (Wagner, public domain) on music box + celesta pad + soft strings."""
    bpm = 84
    beat = 60 / bpm
    # (pitch, beats)
    mel = [("G4", 1), ("C5", 1.5), ("C5", 0.5), ("C5", 2), ("G4", 1), ("D5", 1.5), ("B4", 0.5), ("C5", 2),
           ("G4", 1), ("C5", 1.5), ("F5", 0.5), ("F5", 1), ("E5", 1), ("D5", 1.5), ("C5", 0.5), ("B4", 1),
           ("C5", 1), ("D5", 3), ("G4", 1), ("C5", 1.5), ("C5", 0.5), ("C5", 2), ("G4", 1), ("D5", 1.5),
           ("B4", 0.5), ("C5", 2), ("G4", 1), ("C5", 1.5), ("F5", 0.5), ("E5", 1), ("D5", 1), ("C5", 1.5),
           ("B4", 0.5), ("C5", 4)]
    total = sum(b for _, b in mel)
    dur = total * beat + 4
    buf = np.zeros((int(dur * SR), 2))
    t = 0.0
    for p, b in mel:
        place(buf, musicbox(midi(note(p)), 2.0), t * beat, 0.42, 0.1)
        place(buf, musicbox(midi(note(p) + 12), 1.2), t * beat + 0.004, 0.08, -0.2)
        t += b
    # harmony: chord every 2 beats following pickup
    chords = ["C", "C", "G", "C", "C", "F", "G", "G", "C", "C", "G", "C", "C", "F", "G", "C", "C"]
    roots = {"C": (48, "maj"), "F": (53, "maj"), "G": (43, "7")}
    for i, c in enumerate(chords):
        r, k = roots[c]
        start = (1 + i * 2) * beat
        if start > total * beat:
            break
        tones = [midi(x + 12) for x in chord_tones(r, k)]
        place(buf, pad(tones, 2 * beat + 0.6, 1600, detune=0.003, a=0.25, r=0.5), start, 0.22)
        place(buf, bass(midi(r - 12 if r > 45 else r), 2 * beat * 0.95), start, 0.25)
    return reverb(buf, 2.4, 0.3)


def song_chaos():
    """Collapse: taiko drums, low drone, dissonant brass stabs, 100 bpm."""
    bpm = 100
    beat = 60 / bpm
    bars = 7
    dur = bars * 4 * beat + 3
    buf = np.zeros((int(dur * SR), 2))
    drone = pad([midi(26), midi(38), midi(39)], dur, 400, detune=0.01, a=0.5, r=1.0)
    buf += stereo(drone) * 0.5
    pattern = [0, 0.75, 1.5, 2, 2.5, 3, 3.25, 3.5, 3.75]
    for bar in range(bars):
        t0 = bar * 4 * beat
        for p in pattern:
            place(buf, taiko(), t0 + p * beat, 0.6 if p in (0, 2) else 0.35, pan=rng.uniform(-0.4, 0.4))
        place(buf, kick(0.5, 100, 35), t0, 0.8)
        place(buf, kick(0.5, 100, 35), t0 + 2 * beat, 0.8)
        for h in range(8):
            place(buf, hat(open_=h % 2 == 1), t0 + h * beat / 2, 0.1)
        if bar % 2 == 0:
            stab = pad([midi(50), midi(51), midi(57), midi(62)], 1.0, 2500, a=0.01, r=0.6)
            place(buf, stab, t0, 0.55)
            place(buf, stab * 0.7, t0 + 1.5 * beat, 0.45)
        else:
            stab = pad([midi(48), midi(49), midi(55), midi(60)], 1.0, 2500, a=0.01, r=0.6)
            place(buf, stab, t0, 0.55)
    # siren-like rising whine
    t = t_(dur)
    sirenf = 600 + 250 * np.sin(2 * np.pi * 0.5 * t)
    siren = np.sin(2 * np.pi * np.cumsum(sirenf) / SR) * 0.06
    buf += stereo(siren)
    return reverb(soft_limit(buf, 1.4), 1.6, 0.2)


def song_intro():
    """Dark doc opener: drone, sub hits, shimmer."""
    dur = 12
    buf = np.zeros((int(dur * SR), 2))
    buf += stereo(pad([midi(33), midi(45), midi(52)], dur, 700, detune=0.008, a=2.0, r=3.0)) * 0.6
    buf += stereo(pad([midi(64), midi(69), midi(71)], dur, 3000, detune=0.004, a=4.0, r=3.0)) * 0.12
    for s in (0.3, 3.2):
        place(buf, kick(1.6, 70, 28), s, 0.9)
    for i in range(24):
        place(buf, musicbox(midi(rng.choice([81, 84, 88, 93])), 1.5), 1.0 + i * 0.42, 0.05, rng.uniform(-0.8, 0.8))
    return reverb(buf, 3.0, 0.35)


# ---------------------------------------------------------------- sfx
def sfx_tap():
    t = t_(0.06)
    x = np.sin(2 * np.pi * 1800 * t) * expdecay(len(t), 0.008) + 0.4 * hp(noise(len(t)), 3000) * expdecay(len(t), 0.003)
    return x


def sfx_pop():
    t = t_(0.15)
    f = 400 + 900 * (t / 0.15)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * expdecay(len(t), 0.04)


def sfx_chat():
    x = np.zeros(int(0.5 * SR))
    a = musicbox(midi(88), 0.4)
    b = musicbox(midi(93), 0.4)
    x[: len(a)] += a
    s = int(0.07 * SR)
    x[s:s + len(b)] += b[: len(x) - s]
    return x


def sfx_diamond():
    x = np.zeros(int(0.6 * SR))
    for i, m in enumerate([88, 92, 95, 100]):
        s = int(i * 0.045 * SR)
        y = musicbox(midi(m), 0.5)
        x[s:s + len(y)] += y[: len(x) - s] * (0.9 - i * 0.12)
    return x


def sfx_reel(dur=1.8):
    """slot reel ticking that slows down."""
    x = np.zeros(int(dur * SR))
    tt, gap = 0.0, 0.045
    while tt < dur - 0.05:
        y = bp(noise(int(0.02 * SR)), 2500, 7000) * expdecay(int(0.02 * SR), 0.003)
        y += np.sin(2 * np.pi * 2200 * t_(0.02)) * expdecay(int(0.02 * SR), 0.004) * 0.5
        s = int(tt * SR)
        x[s:s + len(y)] += y[: len(x) - s]
        tt += gap
        if tt > dur * 0.6:
            gap *= 1.12
    return x


def sfx_lose():
    """sad trombone: wah wah wah waaah."""
    out = []
    for m, d in [(62, 0.35), (61, 0.35), (60, 0.35), (59, 1.1)]:
        t = t_(d)
        f = midi(m) * (1 + 0.012 * np.sin(2 * np.pi * 5.5 * t) * (t > 0.2))
        y = saw(1, np.cumsum(f) / SR, 1) * 0
        ph = 2 * np.pi * np.cumsum(f) / SR
        y = sum(np.sin(k * ph) / k ** 0.9 for k in range(1, 14))
        y = lp(y, 1400) * env(len(t), a=0.03, d=0.05, s=0.8, r=0.08)
        out.append(y)
    return np.concatenate(out) * 0.6


def sfx_buzz():
    t = t_(0.35)
    return lp(square(140, t, 10), 2500) * env(len(t), a=0.005, d=0, s=1, r=0.05) * 0.6


def sfx_win():
    x = np.zeros(int(1.2 * SR))
    for i, m in enumerate([72, 76, 79, 84]):
        y = marimba(midi(m), 0.8)
        s = int(i * 0.08 * SR)
        x[s:s + len(y)] += y[: len(x) - s]
    return x


def sfx_purchase():
    """ka-ching: register bell + coins."""
    x = np.zeros(int(1.4 * SR))
    b = bell(1800, 1.2) * 0.4
    x[: len(b)] += b
    for i in range(14):
        s = int((0.12 + rng.random() * 0.4) * SR)
        y = musicbox(rng.uniform(2500, 4500), 0.25) * 0.25
        x[s:s + len(y)] += y[: len(x) - s]
    return x


def sfx_whoosh(dur=1.2):
    n = int(dur * SR)
    x = noise(n)
    out = np.zeros(n)
    # time-varying bandpass via chunks
    chunks = 40
    cl = n // chunks
    for i in range(chunks):
        c = (i + 0.5) / chunks
        fc = 300 + 3500 * np.sin(np.pi * c) ** 2
        seg = bp(x[i * cl:(i + 1) * cl + 2000], fc * 0.6, fc * 1.6)[:cl]
        out[i * cl:(i + 1) * cl] = seg
    return out * np.sin(np.pi * np.linspace(0, 1, n)) ** 1.5


def sfx_sparkle(dur=2.0):
    x = np.zeros(int(dur * SR))
    for i in range(30):
        s = int(rng.random() * (dur - 0.4) * SR)
        y = musicbox(rng.uniform(2000, 6000), 0.35) * rng.uniform(0.2, 0.6)
        x[s:s + len(y)] += y[: len(x) - s]
    return x


def sfx_bells():
    x = np.zeros(int(6 * SR))
    for i, f in enumerate([392, 330, 262, 392, 330, 262]):
        y = bell(f, 4.0)
        s = int(i * 0.55 * SR)
        x[s:s + len(y)] += y[: len(x) - s] * 0.6
    return reverb(x, 2.5, 0.35)


def sfx_cheer(dur=3.5):
    """crowd cheer / applause: thousands of tiny claps + vocal-ish formant noise."""
    n = int(dur * SR)
    x = np.zeros(n)
    for _ in range(int(dur * 380)):
        s = int(rng.random() * (n - 2000))
        c = clap(0.04)[:1500] * rng.uniform(0.1, 0.5)
        x[s:s + len(c)] += c
    voc = noise(n)
    voc = bp(voc, 400, 900) * 0.6 + bp(noise(n), 1100, 2600) * 0.3
    x += voc * 0.4
    e = np.minimum(1, np.linspace(0, 6, n)) * np.minimum(1, np.linspace(3.5, 0, n))
    return reverb(x * e, 1.5, 0.3)


def sfx_rumble(dur=6.0):
    n = int(dur * SR)
    x = np.cumsum(noise(n))
    x = hp(x, 15)
    x = lp(x, 120, 4)
    mod = 0.6 + 0.4 * lp(np.abs(noise(n)), 3)
    return x * mod * np.minimum(1, np.linspace(0, 3, n))


def sfx_boom():
    n = int(3.5 * SR)
    t = t_(3.5)
    x = kick(3.5, 90, 22) * 1.2
    x += lp(noise(n), 800) * expdecay(n, 0.5)
    x += bp(noise(n), 1500, 8000) * expdecay(n, 0.05) * 0.6
    x = soft_limit(x, 2.5)
    return reverb(x, 3.0, 0.3)


def sfx_crack():
    n = int(1.2 * SR)
    x = np.zeros(n)
    for i in range(40):
        s = int((rng.random() ** 2) * 0.8 * SR)
        y = hp(noise(800), 1500) * expdecay(800, 0.002) * rng.uniform(0.3, 1)
        x[s:s + 800] += y
    x += lp(noise(n), 300) * expdecay(n, 0.3)
    return x


def sfx_siren(dur=6.0):
    t = t_(dur)
    f = 650 + 300 * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 1.1 * t)))
    f = lp(f, 30)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = sum(np.sin(k * ph) / k for k in range(1, 8))
    return lp(x, 3500) * 0.6


def sfx_meteor():
    n = int(1.6 * SR)
    t = t_(1.6)
    f = 2400 * np.exp(-t / 0.9) + 200
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.15
    x += bp(noise(n), 300, 3000) * np.linspace(0.2, 1, n)
    return x * np.minimum(1, np.linspace(0, 4, n))


def sfx_disconnect():
    x = np.zeros(int(1.0 * SR))
    for i, m in enumerate([76, 71]):
        y = marimba(midi(m), 0.6)
        s = int(i * 0.16 * SR)
        x[s:s + len(y)] += y[: len(x) - s]
    return x


def sfx_braam():
    dur = 6
    x = pad([midi(26), midi(38), midi(45), midi(50)], dur, 1200, detune=0.012, a=0.02, r=4.0)
    x[: int(4 * SR)] += kick(4, 80, 25) * 0.7
    x = soft_limit(x * 2, 2)
    return reverb(x, 3.5, 0.4)


def sfx_riser(dur=3.0):
    n = int(dur * SR)
    t = t_(dur)
    f = 200 * 2 ** (t / dur * 4)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.3
    x += hp(noise(n), 2000) * (t / dur) ** 2 * 0.5
    return x * (t / dur) ** 1.5


def sfx_scratch():
    n = int(0.6 * SR)
    t = t_(0.6)
    f = 300 + 1800 * np.abs(np.sin(2 * np.pi * 2.4 * t))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.4
    x += bp(noise(n), 500, 4000) * 0.6
    return x * expdecay(n, 0.25)


def sfx_land():
    return kick(0.4, 120, 40) + lp(noise(int(0.4 * SR)), 1000) * expdecay(int(0.4 * SR), 0.06) * 0.5


def sfx_heartpop():
    x = np.zeros(int(1.2 * SR))
    for i in range(8):
        s = int(i * 0.09 * SR)
        y = musicbox(midi(84 + i * 2), 0.4) * 0.4
        y[: int(0.15 * SR)] += sfx_pop() * 0.4
        x[s:s + len(y)] += y[: len(x) - s]
    return x


def sfx_steps(dur=4.0, rate=6.5):
    x = np.zeros(int(dur * SR))
    k = 0.0
    while k < dur - 0.1:
        y = lp(noise(int(0.05 * SR)), 900) * expdecay(int(0.05 * SR), 0.01)
        s = int(k * SR)
        x[s:s + len(y)] += y * rng.uniform(0.6, 1)
        k += 1 / rate + rng.uniform(-0.01, 0.01)
    return x


if __name__ == "__main__":
    write("music/intro.wav", song_intro())
    write("music/lobby.wav", song_lobby())
    write("music/casino.wav", song_casino())
    write("music/sad.wav", song_sad())
    write("music/wedding.wav", song_wedding())
    write("music/chaos.wav", song_chaos())
    for name, fn in [("tap", sfx_tap), ("pop", sfx_pop), ("chat", sfx_chat), ("diamond", sfx_diamond),
                     ("reel", sfx_reel), ("lose", sfx_lose), ("buzz", sfx_buzz), ("win", sfx_win),
                     ("purchase", sfx_purchase), ("whoosh", sfx_whoosh), ("sparkle", sfx_sparkle),
                     ("bells", sfx_bells), ("cheer", sfx_cheer), ("rumble", sfx_rumble), ("boom", sfx_boom),
                     ("crack", sfx_crack), ("siren", sfx_siren), ("meteor", sfx_meteor),
                     ("disconnect", sfx_disconnect), ("braam", sfx_braam), ("riser", sfx_riser),
                     ("scratch", sfx_scratch), ("land", sfx_land), ("heartpop", sfx_heartpop),
                     ("steps", sfx_steps)]:
        write(f"sfx/{name}.wav", fn(), 0.8)
