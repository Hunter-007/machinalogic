# Machina Logic redesign: "Mimic board"

Subject: OT/ICS security for the plants, grids, mines, ports and water works of Africa.
Audience: plant/engineering heads, CISOs, regulators. Job: earn trust, get briefing requests.

The visual language comes from the control room itself: the painted grey panels of
substation mimic boards, single-line electrical diagrams (SLDs), engraved switchgear
nameplates and hazard markings. Nothing like the dark-mode + neon look every cyber site uses.

## Colour
| Token  | Hex     | Role |
|--------|---------|------|
| panel  | #D4D7CF | Page background: control-panel grey (RAL 7035 family) |
| paper  | #EEEFE9 | Raised surfaces, fields, nameplates |
| ink    | #11233F | Text, busbar lines, footer: deep busbar navy, not black |
| flow   | #2350C8 | Normal current flow, links, focus |
| live   | #E0281E | Threats, faults, the single red flood moment |
| hazard | #FFC21A | Primary action, hazard band, the OT side of comparisons |

## Type
- Display: Big Shoulders (opsz 10–72, 800–900): condensed industrial sign lettering, mixed case, tight leading, very large.
- Text: Atkinson Hyperlegible Next: built for legibility, fits a safety-first brand.
- No monospace, no tracked caps labels. Small labels are sentence case on engraved "nameplates".

## Signature (the one bold thing)
A live busbar: one continuous single-line-diagram conductor that runs the length of every page,
drawn by your scroll. It routes through device symbols (breakers, transformers) that close as
current reaches them, carries moving current pulses, and jumps out into each section's artwork.

## Layout
- Left-aligned throughout. A narrow left rail carries the busbar on every page.
- Home: SLD hero → pinned "gap" story (Convergence → Scarcity → Consequence, page floods red)
  → horizontal pinned services track (six animated drawings) → IT/OT spec sheet with hazard OT column
  → Africa network map + sectors → 4-step sequence on the busbar → why us → hazard-band call to action.
- Inner pages: hero + page artwork (exploded Purdue stack on Resources, Africa map on About,
  sector drawings on Industries, service drawings on Services).
- Page-to-page: a hazard-shutter wipe using cross-document view transitions.

## Removed tells
Neon teal on near-black, Space Grotesk/IBM Plex, eyebrow labels, 01/02/03 on non-sequences,
middle-dot meta strings, card grids, corner brackets, scanlines, terminal console, ticker,
highlighted word in the headline, arrows appended to buttons.

## Review against the brief
- First draft used a dark "control room at night" theme: rejected, that is the default cyber look.
- Considered blueprint blue: rejected, a cliché for "engineering".
- Kept primaries in check: red only for faults/threats, yellow only for action/hazard, blue only for flow.
