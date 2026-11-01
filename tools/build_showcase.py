#!/usr/bin/env python3
"""Build the synthetic workshop showcase, editable CAD, PDFs and audit evidence."""
from pathlib import Path
import argparse
import importlib.util
import json
import math
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'plugins/tsbecm-202/skills/draft-cad-from-images/scripts'
sys.path.insert(0, str(SCRIPTS))
from cad_tools import CadDrawing, render_preview
from ezdxf.enums import TextEntityAlignment
import ezdxf
import fitz

SPEC = ROOT / 'examples/industrial-workshop/specification.json'


def label(ms, text, point, height, layer='NOTES', align='LEFT'):
    return ms.add_text(text, dxfattribs={'style':'CAD_TEXT','height':height,'layer':layer}).set_placement(point, align=getattr(TextEntityAlignment, align))


def line(ms, a, b, layer='OUTLINE'):
    return ms.add_line(a,b,dxfattribs={'layer':layer})


def box(ms,x,y,w,h,layer='OUTLINE'):
    return ms.add_lwpolyline([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],close=True,dxfattribs={'layer':layer})


def sheet(number, title, scale, paper=(594,420)):
    d=CadDrawing(title='TSBECM 202 | '+title,plot_scale=scale)
    ms=d.doc.modelspace();w,h=paper
    box(ms,8*scale,8*scale,(w-16)*scale,(h-16)*scale,'FRAME')
    label(ms,'TSBECM 202', (16*scale,(h-25)*scale),7*scale)
    label(ms,title.upper(), (16*scale,(h-37)*scale),3.5*scale)
    label(ms,'SYNTHETIC DRAFTING STUDY | NOT FOR CONSTRUCTION',((w-16)*scale,(h-25)*scale),2.7*scale,align='RIGHT')
    line(ms,(8*scale,62*scale),((w-8)*scale,62*scale),'FRAME')
    label(ms,'INDUSTRIAL WORKSHOP  /  24 m x 36 m', (16*scale,47*scale),4*scale)
    label(ms,'Native geometry + dimensions | Model: mm | Plot at 100% / actual size', (16*scale,35*scale),2.7*scale)
    label(ms,'Member outlines, bracing and plate patterns are educational drafting inputs.', (16*scale,24*scale),2.6*scale)
    label(ms,'No structural sizing, material grades, plate thicknesses or foundation design are provided.', (16*scale,14*scale),2.4*scale)
    label(ms,f'{number}  |  REV A',((w-16)*scale,47*scale),4.5*scale,align='RIGHT')
    label(ms,f'SCALE 1:{scale:g}  |  {w} x {h} mm',((w-16)*scale,35*scale),2.7*scale,align='RIGHT')
    d.configure_layout(paper_width=w,paper_height=h,view_center=(w*scale/2,h*scale/2),name=number)
    return d


def dim(d, ident,p1,p2,base,value,angle=0,status='source'):
    return d.linear_dimension(ident,p1,p2,base=base,expected=value,angle=angle,status=status,
        source='Synthetic specification.json: '+ident,anchors={'start':list(p1),'end':list(p2)})


def grid(ms,p,value,r=300):
    ms.add_circle(p,r,dxfattribs={'layer':'AXES'})
    label(ms,str(value),p,r*1.15,align='MIDDLE_CENTER')


def beam(ms,a,b,width):
    dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
    nx,ny=-dy/length*width/2,dx/length*width/2
    ms.add_lwpolyline([(a[0]+nx,a[1]+ny),(b[0]+nx,b[1]+ny),(b[0]-nx,b[1]-ny),(a[0]-nx,a[1]-ny)],close=True,dxfattribs={'layer':'GRAPHIC_UNDIMENSIONED'})


