#!/usr/bin/env python3
"""Parallax-Based Veto Filter (shell-conditional) — reference simulation.

Generates synthetic background + target-shell populations and applies a shell-window veto
based on parallax-implied sky-plane motion over a short baseline.

Outputs:
- figure3_parallax_veto.png (high-resolution)
- prints recovery/rejection statistics
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt

def calculate_parallax_motion(distance_au: np.ndarray, baseline_days: float, sigma_arcsec: float, rng: np.random.Generator):
    rate_arcsec_per_day = 3600.0 / distance_au
    obs_noise = rng.normal(0.0, sigma_arcsec, size=distance_au.shape[0])
    return rate_arcsec_per_day * baseline_days + obs_noise

def apply_filter(motions: np.ndarray, limit_min: float, limit_max: float):
    return (motions >= limit_min) & (motions <= limit_max)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--target-dist', type=float, default=600.0)
    ap.add_argument('--shell-width', type=float, default=20.0)
    ap.add_argument('--baseline-days', type=float, default=2.0)
    ap.add_argument('--sigma', type=float, default=0.05)
    ap.add_argument('--n-mba', type=int, default=5000)
    ap.add_argument('--n-tno', type=int, default=2000)
    ap.add_argument('--n-signal', type=int, default=1000)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--out', type=str, default='figure3_parallax_veto.png')
    ap.add_argument('--dpi', type=int, default=600)
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)

    d0 = args.target_dist
    dw = args.shell_width
    dt = args.baseline_days

    dist_mba = rng.uniform(2.0, 3.5, args.n_mba)
    motion_mba = calculate_parallax_motion(dist_mba, dt, args.sigma, rng)

    dist_tno = rng.uniform(30.0, 100.0, args.n_tno)
    motion_tno = calculate_parallax_motion(dist_tno, dt, args.sigma, rng)

    dist_sig = rng.uniform(d0 - dw, d0 + dw, args.n_signal)
    motion_sig = calculate_parallax_motion(dist_sig, dt, args.sigma, rng)

    limit_min = (3600.0 / (d0 + dw)) * dt - 0.1
    limit_max = (3600.0 / (d0 - dw)) * dt + 0.1

    passed_mba = apply_filter(motion_mba, limit_min, limit_max)
    passed_tno = apply_filter(motion_tno, limit_min, limit_max)
    passed_sig = apply_filter(motion_sig, limit_min, limit_max)

    recovery = passed_sig.sum() / args.n_signal * 100.0
    total_noise = args.n_mba + args.n_tno
    total_noise_passed = passed_mba.sum() + passed_tno.sum()
    rejection = (total_noise - total_noise_passed) / total_noise * 100.0

    print(f"Filter Window for {d0:.0f} AU (+/- {dw:.0f}): {limit_min:.2f} ~ {limit_max:.2f} arcsec")
    print(f"Recovery Rate: {recovery:.2f}%")
    print(f"Rejection Rate: {rejection:.2f}%")

    plt.figure(figsize=(10, 6))
    plt.scatter(dist_mba, motion_mba, s=10, alpha=0.5, label='Noise (Main Belt)')
    plt.scatter(dist_tno, motion_tno, s=10, alpha=0.5, label='Noise (Ordinary TNOs)')
    plt.scatter(dist_sig, motion_sig, s=20, alpha=0.8, label='Target (Planet 9 Candidate)')

    plt.axhline(y=limit_max, linestyle='--', linewidth=2, label='Filter Thresholds')
    plt.axhline(y=limit_min, linestyle='--', linewidth=2)

    plt.title(f'Figure 3: Efficacy of Parallax-Based Veto Filter ({d0:.0f} AU Shell)')
    plt.xlabel('Heliocentric Distance (AU)')
    plt.ylabel(f'Sky-Plane Motion over {dt:g} days (arcsec)')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True, which='both', ls='-', alpha=0.2)
    plt.legend()

    stats = f"Recovery Rate: {recovery:.1f}%\nRejection Rate: {rejection:.1f}%"
    plt.text(0.05, 0.05, stats, transform=plt.gca().transAxes,
             fontsize=12, bbox=dict(facecolor='white', alpha=0.85))
    plt.tight_layout()
    plt.savefig(args.out, dpi=args.dpi, bbox_inches='tight')
    print(f"Saved: {args.out}")

if __name__ == '__main__':
    main()
