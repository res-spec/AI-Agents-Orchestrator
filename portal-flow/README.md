# Portal Flow

A one-finger hybrid-casual sorting puzzle prototype designed for fast mobile sessions and low production complexity.

## Core loop

1. Each column is a stack of crystals.
2. Only the exposed top crystal can be tapped.
3. Tapped crystals move to a six-slot staging belt.
4. Any three crystals of the same color clear automatically.
5. The player loses if the staging belt fills before a triple forms.
6. Clear every crystal to complete the level.

## Validation-build features

- Responsive mobile-first layout
- Deterministic 20-level campaign with a guaranteed solution path
- Versioned local progress, stars, coins, and settings
- Combo + score system
- Three lightweight tools: Undo, Hint, +1 Slot
- Haptics, reduced-motion setting, installable/offline PWA shell
- A dependency-free game engine with Node tests
- Web Audio generated sound effects (no external/licensed audio assets)
- Win/fail feedback and star grading
- Original visual language and IP-safe theme
- No backend, login, analytics, ads, SDKs, or paid APIs

## Product hypothesis

The mechanic sits between tile-triple, sorting and buffer-management puzzles. The intended strength is immediate readability for short-form ad creatives: a player can understand the risk (six-slot belt) and the mistake state in a few seconds.

## What to validate before production

- Can a new player understand the mechanic without tutorial text?
- Does the staging-belt tension create repeat attempts?
- Are losses perceived as fair rather than random?
- Do 30–90 second levels feel satisfying?
- Which visual wrapper performs best in creative tests: crystals/portal, kitchen/packing, travel/luggage, or workshop/crafting?

## Kill criteria

Do not invest in a large content pipeline until small-user testing shows:

- strong replay intent after a loss,
- low confusion in the first session,
- and a clear creative hook that can be shown in a 10–15 second ad.

## Run and test

```bash
cd portal-flow
npm test
npm run serve
```

## Technical direction

Keep this web build for mechanic validation. If the human test gate passes, wrap it with **Capacitor** for Android/iOS device QA. Do not add ads, analytics, IAP, or store credentials until providers and privacy requirements are approved.
