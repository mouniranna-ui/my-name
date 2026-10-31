#!/usr/bin/env python3
"""Portable CAD authoring/checking helpers. This is not an image tracer."""
from __future__ import annotations

import argparse
import importlib.metadata
import importlib.util
import json
import math
from pathlib import Path
import shutil
import sys


def finite(value, label="value"):
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{label} must be finite")
    return result


def positive(value, label="value"):
    result = finite(value, label)
    if result <= 0:
        raise ValueError(f"{label} must be positive")
    return result


def _ezdxf():
    try:
        import ezdxf
        return ezdxf
    except ImportError as exc:
        raise RuntimeError("ezdxf is missing; see scripts/requirements.txt") from exc


def slope_basis(percent):
    """Return angle in radians, tangent and upward normal for a percent slope."""
    angle = math.atan(finite(percent, "percent") / 100)
    c, s = math.cos(angle), math.sin(angle)
    return angle, (c, s), (-s, c)


def i_section_vertices(h, b, tw, tf, r):
    """Return (x,y,bulge) vertices; centroid x=0, bottom y=0, units unchanged."""
    h, b, tw, tf = (positive(v, n) for v, n in zip((h,b,tw,tf), ("h","b","tw","tf")))
    r = finite(r, "r")
    if r < 0 or h <= 2*(tf+r) or b <= tw+2*r:
        raise ValueError("Invalid I-section envelope, thickness or root radius")
    w, half, q = tw/2, b/2, math.tan(math.pi/8) if r else 0
    raw = [(-half,0,0),(half,0,0),(half,tf,0),(w+r,tf,-q),
           (w,tf+r,0),(w,h-tf-r,-q),(w+r,h-tf,0),(half,h-tf,0),
           (half,h,0),(-half,h,0),(-half,h-tf,0),(-w-r,h-tf,-q),
           (-w,h-tf-r,0),(-w,tf+r,-q),(-w-r,tf,0),(-half,tf,0)]
    result = []
    for point in raw:
        if not result or point[:2] != result[-1][:2]:
            result.append(point)
    return result


def _dimension_text_is_measured(text):
    return text is None or text == "" or "<>" in text


