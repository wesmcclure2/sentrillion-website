# Sentrillion — Redesign Concept

A concept redesign of [sentrillion.com](https://www.sentrillion.com), reimagined in the dark, mission-driven visual language of [endurion.com](https://www.endurion.com): black/charcoal base, a single crimson-red accent, oversized display type, numbered sections, thin hairline dividers, and a huge wordmark footer.

The site is a cinematic one-page **home** (`index.html`) plus **13 detail pages** underneath it — one per Market, Capability, Contract Vehicle, and About sub-topic, plus Careers — mirroring sentrillion.com's real multi-page structure. All of Sentrillion's real content is kept throughout. Every detail page reuses the homepage's exact nav/footer chrome and introduces one new Endurion-style component: a full-bleed photo hero with a giant title, a thick red divider bar, and a bracketed `[ CATEGORY ]` tag — the same pattern endurion.com uses on its own About and Careers pages — followed by numbered content blocks, spec lists, and a "more like this" strip linking to sibling pages.

No build step, no framework, no dependencies beyond a Google Fonts stylesheet. Pure HTML/CSS/JS so it's trivial to host, edit, or hand off. (`build_pages.py` is an optional authoring convenience that generates the 13 detail pages from structured content — see [Customizing](#customizing) — but the committed `.html` files work with nothing but a browser, same as the homepage.)

### Motion & effects

- **Preloader** — brief mark-and-progress-bar loader on first paint, then the hero reveals.
- **Split-text hero entrance** — headline words and eyebrow/sub-copy animate in on load, staggered.
- **Scroll reveal** — every section fades/slides in as it enters the viewport, staggered per item (via a `--i` inline custom property).
- **SVG icon draw-in** — the market icons trace themselves in with `stroke-dashoffset` the first time their card is revealed.
- **Count-up stats** — the impact-numbers row animates from 0 to its target value once scrolled into view.
- **Marquee ticker** — an infinite-scrolling strip of certifications/credentials below the hero (pauses on hover).
- **Cursor glow** — a soft red ambient light follows the pointer on desktop (skipped on touch devices).
- **Magnetic tilt cards** — capability, market, and contract-vehicle cards tilt subtly toward the cursor on hover.
- **Sliding nav underline** and a **nav bar that compacts** on scroll.
- **Hero parallax** — the hero background drifts slightly slower than scroll for depth.
- **Hero terrain flight** &mdash; the homepage opens on a live canvas animation (no video): a slow flight over procedurally generated terrain along the border (a red dashed line), with port-of-entry masts that occasionally fault (red pulse) and restore (green), plus a camera-style HUD with changing coordinates, heading, and a live status line. Headline: "The border never goes dark. Neither do we." It is labeled as an illustrative visualization and uses generic "POE 01"-style labels, never real port names. Code is the "Hero terrain flight" block at the end of `js/main.js`; it only animates while the hero is on screen and renders a single still frame under `prefers-reduced-motion`.
- **Hero targeting reticles** (retired) &mdash; the reticle code in `js/main.js` only runs if a `#heroTargets` element exists; the terrain hero doesn't include one, so the effect is off.
- **Market icon animations** — each of the four market icons has its own continuous ambient motion once its card scrolls into view: a slow opacity pulse (Homeland Security & Law Enforcement), a rotating radar sweep (Defense), streaming motion lines (Transportation & Commercial), and a spinning globe meridian (International).
- **Market card photography** — all four market cards now carry moody, duotone background photography (matching treatment: grayscale/contrast filter, dark gradient overlay, hover zoom) instead of just the first card.
- **Nav dropdowns** — Capabilities, Markets, Contract Vehicles, and About each reveal a dropdown of their detail pages on hover (desktop) or via a caret toggle that expands in place (mobile), while the label itself still jumps to that section of the homepage.
- **Inner-page hero** — every detail page opens with a full-bleed duotone photo, a giant title, a thick red accent bar, and a bracketed `[ CATEGORY ]` eyebrow tag, directly modeled on endurion.com's own About/Careers page hero pattern.
- **Numbered detail blocks & related-pages strip** — each detail page's content is broken into numbered sections (matching the site's existing numbering convention) and ends with a row of links to its sibling pages, with the current page highlighted.
- **Detail-page hero video** — the Homeland Security &amp; Law Enforcement and Transportation &amp; Commercial market pages play a muted, looping background video behind their hero (same duotone/grain treatment as the rest of the site) instead of a static photo: real CBP footage of vehicles crossing into the U.S. at the San Ysidro Port of Entry, and an aerial shot of a gantry crane moving a container at the Port of Baltimore, respectively. A page's `photo` still serves as the `<video>`'s poster frame and as the `prefers-reduced-motion` fallback. See the credits table below for sourcing, and `build_pages.py`'s `PAGES` list (the `video`/`video_poster` keys) to swap in a different clip for any page.
- **Container-tracking scan line** — on the Transportation &amp; Commercial page only (the `scan_line` page flag), a glowing red laser sweeps back and forth over just the one container being lifted on the crane's cables, not the whole scene. It's two nested, independently-timed CSS animations: an outer box (`.page-hero-scan-track`) drifts across the hero in a straight line matching that container's measured on-screen motion over the 8s clip, and the laser itself (`.page-hero-scan`) does its own faster back-and-forth sweep confined to that box, so the "scan" always rides along with the moving container. Hidden under `prefers-reduced-motion`. If the video clip is ever swapped out, `heroContainerTrack`'s two keyframes in `css/style.css` need re-measuring against the new footage.
- **Leadership hover-reveal portraits** — on the Sentrillion Leadership page, hovering (or tab-focusing, for keyboard users) over an executive's card fills the entire card with their real headshot from sentrillion.com (duotone-treated to match the site, name/role staying legible over a dark gradient, bio fading out) — see the credits table below. If a photo is ever missing for someone, the card falls back automatically to a generic placeholder silhouette rather than substituting a stock photo for a real person's likeness.
- **Plate-tracking laser dots** — on the Homeland Security &amp; Law Enforcement page only, a small glowing red dot rides on the plate/front-bumper of every moving (and parked) vehicle in the checkpoint footage &mdash; 10 vehicles in all, each one audited across its full time on screen. Unlike the Transportation page's scan line (a fixed CSS animation timed to the clip length), these dots are driven live from `video.currentTime` every frame (`js/main.js`, "Plate-tracking laser dots"), interpolating between real `[seconds, xPercent, yPercent]` waypoints traced from the actual footage (`HOMELAND_PLATE_TRACKS` in `build_pages.py`, extracted via OpenCV background-subtraction tracking, then every track audited by eye across its full lifespan) and mapped through the video's `object-fit: cover` crop &mdash; so each dot stays glued to its car at any viewport size and can never drift out of sync no matter how the clip loops. Hidden under `prefers-reduced-motion`. If the video clip is ever swapped out, `HOMELAND_PLATE_TRACKS` needs re-tracing against the new footage.
- **Operational Memory, The record in numbers, In the field** (homepage, between the trust bar and the capabilities section, and after capabilities) &mdash; three sections built around the "we know every camera's history" story. Operational Memory sets the headline over a slowly drifting topographic backdrop (contour paths generated offline and inlined as SVG, no image asset) next to a canvas "network console": sensor sites along a stylized border line fail, dispatch to an ops center, and restore, with a scrolling work-order log. It is explicitly labeled illustrative and uses invented site IDs, not operational data. The numbers wall replaces the old generic stats band; only "15+ years supporting CBP" is live, the other three show `##` with a "Pending" tag until real, releasable figures are supplied. In the field is a full-bleed, black-and-white (CSS `grayscale`/contrast filter, not a pre-processed file) silhouette shot of a technician in a cherry-picker bucket reaching up to a pole-top fixture against a storm sky (an unlicensed iStock comp for now, see credits), with a camera HUD whose reticle sits on the fixture, never on the worker. All classes are prefixed `om-`; the JS is the "Operational Memory" block at the end of `js/main.js` and pauses its animation when the console is off screen.

