# Build OS v1.2 — Adversarial + Regression Audit Report

**Date:** 2026-07-31 · **Files reviewed:** `skill/SKILL.md` (v1.2), `skill/references/SOURCES.md`, `data/scorecards.json`, `data/scorecard.template.json`, `docs/index.html`, `README.md`
**Verdict up front:** the audit target (zero P0/P1, every phase ≥8/10) is **NOT met**. 2 P0s, 8 P1s, 12 P2s, 3 P3s after reconciling with the v1.1 audit (see Addendum). The gated dashboard step must NOT run yet. The good news: the core six phases are genuinely strong — most of the damage is concentrated in the type packs, the scoring pipeline, and 7→9-pillar migration debt.

---

## Step 1 — The panel

### Persona 1 · Frontier-lab hiring manager

The core bank discriminates better than 90% of "AI PM interview prep" content I've seen. D1's great-tier ("one specific group, the job they're doing, and the exact messy input that breaks v1") is a real senior filter — bluffers name a persona, seniors name the input that breaks v1. B4 (idempotency), S5 (backoff/breaker/fallback), E2 (judge validation) are questions mediocre candidates reliably fail.

But the whole bank ships with the answer key stapled to it. Every question carries "📝 Example of a strong answer" and nothing in §0 forbids surfacing it before the builder answers. Step 3 implies the example is a stuck-rescue, but Step 2 doesn't say "withhold it," and the SKILL.md is public — a shallow builder reads the file once and pattern-matches "great" on every question. D2 is worst: the 🤔 line hands over a fill-in-the-blank template ("When ___ happens, help me ___ so I can ___") — anyone can mad-lib that to a "good," and the 📝 example shows exactly how to reach "great." S6 has the same problem: the example ("Okay: ≥85% task success. Delight: ≥95%… Never ship: any wrong refund promise") IS the answer with two numbers swapped.

Second: nothing instructs the grader to probe. A real interviewer drills into any suspiciously polished answer. There is no rule like "on a 'great,' ask one follow-up; if it collapses, downgrade." Self-graded + answer-visible + no probe = a scorecard I can't trust from the outside.

Questions a mediocre candidate could ace as written: **D2, S6, B3** (the example fully specifies the shape). Questions that still discriminate even with the example visible: D1, D5, S2, S3, B1, B4, E1, E2, E3, SH1, SH2, R1 — the majority, which is why this is fixable rather than fatal.

### Persona 2 · Staff/principal engineer

Content-level: mostly correct and current. S5's ladder (jittered backoff → retry cap → provider failover → breaker → cached/template fallback) is right. B4's "the safety lives below the model" is exactly the correct framing for idempotency. SH1 correctly treats prompt injection as a data/instruction separation problem, not a "tell the model to be careful" problem, and OWASP LLM01 is the right citation. S8 (prompts as versioned, eval-gated, canaried code) is the 2026 standard.

Where I wince:

1. **E2's own "great" example sets a bar an expert would reject.** "validated against 50 human labels (they agree ~80%)" — 80% raw agreement with no chance-corrected measure is weak. If 80% of your outputs are good, a judge that always says "pass" hits 80% agreement while being useless. The example should demand agreement well above the base rate (report Cohen's κ or at least the confusion matrix, target ~90%+ raw / κ≥0.7) — otherwise the OS's flagship "validate your judge" question teaches a bad target number.
2. **S1 anchors on "GPT-4o" as the frontier default** ("Weak: 'GPT-4o, it's best'" / example built on 4o vs 4o-mini pricing). In 2026 this reads dated on arrival and will rot further. The question should be model-agnostic ("your frontier default vs your small model"), with the example marked as illustrative pricing.
3. **RAG2's parenthetical defines recall/precision loosely but acceptably; RAG3 ("How do you cut documents into pieces") files its output under `docs/COST.md §Chunking test`** — chunking evaluation is a retrieval-quality concern; putting it in COST.md is a category error (it belongs in ARCHITECTURE.md §Retrieval or /evals/retrieval/).
4. **The engineering pipeline of the OS itself has the exact "silent drift" bugs the OS preaches against** — see the lockstep section. An OS whose §12 formula is violated by its own shipped sample, and whose dashboard drops the two newest pillars from the trend chart, undermines the author's reliability pillar more than any missing question would.
5. Unverified sources: "TianPan idempotency in LLM pipelines" and "Statsig provider fallbacks" — plausible but niche; the claims they support are correct regardless. "MarkTechPost" as the source for "explaining value plainly is weighted as heavily as coding at top teams" (SH4) is a content-farm citation for a strong claim — unverified, replace or soften.

### Persona 3 · Open-source maintainer

A stranger cannot run the advertised loop. Three breaks:

1. **`~/build-os/LEARNINGS.md` and `~/build-os/reusable/` (R2, R3, §11) are machine-local home-directory paths.** They're outside any repo, unversioned, invisible to the public, and won't exist on a stranger's machine. Meanwhile README.md says "`LEARNINGS.md` → promoted into `SKILL.md`" as if it lives in the hub — and no LEARNINGS.md exists anywhere in this repo. The self-improving loop — the headline claim — has no canonical, versioned home. Pick one: `hub-repo/LEARNINGS.md`, reference it identically in §11, R2, R3, and README, and ship at least a stub so the file exists.
2. **First-person leakage.** The frontmatter description ("When I start a new GitHub project…"), §11's title ("what makes this MY OS"), and the trigger phrase "run my build OS" are the author talking to their own Claude. Fine for a personal skill; for open publishing, rewrite in second person ("interviews you…") or the first stranger who installs it reads someone else's diary.
3. **It smells like a job-hunt artifact.** Ten-plus citations are interview-prep properties: "Exponent" ×6, "(IGotAnOffer/Meta)", "Nika" ×4, plus SOURCES.md's whole first section being job descriptions and interview guides. The tool is genuinely useful, but a maintainer reading "top coding interviews score exactly this" (B1) and "product interviews score this 'human delta'" (D6) concludes it's interview prep wearing a tool costume. Reframe the "why it matters" lines around production outcomes, keep the interview guides in SOURCES.md if you must, and the same content reads as craft rather than audition.
4. Practical gap: §12 says "append/update the entry in the hub's `data/scorecards.json`" — from inside a *different* project repo. Where is the hub? No path, no env var, no config convention. A stranger's run ends with "I couldn't find your hub." Specify the mechanism (e.g. a `BUILD_OS_HUB` path in the skill config, or "paste this JSON into your hub" as fallback).
5. README says the skill "writes the 9 artifacts" — the schema tracks 13. Stale count, likely 7-pillar-era debt.

### Persona 4 · Skeptical evals/quality lead

Is the self-improving loop real? **Half real.** Harvest→append→promote→prune (§11) is concrete, has a promotion threshold ("2+ projects"), a pruning rule ("never discriminates → demote"), and a versioning discipline. That's more real than 95% of "self-improving" claims. But:

1. **The loop's measurement layer can't be trusted yet.** The only integrity control is "Be honest" (§12). The answer key is visible (see Persona 1), the grader is the same model that's being asked to make its owner look senior, and — the smoking gun — **the shipped sample data already violates its own formula**: invoice-reconciler's pillars sum to 75, so `overall = round(mean×10) = 83`, but both `data/scorecards.json` and the embedded SAMPLE say `"overall": 85`. The very first artifact of the loop is inflated by 2 points. (rag-notes: 57✓, support-triage: 70✓ — only the best project is inflated, which is exactly the direction dishonest drift goes.)
2. **Economics is a ghost pillar.** §12 says "average a pillar's questions" — but zero core questions are tagged `[Economics]`. Tally across all 47 tagged questions: Product Judgment 11, System Design 11, Evaluation 9, Reliability & Ownership 9, Communication 5, Safety 4, **UX/UI & Interaction 2 (only 1 core), Collaboration & Stakeholders 2, Economics 1 (FT1 — fine-tune pack only)**. S1 — the cost question, which literally creates COST.md — is tagged `[Product Judgment][System Design]`. So on any non-fine-tune project, the Economics score in the scorecard is derived from **nothing**. The dashboard has been charting an invented number for a pillar. This is a P0: the scoring spec divides by zero and the samples paper over it.
3. **Fake-gradient check.** Core-phase rubrics mostly pass: weak/good/great are behaviorally distinct (D1: "general users" → group+case → group+job+breaking input; B4: "tell the model not to" → dedupe-by-ID → idempotency key below the model). Two soft spots: R1's "Good: a vague hope" is not an observable tier — it's a joke, and gives the grader nothing between weak and great; D3's good→great gap ("one target group" vs "+ explicit not-yet list") is thin — the 🤔 line already prompts for the not-yet list, so the fallback path leads straight to great.
4. **Ten questions have no "Good" tier at all** (D6, S7, S8, B5, E4, E5, SH6, SH7 — plus core R2 and R3), yet §12 grades every answered question `weak|good|great`. The grader must invent the middle tier ~21% of the time. Either define Good everywhere or declare [A] questions binary and map them into the score explicitly.
5. **Coverage matrix is passable-with-gaps by design:** "confirm each of the nine pillars has ≥1 artifact proving it." One artifact ≥ exists is a low bar — UX/UI passes with a UX.md that has one state described. Tie the matrix to grades ("≥1 core question graded good+"), not file existence.

### Persona 5 · Non-expert career-switcher

The six core phases are the best plain-English technical interviewing I've seen — I could answer **every core-phase question** from the wording + 🤔 + example alone. B4's 🤔 ("your 'send refund' fires twice. How do you guarantee the refund only goes out once?") teaches idempotency without saying idempotency until the payoff line. SH1 does the same for prompt injection. The "third way using MY specific project" rule in §0 Step 3 is exactly what I need.