class CadDrawing:
    """Create a new mm drawing; source interpretation remains the author's job."""

    def __init__(self, title="Technical drawing", plot_scale=2):
        ezdxf = _ezdxf()
        self.plot_scale = positive(plot_scale, "plot_scale")
        self.doc = ezdxf.new("R2013", setup=True)
        self.doc.units = 4
        for name, value in {"$INSUNITS":4,"$MEASUREMENT":1,"$LUNITS":2,
                            "$LUPREC":3,"$AUNITS":0,"$AUPREC":3,
                            "$DIMASSOC":1,"$LTSCALE":1,"$PSLTSCALE":1,
                            "$LWDISPLAY":True,"$FILLMODE":1}.items():
            self.doc.header[name] = value
        self.doc.header["$PROJECTNAME"] = str(title)
        self.doc.linetypes.new("CAD_AXIS", dxfattribs={"description":"Centre line",
            "pattern":[13*self.plot_scale,8*self.plot_scale,-2*self.plot_scale,
                       self.plot_scale,-2*self.plot_scale]})
        self.doc.linetypes.new("CAD_HIDDEN", dxfattribs={"description":"Hidden line",
            "pattern":[5*self.plot_scale,3*self.plot_scale,-2*self.plot_scale]})
        layers = {"OUTLINE":(7,35,"Continuous"),"AXES":(4,13,"CAD_AXIS"),
                  "HIDDEN":(8,18,"CAD_HIDDEN"),"HATCH":(8,13,"Continuous"),
                  "DIMENSIONS":(3,18,"Continuous"),"NOTES":(2,18,"Continuous"),
                  "GRAPHIC_UNDIMENSIONED":(8,25,"Continuous"),
                  "FRAME":(7,35,"Continuous"),"VIEWPORT_NP":(8,13,"Continuous")}
        for name,(color,weight,linetype) in layers.items():
            self.doc.layers.new(name,dxfattribs={"color":color,"lineweight":weight,
                "linetype":linetype,"plot":int(name!="VIEWPORT_NP")})
        self.doc.styles.new("CAD_TEXT",dxfattribs={"font":"arial.ttf"})
        self.doc.dimstyles.new("CAD_MM",dxfattribs={
            "dimtxsty":"CAD_TEXT","dimtxt":2.5*self.plot_scale,
            "dimasz":1.5*self.plot_scale,"dimexo":self.plot_scale,
            "dimexe":1.5*self.plot_scale,"dimgap":0.7*self.plot_scale,
            "dimtad":1,"dimdec":3,"dimzin":8,"dimdsep":44,
            "dimtih":0,"dimtoh":0,"dimatfit":3,"dimscale":1,"dimlfac":1,
            "dimclrd":0,"dimclre":0,"dimclrt":0,"dimlwd":18,"dimlwe":13,
        })
        self.manifest = {"schema":1,"units":4,"title":str(title),
                         "dimensions":[],"features":[],"plot":None}

    def register_dimension(self, dim, ident, *, expected, source,
                           status="source", anchors=None, tolerance=1e-6):
        if any(item["id"] == ident for item in self.manifest["dimensions"]):
            raise ValueError(f"Duplicate dimension id: {ident}")
        if status not in {"source","derived","standard"}:
            raise ValueError("Unresolved/graphic values must not be validated dimensions")
        if not str(source).strip():
            raise ValueError("Record inspected source evidence or a derivation")
        expected = finite(expected, "expected")
        if expected < 0:
            raise ValueError("Expected dimensions cannot be negative")
        entity = dim.dimension if hasattr(dim, "dimension") else dim
        if entity.dxftype() != "DIMENSION":
            raise ValueError("A native DIMENSION is required")
        if not _dimension_text_is_measured(entity.dxf.get("text", "")):
            raise ValueError("Hard-coded dimension text is not permitted; use <>")
        if hasattr(dim, "render"):
            dim.render()
        self.manifest["dimensions"].append({"id":str(ident),"handle":entity.dxf.handle,
            "expected":expected,"source":str(source),"status":status,
            "anchors":anchors,"tolerance":positive(tolerance,"tolerance")})
        return entity

    def linear_dimension(self, ident, p1, p2, *, base, expected, source,
                         angle=0, text="<>", status="source", anchors=None,
                         location=None):
        if not _dimension_text_is_measured(text):
            raise ValueError("Use <> for the measured dimension")
        dim = self.doc.modelspace().add_linear_dim(base=base,p1=p1,p2=p2,
            angle=finite(angle),text=text,dimstyle="CAD_MM",
            dxfattribs={"layer":"DIMENSIONS"})
        if location is not None:
            dim.set_location(location,leader=True,relative=False)
        return self.register_dimension(dim,ident,expected=expected,source=source,
                                       status=status,anchors=anchors)

    def aligned_dimension(self, ident, p1, p2, *, distance, expected, source,
                          text="<>", status="source", anchors=None, location=None):
        if not _dimension_text_is_measured(text):
            raise ValueError("Use <> for the measured dimension")
        dim = self.doc.modelspace().add_aligned_dim(p1,p2,distance=finite(distance),
            text=text,dimstyle="CAD_MM",dxfattribs={"layer":"DIMENSIONS"})
        if location is not None:
            dim.set_location(location,leader=True,relative=False)
        return self.register_dimension(dim,ident,expected=expected,source=source,
                                       status=status,anchors=anchors)

    def slot(self, center, width, overall_length, layer="OUTLINE"):
        width, length = positive(width,"width"), positive(overall_length,"overall_length")
        if length < width:
            raise ValueError("Overall slot length cannot be less than its width")
        x,y = (finite(v) for v in center)
        r, low, high = width/2, y-length/2+width/2, y+length/2-width/2
        ms = self.doc.modelspace()
        if length == width:
            return [ms.add_circle((x,y),r,dxfattribs={"layer":layer})]
        return [ms.add_line((x-r,low),(x-r,high),dxfattribs={"layer":layer}),
                ms.add_line((x+r,low),(x+r,high),dxfattribs={"layer":layer}),
                ms.add_arc((x,high),r,0,180,dxfattribs={"layer":layer}),
                ms.add_arc((x,low),r,180,360,dxfattribs={"layer":layer})]

    def circle_check(self, ident, circles, *, expected_radius, tolerance=1e-6):
        self.manifest["features"].append({"id":str(ident),"type":"circle_radius",
            "handles":[e.dxf.handle for e in circles],
            "expected":positive(expected_radius,"expected_radius"),
            "tolerance":positive(tolerance,"tolerance")})

    def line_slope_check(self, ident, line, *, expected_ratio, tolerance=1e-9):
        self.manifest["features"].append({"id":str(ident),"type":"line_slope",
            "handle":line.dxf.handle,"expected":finite(expected_ratio),
            "tolerance":positive(tolerance,"tolerance")})

    def count_check(self, ident, query, *, expected):
        if int(expected) != expected or expected < 0:
            raise ValueError("Expected count must be a nonnegative integer")
        self.manifest["features"].append({"id":str(ident),"type":"count",
            "query":str(query),"expected":int(expected)})

    def configure_layout(self, *, paper_width=420, paper_height=297,
                         view_center=None, name="Print"):
        w,h = positive(paper_width),positive(paper_height)
        center = view_center if view_center is not None else (w*self.plot_scale/2,h*self.plot_scale/2)
        center = [finite(v) for v in center]
        if len(center)!=2:
            raise ValueError("view_center must have two coordinates")
        if name in self.doc.layouts:
            page = self.doc.layouts.get(name)
        else:
            page = self.doc.layouts.new(name)
        page.page_setup(size=(w,h),margins=(0,0,0,0),units="mm",scale=(1,1),
                        name="CAD_CUSTOM",device="DWG To PDF.pc3")
        page.dxf_layout.dxf.plot_type=5
        vp=page.add_viewport(center=(w/2,h/2),size=(w,h),view_center_point=center,
            view_height=h*self.plot_scale,status=2,dxfattribs={"layer":"VIEWPORT_NP"})
        vp.dxf.flags |= 16384
        self.doc.set_modelspace_vport(height=h*self.plot_scale*1.03,center=center)
        self.manifest["plot"]={"layout":name,"paper_width":w,"paper_height":h,
            "scale":self.plot_scale,"view_center":center,"viewport_handle":vp.dxf.handle}
        return page

    def save(self, dxf_path, manifest_path):
        dxf_path, manifest_path = Path(dxf_path), Path(manifest_path)
        dxf_path.parent.mkdir(parents=True,exist_ok=True)
        manifest_path.parent.mkdir(parents=True,exist_ok=True)
        self.doc.saveas(dxf_path)
        manifest_path.write_text(json.dumps(self.manifest,ensure_ascii=False,indent=2),encoding="utf-8")
        result=audit_dxf(dxf_path,manifest_path)
        if not result["passed"]:
            raise ValueError("Saved CAD failed checks: "+"; ".join(result["issues"]))
        return result


