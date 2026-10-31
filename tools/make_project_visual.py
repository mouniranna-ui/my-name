#!/usr/bin/env python3
"""Create an SVG overview from the workshop's published synthetic geometry."""
from pathlib import Path
from html import escape
import json

ROOT=Path(__file__).resolve().parents[1]
s=json.loads((ROOT/'examples/industrial-workshop/specification.json').read_text())
L,W,E=s['length'],s['span'],s['eaves_height'];H=E+W/2*s['roof_slope_percent']/100

def p(x,y,z):return (985+500*x/L+280*y/W,580-220*x/L+150*y/W-250*z/H)
def points(ps):return ' '.join(f'{x:.2f},{y:.2f}' for x,y in ps)
def text(x,y,value,size=24,fill='#c6d5e4',weight=400,extra=''):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'
def path3(ps,color='#9dd8e7',width=2,opacity=1):
 return f'<polyline points="{points([p(*q) for q in ps])}" fill="none" stroke="{color}" stroke-width="{width}" opacity="{opacity}" stroke-linejoin="round"/>'
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1840" height="900" viewBox="0 0 1840 900" role="img" aria-label="TSBECM 202: synthetic industrial workshop drafting example">',
 '<defs><radialGradient id="light" cx="75%" cy="40%" r="70%"><stop offset="0" stop-color="#15384b"/><stop offset="1" stop-color="#0a1624"/></radialGradient><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#37586b" stroke-width="0.6" opacity="0.22"/></pattern></defs>',
 '<rect width="1840" height="900" rx="28" fill="url(#light)"/>','<rect x="700" y="0" width="1140" height="900" fill="url(#grid)"/>',
 '<g font-family="Arial, Helvetica, sans-serif">',
 text(72,85,'OPEN DRAFTING TOOLKIT',20,'#5ce0ba',700,'letter-spacing="3"'),text(72,175,'TSBECM 202',76,'#ffffff',700),
 text(72,242,'Technical drawings.',40,'#ffffff',500),text(72,294,'Editable CAD.',40,'#ffffff',500),
 text(72,363,'A documented workflow for reading,',24),text(72,399,'reconstructing and checking engineering',24),text(72,435,'drawings with AI-assisted CAD tools.',24),
 '<rect x="72" y="488" width="556" height="2" fill="#294556"/>',
 text(72,540,'24 x 36 m',45,'#ffffff',700),text(72,576,'INDUSTRIAL WORKSHOP STUDY',19,'#7fb4c7',500,'letter-spacing="1"'),
 text(72,641,'3 coordinated sheets',24,'#e4edf4'),text(72,682,'34 native dimensions',24,'#e4edf4'),text(72,723,'Editable DXF + vector PDF',24,'#e4edf4'),
 text(985,85,'REPRODUCIBLE EXAMPLE PROJECT',19,'#5ce0ba',700,'letter-spacing="2"')]
svg.append(f'<polygon points="{points([p(0,0,0),p(L,0,0),p(L,W,0),p(0,W,0)])}" fill="#123345" stroke="#3d6b7c"/>')
for i in range(7):
 x=i*s['bay_spacing']
 svg.append(path3([(x,0,0),(x,0,E),(x,W/2,H),(x,W,E),(x,W,0)],'#d9f4f5' if i==0 else '#79c3d3',3.8 if i==0 else 2.8))
 for y in (0,W):
  u,v=p(x,y,0);svg.append(f'<ellipse cx="{u}" cy="{v}" rx="9" ry="4" fill="#5ce0ba" opacity="0.7"/>')
for y in range(0,W+1,s['purlin_plan_spacing']):
 z=E+min(y,W-y)*s['roof_slope_percent']/100
 svg.append(path3([(0,y,z),(L,y,z)],'#5ce0ba',1.7,0.85))
for y in (0,W):
 for z in (1500,3000,4500):svg.append(path3([(0,y,z),(L,y,z)],'#4e8395',1.2,0.8))
 for x in (0,L-s['bay_spacing']):
  svg.append(path3([(x,y,0),(x+s['bay_spacing'],y,E)],'#f1c582',1.7))
  svg.append(path3([(x+s['bay_spacing'],y,0),(x,y,E)],'#f1c582',1.7))
for i in range(7):
 u,v=p(i*s['bay_spacing'],W+1100,0)
 svg.append(f'<circle cx="{u}" cy="{v}" r="13" fill="#0a1624" stroke="#5e92a6"/>')
 svg.append(text(u,v+5,i+1,14,'#d0e8f1',400,'text-anchor="middle"'))
svg+=['<rect x="72" y="802" width="1696" height="1" fill="#2b485a"/>',
 text(72,850,'CODEX  /  CHATGPT  /  GEMINI',19,'#e9f3f7',700,'letter-spacing="1.5"'),
 text(1768,850,'Synthetic geometry. Educational drafting example; not a structural design.',18,'#a1bdcc',400,'text-anchor="end"'),'</g></svg>']
out=ROOT/'docs/images/project-showcase.svg';out.write_text('\n'.join(svg)+'\n');print(out)
