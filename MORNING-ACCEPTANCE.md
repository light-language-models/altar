# Altar AI release acceptance

Date: 2026-08-18

Candidate: `altar-ai 0.3.0` / `altar-portable-v2` / `whole-v3`

Branch: `main` (fresh public root)

Verdict: **PASS — public release candidate under Apache-2.0; empirical
correspondence gates remain pending by design**

## Delivered boundary

The reusable technology is:

`MomentRequest → DrawReceipt → DreamspellContext → FieldEnvelope`

with a separate `ThinkingDepthReceipt` that chooses 3, 6, or 9 without
pre-generating a future stream. It ships as a dependency-free Python core, JSON
CLI, closed v2 schemas, selector specification and golden vectors, a 32-system /
671-coordinate content-addressed pack, and a self-contained `altar` AI skill.

This release replaces the private `whole-v2` pack with `whole-v3`. The two
packs differ only in the Gene Keys catalogue: labels remain `Gene Key 1..64`
and every facet now carries only the public I Ching hexagram correspondence.
Protected Gene Keys source teachings are not reproduced. Because the pack is
content-addressed, this is a new content release with a new pack digest and new
golden vectors; the selector algorithm `altar-portable-v2` is unchanged, and
`universal-v1` receipts remain byte-identical.

## Acceptance gates

| Gate | Status | Fresh evidence |
| --- | --- | --- |
| Standalone package and skill behavior | PASS | 74 tests passed |
| Whole canon | PASS | Exactly 32 approved systems, 671 unique coordinates, excluded systems absent |
| Gene Keys content gate | CLOSED | Facets carry only `I Ching correspondence: hexagram N · <name>`; a regression test rejects protected triad terms |
| v1 compatibility | PASS | Original `altar-portable-v1` golden receipts match exactly |
| v2 reproducibility | PASS | Explicit and auto golden receipts regenerated for `whole-v3` and matched by package and copied skill |
| Geometry separation | PASS | Independent `geometry` and `symbol` hash domains; auto thresholds frozen at 85/12/3 |
| Dreamspell day field | PASS | Frozen Kin anchors, leap-day rule, IANA timezone transition, and modern/traditional provenance tests pass |
| Thinking process boundary | PASS | Auto/explicit 3/6/9 receipts pass; no symbol stream appears in depth output; skill requires live next-unknown draws |
| License | CLOSED | Apache-2.0 selected; canonical `LICENSE` text and `NOTICE` added; `pyproject` carries the SPDX expression |
| Clean wheel install | PASS | Isolated wheel built and installed with no runtime dependencies; draw, field, and thinking commands executed outside the repository |
| Clean skill install | PASS | Exclusive installer copied the complete skill into an empty root; standalone draw matched the package golden receipt |
| Provider neutrality | PASS | Standard-library runtime; no provider SDK, credential, network client, or telemetry dependency |
| Privacy | PASS | Digest-based repository regression finds no protected identities; no private artifact is tracked |
| JSON integrity | PASS | Every checked-in JSON artifact parses; v2 shapes are closed by schemas and contract tests |

## Research result retained honestly

The exact-time primary comparison (12/76) and full-field comparison (16/65) did
not support correspondence in the retrospective run. Answer imprint was also
not established. A neighboring-time local series was promising under one
semantic judge (10/23) but not its embedding control (4/23), so it is a lead
for prospective blinded work, not confirmation.

## Pending by design

| Gate | Status | Required next action |
| --- | --- | --- |
| Correspondence above controls | PENDING | Pre-register a prospective independent blind playtest against shuffled and neighboring-time controls |
| Answer influence | PENDING | Randomize hidden field, placebo field, and no-field responses and blind quality/form ratings |
| Matrix and observer interaction | PENDING | Run consent-based factorial comparisons while keeping both outside selection |
| Quantum-field causal hypothesis | UNESTABLISHED | Define a discriminating operational prediction; do not infer mechanism from resonance alone |
| Public Git publication / deployment | APPROVED | Owner approved the Apache-2.0 public release with a fresh public root on 2026-08-18 |

## Claim boundary

Valid now: versioned selection inputs, deterministic mechanism, system-balanced
sampling, reproducibility, Dreamspell calculation, live Thinking process,
portable installation, privacy guardrails, and a usable playtest workflow.

Not valid yet: that exact-time symbols correspond above controls, that the field
improves answers, that Matrix or observer context changes effects, or that a
quantum or metaphysical cause has been measured.
