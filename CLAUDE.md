# CLAUDE.md — Safe Travels website (CassSuczeck/website)

The coded version of besafetravels.com for **Safe Travels Mobile Repair** (Be Safe Travels LLC), Port Monmouth / Middletown, NJ. Owner: Feather. Built 2026-10-05 as a **preview** (to-do 19 in `CassSuczeck/calculator` → `PROJECT-STATUS.md`) to compare against the live Squarespace site before the Squarespace plan renews on **Aug 10, 2027**.

## Status
- **Preview only.** The live site is still Squarespace. Every page has `<meta name="robots" content="noindex, nofollow">` (`PREVIEW = True` in `build.py`), `robots.txt` disallows everything, and a yellow "Preview" banner sits in the header. At launch: set `PREVIEW = False`, rewrite `robots.txt`, remove the banner. Pages built with `noindex=True` (Warranty) keep their noindex.
- Planned address: `preview.besafetravels.com` (GitHub Pages + a `CNAME` DNS record in Squarespace Domains, like `tools`).
- Forms (contact form; the two "I agree" forms on `/terms-and-conditions/`) post through one helper (`FORMS_JS` in `build.py`) to the **website form receiver** (Apps Script, code in `CassSuczeck/calculator` → `apps-script/website-receiver.gs`, deploy steps `docs/website-forms-deploy.md`): bot trap + fill time + rate limit, no secrets in this repo. **Deployed 2026-10-24** (v1.0, Sheet "Safe Travels — Website Forms", permissions pinned to that sheet + send mail); `FORMS_ENDPOINT` holds its `/exec` URL. The URL is public in the page source by design: the receiver's bot checks, rate limit and validation are the protection. If `FORMS_ENDPOINT` is ever emptied, the forms fall back to "please call".

## Layout
```
_tools/build.py          page generator: all page text, header, footer and nav live here
index.html               Home
services/ calculator/ reviews/ appointments/ contact/ about/ faq/ cars-we-work-on/ our-tools/   one index.html each
mobile-mechanic-<town>-nj/  one page per town in Home's "Where we work" list (TOWNS + TOWN_PAGES in build.py)
privacy-policy/                 privacy policy, incl. calls and texts (draft, from the 2026-10-13 compliance check)
warranty/  terms-and-conditions/   word for word from the live Squarespace pages; Warranty is noindex for good
promotions/                     DRAFT (2026-10-24), not linked yet
404.html  robots.txt
assets/site.css          all styles (brand tokens at the top)
assets/logo.png|webp, favicon.png, apple-touch-icon.png, service-area-map.jpg, feather.jpg + feather-480|800.webp (About photo)
```
URLs match the Squarespace site so links and rankings survive a switch.

## How to change a page
1. Edit the text in `_tools/build.py` (header, footer and nav are defined once there).
2. Run `python3 _tools/build.py` from the repo root. It rewrites every page.
3. Check in a browser (local: `python3 -m http.server` in the repo root), commit the regenerated HTML.
No other build step; GitHub Pages serves the files as they are.