Then I hit the type packs and the floor disappears. **RAG2, RAG3, AG1, AG2, AG3, FT1, FT2, API1, API2 have no 🤔 fallback, no example, and no rubric at all** (RAG1 has a 🤔 line only). "What does your model's 'nutrition label' say" (FT2) — I don't know what goes on a model card beyond the parenthetical. "How do you cut documents into pieces" (RAG3) — into how big? by what? how would I "test that choice"? I'd stall exactly where the OS promised "never leave me stuck." The rule in §0 Step 3 is global, so a good Claude might improvise a rescue — but v1.2's own standard (§1 format) says every question carries the fallback, and 12 of 47 don't.

One more: the packs are where my project type actually lives. If I'm building a RAG app, the questions most specific to my build are the ones with the least support. That's backwards.

---

## Step 2b — v1.2 regression tests

**1. Plain-English clarity:** core phases pass (a), (b), (c) almost universally. FAIL: all 12 type-pack questions (see table F6); RAG4/AG4/FT2/API2 additionally lack sources.

**2. Nine-pillar balance (tally: all-tags / core-only):** PJ 11/9 · SD 11/8 · Eval 9/6 · R&O 9/8 · Comm 5/5 · Safety 4/3 · **UX 2/1 · Collab 2/2 · Economics 1/0**. The two newest pillars are measurably weaker than the mature ones: UX/UI's only core question is S4 (states); accessibility (SH6) is advanced and may never fire, yet the coverage matrix demands "UX.md (states + accessibility)." Collaboration has exactly two questions, both of which a solo builder can answer hypothetically. Economics is a ghost (P0, above). Named gaps + questions to add: see "Missing questions" below.

**3. Simulation-mode quality:** better than generic role-play — each persona has a named attack surface and a real artifact target, and "quote the actual work" is the right instruction. Three gaps: (a) the sim ranks P1/P2/P3 while this audit and the skill's own culture use P0/P1/P2 — two severity scales in one system; (b) "Research / data review … → writes `/evals/` notes" is the one vague artifact ("notes" is not a file — every other sim writes a named section); (c) no exit criteria — a sim could end after one soft question and still count as run. Add: "minimum 5 findings or an explicit 'clean pass', and state what you did NOT review."

**4. Lockstep regression:** the four canonical pillar lists **match exactly** (SKILL intro = §10 matrix = §12 schema = `PILLARS` array = template = data). But three adjacent lockstep breaks:

- `docs/index.html` line 49: `"How I'm doing across the seven craft pillars"` — **seven**. 7-pillar-era text on the public dashboard header.
- `docs/index.html` trend chart: `const cols=['#7c9cff','#48c78e','#c58bff','#f6c453','#ff6b6b','#5ad1e0','#e08bd0']` — **7 colors for 9 pillars**. `cols[7]` and `cols[8]` are `undefined`, so the two v1.2 pillars (UX/UI & Interaction, Collaboration & Stakeholders) draw with Chart.js's default near-invisible fallback. The chart *silently drops the two newest pillars* — the literal failure mode the P0 lockstep rule exists to catch.
- `artifacts` key drift: schema (§12) and template carry 13 keys including `"adr"`; **all three** entries in `data/scorecards.json` and all three SAMPLE projects in index.html carry 12 — `"adr"` missing. Hub `questions` also carry only `{id,label,grade}` vs the schema's `{id,phase,label,pillars,grade}`.

---

## Step 3 — Scores

| Unit | /10 | One-line reason |
|---|---|---|
| Discovery | 8 | Most discriminating phase; D2's fill-in-the-blank 🤔 and D3's thin good→great gap are the only soft spots. |
| Design | 8 | Strongest content (S2/S3/S5/S8 are senior-grade); carries the Economics mis-tag and a dating GPT-4o anchor. |
| Build | 8 | B1–B4 are real production probes; B3's "deployed this week with a URL" is the right forcing function. |
| Eval | 8 | Right architecture (golden set → judge validation → decomposition → gate); E2's own example blesses a weak 80% bar. |
| Ship | 7 | SH1–SH3 strong; pillar coverage leans on two [A] questions (SH6/SH7) that may never fire; SH4's video artifact is unverifiable by the OS. |
| Retro | 7 | Right idea; R1's "Good: a vague hope" is a non-tier, R2/R3 write to machine-local paths, loop storage contradicts README. |
| RAG pack | 6 | Right questions (RAG1/RAG4 decomposition is correct doctrine), ungradeable format — no rubrics, one 🤔 in four. |
| Agent pack | 6 | AG1–AG3 content is exactly right (Anthropic/OpenAI doctrine); same format collapse; no rubric to grade against. |
| Fine-tune pack | 5 | Two questions; FT2's MODEL_CARD.md isn't in the artifact schema, coverage matrix, or skeleton — untracked deliverable. |
| API pack | 5 | Thinnest; no versioning/breaking-changes, no auth/rate-limits, no deprecation question — the things API builders actually get wrong. |
| Simulation mode | 7 | Specific personas + ranked findings + artifact writes = real; needs exit criteria, one concrete artifact fix, one severity scale. |

**Target check: FAILS.** Ship 7, Retro 7, all four packs <8, plus 2 P0 / 7 P1 findings below.

