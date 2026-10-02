#!/usr/bin/env python3
"""
Generates the 13 Endurion-styled detail pages that sit under the Sentrillion
homepage (markets/, capabilities/, contracts/, about/, careers/). Each page
shares the exact nav/footer chrome from index.html, adjusted for its folder
depth, plus a new Endurion-style inner-page hero and a handful of reusable
content-block components (detail-block, spec-list, spec-meta, people-grid).

This is an authoring convenience, not a build step end users need to run --
the generated .html files are committed as plain static files. Re-run this
script (`python3 build_pages.py`) after editing PAGES below to regenerate.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

MARKET_LINKS = [
    ("Homeland Security & Law Enforcement", "markets/homeland-security-law-enforcement/"),
    ("Defense", "markets/defense/"),
    ("Transportation & Commercial", "markets/transportation-civilian/"),
    ("International", "markets/international/"),
]
CAPABILITY_LINKS = [
    ("Operations & Field Support", "capabilities/operations-field-support/"),
    ("IT & Cyber Services", "capabilities/it-cyber-services/"),
    ("Engineering & Integration", "capabilities/engineering-integration/"),
    ("Identity & Access Management", "capabilities/identity-access-management/"),
]
CONTRACT_LINKS = [
    ("OASIS+ Small Business", "contracts/oasis-small-business/"),
    ("GSA Multiple Award Schedule", "contracts/multiple-award-schedule/"),
]
ABOUT_LINKS = [
    ("Sentrillion Leadership", "about/sentrillion-leadership/"),
    ("Community Outreach", "about/community-outreach/"),
]
RELATED_GROUPS = {
    "markets": ("Markets", MARKET_LINKS),
    "capabilities": ("Capabilities", CAPABILITY_LINKS),
    "contracts": ("Contract Vehicles", CONTRACT_LINKS),
    "about": ("About", ABOUT_LINKS),
}


def nav_html(root):
    """Nav markup identical to index.html's, with hrefs adjusted for folder depth."""
    return f'''<header class="nav" id="nav">
  <div class="nav-inner">
    <a href="{root}index.html" class="logo">
      <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="14" cy="14" r="13" stroke="currentColor" stroke-width="1.4"/>
        <path d="M14 3L14 25M14 3L20 14L14 25L8 14L14 3Z" stroke="currentColor" stroke-width="1.2"/>
      </svg>
      <span>SENTRILLION</span>
    </a>
    <nav class="nav-links" id="navLinks">
      <div class="nav-item">
        <div class="nav-item-row">
          <a href="{root}#capabilities">Capabilities</a>
          <button class="nav-caret" aria-label="Toggle Capabilities submenu" aria-expanded="false">&#9662;</button>
        </div>
        <div class="nav-dropdown">
          <a href="{root}capabilities/operations-field-support/">Operations &amp; Field Support</a>
          <a href="{root}capabilities/it-cyber-services/">IT &amp; Cyber Services</a>
          <a href="{root}capabilities/engineering-integration/">Engineering &amp; Integration</a>
          <a href="{root}capabilities/identity-access-management/">Identity &amp; Access Management</a>
        </div>
      </div>
      <div class="nav-item">
        <div class="nav-item-row">
          <a href="{root}#markets">Markets</a>
          <button class="nav-caret" aria-label="Toggle Markets submenu" aria-expanded="false">&#9662;</button>
        </div>
        <div class="nav-dropdown">
          <a href="{root}markets/homeland-security-law-enforcement/">Homeland Security &amp; Law Enforcement</a>
          <a href="{root}markets/defense/">Defense</a>
          <a href="{root}markets/transportation-civilian/">Transportation &amp; Commercial</a>
          <a href="{root}markets/international/">International</a>
        </div>
      </div>
      <div class="nav-item">
        <div class="nav-item-row">
          <a href="{root}#vehicles">Contract Vehicles</a>
          <button class="nav-caret" aria-label="Toggle Contract Vehicles submenu" aria-expanded="false">&#9662;</button>
        </div>
        <div class="nav-dropdown">
          <a href="{root}contracts/oasis-small-business/">OASIS+ Small Business</a>
          <a href="{root}contracts/multiple-award-schedule/">GSA Multiple Award Schedule</a>
        </div>
      </div>
      <div class="nav-item">
        <div class="nav-item-row">
          <a href="{root}#about">About</a>
          <button class="nav-caret" aria-label="Toggle About submenu" aria-expanded="false">&#9662;</button>
        </div>
        <div class="nav-dropdown">
          <a href="{root}about/sentrillion-leadership/">Sentrillion Leadership</a>
          <a href="{root}about/community-outreach/">Community Outreach</a>
        </div>
      </div>
      <a href="{root}careers/">Careers</a>
      <a href="{root}#contact">Contact</a>
      <span class="nav-underline" id="navUnderline" aria-hidden="true"></span>
    </nav>
    <a href="{root}#contact" class="btn btn-ghost nav-cta">Get in Touch</a>
    <button class="menu-toggle" id="menuToggle" aria-label="Toggle menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>'''


def footer_html(root):
    return f'''<footer class="footer">
  <div class="footer-top">
    <div class="footer-brand">
      <svg width="46" height="46" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="14" cy="14" r="13" stroke="currentColor" stroke-width="1.2"/>
        <path d="M14 3L14 25M14 3L20 14L14 25L8 14L14 3Z" stroke="currentColor" stroke-width="1"/>
      </svg>
    </div>
    <div class="footer-col">
      <span class="footer-heading">General</span>
      <a href="{root}#capabilities">Capabilities</a>
      <a href="{root}#markets">Markets</a>
      <a href="{root}#vehicles">Contract Vehicles</a>
      <a href="{root}#about">About</a>
      <a href="{root}#contact">Contact</a>
    </div>
    <div class="footer-col">
      <span class="footer-heading">Careers</span>
      <a href="{root}careers/">Overview</a>
      <a href="{root}careers/">Find a Career</a>
    </div>
  </div>
  <div class="footer-mid">
    <a href="mailto:info@sentrillion.com" class="footer-email"><span>&#8618;</span> info@sentrillion.com</a>
    <div class="footer-legal">
      <a href="#">Privacy Policy</a>
      <a href="#">Terms &amp; Conditions</a>
    </div>
    <p class="footer-copy">&copy; <span id="year"></span> Sentrillion Corporation. All rights reserved.</p>
    <div class="social-row">
      <a href="#" aria-label="LinkedIn">IN</a>
      <a href="#" aria-label="Twitter / X">X</a>
      <a href="#" aria-label="YouTube">YT</a>
    </div>
  </div>
  <div class="accent-bar"></div>
  <h2 class="footer-wordmark">SENTRILLION</h2>
</footer>'''


def esc(s):
    return s


