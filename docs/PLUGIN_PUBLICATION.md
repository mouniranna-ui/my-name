# ChatGPT plugin: package and publication status

[Project home](../README.md) · [Use in ChatGPT without installation](CHATGPT_START.md)

Updated: **2026-10-31**, package **2.0.0**.

| Route | Current status |
| --- | --- |
| ChatGPT direct instructions and single TXT attachment | Available from this repository; requires the chat's image and code tools for file generation |
| Portable skills-only plugin ZIP | Built for supported ingestion; downloadable below |
| Account installation through Plugin Creator | Not completed in this workflow; the account creation tool was unavailable |
| Public ChatGPT Plugins Directory | Not submitted or published; no verified listing URL exists |

**[Download the plugin package](https://raw.githubusercontent.com/mouniranna-ui/my-name/photo-to-autocad/downloads/tsbecm-202-plugin-2.0.0.zip)**. This is an implementation package, not a completed public submission. Downloading it does not install it into a ChatGPT account.

## What is implemented

- Name: **TSBECM 202**; category: **Productivity**.
- A `draft-cad-from-images` skill, three technical references, Python helpers and the supplied icon.
- Editable DXF, native dimensions, layers and text; checked PDF previews when the host can execute Python.
- English documentation and listing prompts; the workflow can respond in the user's requested language.
- Release notes and English listing text embedded in `plugin.json`.
- A synthetic example, automated CAD checks and distribution checks. The private drawing supplied during development is not included.

This is a **skills-only** plugin. It has no hosted MCP server, external account login or drawing-upload endpoint. It relies on the host's tools. It does not install Python, dependencies, AutoCAD or a licence on a user's computer. A live installation in ChatGPT and a directory review have not been tested.

## Publisher details still needed

The package intentionally omits unknown values. The publisher needs to provide the intended verified individual or business identity, intended countries (or explicitly all supported countries), and whether any payment or purchase is involved.

The public project page and [support instructions](SUPPORT.md) are available. A publisher-approved privacy policy and applicable terms still need to be prepared and hosted from confirmed practices. [Observed data flow](DATA_FLOW.md) provides technical facts for that discussion; it is not a published privacy policy. No identity, legal statement, country targeting or commerce declaration has been invented.

Plugin Creator's preparation workflow asks for all four listing pages. The current public submission documentation distinguishes MCP listing requirements from skills-only metadata validation. Follow the actual portal findings for this skills-only package; a permissive metadata schema does not complete publisher verification or policy decisions.

## Final publication process

After publisher details and required pages are complete:

1. Set the confirmed metadata in a separate public upload copy and rebuild the plugin ZIP. Keep the plugin name and skill identity unchanged.
2. Inspect the ZIP: root `plugin.json`, contained skill assets, no secrets, no root `.app.json` or private app bindings.
3. In the official developer portal, select the intended organization/project and verified publisher. Upload the ZIP as a draft and inspect the imported metadata and skill findings.
4. Resolve required checks. The authorized publisher completes identity verification and legal/policy attestations. A skills-only plugin does not need MCP test cases, reviewer login credentials or a demo recording.
5. Submit for review. If approved, publish the approved version for the confirmed countries.
6. Add the actual verified listing URL to this page, the README and the ChatGPT guide. Only then describe the plugin as publicly installable.

Uploading a draft, submitting it for review and publishing an approved release are separate states. No public approval or review deadline is guaranteed.

## Local preparation commands

```bash
python tools/build_chatgpt_kit.py
python tools/verify_repository.py
python -m unittest discover -s tests -v
python tools/build_release.py
```

These commands generate the current distribution. They do not upload or submit anything. Maintainers should retain versioned release files and update download links when publishing a new version.

Official references: [Package format](https://developers.openai.com/plugins/build/plugins), [Submission and metadata](https://developers.openai.com/plugins/deploy/submission), [Plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines), [Using plugins](https://learn.chatgpt.com/docs/plugins).
