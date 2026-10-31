# Read without inventing measurements

## Source ledger

Keep a record per dimension or unresolved feature:

| Field | Meaning |
| --- | --- |
| id | Stable local name, such as plate.height |
| status | source, derived, standard, unresolved, or graphic |
| value, unit | Normalized value and explicit unit; null if unresolved |
| source | Actual filename, page, crop rectangle, or authoritative URL |
| anchors | Measured edges, axes, points, arc, or angle rays |
| reading | Original notation and alternate readings |
| derivation | Formula and input IDs for derived values |
| confidence | Confidence in both glyph and anchors |

Use a value as a source dimension only when its anchors are clear. Keep crops for contested readings. Confidence labels do not replace visual evidence. Do not put private reference images in this reusable skill.

## Reading order

Inspect full-page context, views, scales, and units. Rotate text upright and inspect at original resolution. Compare duplicate photos. Follow witness lines to their actual part/axis. Distinguish boundaries, dimension lines, breaks, weld symbols, and hidden lines. Preserve diameter, radius, degree, tolerance and decimal symbols. Reconcile relationships without letting a plausible engineering value override the printed one.

## Common traps

- Rotated `129°` can resemble `128°` or `123°`. A symbol beside `6` can look like `16`. Inspect upright.
- `26.4 %` is a ratio of 0.264, about 14.78868 degrees, not 26.4 degrees.
- `TR20 / BL18 / CL 8.8` denotes hole, bolt, and bolt class, not a 20 mm bolt or 18 holes.
- Four rows at pitch 60 have three intervals. For height 240 and top margin 30, the bottom margin is `240 - 30 - 3*60 = 30`.
- A slot of width 16 and overall length 54 has radius 8 and centre spacing 38. First confirm that 54 is overall.
- Apparent symmetry is an inference when no datum confirms it. Name that inference if it locates holes.
- A standard IPE designation does not specify plate size, hole layout, notch radius, or weld.
- A small fitting may show its width but omit height, vertical bolt spacing, and hole diameters. Tag it, e.g. B1, and list those unknowns. A drawn square is not proof of equal dimensions.
- Open ends omit total member lengths. Use convenient graphic display lengths without calling them source dimensions.

## Incomplete or conflicting sources

State the exact issue, e.g. “The total is 240 but the chain sums to 250,” or “401 is readable but its left witness-line anchor is unclear.” Continue independent geometry. Do not choose arbitrary endpoints just to obtain 401.

If a partial deliverable is useful, identify unresolved items inside the CAD drawing and the note. Someone may open the file without seeing the conversation.

## Standards

For European IPE profiles, start with the manufacturer's table:
https://orangebook.arcelormittal.com/node/6

Verify designation (IPE, IPE A, IPE O, etc.) and units at use time. Use relevant primary sources for other profiles and requirements. Do not extend remembered IPE values to unrelated parts. This workflow is a drawing reconstruction, not structural sizing or certification.
