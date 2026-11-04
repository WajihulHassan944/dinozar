#!/usr/bin/env python3
"""Static site generator for the Dex World site.

Run:  python3 build.py
Reads src/home-main.html and the page bodies below, writes every *.html file
next to this script. Shared CSS / JS / images live in css/, js/, images/.
Replace the copy in this file (or move it to your CMS) when real content lands.
"""
import re, pathlib

ROOT = pathlib.Path(__file__).parent
LINKEDIN = "https://www.linkedin.com/in/deniz-onaral-39b955b6"
INSTAGRAM = "https://www.instagram.com/d.xaral/"
EMAIL = "denizonaral@gmail.com"

NAV = [("Home", "index.html"), ("About", "about.html"), ("Journey", "journey.html"),
       ("Gallery", "gallery.html"), ("Contact", "contact.html")]

MENU = [("Home", "index.html", None), ("About Me", "about.html", None), ("Journey", "journey.html", None),
        ("Gallery", "gallery.html", None), ("Press", "press.html", None), ("Wiki", "wiki.html", None),
        ("Tips &amp; Tricks", "tips.html", None),
        ("Stories", "stories.html", [("Allgemein", "stories.html#Allgemein"),
                                     ("Sustain(-able) issues", "stories.html#Sustain(-able) issues"),
                                     ("Travel", "stories.html#Travel")]),
        ("Contact", "contact.html", None), ("Privacy Policy", "privacy.html", None)]

ARROW = '<svg><use href="#arrow"/></svg>'


def nav_html(active):
    items = "".join('<li><a%s href="%s">%s</a></li>' % (' class="on"' if f == active else "", f, n) for n, f in NAV)
    return ('<header><div class="wrap nav">'
            '<a class="logo" href="index.html" aria-label="Dex World home" style="color:var(--fg)"><span class="logo-mark"></span></a>'
            '<nav aria-label="Primary"><ul>%s</ul></nav>'
            '<button class="menu" aria-label="Menu" aria-expanded="false" aria-controls="mo"><i></i><i></i><i></i></button>'
            '</div></header>' % items)


def overlay_html():
    lis = []
    for i, (n, f, subs) in enumerate(MENU):
        sub = ""
        if subs:
            sub = '<ul class="mo-sub">%s</ul>' % "".join('<li><a href="%s">%s</a></li>' % (h, t) for t, h in subs)
        lis.append('<li style="--i:%d"><a href="%s">%s</a>%s</li>' % (i, f, n, sub))
    return ('<div id="mo" aria-hidden="true"><div class="wrap mo-in">'
            '<nav aria-label="Full menu"><ol class="mo-list">%s</ol></nav>'
            '<aside class="mo-side">'
            '<div><h4>Say hello</h4><p>Want to chat? Ask a question?<br><a href="contact.html">Send a message &rarr;</a></p></div>'
            '<div><h4>Follow</h4><div class="mo-social"><a href="%s" target="_blank" rel="noopener">LinkedIn</a><a href="%s" target="_blank" rel="noopener">Instagram</a></div></div>'
            '<div><h4>Dex World</h4><p>Dream. Explore. Xperate.<br>A journey beyond limits.</p></div>'
            '</aside></div></div>' % ("".join(lis), LINKEDIN, INSTAGRAM)).replace("<ol", "<ol", 1)


def footer_html(privacy=True):
    return ('<footer><div class="wrap"><div class="f-left">'
            '<a href="index.html" aria-label="Back home" style="color:var(--fg)"><span class="logo-mark sm"></span></a>'
            '<small>&copy; 2023. All Rights Reserved. / Web Design by Marketing Originals.</small></div>'
            '<div class="f-right"><a href="%s" target="_blank" rel="noopener">LinkedIn</a>'
            '<a href="%s" target="_blank" rel="noopener">Instagram</a>%s</div></div></footer>' % (LINKEDIN, INSTAGRAM, '<a href="privacy.html">Privacy</a>' if privacy else ''))


def connect_html(title="Have a project in mind?", text="Let&rsquo;s turn your ideas into something extraordinary.",
                 btn="Get in Touch", href="contact.html", img="g-peaks.jpg", eyebrow="Let&rsquo;s connect"):
    return ('<section class="connect"><img class="m" src="images/%s" alt="" aria-hidden="true"><div class="c reveal">'
            '<div class="eyebrow" style="color:var(--fg)">%s</div><h2>%s</h2><p>%s</p>'
            '<a class="btn" href="%s">%s <svg><use href="#arrow"/></svg></a></div></section>' % (img, eyebrow, title, text, href, btn))


