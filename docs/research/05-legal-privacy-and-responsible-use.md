# Legal, privacy, and responsible-use review

**Scope:** technical risk analysis for an academic prototype, researched 24 October 2026. This is not legal advice. A real police, agency, vendor, or institution must obtain jurisdiction-specific legal and privacy review before recording, processing, sharing, retaining, or using any call data.

## India status at research date

India's Digital Personal Data Protection Act, 2023 was enacted, but the Government's 13 November 2025 commencement notification phases provisions. Sections 3–17—including the general processing rules and the section 17 offence-investigation exemption—are scheduled to commence eighteen months after publication, not by this research date. The Digital Personal Data Protection Rules, 2025 also phase commencement: Rules 1, 2, and 17–21 took effect on Gazette publication; Rule 4 after one year; Rules 3, 5–16, 22, and 23 after eighteen months. A December 2025 corrigendum changes the wording to “in the Official Gazette.” Verify the exact effective-date calculation and any later notifications before deployment. [R18, R19, R20]

The DPDP Act text describes processing grounds and includes a section 17(1)(c) exemption for certain processing in prevention, detection, investigation, or prosecution of offences. That provision is not a blanket authorization for recording, collecting, analyzing, exporting, or retaining a person's voice. At this snapshot, the section is not yet in force under the staged notification. Other applicable Indian law, lawful-recording authority, state/agency policy, employment rules, evidence procedures, and data access restrictions require separate advice. The Bharatiya Sakshya Adhiniyam section 63 sets requirements concerning electronic-record admissibility; an SER output does not become scientifically valid or admissible merely because it is exported. [R18, R19, R22]

The EU AI Act is not the prototype's governing law in India, but it is relevant comparative context: Article 5(1)(f) prohibits emotion inference in workplace and educational settings with medical/safety exceptions. Article 50 includes transparency duties for certain emotion-recognition systems that are not prohibited. Law-enforcement use is legally distinct and needs a separate applicability analysis; do not infer blanket permission or prohibition from this excerpt. [R21]

## Privacy requirements for the prototype

- Use synthetic audio for unit/security tests. For human speech demos, use only a dataset/sample whose terms are understood and followed. Never place real victim, suspect, informant, police, family, or other private calls in Git, bug reports, screenshots, logs, or a classroom presentation.
- Display the exact purpose and limitations before analysis. User must affirm lawful permission to use the selected file; the checkbox is a product guard, not proof of lawful authority or consent.
- Local inference only: no transcript API, cloud audio model, external analytics, or telemetry. The first model download retrieves public model weights, not the uploaded audio.
- Do not save audio or derived results to disk or a database. Stream a bounded request into memory; discard server buffers after inference. Clear browser file selection, object URL, audio preview, and results when user removes the session. This is application behavior, not forensic secure erasure from RAM, swap, or crash dumps.
- Bind only to `127.0.0.1`, no LAN exposure, no multi-user sharing, no account/case management, no default export. Production identity, access control, audit, retention and evidence policies are out of scope.
- Show the model source, revision, labels, uncalibrated score warning, and data-handling notice. Do not label a raw model score “probability” or a high score “high urgency.”
- Do not assess honesty, deception, intent, credibility, guilt, or suspiciousness. No automated arrest, interrogation, emergency response, or prioritization decisions. No person ranking or voice identity tracking.

## What this model may and may not say

The original research plan assessed the four-class SUPERB checkpoint, but the current app runtime has been changed to `iic/emotion2vec_plus_large`. Its listed output categories are angry, disgusted, fearful, happy, neutral, other, and sad, with surprised also exposed by the model card; these remain model labels, not verified psychological states. Scores are uncalibrated and do not establish distress, nervousness, deception, or mixed state. Use display text such as “Model-estimated vocal-expression label: sad (uncalibrated score). Listen to the segment; this output is not evidence about the person's state or truthfulness.” [R3, R4, R7]

The emotion2vec model is distributed under the FunASR Model Open Source License Agreement v1.1, a custom terms document rather than Apache/MIT. Preserve model name and source/author attribution and recheck license terms for the intended context. [R7, R27]

## Bias, fairness, and human oversight

The training and evaluation corpora are small or corpus-specific compared with real conversational variation. Research documents cross-dataset degradation, differing label practices, cultural/language differences, and speaker effects. Do not claim accuracy across age, accent, language, sex, disability, or culture. Do not use model score as a proxy for urgency or credibility. Show all windows chronologically rather than ranking people/calls; let a human play the underlying recording and disregard the estimate. [R1, R8, R10, R12, R17]

## Legal/open questions before any external use

A lawyer/privacy officer must confirm lawful basis and purpose; whether notices or consent are required; authority to record/process each call source; rules for law-enforcement access and disclosure; whether audio is personal/biometric information under the relevant context; retention and evidence obligations; procurement/model/data license compatibility; cross-border implications of model download or any later service; and current DPDP commencement and subordinate rules. No prototype screen or consent checkbox resolves these questions.
