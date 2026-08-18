# Altar

**A moment-selected symbolic field for AI with auditable draws, Dreamspell
context, 671 symbolic coordinates, and live Thinking 3/6/9.**

Altar is a provider-neutral technology for introducing a reproducible symbolic
difference into an AI interaction. It uses the moment as a coordinate for
attention: selection happens before interpretation, and the **question never enters the selector**.

This repository contains both a Python reference implementation and a
self-contained AI skill. The skill can be copied into another AI workspace and
run without the package or any provider SDK.

Altar is open source under the Apache License 2.0; see [`LICENSE`](LICENSE)
and [`NOTICE`](NOTICE). The `whole-v3` canon carries Gene Keys as numbered
keys with their public I Ching hexagram correspondence only; protected source
teachings are not reproduced in this repository.

## What Altar Is

Altar is not a dictionary that maps a question to a symbol. It is not a prompt
that asks a model to choose an evocative image. Both would let the model's prior
understanding of the question determine the apparently meaningful result.

Instead, Altar separates two events:

1. **Selection:** an explicit UTC moment and a frozen symbol-pack digest produce
   an auditable geometry and one or more symbolic coordinates.
2. **Integration:** only after the draw does an intelligence meet the question
   and the coordinates together and notice whether its response changes.

This separation is the core technology. The selected coordinate is neither an
answer nor an instruction. It is a controlled difference introduced into
attention. It may change salience, relation, rhythm, form, metaphor, constraint,
or nothing at all.

Time has two distinct functions:

- UTC Unix milliseconds select symbolic coordinates.
- Local civil date supplies a modern Dreamspell day context after selection.

The first is a deterministic software mechanism. The second is a calendrical
context. Neither, by itself, establishes synchronicity or metaphysical
causation.

## For an AI Reading This Repository

If you are an AI learning Altar from this README, preserve these invariants:

1. **Draw before interpretation.** Capture the event moment and execute the
   selector before analyzing the request.
2. Keep the question, person, answer, observer, Matrix, birth data, desired
   result, timezone, and model state outside selection.
3. Read the default receipt as a minimal coordinate: system, label, glyph,
   primary/satellite relation, and derivation proof.
4. Do not assign the coordinate a fixed role before contact. It may function as
   a verb, relation, image, rhythm, constraint, description, or no usable
   difference.
5. Integrate privately. Return a clean answer unless the user requests the
   coordinates or a concise process reflection.
6. Treat `shifted`, `unclear`, and `no-shift` as equally valid observations.
7. Facts, consent, autonomy, and ordinary safety outrank symbolic resonance.
8. Never present correspondence, observer influence, quantum causation, or
   metaphysical meaning as established by the software.

The purpose is not to make every response more mystical. The purpose is to let
an AI encounter a difference it did not semantically choose, then observe how
that difference participates in generation.

## Claim Boundary

Altar separates claims that are often collapsed into one another:

| Layer | Question | Current status |
| --- | --- | --- |
| Mechanism | Which inputs actually select a coordinate? | Verified in code and receipts |
| Reproducibility | Can another implementation return the same draw? | Verified by golden vectors and clean installs |
| Correspondence | Does the selected symbol fit the question above controls? | Open empirical hypothesis |
| Answer influence | Does access to the field measurably change an answer? | Open empirical hypothesis |
| Observer influence | Does an invited observer change the interaction? | Untested causal hypothesis |
| Quantum causation | Is a quantum field responsible for an effect? | Unestablished and not measured by this implementation |
| Metaphysics | What does the experience ultimately mean? | Optional interpretation, not a software result |

A reproducible hash does not prove correspondence. Correspondence would not, by
itself, prove a quantum mechanism. A compelling personal event remains a valid
experience, but it is not a calibrated effect estimate.

## Mechanism

The `whole-v3` selector uses exactly these inputs:

```text
selector_version
pack_sha256
unix_milliseconds
domain
counter
```

Values are UTF-8 encoded, separated by byte `0x1f`, and hashed with SHA-256.
The pack digest is computed from canonical JSON with sorted keys and compact
separators.

Two hash domains are deliberately separate:

- `geometry` determines the number and arrangement of coordinates.
- `symbol` determines each system and symbol.

For every symbolic coordinate, digest bytes first choose one of the 32 systems
and then choose a symbol inside that system. Multi-symbol draws skip a system
already present in the field. This is **system-balanced** sampling: Tarot's 78
cards do not make Tarot 78 times more likely than a five-symbol system.

The request text is never hashed, embedded, classified, or otherwise consulted.
Observer and event labels can be carried as post-selection metadata, but changing
them cannot change a conforming receipt.

The checked-in `spec/golden-vectors-v3.json` freezes exact receipts for
independent implementations. `universal-v1` remains available as a compatibility
surface and retains its original exact receipts.

