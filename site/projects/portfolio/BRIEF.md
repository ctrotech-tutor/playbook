# Chapter 69: Build a portfolio

## Objectives

- Connect two project summaries to separate working detail pages.
- Keep primary navigation and current-page information consistent.
- Describe static learning work without inventing clients, outcomes or a contact backend.

## Before you start

Review Chapters 17, 24, 25, 27, 61. Resolve sibling-relative links, structure independent project notes and plan navigation across files.

## Working terms

A project summary introduces one item of work; a detail page supplies its substantive explanation. A current-page marker describes the document currently being viewed. A relative URL is resolved against a base URL, so moving files can change its destination.

## Build contract
Deliver `index.html`, `project.html` and `reading-list.html`. The index introduces a fictional front-end learner's work, summarises two different studies and links each to its own detail page. The notice-board note explains a document-structure study; the reading-list note explains why its collection is a list. Include a contact-status section on the index. No contact form or real personal information is required.

## Implementation route
Write the two summaries before the navigation. Use articles for independently understandable project summaries, with third-level headings under Selected work. Give each link a destination-specific name. Reuse a primary navigation landmark across the three documents and mark only the current document's link with `aria-current="page"`. This attribute supplies current-page information; visible styling and actual destinations still matter.

## Acceptance and recovery
Open each detail page directly, not only through the index. Confirm that its title identifies its own subject and that its primary links still work. Return to `index.html#contact` from each detail. Remove scripting and check again. A browser reload, an extracted ZIP and a narrow viewport must not turn either project into an empty placeholder.

## Reference walkthrough
The supplied files have real relative links, consistent local CSS and no client or revenue claims. Each detail page includes actual sample content and a short design decision. The contact section states that the site does not collect messages. This meets the fictional exercise contract. A real professional portfolio would require the owner's own work, permission to show it, evidence for outcomes and an appropriate verified contact route.

## Assessment rubric: 28 observable points
Award one point for each demonstrated check below, four per area. Record the evidence next to the check; untested checks receive no point. These points are an authoring assessment aid, not WCAG conformance or security certification. A broken primary task, a misleading service claim, unsafe data collection or a dead required destination blocks readiness regardless of the score.

### Portfolio content (4 points)
- The fictional status is visible.
- An introduction is supplied.
- Two distinct studies are summarised.
- No unsupported client or outcome claim appears.

### Detail destinations (4 points)
- The notice-board link opens project.html.
- The reading-list link opens reading-list.html.
- Both detail documents contain substantive content.
- The two links do not lead to the same empty page.

### Structure (4 points)
- Selected work has a heading.
- Each project summary has a subordinate heading.
- Each page has a main landmark.
- Document titles distinguish the three pages.

### Navigation (4 points)
- All three pages expose primary navigation.
- All primary destinations resolve.
- Exactly one link per primary navigation is current.
- Both detail pages can reach the contact status.

### Contact truth (4 points)
- Contact status is present on the index.
- Its ID is unique.
- No fake message submission is offered.
- No real personal details are invented.

### Recovery (4 points)
- Each detail opens directly.
- Links work without JavaScript.
- Links work after ZIP extraction.
- 320-pixel reading does not cause page-wide overflow.

### Delivery (4 points)
- Each page declares its language.
- Focus styling is visible.
- All stylesheet references are local and resolve.
- Assessment notes identify static limitations.

## Exercise

Both project links currently open project.html, while reading-list.html contains only a title. Is the three-file count enough? Explain the repair and how to verify it.
