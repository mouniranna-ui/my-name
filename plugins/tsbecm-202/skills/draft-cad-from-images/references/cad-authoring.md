# Native CAD authoring

## Helper API

Add the actual skill `scripts` directory to `sys.path` in a task-local generator. Do not edit the installed skill to implement a user's drawing.

`CadDrawing` creates millimetre models. Convert other source units explicitly and record the conversion, or use a CAD setup configured for those units. Changing only `$INSUNITS` does not convert existing geometry.

```python
from cad_tools import CadDrawing, slope_basis, i_section_vertices
d = CadDrawing(title="Connection", plot_scale=5)
m = d.doc.modelspace()
m.add_line((0, 0), (100, 0), dxfattribs={"layer": "OUTLINE"})
d.linear_dimension(
    "length", (0, 0), (100, 0), base=(0, -20),
    expected=100, source="drawing.jpg: inspected length dimension",
)
d.save("drawing.dxf", "drawing.checks.json")
```

Supply real inspected evidence in `source`. Read expected values from the source ledger independently. The helpers provide `linear_dimension`, `aligned_dimension`, `register_dimension` for specialized native dimensions, `circle_check`, `line_slope_check`, `slot`, `configure_layout`, and `save`. Standalone functions provide `audit_dxf`, `render_preview`, `slope_basis`, and `i_section_vertices`.

## Geometry

Use shared full-size parameters and rigid transforms for related views. A member's normal depth differs from vertical projection when inclined. `slope_basis(percent)` returns the angle and unit vectors along and normal to the member. `i_section_vertices(h,b,tw,tf,r)` returns a closed I-section outline with concave circular fillets. Supply independently verified values and preserve bulges when transforming it.

Use ARC and CIRCLE rather than polygonal approximations. Reuse fastener blocks. Hatches supplement closed section geometry. Keep schematic outlines on `GRAPHIC_UNDIMENSIONED`.

## Dimensions and text

Dimension text height in model units equals intended paper height times plot scale: 2.5 mm x 5 = 12.5 at 1:5. Lineweights are plotted millimetres. Choose a common CAD font and inspect substituted fonts in the preview. For Arabic translation, verify shaping, direction and recipient font support; a good PDF alone does not prove native TEXT renders correctly.

`<>` displays measured values; `(<>)` marks derived reference measurements. The helper rejects replacement dimension text without `<>`. Dimensions are native and editable, but non-associative unless an actual association is implemented.

## Layout and rendering

Set `configure_layout` with paper dimensions, view centre and scale denominator. Paper-space scale is `(1,1)`. Viewport height is paper height times denominator. Lock it. Render the same view box instead of auto-fitting arbitrary extents. Keep all intended sheet content inside that box.

Export once per PyMuPDF backend; make PNG from the resulting PDF because a second backend export can transform already transformed coordinates.

The bundled renderer uses fractional PDF points for exact paper dimensions; the ezdxf 1.4.4 convenience exporter rounds these. If changing the renderer, check both the PDF page size and a known plotted geometric length. The bundled numerical regression suite can be run with `python <skill-directory>/scripts/test_cad_tools.py`; it does not substitute for reviewing the user's source.

## DWG

Discover a genuine authorized local CAD application or converter. Use its documented interface. With ODA installed, inspect the installed `ezdxf.addons.odafc` interface and use its supported conversion workflow. Reopen DWG or round-trip a copy to DXF; compare units, geometry, dimension measurements, layers and views. Conversion can change handles, so compare semantics. A nonempty file and header check alone do not prove interoperability.

If unavailable, deliver DXF explicitly and explain AutoCAD `SAVEAS`. Never fabricate a DWG extension, use an untrusted converter, or upload source drawings to an online service without authorization.
