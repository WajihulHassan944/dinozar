# Dinozar / Dex World

Static, multi-page site (HTML/CSS/JS, no build step needed to view).

- Open `index.html`, or serve the folder: `python3 -m http.server`
- Pages: `index, about, journey, gallery, press, wiki, tips, stories, post, contact, privacy, 404`
- Shared files: `css/`, `js/`, `images/`
  - `css/theme.css`: homepage design (glows, copper arcs) + shared header, quote, skills, connect band, buttons, footer
  - `css/premium.css`: inner pages (`body.inner`): photo page heroes, ambient glow, glass cards
- Content lives in `build.py` (+ `src/home-main.html`, `js/data.js`); regenerate pages with `python3 build.py`
- Content analysis of the previous site and migration gaps: [CONTENT-ANALYSIS.md](CONTENT-ANALYSIS.md)

## SEO & social preview (homepage)

- Head tags, Open Graph / Twitter card and JSON-LD are generated from `HOME_TITLE`, `HOME_DESC`, `OG_*` and `SITE_URL` in `build.py`.
- Share image: `images/og-home.jpg` (1200x630, ~70 KB). Social apps need absolute URLs, so set `SITE_URL` to the live domain before publishing.
- `robots.txt` and `sitemap.xml` use `https://dinozar.vercel.app`.
