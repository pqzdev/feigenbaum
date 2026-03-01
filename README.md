# Feigenbaum Explorer

An interactive browser-based explorer for the logistic map and its period-doubling route to chaos.

Originally written as a Python/matplotlib animation. Converted to this interactive tool by [Claude Code](https://claude.ai/claude-code).

**Live at: https://feigenbaum.pedroqueiroz.workers.dev**

## What it shows

- **Cobweb diagram** — visualises the iteration of `f(x) = r·x·(1−x)` as a staircase between the parabola and the diagonal `y = x`. Segments are drawn at low opacity so frequently-visited regions glow brighter.
- **Bifurcation diagram** — the classic Feigenbaum diagram showing which x-values the orbit settles on for each r ∈ [2.5, 4.0].
- **Teal attractor dots** — when the orbit is periodic (not chaotic), dots mark the exact cycle points on the parabola.
- **Horizontal guides** — dashed teal lines connect the attractor y-values across both charts when in a periodic window.

## Controls

- **Drag the blue line** on the bifurcation diagram to set r (cursor changes to ↔ near the line).
- **Increment buttons** — fine-tune r in steps of ±0.1 down to ±0.0000001.
- **URL** — the current r value is stored in `?r=`, so any state can be bookmarked or shared.

## Tech Stack

- **Frontend**: Vanilla JavaScript + Canvas 2D API, no dependencies
- **Hosting**: Cloudflare Workers (serves static HTML)

## Deployment

```bash
npm install -g wrangler
npx wrangler login
npx wrangler deploy
```
