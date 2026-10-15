# Chapter 71: Build an article page

## Objectives

- Write consistent borrowing, renewal and return explanations rather than policy placeholders.
- Connect an on-page contents list to three unique section IDs.
- Encode a displayed review date using the time element.

## Before you start

Review Chapters 14, 17, 20, 24, 25. Organise a self-contained article, make fragment links and encode a date that matches its displayed text.

## Working terms

A policy model is the explicit fictional rule set used for this exercise. A review date identifies the stated editorial check date, not the date of every loan. Calendar-day arithmetic here follows the convention stated in the article; it does not infer a real organisation's counting rules.

## Build contract
Write an article titled How lending works with an introduction, an on-page contents navigation, Borrowing, Renewal and Returns sections, and a review date. Label the policy fictional on the page. Give enough information to evaluate the model without contacting a nonexistent desk. This exercise supplies a 14-calendar-day loan, one eligible 14-calendar-day renewal before the due date, and a paper-log practice return. The page itself processes none of these actions.

## Implementation route
Use an article because the guide is a self-contained subject, and give each substantive section its own heading and stable ID. The contents landmark needs a name distinct from any site-wide primary navigation. Describe the loan date arithmetic explicitly: a loan starting 1 October 2026 is due 15 October; one eligible renewal extends that due date to 29 October. Define this convention in prose instead of asking the reader to infer inclusivity from a bare number. Mark the review date with `time datetime="2026-10-15"` while displaying 15 October 2026.

## Acceptance and recovery
Activate all three contents links, inspect their fragments and verify each destination exists once. Read just the headings and confirm the policy sequence makes sense. Check the date attribute against the displayed review date. Disable scripts and repeat navigation. At narrow widths, the contents links must wrap without covering the article. A valid `time` value does not verify that an editor actually reviewed a policy; review provenance remains editorial evidence.

## Reference walkthrough
The supplied article contains the entire practice policy rather than an instruction to ask someone for it. It distinguishes a possible model extension from an actual renewal operation. Returns are represented as a local paper exercise, not a real address or live record. The article footer belongs to that article's review information; the outer project footer carries publication credit. Adaptation to a real library requires replacing both the fictional policy and the unverified service context.

## Assessment rubric: 28 observable points
Award one point for each demonstrated check below, four per area. Record the evidence next to the check; untested checks receive no point. These points are an authoring assessment aid, not WCAG conformance or security certification. A broken primary task, a misleading service claim, unsafe data collection or a dead required destination blocks readiness regardless of the score.

### Article contract (4 points)
- The article has the required title.
- Fictional policy status is visible.
- An introduction identifies the model.
- No real service is implied.

### Contents navigation (4 points)
- The nav has a descriptive accessible name.
- Borrowing links to its section.
- Renewal links to its section.
- Returns links to its section.

### Borrowing (4 points)
- The 14-calendar-day rule is stated.
- A start date example is supplied.
- Its due date is 15 October 2026.
- The model date convention is understandable.

### Renewal (4 points)
- Only one renewal is allowed in the model.
- Eligibility and before-due-date scope are stated.
- The extension is 14 calendar days.
- The sample extended due date is 29 October.

### Returns (4 points)
- A return procedure is actually described.
- The procedure is identified as practice.
- No real branch address is invented.
- No live return recording is claimed.

### Review and structure (4 points)
- Review text displays 15 October 2026.
- datetime contains 2026-10-15.
- All three section IDs are unique.
- The article headings form a coherent hierarchy.

### Resilience (4 points)
- Contents links work without scripts.
- All fragments resolve.
- The page reads at 320 CSS pixels.
- README and solution distinguish static policy from service.

## Exercise

An article says loans last 14 days after 1 October and gives a 14 October due date. Its displayed review date is 15 October but datetime is 2026-10-14. What should change?
