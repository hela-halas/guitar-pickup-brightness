"""
pickup_brightness
=================

Tools for analysing how electric-guitar pickup position shapes tone.

Python reimplementation (2026) of the analysis in my IB Physics Extended Essay
(2023), originally written in MATLAB. Three parts:

1. Theory     - standing-wave nodes/antinodes and the pickup "amplitude
                coefficient" 2|sin(n*pi*x/L)| for each harmonic.
2. Analysis   - extract harmonic magnitudes from a recording with the DFT,
                then compute brightness metrics.
3. Synthesis  - a simple modal model of a plucked string seen by a pickup,
                so the full pipeline can run without the original recordings.
"""

from __future__ import annotations

import numpy as np

# Guitar geometry from the essay (Fender Squier Stratocaster)
SCALE_LENGTH_CM = 64.8   # nut-to-bridge string length
BPP_CM = 4.3             # bridge pickup position, distance from bridge
MPP_CM = 9.3             # middle pickup position, distance from bridge
PLUCK_CM = 13.6          # plucking position, distance from bridge
E2_HZ = 82.41            # nominal open low-E frequency
FS = 44_100              # sampling rate used for the recordings


# ---------------------------------------------------------------------------
# 1. Theory
# ---------------------------------------------------------------------------

def nodes_from_bridge(n: int, length: float = SCALE_LENGTH_CM) -> np.ndarray:
    """Node positions of harmonic n, measured from the bridge: x = mL/n."""
    return np.arange(n + 1) * length / n


def antinodes_from_bridge(n: int, length: float = SCALE_LENGTH_CM) -> np.ndarray:
    """Antinode positions of harmonic n, from the bridge: x = (m + 1/2)L/n."""
    return (np.arange(n) + 0.5) * length / n


def amplitude_coefficient(n, x: float, length: float = SCALE_LENGTH_CM):
    """
    Peak-velocity weighting a pickup at position x applies to harmonic n.

    From v_n(x, t) = -2 A_n w_n sin(n pi x / L) sin(w_n t): with |sin(w_n t)| = 1
    the coefficient is 2|sin(n pi x / L)|. It is 0 at a node and 2 at an antinode.
    """
    n = np.asarray(n)
    return 2 * np.abs(np.sin(n * np.pi * x / length))


# ---------------------------------------------------------------------------
# 2. Analysis
# ---------------------------------------------------------------------------

def to_mono(signal: np.ndarray) -> np.ndarray:
    """Average stereo channels; pass mono through unchanged."""
    signal = np.asarray(signal, dtype=float)
    return signal.mean(axis=1) if signal.ndim == 2 else signal


def harmonic_magnitudes(signal: np.ndarray, fs: int = FS, f0: float = E2_HZ,
                        n_harmonics: int = 9, search_hz: float = 10.0,
                        duration_s: float | None = None):
    """
    Find the DFT peak near each multiple of f0.

    Replaces the hand-unrolled search loops in the original MATLAB script.
    Returns (peak_frequencies_hz, peak_magnitudes) for harmonics 1..n_harmonics.
    """
    x = to_mono(signal)
    if duration_s is not None:
        x = x[: int(duration_s * fs)]
    spectrum = np.abs(np.fft.rfft(x))
    freqs = np.fft.rfftfreq(len(x), d=1 / fs)

    peak_f, peak_m = [], []
    for n in range(1, n_harmonics + 1):
        band = (freqs > n * f0 - search_hz) & (freqs < n * f0 + search_hz)
        i = np.flatnonzero(band)[np.argmax(spectrum[band])]
        peak_f.append(freqs[i])
        peak_m.append(spectrum[i])
    return np.array(peak_f), np.array(peak_m)


def spectral_centroid(freqs, mags) -> float:
    """Magnitude-weighted mean frequency of the harmonics (Hz)."""
    mags = np.asarray(mags, dtype=float)
    return float(np.dot(mags, freqs) / mags.sum())


def brightness_ratio(mags) -> float:
    """Tristimulus-based ratio: (M5 + ... + Mn) / M1."""
    mags = np.asarray(mags, dtype=float)
    return float(mags[4:].sum() / mags[0])


def modified_brightness_ratio(mags) -> float:
    """Upper vs whole lower series: (M5 + ... + Mn) / (M1 + ... + M4)."""
    mags = np.asarray(mags, dtype=float)
    return float(mags[4:].sum() / mags[:4].sum())


def brightness_metrics(freqs, mags) -> dict:
    return {
        "spectral_centroid_hz": spectral_centroid(freqs, mags),
        "brightness_ratio": brightness_ratio(mags),
        "modified_brightness_ratio": modified_brightness_ratio(mags),
    }


# ---------------------------------------------------------------------------
# 3. Synthesis (new in the 2026 refresh)
# ---------------------------------------------------------------------------

def synth_pluck(pickup_cm: float, pluck_cm: float = PLUCK_CM,
                f0: float = E2_HZ, length: float = SCALE_LENGTH_CM,
                duration_s: float = 3.0, fs: int = FS, n_modes: int = 30,
                base_decay: float = 0.6, decay_growth: float = 0.25,
                noise: float = 0.0, seed: int | None = None) -> np.ndarray:
    """
    Modal model of an ideal plucked string as seen by a velocity-sensing pickup.

    - A triangular pluck at pluck_cm gives mode displacements A_n ~ sin(n pi p/L) / n^2.
    - The pickup senses velocity, so each mode is weighted by w_n * sin(n pi x/L).
    - Higher modes decay faster (damping grows linearly with n).
    """
    rng = np.random.default_rng(seed)
    t = np.arange(int(duration_s * fs)) / fs
    out = np.zeros_like(t)
    for n in range(1, n_modes + 1):
        a_n = np.sin(n * np.pi * pluck_cm / length) / n**2
        w_n = 2 * np.pi * n * f0
        gain = a_n * w_n * np.sin(n * np.pi * pickup_cm / length)
        decay = base_decay * (1 + decay_growth * (n - 1))
        out += gain * np.exp(-decay * t) * np.sin(w_n * t)
    out /= np.max(np.abs(out))
    if noise:
        out += noise * rng.standard_normal(len(out))
    return out
