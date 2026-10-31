# Use TSBECM 202 in Gemini

[Project home](../README.md) · [All guides](README.md)

![Gemini routes](images/gemini-steps.svg)

## Gemini CLI

Download and extract the complete project. From its root, run:

```bash
python tools/install_skill.py --target gemini
```

The default destination is `~/.gemini/skills/draft-cad-from-images`. Open a new session or use:

```text
/skills reload
/skills list
```

You can instead use Gemini CLI's native installer:

```bash
gemini skills install ./plugins/tsbecm-202/skills/draft-cad-from-images --scope user
```

Choose one installation method and review any permission prompt shown by the platform. Prepare Python and the dependencies using the [Codex/Python guide](INSTALL_CODEX.md#3-prepare-python). Provide the drawing as an attachment or an accessible file path:

```text
Use draft-cad-from-images to reconstruct this technical drawing.
Create editable DXF and a scaled PDF. Record the source dimensions,
check their actual feature anchors, and identify unresolved information.
```

If several copies appear in different skill directories, inspect `/skills list` to identify the one being used. The project's installer does not install Gemini CLI or configure your Google account; follow the [official setup guide](https://geminicli.com/docs/get-started/) if needed.

## Gemini app and Gems

1. Open **Explore Gems → New Gem** in a supported Gemini interface.
2. Name the Gem **TSBECM 202**.
3. Paste [gemini-gem-instructions.txt](../prompts/gemini-gem-instructions.txt) into its instructions.
4. Optionally add [portable-knowledge.txt](../prompts/portable-knowledge.txt) as knowledge.
5. Preview the workflow with a drawing, then use **Save** to keep the Gem.

A Gem supplies instructions and knowledge; it is not a native CLI skill installation and does not itself install CAD libraries. If the app cannot execute Python and return files, request the source ledger and complete runnable generator. Written code is not the same as a created, checked DXF.

## Check the result

Use the same [delivery review](WORKFLOW.md#review-and-delivery) as in other environments. Do not assume that a platform name or a successful instruction upload guarantees equivalent execution capabilities.

Official references: [Agent skills](https://geminicli.com/docs/cli/skills/), [CLI reference](https://geminicli.com/docs/cli/cli-reference/), [Creating Gems](https://support.google.com/gemini/answer/15235603?hl=en).
