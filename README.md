# c4groundcontrol.com — the site we own

A replacement for the Topline Pro-hosted website. Plain static HTML: no framework,
no build tools, no external requests. Drop `build/` on any host and it works.

**Why this exists:** Topline hosts the current site and every edit goes through their
support team. This one lives here, and changes take seconds. See
`~/organization-agent/website-backup/` for the captured copy of the old site and the
full Topline ownership picture.

## Making changes

Everything you'd want to change is in **`src/content.py`** — phone number, address,
hours, service areas, service descriptions, FAQ, all of it. Edit that, then:

    python3 src/build.py

That regenerates `build/`. Nothing else needs touching.

To preview it:

    cd build && python3 -m http.server 8899

Then open <http://localhost:8899>.

## Layout

    src/content.py     every fact and every word — edit this
    src/build.py       the generator
    src/photo-map.json which photos appeared on which page of the old site
    assets/css/site.css the single stylesheet
    build/             the finished website (regenerated; safe to delete)

## How the photos work

Source images come from `~/organization-agent/website-backup/2026-08-07/images/` —
the 240 originals pulled off Topline's storage. `build.py` shrinks them with `sips`
(macOS built-in) into two sizes: 1600px for full view, 800px for thumbnails. 984 MB
of originals becomes about 47 MB of web images.

Photos are matched to services by which page of the old site they appeared on, so
irrigation photos land on the irrigation page and so on. That mapping is
`photo-map.json`. Hydroseeding has no photos of its own yet and borrows the site-prep
set — see `photos_fallback` in `content.py`; swap it out once we shoot a seeding job.

## What is deliberately different from the Topline site

The old copy was keyword-stuffed to the point of being misleading. The sod page
pushed "christmas lights installation near me" three times, and the homepage
advertised **stone veneer installation**, which C4 does not offer. Both are gone.
Google penalises that kind of stuffing, and advertising a service you don't provide
generates calls you have to turn away.

Also added, because they were missing and they matter for a licensed trade:

- The **license number** (`SCC131154133`) in the header, footer and every service page
- Click-to-call as the primary action everywhere, plus a sticky call bar on mobile
- `LandscapingBusiness` structured data for local search
- Honest service list — seven services, all of which C4 actually does

## Still open before this goes live

1. **Contact form.** There is none — the site drives calls, texts and email instead.
   A form needs somewhere to submit to; that is a small piece of work once we pick a
   host.
2. **Confirm the address.** The footer says 1173 Butler Way, Sanford. There is also a
   Chuluota address on file, and Cole asked Topline to fix a wrong address back in
   April. Worth confirming which is correct before publishing.
3. **Check it on a phone.** Built mobile-first but only verified on desktop.
4. **Hosting.** Not deployed anywhere yet. Deliberate — nothing points at this and
   the live site is untouched.

## Going live (do not skip the order)

1. Pick a host and deploy `build/` — verify it fully on the host's own URL first
2. In GoDaddy, change **only the A record** away from `34.48.158.255`.
   **Do not touch the MX records** or email breaks.
3. Only then cancel Topline — and keep their lead campaign running until a
   replacement source of leads is proven.