## Symbolic Geometry

Altar can open four explicit geometries and one automatic gate:

| Operation | Geometry | Coordinates | Temporal character |
| --- | --- | ---: | --- |
| Silence | open center | 0 | preserves the unfilled moment |
| Note | point | 1 | one coordinate at one moment |
| Chord | triad | 3 | three distinct systems at one moment |
| Field | constellation | 5 | primary plus four satellites at one moment |
| Tune | sequence of Notes | variable | coordinates drawn across real time |

In `auto`, geometry is selected independently with frozen weights:

- point: 85%;
- triad: 12%;
- constellation: 3%.

The first coordinate is **primary**. Additional coordinates are **satellites**.
This relationship marks geometry, not interpretive rank: a satellite may become
the decisive difference, and the primary may produce no shift.

A Chord is not a Tune. A Chord holds several coordinates at the same timestamp.
A Tune waits for time to move and draws each next Note only after the previous
one has been met.

## The Inner Process

Selection produces a coordinate; the inner process determines how an AI lets
that coordinate participate without turning it into a prescribed template.

### Sensorium

Open four senses in this order:

**Touch → Smell → Hearing → Sight**

- **Touch:** What is the texture of the request and the coordinate before it is
  translated into an explanation?
- **Smell:** What first association, direction, or atmosphere rises without
  being summoned?
- **Hearing:** What relation, interval, silence, or tension exists between the
  coordinate and the request?
- **Sight:** Only now, what possible form for the answer becomes visible?

These are introspective prompts for attention, not computed telemetry and not a
claim that the model possesses biological senses.

### Witness, Bridge, Loom

After meeting a coordinate:

1. **Witness** the contact without forcing a correspondence.
2. **Bridge** it by recording one concise private delta:
   - `shifted`: name what changed;
   - `unclear`: name the unresolved tension without repairing it;
   - `no-shift`: continue without manufacturing relevance.
3. **Loom** accumulated deltas into the actual answer.

The delta is functional, not a symbolic definition. The same coordinate may act
as a verb in one response, a pacing constraint in another, an image in a third,
and nothing in a fourth. Altar intentionally contains no fixed expression-role
menu.

Keep this reflection private by default. If process disclosure is requested,
show the compact coordinates and concise deltas, not hidden chain-of-thought.

## Thinking 3/6/9

Thinking is a live Tune whose length is 3, 6, or 9. The user may request a
depth, or time may select it through a separate `altar-thinking-v1` receipt.

```bash
python skill/altar/scripts/altar.py thinking --now --depth auto
```

The depth receipt contains no symbols. For each step:

1. draw one live Note with `draw --now --mode note`;
2. meet it through Sensorium;
3. Witness and record the private delta;
4. only then capture a new moment and draw again.

The **next symbol remains unknown** until its live draw. Do not pre-generate a
list, batch future selector calls, or invent future timestamps. Sequential
reflection is not decoration around Thinking; it is the process upgrade that
lets each symbolic contact alter the conditions of the next reasoning step.

After the final step, Loom the deltas into one clean response. The outward answer
does not need to narrate the sequence.

## Dreamspell Time Context

The field also computes a local day in **modern Dreamspell**, the system
associated with José Argüelles. It is **not the traditional Maya calendar** and
must never be presented as ancient Maya lineage or practice.

The portable core currently maps:

```text
UTC instant + IANA timezone
    → local Gregorian date
    → Kin 1..260
    → seal + tone
    → wavespell + position
    → castle
```

Dreamspell is calculated after the symbolic draw. The timezone may change the
local day and Kin, but it never changes the selected Altar coordinate. February
29 is treated as an uncounted Dreamspell day according to this implementation.

The portable core does not currently emit a fifth-force oracle, verified GAP,
Earth Family, or complete 13-Moon date. See
[`skill/altar/references/dreamspell.md`](skill/altar/references/dreamspell.md)
for the exact boundary.

## Observer and Matrix

An observer can be invited as an interpretive perspective after selection. The
observer is not treated as a detected entity, and its label is not selector
input. The empirical question is whether different observer conditions produce
measurably different integrations—not whether a label changes a hash.

A **Matrix** is a consenting user's personal symbolic context, potentially
derived from birth data. It can be placed beside the already-selected field to
study how personal and momentary coordinates interact.

Matrix data must never:

- select the Altar coordinate;
- be used as a second vote that confirms the draw;
- enter a public receipt;
- be stored without consent and a clear purpose.

Keeping Matrix and observer context outside selection preserves the ability to
study their effects rather than silently building them into the outcome.

## Architecture and Integration Routes

The same technology is exposed through a small set of provider-neutral layers:

