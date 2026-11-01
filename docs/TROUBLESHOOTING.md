# Troubleshooting

[Project home](../README.md) · [All guides](README.md)

| Problem | Check | Next step |
| --- | --- | --- |
| `python` is not found | Python installation and command name | Try `python3` on macOS/Linux or `py -3` on Windows; install Python 3.10+ if needed |
| `ezdxf` or `fitz` is missing | The interpreter used by the agent | Activate the intended environment and run `python -m pip install -r requirements.txt` |
| The skill does not appear | Installer output path and active environment | Open a fresh agent session and inspect the installed skills; cloud and local environments are separate |
| Existing installation differs | Local edits in the installed copy | Use `--replace` only when updating; the installer preserves a backup |
| ChatGPT returns only text | Image access, code execution and file output | Ask which tools are available; use the runnable generator in Codex/Python if execution is absent |
| Uploading a ZIP does not install the plugin | Whether the interface supports plugin ingestion | Use direct-chat instructions, a supported local marketplace or the future verified directory listing |
| A dimension is unreadable | Original image and close-ups | Add a clearer crop; keep the value unresolved rather than guessing |
| Two dimensions conflict | Witness-line endpoints and related views | Record both values and ask a focused question; do not silently select one |
| PDF text overlaps | Plot scale, text size and dimension locations | Adjust annotation placement and render the sheet again |
| A CAD audit fails | Audit errors, automatic fixes and generator output | Fix the generator and rerun; do not report a failed check as passed |
| DWG is requested but no converter exists | Installed CAD applications or converters | Deliver labelled DXF and convert with AutoCAD or another genuine converter |

## Use the environment check

```bash
python tools/cad.py doctor
```

This reports available Python packages and known CAD converters. It does not install them or prove that AutoCAD has opened a file.

## Report a reproducible issue

Follow the [support guide](SUPPORT.md). Include your package version, platform, interpreter version, error message and a small non-confidential fixture. Avoid posting private drawings, account information or credentials in public issues.
