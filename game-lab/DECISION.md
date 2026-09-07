# Product Decision — Portal Flow

## Decision
Continue **Portal Flow** through a measurable 20-level validation build. Do not yet fund ads, IAP, a backend, or a Unity rewrite.

The prototype proves the interaction, but it does not prove retention or differentiation. The product earns one more development gate because it is cheap to test, instantly readable, one-handed, and has a strong visible fail state. Its largest risk is not engineering: it is being perceived as another tile-triple game.

## Evidence status
- The internal product-lead stream supports sort/buffer mechanics, but the cited market claims are not reproduced with URLs in the repository and therefore remain **unverified here**.
- Claude and Gemini result files are absent. No conclusion is attributed to either model.
- The product choice is therefore based on prototype economics and testability, not asserted market leadership.

## Gate now implemented
- deterministic 20-level campaign
- a generator with a known valid removal path for every level
- progressive colors, stack counts, belt pressure, and tutorial copy
- local progression, coins, stars, sound, haptics, reduced-motion support
- Undo, Hint, and +1 Slot boosters
- offline-capable PWA shell and separated, testable game engine

## Validation plan
Test with 10–20 people before SDK work. Record: rule comprehension without explanation, level-5 completion, first-session duration, voluntary replay after failure, and whether players can describe a distinctive hook.

## Kill / pivot gate
Kill or materially change the mechanic if fewer than 70% understand the rule in the first minute, more than 35% leave before level 5, median first session is under 5 minutes, or most testers describe it only as “tile match.” Do not solve a failed test with more meta systems.

## Next production gate
After human validation: replace generated boards with authored/replay-verified level data, add event instrumentation behind a provider-neutral adapter, produce final icons/screenshots/privacy copy, then wrap with Capacitor for device QA. Ads, consent flow, IAP, and store accounts require explicit owner approval and provider choices.
