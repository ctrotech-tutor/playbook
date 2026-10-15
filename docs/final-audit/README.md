# Final-readiness content audit

**The HTML Playbook | Odejobi Abiola Samuel | CTROTECH**  
Updated: **15 October 2026**

## Current position

**53 of 74 chapters have received a substantive first pass; 21 remain.** No chapter has independent approval. All 81 original requirements, all captured coverage routes and all four final-publication gates remain open. There are 25 recorded findings. No scope exclusion has been approved.

The correction candidate includes Chapters 1 to 53, supplied teaching media and the new actual integrity-check script. The website and reading PDF were rebuilt from the maintained source and checked. The durable original release ZIP/PDF remains a historical baseline. The current reading PDF is not the final accessible tagged edition.

**Pushed and remote-verified:** commit `8b0228f640e4f056c11b2b65ff98e004d153d7ce` on `main` in `ctrotech-tutor/playbook`.

```sh
git pull --ff-only origin main
```

Run this from your repository while on `main`; keep your own uncommitted edits safe. The repository contains the maintained source, compiled website, reading PDF and audit documentation. A repository update is not proof of a new Vercel deployment. Hosted Node 24 Ubuntu and Windows CI passed for content commit `8b0228f`; `repository-sync.json` contains its run/job evidence. A deployment claim still requires its own live checks.

## Read the work

- **[Batch 04 findings and evidence](batch04-report.md)**: actual interaction/attribute/metadata improvements, native tests, checker gaps and coverage limits.
- **[Revised Chapters 42 to 53](batch04-chapters42-53.md.gz)**: losslessly archived manuscript, objectives, prerequisites, primary examples, exercises, explained answers and sources.
- [Revised Chapters 28 to 41](batch03-chapters28-41.md.gz) and [batch 03 report](batch03-report.md).
- [Revised Chapters 14 to 27](batch02-chapters14-27.md.gz), [batch 02 report](batch02-report.md) and [batch 01 report](batch01-report.md).
- `audit-register.json`: all 74 chapter states, all 81 requirements and 25 findings.

Older batch prose and receipts describe their recorded checkpoints. A historical count/fingerprint is not current whole-candidate evidence.

## Four final gates

| Gate | State |
| --- | --- |
| Manuscript and answers | Open: Chapters 54–74 still need the first pass, followed by deeper claim-level and independent review. |
| Full promised coverage | Open: complete values/defaults, restrictions, algorithms, conversions/exceptions, members and cross-specification reconciliation remain. |
| Accessibility and security | Open: native scoped keyboard/pointer/local-request and automated checks are not actual OS assistive-technology, touch/IME or complete security approval. |
| Accessible tagged PDF | Open: the rebuilt 427-page reading PDF is not the tagged final publication. The earlier four-page prototype remains separate. |

Next batch: **Chapters 54–67, browser and professional practice.** The audit is the method for completing the content, not a replacement for it or a task transferred to the author.

## Current candidate integrity

Baseline commit: `41550987440d2b9cb59f1eac11d46c7463ba42e7`  
Current fingerprint: `439f8ba540d68e88145e2be29719eddb1249f0dbe3242638edd882de7b015a94`

- `candidate-verification.json`: source and deployment-fixture QA, recovery-patch hashes and boundaries.
- `candidate-static-verification.json`: final generated-output QA.
- `batch04-browser-checks.json`: selected Chapters 42–53 interaction, reflection, local SRI/CORS/CSP/referrer and 320px tests in three engines.
- `batch02-browser-checks.json`, `batch03-browser-checks.json` and `sandbox-candidate-regression.json`: earlier scoped regressions re-executed against this current candidate.
- `candidate-node-tests.log` and `candidate-output-tests.log`: 14 plus three passing Node tests.

Nu accepted two intentionally invalid interaction controls in this batch. A zero-message checker result is not complete authoring or behavioral approval.

## Recovery and storage

`candidate-source.patch.gz` is a losslessly compressed cumulative maintained-source patch against the baseline, now covering 15 files. Decompress and apply it to a separate baseline checkout before rebuilding and verifying. It is recovery material, not a complete deployable final-release package.

`batch02-coverage-review.csv.gz`, `batch03-coverage-review.csv.gz` and `batch04-coverage-review.csv.gz` retain the open owner-route triage. Source archives are bounded verification extracts with third-party-rights notices, not complete specification copies or completed reviews of every nested API.

`AUDIT-FILES.json` records audit file sizes/hashes and excludes itself. Large historical manuscripts and the source patch are retained losslessly without duplicating complete generated website/PDF trees. Repository synchronization evidence, when available, is recorded separately in `repository-sync.json`.

Copyright, author credit, third-party notices, AI-assisted preparation and syntax highlighting remain intact. No new open editorial license has been selected.
