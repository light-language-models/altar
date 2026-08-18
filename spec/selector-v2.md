# Altar portable selector v2

`whole-v3` is a deterministic, content-blind selector. It does not consume the
question, answer, observer label, Matrix, birth data, local timezone, or model
state.

## Inputs

The selection boundary contains only:

1. selector version `altar-portable-v2`;
2. canonical SHA-256 of the `whole-v3` pack;
3. Unix milliseconds of an explicit UTC instant;
4. an ASCII domain label;
5. a non-negative counter.

Parts are UTF-8 encoded and separated with byte `0x1f` before SHA-256.

## Geometry

The `geometry` domain is distinct from every symbol domain. In `auto`, the
first 64 bits modulo 100 resolve as point for 0–84, triad for 85–96, and
constellation for 97–99. Explicit silence, note, chord, and field resolve to
open-center, point, triad, and constellation respectively.

## Coordinates

Each `symbol` counter digest chooses a system from the full system list and then
a symbol inside that system. Duplicate systems are skipped, so satellites
cannot silently overweight a large catalogue. The first coordinate is primary;
the remainder are satellites. Receipts contain labels and proofs, not facets or
prescribed meanings.

Dreamspell day context, observer lenses, Matrix context, and interpretation are
computed only after selection. Thinking selects a depth of 3, 6, or 9, but each
next coordinate is drawn live after the previous private reflection; a future
stream is never pre-generated.
