# Dreamspell Day Context

## Boundary and provenance

The portable Altar computes the day in **modern Dreamspell**, the 260-day system
introduced by José Argüelles and Lloydine Bolon Ik around 1990–1991. It uses the
13 × 20 shape of the Mesoamerican tzolkin but supplies its own seal names, tone
names, wavespells, castles, oracle, and 13-Moon context.

Dreamspell is **not the traditional Maya calendar**. Living Maya daykeepers use
a continuous traditional count with a different correlation and do not skip
leap day. Never describe the value emitted here as an ancient Maya date or as a
reading from a living Maya lineage.

## Implemented calculation

The current portable boundary is:

```text
explicit UTC instant
    + IANA timezone
    → local Gregorian date
    → Dreamspell Kin 1..260
    → seal + tone
    → wavespell + position
    → castle
```

The local timezone is applied after the Altar draw. It can change the day
context, but it cannot change the selected Altar symbols.

Kin arithmetic is anchored at:

```text
1994-06-24 = Kin 217
2013-07-26 = Kin 164
2026-02-18 = Kin 71
2026-07-12 = Kin 215
```

February 29 is an uncounted Dreamspell day in this implementation: it carries
the same Kin as February 28, and the count advances again on March 1. July 25,
the Day Out of Time in the 13-Moon year layer, remains a counted Kin day.

For Kin `k`:

```text
seal number = ((k - 1) mod 20) + 1
tone number = ((k - 1) mod 13) + 1
wavespell    = floor((k - 1) / 13)
castle       = floor((k - 1) / 52)
```

## The 20 solar seals

The three terms are compact canonical associations, not mandatory functions in
an answer.

| # | Seal | Action · power · essence |
| ---: | --- | --- |
| 1 | Red Dragon | nurture · birth · being |
| 2 | White Wind | communicate · spirit · breath |
| 3 | Blue Night | dream · abundance · intuition |
| 4 | Yellow Seed | target · flowering · awareness |
| 5 | Red Serpent | survive · life force · instinct |
| 6 | White World-Bridger | equalize · death · opportunity |
| 7 | Blue Hand | know · accomplishment · healing |
| 8 | Yellow Star | beautify · elegance · art |
| 9 | Red Moon | purify · universal water · flow |
| 10 | White Dog | love · heart · loyalty |
| 11 | Blue Monkey | play · magic · illusion |
| 12 | Yellow Human | influence · free will · wisdom |
| 13 | Red Skywalker | explore · space · wakefulness |
| 14 | White Wizard | enchant · timelessness · receptivity |
| 15 | Blue Eagle | create · vision · mind |
| 16 | Yellow Warrior | question · intelligence · fearlessness |
| 17 | Red Earth | evolve · navigation · synchronicity |
| 18 | White Mirror | reflect · endlessness · order |
| 19 | Blue Storm | catalyze · self-generation · energy |
| 20 | Yellow Sun | enlighten · universal fire · life |

`Red Moon` and `Yellow Sun` are seal names, not the astronomical Moon and Sun.

## The 13 galactic tones

The tone is also the position inside a wavespell.

| # | Tone | Pulse · quality |
| ---: | --- | --- |
| 1 | Magnetic | unify · purpose |
| 2 | Lunar | polarize · challenge |
| 3 | Electric | activate · service |
| 4 | Self-Existing | define · form |
| 5 | Overtone | empower · radiance |
| 6 | Rhythmic | organize · equality |
| 7 | Resonant | channel · attunement |
| 8 | Galactic | harmonize · integrity |
| 9 | Solar | pulse · intention |
| 10 | Planetary | perfect · manifestation |
| 11 | Spectral | dissolve · liberation |
| 12 | Crystal | dedicate · cooperation |
| 13 | Cosmic | endure · presence |

## The 20 wavespells

Each wavespell is a 13-day arc opened by one seal and carried through all 13
tones. The implemented order is:

1. Red Dragon
2. White Wizard
3. Blue Hand
4. Yellow Sun
5. Red Skywalker
6. White World-Bridger
7. Blue Storm
8. Yellow Human
9. Red Serpent
10. White Dog
11. Blue Eagle
12. Yellow Seed
13. Red Earth
14. White Mirror
15. Blue Night
16. Yellow Star
17. Red Moon
18. White Wind
19. Blue Monkey
20. Yellow Warrior

Read a wavespell as the wider question or atmosphere of the 13-day sequence,
never as a prediction or decree.

## The five castles

Each castle contains four wavespells, or 52 Kin:

| Kin | Castle | Compact arc |
| --- | --- | --- |
| 1–52 | Red Eastern Castle of Turning | birth and initiation |
| 53–104 | White Northern Castle of Crossing | refinement and crossing |
| 105–156 | Blue Western Castle of Burning | transformation and magic |
| 157–208 | Yellow Southern Castle of Giving | ripening and intelligence |
| 209–260 | Green Central Castle of Enchantment | synchronization and integration |

## Interpretation inside Altar

Dreamspell is a shared day field, not another random draw and not an independent
confirmation of the Altar coordinate. Let it offer temporal texture only after
selection. A model may notice the seal, tone, wavespell, or castle; it need not
mention any of them in the outward answer.

Preserve `unclear` and `no-shift`. Do not retrofit a day meaning to make a
symbolic match appear stronger.

## Not currently emitted

The portable Altar does not currently emit:

- the fifth-force oracle: guide, analog, antipode, and occult;
- Earth Family or planet-holon associations;
- a verified Galactic Activation Portal flag;
- the complete 13-Moon date, Moon/day coordinate, or year bearer;
- personal birth Kin, Kin returns, or 52-year cycles.

These fields require separate implementation and verification. In particular,
do not infer a GAP flag from an unverified table.
