"""
Reproduce the essay's main results and figures.

    python reproduce.py

Writes figures to figures/ and a results table to results/metrics.md.
"""

from pathlib import Path
import csv
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

sys.path.insert(0, str(Path(__file__).parent / "src"))
import pickup_brightness as pb  # noqa: E402

ROOT = Path(__file__).parent
FIG = ROOT / "figures"
RES = ROOT / "results"
FIG.mkdir(exist_ok=True)
RES.mkdir(exist_ok=True)

# Excel default palette, as used in the essay's graphs
BLUE, ORANGE = "#4472C4", "#ED7D31"
plt.rcParams.update({"figure.dpi": 150, "font.family": "sans-serif", "font.size": 10})

harmonics = np.arange(1, 10)
harmonic_freqs = harmonics * pb.E2_HZ


def load_trials():
    data = {"MPP": [], "BPP": []}
    with open(ROOT / "data" / "harmonic_magnitudes.csv") as f:
        for row in csv.DictReader(f):
            data[row["position"]].append([float(row[f"h{n}"]) for n in harmonics])
    return {k: np.array(v) for k, v in data.items()}


def essay_axes(ax):
    """Light gridlines, box frame and bottom-centred legend, like the essay's Excel charts."""
    ax.grid(True, which="major", color="#d9d9d9", lw=0.8)
    ax.minorticks_on()
    ax.grid(True, which="minor", axis="y", color="#f0f0f0", lw=0.5)
    ax.tick_params(which="minor", length=0)
    ax.set_xticks(harmonics)
    ax.set_xlim(1, 9)
    ax.set_axisbelow(True)


# --- Graph 1: amplitude coefficients (reproduces essay Graph 1) ------------
coef_bpp = pb.amplitude_coefficient(harmonics, pb.BPP_CM)
coef_mpp = pb.amplitude_coefficient(harmonics, pb.MPP_CM)

fig, ax = plt.subplots(figsize=(7, 4.4))
ax.scatter(harmonics, coef_bpp, marker="x", color=BLUE, label="BPP", zorder=3, clip_on=False)
ax.scatter(harmonics, coef_mpp, marker="x", color=ORANGE, label="MPP", zorder=3, clip_on=False)
essay_axes(ax)
ax.set_ylim(0, 2.5)
ax.set_xlabel(r"Harmonic Mode, $n$")
ax.set_ylabel("Amplitude Coefficient")
ax.set_title(r"Amplitude coefficients per harmonic mode ($n$=1, 2, ... , 9)", fontweight="bold")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=2, frameon=False)
fig.tight_layout()
fig.savefig(FIG / "graph1_amplitude_coefficients.png")
plt.close(fig)

# --- Graph 6: mean magnitudes with SD (reproduces essay Graph 6) -----------
trials = load_trials()
fig, ax = plt.subplots(figsize=(7, 4.4))
for pos, color in (("MPP", BLUE), ("BPP", ORANGE)):
    m = trials[pos]
    ax.errorbar(harmonics, m.mean(0), yerr=m.std(0, ddof=1), fmt="x", color=color,
                ecolor=color, elinewidth=0.6, capsize=3, label=pos, zorder=3, clip_on=False)
essay_axes(ax)
ax.set_ylim(0, 5000)
ax.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter("{x:,.0f}"))
ax.set_xlabel(r"Harmonic ($n$)")
ax.set_ylabel("Magnitude [au]")
ax.set_title("Mean magnitude values with standard deviation for each harmonic frequency",
             fontweight="bold", fontsize=10)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=2, frameon=False)
fig.tight_layout()
fig.savefig(FIG / "graph6_mean_harmonic_magnitudes.png")
plt.close(fig)

