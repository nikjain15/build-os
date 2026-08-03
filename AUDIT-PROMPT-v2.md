# Build OS craft audit: continuation brief

You are continuing a Build OS craft audit for Nik Jain (GitHub: `nikjain15`). Read this whole
brief before acting. Everything in it was verified on 2026-08-02, not remembered.

## What exists

Five public product repos, all pushed and green: `conduit`, `pulse`, `rally`, `roleos-app`,
`founderfirst.one`.

The hub is `nikjain15/build-os`. Scores live in `docs/data/scorecards.json` and render at
nikjain15.github.io/build-os/dashboard, which reads the raw GitHub file, so a push is live
within a minute. `skill/SKILL.md` holds the question bank and grading rules.
`scripts/validate_scorecards.py` must pass before any scorecard push. **There is no generator
script** despite what an older brief said; scorecards are hand-maintained against SKILL.md §12,
so recompute pillars programmatically from the questions rather than editing numbers by hand.

Verified heads at handoff: conduit `2d787cb`, pulse `2c51775`, rally `7fcb369`, roleos-app
`8cac2f8`, founderfirst.one `5e841f0`, build-os `0e695f5`. Local clones under
`~/github-profile-build/` are **stale**; clone fresh.

Current scores, 169 questions, 47 great / 111 good / 11 weak:

| Product | Score | Weakest pillar |
|---|---|---|
| Pulse | 81 | System Design |
| FounderFirst | 77 | Evaluation |
| RoleOS | 76 | Evaluation |
| Rally | 76 | Evaluation |
| Conduit | 76 | Communication |

## Non-negotiable standards

Each exists because breaking it produced a real defect that had to be corrected publicly.

1. **Verify, never trust a report.** Run the repo's own checks and read the code before grading
   anything up. Grep for call sites before writing "enforced".
2. **Assert your edits landed.** A find-and-replace must assert the pattern matched, and the
   file must be re-read from disk afterwards. In this session a scorecard script computed a
   change and never wrote it, and the validator passed on unchanged content. Diff, do not trust
   an "OK" line.
3. **Check whether a file is generated before editing it.** FounderFirst's
   `supabase/functions/_shared/inference/core.ts` is a mirror of `packages/inference/src/`;
   editing it directly would have failed `pnpm check:vendor`. Caught before commit, but only
   because it was checked.
4. **A claim the code does not back is worse than a low grade.** Correct overclaims in place and
   leave the correction visible.
5. **Never invent a number.** No threshold nobody measured. If it cannot be measured yet, say so
   and name what would measure it.
6. **Floors below what was measured, in the same commit as the run that justifies them.**
7. **Prose style:** no em-dashes anywhere. No AI co-author lines in commits. Lead with what
   shipped; frame gaps as next actions naming the exact file.
8. **Grading discipline (SKILL.md Step 2.5):** great only when the evidence survives a probe.
   Structure alone caps at good. Show pillar arithmetic in `notes`. A pillar with no graded
   questions is null, never a guess.
9. **Never accept a credential in chat.** Nik pasted an API key in the previous session; it was
   refused and he was told to revoke it. **Confirm he did.** If he pastes another, refuse again
   and give him the command to run himself.

## The work, ranked by measured point value

Point values are computed from the current grades, not estimated. Reaching 90 on all five needs
**64.7 points total**.

### The single highest-value item, and it is not yours to do

**S1, cost. Worth 10.3 points across four repos** (Rally +4.0, FounderFirst +2.2, RoleOS +2.1,
Conduit +2.0) **and blocked entirely on one keyed run.**

All four now have `docs/COST.md` and a `scripts/cost-model.mjs` that reads prices from source.
S1's great tier is a four-part conjunct and only one part is missing:

| | tested cheaper model | cost at volume | caching | routed | S1 |
|---|---|---|---|---|---|
| Rally | **no** | yes | yes | yes | good |
| RoleOS | **no** | yes | no (documented) | yes | good |
| Conduit | **no** | yes | no (D11, deliberate) | yes | good |
| FounderFirst | **no** | yes | no | yes | good |
| Pulse | yes | yes | yes | yes | **great** |

Ask Nik to run one keyed eval per repo comparing the cheap tier against the tier above on that
repo's own examples, then record the result. Do not grade S1 up without it.

### What you can do without any credential

