# Build OS — a self-improving system for shipping excellent AI products

Build OS is an operating system for building AI products with senior-level rigor. On every project
it interviews the builder phase-by-phase, writes production artifacts (PRD, evals, failure-mode
analysis, architecture, cost, safety, decision log) into the repo, grades the work against **nine
craft pillars**, and — the core idea — **improves its own question bank after every build**. This
hub hosts the skill, a live dashboard, and the aggregated scores across all my projects.

## The nine craft pillars
Product Judgment · System Design · Evaluation · Reliability & Ownership · Safety · Economics · Communication · UX/UI & Interaction · Collaboration & Stakeholders

## What's in this repo
```
/skill/SKILL.md            the Build OS itself (the question bank + loop)
/skill/references/         source library the bank is anchored to
/LEARNINGS.md              the loop's memory — harvested failure modes → next questions
/docs/index.html           the GitHub Pages dashboard (radar, trend, cards, heatmap)
/data/scorecards.json      aggregated scores across all my projects (feeds the dashboard)
/data/scorecard.template.json   the per-project schema
```

## How the loop works
1. **Build** a project with the skill (in Claude Code: say `run build os on this repo`). It interviews
   you, writes the full artifact set (13 tracked artifacts), and grades every answer weak/good/great.
2. **Score** — at the end it writes a `scorecard.json` into that project repo and appends the entry to
   this hub's `data/scorecards.json`.
3. **See** — the dashboard renders where you stand on each pillar, your trend over time, per-project
   cards, and a question heatmap of where you keep slipping.
4. **Improve** — new failure modes become new questions (`LEARNINGS.md` → promoted into `SKILL.md`),
   so the next project starts from a sharper bar.

## Turn on the dashboard (GitHub Pages)
1. Push this repo to GitHub (public).
2. Repo **Settings → Pages → Build and deployment → Source: Deploy from a branch**.
3. **Branch: `main`, Folder: `/docs`** → Save.
4. Wait ~1 min; your dashboard is live at `https://<your-handle>.github.io/<repo>/`.
5. The page reads `./data/scorecards.json`. Until you add real projects it shows sample data with a
   banner; replace the sample entries and the banner disappears.

## Adding a project's score
Either let the skill append it automatically at the end of a build, or copy
`data/scorecard.template.json`, fill it in, and add the object to the `projects` array in
`data/scorecards.json`. Keep question `id`s stable (D1, S2, E2, …) so the heatmap tracks the same
question across projects.

## Scoring convention
Each of the nine pillars is 0–10, derived from the graded questions (great ≈ 9–10, good ≈ 6–8, weak ≈ 2–5).
A pillar with no graded questions that project is `null` — a visible gap, never an invented number.
`overall` = round(mean of the non-null pillars × 10), computed (never eyeballed) with the arithmetic
shown in `notes`. Each scorecard also carries `loop_ran` and `projects_since_resource_refresh` so the
self-improving loop is instrumented, not just described. Score honestly — an inflated scorecard
defeats the whole point of the loop.
