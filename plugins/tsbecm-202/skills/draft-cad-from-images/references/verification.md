# Verify consistency and source fidelity separately

| Claim | Required evidence |
| --- | --- |
| Valid DXF | Reopens with no audit errors or automatic fixes |
| Numerically consistent | Saved geometry agrees with independent source expectations |
| Faithful redraw | Values, symbols, anchors, views and inferences reviewed against actual images |
| Tested in AutoCAD | Actually opened and checked in Autodesk AutoCAD |

Passing one row does not prove another. Generating a dimension from a number and comparing it to the same number does not verify its source interpretation.

Check relevant units, native dimensions, feature anchors, hole count/radii/positions, slot envelope, profile thickness, slopes, chains and views. Fail numerical validation for missing manifest handles, nonfinite data, hard-coded dimension replacements, unit conflicts, or incorrect plot ratio. Do not count unresolved annotation-only values as verified native dimensions.

Render the saved file, inspect the sheet and dense crops, and fix:

- Missing views or clipping at the frame/page edge.
- Wrong symbols, decimal separators or font glyphs.
- Ambiguous witness lines, unreadable arrows or text.
- Axes, hatching, or edges crossing dimension values.
- Inconsistent weights or duplicate edges.
- Incorrect paper settings or viewport scale.
- Missing in-drawing identification of unresolved details.

Move annotations, mask their background appropriately, or locally break annotation lines without changing the part. Do not reuse a transformed render backend. Render PNG from the first PDF export.

The final note states source files, units, print scale, actual output formats, checks performed, and exact unresolved information. Distinguish standard-table and derived dimensions from printed ones. Never imply verification supplied absent tolerances or member lengths.