**AG2, stop conditions. +4.1** (RoleOS +2.1, Conduit +2.0). Great needs layered limits: max
steps **and** a token/cost budget **and** loop detection (same state twice halts), each with a
defined "what the user sees" when it trips. Pure engineering.

**E3, hostile inputs. +5.7** (FounderFirst, Pulse, Rally +1.5 each, RoleOS +1.2). Great needs
systematic obviously-wrong, ambiguous and unexpectedly-hard inputs, with a before/after and the
exact fix per break.

**GEN1 performance budget (RoleOS +1.4), GEN2 migrations and rollback (FounderFirst +0.9, RoleOS
+0.8), SH6 accessibility (RoleOS +1.1), API3 breaking-change policy (Conduit +0.9, currently the
only weak there), SH9 retention (Pulse +0.8).**

**E-series evals** across repos: E1 golden set, E4 per-step, E5 regression gate, roughly +0.7 to
+0.8 each.

**E2 judge validation.** Weak only on Rally now (+0.8). Pulse's harness landed this session and
is the template: `pulse/evals/judge-metrics.ts`, `judge-validation-dataset.json`,
`run-judge-validation.ts`. Conduit's is the older reference. Method that matters: binary verdicts
graded separately, class-balanced so an always-pass judge scores zero, Cohen's kappa against a
0.6 floor reported next to raw agreement and both per-class rates, and only the model-and-
dimension pairs the repo actually claims are enforced.

### The biggest lever, and it needs Nik first

**S4, screen states. +15.3 across all five** (Pulse +3.9, FounderFirst +3.8, Conduit +3.7, Rally
+2.3, RoleOS +1.6). Great requires all four states genuinely designed and shipped (empty,
loading, error, success), plus streaming or progressive output while waiting, plus a visible
"check this" treatment when the model is unsure.

**Prerequisite: ask Nik whether each app can detect low confidence today.** The "unsure"
treatment needs a confidence signal to hang on. If one does not exist, that is the first task,
not the last.

### Documentation-shaped, do these last

**SH5, sign-off dates. +9.4 across all five.** Great needs each sign-off named, an owner, and a
dated plan. **Needs Nik's actual dates.** Do this after S4 and S1 so the score never runs ahead
of the product.

**D1, name the real user. +5.0 across four.** Great needs one specific group, the job they are
doing, and the exact messy input that breaks v1. **Needs Nik**; guessing this is worthless.

## State of the estate, verified 2026-08-02

**Advisories:** Conduit **none**. Pulse 1 moderate. Rally 2 moderate. RoleOS 2 high. FounderFirst
1 high, 3 moderate, 5 low.

- RoleOS's two highs are `sharp` via `miniflare` inside `wrangler`, **dev-only**, in two private
  sandbox spike packages, not in the deployed worker. Deliberately ungated and printed on every
  gate run so the count reconciles with Dependabot. Do not "fix" this without reading
  `docs/DECISION_LOG.md`.
- FounderFirst's high is `react-router` GHSA-qwww-vcr4-c8h2, allowlisted to 2026-10-31 because
  the fix needs React 19. Its falsifiable check: grep `apps/app/src` and `apps/admin/src` for
  `unstable_` or `/rsc`; it must return nothing. Re-verified clean this session.
- FounderFirst's remaining 8 are all `torch` in `tools/tts-server`. `chatterbox-tts==0.1.1`
  hard-pins `torch==2.6.0`, confirmed against PyPI metadata directly. Closing this means
  replacing or forking Chatterbox: **a product decision for Nik, not a security patch.** Three
  allowlist entries expire 2026-09-15 and CI goes red by design after that.

**Branch protection is now real on all five**, `enforce_admins: true`, verified by pushing an
empty commit and being rejected. Required checks: conduit 2, pulse 3, rally 3, roleos-app 3,
founderfirst.one 7. The hub `build-os` is deliberately unprotected: it has no workflows, so
requiring checks would recreate the trap FounderFirst was in.

**Every PR merges normally now.** No admin override needed anywhere.

## Blocked on Nik, do not fake these

- **The keyed eval run.** 10.3 points. Highest value item available.
- **Confirm the pasted API key was revoked.**
- **90-second walkthroughs (SH4, +3.9 total).** Conduit's README still has an empty
  `<!-- DEMO_GIF -->` placeholder at line 14 and that alone is why Communication is its weakest
  pillar. Conduit's console is public at `nikjain15.github.io/conduit` against a mock gateway, so
  a silent GIF can be recorded with no login. The other four need him signed in with the tab
  open; **you cannot type credentials into a login form.**