Everything respects `prefers-reduced-motion` (including pausing the hero video and falling back to its poster frame), and the desktop-only effects (cursor glow, tilt) check for a fine pointer / hover support so they never fire on mobile.

## Structure

```
index.html                                     Homepage — markup and content for every section
css/style.css                                  All styling (theme tokens live at the top of the file)
js/main.js                                     Scroll-reveal, mobile nav + dropdowns, hero video, hero reticles
build_pages.py                                 Optional generator for the 13 detail pages below (see Customizing)
assets/photos/                                 Stock photography (see credits below)
assets/video/                                  Hero background video, mp4 + webm (see credits below)

markets/homeland-security-law-enforcement/     Market detail page
markets/defense/                               Market detail page
markets/transportation-civilian/               Market detail page
markets/international/                         Market detail page
capabilities/operations-field-support/         Capability detail page
capabilities/it-cyber-services/                Capability detail page
capabilities/engineering-integration/          Capability detail page
capabilities/identity-access-management/       Capability detail page
contracts/oasis-small-business/                Contract vehicle detail page
contracts/multiple-award-schedule/             Contract vehicle detail page
about/sentrillion-leadership/                  Leadership bios (9 executives)
about/community-outreach/                      Community sponsorships
careers/                                       Careers / benefits / culture
```

