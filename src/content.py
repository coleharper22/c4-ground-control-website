# -*- coding: utf-8 -*-
"""
Every fact and every word of the C4 website lives here.
Change something in this file, run build.py, and the site updates.
Nothing else needs touching.
"""

# ---------------------------------------------------------------- the business

BIZ = {
    "name":        "C4 Ground Control",
    "legal":       "C4 Ground Control LLC",
    "phone":       "(407) 974-5864",
    "phone_href":  "+14079745864",          # what the click-to-call button dials
    "email":       "info@c4groundcontrol.com",
    "address":     "1173 Butler Way, Sanford, FL 32773",
    "license":     "SCC131154133",
    "license_kind": "Florida Irrigation Contractor",
    "facebook":    "https://www.facebook.com/109579671686251",
    "google_maps": "https://maps.google.com/maps?cid=462736651129528887",
    "tagline":     "Landscaping & irrigation across Central Florida",
    "founded":     2022,
}

HOURS = [
    ("Monday – Friday", "8:00am – 6:00pm"),
    ("Saturday",        "8:00am – 2:00pm"),
    ("Sunday",          "Closed"),
]

AREAS = [
    "Orlando", "Sanford", "Oviedo", "Winter Springs", "Apopka", "Ocoee",
    "Alafaya", "Kissimmee", "Deltona", "Titusville", "Chuluota", "Geneva",
]

# ------------------------------------------------------------------- the pitch

# Which photograph sits behind the homepage headline. Set to a filename from
# ~/organization-agent/website-backup/2026-08-07/images/ to choose deliberately,
# or None to let build.py take the first residential gallery shot.
HERO_PHOTO = None

HERO = {
    "headline": "Irrigation and landscaping done right the first time.",
    "sub": (
        "Licensed irrigation contractors serving Orlando, Sanford and the rest of "
        "Central Florida. Sprinklers, sod, drainage, plantings and lighting — "
        "installed by the crew that shows up when it says it will."
    ),
}

ABOUT = (
    "C4 Ground Control is a licensed irrigation and landscaping contractor based in "
    "Sanford, Florida. We install and repair sprinkler systems, lay sod, solve drainage "
    "problems, build out plantings and beds, and light it all up when the sun goes down.",

    "Central Florida soil is sandy, the rain comes all at once, and half the lawns "
    "around here are fighting a losing battle against both. Most of what we get called "
    "for comes down to water — too much of it in the wrong place, or not enough of it "
    "reaching the roots. That is the part we are actually licensed for, and it is the "
    "part most landscapers guess at.",

    "We work on residential and commercial property, we carry insurance, and estimates "
    "are free. If you want it done once and done properly, give us a call.",
)

WHY = [
    ("Licensed irrigation contractor",
     f"Florida license {BIZ['license']}. Sprinkler work is regulated for a reason — "
     "bad backflow protection puts your drinking water at risk. Ask anyone bidding "
     "your job for their license number."),
    ("We show up",
     "You get a real window, and we call if anything moves. No waiting around all day "
     "for a truck that never comes."),
    ("Free estimates, straight pricing",
     "We walk the property, tell you what it needs, and put a number on it. No "
     "pressure and no surprise line items at the end."),
    ("Local and small on purpose",
     "Based in Sanford, working Central Florida. The person who quotes your job is the "
     "person responsible for it."),
]

# ----------------------------------------------------------------- the services
# `photos` maps to the source page in the website backup, so each service page
# gets the real photographs of that actual work.

