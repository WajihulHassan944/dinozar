# dinozar.wtf – content analysis & migration notes

Source: https://dinozar.wtf/ ("Dinozar – Adventures", WordPress, `en-GB`).
Goal: replace it with the new Dex World site (this folder). This document records what exists today, what the new site reproduces, and what still needs real content.

## 1. What the current site is

| Aspect | Finding |
|---|---|
| Platform | WordPress (`wp-content`, `?page_id=`), Revolution Slider hero, lazy-loaded images, RSS feed at `/feed/`, oEmbed enabled |
| Purpose | Personal portfolio + travel / sustainability blog of **Deniz Onaral** (Austria-based, Turkish roots) |
| Language | English with German posts mixed in (several posts exist in both languages) |
| Tone | Personal, curious, a little rebellious ("Think outside the box…" – Banksy) |
| Copyright line | "© Copyright 2023. All Rights Reserved // Web Design by Marketing Originals." |
| Tagline (Stories page) | "I give it a try there you go my adventures and observations of this 'crazy' world." |
| Social | LinkedIn `deniz-onaral-39b955b6`, Instagram `d.xaral` |
| Contact | Form only; the only address in the whole site is in the privacy policy (`denizonaral@gmail.com`) |

## 2. Sitemap (current → new)

| Current URL | Current content | New page |
|---|---|---|
| `/` | Revolution-Slider hero "DEX WORLD · Dream. Explore. Xperate. · DISCOVER"; bio teaser "DENIZ"; "Read more about me"; "* * *" divider with ship image; social links | `index.html` (matches the supplied design comp) |
| `/about-me/` | Bio, EN + DE: grew up on Turkey's south coast (parents in hotel management), top Austrian hospitality school, in Austria since end of 2011, extracurricular projects, 2015 NANO research camp (Baltic Sea), 2016 Rio Olympics internship won via Ö3 radio; DE section adds school and school-ball marketing details | `about.html` (+ `journey.html` timeline) |
| `/press/` | Three groups – **Olympia**, **AHET**, **Royal** – each a list of external press links; plus APA-OTS, Austrian Economics Center, Hayek Institut, KTS Villach items | `press.html` |
| `/?page_id=4838` (Wiki) | **404 at time of analysis** – content unknown | `wiki.html` (starter entries, searchable) |
| `/tips-tricks/` | Ten tips, headings only | `tips.html` |
| `/blog/` (Stories) | 5 pages of posts, sidebar with search, recent posts, `#Olympics` tag, categories dropdown | `stories.html` + `post.html` template |
| `/category/allgemein/` `…/sustain-able-issues/` `…/travel/` | Category archives (Travel = 3 pages) | filter chips on `stories.html` (`stories.html#Travel`, etc.) |
| `/contact/` | "Thank you for visiting my site! Want to chat? Ask a question?…"; fields: name*, email*, subject, message; privacy consent*; optional updates consent; LinkedIn / Instagram | `contact.html` |
| `/privacy-policy/` | Generic policy, 7 sections, last updated 20 Nov 2018 | `privacy.html` |
| (design comp nav) | Home · About · Journey · Gallery · Contact | `journey.html`, `gallery.html` added to satisfy the comp |

## 3. Content inventory

### Posts (16 unique, newest first)
Allgemein = general. Dates as shown on the site (the Rio diary was imported with one date).

1. QUANTUM: ? + ? =? – 8 May 2019 – Allgemein, Travel – **password protected**
2. KAOSPILOT APPLICATION – 18 Mar 2019 – Allgemein, Sustain(-able) issues
3. Über meine Reise mit dem Zug nach Katowice – 9 Dec 2018 – Sustain – DE
4. About my trip by train to Katowice COP24 – 9 Dec 2018 – Allgemein, Sustain – EN
5. Olympic Games 2016 – 21 Nov 2018 – Travel – DE – `#Olympics`
6. Are we going to bear energy scarcity with "energy diplomacy" or with innovation? – 10 Jul 2017 – Sustain – `SDG 9`
7. How can businesses in the energy industry contribute to producing 'clean' energy? … – 3 Jul 2017 – Sustain
8. There is an available whistle-blower internship in the catch 22, anyone interested? – 26 Jun 2017 – Sustain
9. Are there interlinkages between education, ethics, stakeholders waste dumping and product lifespan? – 19 Jun 2017 – Sustain
10. World-wide contrariness which add fuel to the fire of climate change. – 12 Jun 2017 – Sustain
11–18. Rio diary "Tag 16 … Tag 23" (3 Oct 2016, Allgemein + Travel, DE): Heimwerkerkönig Deniz und „Re Boo", Location, Dear weather…, Bronze für Österreich!, Mit den Sportlern kommen die Selfies, Ein Kamel am Morgen…, Mr. Orlando, Ausflug nach Niterói.

