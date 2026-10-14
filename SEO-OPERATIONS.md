# SEO and discovery operations

## Build behavior

`SITE_URL` overrides the HTTPS origin inferred from `VERCEL_PROJECT_PRODUCTION_URL`. Set the primary production origin in Vercel's project settings if necessary. Never use the current preview URL as a production canonical. A production build without a valid origin stops.

The compiler writes unique titles and descriptions, author/Dublin Core metadata, canonical URLs, Open Graph/Twitter cards and language metadata. Indexed pages receive visible-content-consistent Person, Organization, WebSite, Book, chapter/reference and breadcrumb structured data where applicable. There are no fabricated credentials, reviews, ratings, endorsements, translated pages or answer guarantees.

Reading pages are rendered as real HTML. No JavaScript is needed to obtain the chapter prose or source links. JavaScript enhances search, progress, copying and editable demonstrations.

## Public discovery routes

- `/sitemap.xml`: XML indexable-page inventory with maintained editorial dates
- `/site-map`: human-readable sitemap
- `/robots.txt`: standard crawler policy and production sitemap location
- `/llms.txt`: discovery index and scope caveats, not a universal AI standard
- `/llms-full.txt`: chapter prose plus retained API declarations with publication/source caveats, not an independently reviewed complete Standard
- `/markdown/chapter-01.md` through `/markdown/chapter-74.md`: Markdown chapter exports
- `/feed.xml`: Atom release feed
- `/site.webmanifest`: installation/display metadata, not an offline-service-worker claim
- `/assets/social-card.<hash>.png`: generated local social card referenced by absolute production URLs

The generated output is the source of truth for exact hashed filenames and available feed paths. Do not hard-code an asset hash into external integrations.

## Optional ownership tokens

Set these public verification values in Vercel's project environment settings only when supplied by the corresponding service:

- `GOOGLE_SITE_VERIFICATION`
- `BING_SITE_VERIFICATION`
- `YANDEX_SITE_VERIFICATION`
- `PINTEREST_SITE_VERIFICATION`

Rebuild and then complete the ownership check inside your own account. Empty settings create no invented verification tags. These values are verification identifiers, not API keys or account credentials.

## Optional IndexNow

Supply a valid `INDEXNOW_KEY` before building if you want a public key file. The helper runs on your computer against a local `dist/sitemap.xml`: install the npm dependencies and build locally with `DEPLOY_ENV=production`, your real `SITE_URL` and the same `INDEXNOW_KEY` used in Vercel. Cloud environment settings do not automatically set your local shell variables.

The helper defaults to dry-run:

```sh
npm run indexnow
```

Review the host, key location and sitemap-derived URLs. Explicit submission requires:

```sh
npm run indexnow -- --submit
```

The helper can report an HTTP acceptance response, but that is not proof of indexing. IndexNow is not supported by every search engine. No submission was made during package preparation.

## Crawling versus training

The supplied production policy allows general search discovery, including OAI-SearchBot and Claude-SearchBot, and disallows GPTBot, ClaudeBot, Google-Extended and CCBot. These are crawler preferences, not guaranteed enforcement.

A standard robots policy is advisory crawler guidance, not access control or a copyright license. Search crawling, model training and user-triggered retrieval can use different user agents and policies. The default public policy does not create a special blanket training license. Its explicit training-bot exclusions are separate from its search-crawler allowances. Review current provider documentation before selectively excluding a training bot while retaining a search crawler. Keep important reading pages accessible if you want them discoverable.

Official guidance consulted:

- Google AI search features: https://developers.google.com/search/docs/appearance/ai-features
- Google search essentials: https://developers.google.com/search/docs/essentials
- OpenAI crawler distinctions: https://platform.openai.com/docs/bots
- Sitemap protocol: https://www.sitemaps.org/protocol.html
- IndexNow: https://www.indexnow.org/documentation

No special metadata guarantees inclusion in search results, rich results, LLM retrieval or generated answers. `llms.txt` is an optional discovery convention, not a generally enforced standard. Ordinary useful content, correct source links, accessible HTML and deployment quality still matter.

## After deployment

1. Set one primary domain and redirect any extra aliases in Vercel.
2. Inspect the rendered page source for the real canonical, absolute social image URL and actual author.
3. Fetch `/robots.txt` and `/sitemap.xml`. Check that production reading pages are indexable and preview hosts are not.
4. Follow a sitemap chapter URL, an API page and `/pdf`. Open a nonexistent URL and confirm a real 404 response rather than an SPA fallback.
5. Inspect security, cache and noindex headers on real deployed responses. Local route emulation does not certify Vercel's hosted configuration.
6. Validate a representative structured-data page using the target search engine's own tools. Eligibility and indexing decisions remain theirs.
7. If desired, verify the domain and submit the production sitemap inside your own search account. Neither account access nor submissions are included in this delivery.
8. Inspect search diagnostics over time. Update actual editorial dates when content changes, not merely on every build.

If an origin is changed, rebuild the site. Do not upload the synthetic production fixture used in the receipts as if it were your domain.
