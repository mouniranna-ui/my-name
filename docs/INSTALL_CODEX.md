# Install TSBECM 202 in Codex

[Project home](../README.md) · [All guides](README.md) · [Drawing workflow](WORKFLOW.md)

![Codex installation](images/codex-steps.svg)

## 1. Get the complete project

Download the [source ZIP](https://raw.githubusercontent.com/mouniranna-ui/my-name/photo-to-autocad/downloads/tsbecm-202-source-2.0.0.zip), extract it and open a terminal in the directory containing `README.md`, `tools` and `plugins`. Alternatively, clone the project branch using the command in the main README.

Python 3.10 or newer is required. Check with `python --version`; use `python3` on systems without `python`, or `py -3` on Windows.

## 2. Install the skill

```bash
python tools/install_skill.py --target codex
```

The default destination is `~/.agents/skills/draft-cad-from-images`. The installer copies local files; it does not download dependencies or alter global Python packages. The visible skill name is **TSBECM 202**.

To install only for the current project:

```bash
python tools/install_skill.py --target codex --scope project
```

For Codex Cloud, the installed skill files, image and Python environment must exist in the cloud task's repository/environment. A local installation on your computer is a separate environment.

## 3. Prepare Python

```bash
python -m venv .venv
```

Activate the environment as described in the [main README](../README.md), then run:

```bash
python -m pip install -r requirements.txt
python tools/cad.py doctor
```

Tell Codex to use this environment. This project does not require an additional project-specific API key; your platform account and subscription are separate.

## 4. Start a drafting task

Open a new agent session and attach a drawing or provide a path the task can access:

```text
Use $draft-cad-from-images on the attached drawing.
Create editable DXF with native dimensions, a scaled PDF preview and a
source ledger. Preserve all readable annotations. Check the saved geometry
and identify missing or conflicting source information.
```

The bundled helper example is a tool check, not a converter for arbitrary images:

```bash
python tools/cad.py example --output-dir demo-output
```

To regenerate the larger demonstration:

```bash
python tools/build_showcase.py --output-dir workshop-output
```

## 5. Inspect the delivery

Open the DXF in a CAD application. Review units, layer names, native geometry and dimensions. Compare the PDF with the source, including hole positions and dimension endpoints. Keep unresolved data visible. [Detailed review criteria](WORKFLOW.md#review-and-delivery).

## Optional plugin marketplace

From the repository root, in a Codex version supporting plugins:

```bash
codex plugin marketplace add .
```

Open `/plugins`, choose **TSBECM 202**, install it and start a new session. The IDE skill route is separate from plugin support. Avoid installing duplicate copies unless you deliberately need them.

## Update safely

```bash
python tools/install_skill.py --target codex --replace
```

If the existing copy differs, the installer requires `--replace` and keeps a backup outside the active skill directory. It prints the backup location. For removal, remove only the installed `draft-cad-from-images` directory after saving your own edits.

The 2.0.0 rebrand keeps the skill invocation name stable. Older plugin packages used the name Photo to AutoCAD; the current plugin package is `tsbecm-202`.

Official references: [Build skills](https://learn.chatgpt.com/docs/build-skills), [Plugin packages](https://developers.openai.com/plugins/build/plugins).