Pages 2–5 of the blog archive were not read (only page 1 + the Travel archive). The Rio diary likely continues from Tag 1; those posts are not yet in `js/data.js`.

### Themes worth carrying into the new brand
- Hospitality → design thinking → sustainability: a coherent "lateral thinker" story.
- Slow travel / climate (COP24 by train, SDG 9 essays).
- The Rio 2016 Olympics experience is the biggest "proof point" and has the most press.
- The name **Deniz = sea** is the central metaphor (the ship, the sea, "stormy and short-tempered").

### Press links (reusable as-is)
Kleine Zeitung ×4, MeinBezirk, Austria House, APA-OTS, Vi2day, KTS Villach ×2, Ball Royal (Facebook), KTS Royal, Austrian Economics Center, Hayek Institut. All are in `build.py` (`press` list).

## 4. Assets

| Asset | Where it lives on the old site | Used in the new site? |
|---|---|---|
| Logo (white, interlocking links) | `/wp-content/uploads/2018/11/Deniz-Logo-Weis.png` (2565×1355) | Yes – embedded in `css/logo.css` as a recolourable mask |
| Favicon | `Deniz-Logo-sq.png` | Yes – `images/favicon.png` |
| Hero portrait (B&W face) | `Dex-2.jpg` (5017×3345) | Yes – `images/portrait.jpg` on the About page |
| Ship photo | `ship.jpg` (3264×2448) | Yes – `images/ship.jpg` (gallery) |
| All other imagery | lazy-loaded placeholders; no real files exposed | Replaced with the design comp's crops and royalty-free stand-ins (`images/g-*.jpg`) |

The hero, journey card and band images come from the design comps you supplied; `g-*.jpg` are placeholders from Unsplash (free licence) – swap for owned photography before launch.

## 5. Gaps & risks

1. **Wiki page returned 404** – nothing to migrate; entries in `wiki.html` are explanatory starter text.
2. **Tips page has headings only** – descriptions on `tips.html` are draft copy.
3. **Article bodies not captured** – `post.html` is a template with the excerpt as the lead. A real migration should export from WordPress (Tools → Export, or the REST API at `/wp-json/wp/v2/posts`).
4. **Protected post** – `QUANTUM` needs a real password gate (the template only shows the UI).
5. **Contact form** has no back end. Wire `#cf` to a form service / API; it currently validates and shows a thank-you state only.
6. **Privacy policy** is a generic 2018 text; it mentions registration and accounts the site doesn't have, and the opt-out address is missing. Have it rewritten and legally reviewed (GDPR, cookie banner if analytics are added).
7. **Design comp vs reality** – the comp's skills grid (React, Next.js, AWS…) doesn't match Deniz's current content (hospitality, sustainability, design thinking). Kept for fidelity; consider replacing with real skills.
8. **Bilingual content** – posts are EN/DE. Decide: language switcher, separate `/de/` tree, or one language. The new site marks German posts with `lang="de"`.
9. **SEO** – old site has `og:*` tags, RSS feed and WordPress permalinks (`/kaospilot-application/`). Keep or 301-redirect old URLs, add a sitemap.xml and RSS if the blog stays important.
10. **Images** – the old hero is 5 MB; the new images are resized (≤ 1500 px) but not yet in WebP/AVIF.
11. **Third-party links** in Press are `http://` for several outlets and may be stale; run a link check before launch.
12. **Attribution** – footer still credits "Marketing Originals" as in the design comp.

## 6. Technical notes for the new build

- Pure static HTML/CSS/JS, generated by `python3 build.py` from the content in that file and `src/home-main.html`.
- Shared files: `css/site.css`, `css/pages.css`, `css/logo.css`, `js/site.js` (effects, Lenis smooth scroll, loader), `js/pages.js` (menu, filters, lightbox, forms), `js/data.js` (posts).
- Smooth scroll uses Lenis from jsDelivr; everything degrades gracefully without it. `prefers-reduced-motion` disables loader, parallax and tilt.
- Mobile-first checks: no horizontal scroll at 390 px on all 12 pages.
