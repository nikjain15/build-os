# Build OS

An operating system for building products with senior-level rigor. It interviews the builder
phase-by-phase, writes production artifacts into the project repo, grades the work against nine
craft pillars, and improves its own question bank after every build.

This file is the contributor and agent guidance for **this hub repository**. It is not the skill —
the skill is `skill/SKILL.md`, and it is what runs against other repositories.

## Project structure

```
skill/SKILL.md            the Build OS itself (the question bank + the loop)
skill/references/         the source library the bank is anchored to
templates/                skeletons for every artifact the OS writes
templates/github/         copyable PR template, ci.yml, CLAUDE.md stub, protection.json
GITHUB-STANDARDS.md       the one repo bar every repository is held to
reusable/                 assets extracted from past builds, for reuse in the next one
LEARNINGS.md              the loop's memory: harvested failure modes -> next questions
docs/                     the landing page and the GitHub Pages dashboard
docs/data/scorecards.json aggregated real scores across all projects (feeds the dashboard)
scripts/validate_scorecards.py   schema + formula check, enforced in CI
audit/                    adversarial audit prompts and their outputs
```

## Setup and checks

No install step. The only executable is a stdlib-only Python script:

```bash
python3 scripts/validate_scorecards.py   # schema, pillar set, grades, overall formula
```

CI runs exactly this on every push and pull request, plus a parse check on everything in
`docs/data/`. Run it locally before pushing; do not rely on CI to find a broken scorecard for you.

## Conventions

**Scores are real.** `docs/data/scorecards.json` holds actual grades from actual builds. Never add a
projected, illustrative, or aspirational entry — the dashboard is public, and a made-up number there
is a false claim about work that was not done. If a project has not been graded, it does not appear.

**The overall score is computed, not chosen.** It is `round(mean(non-null pillars) * 10)`. The
validator enforces this. If a number looks wrong, fix the pillar grades, not the total.

**The nine pillars are fixed.** Product Judgment, System Design, Evaluation, Reliability & Ownership,
Safety, Economics, Communication, UX/UI & Interaction, Collaboration & Stakeholders. Adding or
renaming one is a change to the schema, the validator, the template, and every historical scorecard
at once — not a local edit.

**New questions come from real failures.** `LEARNINGS.md` is the staging area: a failure mode
observed in a build is written there first, and only promoted into `skill/SKILL.md` once it has
earned its place. Questions invented in the abstract make the interview longer without making it
sharper.

**Templates keep output consistent.** When the shape of an artifact changes, change
`templates/`, not just the one project that prompted it.

## Pull requests

Follow `GITHUB-STANDARDS.md`, which this repository is held to like any other:

- Branch names are `topic/slug` — `standards/`, `evals/`, `fix/`, `docs/`.
- Commit subjects state the outcome in the imperative, describing what is true about the system
  after the merge rather than which files moved.
- Every change arrives by pull request, including one-line changes. "It's one line" is the exact
  reasoning that precedes the unreviewed push that breaks the dashboard.
- `.github/PULL_REQUEST_TEMPLATE.md` asks for testing and rollback. Fill both in.

## A standing obligation

This repository defines the bar the others are measured against. When it fails one of its own rules,
that is the most important bug in it — a standard its own author does not follow is a suggestion.
The compliance snapshot in `GITHUB-STANDARDS.md` names failures by repository, this one included.
Keep it honest, and keep it current.