_LINK_FIX_RE = re.compile(r'href="((?:\.\./)*(?:capabilities|markets|contracts|about|careers)(?:/[a-z0-9-]+)?/)"')


_HOME_HASH_RE = re.compile(r'href="((?:\.\./)+)#')


def fix_links(html):
    """Static hosting (and a browser opening index.html directly via file://)
    won't auto-resolve a bare directory URL to its index.html, so every
    internal link must name the file explicitly."""
    html = _LINK_FIX_RE.sub(lambda m: f'href="{m.group(1)}index.html"', html)
    # Links back to homepage sections ("../../#contact") also need the file named.
    return _HOME_HASH_RE.sub(lambda m: f'href="{m.group(1)}index.html#', html)


def render_blocks(blocks, root=""):
    out = []
    for b in blocks:
        t = b["type"]
        if t == "intro":
            out.append(f'<p class="detail-intro">{b["text"]}</p>')
        elif t == "break":
            out.append(f'<div style="margin-top:56px">'
                        f'<p class="tag"><span class="dot"></span>{b["tag"]}</p>'
                        f'<p class="detail-intro">{b["text"]}</p></div>')
        elif t == "detail":
            rows = []
            for item in b["items"]:
                body = item["body"]
                if isinstance(body, list):
                    body_html = "".join(f"<p>{p}</p>" for p in body)
                else:
                    body_html = f"<p>{body}</p>"
                rows.append(
                    f'<div class="detail-block"><span class="num">{item["num"]}</span>'
                    f'<div><h3>{item["heading"]}</h3>{body_html}</div></div>'
                )
            out.append("".join(rows))
        elif t == "spec_list":
            if b.get("heading"):
                out.append(f'<p class="footnote-left" style="color:var(--white);font-family:var(--font-display);font-weight:500;font-size:1.05rem;margin:8px 0 -6px;">{b["heading"]}</p>')
            items = "".join(f"<li>{i}</li>" for i in b["items"])
            out.append(f'<ul class="spec-list">{items}</ul>')
        elif t == "spec_meta":
            cells = "".join(
                f'<div><span>{k}</span><span>{v}</span></div>' for k, v in b["items"]
            )
            out.append(f'<div class="spec-meta">{cells}</div>')
        elif t == "people":
            cards = []
            for p in b["items"]:
                photo_rel = p.get("photo", "")
                photo_path = os.path.join(ROOT, "assets", "photos", photo_rel) if photo_rel else ""
                has_real_photo = bool(photo_rel) and os.path.isfile(photo_path)
                if has_real_photo:
                    img_src = f"{root}assets/photos/{photo_rel}"
                    photo_class = "person-photo"
                else:
                    img_src = f"{root}assets/photos/placeholder-person.svg"
                    photo_class = "person-photo is-placeholder"
                cards.append(
                    f'<div class="person-card" tabindex="0">'
                    f'<div class="{photo_class}"><img src="{img_src}" alt="{p["name"]}" loading="lazy"></div>'
                    f'<div class="person-card-body">'
                    f'<span class="num">{p["num"]}</span>'
                    f'<h4>{p["name"]}</h4>'
                    f'<span class="role">{p["role"]}</span>'
                    f'<p>{p["bio"]}</p>'
                    f'</div></div>'
                )
            out.append(f'<div class="people-grid">{"".join(cards)}</div>')
        elif t == "sponsors":
            cards = []
            for item in b["items"]:
                body = item["body"]
                if isinstance(body, list):
                    body_html = "".join(f"<p>{p}</p>" for p in body)
                else:
                    body_html = f"<p>{body}</p>"
                logo_rel = item.get("logo", "")
                logo_src = f"{root}assets/logos/{logo_rel}" if logo_rel else ""
                cards.append(
                    f'<div class="sponsor-block">'
                    f'<div class="sponsor-logo"><img src="{logo_src}" alt="{item["heading"]} logo" loading="lazy"></div>'
                    f'<div class="sponsor-body"><span class="num">{item["num"]}</span><h3>{item["heading"]}</h3>{body_html}</div>'
                    f'</div>'
                )
            out.append("".join(cards))
        elif t == "cta":
            out.append(f'<p style="margin-top:8px"><a href="{b["href"]}" class="btn btn-line">{b["label"]}</a></p>')
        elif t == "cta_row":
            links = "".join(
                f'<a href="{href}" class="btn btn-line" style="margin-right:34px">{label}</a>'
                for label, href in b["items"]
            )
            out.append(f'<p style="margin-top:8px">{links}</p>')
        elif t == "footnote":
            out.append(f'<p class="capabilities-footnote footnote-left" style="max-width:680px;margin-top:56px;">{b["text"]}</p>')
    return "\n    ".join(out)


def render_related(related_key, current_path, root):
    label, links = RELATED_GROUPS[related_key]
    items = []
    for name, href in links:
        is_current = ' class="is-current"' if href == current_path else ""
        items.append(f'<a href="{root}{href}"{is_current}>{name}</a>')
    return f'''<div class="related-strip">
    <p class="tag"><span class="dot"></span>MORE {label.upper()}</p>
    <div class="related-links">
      {"".join(items)}
    </div>
  </div>'''


def render_page(page):
    depth = len([p for p in page["path"].split("/") if p])
    root = "../" * depth
    title = page["title"]
    meta_desc = page.get("meta", page["subhead"])
    body = render_blocks(page["blocks"], root)
    related = render_related(page["related_key"], page["path"], root) if page["related_key"] else ""

    if page.get("plate_tracks"):
        tracks_json = json.dumps(page["plate_tracks"], separators=(",", ":"))
        plate_layer_html = '<div class="plate-track-layer" data-plate-tracks=\'' + tracks_json + '\'></div>'
    else:
        plate_layer_html = ""

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<script>document.documentElement.classList.add('js');</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Sentrillion</title>
<meta name="description" content="{meta_desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}css/style.css">
</head>
<body>

<div class="cursor-glow" id="cursorGlow" aria-hidden="true"></div>
<div class="scroll-indicator" id="scrollIndicator"></div>

{nav_html(root)}

<main id="top">

  <section class="page-hero">
    <div class="page-hero-bg" aria-hidden="true">
      {(f'<video autoplay muted loop playsinline preload="auto" poster="{root}assets/photos/{page.get("video_poster", page["photo"])}"><source src="{root}assets/video/{page["video"]}" type="video/mp4"><source src="{root}assets/video/{page["video"].rsplit(".", 1)[0]}.webm" type="video/webm"></video>' if page.get('video') else f'<img src="{root}assets/photos/{page["photo"]}" alt="{page.get("photo_alt", "")}">')}{'<div class="page-hero-scan-track"><div class="page-hero-scan"></div></div>' if page.get('scan_line') else ''}{plate_layer_html}
    </div>
    <div class="page-hero-inner">
      <h1 class="reveal is-visible">{page['title']}</h1>
      <div class="accent-bar"></div>
      <p class="page-hero-tag"><span class="br">[</span> {page['category']} <span class="br">]</span></p>
      <p class="page-hero-sub">{page['subhead']}</p>
    </div>
  </section>

  <section class="page-content">
    {body}

    {related}
  </section>