- **Time to first success (API2).** Needs three real people and a stopwatch. A cold-start run by
  you is a labelled n=1 proxy at best.
- **Kill criteria (R1) and sign-off dates (SH5).** Offer two or three options tied to an
  instrumented metric and let him choose. Never invent a threshold.
- **RoleOS live retrieval.** `evals/retrieval/live/capture.ts` needs `SUPABASE_SERVICE_ROLE_KEY`,
  `NEXT_PUBLIC_SUPABASE_URL`, `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_API_TOKEN`. It is read-only.
  He runs it; it writes `dataset.semantic.json`. Until then the CI retrieval SLA scores a TF-IDF
  stand-in, not the bge and pgvector retriever that ships.

## Closed in the previous session, do not redo

- **Supply chain across all five.** Pulse and Rally's "unfixable" advisories were fixed with npm
  `overrides` (nobody had tried it). RoleOS's audit gate now covers all three lockfiles.
  FounderFirst's gate had two defects fixed: R5 reported live allowlist entries as stale and told
  you to delete them, and a `setuptools<81` ceiling hid a real advisory. Conduit's Dependabot was
  switched on and all ten advisories, including two critical, were cleared.
- **Branch protection on all five**, including diagnosing that FounderFirst required two check
  names (`Vitest`, `pgTAP`) that no workflow can ever produce.
- **Judge validation (E2) on Pulse**, plus fixing an eval that had never run
  (`ERR_MODULE_NOT_FOUND` on every invocation, unnoticed because no CI job ran any eval script).
- **Cost models on Rally, RoleOS, Conduit, FounderFirst.** Pulse already had one.
- **A 3x pricing error.** Rally and FounderFirst both shipped Opus at $15/$75, which is
  Opus-3-era pricing, feeding live cost meters. Conduit billed unpriced models at **zero**. Pulse
  and RoleOS were correct. All fixed, with tests.
- **torch on kokoro-server:** 2.6.0 to 2.13.0, deployed and verified by rendering the same
  sentence before and after through the shipped `_render_mp3`.

## Known open items worth carrying

- **Nothing alerts on anything, in any repo.** Thresholds are computed in several; no
  notification channel exists anywhere. Each says so in a test. Keep it that way until one is
  built.
- **Rally and Pulse retention sweeps** are written and enforced but nothing runs them on a
  schedule.
- **Every cost figure is an estimate.** Prices are now correct and read from source, but token
  counts use a characters/4 approximation. Each script says so in its own output. One
  `count_tokens` call per repo replaces them.

## How to work

Ask before writing to any repo. Work in fresh clones. Batch by theme across repos rather than
finishing one repo at a time, since each theme lifts the same question in five places. Open PRs
rather than pushing to main; protection is real now and every repo merges cleanly. Run each
repo's own checks before committing and say plainly which you ran and which you could not. The
GitHub API secondary rate limit triggers easily: check CI once after a sensible wait rather than
polling.

**After each piece of work, re-score before moving on:**

1. Re-read the relevant tier in `skill/SKILL.md` and grade against the sentence it actually
   asks for, not the spirit of it. S1 is a four-part conjunct; missing one part means good.
2. Update `docs/data/scorecards.json`, recomputing every pillar from its questions
   programmatically. Never hand-edit a pillar number.
3. Run `python3 scripts/validate_scorecards.py`, then **independently recompute** and re-read
   the file from disk.
4. Push, wait, and `curl` the raw published JSON to confirm the dashboard sees it.
5. **If the grade did not move, say so plainly and explain why.** That happened this session:
   four cost models, three pricing bugs fixed, and zero points, because the one part of S1 that
   was missing needs an API key. Recording that honestly is the entire value of the dashboard.

## The ceiling, state it honestly if asked

Completing everything above lands around 90. Reaching 95 needs production evidence that does not
exist: a kill line honestly checked against real data, golden sets grown from real production
failures rather than invented cases, and metrics instrumented before launch. Those need traffic,
not engineering. Do not close that gap by grading more generously; the entire value of this
dashboard is that every grade is checkable against a public repo.

## Start here

Confirm the current state still matches this brief, then propose an order and begin. The
recommended first move is **AG2 on RoleOS and Conduit** (+4.1, needs nothing from Nik), while
asking him in parallel for the keyed eval run (+10.3) and whether each app can currently detect
low model confidence (the S4 prerequisite, +15.3).
