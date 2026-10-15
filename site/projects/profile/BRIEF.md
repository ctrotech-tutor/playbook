# Chapter 68: Build a personal profile

## Objectives

- Organise a fictional person's introduction and experience into a useful heading structure.
- Make a descriptive contact-status link resolve to real content.
- Distinguish a complete static profile from a working contact service.

## Before you start

Review Chapters 7, 14, 17, 18, 23, 25. Create a document shell, choose headings, make a list and connect a same-page link.

## Working terms

A fragment is the part of a URL after # that can identify a document destination. A landmark identifies a major page region through native HTML or an appropriate role. Contact status explains whether a contact route actually exists; it is not itself a messaging service.

## Build contract
Create a one-page profile for Ada, a fictional library volunteer. Include one page-level title, a short introduction, three relevant practice activities and a contact-status section. Make the fictional context visible rather than relying on a README. Do not invent a real address, availability claim or endorsement. The reference has no portrait because no visual information is needed to complete this task.

## Implementation route
Begin with the content, then choose the structure. Put the whole page topic in the main heading. Experience and contact status are separate sections with second-level headings. Use a list for the three activities, not a table or a row of decorative cards. A link to `#contact` takes the reader to the status section. It is navigation, so it remains an anchor even if styled prominently.

## Acceptance and recovery
Open the file without JavaScript. Read it in document order, activate the contact-status link with Enter and confirm that the destination explains the absence of a contact service. Try a 320 CSS-pixel viewport and enlarge text. The profile should remain readable without page-wide horizontal scrolling. No-script operation is a property of this static design, not a claim that the reader has tested it.

## Reference walkthrough
The download adds a language declaration, title, viewport metadata, a keyboard skip link and a local stylesheet around the subject content. Its activity statements are explicitly practice tasks. The contact section gives no coordinator instruction that might be mistaken for a real service. Replacing that status with a real route is a separate publishing decision requiring verified details and the person's agreement.

## Assessment rubric: 28 observable points
Award one point for each demonstrated check below, four per area. Record the evidence next to the check; untested checks receive no point. These points are an authoring assessment aid, not WCAG conformance or security certification. A broken primary task, a misleading service claim, unsafe data collection or a dead required destination blocks readiness regardless of the score.

### Content and truth (4 points)
- Fictional context is visible.
- Ada is named.
- Introduction identifies the practice role.
- No unverifiable service claim appears.

### Structure (4 points)
- One main landmark is present.
- The page topic has an h1.
- Experience has an h2.
- Contact status has an h2.

### Experience (4 points)
- Three activities are supplied.
- Activities form a native list.
- Each activity is specific.
- No table is used for layout.

### Contact navigation (4 points)
- The link says what it opens.
- Its fragment matches a unique ID.
- Keyboard activation reaches the section.
- The section states no contact route is supplied.

### Baseline (4 points)
- No script is needed to read.
- No script is needed to navigate.
- Stylesheet failure leaves logical content.
- No fabricated form is present.

### Presentation (4 points)
- Text remains readable at 320 CSS pixels.
- The page has no horizontal overflow.
- Keyboard focus is visible.
- Text enlargement does not hide the contact section.

### Delivery (4 points)
- The HTML has a useful document title.
- The language is declared.
- All local links resolve.
- The README explains how to open the page.

## Exercise

A learner replaces the contact-status anchor with a button that does nothing and removes the fictional notice. Which checks fail, and what is the smallest truthful repair?
