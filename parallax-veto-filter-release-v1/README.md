# Parallax-Based Veto Filter — Reference Simulation

This repository contains baseline code used in the associated manuscript to demonstrate a
shell-conditional parallax veto for reducing tracklet-linkage combinatorics in distant Planet Nine searches.

## Install
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 1) Baseline Monte Carlo (Figure 3)
```bash
python simulation.py --out figure3_parallax_veto.png --dpi 600
```

## 2) Dirty-data stress test (Figure 4 candidate; Option A, unit-consistent)
This test models spurious tracklets as **total sky-plane displacement over the baseline** (arcsec over 2 days),
drawn from a wide uniform distribution.

```bash
python stress_test.py --out figure4_spurious_tracklets_hist.png --dpi 600
```

The script prints the pass fraction `f_bg` and rejection rate. In the manuscript, the default settings yield
`f_bg = 0.0064` (32/5000) and a rejection rate of 99.36%.

## License
MIT (see LICENSE).
