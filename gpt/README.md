# TSBECM 202 GPT configuration kit

This is a manual configuration kit, not an installed GPT, an import API or a public GPT link. Use it only to update an existing editable GPT or in a managed workspace that currently permits creation.

**Availability checked 2026-10-31:** OpenAI states that personal ChatGPT accounts cannot create or publish new GPTs. Existing GPT editing and managed-workspace availability depend on account permissions and migration status. Use the plugin route for new reusable workflows. Check the current account notice before editing: [official GPT documentation](https://help.openai.com/en/articles/8554397-creating-and-editing-gpts) and [retirement/migration FAQ](https://help.openai.com/en/articles/20001519-custom-gpt-retirement-and-migration-faq).

## What to configure

The release ZIP assembles the following files. In the source repository, the knowledge attachment and icon are reused from their maintained locations rather than duplicated here.

| File in the GPT ZIP | Builder field or purpose |
| --- | --- |
| `configuration.json` | Name, description, conversation starters and capability checklist; copy fields manually |
| `instructions.txt` | Paste its full contents into Instructions |
| `TSBECM-202-ChatGPT.txt` | Upload as a Knowledge file; includes references and exact helper source |
| `icon.png` | Upload as the profile image if the editor permits it |
| `preview-tests.json` | Cases to run in Preview; prepared, not previously executed in a GPT |

## Apply to an eligible GPT

1. Open ChatGPT's GPT area and select the exact existing GPT you own. Choose **Edit GPT**. For new creation, continue only if your workspace actually provides **Create**; this kit cannot enable that permission.
2. Set the name to **TSBECM 202**. Copy the description and four conversation starters from `configuration.json`.
3. Paste `instructions.txt` into Instructions. Upload the knowledge TXT and profile icon.
4. Enable **Code Interpreter & Data Analysis** if available. File output depends on this environment and its installed packages. Web search is useful when authoritative profile data is needed. Image generation is not needed for precise CAD. No external Actions endpoint or API key is supplied or required.
5. Run each case in `preview-tests.json`. Open the resulting files and record actual results. If Knowledge retrieval does not expose the full helper source to Python, attach the knowledge TXT directly to the test conversation; never invent missing code.
6. Update the exact existing GPT or save in the eligible workspace. Review only the sharing options actually offered by that account. Keep the resulting GPT URL only after ChatGPT shows a saved, usable GPT. The ZIP itself creates no share link.

The instructions preserve editable geometry, source uncertainties and honest DXF/DWG reporting. They do not install AutoCAD, select structural members or certify a design.

Build the complete kit from the repository root with `python tools/build_release.py`. The GPT ZIP is emitted alongside the plugin, skill and source ZIPs.