def audit_dxf(dxf_path, manifest_path=None):
    doc=_ezdxf().readfile(dxf_path)
    audit=doc.audit()
    issues=[]
    if audit.errors or audit.fixes:
        issues.append(f"DXF audit: {len(audit.errors)} errors, {len(audit.fixes)} automatic fixes")
    native=list(doc.modelspace().query("DIMENSION"))
    for dim in native:
        if not _dimension_text_is_measured(dim.dxf.get("text","")):
            issues.append(f"Dimension {dim.dxf.handle} has a hard-coded text replacement")
    measurements=[]
    features=[]
    manifest=json.loads(Path(manifest_path).read_text(encoding="utf-8")) if manifest_path else None
    if manifest is not None:
        if doc.units != manifest["units"]:
            issues.append("Model units differ from the check manifest")
        registered=set()
        for item in manifest["dimensions"]:
            try:
                expected=finite(item["expected"])
                ent=doc.entitydb[item["handle"]]
                if ent.dxftype()!="DIMENSION": raise ValueError("Handle is not a DIMENSION")
                value=finite(ent.get_measurement())
                if item.get("status") not in {"source","derived","standard"}:
                    raise ValueError("Unresolved dimension incorrectly registered as verified")
                if abs(value-expected)>positive(item["tolerance"]):
                    raise ValueError(f"Measured {value:g}, expected {expected:g}")
                registered.add(item["handle"])
                measurements.append({"id":item["id"],"measured":value,"expected":expected})
            except Exception as exc:
                issues.append(f"{item.get('id','dimension')}: {exc}")
        uncovered={d.dxf.handle for d in native}-registered
        if uncovered: issues.append(f"{len(uncovered)} native dimensions lack passing registered checks")
        for item in manifest["features"]:
            try:
                kind=item["type"]
                if kind=="circle_radius":
                    if not item["handles"]: raise ValueError("Empty circle check")
                    for handle in item["handles"]:
                        ent=doc.entitydb[handle]
                        if ent.dxftype()!="CIRCLE": raise ValueError("Handle is not a CIRCLE")
                        if abs(finite(ent.dxf.radius,"circle radius")-finite(item["expected"]))>positive(item["tolerance"]):
                            raise ValueError("Circle radius mismatch")
                elif kind=="line_slope":
                    ent=doc.entitydb[item["handle"]]
                    if ent.dxftype()!="LINE": raise ValueError("Handle is not a LINE")
                    dx=finite(ent.dxf.end.x-ent.dxf.start.x,"line delta x")
                    if abs(dx)<1e-12: raise ValueError("Cannot compare a vertical line to a finite slope")
                    value=finite((ent.dxf.end.y-ent.dxf.start.y)/dx,"line slope")
                    if abs(value-finite(item["expected"]))>positive(item["tolerance"]):
                        raise ValueError("Line slope mismatch")
                elif kind=="count":
                    if len(doc.modelspace().query(item["query"]))!=item["expected"]:
                        raise ValueError("Entity count mismatch")
                else: raise ValueError(f"Unknown feature check {kind}")
                features.append(item["id"])
            except Exception as exc:
                issues.append(f"{item.get('id','feature')}: {exc}")
        plot=manifest.get("plot")
        if plot:
            try:
                page=doc.layouts.get(plot["layout"])
                p=page.dxf_layout.dxf
                vp=doc.entitydb[plot["viewport_handle"]]
                for actual, expected, label in [
                    (p.scale_numerator,1,"plot numerator"),(p.scale_denominator,1,"plot denominator"),
                    (p.paper_width,plot["paper_width"],"paper width"),
                    (p.paper_height,plot["paper_height"],"paper height"),
                    (vp.dxf.view_height/vp.dxf.height,plot["scale"],"viewport ratio")]:
                    if abs(finite(actual,label)-finite(expected,label))>1e-8:
                        raise ValueError(f"Incorrect {label}")
                if not vp.dxf.flags & 16384: raise ValueError("Viewport is not locked")
            except Exception as exc: issues.append(f"Plot settings: {exc}")
    return {"passed":not issues,"issues":issues,"audit_errors":len(audit.errors),
            "audit_fixes":len(audit.fixes),"native_dimensions":len(native),
            "measurements":measurements,"feature_checks":features,
            "source_fidelity":"requires visual source-and-anchor review",
            "native_autocad_test":"not performed by this helper"}


