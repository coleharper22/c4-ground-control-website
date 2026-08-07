#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builds the C4 Ground Control website into ../build/.

    python3 src/build.py

Reads facts and copy from content.py, photographs from the website backup, and
writes plain static HTML. No frameworks, no build tools, no external requests —
the output folder can be dropped on any host as-is.
"""

import html
import json
import re
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUILD = os.path.join(ROOT, "build")
ASSETS = os.path.join(ROOT, "assets")
BACKUP = os.path.expanduser("~/organization-agent/website-backup/2026-08-07")
PHOTO_SRC = os.path.join(BACKUP, "images")
PHOTO_MAP = os.path.join(HERE, "photo-map.json")

sys.path.insert(0, HERE)
from content import (BIZ, HOURS, AREAS, HERO, HERO_PHOTO, ABOUT, WHY,  # noqa: E402
                     SERVICES, GALLERIES, FAQ)

LOGO_KEY = "50ea251a-b385-49cb-a51a-5d6cc9610c7b.png"
MAX_PER_SERVICE = 12
MAX_PER_GALLERY = 28
WEB_MAX_PX = 1600
THUMB_MAX_PX = 800
SKIP_EXT = {".quicktime", ".mov", ".mp4"}

e = html.escape


# --------------------------------------------------------------------- photos

def load_photo_map():
    with open(PHOTO_MAP) as f:
        data = json.load(f)
    return data["per_page"], set(data["common"])


def is_image(key):
    return os.path.splitext(key)[1].lower() not in SKIP_EXT


def resize(src, dst, max_px):
    """Shrink with macOS sips. Returns True if dst now exists."""
    if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
        return True
    r = subprocess.run(
        ["sips", "-Z", str(max_px), "-s", "format", "jpeg",
         "-s", "formatOptions", "72", src, "--out", dst],
        capture_output=True,
    )
    return r.returncode == 0 and os.path.exists(dst)


def prepare_photos(per_page, common):
    """Pick photos per service/gallery, emit web + thumb copies, return the picks."""
    os.makedirs(os.path.join(BUILD, "img"), exist_ok=True)
    picked, stats = {}, {"web": 0, "thumb": 0, "missing": 0}

    def take(page, limit):
        keys = [k for k in per_page.get(page, []) if is_image(k) and k not in common]
        return keys[:limit]

    wanted = {}
    for svc in SERVICES:
        keys = take(svc["photos"], MAX_PER_SERVICE)
        if not keys and svc.get("photos_fallback"):
            keys = take(svc["photos_fallback"], MAX_PER_SERVICE)
        wanted[svc["slug"]] = keys
    for slug, _label, page in GALLERIES:
        wanted["gallery-" + slug] = take(page, MAX_PER_GALLERY)

    # The homepage hero: an explicit pick from content.py, else the first
    # residential gallery shot (finished properties photograph best).
    if HERO_PHOTO:
        wanted["hero"] = [HERO_PHOTO]
    else:
        first = wanted.get("gallery-residential") or wanted.get("gallery-commercial") or []
        wanted["hero"] = first[:1]

    for group, keys in wanted.items():
        out = []
        for key in keys:
            src = os.path.join(PHOTO_SRC, key)
            if not os.path.exists(src):
                stats["missing"] += 1
                continue
            stem = os.path.splitext(key)[0]
            web = f"{stem}.jpg"
            thumb = f"{stem}-t.jpg"
            if resize(src, os.path.join(BUILD, "img", web), WEB_MAX_PX):
                stats["web"] += 1
            else:
                stats["missing"] += 1
                continue
            if resize(src, os.path.join(BUILD, "img", thumb), THUMB_MAX_PX):
                stats["thumb"] += 1
            out.append((web, thumb))
        picked[group] = out

    # logo, copied at native size
    logo_src = os.path.join(PHOTO_SRC, LOGO_KEY)
    if os.path.exists(logo_src):
        shutil.copy2(logo_src, os.path.join(BUILD, "img", "logo.png"))
    return picked, stats


# ------------------------------------------------------------------ templating

def nav_items():
    return [("Home", "index.html"), ("Services", "services.html"),
            ("Gallery", "gallery.html"), ("About", "about.html"),
            ("Contact", "contact.html")]


def header(current):
    svc_links = "".join(
        f'<a href="services/{s["slug"]}.html">{e(s["name"])}</a>' for s in SERVICES
    )
    main = "".join(
        f'<a href="{href}"{" aria-current=\"page\"" if href == current else ""}>{label}</a>'
        for label, href in nav_items()
    )
    mob = "".join(
        f'<a href="{href}">{label}</a>' for label, href in nav_items()
    )
    return f"""<div class="topbar"><div class="wrap">
  <span>{e(BIZ['license_kind'])} &middot; Lic. {e(BIZ['license'])}</span>
  <span>Free estimates</span>
  <a href="tel:{BIZ['phone_href']}">{e(BIZ['phone'])}</a>
