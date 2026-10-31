# Drawing workflow

[Project home](../README.md) · [All guides](README.md)

This guide describes the complete path from an image or dimensioned brief to a reviewable CAD package.

## Prepare the source

Supply the complete sheet and any useful close-ups. Keep original files unchanged. Include all related views, units and any known scale information. A photograph may be distorted, so written dimensions take priority over pixel proportions.

For a source brief rather than an image, identify which values are design inputs for the exercise. The industrial workshop uses that route; it is not presented as a photo-reconstruction benchmark.

## Read and record

Inspect small and rotated labels, dimension witness lines, profile designations, hole symbols, weld symbols and slope notes. OCR can help, but it is only a second reading.

Use a source ledger with these fields:

| Field | Purpose |
| --- | --- |
| ID | Stable identifier such as `frame.span` or `plate.hole_pitch` |
| Value and units | The actual number and its model units |
| Status | Source, derived, standard, unresolved or graphic |
| Evidence | Image/region, printed label or calculation |
| Anchors | The two features, centres or edges being measured |
| Notes | Ambiguity, contradiction or review question |

A readable value with uncertain endpoints is still unresolved. Do not invent endpoints merely to make the number fit.

## Resolve relationships

Check dimension chains, repeated patterns, symmetry and agreement between views. Distinguish bolt diameter from hole diameter, slot overall length from centre spacing, and slope percent from degrees. A slope of 15% means a rise/run ratio of 0.15, not an angle of 15 degrees.

Do not silently change a conflicting number. Finish independent geometry, mark unresolved regions and ask a focused question when a missing measurement controls construction. Any approximate illustration belongs on the undimensioned graphic layer and must be labelled as such.

## Construct editable CAD

Draw at full model size in explicit units. Use native lines, arcs, circles and polylines; preserve true curves. Separate outlines, axes, hidden geometry, hatching, dimensions, notes and undimensioned graphics onto layers.

Create native DIMENSION entities. Their displayed numbers must be measured from the geometry; never conceal an incorrect length with replacement text. Editable dimensions are not necessarily associative or parametric.

Use the provided helper functions for document setup, dimensions, slots, profile outlines, layouts and audits. Write a drawing-specific generator from the reviewed ledger. The fixed example command does not reconstruct a new user drawing.

## Verify saved files

Save the DXF, reopen it and inspect the DXF audit. Compare actual dimension measurements with independently recorded expected values. Check feature positions and counts separately: a correct distance can still be attached to the wrong features.

Check model units and print scale. A viewport at 1:100 should use a paper-space plot at 1:1. Render a PDF at the intended paper size, then inspect the full sheet and dense details for overlap, clipping and unreadable text.

## Review and delivery

| Deliverable | Minimum review |
| --- | --- |
| DXF | Opens in a DXF-aware application; native geometry and dimensions remain editable |
| PDF | Correct paper size and scale; legible text; all required views included |
| Ledger | Confirmed and unresolved source information clearly separated |
| Verification note | Actual tests, units, scale, open questions and application testing status |

Native AutoCAD testing, source fidelity, numerical consistency and file integrity are different claims. Report only the checks actually performed. A successful audit does not validate a structural design or prove that missing source dimensions were correct.

## DWG output

Use AutoCAD or a working CAD converter to create a genuine DWG. When only DXF is available, label it DXF and explain the conversion path. Keep the editable DXF as the portable deliverable; never change its extension to imitate DWG.
