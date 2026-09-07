# Game Lab — Multi-Agent Product Discovery

## Goal
Find and validate a simple-to-build mobile puzzle/hybrid-casual game concept inspired by proven WeChat mini-game mechanics, but redesigned as an original IP for Türkiye + global markets.

## Non-negotiables
- Do not copy names, art, characters, brands, level layouts, or proprietary assets.
- Separate verified facts from assumptions.
- Cite current sources for market/ranking/revenue claims.
- Optimize for a very small team, fast MVP, low backend complexity, and store readiness.
- Prefer mechanics that are understandable in <5 seconds and playable with one finger.

## Roles
### Claude — China / WeChat Scout
Research WeChat mini-games and China casual/hybrid-casual trends. Extract the underlying mechanic, retention loop, monetization pattern, and why each candidate works. Focus on proven but technically simple candidates.

### Gemini — Global Store / Creative Scout
Research Google Play + App Store comparables, especially Türkiye/Europe/global. Evaluate saturation, visual/creative angles, ASO/SEO keywords, localization opportunities, and store/IP risks.

### ChatGPT — Product Lead / Builder
Cross-check both research streams, score technical feasibility and differentiation, select the MVP, define product/monetization architecture, and implement the prototype/production code in GitHub.

## Required candidate scorecard
For each candidate score 1-10:
1. Build simplicity
2. Market proof
3. Competition risk (10 = low risk)
4. Ad creative potential
5. Retention potential
6. Monetization fit
7. Original-IP flexibility
8. Store-readiness

Also estimate:
- MVP build effort
- Backend need
- Art/content burden
- Best monetization model
- Main reason it could fail

## Deliverables
1. 10 candidate mechanics
2. Top 3 shortlist
3. One recommended concept
4. 1-page MVP spec
5. First 20-level progression outline
6. Store positioning + naming direction
7. Risks / kill criteria

## Collaboration protocol
Each agent writes its findings under `game-lab/results/`:
- `claude.md`
- `gemini.md`
- `chatgpt.md`

Do not overwrite another agent's findings. ChatGPT produces the final synthesis in `game-lab/DECISION.md` after the other streams are available.