</div></div>
<header class="site">
  <input type="checkbox" id="navtoggle" aria-hidden="true">
  <div class="wrap">
    <a class="brand" href="index.html">
      <img src="img/logo.png" alt="{e(BIZ['name'])} logo" width="46" height="46">
      <b>{e(BIZ['name'])}<small>Sanford, Florida</small></b>
    </a>
    <nav class="main">{main}</nav>
    <a class="btn btn--solid header-cta" href="tel:{BIZ['phone_href']}">{e(BIZ['phone'])}</a>
    <label class="menu-toggle" for="navtoggle" aria-label="Menu">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor"
           stroke-width="2.2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </label>
  </div>
  <div class="mobile-nav">
    {mob}
    <div class="label">Services</div>
    <div class="sub">{svc_links}</div>
  </div>
</header>"""


def cta_block():
    return f"""<section class="cta">
  <div class="wrap">
    <h2>Get a free estimate</h2>
    <p>Tell us what the property needs and we will come look at it. No charge, no obligation.</p>
    <a class="phone" href="tel:{BIZ['phone_href']}">{e(BIZ['phone'])}</a>
    <div class="btn-row">
      <a class="btn btn--call" href="tel:{BIZ['phone_href']}">Call now</a>
      <a class="btn btn--ghost" href="sms:{BIZ['phone_href']}">Send a text</a>
      <a class="btn btn--ghost" href="mailto:{BIZ['email']}">Email us</a>
    </div>
  </div>
</section>"""


def footer():
    svc = "".join(f'<li><a href="services/{s["slug"]}.html">{e(s["name"])}</a></li>'
                  for s in SERVICES)
    areas = "".join(f"<li>{e(a)}, FL</li>" for a in AREAS[:8])
    hrs = "".join(f'<li class="hours-row"><span>{e(d)}</span><span>{e(t)}</span></li>'
                  for d, t in HOURS)
    return f"""{cta_block()}
<footer class="site">
  <div class="wrap">
    <div class="fgrid">
      <div>
        <h4>{e(BIZ['name'])}</h4>
        <ul>
          <li><a href="tel:{BIZ['phone_href']}"><b>{e(BIZ['phone'])}</b></a></li>
          <li><a href="mailto:{BIZ['email']}">{e(BIZ['email'])}</a></li>
          <li>{e(BIZ['address'])}</li>
          <li><a href="{BIZ['google_maps']}" rel="noopener">Find us on Google</a> &middot;
              <a href="{BIZ['facebook']}" rel="noopener">Facebook</a></li>
        </ul>
        <div class="license">
          <b>Licensed &amp; insured</b><br>
          {e(BIZ['license_kind'])}<br>License {e(BIZ['license'])}
        </div>
      </div>
      <div><h4>Services</h4><ul>{svc}</ul></div>
      <div><h4>Service area</h4><ul>{areas}</ul></div>
      <div><h4>Hours</h4><ul>{hrs}</ul></div>
    </div>
    <div class="legal">
      <span>&copy; {BIZ['founded']}&ndash;2026 {e(BIZ['legal'])}. All rights reserved.</span>
      <span>Orlando &middot; Sanford &middot; Central Florida</span>
    </div>
  </div>
