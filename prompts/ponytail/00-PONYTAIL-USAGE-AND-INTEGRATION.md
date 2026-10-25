# Ponytail usage and OMP integration

## Verified local integration

The environment audit on 24 October 2026 found OMP 18.12.6, a user plugin `ponytail@ponytail` version 5.3.2, and the skills `ponytail`, `ponytail-review`, and `ponytail-audit`. OMP skill commands are enabled. The verified invocation forms are `/skill:ponytail-review` and `/skill:ponytail-audit`; do not assume the upstream direct `/ponytail-review` command is registered in OMP. See [`docs/research/10-environment-and-tooling-audit.md`](../../docs/research/10-environment-and-tooling-audit.md) and the official project documentation linked as R26 in [`docs/research/12-references.md`](../../docs/research/12-references.md).

Ponytail is coding guidance and a code-review aid. It does not classify audio, validate emotion labels, establish legal authority, prove model performance, or become part of the running application. The selected SER backend remains the local, documented `superb/wav2vec2-base-superb-er` model.

## Discover before invoking

At the start of a future implementation session, use OMP's local discovery commands if availability is uncertain:

```text
omp --version
omp plugin list
omp skill list
omp config get skills.enableSkillCommands
```

These are read-only checks. Do not inspect credentials, edit global provider configuration, install software, or infer provider entitlement from a model catalog listing. If the skill list or command behavior has changed, follow the current OMP help and Ponytail's official documentation; update this guide only after verifying the actual integration.

## Recommended placement in the build sequence

Use the OMP files in numerical order, one stage per session. Ponytail supplements the tasks at focused checkpoints:

1. After stage 02, ask `/skill:ponytail-review` to review the scaffold diff for unnecessary structure, duplicated dependencies, and missing commands. Keep the required Python model path and security controls.
2. After stages 03–04, use `/skill:ponytail-review` on WAV parsing, request handling, preprocessing, model loading, and label mapping. Verify findings against the research contract and tests.
3. After stage 07, use `/skill:ponytail-review` for the privacy and security changes.
4. After stage 11, use `/skill:ponytail-audit` for the repository-wide final pass. Then check each reported finding against source and test evidence.

Do not send confidential or personal audio to a coding agent. The review can inspect code and synthetic fixtures; it does not need a real call recording.

## How to handle suggestions

Treat every recommendation as a candidate finding. For each one:

- Identify the file, behavior, and evidence that supports it.
- Check whether the recommendation conflicts with `docs/research/07-product-requirements.md`, `08-system-architecture.md`, `09-evaluation-and-test-plan.md`, or the security rules in the relevant OMP stage.
- Preserve actual model inference, input validation, safe failure behavior, privacy, accessibility, and meaningful tests.
- Make only the smallest verified change. Add or update a focused regression test for security-sensitive behavior.
- Record disagreement or deferred work with a reason and next action. Do not silently omit it.

A simplification is not acceptable if it removes a required test, safety notice, permission check, parser bound, real classifier call, or accessible control. Do not apply a broad rewrite solely to satisfy a stylistic suggestion.

## Manual fallback

If the skill cannot be invoked, continue with the manual checklist in `02-SECURITY-AND-CORRECTNESS-REVIEW.md` and the release gates in `03-FINAL-PROTOTYPE-AUDIT.md`. Report Ponytail review as unavailable or not run. Never report a manual review as a Ponytail audit.
