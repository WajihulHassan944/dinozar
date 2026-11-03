# Dinozar / Dex World

Static, multi-page site (HTML/CSS/JS, no build step needed to view).

- Open `index.html`, or serve the folder: `python3 -m http.server`
- Pages: `index, about, journey, gallery, press, wiki, tips, stories, post, contact, privacy, 404`
- Shared files: `css/`, `js/`, `images/`
  - `css/theme.css`: homepage design (glows, copper arcs) + shared header, quote, skills, connect band, buttons, footer
  - `css/premium.css`: inner pages (`body.inner`): photo page heroes, ambient glow, glass cards
- Content lives in `build.py` (+ `src/home-main.html`, `js/data.js`); regenerate pages with `python3 build.py`
- Content analysis of the previous site and migration gaps: [CONTENT-ANALYSIS.md](CONTENT-ANALYSIS.md)
