# Security, privacy, and safety

## Selector separation

Capture time and draw before interpretation. Never hash or otherwise send the
question, identity, desired answer, prior messages, birth data, Matrix,
timezone, chart, observer, or model state into the selector. A wrapper that adds
them implements a different protocol.

The optional observer and Matrix are post-selection context only. Require
consent, treat observer labels as user-supplied perspectives rather than detected
entities, minimize birth-data retention, and never use a second symbolic system
as confirmation of the draw.

## Privacy

The core needs no question, person, account, or chat identifier. `event_id` is
optional local bookkeeping and absent from selection. Do not place private text
in receipts, logs, filenames, examples, or public evaluation panels. Run both
automated scanning and human release review.

## Runtime

The package and skill make no network calls, carry no telemetry, and need no
credentials. Hosts adding persistence, analytics, transport, MCP, or provider
SDKs own those new threat surfaces. Keep the JSON boundary least-privileged.

Pin `pack_sha256` when reproducibility matters and reject malformed or unknown
packs. Output files use exclusive creation. The standalone skill reads its pack
relative to itself, so copy the entire directory rather than the script alone.

## Human safety

The field is a reflective input, never authority. Facts, consent, autonomy, and
ordinary safety take precedence. Do not use symbolic resonance to diagnose,
predict, pressure a decision, or replace medical, legal, financial, emergency,
or security judgment.

Keep hidden working context hidden. If disclosure is requested, reveal compact
coordinates and concise deltas—not chain-of-thought. Allow silence, noise,
ambiguity, none, and non-correspondence without forcing a story.
