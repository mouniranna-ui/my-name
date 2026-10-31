#!/usr/bin/env python3
"""Render instructional SVG diagrams. These are diagrams, not app screenshots."""
from pathlib import Path
from html import escape

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/images'
OUT.mkdir(parents=True,exist_ok=True)

def guide(name,title,subtitle,cards,footer):
    w,h=1440,510
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">',
      '<rect width="1440" height="510" rx="28" fill="#101a2c"/>',
      '<g font-family="Arial, Helvetica, sans-serif">',
      f'<text x="60" y="76" fill="#ffffff" font-size="35" font-weight="700">{escape(title)}</text>',
      f'<text x="60" y="118" fill="#bdcce0" font-size="21">{escape(subtitle)}</text>']
    for i,(heading,lines) in enumerate(cards):
      x=60+i*340
      parts += [f'<rect x="{x}" y="170" width="300" height="240" rx="18" fill="#1e2d44" stroke="#354862"/>',
       f'<circle cx="{x+40}" cy="211" r="20" fill="#4ce2ba"/>',
       f'<text x="{x+40}" y="218" text-anchor="middle" fill="#10263b" font-size="21" font-weight="700">{i+1}</text>',
       f'<text x="{x+25}" y="264" fill="#ffffff" font-size="23" font-weight="700">{escape(heading)}</text>']
      for j,line in enumerate(lines):
       parts += [f'<text x="{x+25}" y="{303+j*29}" fill="#d4e0ed" font-size="18">{escape(line)}</text>']
      if i<3: parts += [f'<path d="M{x+309} 290 h22 m-7 -7 l7 7 -7 7" fill="none" stroke="#4ce2ba" stroke-width="3"/>']
    parts += [f'<text x="60" y="465" fill="#a9bfd5" font-size="18">{escape(footer)}</text>','</g></svg>']
    (OUT/name).write_text('\n'.join(parts),encoding='utf-8')

guide('workflow.svg','PHOTO TO AUTOCAD','An image-based drafting workflow with explicit evidence and editable output.',[
 ('Read the drawing',['Inspect every view','Read dimensions upright','Record unclear features']),
 ('Build native CAD',['Draw at full size','Use layers and dimensions','Keep measured values']),
 ('Check the result',['Reopen and audit DXF','Compare source anchors','Inspect PDF visually']),
 ('Deliver the files',['Editable DXF','Scaled PDF preview','Source and uncertainty note'])],
 'An image without a dimension does not provide a confirmed measurement. DWG requires a real CAD converter.')
guide('codex-steps.svg','CODEX · LOCAL SKILL','Download the repository, then run the installer from its extracted folder.',[
 ('Download',['GitHub → Code','Download ZIP','Extract all files']),
 ('Install',['python tools/install_skill.py','--target codex','No global packages changed']),
 ('Open Codex',['Start a new session','Select the skill with $','Attach the drawing image']),
 ('Request CAD',['Use draft-cad-from-images','Ask for DXF + PDF','Review unresolved details'])],
 'Illustrated instructions, not screenshots. See the Codex guide for the exact one-line command and Python setup.')
guide('chatgpt-steps.svg','CHATGPT · CHOOSE YOUR ROUTE','Local plugin for supported desktop setups; portable instructions for other chats.',[
 ('Get the files',['Download the source ZIP','Read the ChatGPT guide','Choose a supported route']),
 ('Load the workflow',['Desktop: local marketplace','Web/mobile: copy prompt','Attach source images']),
 ('Check capabilities',['Can it read your image?','Can it run Python?','Can it return files?']),
 ('Review delivery',['With execution: DXF/PDF','Without it: code + ledger','Run the code locally'])],
 'Uploading a ZIP to a chat is not plugin installation. A GitHub release is separate from the public Plugins Directory.')
guide('gemini-steps.svg','GEMINI · CLI OR GEM','Use the native skill in Gemini CLI, or the instruction adapter in a Gemini Gem.',[
 ('Download',['Get the repository ZIP','Extract the files','Read the Gemini guide']),
 ('Gemini CLI',['python tools/install_skill.py','--target gemini','Reload skills / new session']),
 ('Gemini app',['Explore Gems → New Gem','Paste the Gem instructions','Add knowledge, then Save']),
 ('Give your drawing',['Attach a clear source','Ask for the source ledger','Generate files if supported'])],
 'The Gem adapter does not install a CLI skill or guarantee Python execution. Platform permissions still apply.')
print('Created four instructional diagrams in docs/images')