</main>

{footer_html(root)}

<script src="{root}js/main.js"></script>
</body>
</html>
'''
    html = fix_links(html)
    out_dir = os.path.join(ROOT, page["path"])
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w") as f:
        f.write(html)
    print("wrote", os.path.join(page["path"], "index.html"))


# Per-vehicle [seconds, xPercent, yPercent] waypoints traced from the real
# border-checkpoint.mp4 footage, used to drive the plate-tracking laser dots
# on the Homeland Security hero video. Vehicles were located with
# background-subtraction tracking, then every candidate track was audited by
# eye across its FULL lifespan (dense per-track contact sheets, not a single
# sample frame) to rule out identity switches, merged/duplicate boxes, and
# non-vehicle detections (a couple of tracks turned out to be a pedestrian or
# a static structure and were discarded). Each waypoint is anchored to the
# front plate specifically: it's offset from the tracked box's center along
# the vehicle's own (smoothed) direction of travel, not a fixed offset, so it
# tracks correctly whichever way the vehicle is oriented on screen. Waypoints
# are spaced closely (~0.12s apart) so the straight-line interpolation in
# js/main.js's "Plate-tracking laser dots" block can't visibly drift off the
# plate between samples, even on curved paths.
HOMELAND_PLATE_TRACKS = {'v1': [[3.403, 85.73, 74.94], [3.537, 85.95, 76.01], [3.67, 87.61, 76.57], [3.804, 88.67, 77.19], [3.937, 89.39, 77.98], [4.071, 89.6, 78.9], [4.204, 90.36, 79.77], [4.338, 90.64, 80.36], [4.471, 91.88, 80.97], [4.605, 92.24, 81.86], [4.738, 92.73, 82.69], [4.872, 93.77, 83.42], [5.005, 93.99, 83.8], [5.138, 94.59, 84.36], [5.272, 95.45, 85.13], [5.405, 96.02, 85.75], [5.539, 97.11, 87.05], [5.672, 97.7, 88.01], [5.806, 97.63, 88.87], [5.839, 97.65, 89.14]], 'v2': [[3.77, 74.34, 63.82], [3.904, 74.41, 64.13], [4.037, 74.41, 64.3], [4.171, 74.73, 64.72], [4.304, 74.89, 65.1], [4.438, 75.06, 65.58], [4.571, 75.47, 68.04], [4.705, 75.9, 68.49], [4.838, 76.25, 68.92], [4.972, 76.43, 69.18], [5.105, 76.91, 69.03], [5.239, 77.36, 69.52], [5.372, 77.75, 71.77], [5.506, 78.04, 70.36], [5.639, 78.13, 71.04], [5.772, 78.37, 71.52], [5.906, 78.55, 72.11], [6.039, 78.96, 72.78], [6.173, 79.4, 73.2], [6.306, 80.19, 73.68], [6.44, 80.07, 74.26], [6.573, 80.5, 74.82], [6.707, 80.9, 75.43], [6.84, 81.33, 75.96], [6.974, 81.72, 76.6], [7.107, 82.2, 77.21], [7.241, 82.73, 77.79], [7.374, 83.25, 78.46], [7.508, 83.77, 79.04], [7.641, 84.37, 79.78], [7.774, 85.02, 80.43], [7.908, 85.51, 81.24], [8.041, 86.1, 82.01], [8.175, 86.68, 82.79], [8.308, 87.35, 83.53], [8.442, 88.01, 84.3], [8.575, 88.69, 85.18], [8.709, 89.32, 85.86], [8.842, 90.01, 86.8], [8.976, 90.69, 87.54], [9.109, 91.39, 88.45], [9.243, 92.13, 89.36], [9.376, 92.97, 90.24], [9.576, 94.12, 91.67], [9.71, 94.93, 92.54], [9.843, 95.74, 93.59], [9.977, 96.65, 94.59], [10.11, 97.2, 95.09], [10.244, 97.41, 95.29], [10.377, 97.5, 95.47], [10.511, 97.87, 95.73], [10.644, 98.14, 95.98], [10.777, 98.12, 96.32], [10.911, 98.44, 96.71], [10.978, 98.47, 96.87]], 'v3': [[4.872, 35.5, 87.69], [5.005, 35.35, 87.38], [5.138, 36.01, 86.76], [5.506, 35.2, 87.43], [5.772, 34.28, 86.83], [5.973, 34.24, 85.78], [6.106, 34.42, 84.97], [6.24, 34.36, 87.68], [6.373, 36.07, 88.91], [6.507, 36.09, 89.43], [6.64, 36.43, 90.07], [6.773, 37.38, 87.29], [6.807, 37.43, 87.3]], 'v4': [[6.006, 60.78, 52.66], [6.139, 61.72, 54.08], [6.273, 62.39, 52.07], [6.406, 62.22, 51.07], [6.54, 62.82, 51.56], [6.673, 62.65, 53.68], [6.807, 62.35, 54.81], [6.94, 62.73, 54.9], [7.074, 63.18, 54.95], [7.207, 63.73, 54.52], [7.341, 64.08, 54.82], [7.474, 64.04, 55.85], [7.608, 63.63, 56.23], [7.774, 64.07, 58.48], [7.941, 64.2, 59.34], [8.075, 64.77, 59.38], [8.208, 65.49, 59.09], [8.342, 66.82, 58.53], [8.475, 67.29, 58.81], [8.609, 67.84, 59.15], [8.742, 68.33, 59.81], [8.876, 68.77, 60.32], [9.009, 69.4, 60.75], [9.109, 69.7, 61.3]], 'v5': [[5.973, 56.74, 73.84], [6.106, 56.92, 74.1], [6.24, 56.97, 74.65], [6.373, 56.89, 74.83], [6.507, 57.62, 81.21], [6.64, 57.89, 81.95], [6.773, 57.46, 82.28], [6.907, 56.52, 83.01], [7.04, 55.61, 83.29], [7.174, 55.35, 83.64], [7.307, 55.46, 84.4], [7.441, 55.52, 85.12], [7.574, 55.47, 85.85], [7.708, 55.01, 86.29], [7.841, 54.44, 86.7], [7.975, 54.18, 87.38], [8.108, 53.85, 87.92], [8.242, 53.41, 88.64], [8.375, 53.26, 89.47], [8.509, 52.89, 90.4], [8.642, 52.68, 91.33], [8.775, 52.3, 92.17], [8.909, 51.84, 92.66], [9.042, 51.43, 93.36], [9.176, 50.99, 94.27], [9.309, 50.6, 95.05], [9.443, 50.44, 95.88], [9.576, 49.76, 96.13], [9.71, 49.11, 95.39], [9.843, 48.15, 93.67], [9.977, 48.04, 93.23], [10.043, 47.57, 92.6]], 'v6': [[6.34, 55.01, 55.77], [6.473, 55.18, 56.46], [6.607, 55.52, 57.07], [6.74, 55.06, 57.62], [6.874, 54.44, 61.11], [7.007, 54.11, 62.08], [7.14, 54.16, 62.43], [7.274, 54.62, 66.4], [7.407, 54.69, 66.69], [7.541, 55.13, 66.99], [7.674, 55.49, 67.4], [7.808, 55.31, 68.01], [7.941, 55.11, 68.51], [8.075, 55.29, 68.73], [8.208, 55.65, 68.92], [8.342, 55.98, 69.22], [8.475, 56.15, 69.61], [8.609, 56.11, 70.12], [8.742, 56.1, 70.59], [8.876, 56.27, 70.78], [9.009, 56.49, 71.09], [9.142, 56.64, 71.44], [9.276, 56.68, 71.89], [9.409, 56.68, 72.48], [9.543, 56.5, 73.09], [9.676, 56.08, 73.64], [9.81, 56.0, 74.19], [9.943, 55.83, 74.61], [10.077, 55.61, 74.9], [10.21, 55.52, 75.43], [10.344, 55.5, 75.86], [10.477, 55.44, 76.26], [10.611, 55.62, 76.67], [10.744, 55.18, 77.12], [10.878, 54.63, 77.33], [11.011, 54.45, 77.62], [11.144, 54.24, 78.14], [11.278, 54.6, 78.82], [11.411, 55.55, 79.41], [11.545, 56.15, 79.63], [11.678, 56.45, 80.02], [11.812, 56.58, 80.38], [11.945, 56.66, 80.67], [12.079, 56.17, 81.53], [12.212, 55.83, 82.54], [12.346, 55.35, 83.01], [12.479, 55.07, 83.56], [12.613, 55.0, 83.91], [12.746, 54.87, 84.69], [12.88, 54.83, 85.25], [12.98, 54.77, 85.64]], 'v7': [[6.94, 48.84, 40.68], [7.241, 48.77, 40.33], [7.407, 48.75, 40.19], [7.541, 49.09, 42.96], [7.674, 48.88, 43.22], [7.808, 48.73, 43.85], [7.941, 48.65, 44.3], [8.075, 48.82, 44.72], [8.208, 48.9, 45.01], [8.342, 48.83, 45.4], [8.475, 48.85, 46.01], [8.609, 48.88, 46.43], [8.742, 48.94, 46.59], [8.876, 49.07, 47.18], [9.009, 49.21, 47.47], [9.142, 49.21, 47.85], [9.276, 49.45, 47.87], [9.409, 49.68, 48.18], [9.543, 49.82, 48.64], [9.676, 49.86, 49.17], [9.81, 49.83, 49.84], [9.943, 49.97, 50.24], [10.077, 50.23, 50.53], [10.21, 50.63, 50.6], [10.344, 50.44, 51.28], [10.477, 50.98, 51.28], [10.611, 51.04, 51.83], [10.744, 51.09, 51.99], [10.878, 51.35, 52.55], [11.011, 51.69, 52.96], [11.144, 51.84, 53.22], [11.278, 51.94, 53.33], [11.411, 51.99, 54.28], [11.545, 52.12, 54.69], [11.678, 52.38, 55.03], [11.812, 52.67, 55.44], [11.945, 52.91, 55.79], [12.079, 53.08, 55.76], [12.212, 53.11, 56.98], [12.346, 53.43, 57.02], [12.479, 53.77, 56.7], [12.613, 54.06, 57.46], [12.746, 54.81, 57.82], [12.88, 55.57, 58.08], [12.98, 55.62, 58.86]], 'v8': [[7.941, 87.36, 58.84], [8.075, 87.55, 59.11], [8.208, 87.38, 59.24], [8.642, 85.7, 60.15], [8.775, 84.26, 60.43], [8.909, 83.7, 61.1], [9.042, 84.1, 61.08], [9.176, 84.07, 61.45], [9.309, 83.44, 62.2], [9.443, 83.31, 61.18], [9.576, 83.06, 61.37], [9.71, 82.78, 61.4], [9.843, 82.42, 61.92], [9.977, 82.14, 62.36], [10.11, 81.83, 62.44], [10.244, 81.61, 62.62], [10.344, 81.41, 62.65]], 'v9': [[8.976, 70.56, 63.62], [9.142, 71.22, 64.31], [9.276, 71.83, 64.99], [9.409, 72.37, 65.56], [9.543, 73.0, 66.34], [9.676, 73.56, 67.02], [9.81, 74.17, 67.67], [9.943, 74.75, 68.38], [10.077, 75.39, 69.16], [10.21, 75.99, 69.82], [10.344, 76.58, 70.39], [11.745, 82.43, 77.27], [11.879, 82.97, 78.07], [12.012, 83.58, 78.73], [12.145, 84.22, 79.39], [12.279, 84.81, 80.15], [12.412, 85.46, 80.82], [12.546, 86.12, 81.59], [12.679, 86.79, 82.26], [12.813, 87.44, 83.05], [12.946, 88.1, 83.83], [12.98, 88.29, 83.97]], 'v10': [[8.976, 61.69, 54.63], [9.142, 61.98, 55.13], [9.276, 61.95, 55.39], [9.409, 62.56, 55.69], [9.543, 62.47, 56.48], [9.676, 63.4, 56.19], [9.81, 63.26, 56.26], [9.943, 63.74, 55.75], [10.077, 64.01, 56.47], [10.21, 64.56, 56.23], [10.344, 64.64, 56.65], [10.477, 64.8, 56.98], [10.611, 65.66, 56.26], [10.744, 65.46, 57.8], [10.878, 66.18, 59.86], [11.011, 66.79, 60.15], [11.144, 67.19, 59.85], [11.278, 67.56, 59.94], [11.411, 67.8, 60.44], [11.545, 67.72, 60.98], [11.678, 67.81, 61.05], [11.812, 68.49, 61.12], [11.945, 68.54, 61.07], [12.079, 69.4, 61.42], [12.212, 69.41, 61.95], [12.346, 69.66, 62.49], [12.479, 70.08, 63.01], [12.613, 70.36, 63.37], [12.746, 70.22, 63.89], [12.88, 70.72, 64.23], [12.98, 70.81, 64.74]]}

PAGES = [
    # ---------------- MARKETS ----------------
    {
        "path": "markets/homeland-security-law-enforcement/",
        "category": "MARKETS",
        "related_key": "markets",
        "photo": "cctv.jpg",
        "photo_alt": "",
        "video": "border-checkpoint.mp4",
        "video_poster": "cctv.jpg",
        "plate_tracks": HOMELAND_PLATE_TRACKS,
        "title": "Helping Secure The Nation",
        "subhead": "Our expertise and world-class security solutions play an important role in helping the Department of Homeland Security meet its mission of ensuring that the nation is safe, secure, and resilient against terrorism and other hazards.",
        "meta": "Sentrillion's DHS-certified physical security solutions provide frontline security along U.S. borders, seaports, and airports.",
        "blocks": [
            {"type": "detail", "items": [
                {"num": "01", "heading": "Improving Border Security", "body": [
                    "Sentrillion has partnered with United States Customs and Border Protection (CBP) for more than 22 years. Our DHS-certified and accredited physical security solutions provide frontline security along the U.S. northern and southern land ports of entry, as well as seaports and airports, and integrate on local, regional, and national levels.",
                    "We have also partnered with CBP to develop new solutions that maximize efficiency and security while cutting costs &mdash; including templates that standardize security technology and processes for different types of security situations, and a system that uses biometric verification to enable trusted travelers to legally cross the border without requiring a CBP officer to be physically present.",
                ]},
                {"num": "02", "heading": "Other Homeland Security Solutions", "body":
                    "Sentrillion also provides services to other Homeland Security agencies. Our solutions protect DHS's National Biodefense Analysis and Countermeasures Center at Fort Detrick, Maryland, and our physical security solutions are applicable to other agencies, such as the Transportation Security Administration."
                },
            ]},
        ],
    },
    {
        "path": "markets/defense/",
        "category": "MARKETS",
        "related_key": "markets",
        "photo": "radar.jpg",
        "photo_alt": "",
        "title": "Mission Tested",
        "subhead": "Sentrillion provides integrated technology products and services that are critical to national security. Our innovative solutions play a vital role in helping our defense customers meet both mission and budgetary requirements.",
        "meta": "Integrated physical security, surveillance, and logistics support for military installations and defense missions.",
        "blocks": [
            {"type": "detail", "items": [
                {"num": "01", "heading": "Protection of Military Facilities", "body": [
                    "Our premier physical security solutions protect essential government facilities and assets. Whether it's a large military installation, a government building or campus, or a classified facility, we deliver tailored solutions built on the latest video and audio surveillance, intrusion detection, and access control technology.",
                    "An example of our physical security prowess is our installation at the Fort Huachuca Army Base, where we provide networked video surveillance at entry/access control points and key facilities throughout the base, a Sentrillion-designed command and control center, a visitor management system, and around-the-clock technical support.",
                ]},
                {"num": "02", "heading": "Integrated Logistics Support", "body": [
                    "Sentrillion's integrated logistics support (ILS) provides a cost-effective way to balance performance, affordability, and mission needs. Our qualified pool of skilled engineers, project managers, programmers, technicians, and systems administrators work side by side with our customers as part of their team &mdash; including at the Army Research Laboratory Defense Supercomputing Resource Center and the Naval Aviation Logistics Command Management Information System.",
                    "More than 30 percent of our employees are military veterans, and 85 percent hold security clearances.",
                ]},
            ]},
            {"type": "cta_row", "items": [
                ("View Identity &amp; Access Management", "../../capabilities/identity-access-management/"),
                ("View Engineering &amp; Integration", "../../capabilities/engineering-integration/"),
            ]},
        ],
    },
    {
        "path": "markets/transportation-civilian/",
        "category": "MARKETS",
        "related_key": "markets",
        "photo": "cargo-port.jpg",
        "photo_alt": "",
        "video": "gantry-crane.mp4",
        "video_poster": "cargo-port.jpg",
        "scan_line": True,
        "title": "On The Go, Because You Are On The Go",
        "subhead": "Sentrillion delivers integrated security, IT, and cyber capabilities that keep the transportation sector safe, resilient, and operational &mdash; from bustling airports to remote shipping yards.",
        "meta": "Integrated security, IT, and cyber capabilities for aviation, transit, seaports, and commercial infrastructure.",
        "blocks": [
            {"type": "detail", "items": [
                {"num": "01", "heading": "Airports &amp; Aviation", "body":
                    "We support the full aviation ecosystem with secure IT networks, cyber monitoring, access control, and surveillance solutions that keep passengers safe and operations compliant with federal and international standards."},
                {"num": "02", "heading": "Bus &amp; Rail Stations", "body":
                    "Public transit systems require constant vigilance. Sentrillion provides surveillance, intrusion detection, help desk support, and integrated monitoring to ensure safety in high-volume passenger hubs."},
                {"num": "03", "heading": "Seaports &amp; Terminals", "body":
                    "From large-scale cargo operations to specialized freight facilities, we safeguard supply chains with access management, cyber defense, and perimeter monitoring that prevent disruption and theft."},
            ]},
            {"type": "break", "tag": "COMMERCIAL", "text": "Meeting Vital Business Challenges &mdash; Sentrillion's physical and telecommunications solutions provide important benefits for a wide range of commercial and industrial customers, forged from nearly 25 years of addressing security and technology challenges."},
            {"type": "detail", "items": [
                {"num": "04", "heading": "Protecting Vital Assets", "body":
                    "Our specialized expertise and physical security solutions protect assets, prevent business and service interruption, and ensure the safety of personnel. These hardened solutions are scalable across a wide range of industrial and critical infrastructure segments. We also provide integrated logistics support and innovative staffing solutions for commercial organizations, including government vendors and security companies."},
            ]},
            {"type": "spec_list", "heading": "Critical infrastructure segments we serve", "items": [
                "Power", "Oil and gas", "Chemical", "Critical manufacturing", "Dams", "Energy", "Nuclear", "Transportation",
            ]},
            {"type": "cta", "label": "View Engineering &amp; Integration", "href": "../../capabilities/engineering-integration/"},
        ],
    },
    {
        "path": "markets/international/",
        "category": "MARKETS",
        "related_key": "markets",
        "photo": "earth-night.jpg",
        "photo_alt": "",
        "title": "Global Reach, Local Expertise",
        "subhead": "Sentrillion delivers trusted solutions across borders, cultures, and environments. Whether it's supporting international airports, securing borders, or deploying advanced IT systems for partner nations, our teams are equipped to operate seamlessly anywhere in the world.",
        "meta": "Scalable, trusted security and IT deployments for partner nations and international missions worldwide.",
        "blocks": [
            {"type": "detail", "items": [
                {"num": "01", "heading": "Scalable and Flexible Deployment", "body":
                    "Our programs are designed with agility in mind &mdash; enabling us to mobilize quickly, integrate with host-nation systems, and adapt to regional requirements. From high-security urban facilities to remote field operations, we bring the same proven processes and disciplined execution."},
                {"num": "02", "heading": "Trusted Partnerships", "body":
                    "With a global network of technology partners and local allies, Sentrillion ensures projects are delivered on time, on budget, and to the highest standards of quality and compliance."},
                {"num": "03", "heading": "Why It Matters", "body":
                    "An example of our physical security prowess is our installation at the Fort Huachuca Army Base, where we provide networked video surveillance at entry/access control points and key facilities throughout the base, a Sentrillion-designed command and control center, a visitor management system, and around-the-clock technical support."},
            ]},
        ],
    },
    # ---------------- CAPABILITIES ----------------
    {
        "path": "capabilities/operations-field-support/",
        "category": "CAPABILITIES",
        "related_key": "capabilities",
        "photo": "technician.jpg",
        "photo_alt": "",
        "title": "Operations &amp; Field Support",
        "subhead": "We deliver flexible, responsive teams that provide capabilities, expertise, and a unified approach to solving multifaceted challenges.",
        "meta": "24x7x365 help desk, field support, corrective maintenance, and program management from a nationwide cadre of technicians.",
        "blocks": [
            {"type": "detail", "items": [
                {"num": "01", "heading": "Corrective Maintenance", "body":
                    "Corrective maintenance often means urgent attention is required to troubleshoot and repair equipment quickly. Through a combination of our 24x7x365 Help Desk, our engineers, and certified technicians, Sentrillion can quickly triage issues &mdash; in many cases remotely &mdash; develop a plan for repair, and effect the repair efficiently. Our VAR relationships and industry connections let us address supply-chain issues in ways many competitors cannot."},
                {"num": "02", "heading": "24 X 7 X 365 Helpdesk", "body":
                    "Sentrillion's help desk delivers true around-the-clock support, every hour, every day of the year. Our U.S.-based Tier I&ndash;III support teams provide rapid resolution and exceptional customer care, integrating seamlessly with the customer's environment &mdash; ServiceNow, Maximo, Remedy, or homegrown ticketing systems &mdash; with proactive monitoring, fast escalation paths, and a culture built on accountability."},
                {"num": "03", "heading": "Field Support", "body":
                    "If we install it &mdash; or even if we didn't &mdash; you can rest assured we are here to support you and your equipment with field support expertise from our nationwide cadre of technicians, poised and ready to respond quickly and get you back into action."},
                {"num": "04", "heading": "Program and Project Management", "body":
                    "Effective, proven program and project management are often the most crucial implied tasks of any effort. Our certified program and project managers bring structured methodologies, clear communication, and disciplined execution to every engagement, from initiation and planning through delivery and sustainment."},
            ]},
        ],
    },
    {
        "path": "capabilities/it-cyber-services/",
        "category": "CAPABILITIES",
        "related_key": "capabilities",
        "photo": "cyber-ops.jpg",
        "photo_alt": "",
        "title": "IT &amp; Cyber Services",
        "subhead": "Sentrillion delivers comprehensive IT and cybersecurity solutions that protect critical infrastructure and sensitive data from evolving threats. Our full-spectrum services keep your networks secure, stable, and mission-ready.",
        "meta": "24x7 NOC/SOC monitoring, system integration, patching, and cloud support hardened for federal environments.",
        "blocks": [
            {"type": "detail", "items": [
                {"num": "01", "heading": "System Integration &amp; Upgrades", "body":
                    "We design and implement seamless integrations across diverse IT environments. From patching and software upgrades to complex system rollouts, our teams ensure mission-critical networks stay secure, stable, and optimized."},
                {"num": "02", "heading": "Enterprise IT Operations", "body":
                    "Sentrillion provides full-spectrum IT support, including configuration, deployment, and lifecycle management of hardware and software. We minimize downtime and maximize reliability through disciplined processes and proven tools."},
                {"num": "03", "heading": "Network &amp; Security Operations (NOC/SOC)", "body":
                    "Our Network and Security Operations Centers deliver 24&times;7 monitoring, threat detection, and incident response, combining human expertise with advanced analytics to keep networks resilient against outages and cyber threats."},
                {"num": "04", "heading": "Patching &amp; Vulnerability Management", "body":
                    "Regular updates and vulnerability remediation are essential to defending modern enterprises. Sentrillion ensures timely patching and compliance with federal and industry standards while minimizing disruption to operations."},
                {"num": "05", "heading": "Help Desk &amp; Field Support", "body":
                    "Our Tier I&ndash;III help desk resolves IT issues around the clock, while our field support teams deliver hands-on expertise for installations, troubleshooting, and on-site repairs."},
                {"num": "06", "heading": "Cloud &amp; Emerging Technology Support", "body":
                    "We support hybrid and cloud environments with secure migrations, integration of emerging technologies, and optimization for performance and cost."},
            ]},
        ],
    },
    {
        "path": "capabilities/engineering-integration/",
        "category": "CAPABILITIES",
        "related_key": "capabilities",
        "photo": "server-room.jpg",
        "photo_alt": "",
        "title": "Engineering &amp; Integration",
        "subhead": "Engineering and lab expertise on demand &mdash; end-to-end physical security and telecommunications solutions, engineered to spec.",
        "meta": "Staffing, engineering, CAD support, and a federally accredited IT lab behind every Sentrillion deployment.",
        "blocks": [
            {"type": "detail", "items": [
                {"num": "01", "heading": "Customer-Centric Staffing", "body":
                    "We take the time to understand your individual requirements and develop a staffing solution geared to your unique needs, drawing from a qualified pool of skilled engineers, project managers, programmers, technicians, and systems administrators available full-time, part-time, or as-needed. Our nationwide presence and extensive bandwidth make it possible to deploy resources quickly and handle contract surge requirements effectively."},
                {"num": "02", "heading": "Engineering Services", "body":
                    "Our engineering teams deliver end-to-end design, development, and deployment support for mission-critical IT systems &mdash; from requirements analysis to system architecture and implementation &mdash; ensuring solutions are reliable, scalable, and aligned with federal standards."},
                {"num": "03", "heading": "CAD Support &amp; System Design", "body":
                    "We leverage advanced Computer-Aided Design tools to model, plan, and document complex IT and security solutions, providing precise technical drawings, as-built documentation, and lifecycle updates that reduce costly design errors."},
                {"num": "04", "heading": "Federally Accredited IT Lab", "body":
                    "Our IT lab is federally accredited to validate, test, and certify solutions in secure environments before deployment &mdash; reducing deployment risk, accelerating timelines, and maintaining strict security standards."},
                {"num": "05", "heading": "Emerging Technologies", "body":
                    "Sentrillion leverages a vast network of partnerships to bring forward the most advanced innovations available today &mdash; from cutting-edge biometrics and next-generation detection systems to the power of artificial intelligence."},
            ]},
            {"type": "spec_list", "heading": "Sentrillion Integrated Logistics Support Services", "items": [
                "Product support management", "Design", "Engineering", "Supply support",
                "Maintenance planning &amp; management", "Packaging, handling &amp; transportation",
                "Technical data", "Support equipment", "Training", "Manpower and personnel",
                "Facilities and infrastructure", "Computer resources",
            ]},
        ],
    },
    {
        "path": "capabilities/identity-access-management/",
        "category": "CAPABILITIES",
        "related_key": "capabilities",
        "photo": "access-control.jpg",
        "photo_alt": "",
        "title": "Securing The Future",
        "subhead": "We provide integrated identity management and physical access control solutions designed to meet the stringent security and interoperability requirements of federal agencies &mdash; supporting PIV credentials and HSPD-12 compliance.",
        "meta": "Access control, intrusion detection, and biometric authentication built for CBP-accredited federal deployments.",
        "blocks": [
            {"type": "detail", "items": [
                {"num": "01", "heading": "Enterprise-Class Solutions", "body":
                    "We understand the importance of comprehensive security management. Our network-based physical security solutions can be implemented at a single facility, across a campus, throughout an organization, or nationwide."},
            ]},
            {"type": "spec_list", "items": [
                "Access control systems", "Intrusion detection systems", "Video and audio surveillance",
                "Barriers, gates, fences, bollards, and lighting", "Visitor management", "Network and communications platforms",
            ]},
            {"type": "detail", "items": [
                {"num": "02", "heading": "Cybersecure Technology", "body":
                    "Each of our systems is cybersecure, integrating best practices to balance security protection, performance, administration, and cost. We operate on the nation's most trusted networks, including DHS's secure network, and have completed CBP's stringent system accreditation process."},
                {"num": "03", "heading": "Full Lifecycle Support", "body":
                    "We back our solutions with full lifecycle support &mdash; from design and construction to installation and maintenance &mdash; with proven professionals concentrating on every aspect of the project to ensure maximum efficiency and superior outcomes."},
            ]},
            {"type": "spec_list", "heading": "Full lifecycle support", "items": [
                "Project management", "Design", "Engineering", "Installation", "Training", "Maintenance",
            ]},
        ],
    },
    # ---------------- CONTRACT VEHICLES ----------------
    {
        "path": "contracts/oasis-small-business/",
        "category": "CONTRACT VEHICLES",
        "related_key": "contracts",
        "photo": "capitol.jpg",
        "photo_alt": "",
        "title": "OASIS+ Small Business",
        "subhead": "A collection of multiple-award, Indefinite Delivery, Indefinite Quantity (IDIQ) contracts available to all federal agencies, including the Department of Defense and Federally Funded Research and Development Centers.",
        "meta": "Sentrillion's OASIS+ Small Business IDIQ contract details, awarded domains, and key features.",
        "blocks": [
            {"type": "spec_meta", "items": [
                ("Type", "Indefinite Delivery Indefinite Quantity (ID/IQ) Contract"),
                ("Contract No.", "47QRCA25DS647"),
                ("Client", "U.S. General Services Administration"),
            ]},
            {"type": "intro", "text": "OASIS+ is a collection of multiple-award, Indefinite Delivery, Indefinite Quantity (IDIQ) contracts, with a five-year base period and one five-year option period that may extend the cumulative ordering period to 10 years. Task orders can be awarded any time prior to the expiration of the ordering period of the master contracts."},
            {"type": "detail", "items": [
                {"num": "01", "heading": "Who Can Use It", "body":
                    "OASIS+ contracts may be used by all federal agencies, including the Department of Defense (DoD) and Federally Funded Research and Development Centers (FFRDCs), though they are not open to state and local governments at this time."},
                {"num": "02", "heading": "Awarded Domains", "body":
                    "Sentrillion holds awards across the Technical &amp; Engineering, Facilities, and Logistics domains &mdash; spanning engineering services, facilities support, security systems services, warehousing and storage, transportation support, and more."},
            ]},
            {"type": "spec_list", "heading": "Key Features", "items": [
                "Flexible/expandable domain-based structure", "Global access to commercial &amp; noncommercial structures",
                "No contract ceiling or cap on awards", "10-year period (5-year base + one 5-year option)",
                "Price evaluation at the contract level", "Task order solicitation through GSA eBuy",
            ]},
            {"type": "footnote", "text": "Have questions about our contract vehicles? Send an email to <a href=\"mailto:info@sentrillion.com\" style=\"color:var(--white)\">info@sentrillion.com</a>."},
        ],
    },
    {
        "path": "contracts/multiple-award-schedule/",
        "category": "CONTRACT VEHICLES",
        "related_key": "contracts",
        "photo": "mas-building.jpg",
        "photo_alt": "",
        "title": "GSA Multiple Award Schedule",
        "subhead": "The Federal Government's streamlined solution for purchasing products, services, and solutions at a fair and competitive cost.",
        "meta": "Sentrillion's GSA Multiple Award Schedule contract details and IT/Security offerings.",
        "blocks": [
            {"type": "spec_meta", "items": [
                ("Type", "Multiple Award Schedule"),
                ("Contract No.", "47QSMS25D002J"),
                ("Client", "U.S. General Services Administration"),
                ("Special Item Numbers", "334290, 334290L, 334512, 54130L, 54151S, OLM"),
            ]},
            {"type": "intro", "text": "Sentrillion provides Information Technology and Security and Protection offerings under the GSA MAS Schedule &mdash; giving federal buyers a streamlined, pre-competed path to our integrated security, IT, and cyber capabilities."},
            {"type": "footnote", "text": "Have questions about our contract vehicles? Send an email to <a href=\"mailto:info@sentrillion.com\" style=\"color:var(--white)\">info@sentrillion.com</a>."},
        ],
    },
    # ---------------- ABOUT ----------------
    {
        "path": "about/sentrillion-leadership/",
        "category": "ABOUT",
        "related_key": "about",
        "photo": "leadership.jpg",
        "photo_alt": "",
        "title": "Our Management Team",
        "subhead": "Leadership means more than direction. It's about empowering teams, inspiring innovation, and delivering results that matter &mdash; leaders who combine deep expertise across public and private sectors with strategic insight and operational precision.",
        "meta": "Meet the executive team leading Sentrillion's federal security, IT, and cyber programs.",
        "blocks": [
            {"type": "people", "items": [
                {"num": "01", "name": "Brannon Donlon", "role": "President", "photo": "leadership/brannon-donlon.jpg", "bio": "Leads the company's strategic direction, customer engagement, and delivery of mission-critical services for federal clients, overseeing Program Management, Business Development, Engineering, and Operations. Joined Sentrillion in 2016 with senior leadership experience at U.S. Customs and Border Protection and Fortune 500 companies."},
                {"num": "02", "name": "Katie Powers", "role": "President", "photo": "leadership/katie-powers.jpg", "bio": "Provides executive leadership for the company's strategic direction, financial performance, and long-term growth. More than 20 years of experience in finance, cost accounting, and government contracting."},
                {"num": "03", "name": "Bryan Ackerman", "role": "Chief Administration Officer", "photo": "leadership/bryan-ackerman.jpg", "bio": "Serves as a strategic advisor to the Executive Management Team, overseeing legal affairs, accounting, contracts administration, human resources, and quality management. More than 20 years in government contracts law and corporate governance."},
                {"num": "04", "name": "David Goldberg", "role": "Vice President, Delivery", "photo": "leadership/david-goldberg.jpg", "bio": "Leads execution of complex, mission-focused intelligence and operational programs for federal clients, with more than 25 years across the Intelligence Community, DHS, CBP, DIA, and FinCEN."},
                {"num": "05", "name": "Anthony &ldquo;Tony&rdquo; Holladay", "role": "Vice President, Operations", "photo": "leadership/tony-holladay.jpg", "bio": "Brings 30 years of law enforcement and executive leadership experience, including U.S. Air Force law enforcement, nearly 25 years with U.S. Border Patrol, and recognition as a DHS subject matter expert."},
                {"num": "06", "name": "Daniel Dreyfus", "role": "VP, Strategic Growth &amp; Business Development", "photo": "leadership/daniel-dreyfus.jpg", "bio": "Leads expansion initiatives, strategic partnerships, and solution development for government and international clients, specializing in border security, customs operations, and supply chain resilience."},
                {"num": "07", "name": "Kara Gates", "role": "Vice President, Finance", "photo": "leadership/kara-gates.jpg", "bio": "Responsible for the company's financial strategy, budgeting, reporting, and regulatory compliance, with deep expertise in financial controls, audit readiness, and FAR/CAS compliance."},
                {"num": "08", "name": "Deanna Lyons", "role": "Vice President, Human Resources", "photo": "leadership/deanna-lyons.jpg", "bio": "Leads the company's talent strategy, workforce planning, and HR operations, overseeing recruiting, compensation, benefits, and organizational development."},
                {"num": "09", "name": "Meghan Thomas", "role": "Vice President, Engineering", "photo": "leadership/meghan-thomas.jpg", "bio": "Responsible for engineering strategy, resource management, and execution of complex security and surveillance programs supporting DoD and DHS missions, with more than 20 years in electrical and data systems design."},
            ]},
        ],
    },
    {
        "path": "about/community-outreach/",
        "category": "ABOUT",
        "related_key": "about",
        "photo": "community-outreach.jpg",
        "photo_alt": "",
        "title": "Giving Back",
        "subhead": "Sentrillion is committed to being a good corporate citizen and helping improve the communities in which we live and work &mdash; through outreach and giving programs, by partnering with community organizations, and through volunteering.",
        "meta": "Sentrillion's community sponsorships, including the Border Patrol Foundation and the American Foundation for Suicide Prevention.",
        "blocks": [
            {"type": "sponsors", "items": [
                {"num": "01", "heading": "Border Patrol Foundation", "logo": "border-patrol-foundation.png", "body":
                    "We are proud to be a National Sponsor supporting the Border Patrol Foundation (BPF). We deeply value BPF's mission to honor the memory of fallen U.S. Border Patrol agents and to provide meaningful support to their families. The Foundation's commitment to assisting Border Patrol employees and their loved ones during times of loss, injury, illness, and personal hardship reflects a profound dedication to service and compassion. Sentrillion's support helps ensure that these heroes and their families receive the care, resources, and recognition they deserve."},
                {"num": "02", "heading": "Crohn's &amp; Colitis Foundation", "logo": "crohns-colitis-foundation.jpg", "body":
                    "We are honored to be a Presenting Sponsor supporting the Crohn's &amp; Colitis Foundation. We proudly stand behind the Foundation's mission to cure Crohn's disease and ulcerative colitis, and to improve the quality of life for children and adults affected by these chronic conditions. Through its commitment to groundbreaking research, comprehensive education, and compassionate support services, the Foundation empowers patients and healthcare professionals alike. Sentrillion is grateful to contribute to this vital work and help advance hope, healing, and progress."},
                {"num": "03", "heading": "American Foundation for Suicide Prevention", "logo": "afsp.png", "body":
                    "We are a proud supporter of the American Foundation for Suicide Prevention (AFSP). We stand with AFSP in its mission to provide a nationwide community for those affected by suicide&mdash;empowered by research, education, and advocacy. Suicide is a leading cause of death, and we are committed to helping take action through awareness, compassion, and support. Together, we can foster hope and healing."},
            ]},
        ],
    },
    # ---------------- CAREERS ----------------
    {
        "path": "careers/",
        "category": "CAREERS",
        "related_key": None,
        "photo": "careers.jpg",
        "photo_alt": "",
        "title": "Exciting Opportunities. Important Work.",
        "subhead": "We are looking for talented people who want to become part of an exciting company and a winning team.",
        "meta": "Careers at Sentrillion: benefits, culture, and what it's like to join Team Sentrillion.",
        "blocks": [
            {"type": "spec_list", "items": [
                "Join an organization that values people, promotes teamwork, and encourages a healthy work-life balance",
                "Do interesting and important work that contributes to the well-being of the nation",
                "Take advantage of advancement, career growth, and training opportunities",
            ]},
            {"type": "detail", "items": [
                {"num": "01", "heading": "Join Team Sentrillion", "body":
                    "We offer our employees competitive compensation, vacation, and benefits, along with a fast-paced and exciting work environment with opportunities nationwide. If you're interested in a career where you can grow personally and professionally while making a difference, we invite you to consider joining Team Sentrillion."},
                {"num": "02", "heading": "We&rsquo;ve Got You Covered", "body":
                    "Our benefits include health, dental, and vision coverage; life and AD&amp;D insurance; long- and short-term disability insurance; a health care flexible spending account; a 401(k) plan with match; education and training/certificate reimbursement; and paid time off, holidays, jury duty, bereavement, and qualified military leave."},
                {"num": "03", "heading": "Culture of Commitment", "body": [
                    "Corporate culture is one of the most important factors in any career decision. At Sentrillion, we foster a culture of collaboration, respect, uncompromising performance, and pride in accomplishing our mission &mdash; with transparency as one of our defining principles.",
                    "We're a family-oriented company where people care about each other, and a number of employees have been with us for more than a decade.",
                ]},
            ]},
            {"type": "cta", "label": "Get in Touch", "href": "../#contact"},
            {"type": "footnote", "text": "Sentrillion is an Equal Opportunity employer. All qualified applicants will receive consideration for employment without regard to race, color, religion, sex, sexual orientation, gender identity, national origin, disability, or status as a protected veteran."},
        ],
    },
]


def main():
    for page in PAGES:
        render_page(page)


if __name__ == "__main__":
    main()
