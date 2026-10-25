# Environment and tool audit

**Audit date:** 24 October 2026. Commands were run read-only in the current project directory; credentials, environment values, and tokens were not printed.

## Repository and application runtime

- Current directory: `/Users/mrinmoykundu/Documents/Codex/2026-10-24/files-mentioned-by-the-user-screenshot`.
- Directory contained only `outputs/` and `work/`; `rg --files --hidden -g '!node_modules' -g '!.git' .` returned no project files. `git rev-parse --show-toplevel` returned no repository. There is no existing code, framework, package manifest, or test suite to preserve.
- Host: MacBook Air Mac17,3, Apple M5, 10 CPU cores, 16 GB RAM; macOS 27.0.1; Apple Silicon arm64.
- `node`, `npm`, `yarn`, `bun`, `ffmpeg`, and `ffprobe` are not on PATH. `pnpm` 11.25.0 exists as a Codex fallback runtime, but Node is absent, so it is not a reason to choose a Node frontend.
- Python: `/Library/Frameworks/Python.framework/Versions/3.16/bin/python3`, version 3.16.0a1; `pip3` 26.2.1. No stable `python3.14` command on PATH. Homebrew 7.0.9 is installed; Homebrew's `python@3.14` formula supports Apple Silicon and provides `python3.14`. PyTorch's current macOS guidance recommends Python 3.10–3.14, so the alpha runtime is not the project environment. [R13, R25]
- No app dependencies are installed: torch, torchaudio, Transformers, SpeechBrain, NumPy, SciPy, FastAPI, Uvicorn, soundfile, librosa, WebRTC VAD, soxr, and pytest were absent. No model weights were downloaded. No audio inference or latency test was run.

## OMP audit

- `omp` resolves to `/Users/mrinmoykundu/.local/bin/omp`; local version output: `omp/18.12.6`.
- `omp --help` confirms `omp --model=<value>`, `@file` arguments, `--continue`, interactive mode, and skill discovery. The exact prompt-file form is `omp --model google-antigravity/gemini-3.8-flash @prompts/omp/<file>.md`.
- `omp models google-antigravity` lists `gemini-3.8-flash` with 1M context and supported thinking levels. `omp models find gemini-3.8-flash` also lists an OpenRouter model, but the local execution sequence selects the locally visible `google-antigravity` provider. This catalog result does not prove provider login, account entitlement, or a completed model request; authentication was not inspected.
- OMP's documented prompt context supports `@` file loading and project `.omp/AGENTS.md`. No project-specific context exists in this empty directory. [R23]

## Ponytail audit

- No standalone `ponytail` executable is on PATH. OMP's `plugin list` does show user plugin `ponytail@ponytail (5.3.2)`. OMP's `skill list` resolves `ponytail`, `ponytail-review`, and `ponytail-audit`; `omp config get skills.enableSkillCommands` is `true`.
- Use OMP's verified skill syntax: `/skill:ponytail-review` and `/skill:ponytail-audit`. The upstream README advertises direct `/ponytail-review` commands for several hosts, but the current OMP integration is installed as skills; do not assume a bare slash command exists here. [R26]

## Build environment decision

Use Homebrew's supported stable Python 3.14 in a project-local virtual environment. Keep the app Python-only (FastAPI + static page), with CPU as the dependable baseline and optional MPS after a real model check. The M5/16 GB capacity is an engineering indication that a 378 MB model is worth trying locally; it is not evidence of a particular inference speed. The project prompts must ask the future OMP agent to verify installed package compatibility and report any missing dependency rather than assume it. [R3, R13, R25]

## OMP/Ponytail workflow facts

Use one numbered prompt file per OMP session to keep execution reviewable. OMP's model selector uses `provider/model-id`; installed catalog prefix is `google-antigravity`. Skills can be invoked as `/skill:<name>` because skill commands are enabled. If that command or model request fails in a later app run, inspect `omp --help`, `omp models`, and `/skill:` autocomplete; do not edit global auth/provider settings as a workaround. [R23]