SERVICES = [
    {
        "slug": "irrigation",
        "name": "Irrigation System Design & Install",
        "short": "Sprinkler systems designed, installed and repaired",
        "photos": "service-irrigation.html",
        "blurb": (
            "New systems designed around your actual property, and repairs on systems "
            "that were never designed at all."
        ),
        "body": (
            "A sprinkler system is only as good as its layout. We design around your "
            "property's real zones — sun, shade, slope, soil and what is actually "
            "planted where — so every head is doing useful work instead of watering "
            "the driveway.",

            "We install new systems from scratch and we fix existing ones: broken and "
            "buried heads, cracked lines, valves that will not close, controllers "
            "nobody has been able to program in years, and backflow devices that need "
            "to be brought up to code.",

            "If your water bill climbed or you have got one green stripe and one brown "
            "stripe across the same lawn, that is a coverage problem and it is fixable.",
        ),
        "bullets": [
            "New system design and installation",
            "Repairs: heads, valves, lines, controllers",
            "Zone and coverage corrections",
            "Backflow protection to code",
            "Drip irrigation for beds and plantings",
            "Rain sensors and smart controllers",
        ],
    },
    {
        "slug": "sod",
        "name": "Sod Install",
        "short": "New lawns, laid on ground that was prepared properly",
        "photos": "service-sod.html",
        "blurb": (
            "Fresh sod on properly prepped ground — the prep is what decides whether "
            "it takes."
        ),
        "body": (
            "Sod fails for boring reasons: it went down on compacted ground, on old "
            "dead grass nobody stripped, or in a yard with no working irrigation to "
            "keep it alive through the first three weeks.",

            "We strip what is there, grade it, prepare the soil and lay tight seams so "
            "you are not left with a grid of brown lines. Then we make sure water can "
            "actually reach it — which is why sod and irrigation usually get quoted "
            "together.",

            "We work in St. Augustine, Bahia, Zoysia and Bermuda, and we will tell you "
            "honestly which one suits your light and your watering situation instead of "
            "selling you whatever is cheapest on the truck.",
        ),
        "bullets": [
            "Old lawn removal and haul-off",
            "Grading and soil preparation",
            "St. Augustine, Bahia, Zoysia, Bermuda",
            "Tight-seam installation",
            "Watering schedule for establishment",
            "Full or partial replacement",
        ],
    },
    {
        "slug": "landscaping",
        "name": "Landscaping Installations",
        "short": "Plantings, beds, borders and full landscape builds",
        "photos": "service-landscaping.html",
        "blurb": (
            "Plants, beds and borders chosen for Florida heat — designed and installed "
            "start to finish."
        ),
        "body": (
            "Design and installation for front yards, back yards and whole properties: "
            "plant beds, trees and palms, shrub borders, mulch and rock, edging and "
            "curbing.",

            "Plant selection matters more here than most people expect. Something that "
            "thrives in a shaded Oviedo back yard will cook in full Kissimmee sun, and "
            "the wrong plant in the wrong spot means you are replacing it in two "
            "summers. We pick for the conditions you actually have.",

            "Every bed gets drip irrigation where it makes sense. New plantings need "
            "water at the root, not a sprinkler head throwing water at their leaves.",
        ),
        "bullets": [
            "Landscape design and layout",
            "Plant, shrub, tree and palm installation",
            "Bed construction, mulch and decorative rock",
            "Edging, borders and curbing",
            "Drip irrigation to new plantings",
            "Full property transformations",
        ],
    },
    {
        "slug": "drainage",
        "name": "Drainage System Install & Repair",
        "short": "Standing water, runoff and erosion, solved at the cause",
        "photos": "service-drainage.html",
        "blurb": (
            "French drains, catch basins and grading that move water away from your "
            "house instead of into it."
        ),
        "body": (
            "Central Florida gets its rain in short violent bursts, and sandy soil "
            "handles it fine until it hits a layer that does not. Then you have got a "
            "pond in the back yard, water pushing against your foundation, or a section "
            "of lawn washing out every August.",

            "We find where the water is actually going — which is rarely where people "
            "assume — and give it somewhere better to be. French drains, catch basins, "
            "channel drains, downspout extensions, dry wells and regrading.",

            "This is the work that protects everything else. Perfect sod over bad "
            "drainage is money spent twice.",
        ),
        "bullets": [
            "French drain installation",
            "Catch basins and channel drains",
            "Downspout and gutter tie-ins",
            "Regrading and swale work",
            "Erosion control",
            "Repairs to failed or clogged systems",
        ],
    },
    {
        "slug": "lighting",
        "name": "Outdoor Lighting",
        "short": "Low-voltage landscape and pathway lighting",
        "photos": "service-lighting.html",
        "blurb": (
            "Path, accent and uplighting that makes the property look finished after "
            "dark."
        ),
        "body": (
            "Low-voltage lighting laid out to show the property off rather than blind "
            "the neighbours: uplights on palms and specimen trees, path lights along "
            "walkways and drives, wash lighting on the front of the house, and lighting "
            "on patios and outdoor kitchens.",

            "Done well, lighting does two things at once — it makes the place look "
            "considerably more expensive than it did at 5pm, and it removes the dark "
            "corners around your house.",

            "LED fixtures on transformers and timers, wired below grade, with a layout "
            "planned before anything goes in the ground.",
        ),
        "bullets": [
            "Path and driveway lighting",
            "Tree and palm uplighting",
            "Facade and wash lighting",
            "Patio and outdoor kitchen lighting",
            "LED fixtures, transformers and timers",
            "Repairs to existing lighting",
        ],
    },
    {
        "slug": "site-prep",
        "name": "Site Prep & Cleanup",
        "short": "Clearing, grading and haul-off to get a site ready",
        "photos": "service-siteprep.html",
        "blurb": (
            "Clearing, grubbing, grading and haul-off — the work that has to happen "
            "before anything good can."
        ),
        "body": (
            "Lot clearing, brush and undergrowth removal, stump and root grubbing, "
            "rough and finish grading, and hauling the whole mess away.",

            "We do this ahead of our own installs and as standalone work for builders, "
            "property managers and owners with a lot that has got away from them.",

            "Grading is the part worth paying attention to. Get the fall right at this "
            "stage and drainage stops being a problem later, which is a great deal "
            "cheaper than fixing it after the sod is down.",
        ),
        "bullets": [
            "Lot clearing and brush removal",
            "Stump and root grubbing",
            "Rough and finish grading",
            "Debris haul-off and disposal",
            "Storm and overgrowth cleanup",
            "Commercial and builder site prep",
        ],
    },
    {
        "slug": "hydroseeding",
        "name": "Hydroseeding & Seed Planting",
        "short": "Seed coverage for large areas where sod is not practical",
        # No hydroseeding photos exist yet — borrow the site-prep set, which is the
        # same kind of open prepared ground. Replace once we shoot a seeding job.
        "photos": "service-hydroseeding.html",
        "photos_fallback": "service-siteprep.html",
        "blurb": (
            "Sprayed seed, mulch and tack — economical grass coverage over large or "
            "awkward ground."
        ),
        "body": (
            "Hydroseeding sprays a slurry of seed, mulch and tackifier over prepared "
            "ground. The mulch holds moisture and keeps the seed put while it "
            "germinates, which is what makes it work on slopes where loose seed would "
            "simply wash off.",

            "For big open areas — acreage, commercial lots, retention slopes, pasture — "
            "it covers far more ground per dollar than sod. It takes longer to look "
            "like a lawn, so it is the wrong choice for a small front yard and the "
            "right one for two acres.",

            "Tell us the area and what it is for and we will tell you straight whether "
            "seed or sod is the better buy.",
        ),
        "bullets": [
            "Large-area and acreage seeding",
            "Slope and retention-pond stabilisation",
            "Commercial and builder sites",
            "Erosion control seeding",
            "Overseeding thin turf",
            "Pasture and field seeding",
        ],
    },
]

