# Chapter 70: Build a registration form

## Objectives

- Associate required labels, instructions and field errors with three practice controls.
- Keep a no-script or failed-script form disabled instead of falling back to GET collection.
- Test linked error correction, reset and honest local-success messaging.

## Before you start

Review Chapters 34, 35, 36, 38, 40, 41, 53, 66. Build labelled controls, inspect browser validity, distinguish form submission from local script and preserve a safe failure baseline.

## Working terms

Constraint validation checks applicable browser-side rules, not server trust. An error summary collects correction links above a form. Custom validity is a script-supplied message that makes a control invalid while the message is nonempty. A disabled baseline keeps this practice task unavailable until its local handlers are installed.

## Build contract
Collect only fictional practice values for name, one email and a session choice. This is a browser-side interface study, not a registration service. The baseline fieldset is disabled. No control has a submission name and there is no application endpoint. Tell readers not to enter personal information. The local script must install its handlers before enabling fields, cancel submit, validate the fields and display only a local result.

## Implementation route
Use explicit labels and visible required indicators. Leave native `required` and `type="email"` constraints on the controls. After setup, `form.noValidate = true` selects the custom-summary submit path; it does not remove ValidityState or make the values trusted. The script inspects each control's validity and adds a non-whitespace rule for the practice name with `setCustomValidity()`. The browser email syntax check cannot prove that an address exists or belongs to the user.

Place a summary before the form with links to invalid fields. Reveal inline error text, set `aria-invalid="true"` only on failed fields and focus the summary after an unsuccessful submit. Use stable description IDs for the field messages and email hint. When the learner edits a failed field, revalidate it and remove that error when corrected. Clear any previous success message as soon as input changes. The script builds message nodes using text content, not HTML interpolation.

## Acceptance and recovery
Submit all fields empty, then a whitespace-only name and malformed email, then a valid practice set. Follow every summary link with the keyboard. Confirm that no form navigation or application request occurs and the URL does not acquire query values. Reset after an error and after success; values, errors, invalid states and custom name validity must return to their initial state. With JavaScript disabled or `demo.js` blocked, the form remains disabled and its explanation stays readable. This is failure containment for this static reference, not a claim of universal browser privacy.

## Reference walkthrough
The chapter's marked form content is reused in both the registration and capstone downloads. One maintained local script supplies both copies. The form has no named application controls, but that omission is not the primary no-submit mechanism: the disabled baseline and installed submit handler are essential. `autocomplete="off"` is only a browser hint and cannot guarantee that a browser stores nothing. The demonstration does not write application data to cookies or Web Storage. A real service needs a real endpoint, server validation, an appropriate transport and request-security design, data minimisation and a truthful retention notice; enabling this static form is not that implementation.

## Assessment rubric: 28 observable points
Award one point for each demonstrated check below, four per area. Record the evidence next to the check; untested checks receive no point. These points are an authoring assessment aid, not WCAG conformance or security certification. A broken primary task, a misleading service claim, unsafe data collection or a dead required destination blocks readiness regardless of the score.

### Control contract (4 points)
- The page visibly says practice only.
- Exactly name/email/session data are requested.
- All controls have explicit labels.
- Required state is visible and programmatic.

### Disabled baseline (4 points)
- The initial fieldset is disabled.
- No application endpoint is claimed.
- Blocked scripting leaves the fields disabled.
- Instructions remain readable without scripts.

### Validation (4 points)
- Empty values produce three errors.
- Whitespace-only name is rejected.
- Malformed single-email syntax is rejected.
- A valid practice set produces only local success.

### Error navigation (4 points)
- The summary precedes the form.
- The failed-submit summary receives focus.
- Each error link focuses its field.
- Each invalid field has an associated visible message.

### Correction (4 points)
- Invalid fields expose aria-invalid.
- Correcting a failed field removes its error.
- Editing removes an earlier success message.
- Hidden summary content is not left visibly stale.

### Reset (4 points)
- Name/email/session values reset.
- Custom name validity resets.
- Inline and summary errors clear.
- Invalid attributes and earlier success clear.

### Boundary evidence (4 points)
- Submit does not change the URL.
- No application request is emitted.
- The script writes no application storage.
- Real-service requirements are clearly distinguished.

## Exercise

Why must this static reference not use a GET-to-fragment fallback? Describe the failed-script behaviour, then explain what reset must clear after a whitespace-name error.
