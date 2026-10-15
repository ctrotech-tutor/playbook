# Final-readiness content audit

**The HTML Playbook | Odejobi Abiola Samuel | CTROTECH**  
Updated: **15 October 2026**

## Current position

**67 of 74 chapters have received a substantive first pass; seven remain.** No chapter has independent approval. All 81 original requirements and the four final-publication gates remain open. There are 30 recorded findings and no approved scope exclusions. Chapter passes and inventory mentions are not exhaustive feature/API coverage.

The cumulative correction candidate covers Chapters 1–67, supplied teaching media and actual interaction/filtering/integrity/worker examples. The website and 438-page reading PDF are rebuilt from the maintained source. The PDF is not the final tagged accessible edition.

Repository delivery is through `main` in `ctrotech-tutor/playbook`. Check `repository-sync.json` for the exact verified pushed commit and its actual CI state. A passing local check or Git push does not establish a new Vercel deployment.

```sh
git pull --ff-only origin main
```

Run that from your repository on `main`, keeping your own uncommitted edits safe.

## Read the work

- **[Batch 05 report](batch05-report.md)**: browser/professional-practice corrections, working examples, native evidence and retained verification anomaly.
- **[Revised Chapters 54–67](batch05-chapters54-67.md.gz)**: lossless manuscript archive with objectives, prerequisites, examples, exercises, answers and sources. Canonical source remains `content/chapters.json`.
- [Batch 04 report](batch04-report.md) and [Chapters 42–53](batch04-chapters42-53.md.gz).
- [Batch 03 report](batch03-report.md) and [Chapters 28–41](batch03-chapters28-41.md.gz).
- [Batch 02 report](batch02-report.md), [Chapters 14–27](batch02-chapters14-27.md.gz) and [batch 01 report](batch01-report.md).
- `audit-register.json`: 74 chapter states, 81 requirements, 30 findings and explicit coverage boundaries.

Historical reports describe their original checkpoints. Their counts and fingerprints are not automatically current whole-candidate evidence.

## Four final gates

| Gate | State |
| --- | --- |
| Manuscript and answers | Open: Chapters 68–74 still need the first pass, followed by deeper claim-level and independent review. |
| Full promised coverage | Open: complete values/defaults, restrictions, algorithms, conversions/exceptions, inherited/imported members and cross-specification reconciliation remain. |
| Accessibility and security | Open: scoped keyboard/pointer/native/local-request and automated checks are not OS AT, full WCAG, real touch/IME/device or complete security approval. |
| Accessible tagged PDF | Open: the reading PDF has selectable syntax-coloured text and bookmarks, not a full semantic tag tree. The four-page prototype is not a full-book certificate. |

Next: **Chapters 68–74, projects and capstone**, then the required full reconciliation and reviews. This work is not reassigned to the author.

## Current candidate integrity

Baseline commit: `41550987440d2b9cb59f1eac11d46c7463ba42e7`  
Current fingerprint: `cec82d32c5a8573d5f96523cd66675b8ff50153b7a82bfb55dfbf347827c843a`

- `candidate-verification.json`: source/deployment-fixture evidence, cumulative source-patch hashes and limits.
- `candidate-static-verification.json`: final generated-output verification.
- `batch05-browser-checks.json` and `batch05-compiled-browser-checks.json`: selected new examples and native parser/lifecycle/API/security cases, with 320px chapter/example checks in three engines.
- `batch02-browser-checks.json`, `batch03-browser-checks.json`, `batch04-browser-checks.json` and `sandbox-candidate-regression.json`: earlier scoped regressions re-executed against this candidate.
- `candidate-node-tests.log` and `candidate-output-tests.log`: 14 plus three passing Node tests.

An earlier concurrent predecessor scan reported one `summary-name` issue. Its failure log and five isolated probes are retained. Later sequential checks passed without disabling the rule; the root cause remains unproven and the manual accessibility gate remains open.

## Recovery and storage

`candidate-source.patch.gz` is the cumulative, losslessly compressed maintained-source recovery patch against the baseline, covering 17 files. Apply it in a separate baseline checkout before rebuilding and checking. It is not a complete deployable final-release package.

Batch 02–05 `coverage-review.csv.gz` files preserve overlapping captured owner routes; all stay open. Source excerpts are bounded verification records with original third-party rights, not full specification copies or completed nested-API reviews.

`AUDIT-FILES.json` records file sizes/hashes, excluding itself. JSON values are preserved in compact formatting. Workspace baseline storage was separately archived with byte checks; that historical workspace archive is not required by this repository. Use this checkout for the current maintained source and reading outputs, or the baseline Git commit plus recovery patch for reconstruction.

Author credit, copyright, third-party notices, AI-assisted preparation and syntax highlighting are preserved. No new open editorial license has been selected.
