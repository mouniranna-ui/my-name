# TSBECM 202: existing GPT setup and current availability

[Project home](../README.md) · [ChatGPT plugin setup](INSTALL_CHATGPT.md) · [Direct chat](CHATGPT_START.md)

Checked **2026-10-31**. This repository provides a **GPT configuration kit**, not a created or published GPT. There is no verified TSBECM 202 GPT URL.

## Check eligibility first

OpenAI's current documentation says new GPT creation and publishing are unavailable on personal accounts, including Free, Go, Plus and Pro. Existing GPTs can remain editable depending on plan, permissions and migration status. In managed workspaces, follow the workspace's actual availability notice; affected Enterprise workspaces reached the new-creation cutoff on October 26, 2026, with the documented FedRAMP exception.

Do not buy a different personal plan on the assumption that it restores GPT creation. Use [the plugin route](INSTALL_CHATGPT.md) for this new reusable workflow. The compatibility kit remains useful for an existing editable GPT or an eligible managed workspace. Review the official [creation/editing documentation](https://help.openai.com/en/articles/8554397-creating-and-editing-gpts), [sharing documentation](https://help.openai.com/en/articles/8798878-sharing-and-publishing-gpts) and [migration FAQ](https://help.openai.com/en/articles/20001519-custom-gpt-retirement-and-migration-faq).

## Prepared configuration

Download the [GPT configuration ZIP](https://raw.githubusercontent.com/mouniranna-ui/my-name/photo-to-autocad/downloads/tsbecm-202-gpt-2.1.1.zip). Extract it before using the builder. Its JSON is a field checklist, not an OpenAI import format.

| Setting | Prepared value |
| --- | --- |
| Name | TSBECM 202 |
| Description and starters | `configuration.json` |
| Instructions | `instructions.txt` |
| Knowledge | `TSBECM-202-ChatGPT.txt`, containing workflow, references and CAD helper source |
| Profile image | `icon.png` |
| File generation | Enable Code Interpreter & Data Analysis when available |
| External Actions / API keys | None required; no hosted conversion API exists |
| Preview | Six prepared acceptance cases in `preview-tests.json` |

Follow the [complete configuration walkthrough](../gpt/README.md). The included instructions are English and tell the assistant to respond in the user's language. Actual drawings must be reconstructed from the current user's source; public synthetic fixtures are examples only.

## Validate before sharing

Run the preview cases in the actual saved GPT, with its actual tools. Verify editable entities, native dimension measurements, uncertainty handling and the returned files. A local Python check does not establish that GPT Knowledge or its execution tools work. Record the saved GPT version and results before sharing any URL.

If the account offers an existing GPT that you own, update that exact GPT only. If the editor is unavailable or the GPT is already migrated and read-only, use the plugin or direct-chat route. This repository does not bypass account restrictions or migrate other GPTs automatically.
