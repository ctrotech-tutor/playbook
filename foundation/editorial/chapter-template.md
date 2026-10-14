# Chapter production template — not Chapter 1

```yaml
id: CH-XX
slug: replace-with-unique-slug
title: Replace with the approved title
status: planned
prerequisites: []
objectives: []
coverage_ids: []
reference_entries: []
example_ids: []
exercise_ids: []
sources: []
normative_review: pending
accessibility_review: pending
security_review: pending
compatibility_review: pending
example_review: not_written
exercise_review: not_written
editorial_review: pending
reviewer: null
reviewed_at: null
evidence: []
```

## Before you start
Prerequisites; what the reader can already do; terms introduced; measurable objectives.

## The mental model
A plain-language explanation followed by precise definitions. Identify standard requirements, recommendations, browser observations, accessibility guidance and optional engineering choices.

## First purposeful example
Include or extract source from a real example file. State its surrounding context, expected DOM/behavior and testable outcome. Explain why the markup is appropriate.

## Deeper behavior and constraints
Permitted contexts/content, categories, valid attributes/values, defaults, state restrictions, parser behavior and interface/reflection ties where relevant. Link the reference entry rather than duplicating a separately maintained list.

## Accessibility and security
Topic-specific implications, native semantics, names, keyboard/focus behavior, trust boundaries and safe alternatives. Mark not applicable only with a reviewed explanation.

## Compatibility and progressive enhancement
Review date, pinned BCD/version evidence, flags/notes, tested environments, fallback and remaining uncertainty. Standard presence is not implementation evidence.

## Mistakes and repairs
Deliberately invalid or problematic examples must be labeled, explained and corrected. Test that the expected-failure fixture detects the intended mistake.

## Practice and explained solutions
Prediction question; diagnosis or repair task; practical build where suitable. Explain why each answer is correct and why plausible alternatives fail. Reference runnable answer fixtures.

## Summary, reference and next steps
Objectives revisited; exact normative sources and secondary explanations; glossary links; next chapter; reference entries; last review date.

## Acceptance evidence
- [ ] Each assigned coverage record reconciled against its actual definition.
- [ ] Examples have executed conformance and relevant behavioral checks.
- [ ] Expected failures verified; no invented pass claims.
- [ ] Exercise/quiz answers verified against actual examples.
- [ ] Accessibility, security and compatibility review recorded.
- [ ] All links, IDs and prerequisites resolve.
- [ ] Prose, site rendering and PDF rendering reviewed.
- [ ] Reviewer, date, evidence paths and remaining limitations recorded.