---

## Prioritized findings table

| ID | Sev | Location (quote) | Problem | Concrete fix |
|---|---|---|---|---|
| F1 | **P0** | SKILL §12 "average a pillar's questions" vs S1 tag `` `[Product Judgment][System Design]` ``; grep confirms `[Economics]` appears on FT1 only | Economics has **zero core questions**. On any non-fine-tune project the pillar score is derived from nothing; samples chart invented numbers (rag-notes Economics 6 with no Economics question asked). | Retag S1 `[Economics][System Design]`; tag RAG3 `[Economics]` too if it stays in COST.md. Add to §12: "A pillar with no graded questions this project is scored `null` and rendered as a gap — never invent a number." Update dashboard to skip nulls. |
| F2 | **P0** | index.html: `const cols=['#7c9cff','#48c78e','#c58bff','#f6c453','#ff6b6b','#5ad1e0','#e08bd0']` then `PILLARS.forEach((p,i)=>…borderColor:cols[i]…)` | 7 colors, 9 pillars → `cols[7]`, `cols[8]` undefined → **UX/UI & Interaction and Collaboration & Stakeholders silently vanish from the trend chart**. Lockstep drift in the dashboard, the exact P0 class. | Add two colors (e.g. `'#f19a6d','#8be3c2'`) or use `cols[i % cols.length]` with 9 entries. Add a startup assert: `if(cols.length<PILLARS.length) banner("pillar/color drift")`. |
| F3 | P1 | index.html line 49: `"How I'm doing across the seven craft pillars"` | Public dashboard header still says **seven** pillars — v1.0-era text contradicting everything else on the page. | Change to "nine craft pillars" — or make it dynamic: `` `across the ${PILLARS.length} craft pillars` ``. |
| F4 | P1 | `data/scorecards.json`: invoice-reconciler `"overall": 85` but pillars sum 75 → round(75/9×10) = **83**; same in index.html SAMPLE | Shipped sample violates §12's own formula — and only on the best-scoring project. The loop's first artifact is inflated; a skeptical reviewer finds this in 5 minutes with a calculator. | Set to 83 in both files. Better: make §12 require showing the arithmetic in `notes`, and have the dashboard recompute overall from pillars, flagging any mismatch. |
| F5 | P1 | Schema/template `artifacts` = 13 keys incl. `"adr"`; all 3 hub entries and all 3 SAMPLE entries = 12 keys, no `"adr"` | Hub data and embedded sample lag the schema — the adr chip never renders, and any consumer validating against the template rejects the hub file. | Add `"adr": true/false` to all six project objects (both files). |
| F6 | P1 | §8, all packs — e.g. RAG3 `**How do you cut documents into pieces…**` and FT2, with no `Weak/Good/Great`, no `🤔`, no `📝` (12 of 47 questions; only RAG1 has even a 🤔) | Type packs violate every v1.2 rule: ungradeable (no rubric → grades feeding the scorecard are improvised) and stuck-prone (no fallback for the non-expert) — on exactly the questions most specific to the builder's project type. | Rewrite all four packs in the §1 format. Full RAG pack rewrite provided below (Rewrite #2); replicate the pattern for AG/FT/API. |
| F7 | P1 | Tally: UX/UI core = S4 only (SH6 is `[A]`); Collab = D5 + SH5; §10 demands "UX.md (states + accessibility)" | The two v1.2 pillars are provably thinner than mature pillars; UX's accessibility evidence comes from a question that may never be asked, so the coverage matrix can't be honestly ticked. | Promote SH6 to `[C]` for any product with a UI, and add one core UX question + one core Collab question (named in "Missing questions" below). |
| F8 | P1 | R2 `📄 Creates: ~/build-os/reusable/`; R3/§11 `~/build-os/LEARNINGS.md`; README: "`LEARNINGS.md` → promoted into `SKILL.md`"; no LEARNINGS.md exists in the hub | The self-improving loop — the headline claim — writes to machine-local, unversioned paths that contradict the README and don't exist for any stranger. The loop is unverifiable in public. | Canonical home: `LEARNINGS.md` at hub root. Update §11 step 2, R2, R3, and README to the same path; commit a stub with the schema line so the file exists on day one. |
| F9 | P1 | §1 block includes "📝 Example of a strong answer" for every question; §0 Step 2 never says to withhold it; no probe rule anywhere | The answer key ships with the test: pattern-matching the visible example yields "great" grades (worst: D2, S6, B3). Self-graded scores then feed a public credibility dashboard. | Add grading-integrity rules to §0 (full text in Rewrite #3): withhold 📝 until after first attempt; probe every "great" with one drill-down; parroted-example answers cap at "good" until the probe passes. |
| F10 | P2 | D6, S7, S8, B5, E4, E5, SH6, SH7 + **core** R2, R3: `Weak: … · Great: …` with no Good tier | 10 of 47 questions are two-point scales in a three-point grading system; the grader invents the middle tier. | Add a Good tier to all ten (R2 e.g. "Good: names something reusable but doesn't extract it"), or declare [A] questions binary in §12 and map weak→weak, pass→great. |
| F11 | P2 | Hub questions `{"id","label","grade"}` vs §12 schema `{id, phase, label, pillars, grade}` | Hub data is schema-noncompliant; anything consuming `phase`/`pillars` (future heatmap grouping, per-pillar drill-down) breaks silently. | Backfill `phase` and `pillars` on all hub question entries; they're mechanical from the bank. |
| F12 | P2 | E2 📝: "validated against 50 human labels (they agree ~80%)" | 80% raw agreement with no chance correction is a weak judge — a constant-pass judge hits the base rate. The flagship judge-validation question teaches a bad target. | Rewrite example: "agreement 92% vs a 78% pass base rate, Cohen's κ 0.71; I retuned the judge prompt until κ cleared 0.7 and I report its error rate next to every eval score." |
| F13 | P2 | FT2 `📄 docs/MODEL_CARD.md` — absent from §12 `artifacts`, §10 matrix, and the §1 skeleton | A fine-tune project's key deliverable is invisible to the scorecard and coverage check. | Add `"MODEL_CARD.md"` to the artifacts object as a type-conditional key (document: "packs may add artifact keys"), and mention it in §10 for fine-tune builds. |
| F14 | P2 | SOURCES.md: "Re-run research… (see SKILL.md §10, step 5)" | Wrong cross-reference — the re-source ritual is §11 step 5; §10 is the coverage matrix. | Change to "§11, step 5." |
| F15 | P2 | README: "It interviews you, writes the 9 artifacts" | Stale count (7-pillar-era debt): schema tracks 13 artifacts. | "writes the 13 artifacts" or "the full artifact set." |
| F16 | P2 | §12: "append/update the entry in the hub's `data/scorecards.json`" | Cross-repo write with no mechanism — the skill runs in a project repo and has no idea where the hub is. A stranger's run dead-ends. | Define the convention: check for `BUILD_OS_HUB` env/config; else emit the JSON block and say "paste into your hub's data/scorecards.json." |
| F17 | P2 | "Exponent" ×6, "(IGotAnOffer/Meta)", "Nika" ×4, "top coding interviews score exactly this" (B1), "(MarkTechPost)" (SH4) | Interview-prep citations make an open-source tool read as a job-hunt artifact; MarkTechPost is a weak source for a strong claim. | Reframe "why it matters" lines around production outcomes; keep interview guides in SOURCES.md only; replace/soften the MarkTechPost claim. |
| F18 | P2 | S1: `Weak: "GPT-4o, it's best."` + example "4o at 50k/day = $500/day. 4o-mini…" | Anchoring the cost question to one vendor's 2024-25 lineup dates the doc immediately in 2026 and rots further. | Make it model-agnostic: "Weak: names the biggest frontier model 'because it's best.'" Mark example pricing as illustrative. |
| F19 | P3 | index.html heatmap header: `p.title.split(' ')[0]` | Two projects starting with the same word get identical column headers. | Use a `short` field or truncate: `p.title.slice(0,12)`. |
| F20 | P3 | §9: "ranked P1/P2/P3" vs audit culture P0/P1/P2; "→ writes `/evals/` notes" | Two severity scales in one system; one sim writes to "notes" instead of a named artifact; no sim exit criteria. | Standardize on P0/P1/P2; data review → `/evals/REVIEW.md`; require ≥5 findings or explicit clean-pass + "not reviewed" list. |
| F21 | P3 | SOURCES.md: "anchored to these authoritative 2025–2026 sources" then cites Nygard (2011), Christensen, Google eng-practices | Mislabeled — several anchors are evergreen classics, not 2025–2026. | "…to these authoritative sources (2025–2026 for the fast-moving areas, classics where the ground doesn't move)." |

---

## The 3 highest-leverage rewrites (in full)

### Rewrite #1 — S1 retag + the null-pillar rule (kills F1, the worst P0)

Replace S1's opening line:

```
- [C · S1] `[Economics][System Design]` **Which model did you pick, what does one use cost at your expected volume, and what's your backup if it's too slow or pricey?**
```

Also tag RAG3 `[Economics][System Design]` (it writes to COST.md). Then append to §12, after "average a pillar's questions":

```
**Null-pillar rule:** if a pillar had no graded questions this project (e.g. Economics was only
probed via an artifact, or a pack didn't fire), score it `null` — never invent or carry over a
number. The dashboard renders null as a visible gap. A gap you can see is information; a guessed
score is corruption of the loop.
```

And in `docs/index.html`, wherever pillar values are read (`latest.pillars[p]`, `x.pillars[p]`), skip/mask nulls rather than plotting them as 0.

### Rewrite #2 — the RAG pack in full v1.2 format (kills F6 for 8A; replicate the pattern for 8B–8D)

```
### 8A. RAG / search product

- [C · RAG1] `[Evaluation]` **When an answer is wrong, can you tell whether it grabbed the wrong documents or wrote badly from the right ones — and which do you fix first?**
  - 🤔 Not sure what I mean? → A RAG app does two jobs: find the right pages, then write from them. If the final answer is bad, you need to know WHICH job failed. e.g. re-run the question and look at what documents it pulled before it wrote anything.
  - Weak: only looks at the final answer. · Good: eyeballs the retrieved documents when something's off. · Great: scores retrieval and generation separately with their own metrics, and fixes retrieval first — good writing can't save wrong sources.
  - 📝 Example: "I log the retrieved chunks per query. Bad answer → check retrieval hit-rate first; 70% of my failures were retrieval misses, so I fixed chunking before touching the prompt."
  - 💡 Why it matters: end-to-end-only scores can't tell you where to fix; retrieval errors poison everything downstream. (Hamel Husain; RAGAS)
  - 📄 Creates: `/evals/retrieval/`, `docs/ARCHITECTURE.md` §Retrieval.

- [C · RAG2] `[Evaluation]` **How do you measure whether the search step is pulling the right stuff — with what numbers, on what test set?**
  - 🤔 Not sure what I mean? → Two numbers: "did the right document show up in the top results?" (recall) and "how much junk came along with it?" (precision). You need a small set of questions where you KNOW which document holds the answer.
  - Weak: "the answers seem good." · Good: a labeled set of query→correct-document pairs, reports recall@k. · Great: recall@k AND precision on a versioned labeled set, tracked across every change to chunking, embeddings, or k.
  - 📝 Example: "30 real questions, each labeled with its source doc. Recall@5 is 87%; when I switched embedding models it dropped to 79% and the eval caught it before users did."
  - 💡 Why it matters: retrieval quality is measurable exactly — guessing at it when you could measure it is amateur hour. (RAGAS metrics)
  - 📄 Creates: `/evals/retrieval/`, `docs/ARCHITECTURE.md` §Retrieval.

- [C · RAG3] `[Economics][System Design]` **How do you split documents into chunks — and did you actually test that choice against alternatives, or guess?**
  - 🤔 Not sure what I mean? → The system can't feed whole documents to the model, so it cuts them into pieces (chunks). Cut too small and answers lose context; too big and the right passage drowns in noise — and costs more. e.g. try 300-token vs 800-token pieces and see which answers better.
  - Weak: used the library default. · Good: picked a size for a stated reason. · Great: tested 2–3 chunking strategies against the retrieval eval (RAG2) and picked on measured recall + cost per query, noting the tradeoff.
  - 📝 Example: "Tested 400/800/1200 tokens with 15% overlap: 800 won on recall@5 (87% vs 81%) and cut cost 22% vs 1200. Wrote the numbers into COST.md."
  - 💡 Why it matters: chunking is the highest-leverage cheap knob in RAG, and it's testable — untested defaults are silent quality caps. (RAGAS; Hamel Husain)
  - 📄 Creates: `docs/ARCHITECTURE.md` §Chunking, `docs/COST.md` §Chunking test.

- [A · RAG4] `[Evaluation]` **Do you separately check "the answer only uses the sources" versus "the answer actually addresses the question"?**
  - 🤔 Not sure what I mean? → An answer can fail two different ways: it makes things up beyond what the documents say (faithfulness), or it sticks to the documents but doesn't answer what was asked (relevance). One check can't catch both.
  - Weak: one overall "is it good?" check. · Good: spot-checks for made-up claims. · Great: separate faithfulness and relevance checks in the eval suite, because their fixes differ — grounding failures need retrieval/prompt fixes, relevance failures need query understanding.
  - 📝 Example: "Judge scores faithfulness and relevance separately; a spike in unfaithful-but-relevant answers pointed at chunk truncation, not the prompt."
  - 💡 Why it matters: faithfulness vs relevance is the standard decomposition of RAG answer quality — conflating them hides which fix you need. (RAGAS: faithfulness / answer relevancy)
  - 📄 Creates: `docs/FAILURE_MODES.md`, `/evals/judge/`.
```

### Rewrite #3 — grading-integrity rules for §0 (kills F9, defuses Persona 1 and 4's core objection)

Insert into §0 as **Step 2½ — Grade like an interviewer, not a cheerleader**:

```
**Step 2½ — Grade like an interviewer, not a cheerleader.**
(a) **Never show the 📝 example before my first attempt.** The example is a rescue (Step 3) and a
    calibration for YOU — not a template for me. If I ask to see it first, show it only after
    noting the answer will be graded as assisted.
(b) **Probe every "great."** Before recording a great, ask exactly one drill-down into the weakest
    part of my answer ("you said retries are safe — what makes the SECOND retry safe?"). If the
    answer collapses, grade what's left.
(c) **Parroting caps at good.** If my answer mirrors the 📝 example's structure and numbers rather
    than my project's, it can't grade above good until the probe in (b) passes on MY specifics.
(d) **Show the arithmetic.** When writing the scorecard (§12), list each pillar's question grades
    and the resulting average in `notes`, and compute `overall` from the formula — never eyeball
    it. A pillar with no graded questions is `null` (see §12), not a guess.
```

---

## Missing questions / pillar gaps (to make it best-in-class)

**UX/UI & Interaction (worst gap — 1 core question).** Add `[C · UX1] [UX/UI & Interaction][Evaluation]`: **"When the AI gets it wrong, how does the user tell it — and where does that signal go?"** (weak: no feedback affordance · good: thumbs up/down stored · great: correction UX that feeds the eval set — closing the product's own loop). Also promote SH6 (accessibility) to `[C]` for any product with a UI; §10 currently demands accessibility evidence a `[A]` question may never generate.

**Collaboration & Stakeholders (2 questions, both hypothetical for solo builders).** Add `[C · CS1]`: **"What's one decision where a stakeholder (real or simulated) disagreed with you — what did they say, and what did you change or defend?"** — with the §9 simulations as the mechanism for solo builders, which neatly ties the two v1.2 features together and makes the sim mode load-bearing rather than optional.

**API pack.** Add `[C · API3] [System Design]`: **"When you need to change your API in a way that breaks existing users, what happens?"** (versioning, deprecation windows, changelogs) and `[A · API4] [Safety][System Design]`: auth + rate-limiting ("what stops one user's script from eating your whole model budget?").

**Safety.** Data lifecycle exists only inside the §9 security sim. Add `[A · SH8]`: **"What user data do you keep, for how long, and what would you have to delete if a user asked?"** (retention/PII → SAFETY.md §Data).

**Eval.** E1–E5 never ask about eval set size/confidence — a 20-example golden set moving 85%→90% is one flipped example. Fold into E5's Great tier: "…and you know how many examples a score must move on before you believe it."

---

## Verdicts

| Persona | Verdict | One reason |
|---|---|---|
| Frontier-lab hiring manager | **With reservations** | The bank discriminates, but until Rewrite #3 exists, a repo built with this could be pattern-matched seniority — the answer key ships with the test. |
| Staff/principal engineer | **With reservations** | Content is technically sound; but the OS's own pipeline shipped a divide-by-zero pillar, a formula-violating sample, and a chart that drops two pillars — the exact silent drift it preaches against. |
| Open-source maintainer | **With reservations** | Genuinely useful tool wearing a job-hunt costume: first-person voice, `~/build-os` paths, a LEARNINGS.md that doesn't exist, and interview-guide citations throughout. |
| Skeptical evals/quality lead | **With reservations** | The loop is more real than decorative (harvest→promote→prune has thresholds), but self-grading with visible answers plus an inflated sample scorecard (85≠83) means the numbers can't be trusted yet. |
| Non-expert career-switcher | **With reservations** | "Could I complete a project without getting stuck?" — Yes through all six core phases (the plain-English work is excellent); No the moment a type pack fires, which is precisely where MY project's questions live. |

**Bottom line:** this is a v1.2 that's one focused editing pass away from surviving the panel. Fix order: F1+F2 (P0s), F3–F9 (P1s, of which F6 is the big rewrite), then bump to v1.3 in the Changelog noting "audit pass 1: Economics tag + null-pillar rule, 9-pillar dashboard fixes, type packs brought to v1.2 format, grading-integrity rules, LEARNINGS.md canonicalized." Then re-run this audit. Do **not** run the gated dashboard step until that second pass is clean.

**Fed back into the loop (per "How to use the output," step 5):** candidate LEARNINGS entry — `2026-07-31 · meta · audit · "When you add a dimension to a scoring system, grep every consumer for the old count" · weak: fix the schema only / great: fix schema + renderers + samples + prose in one commit with an assert · source: this audit (F1–F5) · artifact: LEARNINGS.md`.

---

# Addendum — reconciliation against the v1.1 panel audit

The v1.1 audit (run against SKILL.md v1.1 before the v1.2 rewrite) was cross-checked after this report was first issued. Verdict on the v1.2 rewrite as a *response to that audit*: **it applied the cheap fixes and skipped both P0s.** Tracker:

| v1.1 finding | v1.2 status | This audit |
|---|---|---|
| F1 **P0** — model answers visible + self-grading | **NOT fixed** (📝 on every question, no withhold/probe rule) | Re-caught as F9 + Rewrite #3 |
| F2 **P0** — `~/build-os/` private paths break the loop for strangers | **NOT fixed** (verbatim in R2, R3, §11) | Re-caught as F8 |
| F3 P1 — "(§9)" wrong loop cross-ref | **Fixed** in SKILL.md (R3 now says §11) — but the same bug class reappeared in SOURCES.md ("§10, step 5") | New instance caught as F14 |
| F4 P1 — κ=0.8 quoted as the trust bar | **Regressed sideways**: κ removed entirely, replaced by raw "~80%" agreement — weaker than what was criticized | Caught as F12 |
| F5 P1 — "TPM/RPM breaks first" false universal | **Fixed** by removal (claim no longer appears) | Nothing to flag — confirmed absent |
| F6 P1 — type packs have no weak/good tiers | **NOT fixed**; now also violates v1.2's own 🤔/📝 standard | Re-caught as F6 + Rewrite #2 |
| F7 P1 — coverage matrix "Present? ▢" = existence, not quality | **NOT fixed** (line 431 verbatim) | **Missed from the table first pass** → added as F22 |
| F8 P1 — first-person diary framing vs open-tool claim | **NOT fixed** ("MY OS", "interviews me", "run my build OS") | In Persona 3 prose only → promoted to table as F26 |
| F9 P1 — D4 merged 🟡→✅ tier | **Fixed** (D4 now has three genuine tiers) | Confirmed fixed |
| F10 P2 — 8C missing data provenance / train-test contamination | **NOT fixed** (no provenance/license/contamination question exists) | **Missed first pass** → added as F24 |
| F11 P2 — unverified 2026 sources (TianPan, MarkTechPost) | **NOT fixed** | Partially re-caught (F17 + Persona 2); stands |
| F12 P2 — jargon/no glossary | **Largely fixed** by the plain-English rewrite + 🤔 — the one v1.1 finding v1.2 truly nailed | Residual gaps only in packs (F6) |
| F13 P2 — loop uninstrumented (no counters in schema) | **NOT fixed** (no `projects_since_resource_refresh` / `loop_ran` anywhere) | **Missed first pass** → added as F23 |
| Missing-Q: privacy/PII retention | **NOT added** | Independently re-proposed (SH8) |
| Missing-Q: rollback/incident response | **NOT added** (S8 covers prompt canary/rollback only; no "bad model live now — who's paged, how do you roll back" question) | **Missed first pass** → added as F25 |
| Missing-Q: second Economics question | **NOT added** — and v1.2 made it worse: S1 lost/never had the Economics tag | Superseded by F1 (P0 ghost pillar) |

## Findings added by reconciliation

| ID | Sev | Location (quote) | Problem | Concrete fix |
|---|---|---|---|---|
| F22 | **P1** | §10 line 431: `\| Craft pillar \| Proven by \| Present? \|` | Second-time survivor (v1.1 F7). Coverage = "artifact exists," so a one-line SAFETY.md ticks the box; matrix never reconciles with §12 grades — Safety can score 3/10 while showing "present ✓". | Change column to "Meets bar?" = the pillar's §12 grade band (weak/good/great); a pillar below `good` is a named gap, not a tick. |
| F23 | P2 | §11 step 5 "Re-source every ~5 projects" + §12 schema (no tracking field) | Second-time survivor (v1.1 F13). The loop's cadence is unfalsifiable — nothing counts projects, nothing records that the loop ran. | Add `"loop_ran": true, "projects_since_resource_refresh": N` to the §12 schema + template; dashboard shows the counter; "if you can't point to the counter, you haven't run the loop." |
| F24 | P2 | §8C — pack is FT1 (money case) + FT2 (model card) only | Second-time survivor (v1.1 F10). The question every serious team asks a fine-tune project — data provenance, licensing, train/test contamination — is absent; FT2's model card even asks "what data trained it" without probing whether that data leaks into the eval set. | Add `[C · FT3] [Evaluation][Safety]`: "Where did your training data come from, are you allowed to use it, and how do you guarantee none of it leaks into your test set?" → `docs/MODEL_CARD.md` §Data + `/evals/`. |
| F25 | P2 | Phase 5 — SH3 alerts, S8 canaries prompts; no incident question | v1.1 missing-Q, still missing. The OS ships and observes but never asks: "a bad prompt/model is live and users are hurting RIGHT NOW — what do you roll back, in what order, and who gets paged?" S8's 5% canary covers prompts pre-incident, not response mid-incident. | Add `[C · SH8-inc] [Reliability & Ownership]` incident question → `docs/ARCHITECTURE.md` §Incident response (rollback order: prompt → model pin → feature flag off; alert → owner). |
| F26 | P2 | Frontmatter "interviews me"; §11 title "what makes this MY OS"; trigger "run my build OS" | Second-time survivor (v1.1 F8), previously only in Persona 3 prose here. First-person diary framing contradicts open publishing. | Convert to second person throughout, or add a one-line preface declaring it a personal OS that readers should fork and re-voice. |

## Revised counts and severity note

**Revised totals: 2 P0 · 8 P1 · 12 P2 · 3 P3.** (F22 enters as P1; F23–F26 as P2; F17 partially merges with v1.1 F11.)

**Escalation note:** F8 (private-path loop) and F9 (visible answer key) were the v1.1 audit's two P0s, are unchanged in v1.2, and have now survived a full version bump. A finding that survives an audit unfixed should escalate, not coast — treat F8 and F9 as **P0-equivalent** in fix order: F1, F2, F8, F9 first, then the rest of the P1s. The v1.2 Changelog claims the version responded to review ("Rewrote every question…") while the two highest-severity findings from its own prior audit went unaddressed and unlogged — worth a Changelog line in v1.3 admitting exactly that, since honest defect history is itself evidence for the Reliability & Ownership pillar.