</footer>
<a class="callbar" href="tel:{BIZ['phone_href']}">
  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8c1.2 2.3 3.1 4.2 5.4 5.4l1.8-1.8c.2-.2.6-.3.9-.2 1 .3 2.1.5 3.2.5.5 0 .9.4.9.9V19c0 .5-.4.9-.9.9-8 0-14.4-6.5-14.4-14.4 0-.5.4-.9.9-.9h3.4c.5 0 .9.4.9.9 0 1.1.2 2.2.5 3.2.1.3 0 .7-.2.9l-1.8 1.8z"/></svg>
  Call {e(BIZ['phone'])}
</a>"""


EXTERNAL = ("http://", "https://", "mailto:", "tel:", "sms:", "#", "data:", "//")


def relativise(markup, up):
    """Prefix every page-local href/src with `up` so subfolder pages resolve.

    Applied once to the whole assembled page, so the shared header and footer
    get the same treatment as the body — they are page-local links too.
    """
    if not up:
        return markup

    def sub(m):
        attr, val = m.group(1), m.group(2)
        if val.startswith(EXTERNAL) or val.startswith(up):
            return m.group(0)
        return f'{attr}="{up}{val}"'

    return re.sub(r'(href|src)="([^"]+)"', sub, markup)


def page(filename, title, description, body, current, depth=0):
    up = "../" * depth
    inner = relativise(f"{header(current)}\n{body}\n{footer()}", up)

    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="stylesheet" href="{up}css/site.css">
<link rel="icon" href="{up}img/logo.png">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:type" content="website">
<script type="application/ld+json">
{json.dumps({
    "@context": "https://schema.org",
    "@type": "LandscapingBusiness",
    "name": BIZ["name"],
    "legalName": BIZ["legal"],
    "telephone": BIZ["phone"],
    "email": BIZ["email"],
    "address": {"@type": "PostalAddress", "streetAddress": "1173 Butler Way",
                "addressLocality": "Sanford", "addressRegion": "FL",
                "postalCode": "32773", "addressCountry": "US"},
    "areaServed": [{"@type": "City", "name": a} for a in AREAS],
    "sameAs": [BIZ["facebook"], BIZ["google_maps"]],
}, indent=1)}
</script>
</head>
<body>
{inner}
</body>
</html>
"""
    out = os.path.join(BUILD, filename)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)


# ---------------------------------------------------------------------- pages

