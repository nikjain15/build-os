# Build OS — LEARNINGS (the loop's memory)

One line per harvested lesson:
`date · product-type · phase · new question · rubric sketch · source · artifact`

Promote a line into `skill/SKILL.md` when it shows up across 2+ projects (§11 step 3), then bump the
version and note it in the Changelog. This file lives at the hub-repo root so the loop is versioned
and public — a fresh clone works with no edits.

- 2026-07-31 · meta · audit · "When you add a dimension to a scoring system, grep every consumer for the old count" · weak: fix the schema only / great: fix schema + renderers + samples + prose in one commit with an assert · source: v1.2 adversarial audit (F1–F5) · artifact: this file
- 2026-07-31 · meta · audit · "A finding that survives a version bump unfixed escalates, it doesn't coast" · weak: re-log it / great: close it or log WHY not, in the changelog · source: v1.1→v1.2 reconciliation · artifact: SKILL.md Changelog
- 2026-08-01 · meta · audit · "Trace every deploy-time path (fetch URLs, Pages folder rules) as deployed, not as written" · weak: read the prose / great: resolve each URL against the real hosting root before publishing · source: v1.4 stress test (dashboard fetched /data which Pages never serves) · artifact: AUDIT-PROMPT.md Step 2b.5
- 2026-08-01 · meta · audit · "A version bump must sweep every companion doc (audit prompt, README counts, paths) or the toolchain contradicts itself" · weak: bump SKILL only / great: grep companions for the old version/paths in the same commit · source: v1.4 stress test (audit prompt still said 'for v1.2') · artifact: AUDIT-PROMPT.md Step 2b.6
- 2026-08-01 · meta · scope · "State the system's true scope; 'all products' needs a non-AI path or it's false advertising" · weak: rename the ambition / great: swap table + pack so non-AI runs at full rigor · source: v1.4 stress test · artifact: SKILL.md §8E