def page(fname, title, body, active=None, desc="", loader=False, data=False, css="css/premium.css", body_class="inner", privacy=True):
    loading = '"js","loading"' if loader else '"js"'
    loader_html = ('<div id="loader" aria-hidden="true"><span class="logo-mark"></span><div class="bar"></div><small>Dex World</small></div>'
                   if loader else "")
    scripts = ('<script src="js/data.js"></script>' if data else "") + '<script src="js/site.js"></script><script src="js/pages.js"></script>'
    html = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>%s</title>\n<meta name="description" content="%s">\n<meta name="theme-color" content="#0a0a0a">\n'
            '<link rel="icon" href="images/favicon.png">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Lato:ital,wght@0,300;0,400;0,700;1,300;1,400&display=swap">\n'
            '<link rel="stylesheet" href="css/logo.css"><link rel="stylesheet" href="css/site.css"><link rel="stylesheet" href="css/pages.css"><link rel="stylesheet" href="css/theme.css">%s\n'
            '</head>\n<body%s>\n<script>document.documentElement.classList.add(%s)</script>\n%s\n'
            '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
            '<symbol id="arrow" viewBox="0 0 14 10"><path d="M0 5h12M8 1l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1"/></symbol></defs></svg>\n'
            '%s\n%s\n<main>\n%s\n</main>\n%s\n%s\n</body>\n</html>\n'
            % (title, desc or "Dex World – Dream. Explore. Xperate. A journey beyond limits.",
               ('<link rel="stylesheet" href="%s">' % css) if css else "", (' class="%s"' % body_class) if body_class else "",
               loading, loader_html, nav_html(active), overlay_html(), body, footer_html(privacy), scripts))
    (ROOT / fname).write_text(html, encoding="utf-8")
    print("wrote", fname, len(html) // 1024, "KB")


PHERO_IMG = {"About": "portrait.jpg", "Journey": "ship.jpg", "Gallery": "g-clouds.jpg", "Press": "g-harbor.jpg",
             "Wiki": "g-fog.jpg", "Tips & Tricks": "g-sunset.jpg", "Stories": "g-mist.jpg", "Contact": "g-tanker.jpg",
             "Privacy Policy": "g-peaks.jpg"}


def phero(eyebrow, title, lead, crumb, img=None, actions=""):
    img = img or PHERO_IMG.get(crumb)
    pimg = '<div class="pimg" style="background-image:url(images/%s)" aria-hidden="true"></div>' % img if img else ""
    pimg += '<span class="ph-arc" aria-hidden="true"></span><span class="ph-bloom" aria-hidden="true"></span>'
    return ('<section class="phero">%s<div class="wrap"><p class="crumbs"><a href="index.html">Home</a><i></i><span>%s</span></p>'
            '<div class="eyebrow" style="margin-bottom:22px">%s</div><h1>%s</h1><p class="lead">%s</p>%s</div></section>'
            % (pimg, crumb, eyebrow, title, lead, ('<div class="phero-actions">%s</div>' % actions) if actions else ""))


# ---------------------------------------------------------------- HOME
home = (ROOT / "src/home-main.html").read_text(encoding="utf-8")
home = (home.replace('href="#journey"><span class="c">', 'href="journey.html"><span class="c">')
            .replace('<a class="btn" href="#journey">Discover More', '<a class="btn" href="about.html">Discover More')
            .replace('href="#expertise">Explore Skills', 'href="about.html#expertise">Explore Skills')
            .replace('href="#gallery">View Gallery', 'href="gallery.html">View Gallery')
            .replace('href="#contact">Get in Touch', 'href="contact.html">Get in Touch'))
home = re.sub(r'<section class="connect" id="contact">', '<section class="connect" id="contact">', home)
page("index.html", "Dex World", home, active="index.html", loader=True, css=None, body_class="home", privacy=False,
     desc="Dex World – Dream. Explore. Xperate. A journey beyond limits.")

# expertise block reused on the About page
m = re.search(r'<section class="expertise" id="expertise">.*?</section>', home, re.S)
expertise = m.group(0) if m else ""
expertise = expertise.replace('<a class="btn" href="about.html#expertise">Explore Skills <svg><use href="#arrow"/></svg></a>',
                              '<a class="btn" href="contact.html">Work with me <svg><use href="#arrow"/></svg></a>')

# ---------------------------------------------------------------- ABOUT
facts = ('<div class="facts reveal"><div class="fact"><b>5+</b><small>Years of experience</small></div>'
         '<div class="fact"><b>50+</b><small>Projects completed</small></div>'
         '<div class="fact"><b>100%</b><small>Passion</small></div>'
         '<div class="fact"><b>2011</b><small>Based in Austria since</small></div></div>')

about_tl = [
    ("Early years", "Turkey&rsquo;s south coast", "Grew up where the Mediterranean meets Anatolia, with parents working in hotel management. Hospitality was the family business and the first classroom."),
    ("2011", "A new home in Austria", "Moved to Austria at the end of 2011 and began training at one of the country&rsquo;s top hospitality schools."),
    ("2015", "Gold &amp; bronze at the AEHT", "Part of the school delegation that returned from the European tourism-school championships with medals &mdash; and organised a string of extracurricular projects along the way."),
    ("2015", "NANO research camp", "Joined a research camp on the Baltic Sea, which later led to a meeting with the Federal President in Vienna."),
    ("2016", "Rio 2016 Olympic internship", "Won an internship at the Summer Olympics after a radio call-out on Austrian station &Ouml;3 &mdash; a summer of long days in Rio de Janeiro."),
    ("2018&ndash;19", "Climate, trains &amp; Kaospilot", "Travelled by train to the COP24 climate conference in Katowice and applied to Kaospilot in Aarhus to keep learning how to change things.")]
tl_items = "".join('<div class="tl-item reveal"><div class="tl-card"><div class="tx"><span class="tl-year">%s</span><h3>%s</h3><p>%s</p></div></div></div>' % t for t in about_tl)

about_body = (phero("About me", "Deniz", "A lateral thinker with affinity to design thinking &mdash; whose name, Deniz, means <em style=\"font-style:normal;color:var(--copper)\">sea</em> in Turkish.",
                    "About", img="portrait.jpg", actions='<a class="btn" href="contact.html">Get in touch <svg><use href="#arrow"/></svg></a><a class="btn" href="journey.html">See my journey <svg><use href="#arrow"/></svg></a>')
              + '<section class="sec"><div class="wrap grid2"><div class="sticky reveal"><div class="eyebrow">The story</div>'
              '<h2 style="font-size:clamp(34px,4.4vw,56px);line-height:1.06;margin:20px 0 0">Stormy, short-tempered &mdash; as the sea.</h2></div>'
              '<div class="prose reveal"><p class="big">Deniz is a lateral thinker with affinity to design thinking, and his name &mdash; the translation means sea &mdash; makes all honor.</p>'
              '<p>He is constantly on the move and looking for new challenges, sometimes stormy and short-tempered, as the sea. He grew up on the south coast of Turkey, where his parents worked in hotel management, and discovered early on that he loves the hospitality business.</p>'
              '<p>He graduated from a top hospitality school in Austria, where he has lived since the end of 2011. Between lessons he organised extracurricular projects, joined a research camp on the Baltic Sea in 2015 and won an internship at the 2016 Summer Olympics in Rio de Janeiro.</p>'
              '<p>Today the curiosity stays the same: always chasing new challenges, exploring the unknown and pushing boundaries &mdash; with design thinking as the compass.</p></div></div></section>'
              '<section class="sec"><div class="wrap">' + facts + '</div></section>'
              '<section class="sec"><div class="wrap"><div class="sec-head reveal"><div class="eyebrow">Milestones</div><h2>The road so far</h2>'
              '<p>A few of the stops that shaped the way of thinking.</p></div><div class="tl compact">' + tl_items + '</div></div></section>'
              + expertise + connect_html("Have a project in mind?"))
page("about.html", "About – Dex World", about_body, active="about.html",
     desc="About Deniz – a lateral thinker with affinity to design thinking.")

# ---------------------------------------------------------------- JOURNEY
jr = [
    ("Early years", "Where it began", "Turkey&rsquo;s south coast &mdash; family, hotels and the sea that gave him his name.", "g-harbor.jpg", "Turkey"),
    ("2011", "Austria", "A new country, a new language and a hospitality school in the mountains.", "g-peaks.jpg", "Home base"),
    ("2015", "Medals &amp; the Hofburg", "Gold and bronze at the European tourism-school championships and a reception hosted by the Federal President.", "g-summit.jpg", "AEHT"),
    ("2015", "Baltic Sea research camp", "Ten days of science, sea air and big questions on the NANO research camp.", "g-tanker.jpg", "NANO"),
    ("2016", "Rio de Janeiro", "A radio call-out, a dream internship and a summer at the Olympic Games &mdash; documented day by day in the travel diary.", "g-sunset.jpg", "Olympics"),
    ("2018", "Katowice by train", "Choosing the slow way to the COP24 climate conference: fewer emissions, more stories.", "g-clouds.jpg", "COP24"),
    ("2019", "Aarhus calling", "An application to Kaospilot &mdash; because design, change-making and a little chaos belong together.", "g-mist.jpg", "Kaospilot")]
jr_items = "".join('<div class="tl-item reveal"><div class="tl-card"><div class="ph"><img loading="lazy" src="images/%s" alt=""></div>'
                   '<div class="tx"><span class="tl-year">%s</span><h3>%s</h3><p>%s</p><span class="tl-tag">%s</span></div></div></div>' % (i, y, t, d, tag)
                   for (y, t, d, i, tag) in jr)
journey_body = (phero("My journey", "Exploring the world <em>through my lens</em>", "From breathtaking landscapes to captivating moments &mdash; photography has always been my escape and inspiration. Follow the route, chapter by chapter.",
                      "Journey", actions='<a class="btn" href="gallery.html">View gallery <svg><use href="#arrow"/></svg></a><a class="btn" href="stories.html">Read the stories <svg><use href="#arrow"/></svg></a>')
                + '<section class="sec"><div class="wrap"><div class="tl">' + jr_items + '</div></div></section>'
                + connect_html("Where to next?", "Every journey starts with a conversation.", "Plan something together", "contact.html", "quote.jpg", "Next chapter"))
page("journey.html", "Journey – Dex World", journey_body, active="journey.html", desc="The route so far: Turkey, Austria, the Baltic Sea, Rio 2016, Katowice and beyond.")

# ---------------------------------------------------------------- GALLERY
gallery = [
    ("ship.jpg", "The Deck", "Sea", "Sea"), ("g-sunset.jpg", "Last Light", "Landscapes", "Landscapes"),
    ("g-peaks.jpg", "Above the Weather", "Landscapes", "Landscapes"), ("g-tanker.jpg", "Golden Hour at Sea", "Sea", "Sea"),
    ("portrait.jpg", "Deniz", "People", "People"), ("g-clouds.jpg", "Sea of Clouds", "Landscapes", "Landscapes"),
    ("g-harbor.jpg", "Harbour Evening", "Sea", "Sea"), ("g-summit.jpg", "The Summit", "People", "People"),
    ("g-fog.jpg", "Fog Valley", "Landscapes", "Landscapes"), ("journey.jpg", "Red Deck, Last Light", "Sea", "Sea"),
    ("g-mist.jpg", "Edge of Mist", "People", "People")]
gal_items = "".join('<button class="g reveal" data-cat="%s" aria-label="Open %s"><img loading="lazy" src="images/%s" alt="%s"><figcaption><b>%s</b><small>%s</small></figcaption></button>'
                    % (c, t, f, t, t, s) for (f, t, s, c) in gallery)
gallery_body = (phero("Gallery", "Through <em>my lens</em>", "Landscapes, seascapes and people &mdash; captured on the road. Hover to bring back the colour, click to open.", "Gallery")
                + '<section class="sec"><div class="wrap"><div class="chips" style="margin:0 0 40px">'
                '<button class="chip on" data-gcat="all">All</button><button class="chip" data-gcat="Landscapes">Landscapes</button>'
                '<button class="chip" data-gcat="Sea">Sea</button><button class="chip" data-gcat="People">People</button></div>'
                '<div class="gal">' + gal_items + '</div></div></section>'
                + '<div id="lb" aria-hidden="true" role="dialog" aria-label="Photo viewer"><button class="x" aria-label="Close">&times;</button>'
                '<button class="pv" aria-label="Previous">&larr;</button><button class="nx" aria-label="Next">&rarr;</button>'
                '<figure><img alt=""><figcaption><b></b><small></small></figcaption></figure></div>'
                + connect_html("Like what you see?", "Let&rsquo;s tell the next story together.", "Get in Touch"))
page("gallery.html", "Gallery – Dex World", gallery_body, active="gallery.html", desc="Photo gallery: landscapes, seascapes and people.")

# ---------------------------------------------------------------- PRESS
press = [
    ("Olympia", "Rio 2016", "Austrian media followed the summer a Carinthian student spent as an intern at the Olympic Games.", [
        ("Kleine Zeitung", "Sommerspiele Rio: Deniz Onaral ist der olympische Ferialpraktikant", "http://www.kleinezeitung.at/kaernten/villach/4999219/Sommerspiele-Rio_Deniz-Onaral-ist-der-olympische-Ferialpraktikant"),
        ("MeinBezirk", "Drautaler schnappt sich Super-Ferialjob bei den Olympischen Spielen in Rio", "http://www.meinbezirk.at/villach/lokales/drautaler-schnappt-sich-super-ferialjob-bei-den-olympischen-spielen-in-rio-d1762500.html"),
        ("Kleine Zeitung", "Leute: Gold für ein unvergessliches Abenteuer in Rio", "http://www.kleinezeitung.at/kaernten/villach/aktuelles_villach/5074411/Leute_Gold-fur-ein-unvergessliches-Abenteuer-in-Rio"),
        ("Austria House", "Austria House press page", "http://www.austria-house.at/main.asp?VID=1&kat1=87&kat2=644&NID=685"),
        ("APA-OTS", "Karl Stoss am 31. Juli zu Gast in Ö3-Frühstück bei mir", "http://www.ots.at/presseaussendung/OTS_20160729_OTS0051/karl-stoss-am-31-juli-zu-gast-in-oe3-fruehstueck-bei-mir")]),
    ("AEHT", "European championships", "Medals at the European tourism-school championships and the trip across the Baltic Sea.", [
        ("Kleine Zeitung", "Europameisterschaften: Gold und Bronze für Tourismusschulen", "http://www.kleinezeitung.at/kaernten/villach/peak_villach/4852097/Europameisterschaften_Gold-und-Bronze-fur-Tourismusschulen"),
        ("Vi2day", "AEHT 2015 report", "http://www.vi2day.at/blog/item/14548-2015-10-25-17-16-33"),
        ("Kleine Zeitung", "Villacher Köpfe: Über die Ostsee zum Treffen mit dem Bundespräsidenten", "http://www.kleinezeitung.at/kaernten/villach/peak_villach/4813069/Villacher-Kopfe_Ueber-die-Ostsee-zum-Treffen-mit-dem"),
        ("KTS Villach", "Kulturtage in Wien und Schülerempfang in der Hofburg", "http://www.kts-villach.at/news-reader/kulturtage-in-wien-und-schuelerempfang-in-der-hofburg-durch-den-bundespraesidenten-dr-heinz-fischer.html")]),
    ("Royal", "School &amp; community", "Projects and alumni life around the school ball and the KTS Royal community.", [
        ("Facebook", "Ball Royal", "https://www.facebook.com/Xballroyal/?fref=ts"),
        ("KTS Royal", "AlumniROYAL", "http://www.kts-royal.at/"),
        ("KTS Villach", "Weinlese: Hl. Urban sei Dank", "http://www.kts-villach.at/news-reader/hl-urban-sei-dank.html")]),
    ("More", "Events &amp; context", "Further mentions and event coverage.", [
        ("Austrian Economics Center", "Annual Gala: Peter Thiel awarded by the Austrian Economics Center", "http://www.austriancenter.com/2015/11/11/annual-gala-peter-thiel-awarded-by-the-austrian-economics-center/"),
        ("Hayek Institut", "Peter Thiel mit dem Hayek Lifetime Achievement Award ausgezeichnet", "http://www.hayek-institut.at/peter-thiel-mit-dem-hayek-lifetime-achievement-award-ausgezeichnet.html")])]
groups = ""
for (name, sub, desc, rows) in press:
    r = "".join('<a class="prow" href="%s" target="_blank" rel="noopener"><span class="o">%s</span><span class="t">%s</span><span class="a">&#8599;</span></a>' % (u, o, t) for (o, t, u) in rows)
    groups += ('<div class="pgroup reveal"><div><div class="eyebrow">%s</div><h2>%s</h2><p class="d">%s</p></div><div>%s</div></div>' % (sub, name, desc, r))
press_body = (phero("Press", "In the <em>news</em>", "Coverage of the Rio 2016 internship, the European championships and school projects &mdash; collected in one place.", "Press")
              + '<section class="sec"><div class="wrap"><div class="outlets reveal"><span>Kleine Zeitung</span><span>MeinBezirk</span><span>&Ouml;3</span><span>Vi2day</span><span>APA-OTS</span><span>Austria House</span><span>KTS Villach</span></div>'
              + groups + '</div></section>' + connect_html("Press or media enquiry?", "Happy to share stories, photos and quotes.", "Get in Touch"))
page("press.html", "Press – Dex World", press_body, desc="Press coverage and media mentions.")

# ---------------------------------------------------------------- WIKI
wiki = [
    ("A", "AEHT", "Education", "The Association of European Hotel and Tourism Schools &mdash; a network of schools that also runs European championships where students compete in hospitality and tourism disciplines."),
    ("C", "COP24", "Climate", "The 24th UN climate conference of the parties, held in Katowice, Poland, in December 2018. It produced the rulebook for putting the Paris Agreement into practice."),
    ("D", "Design thinking", "Method", "A human-centred, iterative way of solving problems: empathise with people, define the problem, ideate, prototype and test &mdash; then repeat."),
    ("K", "Kaospilot", "Education", "A school for creative leadership and social entrepreneurship in Aarhus, Denmark, mixing business, design and project-based learning."),
    ("L", "Lateral thinking", "Method", "Solving problems through indirect, creative approaches instead of step-by-step logic &mdash; a term popularised by Edward de Bono."),
    ("O", "&Ouml;3", "Media", "Austria&rsquo;s popular public radio station. A call-out on &Ouml;3 for dream summer jobs led to the 2016 Olympic internship in Rio."),
    ("R", "Rio 2016", "Travel", "The Games of the XXXI Olympiad, held in Rio de Janeiro in August 2016. The travel diary covers the weeks around them."),
    ("S", "SDGs", "Sustainability", "The UN Sustainable Development Goals. SDG 9 &mdash; industry, innovation and infrastructure &mdash; features in several stories."),
    ("S", "Slow travel", "Sustainability", "Choosing slower, lower-emission ways of getting there &mdash; like the train to Katowice &mdash; and treating the journey as part of the trip.")]
letters = ["All"] + sorted({w[0] for w in wiki})
chips = "".join('<button class="chip%s" data-chip="%s">%s</button>' % (" on" if l == "All" else "", l.lower() if l == "All" else l, l) for l in letters)
wk = "".join('<details class="wk" data-filter-item data-letter="%s"><summary><span class="l">%s</span><span class="tt">%s<small>%s</small></span><span class="pl"></span></summary><div class="bd">%s</div></details>'
             % (l, l, t, c, d) for (l, t, c, d) in wiki)
wiki_body = (phero("Wiki", "A little <em>knowledge base</em>", "Terms, places and ideas that keep coming up in the stories &mdash; explained in a few lines.", "Wiki")
             + '<section class="sec"><div class="wrap"><div class="search reveal"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>'
             '<input type="search" placeholder="Search the wiki&hellip;" aria-label="Search the wiki" data-filter-input></div>'
             '<div class="chips">' + chips + '</div><div class="wk-list">' + wk + '</div><p class="empty" hidden>Nothing found &mdash; try another term.</p>'
             '<p style="margin-top:46px;color:var(--muted);font-size:12.5px">Starter entries &mdash; replace with your own wiki content.</p></div></section>'
             + connect_html("Missing a term?", "Tell me what should be explained next.", "Suggest an entry"))
page("wiki.html", "Wiki – Dex World", wiki_body, desc="A small knowledge base of terms from the stories.")

# ---------------------------------------------------------------- TIPS
ICON = {
    "talk": '<path d="M4 5h12v8H9l-4 3v-3H4z"/><path d="M16 9h4v8h-1v3l-3-3h-5v-1"/>',
    "plug": '<path d="M9 3v5M15 3v5M7 8h10v3a5 5 0 0 1-10 0zM12 16v5"/>',
    "heart": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
    "q": '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.4-1 1-1 1.7M12 17h.01"/>',
    "bag": '<rect x="4" y="8" width="16" height="12" rx="2"/><path d="M9 8V5h6v3M4 13h16"/>',
    "sock": '<path d="M9 3h6v8l4 4a3 3 0 0 1-3 5c-2 0-3-1-5-3l-2-2z"/>',
    "snow": '<path d="M12 3v18M4.2 7.5l15.6 9M19.8 7.5l-15.6 9M9 4l3 2 3-2M9 20l3-2 3 2"/>',
    "book": '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2zM4 19a2 2 0 0 1 2-2h13"/>',
    "smile": '<circle cx="12" cy="12" r="9"/><path d="M8.5 14a4 4 0 0 0 7 0M9 9.5h.01M15 9.5h.01"/>',
    "spark": '<path d="M12 3l2.2 6.3L21 12l-6.8 2.7L12 21l-2.2-6.3L3 12l6.8-2.7z"/>'}
tips = [
    ("talk", "Communicate &amp; Respect", "Greet people in their language, ask before you photograph, and listen more than you talk."),
    ("plug", "Don&rsquo;t forget your charger", "Phone, camera, power bank &mdash; and the right plug adapter. Nothing ends a photo day faster than 0%."),
    ("heart", "Be Thankful", "A sincere thank-you opens more doors than any guidebook. Say it often, and mean it."),
    ("q", "Try to find out what is &lsquo;normal&rsquo;?", "Every place has its own rhythm: meal times, dress codes, tipping. Observe first, then join in."),
    ("bag", "Pack the right things", "Pack light, pack layers, and leave room for what you will bring back."),
    ("sock", "Don&rsquo;t forget your socks", "The small things make the difference &mdash; dry socks win long days on foot."),
    ("snow", "A/C can kill you on your trip!", "Buses, trains and hotels are often freezing. Keep a light jacket within reach."),
    ("book", "Knowledge &ndash; acquire it", "Read, ask, visit the museum nobody mentioned. Curiosity is the best travel insurance."),
    ("smile", "Smile &ndash; keep it", "It is the one phrase that works in every language."),
    ("spark", "Love &ndash; value it", "People, places, moments &mdash; the things you love are what you will remember.")]
tip_html = "".join('<article class="card tip reveal" style="--d:%.2fs"><span class="n">%02d</span><div class="ic"><svg viewBox="0 0 24 24">%s</svg></div><h3>%s</h3><p>%s</p></article>' % ((i % 3) * 0.08, i + 1, ICON[k], t, d)
                   for i, (k, t, d) in enumerate(tips))
tips_body = (phero("Tips &amp; Tricks", "Ten small things that make <em>every trip better</em>", "Hard-won lessons from the road &mdash; short, practical and (mostly) learned the hard way.", "Tips & Tricks")
             + '<section class="sec"><div class="wrap"><div class="tips">' + tip_html + '</div>'
             '<p style="margin-top:34px;color:var(--muted);font-size:12.5px">Headlines come from the current site; the short descriptions are draft copy &mdash; replace with your own.</p></div></section>'
             + connect_html("Got a tip of your own?", "Share it &mdash; the best ones end up on this page.", "Send it over"))
page("tips.html", "Tips & Tricks – Dex World", tips_body, desc="Ten travel tips and tricks.")

# ---------------------------------------------------------------- STORIES
stories_body = (phero("Stories", "Adventures &amp; <em>observations</em>", "I give it a try &mdash; there you go: my adventures and observations of this &lsquo;crazy&rsquo; world.", "Stories")
                + '<section class="quote tall" aria-label="Quote"><img class="m" src="images/quote.jpg" alt="" aria-hidden="true"><div class="q reveal">'
                '<blockquote>Think outside the box, collapse the box and take a fucking sharp knife to it.</blockquote><cite>Banksy</cite></div></section>'
                '<section class="sec" style="padding-top:clamp(56px,8vw,100px)"><div class="wrap st-layout"><div>'
                '<div class="st-tools" id="st-top"><div class="chips" style="margin:0">'
                '<button class="chip on" data-cat="all">All stories</button><button class="chip" data-cat="Allgemein">Allgemein</button>'
                '<button class="chip" data-cat="Sustain(-able) issues">Sustain(-able) issues</button><button class="chip" data-cat="Travel">Travel</button></div>'
                '<div class="search" style="max-width:none"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>'
                '<input id="st-q" type="search" placeholder="Search stories&hellip;" aria-label="Search stories"></div></div>'
                '<div class="posts" id="posts"></div><div class="pager-n" id="pager"></div></div>'
                '<aside class="side"><div class="card"><h4>Recent posts</h4><ul id="recent"></ul></div>'
                '<div class="card"><h4>Tags</h4><div class="chips" style="margin:0"><span class="chip">#Olympics</span><span class="chip">#SDG 9</span></div></div>'
                '<div class="card"><h4>Follow</h4><ul><li><a href="%s" target="_blank" rel="noopener">LinkedIn</a></li><li><a href="%s" target="_blank" rel="noopener">Instagram</a></li></ul></div>'
                '</aside></div></section>' % (LINKEDIN, INSTAGRAM)
                + connect_html("Have a story to tell?", "Let&rsquo;s write the next chapter together.", "Get in Touch"))
page("stories.html", "Stories – Dex World", stories_body, data=True, desc="Adventures and observations of this crazy world.")

post_body = ('<section class="phero" style="padding-bottom:50px"><div class="wrap"><p class="crumbs"><a href="index.html">Home</a><i></i><a href="stories.html">Stories</a><i></i><span id="a-crumb">Story</span></p>'
             '<div class="eyebrow" style="margin-bottom:22px" id="a-cats">Story</div><h1 id="a-title" style="font-size:clamp(34px,5vw,68px)">Story</h1></div></section>'
             '<section class="sec"><div class="wrap"><article class="article" id="article"><div class="cover"><img alt=""></div>'
             '<div class="prose" id="a-body"></div><div class="post-nav" id="a-nav"></div></article></div></section>'
             + connect_html("Enjoyed the story?", "Say hello &mdash; I read every message.", "Get in Touch"))
page("post.html", "Story – Dex World", post_body, data=True, desc="Story template.")

# ---------------------------------------------------------------- CONTACT
contact_body = (phero("Contact", "Let&rsquo;s <em>talk</em>", "Thank you for visiting my site! Want to chat? Ask a question? Please feel free to contact me &mdash; I read all emails and will do my best to get back to you in a timely manner.", "Contact")
                + '<section class="sec"><div class="wrap c-grid"><div class="reveal"><form class="cf" id="cf" novalidate action="#" method="post">'
                '<div class="fld" data-req><label for="n">Your name <em>*</em></label><input id="n" name="name" autocomplete="name"><span class="em">Please tell me your name.</span></div>'
                '<div class="fld" data-req><label for="e">Your email <em>*</em></label><input id="e" name="email" type="email" autocomplete="email"><span class="em">Please enter a valid email address.</span></div>'
                '<div class="fld"><label for="s">Subject</label><input id="s" name="subject"></div>'
                '<div class="fld" data-req><label for="m">Your message <em>*</em></label><textarea id="m" name="message" rows="5"></textarea><span class="em">Write a few words first.</span></div>'
                '<label class="chk"><input type="checkbox" id="consent" name="consent"><span>I have read and accept the <a href="privacy.html">Privacy Policy</a> and consent to Dex World contacting me about my enquiry.</span></label>'
                '<label class="chk"><input type="checkbox" name="updates"><span>I give consent to Dex World contacting me with future updates. <em style="color:var(--muted)">(optional)</em></span></label>'
                '<button class="btn" type="submit">Send message <svg><use href="#arrow"/></svg></button></form>'
                '<div class="cf-ok" id="cf-ok"><div class="tick"><svg viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></div><h3>Thank you!</h3><p>Your message is on its way &mdash; I&rsquo;ll get back to you soon.</p></div></div>'
                '<aside class="info reveal"><div class="card"><h4>Say hello</h4><p>Want to chat? Ask a question? Feel free to reach out about projects, stories or collaborations.</p></div>'
                '<div class="card"><h4>Elsewhere</h4><a class="sl" href="%s" target="_blank" rel="noopener">LinkedIn <span>&#8599;</span></a><a class="sl" href="%s" target="_blank" rel="noopener">Instagram <span>&#8599;</span></a></div>'
                '<div class="card"><h4>Based in</h4><p>Austria &mdash; and wherever the next adventure leads.</p></div></aside></div></section>' % (LINKEDIN, INSTAGRAM))
page("contact.html", "Contact – Dex World", contact_body, active="contact.html", desc="Get in touch with Deniz.")

# ---------------------------------------------------------------- PRIVACY
legal = [
    ("intro", "Introduction", "<p>Dex World (the &ldquo;Company&rdquo;) wants to protect your privacy. This policy explains what information we collect, how we use it and the choices you have. By using the site or its services you accept this policy. &ldquo;Site&rdquo;, &ldquo;Service&rdquo;, &ldquo;we&rdquo; and &ldquo;you&rdquo; have their everyday meaning.</p>"),
    ("collect", "Information we collect", "<h3>Non-personal information</h3><p>Usage data such as referring URLs, platform types and click counts.</p><h3>Personal information</h3><p>Name, email address and phone number if you submit them &mdash; for example through the contact form.</p><h3>Cookies</h3><p>We use persistent and session cookies to see which pages are viewed, which browser and device are used and when the site is accessed.</p><h3>Accounts</h3><p>If registration is ever offered it will require an email address, username and password.</p><h3>Children</h3><p>The site is not directed at anyone under 13. If we learn we hold data from a child it will be deleted. Contact <a href=\"mailto:%s\">%s</a> with questions.</p>" % (EMAIL, EMAIL)),
    ("use", "How we use and share information", "<ul><li>Personal information is used to answer you, provide support, request feedback and &mdash; with your consent &mdash; send updates.</li><li>It is not sold or shared for marketing without consent, except with service vendors (for example an email provider) or where the law requires it.</li><li>Non-personal information may be used and shared with partners and advertisers.</li><li>Personal data may transfer in a merger, acquisition or sale of assets.</li></ul>"),
    ("protect", "How we protect information", "<p>We use passwords, encryption, firewalls and SSL. No measure can guarantee complete protection, and by using the service you accept this residual risk.</p>"),
    ("rights", "Your rights", "<p>You can opt out of marketing emails at any time through the unsubscribe link or by writing to <a href=\"mailto:%s\">%s</a>. Administrative emails, such as policy updates, may still be sent.</p>" % (EMAIL, EMAIL)),
    ("links", "Links to other websites", "<p>We are not responsible for the privacy practices of third-party sites we link to. Their own policies apply when you visit them.</p>"),
    ("changes", "Changes to this policy", "<p>We may update this policy. Significant changes take effect 30 days after notice (by email or a notice on the site); minor changes take effect immediately.</p>"),
    ("contact", "Contact us", "<p>Questions about this policy? Write to <a href=\"mailto:%s\">%s</a> or use the <a href=\"contact.html\">contact form</a>.</p>" % (EMAIL, EMAIL))]
roman = ["", "I", "II", "III", "IV", "V", "VI", "VII"]
toc = "".join('<a href="#%s">%s</a>' % (i, t) for (i, t, _) in legal)
secs = "".join('<section id="%s" class="reveal"><h2><span>%s</span>%s</h2>%s</section>' % (i, ("0%d" % n) if n else "", t, b) for n, (i, t, b) in enumerate(legal))
privacy_body = (phero("Legal", "Privacy <em>policy</em>", "How your information is collected, used and protected.", "Privacy Policy")
                + '<section class="sec"><div class="wrap legal"><nav class="toc" aria-label="Contents">' + toc + '</nav><div>' + secs
                + '<p class="updated"><i></i>Last updated 20 November 2018</p><p style="margin-top:18px;color:var(--muted);font-size:12.5px">Placeholder policy text &mdash; have it reviewed before launch.</p></div></div></section>')
page("privacy.html", "Privacy Policy – Dex World", privacy_body, desc="Privacy policy.")

# ---------------------------------------------------------------- 404
nf = ('<section class="nf"><p class="crumbs" style="justify-content:center"><span>Page not found</span></p><h1>404</h1>'
      '<p>Looks like this route is not on the map.</p><div><a class="btn" href="index.html">Back to home <svg><use href="#arrow"/></svg></a></div></section>')
page("404.html", "Not found – Dex World", nf, desc="Page not found.")
