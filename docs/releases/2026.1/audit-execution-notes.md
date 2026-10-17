# Release-check execution notes

The initial attempt to run four whole-site axe ranges plus native security checks concurrently exhausted the 2 GiB sandbox working memory. One native browser navigation timed out; this was not reported as a security assertion pass. The incomplete ranges were stopped and rerun sequentially, without changing rules, test assertions or publication source. Completed final range reports and the later native regression report are the evidence of record. The initial native timeout log is retained.

The primary PDF validation initially rejected a CFF subset with missing-glyph references. That failed staging artifact was never promoted. Its XML is retained. The corrected, renamed and licensed TrueType subset passed a small glyph-profile test, full-book validation, canonical-text/structure checks and syntax/font checks.
