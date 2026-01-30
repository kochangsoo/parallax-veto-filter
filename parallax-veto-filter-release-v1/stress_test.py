#!/usr/bin/env python3
"""Dirty-data stress test for the shell-window veto (Option A).

This script evaluates robustness against non-Gaussian outliers by generating synthetic
*spurious tracklets* whose motion does not obey orbital mechanics.

Option A (unit-consistent with the manuscript):
- We model spurious tracklets as **total sky-plane displacement** (arcsec) over the baseline (e.g., 2 days),
  not a per-day rate.
- Displacements are drawn from a wide uniform distribution to emulate outliers.

Outputs:
- Prints pass fraction and rejection rate
- Saves a histogram figure with the veto window overlay (default: Figure 4 candidate)

Dependencies: numpy, matplotlib
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt


def run_stress_test(
    target_dist: float,
    shell_width: float,
    baseline_days: float,
    n_artifacts: int,
    seed: int,
    displacement_min: float,
    displacement_max: float,
    margin_arcsec: float,
    out_fig: str,
    dpi: int,
):
    rng = np.random.default_rng(seed)

    # Spurious tracklets: total displacement over baseline (arcsec over baseline_days)
    spurious_disp = rng.uniform(displacement_min, displacement_max, n_artifacts)

    # Veto window: total parallax displacement over baseline (arcsec over baseline_days)
    limit_min = (3600.0 / (target_dist + shell_width)) * baseline_days - margin_arcsec
    limit_max = (3600.0 / (target_dist - shell_width)) * baseline_days + margin_arcsec

    passed = (spurious_disp >= limit_min) & (spurious_disp <= limit_max)
    n_passed = int(passed.sum())
    pass_fraction = n_passed / n_artifacts
    rejection_rate = (1.0 - pass_fraction) * 100.0

    print("=" * 60)
    print(f"[Stress Test Result] Spurious tracklets (N={n_artifacts})")
    print(f" - Uniform displacement range: [{displacement_min}, {displacement_max}] arcsec over {baseline_days:g} days")
    print(f" - Filter window: {limit_min:.2f} ~ {limit_max:.2f} arcsec over {baseline_days:g} days")
    print(f" - False positives (passed): {n_passed} objects")
    print(f" - Pass fraction f_bg: {pass_fraction:.4f}")
    print(f" - Rejection rate: {rejection_rate:.2f}%")
    print("=" * 60)

    # Figure (histogram + window)
    plt.figure(figsize=(10, 5.5))
    plt.hist(spurious_disp, bins=80, alpha=0.9)
    plt.axvline(limit_min, linestyle="--", linewidth=2)
    plt.axvline(limit_max, linestyle="--", linewidth=2)
    plt.title("Dirty-Data Stress Test: Spurious Tracklets vs Shell-Window Veto")
    plt.xlabel(f"Total sky-plane displacement over {baseline_days:g} days (arcsec)")
    plt.ylabel("Count")
    plt.grid(True, which="both", ls="-", alpha=0.2)

    stats = (
        f"N = {n_artifacts}\n"
        f"Window = [{limit_min:.2f}, {limit_max:.2f}] arcsec\n"
        f"Passed = {n_passed} (f_bg={pass_fraction:.4f})\n"
        f"Rejection = {rejection_rate:.2f}%"
    )
    plt.text(0.02, 0.98, stats, transform=plt.gca().transAxes, va="top",
             bbox=dict(facecolor="white", alpha=0.85))

    plt.tight_layout()
    plt.savefig(out_fig, dpi=dpi, bbox_inches="tight")
    print(f"Saved: {out_fig}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target-dist", type=float, default=600.0, help="Target shell center distance (AU)")
    ap.add_argument("--shell-width", type=float, default=20.0, help="Half-width of target shell (AU)")
    ap.add_argument("--baseline-days", type=float, default=2.0, help="Revisit baseline (days)")
    ap.add_argument("--n-artifacts", type=int, default=5000, help="Number of spurious tracklets")
    ap.add_argument("--seed", type=int, default=99, help="RNG seed")
    ap.add_argument("--disp-min", type=float, default=-100.0, help="Min total displacement (arcsec over baseline)")
    ap.add_argument("--disp-max", type=float, default=100.0, help="Max total displacement (arcsec over baseline)")
    ap.add_argument("--margin", type=float, default=0.1, help="Margin added to veto window (arcsec)")
    ap.add_argument("--out", type=str, default="figure4_spurious_tracklets_hist.png", help="Output figure filename")
    ap.add_argument("--dpi", type=int, default=600, help="Output DPI")
    args = ap.parse_args()

    run_stress_test(
        target_dist=args.target_dist,
        shell_width=args.shell_width,
        baseline_days=args.baseline_days,
        n_artifacts=args.n_artifacts,
        seed=args.seed,
        displacement_min=args.disp_min,
        displacement_max=args.disp_max,
        margin_arcsec=args.margin,
        out_fig=args.out,
        dpi=args.dpi,
    )


if __name__ == "__main__":
    main()