Every folder above holds a single `index.html`, so links resolve cleanly whether the site is served locally, from GitHub Pages, or from any static host.

## Running it locally

No build tools needed. Either:

- Open `index.html` directly in a browser, or
- Serve it locally so relative paths behave exactly like production:
  ```bash
  python3 -m http.server 8000
  # then visit http://localhost:8000
  ```

## Customizing

- **Colors / fonts**: edit the `:root` variables at the top of `css/style.css` (`--red` is the single accent color used throughout).
- **Homepage copy**: all text lives directly in `index.html`, organized by `<section>` with a matching class name (`.hero`, `.trust`, `.capabilities`, `.markets`, `.vehicles`, `.about`, `.cta`).
- **Detail-page copy**: each of the 13 pages under `markets/`, `capabilities/`, `contracts/`, `about/`, and `careers/` is a plain static `index.html` — edit any one directly. If you'd rather edit content in one place, `build_pages.py`'s `PAGES` list has the same content as structured Python data (title, subhead, numbered blocks, spec lists, etc.); edit an entry and re-run `python3 build_pages.py` to regenerate that page (it rewrites all 13 in place, so re-run after any edit to that file).
- **Icons**: the market icons are inline SVGs in `index.html` — swap the `<svg>` markup for your own line-art or an icon library.
- **Photography**: `assets/photos/` — swap any file for real Sentrillion photography (a facility, a team member, actual field/ops shots) and the existing grayscale/duotone CSS treatment (`.halftone-block img`, `.hero-bg-img`, `.about-bg img`, `.market-photo img`, `.page-hero-bg img`) will restyle it to match automatically — no other changes needed.
- **Hero**: the homepage hero is now the canvas terrain flight described above. The old desert flyover (`assets/video/border-flyover.{mp4,webm}`, with `hero-corridor.jpg` as its poster) is no longer referenced by the homepage but is kept in the repo in case you want it back.

### Photo & video credits

The placeholder photography and footage in `assets/photos/` and `assets/video/` are stock media, all free for commercial use with no attribution required:

