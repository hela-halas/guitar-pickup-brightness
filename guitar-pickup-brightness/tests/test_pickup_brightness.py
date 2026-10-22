import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import pickup_brightness as pb  # noqa: E402


def test_amplitude_coefficients_match_essay_table_2():
    n = np.arange(1, 10)
    bpp = [0.42, 0.80, 1.18, 1.48, 1.72, 1.90, 1.98, 2.00, 1.90]
    mpp = [0.88, 1.56, 1.96, 1.94, 1.56, 0.84, 0.02, 0.90, 1.58]
    assert np.allclose(pb.amplitude_coefficient(n, pb.BPP_CM), bpp, atol=0.02)
    assert np.allclose(pb.amplitude_coefficient(n, pb.MPP_CM), mpp, atol=0.02)


def test_node_of_seventh_harmonic_sits_on_middle_pickup():
    nodes = pb.nodes_from_bridge(7)
    assert np.min(np.abs(nodes - pb.MPP_CM)) == pytest.approx(0.04, abs=0.01)


def test_harmonic_extraction_recovers_pure_tones():
    # 82.5 Hz over 2 s is a whole number of cycles, so each tone sits exactly
    # on a DFT bin (no leakage), which isolates the peak-picking logic.
    fs, f0 = pb.FS, 82.5
    t = np.arange(fs * 2) / fs
    amps = np.array([1.0, 0.5, 0.25])
    sig = sum(a * np.sin(2 * np.pi * (k + 1) * f0 * t) for k, a in enumerate(amps))
    freqs, mags = pb.harmonic_magnitudes(sig, f0=f0, n_harmonics=3)
    assert np.allclose(freqs, f0 * np.arange(1, 4), atol=1.0)
    assert np.allclose(mags / mags[0], amps, rtol=0.05)


def test_stereo_is_averaged_to_mono():
    stereo = np.column_stack([np.ones(4), np.zeros(4)])
    assert np.allclose(pb.to_mono(stereo), 0.5)


def test_brightness_metrics_on_known_spectrum():
    mags = np.array([10, 0, 0, 0, 5, 5, 0, 0, 0], dtype=float)
    assert pb.brightness_ratio(mags) == pytest.approx(1.0)
    assert pb.modified_brightness_ratio(mags) == pytest.approx(1.0)
    freqs = np.arange(1, 10) * 100.0
    assert pb.spectral_centroid(freqs, mags) == pytest.approx((1000 + 2500 + 3000) / 20)


def test_synthetic_bridge_pluck_is_brighter():
    metrics = {}
    for name, x in (("mpp", pb.MPP_CM), ("bpp", pb.BPP_CM)):
        f, m = pb.harmonic_magnitudes(pb.synth_pluck(x, seed=0), duration_s=2.2)
        metrics[name] = pb.brightness_metrics(f, m)
    for key in metrics["mpp"]:
        assert metrics["bpp"][key] > metrics["mpp"][key]
