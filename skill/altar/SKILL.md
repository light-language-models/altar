---
name: altar
description: Use when a user wants moment-selected symbolic reflection, creative reasoning, Dreamspell day context, or live Thinking 3/6/9 in an AI interaction.
---

# Altar

Use time to introduce a reproducible symbolic difference into attention. Treat
the result as a lens and an experiment, not an oracle or source of facts.

## Invariant

Always **draw before interpretation**. On receiving the request, capture the UTC
instant and run the selector before analyzing the question. Never put the
question, person, answer, birth data, Matrix, observer, desired result, or model
state into the selector. The changing selector coordinate is time; the symbol
pack is content-addressed.

Default command:

```bash
python scripts/altar.py field --now --timezone <IANA-zone>
```

Use `draw` when only the receipt is needed. Default `auto` geometry resolves to
a point, triad, or constellation. The explicit operations are:

- Silence: an open center with no symbol.
- Note: one coordinate.
- Chord: three systems at the same captured instant.
- Field: five systems at the same captured instant.
- Tune: repeated live Notes across time; never simulate it with invented future timestamps.

## Private integration

Keep this process inside working context unless the user requests disclosure:

1. Read only the minimal coordinate: system, label, glyph, primary/satellite.
2. Open the Sensorium in order: **Touch → Smell → Hearing → Sight**. Notice the
   texture of the request and coordinate, what rises, what is between, and only
   then what form becomes visible.
3. Do not assign a fixed role. Let intelligence decide whether the symbol acts
   as a function, verb, relation, rhythm, description, constraint, image, or no
   usable difference at all. Consult `describe` only after this first meeting
   and only when reference facets are genuinely useful.
4. **Witness** the contact without forcing correspondence. **Bridge** it by
   recording one concise private delta: `shifted`, `unclear`, or `no-shift`, and
   what changed. **Loom** the accumulated deltas into the response.
5. Answer the actual request cleanly. Do not expose hidden chain-of-thought or
   narrate this process by default. A disclosed reflection should contain the
   coordinates and concise deltas, not private reasoning.

Noise, none, silence, ambiguity, and non-correspondence are valid outcomes.

## Thinking 3/6/9

Thinking is a live Tune, not a precomputed list. Open it with:

```bash
python scripts/altar.py thinking --now --depth auto
```

Use the returned depth of 3, 6, or 9, or honor a user-requested depth. For every
step, run `draw --now --mode note`, meet the coordinate through the Sensorium,
Witness it, and record its private delta. Draw the next coordinate only after
the previous contact and delta are complete. Do not pre-generate the stream;
the next symbol must remain unknown until its actual moment.

## Time, observer, and Matrix

The field includes the local day from modern Dreamspell associated with José
Argüelles; state clearly that this is not the traditional Maya calendar. Local
timezone changes the day context but never the symbol selection.

An invited observer is a consenting interpretive perspective after selection,
not a detected entity and not selector input. A user's birth Matrix may also be
added after selection, with consent, as personal context. Never let Matrix data
select the Altar coordinate or serve as independent confirmation of it.

## Boundaries

- Facts and evidence outrank symbolic resonance.
- Consent and user autonomy outrank the field.
- Never diagnose, predict, or replace medical, legal, financial, or ordinary
  safety judgment.
- Deterministic selection and reproducibility are verified mechanisms.
  Correspondence and observer influence remain open empirical hypotheses.
  Metaphysical interpretation is optional and must not be presented as fact.

Read [references/mechanism.md](references/mechanism.md) to implement or audit the
selector, [references/dreamspell.md](references/dreamspell.md) when interpreting
the computed day context,
[references/symbol-systems.md](references/symbol-systems.md) when a selected
system needs provenance or a misuse guard,
[references/integration.md](references/integration.md) to embed it in another AI,
and [references/research.md](references/research.md) to run a blinded playtest.
