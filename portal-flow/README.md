# Portal Flow

A one-finger hybrid-casual sorting puzzle prototype designed for fast mobile sessions and low production complexity.

## Core loop

1. Each column is a stack of crystals.
2. Only the exposed top crystal can be tapped.
3. Tapped crystals move to a six-slot staging belt.
4. Any three crystals of the same color clear automatically.
5. The player loses if the staging belt fills before a triple forms.
6. Clear every crystal to complete the level.

## Prototype features

- Responsive mobile-first layout
- Procedural seeded levels
- Persistent unlocked level using `localStorage`
- Combo + score system
- Three lightweight tools: Undo, Hint, Shuffle
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

## Technical direction

Keep the web prototype for rapid mechanic iteration. If the mechanic validates, move to a mobile production shell using **Capacitor** first rather than rewriting immediately in Flutter. This keeps the validated JavaScript game logic intact and allows Android/iOS packaging, haptics, ads and IAP integrations with less rewrite risk. A Flutter/Flame rewrite only becomes worthwhile if the game evolves into heavier animation, physics, large scene management or performance-sensitive systems.
