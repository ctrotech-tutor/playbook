# Chapter 74: Capstone: the library site

## Objectives

- Integrate Home, Catalogue, Membership and Visit with consistent navigation and truthful service boundaries.
- Reuse and retest the disabled-baseline local form instead of implying a real membership backend.
- Assess the whole extracted site against observable functional, accessibility and privacy checks.

## Before you start

Review Chapters 27, 61, 62, 66, 68, 69, 70, 71, 72, 73. Complete the six smaller projects, plan file routes and test both successful enhancement and failed-script recovery.

## Working terms

Integration testing checks connected components as one task flow. A service boundary identifies what the static interface cannot do. An acceptance blocker is a critical failure that prevents readiness even when other rubric points are earned. Offline delivery means the supplied local documents and resources can be used without fetching a remote dependency.

## Build contract
Deliver four documents: `index.html`, `catalogue.html`, `membership.html` and `visit.html`. The fictional context must be visible throughout the site. Home links readers to the other tasks. Catalogue contains three fictional titles and their collections. Membership reuses the Chapter 70 local demonstration, not a collection endpoint. Visit supplies fictional practice hours and explicitly says that no actual destination, access conditions or contact route have been verified.

## Implementation route
Use the same primary-navigation labels and destinations on every page, with exactly one current-page marker. Give each document its own title and main heading. Keep the catalogue caption and headers meaningful. Bound its wide table inside a labelled, focusable scroll region rather than hiding its second column on a phone. Reuse the form markup and maintained script from Chapter 70, then test that the integration still preserves all error, correction, reset and failed-script behaviours.

## Truthful visit information
The practice timetable is Tuesday to Saturday, 09:00 to 17:00, closed Sunday and Monday. These are example hours, not a real timetable. Do not infer step-free access from an invented building or publish an imaginary address as a destination. The reference clearly states that entrance routes, parking and facilities are unverified. A real service needs verified location and relevant access details, not a generic accessible badge.

## Acceptance and recovery
Enter the site through every page directly and follow every primary link. Check all four at 320 CSS pixels, with keyboard-only navigation and without scripting. Use valid and invalid fictional values on Membership and inspect requests and the URL. Re-run the form suite rather than assuming component reuse proves correct integration. Extract the ZIP and inspect the same tasks offline. Styles or images failing should not remove the page's content, and script failure must leave the form disabled.

## Reference walkthrough
The supplied site offers only reading and local validation tasks. It cannot reserve a title, accept an application, search a catalogue or record a visit. Catalogue entries are static HTML, not a backend disguised by a polished layout. The Visit page makes its missing real-service details explicit. README, BRIEF and SOLUTION describe these limits from the same chapter source. This reference is a teaching implementation, not independent accessibility approval, a security audit or a production service.

## Assessment rubric: 28 observable points
Award one point for each demonstrated check below, four per area. Record the evidence next to the check; untested checks receive no point. These points are an authoring assessment aid, not WCAG conformance or security certification. A broken primary task, a misleading service claim, unsafe data collection or a dead required destination blocks readiness regardless of the score.

### Four-page contract (4 points)
- All four required documents exist.
- Every page has its own document title.
- Every page has a main heading.
- Fictional static-service status is visible.

### Navigation (4 points)
- All primary labels are consistent.
- All primary destinations resolve from every page.
- Exactly one current-page link appears per page.
- The skip link reaches each main landmark.

### Catalogue (4 points)
- Three fictional entries are supplied.
- The caption describes the data.
- Row and column headers identify relationships.
- The table scrolls inside a named keyboard-focusable region.

### Membership safety (4 points)
- The no-script baseline is disabled.
- Setup enables only local validation.
- Invalid submit provides linked field errors.
- Valid submit claims no sent application.

### Membership recovery (4 points)
- Correcting failed fields removes their errors.
- Editing clears prior success.
- Reset clears values/errors/custom validity.
- Blocked script leaves instructions and disabled fields.

### Visit truth (4 points)
- Practice hours are explicitly fictional.
- Sunday/Monday closure is stated.
- No real address or contact is invented.
- Access conditions are explicitly unverified.

### Integrated evidence (4 points)
- Every page opens directly after extraction.
- All four pages fit a 320-pixel viewport outside tables.
- Keyboard focus remains visible.
- Submit emits no application request or URL values.

## Exercise

Home passes a visual check, but Membership submits named values with GET when its script is blocked and Visit claims step-free access without evidence. Can a high rubric total make this ready?
