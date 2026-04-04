# Harness Skills Suite

## Overview

`Refinex-Skills` is a personal, high-discipline skill suite built
around Harness Engineering. Its goal is not to produce toy code, but to
let agents work inside real repositories in a way that is stable,
auditable, and resumable.

The suite is built on four control-plane ideas:

- the repository is the primary source of truth
- continuity is externalized into `AGENTS.md`, `docs/`, execution plans,
  and generated facts
- runtime visibility, validation, and drift repair are part of the harness
- task execution and control-plane maintenance are separated but tightly connected

## The Four Skills

### 1. `harness-bootstrap`

Used to initialize or complete the Harness baseline in a new or
existing repository.

It is responsible for:

- root and local `AGENTS.md`
- `docs/PLANS.md` and `docs/OBSERVABILITY.md`
- `docs/exec-plans/tech-debt-tracker.md`
- `docs/generated/harness-manifest.md`
- repo-local `scripts/check_harness.py`

Typical use:

```text
$harness-bootstrap
Task: establish a Harness Engineering control plane for this repository
```

### 2. `harness-garden`

Used to continuously audit and repair Harness drift in repositories
that already have a baseline.

It is responsible for:

- routing and boundary drift audit
- stale managed docs / manifest / repo check detection
- low-risk auto-repair
- remediation-plan generation for high-risk semantic drift

Typical use:

```text
$harness-garden
Task: audit and repair Harness drift in this repository
```

### 3. `harness-feat`

Used for new features, capability delivery, and structured refactors.

It is responsible for:

- rewriting the raw task prompt
- running harness preflight
- creating or updating an active execution plan
- implementing in small validated slices
- syncing `docs/PLANS.md` deterministically
- archiving the plan deterministically when done

Typical use:

```text
$harness-feat
Task: implement a provider health view
```

### 4. `harness-fix`

Used for bugs, regressions, incidents, flaky paths, and repair work.

It is responsible for:

- rewriting the bug brief
- running harness preflight
- reproducing or bounding the failure
- creating or updating a fix plan
- isolating root cause
- applying the narrowest justified repair
- adding regression protection
- syncing `docs/PLANS.md` deterministically
- archiving the plan deterministically when done

Typical use:

```text
$harness-fix
Task: fix the request hanging after provider switch
```

## Recommended Workflow

### New repository

1. Start with `harness-bootstrap`
2. Use `harness-garden` periodically
3. Use `harness-feat` for feature work
4. Use `harness-fix` for repair work

### Existing repository

1. If the control plane is incomplete, start with `harness-bootstrap`
2. If the baseline exists but may have drifted, run `harness-garden`
3. Then use `harness-feat` or `harness-fix` depending on task type

## Why This Suite Exists

- Consistent style: all four skills share one Harness vocabulary and lifecycle
- Mechanically verifiable: manifest, repo checks, and fixture/golden tests are first-class
- Safe by default: unmanaged strategic docs are preserved
- Resumable: work is externalized into active and archived execution plans
- Production-oriented: the focus is correctness, continuity, and engineering constraints

## Repository Layout

```text
skills/
├── harness-bootstrap/
├── harness-garden/
├── harness-feat/
└── harness-fix/
```

Each skill contains:

- `SKILL.md`
- `agents/openai.yaml`
- `references/`
- `assets/`
- `scripts/`

Some skills also include fixed `fixture + golden` regression tests.

## License

This repository is released under the MIT License.