def build_home(photos):
    hero = photos.get("hero") or photos.get("landscaping") or []
    hero_img = f'<img class="bg" src="img/{hero[0][0]}" alt="" fetchpriority="high">' if hero else ""
    cards = ""
    for s in SERVICES:
        p = photos.get(s["slug"])
        img = (f'<img src="img/{p[0][1]}" alt="{e(s["name"])}" loading="lazy">'
               if p else '<img src="img/logo.png" alt="" loading="lazy">')
        cards += f"""<a class="card" href="services/{s['slug']}.html">
      {img}
      <div class="body">
        <h3>{e(s['name'])}</h3><p>{e(s['blurb'])}</p>
        <span class="more">Learn more &rarr;</span>
      </div></a>"""
    why = "".join(f"<li><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t, d in WHY)
    areas = "".join(f"<li>{e(a)}, FL</li>" for a in AREAS)
    faq = "".join(f"<details class=\"faq\"><summary>{e(q)}</summary><p>{e(a)}</p></details>"
                  for q, a in FAQ[:5])

    body = f"""<section class="hero">{hero_img}<div class="wrap">
  <h1>{e(HERO['headline'])}</h1>
  <p>{e(HERO['sub'])}</p>
  <div class="btn-row" style="margin-top:26px">
    <a class="btn btn--call" href="tel:{BIZ['phone_href']}">Call {e(BIZ['phone'])}</a>
    <a class="btn btn--ghost" href="contact.html">Get a free estimate</a>
  </div>
  <ul class="badges">
    <li>Licensed irrigation contractor</li><li>Insured</li>
    <li>Free estimates</li><li>Residential &amp; commercial</li>
  </ul>
</div></section>

<section class="section"><div class="wrap">
  <p class="eyebrow">What we do</p>
  <h2>Services</h2>
  <p class="lede narrow">Seven things, done properly, across Central Florida.</p>
  <div class="grid grid--3" style="margin-top:36px">{cards}</div>
</div></section>

<section class="section section--sand"><div class="wrap">
  <p class="eyebrow">Why C4</p>
  <h2>What you get working with us</h2>
  <ul class="why" style="margin-top:34px">{why}</ul>
</div></section>

<section class="section"><div class="wrap two-col">
  <div>
    <p class="eyebrow">About</p>
    <h2>A licensed contractor, not a lawn crew</h2>
    {''.join(f'<p>{e(p)}</p>' for p in ABOUT)}
    <a class="btn btn--solid" href="about.html">More about us</a>
  </div>
  <div class="aside">
    <h3>Straight to a person</h3>
    <p>Calls go to us, not a call centre. If we are on a job and miss you, we call back.</p>
    <p><a class="btn btn--call" href="tel:{BIZ['phone_href']}" style="width:100%">
      {e(BIZ['phone'])}</a></p>
    <p style="margin:0;font-size:.9rem;color:var(--ink-soft)">
      {''.join(f'{e(d)}: {e(t)}<br>' for d, t in HOURS)}
    </p>
  </div>
</div></section>

<section class="section section--dark"><div class="wrap">
  <p class="eyebrow">Where we work</p>
  <h2>Serving Central Florida</h2>
  <p class="lede" style="margin-bottom:26px">Based in Sanford, out across the whole region.</p>
  <ul class="chips">{areas}</ul>
</div></section>

<section class="section"><div class="wrap narrow">
  <p class="eyebrow">Questions</p>
  <h2>Common questions</h2>
  <div style="margin-top:24px">{faq}</div>
</div></section>"""
    page("index.html", f"{BIZ['name']} — Irrigation & Landscaping in Orlando & Sanford, FL",
         "Licensed irrigation and landscaping contractor serving Orlando, Sanford and Central "
         "Florida. Sprinkler install and repair, sod, drainage, plantings and outdoor lighting. "
         "Free estimates.", body, "index.html")


def build_services_index(photos):
    cards = ""
    for s in SERVICES:
        p = photos.get(s["slug"])
        img = (f'<img src="img/{p[0][1]}" alt="{e(s["name"])}" loading="lazy">'
               if p else '<img src="img/logo.png" alt="" loading="lazy">')
        cards += f"""<a class="card" href="services/{s['slug']}.html">{img}
      <div class="body"><h3>{e(s['name'])}</h3><p>{e(s['blurb'])}</p>
      <span class="more">Learn more &rarr;</span></div></a>"""
    body = f"""<section class="hero hero--slim"><div class="wrap">
  <h1>Our services</h1>
  <p>Irrigation, sod, drainage, plantings, lighting and site work &mdash; across Central Florida.</p>
</div></section>
<section class="section"><div class="wrap">
  <div class="grid grid--3">{cards}</div>
</div></section>"""
    page("services.html", f"Services — {BIZ['name']}",
         "Irrigation design and repair, sod installation, drainage, landscaping, outdoor "
         "lighting, site prep and hydroseeding across Central Florida.", body, "services.html")


def build_service(svc, photos):
    p = photos.get(svc["slug"], [])
    hero = f'<img class="bg" src="img/{p[0][0]}" alt="">' if p else ""
    shots = "".join(
        f'<a href="img/{web}" target="_blank" rel="noopener">'
        f'<img src="img/{thumb}" alt="{e(svc["name"])} — {BIZ["name"]}" loading="lazy"></a>'
        for web, thumb in p[1:]
    )
    gallery = f"""<section class="section section--sand"><div class="wrap">
  <p class="eyebrow">Our work</p><h2>{e(svc['name'])} photos</h2>
  <p class="lede">Real jobs, our own photographs.</p>
  <div class="gallery" style="margin-top:30px">{shots}</div>
</div></section>""" if shots else ""

    # Written root-relative like every other link; relativise() adds the ../ prefix.
    others = "".join(
        f'<li><a href="services/{o["slug"]}.html">{e(o["name"])}</a></li>'
        for o in SERVICES if o["slug"] != svc["slug"]
    )
    body = f"""<section class="hero hero--slim">{hero}<div class="wrap">
  <p class="crumbs"><a href="index.html">Home</a> &rsaquo;
     <a href="services.html">Services</a> &rsaquo; {e(svc['name'])}</p>
  <h1>{e(svc['name'])}</h1>
  <p>{e(svc['blurb'])}</p>
  <div class="btn-row" style="margin-top:24px">
    <a class="btn btn--call" href="tel:{BIZ['phone_href']}">Call {e(BIZ['phone'])}</a>
    <a class="btn btn--ghost" href="contact.html">Free estimate</a>
  </div>
</div></section>

<section class="section"><div class="wrap two-col">
  <div>
    {''.join(f'<p>{e(par)}</p>' for par in svc['body'])}
    <h3 style="margin-top:1.6em">What this covers</h3>
    <ul class="ticks">{''.join(f'<li>{e(b)}</li>' for b in svc['bullets'])}</ul>
  </div>
  <div>
    <div class="aside">
      <h3>Free estimate</h3>
      <p>We will come out, look at it, and give you a number in writing.</p>
      <a class="btn btn--call" href="tel:{BIZ['phone_href']}" style="width:100%">
        {e(BIZ['phone'])}</a>
      <p style="margin:14px 0 0;font-size:.88rem;color:var(--ink-soft)">
        Licensed {e(BIZ['license'])} &middot; Insured</p>
    </div>
    <div class="aside" style="margin-top:20px">
      <h3>Other services</h3>
      <ul class="ticks" style="grid-template-columns:1fr;margin:0">{others}</ul>
    </div>
  </div>
</div></section>
{gallery}"""
    page(f"services/{svc['slug']}.html", f"{svc['name']} — Orlando & Central Florida | {BIZ['name']}",
         svc["short"] + f". Licensed and insured, serving Orlando, Sanford and Central Florida. "
         f"Free estimates — call {BIZ['phone']}.",
         body, "services.html", depth=1)


def build_gallery(photos):
    sections = ""
    for slug, label, _page in GALLERIES:
        p = photos.get("gallery-" + slug, [])
        if not p:
            continue
        shots = "".join(
            f'<a href="img/{web}" target="_blank" rel="noopener">'
            f'<img src="img/{thumb}" alt="{e(label)} landscaping — {BIZ["name"]}" loading="lazy"></a>'
            for web, thumb in p
        )
        sections += f"""<section class="section"><div class="wrap">
  <h2>{e(label)}</h2><div class="gallery" style="margin-top:24px">{shots}</div>
</div></section>"""
    body = f"""<section class="hero hero--slim"><div class="wrap">
  <h1>Our work</h1>
  <p>Photographs of our own jobs across Central Florida &mdash; no stock images.</p>
</div></section>
{sections}"""
    page("gallery.html", f"Gallery — Our Work | {BIZ['name']}",
         "Photos of irrigation, sod, drainage, landscaping and lighting jobs completed by "
         "C4 Ground Control across Central Florida.", body, "gallery.html")


def build_about():
    why = "".join(f"<li><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t, d in WHY)
    faq = "".join(f"<details class=\"faq\"><summary>{e(q)}</summary><p>{e(a)}</p></details>"
                  for q, a in FAQ)
    body = f"""<section class="hero hero--slim"><div class="wrap">
  <h1>About C4 Ground Control</h1>
  <p>{e(BIZ['tagline'])} &mdash; based in Sanford, licensed and insured.</p>
</div></section>
<section class="section"><div class="wrap narrow">
  {''.join(f'<p class="lede">{e(p)}</p>' if i == 0 else f'<p>{e(p)}</p>'
           for i, p in enumerate(ABOUT))}
</div></section>
<section class="section section--sand"><div class="wrap">
  <h2>How we work</h2><ul class="why" style="margin-top:30px">{why}</ul>
</div></section>
<section class="section"><div class="wrap narrow">
  <h2>Questions</h2><div style="margin-top:22px">{faq}</div>
</div></section>"""
    page("about.html", f"About — {BIZ['name']} | Sanford, FL",
         f"C4 Ground Control is a licensed irrigation and landscaping contractor in Sanford, "
         f"Florida. License {BIZ['license']}. Serving Orlando and Central Florida.",
         body, "about.html")


def build_contact():
    hrs = "".join(f'<li class="hours-row"><span>{e(d)}</span><span>{e(t)}</span></li>'
                  for d, t in HOURS)
    areas = "".join(f"<li>{e(a)}, FL</li>" for a in AREAS)
    body = f"""<section class="hero hero--slim"><div class="wrap">
  <h1>Get in touch</h1>
  <p>Call or text for a free estimate. We answer the phone ourselves.</p>
</div></section>
<section class="section"><div class="wrap two-col">
  <div>
    <h2 class="mt0">Fastest way to reach us</h2>
    <p class="lede">Pick up the phone. Estimates are free and we can usually be out within
    a few days &mdash; sooner for a leaking irrigation line.</p>
    <div class="btn-row" style="margin:26px 0">
      <a class="btn btn--call" href="tel:{BIZ['phone_href']}">Call {e(BIZ['phone'])}</a>
      <a class="btn btn--solid" href="sms:{BIZ['phone_href']}">Send a text</a>
    </div>
    <h3>Email</h3>
    <p><a href="mailto:{BIZ['email']}">{e(BIZ['email'])}</a> &mdash; good for photos of the
    problem, plans or documents. We reply the same working day.</p>
    <h3>Where we are</h3>
    <p>{e(BIZ['address'])}<br>
    <a href="{BIZ['google_maps']}" rel="noopener">Open in Google Maps</a></p>
    <h3>What to tell us</h3>
    <ul class="ticks">
      <li>The address of the property</li>
      <li>What you are trying to fix or build</li>
      <li>Whether it is residential or commercial</li>
      <li>Photos, if you have them</li>
    </ul>
  </div>
  <div>
    <div class="aside"><h3 class="mt0">Hours</h3>
      <ul style="list-style:none;padding:0;margin:0;display:grid;gap:9px">{hrs}</ul>
      <p style="margin:16px 0 0;font-size:.9rem;color:var(--ink-soft)">
        Miss us? Leave a message and we call back &mdash; we are usually on a job.</p>
    </div>
    <div class="aside" style="margin-top:20px">
      <h3 class="mt0">Licensed &amp; insured</h3>
      <p style="margin:0">{e(BIZ['license_kind'])}<br>
      License <b>{e(BIZ['license'])}</b><br>Liability insured &mdash; certificate on request.</p>
    </div>
  </div>
</div></section>
<section class="section section--dark"><div class="wrap">
  <h2>Service area</h2>
  <p class="lede" style="margin-bottom:24px">Not listed? Call and ask &mdash; we travel.</p>
  <ul class="chips">{areas}</ul>
</div></section>"""
    page("contact.html", f"Contact — Free Estimates | {BIZ['name']}",
         f"Call {BIZ['phone']} for a free landscaping or irrigation estimate in Orlando, "
         "Sanford and Central Florida.", body, "contact.html")


def build_extras():
    urls = ["index.html", "services.html", "gallery.html", "about.html", "contact.html"]
    urls += [f"services/{s['slug']}.html" for s in SERVICES]
    with open(os.path.join(BUILD, "sitemap.txt"), "w") as f:
        for u in urls:
            f.write(f"https://c4groundcontrol.com/{u}\n")
    with open(os.path.join(BUILD, "robots.txt"), "w") as f:
        f.write("User-agent: *\nAllow: /\nSitemap: https://c4groundcontrol.com/sitemap.txt\n")
    with open(os.path.join(BUILD, "CNAME"), "w") as f:
        f.write("c4groundcontrol.com\n")


def main():
    os.makedirs(BUILD, exist_ok=True)
    shutil.rmtree(os.path.join(BUILD, "css"), ignore_errors=True)
    shutil.copytree(os.path.join(ASSETS, "css"), os.path.join(BUILD, "css"))

    per_page, common = load_photo_map()
    print("Preparing photographs (sips)…")
    photos, stats = prepare_photos(per_page, common)
    print(f"  web copies: {stats['web']}   thumbs: {stats['thumb']}   skipped: {stats['missing']}")

    build_home(photos)
    build_services_index(photos)
    for svc in SERVICES:
        build_service(svc, photos)
    build_gallery(photos)
    build_about()
    build_contact()
    build_extras()

    pages = sum(len([f for f in fs if f.endswith(".html")]) for _, _, fs in os.walk(BUILD))
    size = subprocess.run(["du", "-sh", BUILD], capture_output=True, text=True).stdout.split()[0]
    print(f"\nBuilt {pages} pages into {BUILD}  ({size})")


if __name__ == "__main__":
    main()
