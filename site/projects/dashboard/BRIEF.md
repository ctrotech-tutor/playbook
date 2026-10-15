# Chapter 72: Build a data dashboard

## Objectives

- Reconcile a displayed total with all three fictional collection counts.
- Provide a caption and explicit row and column headers for a simple data table.
- Keep wide data readable in a labelled keyboard-focusable scroll region.

## Before you start

Review Chapters 26, 61, 62. Create a captioned simple table, distinguish headers from data and test a keyboard-accessible scrolling region.

## Working terms

A measure is the quantity counted, here loan entries. A unit tells readers how to interpret a value. Reconciliation checks that summary and rows describe the same dataset and arithmetic. A table header association connects a data cell with its relevant row or column heading.

## Build contract
Build a static October 2026 dashboard for three fictional loan counts: Fiction 42, Local history 18 and Reference 9. Display their total, 69 loans, and the count of represented collections, three. Label the values as fictional loan entries, not unique people, stock levels or live availability. There is no comparison period, so do not invent a growth arrow or percentage.

## Implementation route
Use a description list for the named summary values and a table for the cross-row data relationships. Give the table a caption that identifies the subject and period. Mark column headers with `scope="col"` and each collection's row header with `scope="row"`. Include a period column so that a copied row retains useful context. Scope is suitable for this simple grid; complex multi-level tables need an explicit association review rather than a mechanical copy of this example.

## Acceptance and recovery
Recalculate the total from the rows, then compare every displayed summary against the table. At 320 CSS pixels, the document itself should fit the viewport. The wide table may scroll inside its labelled region; preserve the two-dimensional relationships instead of hiding columns. Tab to that region, check its visible focus and inspect horizontal scroll. Reflow permits exceptions for content that requires two-dimensional layout, but the exception does not excuse page-wide overflow or an inaccessible scrolling surface.

## Reference walkthrough
The supplied dashboard is all static HTML. It exposes the period, units and fiction notice without hover, script or colour interpretation. Its summary cannot remain correct if someone changes a row without updating the total, so reconciliation is an explicit acceptance check. The scroll wrapper is focusable and named. Native markup provides associations for this simple table; confirming its actual presentation in a screen reader still requires an assistive-technology review.

## Assessment rubric: 28 observable points
Award one point for each demonstrated check below, four per area. Record the evidence next to the check; untested checks receive no point. These points are an authoring assessment aid, not WCAG conformance or security certification. A broken primary task, a misleading service claim, unsafe data collection or a dead required destination blocks readiness regardless of the score.

### Data truth (4 points)
- Fictional status is visible.
- The period is October 2026.
- Units mean loan entries.
- No live feed or unsupported comparison is claimed.

### Rows (4 points)
- Fiction is 42.
- Local history is 18.
- Reference is 9.
- All three rows carry the period.

### Summary (4 points)
- Total is visibly 69 loans.
- The total equals 42 + 18 + 9.
- Three collections are reported.
- Summary labels explain their quantities.

### Table structure (4 points)
- A subject-and-period caption is present.
- A thead groups column headings.
- Each column heading has scope=col.
- Each collection heading has scope=row.

### Narrow layout (4 points)
- The 320-pixel document fits its viewport.
- The table is inside a bounded scroll region.
- No data column is hidden.
- The scroll region has an accessible name.

### Keyboard and baseline (4 points)
- The table region can receive keyboard focus.
- Focus is visible.
- Data remain readable without scripts.
- Reading order retains caption/headings/rows.

### Delivery (4 points)
- Local CSS resolves.
- Document title identifies the dashboard.
- No unexplained chart substitutes for data.
- Solution notes require recalculation after edits.

## Exercise

Someone changes Reference from 9 to 12 but leaves 69 loans in the summary and adds “69 readers.” What needs correction and why?
