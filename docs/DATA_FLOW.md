# TSBECM 202 — observed data flow

These notes describe the distributed code. They are **not a privacy policy or terms of service**, and do not establish the publisher's identity or commitments.

| Step | Data and destination |
| --- | --- |
| Get the package or TXT file | Downloaded from GitHub; that service handles the request |
| Attach a drawing in ChatGPT, Codex or Gemini | The selected host receives the attachment and handles it under its own settings and terms |
| Read the drawing and run CAD helpers | Runs in the environment supplied by the host or the user's local Python environment |
| Install missing Python dependencies | If permitted and needed, the package installer contacts its configured package source |
| Save DXF, PDF and notes | Saved using the current host's file workflow or a local output directory |
| Post a support issue | Anything posted is sent to the public GitHub repository |

The repository contains no hosted drawing-processing service, telemetry endpoint, payment integration or separate user database. Its installer copies local files and its CAD helpers create or inspect local files. The chat host may execute additional actions to fulfil a user's request; these notes do not describe or control that host's storage, training, retention or sharing policies.

The publisher, **owen a**, confirmed that there is no separate external storage for user data. The [privacy policy](PRIVACY.md) describes that practice, the host's separate role and public GitHub support. [Terms of use](TERMS.md) describe the free workflow and existing MIT licence. These implementation notes do not assert a fixed retention or deletion policy for another service.
