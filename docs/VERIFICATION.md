# Verification and evidence

[Project home](../README.md) · [Drawing workflow](WORKFLOW.md)

The project separates numerical checks, file integrity, visual review, source interpretation and native application testing.

## Industrial workshop

The [specification](../examples/industrial-workshop/specification.json) is a synthetic drafting brief. Each drawing has a saved check manifest and an audit report. The [combined verification record](../examples/industrial-workshop/verification.json) records sheet results and independent feature checks.

Checks cover native dimensions, hole counts and radii, plate hole centres, roof slopes, bay totals, the derived ridge height, millimetre units and plot settings. PDF pages are rendered from the DXF and visually inspected. The example does not establish photo-reading accuracy or structural adequacy.

## Plate reconstruction fixture

The independent [plate example](../examples/plate/README.md) uses a 160 × 280 mm source image with eight diameter-14 holes and a 16 × 54 mm slot. Fifteen native dimensions were checked. Thickness, material and manufacturing tolerances remain unspecified. The vector PDF uses A3 portrait at 1:1.

## Automated checks

| Check group | Coverage |
| --- | --- |
| CAD helper tests | Saved dimensions, invalid overrides, missing checks, hole geometry, slopes, slots, fillets, units, plot scale and PDF |
| Distribution tests | Installer idempotency, backup behavior, symlink refusal, archive entry points and exact ChatGPT attachment extraction |
| Repository verifier | Local documentation links, plugin metadata, icons, YAML, SVGs, workflow files and attachment freshness |
| Showcase build | Reopened dimensions, hole positions, bay totals and ridge height against explicit fixture values |

```bash
python -m pip install -r requirements-dev.txt
python tools/build_chatgpt_kit.py
python tools/verify_repository.py
python -m unittest discover -s tests -v
python plugins/tsbecm-202/skills/draft-cad-from-images/scripts/test_cad_tools.py
python tools/build_showcase.py --output-dir workshop-output
```

## Limits of the evidence

- No native Autodesk AutoCAD application test was performed in this development environment.
- Live logged-in Codex, Gemini and public ChatGPT plugin installations were not tested across every account or platform.
- Configured CI workflows are not proof that a hosted workflow run completed.
- No load analysis, member sizing, connection design or fabrication approval was performed.

A passing DXF audit does not certify missing source information. Review the actual measurements, their anchors and the final sheets.
