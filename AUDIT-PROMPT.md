# Build OS — Adversarial + Regression Audit Prompt (canonical, version-agnostic)

**This file supersedes any earlier audit prompt.** It audits **whatever SKILL.md version is attached**
— the panel must read the attached file's own `## Changelog` and test THAT version's claims, not the
version this prompt was last edited against. **First check:** if the attached SKILL.md's changelog
lists changes this prompt doesn't cover (new packs, new rules), the panel must still audit them —
and file a P2 to update this prompt.

Paste this into a **fresh Claude session** (or a new Cowork task), attach the current `SKILL.md`
(and, for the lockstep test, `docs/data/scorecards.json`, `docs/data/scorecard.template.json`, and
`docs/index.html`). Run it before publishing or after any edit. A polished OS should survive the panel
with **zero P0/P1 findings and every phase ≥8/10.**

---

## THE PROMPT (copy everything below the line)

---

You are convening an **adversarial + regression review panel** to stress-test the **Build OS** — a
self-improving operating system (version per the attached changelog) that interviews a builder
phase-by-phase in plain English while they build a product (AI or non-AI), writes engineering/product artifacts into their GitHub repo, and scores the
work against **nine craft pillars**: Product Judgment, System Design, Evaluation, Reliability &
Ownership, Safety, Economics, Communication, UX/UI & Interaction, Collaboration & Stakeholders. It also
has a **stakeholder-simulation mode** (role-play a designer, staff engineer, security/legal, data lead,
or GTM lead) and emits a `scorecard.json` that feeds a dashboard. It will be **published open-source**
and must make any expert reviewer conclude the author operates at a senior, production-grade level.

The attached `SKILL.md` is the document under review. **Do not be polite. Do not summarize it back.
Find everything wrong before a real expert does.**

### Step 1 — Convene the panel
Adopt FIVE reviewers in turn. Each reads the WHOLE document through their lens and writes findings in
their own voice. Disagree with each other where you'd genuinely differ.

1. **Frontier-lab hiring manager** (screened 500+ candidates). Does each question + rubric actually
   *discriminate* a strong builder from a bluffer? Flag any question a mediocre candidate could ace.
2. **Staff/principal engineer** (ships production LLM systems). Technical correctness — eval metrics,
   RAG, agents, idempotency, scale, safety, architecture/ADRs, testing. Flag anything an expert would
   wince at or that's outdated for 2026.
3. **Open-source maintainer** (10k-star repos). Will a stranger understand and *use* this unaided?
   Flag leaked private context, unclear instructions, résumé-stuffing, or anything that reads as a
   job-hunt artifact rather than a genuinely useful tool.
4. **Skeptical evals/quality lead**. Is the "self-improving loop" real or decorative? Does every rubric
   have a valid weak/good/great gradient, or is "great" just "good" with more words? Can a project pass
   the coverage matrix with real gaps?
5. **Non-expert career-switcher** (the actual user — smart, motivated, NOT yet fluent in the jargon).
   For each question: could you answer it from the plain wording + the `🤔` fallback + the example
   alone, without googling? Flag every question where the answer is still "no."

### Step 2 — Attack each phase, type pack, and simulation
For EVERY phase (Discovery, Design, Build, Eval, Ship, Retro), EVERY Type Pack listed in the attached
SKILL.md (currently RAG, agent, fine-tune, API, non-AI — trust the file, not this list), and EVERY
stakeholder simulation, apply these tests and quote the exact line:

- **Discrimination:** could a shallow builder give a "great" answer by copying the example without
  understanding? If yes, the question is weak — rewrite it.
- **Rubric gradient:** are weak/good/great genuinely distinct and *observable* (not just confidence or
  length)? Reject fake gradients.
- **Source:** is every "why it matters" claim real, current (2025–2026), and actually supporting the
  point? Flag unsourced, stale, or mis-cited.
- **Artifact:** does the "Creates" target produce something a reviewer would actually open and be
  impressed by? Flag vague artifacts.
- **Correctness:** any technically wrong or oversimplified claim? Give the correct version.
- **Coverage:** any critical question a top team would ask that's missing? Name it.

### Step 2b — v1.2 regression tests (run these IN ADDITION)
1. **Plain-English clarity test.** For every question: (a) is the main wording free of unexplained
   jargon? (b) is there a `🤔` fallback that genuinely re-phrases it more simply (not just repeats it)?
   (c) is there a concrete example a non-expert could act on? Any question failing (a), (b), or (c) is a
   finding. Persona 5 owns this test.
2. **Nine-pillar balance & coverage.** Tally questions per pillar. Flag any pillar that is thin
   (too few discriminating questions to prove it) or bloated. Specifically check the two newest pillars
   — **UX/UI & Interaction** and **Collaboration & Stakeholders** — are they as rigorous as the mature
   pillars, or noticeably weaker? Name the gap and the question to add.
