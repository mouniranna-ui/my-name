# TSBECM 202 in ChatGPT

[Project home](../README.md) · [Direct-chat quick start](CHATGPT_START.md) · [All guides](README.md)

![ChatGPT routes](images/chatgpt-steps.svg)

## Choose a route

| Route | What it provides | Status |
| --- | --- | --- |
| Direct chat | Instructions and optional helper source attached to the conversation | Available now; host execution tools are required for files |
| Account plugin through Plugin Creator | A saved reusable plugin selected with `@` | Package ready; account save and live test remain pending |
| Local desktop marketplace | A reusable plugin in a supported local ChatGPT/Codex setup | Package supplied; availability depends on the local client |
| Public Plugins Directory | A discoverable account-installed plugin | Not submitted or published |
| Existing editable GPT | Instructions, knowledge, icon and preview cases | Configuration kit supplied; [check current eligibility](CUSTOM_GPT.md) |

## Save the plugin inside ChatGPT

1. Download the [TSBECM 202 plugin ZIP](https://raw.githubusercontent.com/mouniranna-ui/my-name/photo-to-autocad/downloads/tsbecm-202-plugin-2.1.0.zip). Keep the ZIP intact; it contains root `plugin.json` and the drafting skill.
2. In ChatGPT, start a conversation and select **Plugin Creator** from the `@` menu. Use the account/workspace where the plugin should live.
3. Attach the plugin ZIP and paste [the prepared creation request](../prompts/create-chatgpt-plugin.txt). It asks Plugin Creator to reuse the package, check for an existing owned plugin, save the intended plugin and return its real link.
4. Confirm that the saved product is named **TSBECM 202** and includes **draft-cad-from-images**. A generated ZIP, a local marketplace entry or a response saying "ready" is not proof of account installation. If the save capability is unavailable, preserve the ZIP and keep installation pending.
5. Start a fresh conversation, select the saved plugin with `@`, attach a source drawing and request DXF, PDF and verification. For an initial synthetic test, use the dimensioned-plate case in [preview-tests.json](../gpt/preview-tests.json).
6. Open the returned files. Check native geometry, dimensions, layers, units and the PDF before using the workflow on your project.

The current package has **not yet been saved or live-tested as an account plugin in this workflow**. There is no verified account-plugin URL to link here. Plugin creation availability depends on the account/workspace and enabled capabilities.

Private creation, sharing a saved plugin with a workspace, and publishing it to the public directory are separate stages. A public listing needs publisher information and applicable review. See [publication status](PLUGIN_PUBLICATION.md) before inviting people to search the directory.

## Direct chat: no local installation

Follow the [illustrated quick start](CHATGPT_START.md). Attach your drawing with [TSBECM-202-ChatGPT.txt](../prompts/TSBECM-202-ChatGPT.txt), then ask for editable DXF, a PDF and a record of unresolved dimensions.

An attached TXT or ZIP is not plugin installation. Instructions alone do not add image access, Python execution or file output capabilities.

## Supported local desktop setup

The project contains a local marketplace and a portable plugin:

- `.agents/plugins/marketplace.json`
- `plugins/tsbecm-202/plugin.json`
- `plugins/tsbecm-202/skills/draft-cad-from-images/`

Open the extracted repository in a supported local ChatGPT/Codex desktop environment. Use **Plugins** to find the local **TSBECM 202** marketplace and install the plugin. If your version does not expose local marketplaces, use direct chat or the [Codex CLI route](INSTALL_CODEX.md). Local installation in one environment does not install the plugin in every web or mobile account.

After installation, start a fresh conversation and select the plugin or its skill using `@` where supported. The technical skill name remains `draft-cad-from-images`.

## Future public directory listing

The plugin is a skills-only package: no hosted MCP server or separate project login is provided. It still relies on the host's file and Python tools. The official submission process requires the appropriate publisher identity, metadata and applicable checks.

When a genuine listing is published, this guide will link to it. Only then should users search for and install **TSBECM 202** from the public directory. [Current publication status and remaining work](PLUGIN_PUBLICATION.md).

## Expected deliverables

Ask for the actual DXF, a scaled PDF preview and a verification note. Compare the drawing with the source, especially the feature anchors of each dimension. The plugin does not install Autodesk AutoCAD or provide a licence. Native AutoCAD application testing must be reported separately from a DXF audit.

Official references: [Plugins](https://learn.chatgpt.com/docs/plugins), [Package format](https://developers.openai.com/plugins/build/plugins), [Submission](https://developers.openai.com/plugins/deploy/submission).
