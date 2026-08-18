# Mechanism v2

`altar-portable-v2` maps one UTC Unix millisecond and the canonical SHA-256 of
the `whole-v3` pack to an auditable geometry and ordered coordinates. It does
not consume the question, observer, Matrix, local timezone, model, or answer.

Hash UTF-8 values separated by byte `0x1f`:

1. selector version;
2. pack SHA-256;
3. Unix milliseconds;
4. domain;
5. counter.

The `geometry` domain is independent of every `symbol` domain. Auto geometry
maps percentiles 0–84 to point, 85–96 to triad, and 97–99 to constellation.
Each accepted symbol digest chooses a system from the system list and then a
symbol inside it. Repeated systems are skipped, making every system the first
sampling unit instead of overweighting larger catalogues. The first coordinate
is primary and later coordinates are satellites.

Receipts intentionally expose only coordinate labels and derivation hashes.
Run `describe --system <id> --symbol <id>` after selection for optional facets.
A receipt proves reproducible selection from named inputs; it does not prove
semantic correspondence, observer influence, or metaphysical causation.

The modern Dreamspell day field is computed after selection from a local date.
February 29 is uncounted in this implementation. It is the modern system
associated with José Argüelles, not the traditional Maya calendar.

`thinking` uses a separate `altar-thinking-v1` domain to choose only a depth of
3, 6, or 9. It never chooses or returns the future symbolic stream.
