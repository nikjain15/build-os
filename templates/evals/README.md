# /evals — <product name>

- `dataset/` — golden set (E1): origin, versioning, held-out split. Non-AI: end-to-end test specs.
- `judge/` — judge prompt + validation vs human labels (E2): report κ / per-class rates, not raw agreement.
- `ci/` — the gate (E5): what blocks a merge; every production bug becomes a permanent case.
- `REVIEW.md` — §9 data-review sim findings.
