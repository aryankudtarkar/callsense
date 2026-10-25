# Final prototype audit

Use this with OMP stage `11-FINAL-AUDIT-AND-REPAIR.md`. Invoke `/skill:ponytail-audit` if the installed OMP skill is still available. Inspect its findings independently and complete the evidence table below; an audit suggestion is not proof that a control works.

## Release gates

Mark each row **pass**, **fail**, or **not run**. Include a file, command, test, measurement, or reason. Do not convert “not run” into a pass.

| Gate | Evidence required |
|---|---|
| Scope and data path | Repository matches the recorded-audio local prototype; no cloud audio path, transcription service, identity feature, or unapproved data store. |
| Real inference | Pinned `superb/wav2vec2-base-superb-er` revision and hashes are recorded; actual backend inference was attempted with a permitted test input; model load/inference status and any network access needed to obtain weights are stated. |
| Input safety | Parser accepts only bounded mono PCM16 16 kHz WAV and rejects malformed, oversized, unsupported, truncated, too-short, and silent inputs safely. |
| Privacy behavior | Loopback-only binding; no file/result persistence, sensitive request logging, or outbound audio; UI Clear Session removes browser-side selection, preview, and results. |
| Output semantics | Only angry/happy/neutral/sad appear as dataset labels; score labeling is uncalibrated unless calibrated on a separated set; limitations appear beside results. No truth, deception, intent, urgency, credibility, guilt, or investigative decision claim. |
| Software correctness | Discovered project test/build commands actually run; unit and backend integration outcomes are reported. Browser E2E is listed separately and only reported if performed. |
| Model evaluation | If dataset evaluation ran, actor-disjoint split, source/license, class counts, per-class metrics, macro-F1, confusion matrix, and limitations are documented. If not run, say so. |
| Runtime performance | If benchmarked, report machine, OS, Python/dependency versions, device, model revision, cold load, warm window latency, audio duration, and end-to-end time. Never infer “real-time” from hardware capability alone. |
| Responsible-use review | No ranking or automated action; synthetic fixtures for security tests; permitted public audio only; no claim that results support real investigations. |
| Accessibility and operations | Keyboard and visible-focus behavior, labels, errors, setup/run instructions, stop/clear controls, and known limitations are checked or explicitly not run. |

## Separate the kinds of evidence

- **Software correctness** means specific code paths and tests behave as expected.
- **Model performance** means measured agreement against a permitted, labeled dataset under a documented split. It does not establish field validity.
- **Runtime performance** means measured latency under named hardware, model, and workflow conditions. It is not a real-time claim unless end-to-end timing supports it.
- **Responsible-use and security** means controls and user-facing semantics were checked; this is not legal advice, a formal security certification, or operational approval.

A working local inference path can still have weak or unmeasured model validity. A successful test suite cannot turn acted-corpus performance into cybercrime-call accuracy.

## Audit finding disposition

For each Ponytail or manual finding, record:

1. Finding and severity.
2. Concrete code or test evidence.
3. Whether it was reproduced.
4. Minimal repair and regression check, or why it is deferred.
5. Final state: fixed, accepted limitation, blocked, or not applicable.

Do not auto-apply broad rewrites. Preserve safe failure behavior when model dependencies, weights, browser tooling, or authorized data are unavailable. Do not claim a security test, benchmark, browser journey, or model inference ran unless it actually did.

## Final report template

```text
Ponytail audit: run / unavailable / not run
Repository status and changed files:
Commands run and results:
Unit/integration/browser checks: passed / failed / skipped, with evidence
Real model loaded and invoked: yes / no / blocked (details)
Model dataset metrics: measured / not measured (details)
Latency: measured / not measured (details)
Privacy and security findings:
Accessibility checks:
Unresolved risks and next action:
Prototype claim supported by the evidence:
```
