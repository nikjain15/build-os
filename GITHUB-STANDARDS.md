# GitHub Standards

**One bar, every repository.** This is not aspirational best practice copied from a blog post. Every
rule below was extracted from a decision already made in one of these repositories, and each one
cites the commit, branch, or incident that produced it. Where a rule exists, something once went
wrong without it.

The bar is uniform. Some repositories do not meet it yet — the compliance snapshot at the bottom
says which, by name. A standard that only describes the repositories that already pass is a
description, not a standard.

Scope: every non-fork, non-archived repository under [github.com/nikjain15](https://github.com/nikjain15).

---

## 1. The repository must be findable

**Rule.** Description, at least three topics, and — if it deploys — a homepage URL pointing at the
canonical production host.

**Why.** `clearhouse` shipped a full MCP server, a scoring engine, and a 42-finding adversarial audit
with an empty description field for twelve days. It was invisible in search, in `gh repo list`, and
on the profile page. The README was excellent; nobody reaching the repo through a listing ever saw it.
A README is what you read *after* you decide to click. The description is what makes you click.

**Test.** `gh api repos/nikjain15/<repo> --jq '{description, topics, homepage}'` returns no nulls and
no empty arrays.

---

## 2. `main` is protected, and CI is the gate

**Rule.** Branch protection on `main` requiring status checks to pass. No direct pushes. Every change
arrives by pull request, including one-line changes.

**Why.** `rally`, `pulse`, `roleos-app`, `founderfirst.one`, `conduit`, `agent-commerce-os`, and
`lossless-modernization` already enforce this — `rally` requires
`typecheck · lint · unit · evals`, `dependency audit · secret scan`, and
`rules · integration (Firestore emulator)` before anything lands. `clearhouse` did not, and the gap
was not theoretical: a one-line URL fix could have gone straight to `main` unreviewed on the morning
of a demo.

**The rule holds for trivial changes specifically.** "It's one line" is the exact reasoning that
precedes the unreviewed push that breaks the deploy.

**Test.** `gh api repos/nikjain15/<repo>/branches/main/protection --jq .required_status_checks.contexts`
returns a non-empty list.

---

## 3. CI verifies the build with no credentials

**Rule.** A `.github/workflows/ci.yml` running on push to `main` and on pull request. It must
typecheck, test, and build. The build step must succeed with no secrets in the environment.

**Why.** `clearhouse/.github/workflows/ci.yml` sets `CLEARHOUSE_REPLAY_ONLY: '1'` on the build step,
with the reason written into the workflow: *the build must succeed with no credentials, the same
property the demo depends on — the hero path never needs a network*. That is the general principle.
A build that only passes when someone's local `.env` is present is a build that will fail in front of
an audience.

Use `concurrency` with `cancel-in-progress` so a fast follow-up push cancels the stale run, and set
`timeout-minutes` so a hung job cannot burn the runner budget. Both are already in the `clearhouse`
workflow and are the pattern to copy.

**Test.** CI is green on `main`, and the most recent run finished in under two minutes.

---

## 4. Secrets cannot enter the repository, by mechanism

**Rule.** Four layers, all of them:

1. `.env` and `.env*.local` in `.gitignore`, with a committed `.env.example` listing every variable by
   name and no real value.
2. GitHub secret scanning **and** push protection enabled.
3. Dependabot security updates enabled.
4. A secret-scan step in CI for repositories handling credentials, money, or personal data —
   `rally` and `roleos-app` use `.gitleaks.toml` for this.

**Why.** Layers 1 and 2 stop different things: `.gitignore` stops the file you know about, push
protection stops the key you pasted into a source file at 2am. On layer 3, the evidence is direct —
`pulse` shipped `fix(deps): bump nanoid to 3.3.18 to clear GHSA-2v37-7h3g-55p8 (#31)`, `conduit`
shipped `Bump fast-uri to 3.1.5 and hono to 4.13.0 for Dependabot alerts (#15)`, and `pulse` ran an
entire branch named `supply-chain/close-the-three-highs`. Three separate repositories have already
had to close real advisories. Dependabot is how you find out before a reviewer does.

**Test.** `git log --all -- .env .env.local` is empty, `.env.example` exists, and
`security_and_analysis` reports `secret_scanning`, `secret_scanning_push_protection`, and
`dependabot_security_updates` all `enabled`.

---

## 5. Contributor and agent guidance lives in `AGENTS.md`, with a `CLAUDE.md` pointer

**Rule.** `AGENTS.md` at the root holds setup, testing, conventions, structure, and PR rules.
`CLAUDE.md` is a three-line stub pointing at it. Never two sources of truth.

**Why.** `rally`, `pulse`, and `agent-commerce-os` already carry a byte-identical stub:

```markdown
# CLAUDE.md

This repository's contributor and agent guidance lives in [AGENTS.md](AGENTS.md).
Read it for setup, testing, conventions, project structure, and PR rules.
```

Different agent tools look for different filenames. The stub satisfies both conventions without
letting the guidance drift into two copies that disagree six weeks later.

**Test.** Both files exist; `CLAUDE.md` contains no guidance of its own.

---

## 6. The pull request template asks for the reasoning, not just the diff

**Rule.** `.github/PULL_REQUEST_TEMPLATE.md` requiring, at minimum: what changes and why, the
concrete change list, testing performed, risk and rollback, and a checklist covering tests, secrets,
docs, and breaking changes.

**Why.** The `rally` template asks for a **Technical edge** — *"what makes this strong or non-trivial:
a guardrail, correctness invariant, performance or cost win, security property, or novel approach"* —
and a **Risk & rollback** section. The `clearhouse` template goes further and encodes project
invariants directly as checkboxes: *no canary string or holdout question entered the repository*,
*versioned config was added as a new version rather than edited in place*, *any new number on screen
traces to `docs/EVIDENCE.md` or is computed from the formula*.

That is the pattern worth generalizing: **the template is where a project's invariants become
mechanical**. A rule stated in a design document is a hope. The same rule as a checkbox on every PR
is a process.

Filename is `PULL_REQUEST_TEMPLATE.md` (uppercase), for consistency across repositories. GitHub
accepts either case.

---

## 7. Commit subjects state the outcome

**Rule.** Imperative mood, sentence case, describing what is true after the merge — not which files
moved. Squash-merge so `main` carries one commit per PR with its number appended.

**Why.** This is already the house voice, and it is unusually good. From the log:

- `Give Rally a cost number, and cache the one path that scales with volume`
- `Three bounds on an agent run, not one`
- `Validate the judge, and fix the eval that had never run`
- `A kill line with a number, and the ADR for the choice it governs`
- `Make exposure caps bind cumulatively across files`
- `Correct the Opus price: it was 3x too high, in the live meter`

Every one of those tells a reader what changed about the *system*. None of them says "update
handler". A `git log` written this way is a changelog you never had to write separately.

Conventional-commit prefixes (`feat(scope):`, `fix(deps):`) are used in `roleos-app` and `pulse`
where the repository ships versioned artifacts. Both forms are acceptable; the outcome-stating
subject is not optional in either.

**Branch names** are `topic/slug`, where the topic names the concern:
`cost/`, `evals/`, `supply-chain/`, `harden/`, `fix/`, `presence/`.

---

## 8. Every claim in the README is sourced

**Rule.** Numbers, benchmarks, and competitive claims in a README must trace to a file in the
repository. Install lines and URLs must be verified against the live host before merge.

**Why.** `clearhouse` has `docs/EVIDENCE.md` and a README line reading *"Sources for every claim on
this page are in docs/EVIDENCE.md"* — the strongest version of this practice anywhere in the
portfolio. It also demonstrates the failure mode: `app/arena/page.tsx` advertised
`https://clearhouse.vercel.app/api/mcp`, an unrelated Vercel project that returns 404, while the
three other call sites used the working host. Anyone copying the install line off the demo page got
a dead server.

**One canonical URL per deployment**, used in the README, the app, the skill definition, and the
GitHub homepage field. Aliases may resolve; only one is advertised.

**Test.** `grep -r "https://" README.md` — every host resolves, and every documented endpoint returns
a non-error status.

---

## 9. A license, always

**Rule.** MIT unless there is a stated reason for something else, and the reason belongs in the
README.

**Why.** Eleven repositories are MIT. Three carry a custom license GitHub reports as `NOASSERTION` —
that is a deliberate choice for the RoleOS and FounderFirst products, and it is fine, but it should
be legible as a choice. Repositories with no license at all are not open source regardless of being
public: without one, nobody may legally use the code.

---

## Compliance snapshot

Taken 2026-08-28 across 20 non-fork, non-archived repositories. `—` is absent, `w` is a weak pass
(exists but not enforcing).

| Repository | Desc | Topics | License | CI | `main` protected | Secret scan | Dependabot | AGENTS | CLAUDE | PR tpl |
|---|---|---|---|---|---|---|---|---|---|---|
| rally | ✅ | ✅ | MIT | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| pulse | ✅ | ✅ | MIT | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| roleos-app | ✅ | ✅ | custom | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| founderfirst.one | ✅ | ✅ | custom | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| agent-commerce-os | ✅ | ✅ | MIT | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| agentic-payments | ✅ | ✅ | MIT | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| nikjain15.github.io | ✅ | ✅ | — | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| nikjain15 | ✅ | ✅ | — | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| clearhouse | ✅ | ✅ | MIT | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| conduit | ✅ | ✅ | MIT | ✅ | ✅ | **—** | ✅ | — | — | — |
| lossless-modernization | ✅ | ✅ | MIT | — | ✅ | ✅ | ✅ | — | — | ✅ |
| toddler-learning-companion | ✅ | ✅ | MIT | ✅ | **w** | ✅ | — | — | — | — |
| roleos-site | ✅ | ✅ | custom | ✅ | **w** | ✅ | — | — | — | — |
| hallmark | ✅ | — | — | ✅ | **w** | ✅ | — | — | — | — |
| nik-ai-assistant | ✅ | ✅ | MIT | — | ✅ | — | — | — | — | — |
| virtue-foundation-agent | ✅ | ✅ | MIT | — | ✅ | — | — | — | — | — |
| build-os | ✅ | ✅ | MIT | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| nik-jain-jobos (private) | ✅ | — | — | — | n/a | — | ✅ | — | — | — |
| role-os-private (private) | ✅ | — | — | — | n/a | — | — | — | — | — |
| healthcare (private) | — | — | — | — | n/a | — | — | — | — | — |

Branch protection is unavailable on private repositories without GitHub Pro; those rows read `n/a`
rather than failing.

### What the snapshot says

Six repositories — `rally`, `pulse`, `roleos-app`, `founderfirst.one`, `clearhouse`, and this one —
pass every applicable rule. The first four are the reference implementations, and the templates in
`templates/github/` are extracted from them. `clearhouse` and `build-os` were brought up to the bar
on 2026-08-28, in the same pass that wrote this document.

The most common gaps, in order:

1. **CI absent in seven repositories.** Several are documentation-only, where a link checker is the
   appropriate CI rather than a test suite. `build-os` shipped `scripts/validate_scorecards.py` with
   the instruction to *run before commit* — a validation that is now a workflow rather than a habit.
2. **Secret scanning off in three.** This is a settings toggle and costs nothing.
3. **`AGENTS.md` / `CLAUDE.md` missing in seven**, after `clearhouse` and `build-os` were fixed.
4. **`healthcare` has no description and no license** — the only repository failing rule 1 outright.
5. **Six repositories carry no license**, so despite being public nobody may legally use them:
   `nikjain15.github.io`, `hallmark`, and the four private repos. Rule 9 is the cheapest rule in this
   document to satisfy and the one with the clearest consequence for getting it wrong.

---

## Adopting this in a new repository

```bash
# 1. Metadata, at creation time, not later
gh repo edit <owner>/<repo> --description "<outcome, in one sentence>" \
  --add-topic <a> --add-topic <b> --add-topic <c> --homepage "<canonical url>"

# 2. Standard files
cp templates/github/PULL_REQUEST_TEMPLATE.md .github/
cp templates/github/ci.yml .github/workflows/
cp templates/github/CLAUDE.md .

# 3. Security settings
gh api -X PATCH repos/<owner>/<repo> -f 'security_and_analysis[secret_scanning][status]=enabled' \
  -f 'security_and_analysis[secret_scanning_push_protection][status]=enabled'

# 4. Protect main once CI has run at least once and the check name is known
gh api -X PUT repos/<owner>/<repo>/branches/main/protection --input templates/github/protection.json
```

Rule 2 has an ordering constraint worth stating: branch protection references status checks *by
name*, so CI must run once before the check name exists to require.
