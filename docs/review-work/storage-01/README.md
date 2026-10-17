# Storage unit evidence and replay

Prepared 17 October 2026. Unreleased work. See the [readable manuscript](storage-behavior-review.md) and [overall checkpoint](../README.md).

## Evidence

- `contract-source.json`: sole authored review unit, including exact exercise code.
- `render_review.py`: reproducible source-to-Markdown renderer.
- `storage-browser-results.json`: 267 executed observations, one open WebKit observation.
- `exercise-browser-results.json`: 30 passing exercise scenarios; denial/quota branch fault injections are identified.
- `normative-source-retrievals.json`: source URLs, retrieved date, full-capture sizes and hashes.
- `normative-captures/`: complete compressed source captures matching the retrieval hashes, including their original source notices.
- `normative-source-excerpts.json.gz`: selected algorithm text with source anchors, not a claim that every specification clause was reviewed.
- `initial-event-wait-timeout.log`: retained diagnostic history, not the current aggregate result.
- `orca-evidence/assessment.json`: bounded native keyboard and actual Orca evidence, with two open observations.
- `orca-evidence/speech-output.txt`: complete multiline speech-output transcript.
- `orca-evidence/orca-debug.log.gz`: full raw debug trace.
- `orca-evidence/speech-s16le-16000hz-mono.pcm.gz`: genuine output-monitor recording, not a generated voiceover.
- `orca-evidence/audio.json`: format, duration and exact uncompressed PCM hash. No human listening claim.
- `orca-evidence/initial-setup-result.json` and `first-keyboard-result-no-content-speech.json`: unsuccessful harness history, retained to avoid implying installation or keyboard-only evidence was a successful AT session.
- `evidence-manifest.json`: exact-file hashes and verified production non-change boundary.

The complete final trace, rather than a live buffered file, is used to attribute announcements to recorded task-time windows. This prevents late file flushes from being mistaken for absent announcements. The missing skip-link label remains an observation within a bounded window, not proof that it can never be announced. The long opening-dialog utterance needs a listener's usability judgment, not a guessed site patch.

## Linux harness prerequisites

The executed environment used Orca 48.1, AT-SPI 2.56.2, headed Chromium 156.0.8078.4 and Playwright 1.64.0. Required local tools include Xvfb, D-Bus, Openbox, xdotool, PulseAudio with `pactl`/`parec`, speech-dispatcher with the eSpeak-ng module, system Python with GI/pyatspi, and Python Playwright. This is a private virtual X11 environment, not NVDA, JAWS, VoiceOver or a physical desktop-user assessment.

The harness starts a dedicated PulseAudio null sink and foreground speech service using private sockets. It cleans up its own audio/window-manager/AT processes. The old shared speech daemon was unsuitable for this isolated recording fixture. No general user audio configuration should be changed for replay.

From the repository root, after installing these prerequisites:

```sh
mkdir -p .cache/orca/prefs
cp docs/review-work/storage-01/orca-harness/run.sh .cache/orca/run.sh
cp docs/review-work/storage-01/orca-harness/drive.py .cache/orca/drive.py
cp docs/review-work/storage-01/orca-harness/user-settings.conf .cache/orca/prefs/
# The launcher's browser-binary cache path must match your Playwright installation.
xvfb-run -a -s '-screen 0 1280x900x24 -nolisten tcp' \
  dbus-run-session -- bash .cache/orca/run.sh > .cache/orca/session.log 2>&1
python3 docs/review-work/storage-01/finalize_orca_evidence.py
```

The driver serves the existing `site/`, not a rebuilt new manuscript. On a new checkout, a verified production build must exist before replay. Always identify the served build, not only the current Git HEAD. Historical reports identify the baseline build used for this run. Replay outputs are new evidence and must not be represented as the historical run.

To create a WAV for an actual listener without resynthesizing or changing the recording:

```python
from pathlib import Path
import gzip, wave
p = Path('docs/review-work/storage-01/orca-evidence')
pcm = gzip.decompress((p/'speech-s16le-16000hz-mono.pcm.gz').read_bytes())
with wave.open('/tmp/orca-review.wav', 'wb') as out:
    out.setnchannels(1)
    out.setsampwidth(2)
    out.setframerate(16000)
    out.writeframes(pcm)
```

An output transcript records what Orca submitted for speech, not proof that every complete utterance was heard before the next interrupting key. The PCM monitor records actual output; an experienced listener still needs to assess intelligibility, task comprehension and interruption. No independent approval is recorded.

The frozen checkpoint verifier checks this baseline's unchanged production inputs and PDF. It is a review-only command, not a requirement that future editions keep the old production fingerprint.