def make_plan(s):
    d=sheet('S01','Roof plan and structural grid',100);ms=d.doc.modelspace()
    ox,oy=9000,11000;L,W,bay=s['length'],s['span'],s['bay_spacing']
    box(ms,ox,oy,L,W)
    for i in range(s['frame_count']):
        x=ox+i*bay
        line(ms,(x,oy-650),(x,oy+W+650),'AXES')
        grid(ms,(x,oy+W+1250),i+1)
        for y in (oy,oy+W):box(ms,x-150,y-250,300,500)
        if i<s['frame_count']-1:
            dim(d,f'grid.bay.{i+1}',(x,oy),(x+bay,oy),(x,oy-1200),bay)
    dim(d,'grid.length',(ox,oy),(ox+L,oy),(ox,oy-2700),L)
    dim(d,'grid.span',(ox+L,oy),(ox+L,oy+W),(ox+L+2700,oy),W,90)
    for y,name in [(oy,'A'),(oy+W,'B')]:
        line(ms,(ox-800,y),(ox+L+700,y),'AXES');grid(ms,(ox-1400,y),name)
    for pos in range(0,W+1,s['purlin_plan_spacing']):
        y=oy+pos
        line(ms,(ox,y),(ox+L,y),'HIDDEN' if pos!=W/2 else 'AXES')
    for x in (ox,ox+L-bay):
        for y in (oy,oy+W/2):
            line(ms,(x,y),(x+bay,y+W/2),'GRAPHIC_UNDIMENSIONED')
            line(ms,(x+bay,y),(x,y+W/2),'GRAPHIC_UNDIMENSIONED')
    label(ms,'RIDGE LINE',(ox+L/2,oy+W/2+500),300,align='CENTER')
    label(ms,'PURLIN LINES @ 2400 PLAN SPACING',(ox+L/2,oy+W-1700),280,align='CENTER')
    label(ms,'7 FRAME LINES | 6 BAYS @ 6000',(ox+L/2,oy+W+2600),320,align='CENTER')
    return d


def make_elevations(s):
    d=sheet('S02','Transverse frame and longitudinal elevation',100);ms=d.doc.modelspace()
    W,L,E,bay=s['span'],s['length'],s['eaves_height'],s['bay_spacing']
    rise=W/2*s['roof_slope_percent']/100;R=E+rise
    ox,oy=9000,25500
    left=(ox,oy+E);ridge=(ox+W/2,oy+R);right=(ox+W,oy+E)
    for x in (ox,ox+W):
        beam(ms,(x,oy),(x,oy+E),s['graphic_member_depth'])
        box(ms,x-500,oy-450,1000,450,'GRAPHIC_UNDIMENSIONED')
    beam(ms,left,ridge,s['graphic_member_depth']);beam(ms,ridge,right,s['graphic_member_depth'])
    l=line(ms,left,ridge,'AXES');r=line(ms,ridge,right,'AXES')
    d.line_slope_check('roof.left_slope',l,expected_ratio=0.15)
    d.line_slope_check('roof.right_slope',r,expected_ratio=-0.15)
    line(ms,(ox-2000,oy),(ox+W+2200,oy),'AXES')
    dim(d,'frame.span',(ox,oy),(ox+W,oy),(ox,oy-2200),W)
    dim(d,'frame.eaves',(ox,oy),left,(ox-2200,oy),E,90)
    dim(d,'frame.ridge',(ox+W,oy),(ox+W,oy+R),(ox+W+2600,oy),R,90,'derived')
    label(ms,'TRANSVERSE FRAME  /  GRID 1-7',(ox,oy+R+1500),360)
    label(ms,'15% ROOF SLOPE',(ox+W/2,oy+R+650),280,align='CENTER')
    label(ms,'LEVEL +0.000',(ox-1600,oy+450),250)
    label(ms,'ILLUSTRATIVE MEMBER DEPTH: 300',(38000,32600),270)
    label(ms,'Roof rise = 12000 x 0.15 = 1800',(38000,31600),260)
    label(ms,'Ridge level = 6500 + 1800 = 8300',(38000,30600),260)
    label(ms,'Member sections are not selected.',(38000,29100),260)
    label(ms,'Refer to S03 for plate patterns.',(38000,28100),260)
    ox,oy=9000,11200
    for i in range(s['frame_count']):
        x=ox+i*bay
        beam(ms,(x,oy),(x,oy+E),s['graphic_member_depth'])
        grid(ms,(x,oy+E+900),i+1)
        box(ms,x-450,oy-350,900,350,'GRAPHIC_UNDIMENSIONED')
        if i<s['frame_count']-1:dim(d,f'elevation.bay.{i+1}',(x,oy),(x+bay,oy),(x,oy-1100),bay)
    line(ms,(ox,oy+E),(ox+L,oy+E))
    for y in (1500,3000,4500):line(ms,(ox,oy+y),(ox+L,oy+y),'HIDDEN')
    for x in (ox,ox+L-bay):
        line(ms,(x,oy),(x+bay,oy+E),'GRAPHIC_UNDIMENSIONED')
        line(ms,(x+bay,oy),(x,oy+E),'GRAPHIC_UNDIMENSIONED')
    dim(d,'elevation.length',(ox,oy),(ox+L,oy),(ox,oy-2600),L)
    dim(d,'elevation.height',(ox+L,oy),(ox+L,oy+E),(ox+L+2000,oy),E,90)
    label(ms,'LONGITUDINAL ELEVATION  /  AXIS A',(ox,oy+E+2000),360)
    return d


