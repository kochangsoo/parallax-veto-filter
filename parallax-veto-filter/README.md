# Parallax-Based Veto Filter — Reference Simulation

This repo contains the baseline Monte Carlo simulation code used to illustrate a **shell-conditional parallax veto**
for reducing tracklet-linkage combinatorics in distant Planet Nine searches.

## Install
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```bash
python simulation.py --out figure3_parallax_veto.png --dpi 600
```

## Scope note
This is a controlled baseline (scalar motion + Gaussian noise). End-to-end pipeline usage should use:
- displacement vector (Δα cosδ, Δδ),
- survey geometry (ε, β) and projection factors,
- astrometric covariance for probabilistic acceptance,
- benchmarking against slow backgrounds and spurious detections.