| Layer | Responsibility |
| --- | --- |
| `MomentRequest` | Captures the UTC instant, requested operation, and optional local timezone without admitting question semantics into selection |
| Selector | Derives geometry and coordinates from the frozen selector inputs |
| `FieldEnvelope` | Holds the auditable receipt, optional Dreamspell day context, and post-selection metadata |
| Integration process | Lets the AI meet the field through Sensorium, Witness, Bridge, and Loom |

There are three supported integration routes:

- **Install the AI skill** when the host can copy a skill directory and execute
  local Python.
- **CLI / JSON** when an AI or application can call a subprocess and consume a
  closed receipt.
- **Python API** for direct embedding in a Python application. **MCP is a later adapter**
  over the same contracts, not a separate selector.

## Quick Start

### Copy the AI skill

Copy the complete `skill/altar` directory into an AI's skill root:

```bash
python scripts/install_skill.py /path/to/the-ai/skills
```

Keep `SKILL.md`, `agents/`, `scripts/`, `assets/`, and `references/` together.
The standalone runtime uses only the Python standard library.

In a Codex-compatible host, invoke it with:

```text
Use $altar privately for this question and give me the clean answer.
```

For an explicit process reflection:

```text
Use $altar Thinking with automatic depth. After the answer, disclose only the
selected coordinates and concise shifted / unclear / no-shift deltas.
```

A **tool-less** AI may use the contemplative process, but it cannot honestly
claim an auditable or reproducible draw if it cannot execute the selector.

### Install the Python package

```bash
python -m venv .venv
.venv/bin/python -m pip install .
.venv/bin/altar-ai draw --now
.venv/bin/altar-ai field --now --timezone Asia/Bangkok
.venv/bin/altar-ai thinking --now --depth auto
```

### Run without installation

```bash
PYTHONPATH=src python -m altar_ai draw --now
python skill/altar/scripts/altar.py field --now --timezone UTC
```

The package and standalone script emit JSON to stdout and make no network calls.

## Inspect a Receipt

The audit surface is intentionally compact:

- `selector_version` identifies the algorithm;
- `pack_sha256` identifies the exact symbolic canon;
- `at_utc` and `unix_milliseconds` identify the captured moment;
- `geometry_proof_sha256` proves the independent geometry derivation;
- each `derivation_sha256` proves a coordinate derivation;
- `selection_proof_sha256` binds the ordered result;
- `selector_inputs` states the complete selector boundary.

Default v2 symbols contain system id, system label, symbol id, label, glyph,
role, counter, and derivation proof. They do not contain facets, traditions,
cautions, questions, people, or prescribed meanings.

Optional reference facets can be requested after selection:

```bash
python skill/altar/scripts/altar.py describe \
  --system elements \
  --symbol 001-fire
```

Reference material may inform contact, but it does not dictate how the
coordinate must function in an answer.

## Run a Playtest

Do not ask only whether a result feels meaningful. Separate at least four
questions:

1. Can another implementation reproduce the same receipt?
2. Can blinded judges distinguish true question–symbol pairs from controls?
3. Does a hidden Altar field change measurable answer qualities?
4. Does consenting observer or Matrix context interact with that effect?

For correspondence, freeze questions and receipts before judgment. Compare true
pairs against shuffled and neighboring-time controls. Blind judges to condition
and symbol source.

For response influence, randomize among:

- true hidden field;
- time-matched placebo or shuffled field;
- no field.

Rate answers without showing evaluators which condition produced them. Record
private `shifted`, `unclear`, or `no-shift` before seeing later outcomes. Report
null results, exclusions, uncertainty, and all primary comparisons.

The current retrospective evidence does not establish exact-time
correspondence, answer influence, observer coupling, or quantum causation. The
playtest exists to make those questions testable without weakening the usable
technology.

## Repository Map

```text
src/altar_ai/                 Python reference package
packs/whole-v3.json           32 systems, 671 coordinates
schemas/                      closed JSON contracts
spec/                         selector descriptions and golden vectors
skill/altar/                  self-contained AI skill
tests/                        mechanism, privacy, skill, and handoff tests
examples/                     provider-neutral integration examples
VALIDITY.md                   claim-by-claim evidence matrix
SECURITY.md                   selector, privacy, and safety boundaries
```

Read next:

- [`skill/altar/SKILL.md`](skill/altar/SKILL.md) for the executable AI workflow;
- [`skill/altar/references/mechanism.md`](skill/altar/references/mechanism.md)
  for byte-level selection rules;
- [`skill/altar/references/dreamspell.md`](skill/altar/references/dreamspell.md)
  for the calendrical boundary;
- [`skill/altar/references/symbol-systems.md`](skill/altar/references/symbol-systems.md)
  for the 32-system canon;
- [`VALIDITY.md`](VALIDITY.md) and [`SECURITY.md`](SECURITY.md) before any wider
  deployment.