def make_details(s):
    d=sheet('S03','Dimensioned plate patterns',4,paper=(594,420));ms=d.doc.modelspace()
    for name in ['BASE_HOLES','END_HOLES']:d.doc.layers.new(name,dxfattribs={'color':7,'lineweight':25})
    x,y=350,600;b=s['base_plate'];w,h=b['width'],b['height'];edge=b['edge_distance']
    box(ms,x,y,w,h)
    circles=[]
    for xx in (edge,w-edge):
        for yy in (edge,h-edge):
            p=(x+xx,y+yy)
            circles.append(ms.add_circle(p,b['hole_diameter']/2,dxfattribs={'layer':'BASE_HOLES'}))
            line(ms,(p[0]-30,p[1]),(p[0]+30,p[1]),'AXES');line(ms,(p[0],p[1]-30),(p[0],p[1]+30),'AXES')
    line(ms,(x-25,y+h/2),(x+w+25,y+h/2),'AXES');line(ms,(x+w/2,y-25),(x+w/2,y+h+25),'AXES')
    dim(d,'base.width',(x,y),(x+w,y),(x,y-70),w)
    dim(d,'base.height',(x,y),(x,y+h),(x-70,y),h,90)
    dim(d,'base.edge',(x,y+h),(x+edge,y+h),(x,y+h+45),edge)
    dim(d,'base.pitch',(x+edge,y+h),(x+w-edge,y+h),(x,y+h+45),w-2*edge,status='derived')
    diameter=ms.add_diameter_dim(center=(x+edge,y+edge),radius=15,location=(x+180,y+180),dimstyle='CAD_MM',text='4x <>',dxfattribs={'layer':'DIMENSIONS'})
    d.register_dimension(diameter,'base.hole_diameter',expected=30,source='specification.json base_plate.hole_diameter')
    d.circle_check('base.hole_radii',circles,expected_radius=15);d.count_check('base.hole_count','CIRCLE[layer=="BASE_HOLES"]',expected=4)
    label(ms,'D01 / BASE PLATE PATTERN',(x,y+h+100),15)
    label(ms,'4 HOLES, DIAMETER 30',(x,y-120),12)
    label(ms,'THICKNESS / MATERIAL / ANCHORS: NOT SPECIFIED',(x,y-145),9.5)
    x,y=1450,600;b=s['end_plate'];w,h=b['width'],b['height'];box(ms,x,y,w,h)
    circles=[]
    for xx in b['x_centres']:
        line(ms,(x+xx,y-25),(x+xx,y+h+25),'AXES')
        for yy in b['y_centres']:
            p=(x+xx,y+yy);circles.append(ms.add_circle(p,b['hole_diameter']/2,dxfattribs={'layer':'END_HOLES'}))
            line(ms,(p[0]-25,p[1]),(p[0]+25,p[1]),'AXES')
    dim(d,'end.width',(x,y+h),(x+w,y+h),(x,y+h+60),w)
    dim(d,'end.height',(x+w,y),(x+w,y+h),(x+w+135,y),h,90)
    dim(d,'end.column_pitch',(x+70,y),(x+250,y),(x,y-50),180,status='derived')
    dim(d,'end.side_edge',(x,y),(x+70,y),(x,y-50),70)
    ys=[0]+b['y_centres']+[h]
    for i,(a,bv) in enumerate(zip(ys,ys[1:])):
        dim(d,f'end.row_chain.{i}',(x+w,y+a),(x+w,y+bv),(x+w+65,y+a),bv-a,90,status='derived')
    diameter=ms.add_diameter_dim(center=(x+70,y+220),radius=13,location=(x-120,y+250),dimstyle='CAD_MM',text='8x <>',dxfattribs={'layer':'DIMENSIONS'})
    d.register_dimension(diameter,'end.hole_diameter',expected=26,source='specification.json end_plate.hole_diameter')
    d.circle_check('end.hole_radii',circles,expected_radius=13);d.count_check('end.hole_count','CIRCLE[layer=="END_HOLES"]',expected=8)
    label(ms,'D02 / END PLATE PATTERN',(x-30,y+h+110),15)
    label(ms,'8 HOLES, DIAMETER 26',(x,y-100),12)
    label(ms,'BOLT SIZE / GRADE / WELDS: NOT SPECIFIED',(x-70,y-125),9.5)
    return d