def render_preview(dxf_path, manifest_path, pdf_path, png_path, *, dpi=144):
    from ezdxf.addons.drawing import Frontend, RenderContext, layout, config
    from ezdxf.addons.drawing.pymupdf import PyMuPdfBackend, PyMuPdfRenderBackend
    from ezdxf.math import BoundingBox2d
    import fitz
    manifest=json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    plot=manifest.get("plot")
    if not plot: raise ValueError("Configure a plot layout before rendering a scaled preview")
    w,h,scale=(positive(plot[k]) for k in ("paper_width","paper_height","scale"))
    cx,cy=plot["view_center"]
    doc=_ezdxf().readfile(dxf_path)
    backend=PyMuPdfBackend()
    cfg=config.Configuration(color_policy=config.ColorPolicy.BLACK,
        background_policy=config.BackgroundPolicy.WHITE,min_lineweight=0.08)
    Frontend(RenderContext(doc),backend,config=cfg).draw_layout(doc.modelspace(),finalize=True)
    box=BoundingBox2d([(cx-w*scale/2,cy-h*scale/2),(cx+w*scale/2,cy+h*scale/2)])
    pdf_path,png_path=Path(pdf_path),Path(png_path)
    pdf_path.parent.mkdir(parents=True,exist_ok=True)
    png_path.parent.mkdir(parents=True,exist_ok=True)
    # ezdxf 1.4.4's convenience exporter rounds the page and coordinate space
    # to integer PDF points. Use fractional points to retain exact paper scale.
    page=layout.Page(w,h)
    settings=layout.Settings(fit_page=True,output_layers=True,
        output_coordinate_space=max(w,h)*72/25.4)
    placement=layout.Layout(box,flip_y=True)
    player=backend.player()
    player.transform(placement.get_placement_matrix(page,settings=settings,top_origin=True))
    renderer=PyMuPdfRenderBackend(page,settings)
    renderer.page_width_in_pt=w*72/25.4
    renderer.page_height_in_pt=h*72/25.4
    renderer.page.set_mediabox(fitz.Rect(0,0,renderer.page_width_in_pt,renderer.page_height_in_pt))
    renderer.content_shape=renderer.page.new_shape()
    player.replay(renderer)
    # Export once. Render PNG from this PDF, never from the transformed player.
    pdf_path.write_bytes(renderer.get_pdf_bytes())
    with fitz.open(pdf_path) as pdf:
        pdf[0].get_pixmap(dpi=int(positive(dpi,"dpi"))).save(png_path)
    return {"pdf":str(pdf_path),"png":str(png_path)}


