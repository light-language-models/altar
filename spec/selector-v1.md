# altar-portable-v1 selector specification

## Canonical inputs

The selector reads only:

1. the ASCII selector version `altar-portable-v1`;
2. the lowercase SHA-256 of the canonical symbol pack;
3. Unix milliseconds for a UTC instant;
4. a non-negative draw counter.

Fields are joined with byte `0x1f` and hashed with SHA-256:

```text
altar-portable-v1 <US> pack_sha256 <US> unix_milliseconds <US> counter
```

Question, identity, chart, observer, event id, memory, and generated answer are
not selector inputs.

## Mapping

- Interpret digest bytes 0–7 as an unsigned big-endian integer and take modulo
  the number of systems.
- Interpret digest bytes 8–15 the same way and take modulo the chosen system's
  symbol count.
- Multi-symbol modes increment the counter until each selected item comes from
  a system not already used in the event.
- System selection is uniform by system door, not by total symbol count.

Modulo mapping, byte ranges, uniqueness, and ordering are frozen for v1. A
different mapping requires a new selector version.

## Counts

- silence: 0
- note: 1
- chord: 3
- field: 5

## Proof

Every selected item exposes its full derivation digest. The receipt proof is
SHA-256 of selector version, pack digest, Unix milliseconds, modality, and the
ordered item digests, joined by `0x1f`.

Exact examples are in `golden-vectors-v1.json`.