def build(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);s=json.loads(SPEC.read_text())
    reports=[];combined=fitz.open()
    for stem,make in [('S01_roof_plan',make_plan),('S02_elevations',make_elevations),('S03_plate_details',make_details)]:
        d=make(s);dxf=out/f'{stem}.dxf';checks=out/f'{stem}.checks.json'
        report=d.save(dxf,checks)
        render_preview(dxf,checks,out/f'{stem}.pdf',out/f'{stem}.png',dpi=96)
        with fitz.open(out/f'{stem}.pdf') as pdf:combined.insert_pdf(pdf)
        (out/f'{stem}.audit.json').write_text(json.dumps(report,indent=2)+'\n')
        reports.append({'sheet':stem,'native_dimensions':report['native_dimensions'],'audit_errors':report['audit_errors'],'audit_fixes':report['audit_fixes'],'passed':report['passed']})
    combined.save(out/'TSBECM-202_Workshop_Drawing_Set.pdf');combined.close()
    # Inspect independently reopened geometry and compare with explicit fixture anchors.
    plan=ezdxf.readfile(out/'S01_roof_plan.dxf');elev=ezdxf.readfile(out/'S02_elevations.dxf');details=ezdxf.readfile(out/'S03_plate_details.dxf')
    base=sorted((round(c.dxf.center.x-350,6),round(c.dxf.center.y-600,6),c.dxf.radius) for c in details.modelspace().query('CIRCLE[layer=="BASE_HOLES"]'))
    end=sorted((round(c.dxf.center.x-1450,6),round(c.dxf.center.y-600,6),c.dxf.radius) for c in details.modelspace().query('CIRCLE[layer=="END_HOLES"]'))
    assert base==[(90,90,15),(90,410,15),(410,90,15),(410,410,15)]
    assert end==[(x,y,13) for x in (70,250) for y in (60,220,380,540)]
    assert s['bay_spacing']*(s['frame_count']-1)==s['length']
    assert s['eaves_height']+s['span']/2*s['roof_slope_percent']/100==8300
    assert all(doc.units==4 for doc in (plan,elev,details))
    summary={'project':s['project'],'source_type':'synthetic specification, not a photograph','sheets':reports,'native_dimensions':sum(r['native_dimensions'] for r in reports),'hole_positions_independently_checked':12,'bay_chain_checked':True,'ridge_height_checked':8300,'native_autocad_test':'not performed','structural_design':'not performed'}
    (out/'verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,default=ROOT/'examples/industrial-workshop')
    build(parser.parse_args().output_dir)
