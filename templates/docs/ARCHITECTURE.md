# Architecture — <product name>

## How it's built (S2)
<request path diagram: user → … → response; where safety, tools, state sit>

## Failure recovery (S5)
<retries/backoff, breaker, fallback; or third-party-down plan for non-AI>

## Edge cases (B1)
| Case | Guard (in code) |
|---|---|

## Only-once actions (B4)
<idempotency approach for state-changing actions>

## Prompt versioning (S8) / Change rollout (non-AI swap)
<how prompt/config changes ship: versioned, gated, staged, rollback>

## Performance budget (GEN1)
<p95 per key flow + what enforces it>

## Migrations (GEN2)
<expand-then-contract plan, backup + rollback>

## Observability (SH3)
<what's traced, alert thresholds>

## Incident response (SH8)
Rollback order: <1 → 2 → 3>; who is paged; incident → permanent eval case.