# --- New (2026): measured vs ideal-string model ------------------------------
fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.8), sharey=True)
for ax, pos, color in ((axes[0], "MPP", BLUE), (axes[1], "BPP", ORANGE)):
    mean = trials[pos].mean(0)
    x = pb.MPP_CM if pos == "MPP" else pb.BPP_CM
    # Ideal plucked string seen by a velocity pickup: n * sin(n pi p/L)/n^2 * sin(n pi x/L)
    model = np.abs(np.sin(harmonics * np.pi * pb.PLUCK_CM / pb.SCALE_LENGTH_CM)
                   * np.sin(harmonics * np.pi * x / pb.SCALE_LENGTH_CM) / harmonics)
    ax.scatter(harmonics, mean / mean.sum(), marker="x", color=color, zorder=3, clip_on=False,
               label=f"{pos}, measured (mean of 5 trials)")
    ax.plot(harmonics, model / model.sum(), ".--", color="#595959", lw=0.8, zorder=2,
            label="ideal-string model")
    essay_axes(ax)
    ax.set_title(f"{pos} ($x_{{{pos}}}$ = {x} cm)", fontweight="bold", fontsize=10)
    ax.set_xlabel(r"Harmonic ($n$)")
    ax.legend(loc="upper right", frameon=False, fontsize=8)
axes[0].set_ylabel(r"Relative magnitude $M_n / M$")
axes[0].set_ylim(0, 0.45)
fig.suptitle("Measured relative magnitudes vs an ideal plucked-string model", fontweight="bold")
fig.tight_layout()
fig.savefig(FIG / "new_measured_vs_model.png")
plt.close(fig)

# --- Metrics -----------------------------------------------------------------
lines = ["# Results", "",
         "Sound characteristics from the mean harmonic magnitudes, first 2.2 s (reproduces essay Table 5).", "",
         "| Characteristic | MPP | BPP | Ratio (BPP/MPP) |",
         "|---|---|---|---|"]
summary = {}
for pos in ("MPP", "BPP"):
    summary[pos] = pb.brightness_metrics(harmonic_freqs, trials[pos].mean(0))
names = {"spectral_centroid_hz": "C_t – Spectral Centroid [Hz] (Equation 12)",
         "brightness_ratio": "R_b – Brightness Ratio / Tristimulus (Equation 13)",
         "modified_brightness_ratio": "R_mb – Modified Brightness Ratio (Equation 14)"}
for key, name in names.items():
    a, b = summary["MPP"][key], summary["BPP"][key]
    lines.append(f"| {name} | {a:.2f} | {b:.2f} | {b / a:.2f} |")

# New in 2026: per-trial metrics and a significance test the essay didn't include
lines += ["", "## Per-trial significance (added 2026)", "",
          "Metrics computed for each of the 5 trials per position, compared with Welch's t-test.", "",
          "| Characteristic | MPP (mean ± SD) | BPP (mean ± SD) | Welch t | p |",
          "|---|---|---|---|---|"]
for key, name in names.items():
    per = {pos: np.array([pb.brightness_metrics(harmonic_freqs, row)[key] for row in trials[pos]])
           for pos in ("MPP", "BPP")}
    t, p = stats.ttest_ind(per["BPP"], per["MPP"], equal_var=False)
    d = 1 if "centroid" in key else 3
    lines.append(f"| {name} | {per['MPP'].mean():.{d}f} ± {per['MPP'].std(ddof=1):.{d}f} "
                 f"| {per['BPP'].mean():.{d}f} ± {per['BPP'].std(ddof=1):.{d}f} | {t:.1f} | {p:.1e} |")

# Synthetic pipeline check: does DFT extraction recover the same ordering?
lines += ["", "## Synthetic pipeline check", "",
          "Full pipeline (synthesis → DFT peak-picking → metrics) on modelled plucks, first 2.2 s.", "",
          "| Characteristic | MPP | BPP |", "|---|---|---|"]
syn = {}
for pos, x in (("MPP", pb.MPP_CM), ("BPP", pb.BPP_CM)):
    f, m = pb.harmonic_magnitudes(pb.synth_pluck(x, seed=1, noise=0.002), duration_s=2.2)
    syn[pos] = pb.brightness_metrics(f, m)
for key, name in names.items():
    lines.append(f"| {name} | {syn['MPP'][key]:.2f} | {syn['BPP'][key]:.2f} |")

(RES / "metrics.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
