---
title: Roadmap
status: active
type: development
updated: 2026-10-19
tags: [roadmap, create-swords]
---

# Roadmap

Remaining work against [[Design/Game Design Document]]. Built behavior and verification limits belong in [[Current Status]] and [[Development/Code Map]]. Completed historical phases are preserved in [[Archive/Project History/Roadmap before vault organization — 2026-10-19]].

## First-session loop

- [ ] Set base forge heating to **10 seconds** (latest build note still reports 15).
- [ ] Implement ore roulette: one shared lever cycles all empty stands in under five seconds; occupied stands retain their results until collected; no automatic restart.
- [ ] Start with the tantō blueprint and on-screen guidance. Suppress customer visits during the first craft; the first listing triggers the tutorial customer.
- [ ] Guarantee a fair first offer; teach haggling on the second ordinary shop sale.
- [ ] After the first sale, introduce **Iron Wakizashi**, minimum 90% quality, providing the blueprint at commission start. Grinding remains optional.
- [ ] Deliver commissions through a sword picker for the agreed reward, without display listing or haggling.
- [ ] After delivery, offer the **second material stand** upgrade; tune its cost against tutorial earnings.
- [ ] Replace hilt timing/seat bonuses with three untimed taps; introduce tradition-matched fittings unlocked by crafting milestones.
- [ ] Introduce katana through a later local teaching commission.
- [ ] Implement session-locked persistent saves for currencies, inventory, unlocks, and upgrades.

## Crafting quality and validation

- [ ] Tune hit rhythm, staged/local deformation, blade proportions, full-blade camera framing, and hot-to-steel presentation from player feedback. Retain the initial shared hit count; tune modest extra effort for higher tiers later.
- [ ] Verify grinding is understandable, safe, and genuinely optional in coins earned per minute; test enjoyment after several swords.
- [ ] Recheck revised crafting → hilt → held sword → display → sale, including grinding, after further changes.
- [ ] Reduce the documented one-EditableMesh-per-visible-sword resource pressure; decide caching/static-mesh strategy while preserving refined appearance.
- [ ] Test published clients, lower-memory phones, multiplayer observers, and leaving/rejoining during crafting. Studio probe timings are not device-wide performance evidence.
- [ ] Tune blueprint prices/stars, fitting milestones, material rewards, and commission requirements.

## Shop, village, and progression

- [ ] Build six-player plot assignment and the shared mountain village.
- [ ] Build spacious properties with distinct storefront/crafting areas, broad routes, and expansion reserve; exact dimensions still need blockout testing.
- [ ] Implement early/mid/late building and station upgrades using [[Art/Japanese Village Concept Art]] as the visual reference; concept counts are illustrative.
- [ ] Add upgrade purchases for holders, forge capacity, heating speed, ingot storage, material stands, and roll luck; add Material Index.
- [ ] Use displayed stock to influence regular customers and reputation to unlock special arrivals. Include primarily local early customers and an early special outsider.
- [ ] Add letters, in-person commissions, untimed special requests, familiarity, and personal commission chains.
- [ ] Introduce outside sword traditions through visitor commissions, then offer additional blueprints for coins.
- [ ] Make functional facilities affect business while keeping decoration cosmetic.

## Later systems and launch

- [ ] Add cashier and apprentice smith upgrades; tune output and worker roles.
- [ ] Review optional polish, color, etching, and gem-work scope before adding required stations or interactions.
- [ ] Implement gem rewards/upgrades and review monetization proposals against the final loop.
- [ ] Finish HUD/offer/assembly UI, sound, environment art, tutorial polish, and storefront imagery.
- [ ] Run new-player tests across desktop and touch, then public testing and launch checks.

## Already built — see Current Status for evidence

Browser study/editor, BladeCore port, untimed anvil forging, safe grinding, server Finish checks, and the Japanese workshop/station rebuild are documented as implemented. They are not new pending tasks here. A complete build chronology remains in [[Sessions/2026-10-19]].