| File | Source | License |
|---|---|---|
| `hero-corridor.jpg` (now used as the hero's poster/fallback frame), `server-room.jpg` | [pexels.com/photo/37730212](https://www.pexels.com/photo/data-center-server-racks-with-active-equipment-37730212/), [4508751](https://www.pexels.com/photo/server-racks-on-data-center-4508751/) | Pexels License |
| `cyber-ops.jpg` (homepage capabilities strip and the IT & Cyber Services page hero) | [dvidshub.net/image/6762557](https://www.dvidshub.net/image/6762557/uscybercom-integrated-intelligence-center-joint-operations-center) &mdash; official U.S. Cyber Command photo (by Josef Cole, Fort George G. Meade, MD, 04.02.2021) of the USCYBERCOM Integrated Intelligence Center / Joint Operations Center: a curved wall of cyber threat-map displays with an analyst silhouetted at a workstation. Went through two earlier replacements per feedback &mdash; first swapped an original "hooded hacker at a laptop" cliché for a real CDC operations-center photo (didn't land), then for this real USCYBERCOM photo (public domain, no identifiable faces, and genuinely cyber- rather than tactical/military-themed, which is why it was picked over an equally strong Combined Air Operations Center candidate). Cropped slightly to a 16:10 frame. | U.S. Government Work &mdash; public domain (17 U.S.C. &sect;105), no restrictions |
| `technician.jpg` | [pexels.com/photo/442150](https://www.pexels.com/photo/electronics-engineer-fixing-cables-on-server-442150/) | Pexels License |
| `canyon.jpg` (About section background) | [pexels.com/photo/976857](https://www.pexels.com/photo/grand-canyon-976857/) — Grand Canyon, by Josh Sorenson | Pexels License |
| `cctv.jpg` | [pexels.com/photo/9739769](https://www.pexels.com/photo/gray-cctv-camera-in-close-up-shot-9739769/) | Pexels License |
| `radar.jpg` (Defense market card) | [pexels.com/photo/38038508](https://www.pexels.com/photo/large-military-radar-system-against-clear-sky-38038508/) — Large Military Radar System against Clear Sky, by Magda Ehlers | Pexels License |
| `cargo-port.jpg` (Transportation & Commercial market card) | [pexels.com/photo/4570835](https://www.pexels.com/photo/aerial-photography-of-blue-and-red-cargo-containers-on-a-pier-4570835/) — aerial/drone shot of cargo containers at Barcelona's port, by James Heming | Pexels License |
| `earth-night.jpg` (International market page) | [pexels.com/photo/12990385](https://www.pexels.com/photo/planet-earth-in-black-background-12990385/) — Planet Earth in Black Background (night lights), by T Keawkanok | Pexels License |
| `capitol.jpg` (OASIS+ Small Business page) | [pexels.com/photo/32386662](https://www.pexels.com/photo/iconic-us-capitol-building-in-washington-dc-32386662/) — Iconic US Capitol Building in Washington DC | Pexels License |
| `mas-building.jpg` (GSA Multiple Award Schedule page) | [pexels.com/photo/17312238](https://www.pexels.com/photo/eisenhower-executive-office-building-in-washington-17312238/) — Eisenhower Executive Office Building in Washington, by Paige Thompson | Pexels License |
| `access-control.jpg` (Identity & Access Management page) | [pexels.com/photo/33335255](https://www.pexels.com/photo/modern-security-system-in-industrial-hallway-33335255/) — Modern Security System in Industrial Hallway, by Jakub Zerdzicki | Pexels License |
| `leadership.jpg` (Sentrillion Leadership page) | [pexels.com/photo/6949494](https://www.pexels.com/photo/businesspeople-at-conference-in-boardroom-6949494/) — Businesspeople at Conference in Boardroom, by Werner Pfennig | Pexels License |
| `community-outreach.jpg` (Community Outreach page hero) | [dvidshub.net/image/9814786](https://www.dvidshub.net/image/9814786/border-patrol-agent-works-campo-area-responsibility) — "Border Patrol Agent Works the Campo Area of Responsibility," a U.S. Border Patrol agent using binoculars to overlook the Campo Station area of responsibility and border wall near Tecate, Calif.; CBP photo by Jeff Underwood, U.S. Customs and Border Protection Office of Public Affairs, 06.26.2026 (VIRIN 260626-H-XI905-1107) | U.S. Government Work — public domain (17 U.S.C. &sect;105), no restrictions |
| `careers.jpg` (Careers page) | [pexels.com/photo/5256819](https://www.pexels.com/photo/coworkers-with-their-hands-together-5256819/) — Coworkers with Their Hands Together, by Thirdman | Pexels License |
| `leadership/*.jpg` (hover-reveal portraits on the Sentrillion Leadership page — Brannon Donlon, Katie Powers, Bryan Ackerman, David Goldberg, Tony Holladay, Daniel Dreyfus, Kara Gates, Deanna Lyons, Meghan Thomas) | Sentrillion's own company-published headshots, pulled from sentrillion.com/about/sentrillion-leadership/ and cropped square. These are real photos of Sentrillion's real employees, sourced from their own site — not stock photography standing in for anyone. `build_pages.py`'s `people` block falls back to `placeholder-person.svg` (a plain generic silhouette, no license needed) automatically for anyone whose photo file isn't present. | Sentrillion Corporation (company-published employee photos) |
| `logos/border-patrol-foundation.png`, `logos/crohns-colitis-foundation.jpg`, `logos/afsp.png` (sponsor logos on the Community Outreach page) | Each organization's own official logo, pulled directly from sentrillion.com/about/community-outreach/, where Sentrillion displays them to identify its real community sponsorships (Border Patrol Foundation, Crohn's &amp; Colitis Foundation, American Foundation for Suicide Prevention). Used here solely to identify these organizations, matching the real site's own usage — not decorative stock imagery. | Border Patrol Foundation, Crohn's &amp; Colitis Foundation, and American Foundation for Suicide Prevention, respectively (each organization's own trademarked logo) |
| `border-flyover.mp4` / `.webm` (hero background video) | [pixabay.com/videos/rock-formation-new-mexico-desert-43953](https://pixabay.com/videos/rock-formation-new-mexico-desert-43953/) — drone flyover of the badlands/rock formations of New Mexico, by mdherren; the full ~13.5s clip is used (no trimming), slowed to 0.625&times; speed (`setpts=1.6*PTS`, ~21.6s) per feedback that the original pace felt too fast for a hero background | Pixabay Content License |
| `border-checkpoint.mp4` / `.webm` (Homeland Security & Law Enforcement page hero video) | [dvidshub.net/video/970320](https://www.dvidshub.net/video/970320/b-roll-san-ysidro-port-entry-busiest-port-world) — "B-Roll: San Ysidro Port of Entry - The Busiest Port in the World," official U.S. Customs and Border Protection B-roll showing CBP officers and vehicle/pedestrian traffic entering the U.S. from Mexico at the actual San Ysidro Land Port of Entry; videographer Jeff Underwood, CBP Office of Public Affairs, 06.10.2025 (VIRIN 250610-H-XI905-1001); a ~13s segment (05:55&ndash;06:08) was trimmed, downscaled, and re-encoded with audio removed | U.S. Government Work — public domain (17 U.S.C. &sect;105), no restrictions |
| `field-silhouette.mp4` / `.webm`, `field-silhouette.jpg` (homepage "In the field" video and poster) | **iStock comp (watermarked preview), not yet licensed.** [istockphoto.com/video/...gm2156146404-576923762](https://www.istockphoto.com/video/silhouette-of-an-electrician-to-repair-street-lighting-gm2156146404-576923762) &mdash; a technician silhouetted in a cherry-picker bucket against a dramatic storm sky, reaching up to a pole-top fixture (stock title says street lighting; kept generic as "mast equipment" on the HUD for the same reason as earlier candidates). First 14s of the clip. Because the shot is already a high-contrast silhouette, it gets its own lighter CSS treatment (`.om-field--silo video { filter: grayscale(1) contrast(1.08); }`, no brightness cut) instead of the site's standard `.om-field video` filter, which crushed the storm clouds to near-black when tested against this footage; the source file itself is untouched color. The 768px watermarked comp is used as-is for internal review. iStock's terms allow comps only for test/sample layouts, not in final or publicly available materials, and only for 30 days after download (downloaded Sep 22, 2026). **Before this site goes public, license the clip and replace both files with the licensed download,** then remove the "iStock comp · license pending" line from `index.html`. Earlier candidates tried and replaced, kept here for reference: a technician installing a security camera from a cherry picker, [gm2259823804-672731115](https://www.istockphoto.com/video/technician-installing-a-security-camera-using-a-cherry-picker-bucket-truck-gm2259823804-672731115) (too soft-focus, worker mostly cropped out); a two-shot wide/close-up edit of a bucket-truck technician on a street-light-style fixture, [gm1481001553-508456645](https://www.istockphoto.com/video/worker-on-height-lifting-platform-installing-new-street-light-bulb-electrician-work-gm1481001553-508456645); a technician servicing a pole-mounted camera from the crossarm, [gm2233104192-648621721](https://www.istockphoto.com/video/electrician-and-engineer-checking-cctv-project-gm2233104192-648621721) (read as cleaning, not repair); and a lineman on a steel transmission tower, [gm2200421551-704957494 family](https://www.istockphoto.com/video/) (real electrical work, but the tower/PPE don't match a border-camera pole and would look like a different job site cut in). | iStock comp terms (pending license) |
| `gantry-crane.mp4` / `.webm` (Transportation & Commercial page hero video) | [pexels.com/video/6618019](https://www.pexels.com/video/aerial-shot-of-gantry-crane-lifting-cargo-container-6618019/) — aerial shot of a gantry crane moving cargo containers at the Port of Baltimore, by K; an 8s segment (00:13&ndash;00:21) was trimmed to the part where the suspended container is clearly visible and steadily in motion, downscaled, and re-encoded with audio removed | Pexels License |

Note on the hero video: no freely-licensed drone footage of the literal Rio Grande / border corridor could be sourced, so this uses New Mexico desert badlands footage instead — real U.S. Southwest terrain, with the camera genuinely flying forward over miles of eroded canyon country under a big, stormy sky, evoking a solitary reconnaissance/patrol flight rather than a vehicle or person as the subject. Earlier versions of this hero video were tried and replaced per feedback: first a lower, slower close-up of red-rock canyon walls (Arizona), then a vehicle crossing a desert plain (Tajikistan) — both read as "showcase" shots rather than a patrol flyover, so this New Mexico badlands clip replaces them with genuine forward/translational drone motion and no vehicle or person in frame. `capitol.jpg` was originally swapped out of the homepage's About section in favor of `canyon.jpg`; it's now back in use as the OASIS+ Small Business contract page's photo.

None of the *background* photography on the leadership, contract-vehicle, or capability pages depicts real Sentrillion people, facilities, or documents — it's stand-in stock photography chosen to match each page's subject, same as the rest of the site's imagery. The exceptions are the 9 hover-reveal portraits on the Leadership page itself, which are Sentrillion's own real, company-published employee headshots; the 3 sponsor logos on the Community Outreach page, which are the real organizations' own logos matching Sentrillion's actual sponsorships; and the Community Outreach page's hero photo itself, a real, official CBP/Border Patrol photograph (not generic stock) chosen to match its lead sponsorship, the Border Patrol Foundation (see the credits table above).

Treat these as placeholders for the pitch — swap in real Sentrillion photography/footage before this goes anywhere near production, both for authenticity and because none of these actually depict Sentrillion's people, facilities, or actual operating areas.

## Deploying to GitHub Pages

1. Push this repo to GitHub (see commands below).
2. In the repo on GitHub: **Settings → Pages → Source**, select the `main` branch and `/ (root)`, then save.
3. GitHub will publish it at `https://<your-username>.github.io/<repo-name>/` within a minute or two.

## Pushing this to your GitHub account

This folder is already a git repo with one commit made (`git log` will show it). From inside this project folder, just point it at your GitHub repo and push (replace `<your-username>` and `<repo-name>`):

```bash
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

If the repo doesn't exist on GitHub yet, create an empty one first — **no** README, license, or .gitignore (so it doesn't conflict with this push) — at `https://github.com/new`, then run the two commands above.

If you'd rather start totally fresh, delete the `.git` folder and re-run:

```bash
git init
git add .
git commit -m "Initial commit: Endurion-inspired Sentrillion redesign concept"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

---

*This is a concept/pitch redesign, not a drop-in replacement — it restyles Sentrillion's real content and page structure (a cinematic homepage plus 13 detail pages) into Endurion's dark, mission-driven visual language. Treat it as a visual direction to react to, not a final IA.*
