# Integration guide

## Copy into an AI workspace

Install the entire `altar` directory as a skill, keeping `SKILL.md`,
`scripts/altar.py`, `assets/whole-v3.json`, and `references/` together. The
script uses only the Python standard library and emits JSON on stdout, so a host
can also invoke it as a subprocess without understanding skill metadata.

The minimum host sequence is:

1. capture the event time before interpreting the request;
2. call `field --at <UTC> --timezone <IANA-zone>`;
3. place `hidden_field` and the Sensorium instructions in private model context;
4. let the model produce its own concise delta before weaving the answer;
5. return a clean answer, disclosing coordinates only when requested.

A tool-less model may use the contemplative workflow, but must not claim that a
draw is auditable or reproducible if it could not execute the selector.

## Thinking

Call `thinking --now --depth auto` once. Then loop exactly that many times. On
each iteration call `draw --now --mode note` only after the previous private
delta is complete. Do not batch calls or substitute artificial timestamps.

## Personal context

Observer profiles and birth Matrix data belong in a post-selection context
block. Require consent, minimize stored birth data, and never use it as selector
material or as a second vote that validates the draw. Profiles may change how a
host attends; they do not change the receipt.

## Surfaces

- Skill: best for an agent that can run local scripts.
- CLI/subprocess: best for any host with Python 3.11+.
- Python package: best for applications needing typed contracts and schemas.
- MCP adapter: a later thin wrapper around the same JSON boundary; it must not
  add question content to selector inputs.
