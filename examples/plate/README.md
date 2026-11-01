# Synthetic plate example

This fixture is a deliberately created technical drawing, not a customer's document.

- `source.png`: the dimensioned reference.
- `drawing.dxf`: editable native CAD reconstruction.
- `preview.pdf`: vector A3 portrait preview at 1:1.
- `preview.png`: rendered preview of that PDF.

Known geometry: 160 × 280 mm rectangle; two hole columns at x=40 and 120 mm; four rows at y=35, 105, 175 and 245 mm; hole diameter 14 mm. The slot is centered at (80,140), width 16 mm, overall length 54 mm, end radius 8 mm, arc-center spacing 38 mm.

Fifteen native dimensions were checked after DXF save/reopen. The DXF audit reported no errors or automatic fixes. Source anchors and the PDF were visually reviewed. No native Autodesk AutoCAD application test was performed.

Thickness, material and manufacturing tolerances are not supplied. Their omission is marked in the drawing. This example demonstrates reconstruction and checking; it is not a certified manufacturing drawing.

To regenerate a separate, simpler helper demonstration, run `python tools/cad.py example --output-dir demo-output` from the repository root. That command uses its own synthetic fixture and does not recreate this exact plate.
