# CLAUDE.md — Safe Travels website (CassSuczeck/website)

The coded version of besafetravels.com for **Safe Travels Mobile Repair** (Be Safe Travels LLC), Port Monmouth / Middletown, NJ. Owner: Feather. Built 2026-10-05 as a **preview** (to-do 19 in `CassSuczeck/calculator` → `PROJECT-STATUS.md`) to compare against the live Squarespace site before the Squarespace plan renews on **Aug 10, 2027**.

## Status
- **Preview only.** The live site is still Squarespace. Every page has `<meta name="robots" content="noindex, nofollow">`, `robots.txt` disallows everything, and a yellow "Preview" banner sits in the header. Remove all three at launch.
- Planned address: `preview.besafetravels.com` (GitHub Pages + a `CNAME` DNS record in Squarespace Domains, like `tools`).
- Contact form is **not connected** (`ENDPOINT = ''` in `/contact/`): it validates and then asks people to call. At launch it posts to an Apps Script lead receiver, same pattern as the calculator (bot trap + fill time, no secrets in this repo).

## Layout
```
_tools/build.py          page generator: all page text, header, footer and nav live here
index.html               Home
services/ calculator/ reviews/ appointments/ contact/ about/ faq/ brands/   one index.html each
mobile-mechanic-<town>-nj/  one page per town in Home's "Where we work" list (TOWNS + TOWN_PAGES in build.py)
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
- **Town page intros** (`TOWN_PAGES` in `build.py`, 24 towns): each has one or two lines of local fact (borders, neighborhoods, rivers). Confirm each is right and that she wants to be listed there. Towns marked "edge of our service area" (Asbury Park, Wall, Perth Amboy, Woodbridge) say a $1/mile round-trip charge may apply beyond 30 minutes; check which towns are really beyond 30 minutes.
- **Brands page** (`/brands/`): make list copied from the calculator's `BRAND_TIER`/`DOMESTIC_MAKES` (Tools repo). Keep the two in sync.
- Adding a town: add it to both `TOWNS` and `TOWN_PAGES` (the home list links every town to its page).

## Rules (same as the calculator repo)
- **Don't commit or push before Feather approves.** A push to `main` goes live on GitHub Pages in about 2 minutes.
- Public repo: **never commit secrets**.
- Marketing copy: never disparage competitors, dealers or DIY/backyard mechanics; no fear-based (FUD) copy. Customer reviews are quoted word for word.
- NJ: the calculator is a ballpark; a written estimate comes before any work. Diagnostic fees credit toward the repair.
- Accessibility: one H1 per page, WCAG 2.2 AA contrast (brand pairs in `site.css` pass), visible focus ring, labeled form fields, 16px+ inputs.
- Brand: Navy #070453, Sky Blue #5E85EE, Blue Gray #CEDAF4, Coral #F8826C, White #FCFCFC; Montserrat headings, Inter body.

## Facts the pages rely on
Phone (908) 986-3415 (`tel:+19089863415`, texts `sms:+19089863415`) · info@besafetravels.com · calls 7am–8pm, visits 8:30am–5pm Mon–Sat · labor $159.99/hr, 1-hour minimum · free phone consultation · small jobs $25 trip fee + parts + $1/mile round trip from Port Monmouth, waived when bundled to the 1-hour minimum · oil change from $80 plus parts (driveway only sometimes) · EVs: only hitch/accessory installs and some brake, suspension and interior work · model year 1996+ only · booking: Calendly `besafetravelsllc/consultation` · calculator: https://tools.besafetravels.com/calculator/
