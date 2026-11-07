"""Procedural, royalty-free soundtrack for RIWAQ clips (no samples, no licensed music).
make(path, total, t_drop, t_cta): pad + riser intro, warm 112 BPM groove after the drop, bell + pad on the CTA."""
import numpy as np
from scipy import signal
from scipy.io import wavfile

SR = 44100

def _lp(x, fc, o=2):
    b, a = signal.butter(o, min(fc, SR * .45) / (SR / 2), "low"); return signal.lfilter(b, a, x)
def _hp(x, fc, o=2):
    b, a = signal.butter(o, fc / (SR / 2), "high"); return signal.lfilter(b, a, x)
def _bp(x, f1, f2, o=2):
    b, a = signal.butter(o, [f1 / (SR / 2), min(f2, SR * .45) / (SR / 2)], "band"); return signal.lfilter(b, a, x)
def _t(d): return np.arange(int(d * SR)) / SR

def _add(buf, x, t0, gain=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= buf.shape[0] or i + len(x) <= 0: return
    j = min(buf.shape[0], i + len(x)); x = x[:j - i] * gain
    buf[i:j, 0] += x * np.sqrt(0.5 * (1 - pan)) * 1.414
    buf[i:j, 1] += x * np.sqrt(0.5 * (1 + pan)) * 1.414

def kick():
    t = _t(0.42); f = 44 + 100 * np.exp(-t / 0.04)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.13) + 0.15 * np.sin(2 * np.pi * 2000 * t) * np.exp(-t / 0.003)

def hat(rng, d=0.06):
    n = int(d * SR); return _hp(rng.standard_normal(n), 7500) * np.exp(-np.arange(n) / SR / 0.014)

def snap(rng):
    n = int(0.22 * SR); x = _bp(rng.standard_normal(n), 1100, 3800); e = np.exp(-np.arange(n) / SR / 0.06)
    for k in (0.0, 0.011, 0.022):                                  # three quick hits, like hand claps
        e += 0.6 * np.exp(-np.maximum(np.arange(n) / SR - k, 0) / 0.006) * (np.arange(n) / SR >= k)
    return x * e * 0.5

def pluck(f, d=0.5):
    t = _t(d); x = sum(np.sin(2 * np.pi * f * k * t) / k ** 1.3 for k in range(1, 6))
    return _lp(x, 900) * np.exp(-t / 0.18)

def pad(freqs, d, rng, bright=1400):
    t = _t(d); x = np.zeros(len(t))
    for f in freqs:
        for det in (-0.004, 0.0, 0.0045):
            ph = rng.random() * 6.28
            x += 2 * ((f * (1 + det) * t + ph / 6.28) % 1) - 1
    x = _lp(x / (3 * len(freqs)), bright, 2)
    att, rel = min(0.35, d / 3), min(0.6, d / 3)
    env = np.minimum(1, t / att) * np.minimum(1, (d - t) / rel)
    return x * env

def bell(f0, d=2.4):
    t = _t(d); x = np.zeros(len(t))
    for m, a, tau in ((1, 1, 1.4), (2.0, .5, .9), (2.76, .35, .6), (5.4, .2, .25), (8.93, .1, .12)):
        x += a * np.sin(2 * np.pi * f0 * m * t) * np.exp(-t / tau)
    return x * 0.35

def whoosh(rng, d=0.7, rise=True):
    n = int(d * SR); x = rng.standard_normal(n); t = np.arange(n) / n
    fc = (300 + 5000 * t ** 2) if rise else (5200 - 4800 * t ** 0.5)
    y = np.zeros(n); blk = 512
    for i in range(0, n, blk):
        c = float(fc[i]); y[i:i + blk] = _bp(x[i:i + blk], max(c * 0.6, 60), c * 1.6, 1)
    env = (t ** 1.6) * (1 - t) ** 0.3 if rise else (1 - t) ** 2
    return y * env * 0.5

CHORDS = [  # Am – F – C – G (warm, neutral)
    ([220.0, 261.63, 329.63], 110.0), ([174.61, 220.0, 261.63], 87.31),
    ([261.63, 329.63, 392.0], 130.81), ([196.0, 246.94, 293.66], 98.0)]

def make(path, total, t_drop, t_cta, bpm=112, seed=3):
    rng = np.random.default_rng(seed)
    buf = np.zeros((int((total + 0.5) * SR), 2))
    beat = 60.0 / bpm; bar = 4 * beat
    # intro: soft pad + riser into the drop
    _add(buf, pad(CHORDS[0][0], t_drop + 0.4, rng, 900), 0.0, 0.32, -0.15)
    _add(buf, pad([c * 2 for c in CHORDS[0][0]], t_drop + 0.4, rng, 1600), 0.0, 0.12, 0.2)
    _add(buf, whoosh(rng, min(1.4, t_drop), True), max(0, t_drop - 1.4), 0.55)
    # groove
    t, k = t_drop, 0
    while t < t_cta - 0.05:
        ch, root = CHORDS[(k // 4) % 4]
        if k % 4 == 0: _add(buf, pad(ch, bar + 0.3, rng), t, 0.28, 0.0)
        _add(buf, kick(), t, 0.85 if k % 2 == 0 else 0.55)
        if k % 2 == 1: _add(buf, snap(rng), t, 0.5, 0.1)
        _add(buf, hat(rng), t + beat / 2, 0.6, 0.35); _add(buf, hat(rng, 0.03), t, 0.25, -0.3)
        _add(buf, pluck(root), t, 0.5)
        if k % 4 == 2: _add(buf, pluck(root * 2, 0.35), t + beat * 0.75, 0.22, -0.2)
        t += beat; k += 1
    # CTA: whoosh, bell, resolving pad
    _add(buf, whoosh(rng, 0.6, False), t_cta - 0.05, 0.45)
    _add(buf, kick(), t_cta, 0.8)
    _add(buf, bell(659.25), t_cta + 0.05, 0.5, 0.15); _add(buf, bell(987.77, 1.8), t_cta + 0.35, 0.28, -0.2)
    _add(buf, pad(CHORDS[0][0], total - t_cta + 0.3, rng, 1100), t_cta, 0.3)
    tt = t_cta
    while tt < total - 0.6:
        _add(buf, hat(rng, 0.03), tt + beat / 2, 0.35, 0.3); tt += beat
    # master: gentle saturation, fades, peak -1 dBFS
    buf = np.tanh(buf * 1.2) / np.tanh(1.2)
    n = int(total * SR); buf = buf[:n]
    f = np.ones(n); fo = int(0.9 * SR); f[-fo:] = np.linspace(1, 0, fo) ** 1.5; f[:int(0.03 * SR)] = np.linspace(0, 1, int(0.03 * SR))
    buf *= f[:, None]
    buf *= 10 ** (-1 / 20) / max(1e-9, np.abs(buf).max())
    wavfile.write(path, SR, (buf * 32767).astype(np.int16))
    return path

if __name__ == "__main__":
    import sys
    print(make(sys.argv[1], 14.0, 2.4, 10.6))