# ------------------------------------------------------------------- galleries

GALLERIES = [
    ("residential", "Residential", "gallery-Residential.html"),
    ("commercial",  "Commercial",  "gallery-Commercial.html"),
]

FAQ = [
    ("Are estimates really free?",
     "Yes. We come out, walk the property, and give you a written number. There is no "
     "charge and no obligation."),
    ("Are you licensed and insured?",
     f"Yes — Florida irrigation contractor license {BIZ['license']}, and we carry "
     "liability insurance. We are happy to send proof of both before we start."),
    ("What areas do you cover?",
     "We are based in Sanford and work across Central Florida — Orlando, Oviedo, "
     "Winter Springs, Apopka, Ocoee, Kissimmee, Deltona, Titusville and the "
     "surrounding communities. Call and ask if you are not sure."),
    ("How soon can you get out here?",
     "Usually within a few days for an estimate. Emergency irrigation repairs — a "
     "line blowing water — we treat as same-day where we can."),
    ("Do you handle both residential and commercial?",
     "Both. Single-family homes through to commercial properties, HOAs and builder "
     "site work."),
    ("My sprinklers work but my grass is still patchy. What is going on?",
     "Almost always coverage rather than pressure. Heads get buried, knocked out of "
     "alignment, or were never spaced to overlap in the first place, so parts of the "
     "lawn get watered twice and parts get missed. It is a quick thing for us to "
     "diagnose in person."),
]