3. **Simulation-mode quality.** For each stakeholder simulation (§9): is the persona specific and tough,
   does it ask real questions, produce ranked findings, and write to a real artifact — or is it generic
   role-play? Flag any simulation that a real designer/engineer/lawyer would find shallow.
4. **Lockstep regression (most important — any drift is P0).** Confirm the pillar list is IDENTICAL in
   all four places: `SKILL.md` (the 9 pillars intro), the `scorecard.json` schema (§12), the coverage
   matrix (§10), and `docs/index.html`'s `PILLARS` array. Confirm the scorecard schema fields and
   question `id`s match what the dashboard reads. Any mismatch silently drops data from the charts —
   report it as **P0** with the exact divergence.
5. **Deployment reality test (P0 if broken).** Trace the dashboard's data path end-to-end AS DEPLOYED:
   `index.html`'s fetch URL, resolved relative to where GitHub Pages actually serves the page, must
   land on the real scorecards file — remember Pages serving from `/docs` publishes ONLY `/docs`.
   Also verify README's setup steps and the SKILL's file paths (§11, §12) all point at files that
   exist in the repo. An audit that only reads prose misses exactly this class of bug.
6. **Version-lockstep of the toolchain itself.** This prompt, the SKILL version, and the README must
   not contradict each other (stale version numbers, stale paths, stale artifact counts). Any
   contradiction is at least P1.

### Step 3 — Score and prioritize
- Score each of the 6 phases, 4 type packs, and the simulation mode **/10** with a one-line reason.
- Produce a single **prioritized findings table**: `ID | Severity (P0 blocker / P1 major / P2 minor) |
  Location (quote) | Problem | Concrete fix`, most-severe first, fixes unambiguous.
- List the **3 highest-leverage rewrites** that would most raise credibility, in full.
- Name any **missing question or pillar gap** (especially in the two new pillars) to make this
  best-in-class.
- Verdict: seeing a repo built with this OS, would each of the five personas conclude the author is
  genuinely excellent? **Yes / With reservations / No** — one reason each. Persona 5's verdict is
  specifically: "could I, a non-expert, actually complete a project with this without getting stuck?"

### Rules
- Quote exact lines; never hand-wave. "Some rubrics are weak" is useless — name them.
- Prefer surgical fixes over praise. If something is strong, say so in one line and move on.
- Do not rewrite the whole document; give the findings table + the 3 rewrites in full.
- If you can't verify a technical claim, say "unverified — check X" rather than guessing.

---

## How to use the output
1. Apply all **P0** and **P1** fixes (P0 lockstep drift first — it silently breaks the dashboard).
2. Add any missing question / close any thin-pillar gap the panel named.
3. Bump the `## Changelog` version (e.g., v1.2 → v1.3) noting what the audit changed.
4. Re-run this prompt. Target: **zero P0/P1 findings and every phase ≥8/10** before publishing.
5. Feed any *new* failure mode into `LEARNINGS.md` — the audit is itself part of the self-improving loop.

---

## GATED NEXT STEP — build/refresh the dashboard (run ONLY after step 4 passes)

Do not run this until the panel returns **zero P0/P1 findings and every phase ≥8/10.** A dashboard built
on an unhardened OS just visualizes noise. Once it passes, paste the prompt below.

---

You are finalizing the **Build OS hub repo** so it publishes a GitHub Pages dashboard that tracks the
builder's craft level over time. `SKILL.md` (v1.2, nine pillars) has passed its adversarial + regression
audit. Do the following:
1. **Confirm the nine-pillar set** is identical in `SKILL.md`, the dashboard's `PILLARS` array, the
   `scorecard.json` schema (§12), and the coverage matrix (§10). If the audit renamed/added a pillar,
   update all four together — a mismatch silently drops data. (This is the P0 lockstep rule.)
2. **Verify the scorecard schema** (§12) is complete: `project, title, date, type, overall, pillars{9},
   artifacts{13}, questions[{id,phase,label,pillars,grade}], notes, weakest_pillar, next_focus`. Ensure
   every question in the bank has a stable `id` and a short `label` the heatmap can display.
3. **Regenerate `/docs/index.html`** if the pillar set or schema changed, keeping all four views:
   9-spoke current-level radar, improvement-over-time trend, per-project scorecards, and a question
   heatmap whose rows derive from the scorecard `label`s. Keep it one self-contained file that reads
   `./data/scorecards.json` with an embedded sample-data fallback so it renders locally and on Pages.
4. **Update `/docs/data/scorecard.template.json`** and the README scoring convention to match nine pillars.
5. **Re-aggregate `/docs/data/scorecards.json`** from all existing project scorecards.
6. Output: the updated files + a one-paragraph note on exactly what changed and why, plus the Pages URL
   to expect once pushed.

Rule: the SKILL, the scorecard schema, the coverage matrix, and the dashboard must ALWAYS agree on the
nine pillars and the question ids. Treat any drift as a P0 bug.

---

After this step, commit, push, and confirm the dashboard renders your real projects (not the sample
banner). Then you have the full loop: **build → score → see → improve.**
