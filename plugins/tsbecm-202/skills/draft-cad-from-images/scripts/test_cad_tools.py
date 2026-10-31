"""Numerical regression checks; these do not prove fidelity to an input image."""
import copy
import json
import math
from pathlib import Path
import tempfile
import unittest

import ezdxf
from ezdxf import bbox

from cad_tools import CadDrawing, audit_dxf, i_section_vertices, render_preview, slope_basis


class CadChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.dxf = self.root / "drawing.dxf"
        self.manifest = self.root / "drawing.checks.json"
        self.d = CadDrawing(plot_scale=2)
        ms = self.d.doc.modelspace()
        ms.add_lwpolyline([(0,0),(100,0),(100,80),(0,80)],close=True,
                         dxfattribs={"layer":"OUTLINE"})
        self.dim = self.d.linear_dimension("width",(0,0),(100,0),base=(0,-12),
                                          expected=100,source="Synthetic width")
        self.circle = ms.add_circle((20,30),6,dxfattribs={"layer":"OUTLINE"})
        self.line = ms.add_line((0,0),(100,26.4),dxfattribs={"layer":"OUTLINE"})
        self.d.circle_check("hole",[self.circle],expected_radius=6)
        self.d.count_check("holes","CIRCLE",expected=1)
        self.d.line_slope_check("slope",self.line,expected_ratio=.264)
        self.d.configure_layout(paper_width=210,paper_height=297,view_center=(50,40))
        self.d.save(self.dxf,self.manifest)

    def tearDown(self):
        self.temp.cleanup()

    def mutated(self, mutate):
        doc=ezdxf.readfile(self.dxf)
        mutate(doc)
        target=self.root/"mutated.dxf"
        doc.saveas(target)
        return audit_dxf(target,self.manifest)

    def test_saved_document_and_measured_dimension(self):
        report=audit_dxf(self.dxf,self.manifest)
        self.assertTrue(report["passed"],report)
        self.assertEqual(report["native_dimensions"],1)
        self.assertEqual(report["measurements"][0]["measured"],100)
        self.assertIn("requires visual",report["source_fidelity"])
        self.assertEqual(report["audit_fixes"],0)

    def test_geometry_and_text_mismatches_fail(self):
        changes=[
            lambda doc:setattr(doc.entitydb[self.dim.dxf.handle].dxf,"defpoint3",(101,0,0)),
            lambda doc:setattr(doc.entitydb[self.dim.dxf.handle].dxf,"text","100"),
            lambda doc:doc.entitydb.delete_entity(doc.entitydb[self.dim.dxf.handle]),
        ]
        for change in changes:
            with self.subTest(change=change):
                self.assertFalse(self.mutated(change)["passed"])
        with self.assertRaises(ValueError):
            self.d.linear_dimension("fake",(0,0),(5,0),base=(0,0),
                                    expected=100,source="Synthetic",text="100")
        with self.assertRaises(ValueError):
            self.d.linear_dimension("unknown",(0,0),(5,0),base=(0,0),
                                    expected=5,source="Synthetic",status="unresolved")

    def test_circle_slope_and_count_changes_fail(self):
        changes=[
            lambda doc:setattr(doc.entitydb[self.circle.dxf.handle].dxf,"radius",7),
            lambda doc:setattr(doc.entitydb[self.circle.dxf.handle].dxf,"radius",float("nan")),
            lambda doc:setattr(doc.entitydb[self.line.dxf.handle].dxf,"end",(100,27,0)),
            lambda doc:setattr(doc.entitydb[self.line.dxf.handle].dxf,"end",(0,27,0)),
            lambda doc:setattr(doc.entitydb[self.line.dxf.handle].dxf,"end",(100,float("nan"),0)),
            lambda doc:doc.modelspace().add_circle((60,30),6),
        ]
        for change in changes:
            with self.subTest(change=change):
                self.assertFalse(self.mutated(change)["passed"])

    def test_units_and_plot_changes_fail(self):
        vp=self.d.manifest["plot"]["viewport_handle"]
        changes=[
            lambda doc:setattr(doc,"units",1),
            lambda doc:setattr(doc.layouts.get("Print").dxf_layout.dxf,"scale_denominator",5),
            lambda doc:doc.layouts.get("Print").page_setup(size=(210,297),scale=1),
            lambda doc:setattr(doc.entitydb[vp].dxf,"view_height",500),
            lambda doc:setattr(doc.entitydb[vp].dxf,"flags",0),
        ]
        for change in changes:
            with self.subTest(change=change):
                self.assertFalse(self.mutated(change)["passed"])

    def test_missing_check_or_handle_fails(self):
        for mutation in ("unregistered","bad_handle","nonfinite_expected"):
            spec=copy.deepcopy(self.d.manifest)
            if mutation=="unregistered": spec["dimensions"]=[]
            elif mutation=="bad_handle": spec["dimensions"][0]["handle"]="F0000"
            else: spec["dimensions"][0]["expected"]=float("nan")
            path=self.root/"bad.checks.json"
            path.write_text(json.dumps(spec))
            self.assertFalse(audit_dxf(self.dxf,path)["passed"])

    def test_slot_uses_true_arcs_and_overall_length(self):
        entities=self.d.slot((30,40),16,54)
        ext=bbox.extents(entities)
        self.assertAlmostEqual(ext.size.x,16)
        self.assertAlmostEqual(ext.size.y,54)
        arcs=[e for e in entities if e.dxftype()=="ARC"]
        self.assertEqual(len(arcs),2)
        self.assertEqual([e.dxf.radius for e in arcs],[8,8])
        self.assertEqual(abs(arcs[0].dxf.center.y-arcs[1].dxf.center.y),38)
        self.assertEqual(self.d.slot((0,0),16,16)[0].dxftype(),"CIRCLE")
        with self.assertRaises(ValueError): self.d.slot((0,0),16,15)

    def test_i_section_root_arcs_and_envelope(self):
        # Synthetic section dimensions, not a standard profile lookup.
        vertices=i_section_vertices(200,100,8,12,10)
        poly=self.d.doc.modelspace().add_lwpolyline(vertices,format="xyb",close=True)
        entities=list(poly.virtual_entities())
        ext=bbox.extents(entities)
        self.assertAlmostEqual(ext.size.x,100)
        self.assertAlmostEqual(ext.size.y,200)
        arcs=[e for e in entities if e.dxftype()=="ARC"]
        self.assertEqual(len(arcs),4)
        for arc in arcs: self.assertAlmostEqual(arc.dxf.radius,10)
        self.assertTrue(all(v[2]<0 for v in vertices if v[2]))
        self.assertEqual(len(i_section_vertices(200,100,8,12,0)),12)
        with self.assertRaises(ValueError): i_section_vertices(20,100,8,12,10)

    def test_percent_slope_basis(self):
        angle,tangent,normal=slope_basis(26.4)
        self.assertAlmostEqual(math.degrees(angle),14.7886776142,places=8)
        self.assertAlmostEqual(tangent[1]/tangent[0],.264)
        self.assertAlmostEqual(sum(a*b for a,b in zip(tangent,normal)),0)
        with self.assertRaises(ValueError): slope_basis(float("inf"))

    def test_preview_has_correct_page_and_visible_geometry(self):
        import fitz
        from PIL import Image, ImageChops
        pdf,png=self.root/"drawing.pdf",self.root/"drawing.png"
        render_preview(self.dxf,self.manifest,pdf,png,dpi=96)
        with fitz.open(pdf) as f:
            self.assertEqual(len(f),1)
            self.assertAlmostEqual(f[0].rect.width*25.4/72,210,places=3)
            self.assertAlmostEqual(f[0].rect.height*25.4/72,297,places=3)
            self.assertGreater(len(f[0].get_drawings()),5)
            # The 100 mm outline at 1:2 must span 50 paper millimetres.
            spans=[path["rect"].width*25.4/72 for path in f[0].get_drawings()]
            self.assertTrue(any(abs(span-50)<.001 for span in spans))
        img=Image.open(png).convert("RGB")
        bounds=ImageChops.difference(img,Image.new("RGB",img.size,"white")).getbbox()
        self.assertIsNotNone(bounds)
        self.assertGreater(bounds[2]-bounds[0],150)
        self.assertGreater(bounds[3]-bounds[1],100)


if __name__=="__main__":
    unittest.main(verbosity=2)