## Needs Feather's review before launch
- **Town page intros** (`TOWN_PAGES` in `build.py`, 40 towns, matched to the 2026-10-24 "New Service Area" map): each has one or two lines of local fact (borders, neighborhoods, rivers). Confirm each is right and that she wants to be listed there. Towns marked "edge of our service area" (Belmar, Wall, Manalapan, Englishtown, Freehold, North Brunswick, New Brunswick) say a $1/mile round-trip charge may apply beyond 30 minutes; check which towns are really beyond 30 minutes.
- **Cars we work on** (`/cars-we-work-on/`): make list copied from the calculator's `BRAND_TIER`/`DOMESTIC_MAKES` (Tools repo). Keep the two in sync.
- **Our Tools** (`/our-tools/`): tool and factory-software brands from the calculator repo's `docs/brands-page-draft.md` (to-do 16). Names only: logos need each brand's written OK.
- **Warranty and Terms** (`/warranty/`, `/terms-and-conditions/`, linked in every footer; Home's trust line links `/warranty/`): **follow the live Squarespace pages word for word** (Feather, 2026-10-24; source: Chrome capture "live-warranty-terms-text-2026-10-24" in Drive). Text lives in `WEBSITE_TERMS`/`SERVICE_TERMS`/`NOTICE` and the `/warranty/` page in `build.py`; when the live pages change, update them and `TERMS_VERSION_ID`. **Legal freeze (Feather, 2026-10-24): an attorney is reviewing the whole Squarespace site; no changes to the Terms (or other legal pages) until the attorney is done.** The Terms are attorney-built to limit liability; the Warranty page is Feather's own (written with Claude, not attorney-reviewed), deliberately more generous (e.g. free return visit within ~30 minutes vs. the Terms' "at customer's expense"); raise that difference with the attorney. Both live "I agree" forms are on the preview (same fields, checkbox text and "I agree" button). Warranty stays `noindex` after launch.
- **Promotions** (`/promotions/`, draft 2026-10-24, to-do 14): standing prices and policies only (consolidated visit, winter readiness review = multipoint inspection $99.99, pre-purchase inspection $59.99, free phone consult), so no end dates. Tone: calm, specific, no "deals"/countdowns. Not linked anywhere until Feather approves; a dated offer must state its dates and terms on the page. **Community offers** (Feather, 2026-10-24; `PROMO_END` = Nov 24, 2026): 50% off for Memorial Sloan Kettering (MSK) patients, 10% off for Friendly Dental and for Joint Physical Therapy patients; each includes caregivers and family members. Discounts come off the service visit's final price before tax (parts and labor; inspection or repair). Honor-based: no coupon, code or proof, ever; honored however people heard of it. Never record a customer's health or provider on an invoice; label it "Community offer". Not affiliated with any of the three (disclaimer on the page); never give the offices or their staff anything for referrals. The "subject to change without notice" line is only a shield for pulling the offers early. Remove or update the section after `PROMO_END`.
- Adding a town: add it to both `TOWNS` and `TOWN_PAGES` (the home list links every town to its page).
- **Privacy policy** (`/privacy-policy/`): follows the live Squarespace policy (2026-10-24), changed only where the new site differs: GitHub hosting, Google Fonts, Calendly embed, no cookies of its own, no statistics, no reCAPTCHA, no Weglot, forms to our Google Sheet. If launch adds analytics, a language menu or another service that handles customer data, update "What's collected automatically" and "Who else handles it". The freeze covers the live pages; the preview's legal pages should go to the attorney before launch.

## Compliance (check of Oct 13, 2026)
- Contact form and calculator form both carry the call/text consent line ("Reply STOP to opt out"). The calculator line has no links yet: add a link to `/privacy-policy/` once the new site is live.
- Every page footer links to `/privacy-policy/`. Mileage is stated as $1 per mile, round trip, from Port Monmouth wherever it is mentioned.
- Estimates: Feather's T&C ("BST T&C 07.30.2026", Drive) cites N.J.A.C. 13:45A-26C.2 and prints the required customer notice. She always gives a written estimate (never uses the waiver). Odometer photo and repair description are recorded at the car in her shop management software (uploaded to Carfax).
- Review sources: C.W., D.P. on Nextdoor; C.H., E.C. on Google; the dash cam review is by Feather's spouse, so its attribution says so (FTC endorsement rule: disclose family ties). Keep a screenshot of each.

## Rules (same as the calculator repo)
- **Security first** (Feather, 2026-10-24): always consider cybersecurity when writing code, especially anything open to input from the public (forms, receivers, URLs, uploads). Validate on the server, cap lengths, neutralize spreadsheet formulas, rate-limit, never trust the browser, keep secrets out of public repos, and ask only for the **narrowest permissions** (pin Apps Script scopes in `appsscript.json`; never name the full-mailbox Gmail service in code or comments, because Apps Script guesses scopes from the text). Check what a consent screen will show before Feather runs it.
- **Don't commit or push before Feather approves.** A push to `main` goes live on GitHub Pages in about 2 minutes.
- Public repo: **never commit secrets**.
- Marketing copy: never disparage competitors, dealers or DIY/backyard mechanics; no fear-based (FUD) copy. Customer reviews are quoted word for word.
- NJ: the calculator is a ballpark; a written estimate comes before any work. Diagnostic fees credit toward the repair.
- Accessibility: one H1 per page, WCAG 2.2 AA contrast (brand pairs in `site.css` pass), visible focus ring, labeled form fields, 16px+ inputs.
- Brand: Navy #070453, Sky Blue #5E85EE, Blue Gray #CEDAF4, Coral #F8826C, White #FCFCFC; Montserrat headings, Inter body.

## Facts the pages rely on
Phone (908) 986-3415 (`tel:+19089863415`, texts `sms:+19089863415`) · info@besafetravels.com · calls 7am–8pm, visits 8:30am–5pm Mon–Sat · labor $159.99/hr, 1-hour minimum · free phone consultation · small jobs $25 trip fee + parts + $1/mile round trip from Port Monmouth, waived when bundled to the 1-hour minimum · oil change from $80 plus parts (driveway only sometimes) · EVs: only hitch/accessory installs and some brake, suspension and interior work · model year 1996+ only · fully insured (businessowner's and garagekeepers through biBERK, commercial auto through GEICO; Feather 2026-10-22; the site says "Fully insured" only) · **no ASE certifications** (Feather, 2026-10-22: don't claim ASE or "certified" anywhere, and don't ask again) · "Licensed" not used on the site unless Feather names the license · booking: Calendly `besafetravelsllc/consultation` · calculator: https://tools.besafetravels.com/calculator/
