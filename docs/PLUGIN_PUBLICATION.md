# ChatGPT plugin: package and publication status

[Project home](../README.md) · [Use in ChatGPT without installation](CHATGPT_START.md)

Updated: **2026-11-01**, package **2.1.2**.

| Route | Current status |
| --- | --- |
| ChatGPT direct instructions and single TXT attachment | Available from this repository; requires the chat's image and code tools for file generation |
| Portable skills-only plugin ZIP | Built for supported ingestion; downloadable below |
| GPT compatibility kit | Prepared instructions, knowledge, icon and six preview cases; no saved GPT exists |
| Account installation through Plugin Creator | Not completed in this workflow; the account creation tool was unavailable |
| Public ChatGPT Plugins Directory | Not submitted or published; no verified listing URL exists |

**[Download the plugin package](https://raw.githubusercontent.com/mouniranna-ui/my-name/photo-to-autocad/downloads/tsbecm-202-plugin-2.1.2.zip)**. This is an implementation package, not a completed public submission. Downloading it does not install it into a ChatGPT account.

For account creation, use the [step-by-step Plugin Creator guide](INSTALL_CHATGPT.md#save-the-plugin-inside-chatgpt) and [prepared creation request](../prompts/create-chatgpt-plugin.txt). For an existing editable GPT, use the separate [GPT compatibility kit](CUSTOM_GPT.md).

## What is implemented

- Name: **TSBECM 202**; category: **Productivity**.
- A `draft-cad-from-images` skill, three technical references, Python helpers and the supplied icon.
- Editable DXF, native dimensions, layers and text; checked PDF previews when the host can execute Python.
- English documentation and listing prompts; the workflow can respond in the user's requested language.
- Release notes and English listing text embedded in `plugin.json`.
- A synthetic example, automated CAD checks and distribution checks. The private drawing supplied during development is not included.

This is a **skills-only** plugin. It has no hosted MCP server, external account login or drawing-upload endpoint. It relies on the host's tools. It does not install Python, dependencies, AutoCAD or a licence on a user's computer. A live installation in ChatGPT and a directory review have not been tested.

## Publisher choices recorded

The creator supplied these choices on **2026-10-31**:

| Setting | Confirmed choice | Package field |
| --- | --- | --- |
| Publisher-selected name | **owen a** | `author.name` and `extensions.com.openai.interface.developerName` |
| Price / commerce | **Free; no payments or purchases** | `extensions.com.openai.review.commerce: false` |
| Country targeting | **All supported countries** | `extensions.com.openai.publication.countries: []` |
| Publisher storage | **No separate external storage of user data** | [Privacy policy](PRIVACY.md) |

The empty country list deliberately applies no publisher country restriction. It does not bypass OpenAI regional availability or account rules. Free refers to this project; access to a host platform or third-party software is governed separately.

The name is publisher-supplied, **not a verified identity claim**. The selected developer identity still needs to be verified in the publication portal, and the saved listing must show the intended identity. The package cannot override a portal-verified publisher name.

## Listing pages and package readiness

All four listing pages are supplied in the package metadata:

| Listing field | Public page |
| --- | --- |
| `websiteURL` | [Project home and publisher](../README.md) |
| `supportURL` | [Support](SUPPORT.md) |
| `privacyPolicyURL` | [Privacy policy](PRIVACY.md) |
| `termsOfServiceURL` | [Terms of use](TERMS.md) |

The privacy policy reflects the creator's confirmation of no separate external storage. It distinguishes private drawings processed in the chosen host from information voluntarily posted to public GitHub support. The terms preserve the existing MIT licence, free use and established drafting limits. They add no subscription, guaranteed response time, jurisdiction or arbitration terms.

The portable source, listing metadata, icon, review prompts, country selection and policy pages are prepared. Local package checks do not replace validation in the publication portal. A skills-only package needs no MCP server connection, MCP review cases, recorded MCP demo or reviewer account credentials.

## Remaining portal steps

The publisher identity has not been verified in this workflow. No draft has been uploaded or submitted, and no directory release has been approved or published. There is no verified public plugin or saved GPT link. Account-plugin creation is also uncompleted because that capability was unavailable.

Select the intended verified developer identity in the official portal, upload the package, inspect the saved metadata and skill inventory, resolve required checks, complete the publisher's legal/policy attestations, then submit for review. Only an approved release can be published to the public directory. Country targeting remains all supported countries; the project remains free.

## Final publication process

Use the prepared package in the official publication portal:

1. Use the current versioned plugin ZIP. Keep the technical plugin name `tsbecm-202` and skill identity unchanged; preserve public upload separation from any later private app bindings.
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
