# CTROTECH HTML Playbook

By **Odejobi Abiola Samuel**. © 2026 Odejobi Abiola Samuel. Third-party rights are retained.

This is the self-deployable Vercel delivery of the playbook. No GitHub repository or integration is required. The ZIP contains the precompiled reading site, matching PDF, canonical content, local fonts, source notices, builders and verification receipts.

**Content status:** all 74 chapter drafts are present. The declaration register is substantially expanded, but exhaustive behavioral documentation and independent technical/answer review remain open. This package is not represented as a completed whole-Standard audit or a tagged accessible PDF.

## Deploy on Vercel

1. Unzip the package and open a terminal in the folder containing `vercel.json` and `package.json`.
2. Use Node.js 24 and install the Vercel CLI on your computer if needed:

```sh
npm install --global vercel@latest
vercel login
vercel deploy --prod
```

3. Select your own Vercel account/team and create the project when prompted. Use the current folder as the project root. The package supplies the build settings.
4. Check the returned production URL. Open a chapter, search, a reference page, the PDF and a deliberately nonexistent address.

`vercel.json` selects the static/Other preset, runs `npm ci --ignore-scripts` and `npm run build`, and publishes only `dist/`. There are no application functions or collection backends. Hosting plan limits and terms still apply.

The agent has not signed in, linked an account, created a project or deployed this package. Your own CLI login and deployment happen on your computer.

### Production domain and canonicals

The build uses `SITE_URL` if you set it. Otherwise, it uses Vercel's `VERCEL_PROJECT_PRODUCTION_URL`, prefixed with HTTPS. This works with a Vercel project domain or a custom domain.

Keep Vercel's **Enable access to System Environment Variables** setting enabled. If the production domain cannot be resolved, the build stops with an actionable error rather than publishing placeholder canonicals.

Set `SITE_URL` to the bare origin, for example your real `https://book.your-domain`, without a path, query, credentials or port. The `.env.example` lists optional public configuration names. Set cloud build variables in Vercel's project settings; do not upload private `.env` files.

Choose one primary domain and redirect extra aliases in Vercel's domain settings. After adding or changing the primary domain, rebuild so canonicals, sitemap, social image URLs, feed and structured data use it.

Preview and development builds are intentionally not indexable. A local build without a domain has no fabricated canonical URLs. The production build has indexable reading pages; thin demonstrations, raw downloads and operational pages are kept out of the sitemap and marked noindex where appropriate.

## What is included

- 74 chapter drafts with objectives, examples, common mistakes, source routes and explained exercises
- 113 named built-in HTML element entries, with integration/custom-element boundaries kept separate
- 314 named WebIDL declaration owners and 1,574 direct member declarations, including 1,398 matched member routes and labelled owner-route fallbacks
- 437 public keyword, state, enumeration-value and event definition records
- Seven complete static reference projects and 74 exact UTF-8 example files
- A 401-page PDF with 400 bookmarks, selectable syntax-coloured HTML/WebIDL, author metadata, XMP metadata, language metadata and attached font/source notices
- Search, chapter navigation, reading settings, local progress, exact copying and an opaque-origin editable preview
- Production-domain SEO, social cards, JSON-LD, XML/HTML sitemaps, a release feed, Markdown chapters and plain-text discovery exports

Read `PRODUCTION-READINESS.md` for the distinction between delivered reference declarations, executed checks and unfinished behavior-level review.

## Run locally

```sh
npm ci --ignore-scripts
npm run build
npm start
```

Open the server's displayed address. The default port is 3000. Local output is deliberately noindex until built in production mode with a real origin. Static assets and fonts are local; there are no analytics or CDN runtime dependencies.

`npm start` is a local route/header preview, not a Vercel backend. A temporary HTTPS fixture is used by the cross-engine checks because WebKit upgrades HTTP subresources under the production CSP.

## Maintain the book

The authoritative content is in `content/chapters.json`, `content/publication.json`, `content/reference-snapshot.json`, `content/api-register.json`, `content/glossary.json` and `content/value-routes.json`.

After changing maintained content or build inputs, rebuild the precompiled site and PDF:

```sh
python3 -m pip install -r requirements-build.txt
python3 tools/build.py --pdf
npm run build
```

The Python build writes `build/site/` and `deliverables/ctrotech-html-playbook.pdf`. It uses bundled fonts, not system-installed font binaries. The deployment ZIP supplies the compiled `site/` fallback, so ordinary Vercel deployments do not need Python, Java or a live specification fetch.

The Node build prefers a freshly generated `build/site/`, otherwise it uses the supplied `site/`. Its input manifest checks the maintained bytes. If you edit the manuscript and forget to regenerate the compiled source, deployment fails instead of silently shipping inconsistent content.

### Refresh upstream declaration data

```sh
npm ci --include=dev --ignore-scripts
node tools/update_api_register.mjs --refresh
```

This explicitly retrieves current W3C Webref extraction files. Review the differences, source hashes and source licenses before accepting an update. Then rebuild and reverify. Mutable upstream URLs are not historical snapshots. New declaration counts are not a substitute for reviewing behavior and compatibility.

## Verification

The retained receipts cover:

- 493 source-built HTML documents with zero Nu messages
- 497 generated Vercel HTML documents with zero Nu messages
- 2,654 live source URL/fragment targets in 75 documents
- Exact chapter-code preservation in website code, raw UTF-8 files and archive entries
- All 349 consolidated/partial WebIDL declaration blocks found in extracted PDF code text
- PDF token contrast of at least 5.42:1 and a four-page wrapping/splitting regression
- Chromium 156.0.8078.4, Firefox 157.0 and WebKit 27.2 smoke tests using local HTTPS fixtures
- No mobile page overflow at 390px across 397 tested pages in Chromium, with 12 representative routes in each additional engine
- Zero automated axe violations on 16 representative pages, not a WCAG certificate
- Correct local 308 redirects, genuine 404 responses, non-submitting demo forms and parent-blocked editable iframes

The synthetic `.example.test` origin appearing in verification receipts is a test fixture. It is not a production domain and is not embedded as a canonical in the supplied precompiled source.

To rerun the full checks, install the pinned verification dependencies, browsers and their host libraries, then obtain the recorded Nu checker:

```sh
npm ci --include=dev --ignore-scripts
python3 -m pip install -r requirements-verify.txt
python3 tools/install_nu.py
python3 -m playwright install chromium firefox webkit
python3 -m playwright install-deps chromium firefox webkit
python3 tools/build.py --pdf
python3 tools/check_sources.py
python3 tools/verify.py
python3 tools/build.py
python3 tools/verify_seo.py
python3 tools/build.py
python3 tools/check_build.py
python3 tools/verify_seo.py --static-only
```

Use Node 24 for these commands. Nu verification also needs Java; Java 21 was used. The Nu installer enforces a recorded SHA-256 and fails if the mutable upstream asset changes. Do not bypass that check. Source-target checks verify availability, not every assertion's interpretation.

## SEO and AI discovery

Read `SEO-OPERATIONS.md` for optional verification tokens, crawler policy, IndexNow, post-deployment checks and limits. No metadata can guarantee indexing, rankings, rich results or inclusion in an AI answer. No search account has been verified or sitemap submitted on your behalf.

## Rights and notices

Original editorial work carries the requested author/copyright notice. No new open reuse license or blanket grant has been selected. That does not stop the author from deploying the publication; it also does not restrict rights already granted by upstream licenses.

WHATWG source material, W3C Webref extraction software, selected Browser Compatibility Data and the fonts retain their respective notices. Material has been extracted, arranged and linked; upstream endorsement is not implied. Complete notices are included under `docs/third-party/`, `assets/` and `fonts/pdf/`. Applicable notices are also attached to the standalone PDF. Humanizer guidance remains under its supplied MIT license in `docs/writing-guidance/`.

## Delivery and integrity

`tools/package.py` builds the Vercel ZIP with a per-file SHA-256 manifest and verifies its CRC. `deliverables/package-checksums.json` supplies the final artifact hashes. The previous review archives are superseded by this deployment bundle. Generated `build/` and `dist/` folders are disposable outputs, not separate sources of truth.