def example(output_dir):
    spec=json.loads((Path(__file__).resolve().parents[1]/"assets"/"plate_example.json").read_text())
    out=Path(output_dir)
    out.mkdir(parents=True,exist_ok=True)
    d=CadDrawing(title=spec["title"],plot_scale=1)
    ms=d.doc.modelspace()
    w,h=spec["width"],spec["height"]
    ms.add_lwpolyline([(0,0),(w,0),(w,h),(0,h)],close=True,dxfattribs={"layer":"OUTLINE"})
    circles=[]
    for y in spec["row_centres"]:
        for x in spec["column_centres"]:
            circles.append(ms.add_circle((x,y),spec["hole_diameter"]/2,dxfattribs={"layer":"OUTLINE"}))
    d.linear_dimension("plate.width",(0,h),(w,h),base=(0,254),expected=w,source="Synthetic fixture: width")
    d.linear_dimension("plate.height",(0,0),(0,h),base=(-20,0),angle=90,expected=h,source="Synthetic fixture: height")
    d.linear_dimension("holes.column_pitch",(30,30),(90,30),base=(0,-10),expected=60,source="Synthetic fixture: columns")
    d.linear_dimension("holes.row_pitch",(90,30),(90,90),base=(136,0),angle=90,expected=60,source="Synthetic fixture: rows")
    d.circle_check("holes.radius",circles,expected_radius=6)
    d.count_check("holes.count","CIRCLE",expected=8)
    ms.add_text("SYNTHETIC EXAMPLE / mm / 1:1",dxfattribs={"style":"CAD_TEXT","height":3,"layer":"NOTES"}).set_placement((-30,-21))
    ms.add_lwpolyline([(-40,-24),(160,-24),(160,264),(-40,264)],close=True,dxfattribs={"layer":"FRAME"})
    d.configure_layout(paper_width=210,paper_height=297,view_center=(60,120))
    dxf,manifest=out/"example_plate.dxf",out/"example_plate.checks.json"
    report=d.save(dxf,manifest)
    render_preview(dxf,manifest,out/"example_plate.pdf",out/"example_plate.png")
    (out/"example_plate.audit.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    return {"dxf":str(dxf),"checks":str(manifest),"audit":report}


def doctor():
    packages={}
    for distribution,module in [("ezdxf","ezdxf"),("PyMuPDF","fitz"),("Pillow","PIL")]:
        try: version=importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError: version=None
        packages[distribution]={"available":importlib.util.find_spec(module) is not None,"version":version}
    return {"python":sys.version.split()[0],"packages":packages,
            "converters":{name:bool(shutil.which(name)) for name in ["ODAFileConverter","dwgwrite","accoreconsole"]},
            "dwg":"A genuine converter is required; DXF is the portable default"}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest="command",required=True)
    sub.add_parser("doctor")
    p=sub.add_parser("example");p.add_argument("--output-dir",required=True)
    p=sub.add_parser("audit");p.add_argument("dxf");p.add_argument("--manifest")
    p=sub.add_parser("render");p.add_argument("dxf");p.add_argument("--manifest",required=True)
    p.add_argument("--pdf",required=True);p.add_argument("--png",required=True)
    args=parser.parse_args()
    if args.command=="doctor": result=doctor()
    elif args.command=="example": result=example(args.output_dir)
    elif args.command=="audit": result=audit_dxf(args.dxf,args.manifest)
    else: result=render_preview(args.dxf,args.manifest,args.pdf,args.png)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if result.get("passed") is False: return 1
    return 0


if __name__=="__main__":
    raise SystemExit(main())
