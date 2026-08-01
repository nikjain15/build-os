# Build OS — Deep Content Audit + Interview + Fix (paste into a fresh chat)

Copy everything below the line into a new Claude Code session started in any folder that can
reach GitHub. It upgrades the current evidence-only scores into content-quality scores, by
auditing deeply, interviewing you, and fixing gaps with you, then publishing the new scorecards
so the live dashboard updates.

---

You are running a **Build OS deep audit** for Nik Jain (GitHub: nikjain15). Read this whole
brief before acting.

## Context

- The hub repo is `nikjain15/build-os`. Read `skill/SKILL.md` (the question bank, grading
  rules in Step 2 and Step 2½, and the section 12 scorecard schema) before anything else.
- `docs/data/scorecards.json` holds the current scores for five products: FounderFirst
  (`founderfirst.one`), RoleOS (`roleos-app`), Pulse (`pulse`), Rally (`rally`), Conduit
  (`conduit`). These were scored by an EVIDENCE audit only: file trees, test counts, eval
  datasets, CI workflows. Nobody has yet judged the CONTENT quality, and `loop_ran` is
  honestly false on all five.
- Your job: replace those evidence-only grades with content-quality grades, close the gaps
  found along the way, and publish updated scorecards. The dashboard at
  nikjain15.github.io/build-os/dashboard reads the data live; recruiters will see it, and
  every claim must stay checkable against the public repos.

## Phase 1 — Deep content audit (one repo at a time, no questions yet)

For each repo, in this order: `conduit`, `pulse`, `rally`, `roleos-app`, `founderfirst.one`:

1. Read the actual content: README, every file in `docs/`, the eval datasets and runners, a
   sample of the test files, and the CI workflows. Quality, not presence.
2. Grade every applicable question from SKILL.md (core questions plus the matching type
   pack) as weak / good / great using the written rubrics. Quote the exact evidence for each
   grade: a file path and the line or passage that earns it. A grade with no quote does not
   count.
3. Apply SKILL.md Step 2½ discipline: probe anything that looks great, never grade above
   good on structure alone, and record the arithmetic.
4. Produce a per-repo findings table: question id, grade, evidence quote, and the single
   change that would move it up one tier.

## Phase 2 — Interview Nik (this is where you ask questions)

For every question Phase 1 could NOT grade from the repo alone (intent, users, kill
criteria, cost reasoning, stakeholders, anything that lives in the builder's head):

- Ask ONE question at a time, in plain English, following SKILL.md Step 2 and Step 3
  (simpler re-phrasing if stuck, third try using the specific project).
- Grade the answer out loud (weak / good / great), say the single change that would raise
  it a tier, and record it.
- Never show the example answer before the first attempt. Probe every great once.
- Keep the session to one repo at a time so it stays focused; confirm before moving to the
  next repo.

## Phase 3 — Fix together

For each finding from Phases 1 and 2, ranked highest-leverage first:

- Propose the concrete fix (a real file: PRD section, ADR, judge-validation script, cost
  ledger) and ask Nik yes/no before writing it.
- On yes, write the artifact into the actual project repo (clone, edit, commit as Nik Jain,
  push). Use the hub's `templates/` skeletons so structure stays consistent.
- After each fix, re-grade the affected question with the new evidence.

## Phase 4 — Publish the new scorecards

1. Rebuild each project's entry for `docs/data/scorecards.json` using the section 12 schema:
   grades map great=9, good=7, weak=4; pillar = average of its questions' values; a pillar
   with no graded questions is null, never a guess; overall = round(mean of non-null
   pillars x 10) with the arithmetic shown in `notes`.
2. Set `loop_ran: true` (this run IS the loop) and harvest any new failure modes into the
   hub's `LEARNINGS.md`.
3. Style rules for every public-facing string (`notes`, `next_focus`): no em-dashes,
   positive and specific tone, lead with what shipped, frame gaps as "next" actions with
   the exact file to create. Recruiters read this.
4. Run `python3 scripts/validate_scorecards.py` in the hub repo; it must pass.
5. Commit and push the hub repo as Nik Jain (no AI co-author lines). The dashboard reads
   raw.githubusercontent.com, so it updates within a minute of the push.

## Rules

- Honesty outranks flattery: a grade the repo cannot back up is worse than a lower grade,
  because everything here is publicly checkable.
- Quote evidence for every grade. "The docs are good" is not a finding.
- One question at a time in Phase 2; wait for the answer; never re-ask what is answered.
- Ask before writing to any repo, and before moving between repos.
- Start now with Phase 1 on `conduit`, and give a time estimate for the full run.
