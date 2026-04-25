# Freshness Thresholds

Defines how long each artifact type can go without verification before it's considered stale. Thresholds are not arbitrary — they're calibrated to the rate at which each artifact type typically drifts.

## Default Thresholds

| Artifact Type              | Staleness Threshold | Rationale                                                                                           |
| -------------------------- | ------------------- | --------------------------------------------------------------------------------------------------- |
| Root AGENTS.md             | 14 days             | High-traffic file; module additions, command changes, and pattern evolution happen frequently        |
| Module AGENTS.md           | 30 days             | Modules change less frequently than the root project                                                |
| docs/ARCHITECTURE.md       | 30 days             | Architecture evolves gradually; major changes trigger explicit updates                               |
| docs/OBSERVABILITY.md      | 21 days             | Build commands and CI configs change with dependency updates                                        |
| docs/PLANS.md              | 7 days              | Active work index; stale within a week as plans are created and completed                           |
| docs/exec-plans/active/*   | No staleness        | Active plans are ephemeral — their lifecycle is completion, not freshness                            |
| docs/exec-plans/completed/*| No staleness        | Completed plans are archival — they never need refreshing                                           |
| tech-debt-tracker.md       | 30 days             | Debt items resolved or added regularly; monthly review is sufficient                                |
| harness-manifest.md        | 0 days (auto)       | Refreshed on every garden audit — if it's stale, no audit has run                                   |
| scripts/check_harness.py   | 90 days             | Script logic rarely changes; only update when the manifest schema changes                           |

## Adjusting Thresholds

Thresholds should be adjusted based on repository activity:

### High-Velocity Repos (>5 PRs/day)

Tighten thresholds by ~50%:
- Root AGENTS.md: 7 days
- OBSERVABILITY.md: 14 days
- PLANS.md: 3 days

### Low-Velocity Repos (<1 PR/week)

Relax thresholds by ~2x:
- Root AGENTS.md: 30 days
- OBSERVABILITY.md: 45 days
- PLANS.md: 14 days

### Post-Major-Refactor

Override all thresholds to 0 — everything should be re-verified immediately after a major refactor (module renames, build system migration, framework upgrade).

## Velocity-Based Adjustment Heuristic

Instead of using fixed thresholds, consider adjusting based on the artifact's change velocity:

```
effective_threshold = base_threshold × (1 / change_velocity_factor)
```

Where `change_velocity_factor` is:

| Recent git history for the artifact's scope | Factor |
| ------------------------------------------- | ------ |
| >10 commits in last 14 days                 | 2.0    |
| 3-10 commits in last 14 days                | 1.0    |
| 1-2 commits in last 14 days                 | 0.5    |
| 0 commits in last 14 days                   | 0.3    |

Example: ARCHITECTURE.md has a base threshold of 30 days. If there have been 8 commits touching the architecture-relevant directories in the last 14 days, the effective threshold drops to 15 days (30 / 2.0). If nothing has changed, it extends to 100 days (30 / 0.3).

This ensures that actively changing areas get more frequent verification while stable areas don't generate noise.

## Freshness vs. Content Accuracy

Freshness is a proxy for accuracy, not a guarantee. A file can be "fresh" (recently verified) but still contain stale content if the verification was superficial. Conversely, a file can be "stale" by threshold but perfectly accurate because nothing in its scope changed.

The garden audit addresses this by:

1. Using freshness as a **prioritization signal** — stale artifacts get checked first
2. Performing **semantic verification** regardless of freshness — even recently verified artifacts are spot-checked
3. Only refreshing dates after **actual content verification** — not just existence checks

## Recommended Audit Cadence

| Repo Context         | Recommended Cadence  | Rationale                                                        |
| -------------------- | -------------------- | ---------------------------------------------------------------- |
| Rapid development    | Weekly               | High velocity means high drift potential                         |
| Steady development   | Bi-weekly            | Balance between vigilance and overhead                           |
| Maintenance mode     | Monthly              | Low change rate means low drift risk                             |
| Pre-release          | On-demand            | Verify control plane accuracy before any major milestone         |
| Post-refactor        | Immediately          | Refactors are the #1 cause of structural and semantic drift      |

## Integration with CI

Consider running `scripts/check_harness.py` in CI as a lightweight continuous check:

- **On every PR**: run `check_harness.py` — catches structural drift immediately
- **Scheduled (weekly)**: run full `harness-garden` audit — catches semantic drift

The CI check is fast (sub-second) and prevents PRs that break cross-links or delete managed files without updating the manifest. The scheduled audit is slower (requires code search and semantic verification) but catches the deeper drift that mechanical checks miss.
