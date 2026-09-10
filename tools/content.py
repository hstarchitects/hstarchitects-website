# -*- coding: utf-8 -*-
"""Single source of truth for every word, image and SEO field on hstarchitects.com.

SOURCING RULE
-------------
Everything factual on this site must be traceable to one of the two company
profile PDFs supplied by the client. Where a field is marked ``UNVERIFIED`` it is
deliberately left empty rather than filled with a plausible guess: no invented
dates, floor areas, prices, durations, project counts or client quotes.

If the studio can supply a figure, add it here and rebuild. Do not let marketing
copy assert something the sources do not support.

Edit copy here, then run `python tools/build_site.py` to regenerate the HTML.
"""

SITE = {
    "name": "HST Architects",
    "legal": "HST Group",
    "domain": "https://hstarchitects.com",
    "tagline": "Interior Design, Renovation & Landscaping in Dubai",
    "short_desc": (
        "HST Architects is a Dubai interior design, renovation and landscaping studio "
        "delivering villas, offices, showrooms and outdoor spaces across the UAE."
    ),
    # source: HST GROUP PROFILE p28 contact panel
    "phone_display": "+971 50 399 9314",
    "phone_link": "+971503999314",
    "landline_display": "+971 4 332 2002",
    "landline_link": "+97143322002",
    "email": "info@hstglobal.co",
    "address_line": "Boulevard Plaza Tower 1, Office 1603",
    "address_locality": "Downtown Dubai",
    "address_region": "Dubai",
    "address_country": "AE",
    # Boulevard Plaza Tower 1, Downtown Dubai
    "geo": {"lat": "25.1959", "lng": "55.2745"},
    # schema.org day tokens; a plain "Sa-Th" string is not parseable
    "hours_days": ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"],
    "hours_open": "09:00",
    "hours_close": "18:00",
    "hours_display": "Saturday to Thursday, 9am to 6pm",
    # every emirate/community named in the two source portfolios
    "areas": [
        "Dubai", "Downtown Dubai", "Business Bay", "Dubai Marina", "Emirates Hills",
        "Damac Hills", "District One", "Jumeirah", "Al Barsha", "Al Wasl", "Deira",
        "Abu Dhabi",
    ],
    "socials": {
        "instagram": "https://www.instagram.com/hst.arch",
    },
}

# --------------------------------------------------------------------------
# Navigation
# --------------------------------------------------------------------------
NAV = [
    {"label": "Home", "url": "/", "key": "home"},
    {"label": "Services", "url": "/services/", "key": "services", "children": [
        {"label": "Interior Design", "url": "/services/interior-design/", "key": "interior-design"},
        {"label": "Renovation & Fit-Out", "url": "/services/renovation/", "key": "renovation"},
        {"label": "Landscaping", "url": "/services/landscaping/", "key": "landscaping"},
    ]},
    {"label": "Projects", "url": "/projects/", "key": "projects"},
    {"label": "About", "url": "/about/", "key": "about"},
    {"label": "Contact", "url": "/contact/", "key": "contact"},
]

# --------------------------------------------------------------------------
# Services
#   Capabilities below are drawn from the two source service lists:
#   HST profile:      interior fit out, landscape, conceptual designing, annual
#              maintenance contracts, technical services, furniture, designing
#   Second profile:  design consultation, concept development & visualisation, space
#              planning, material selection & procurement, renovation &
#              construction management, custom furniture & millwork
# --------------------------------------------------------------------------
SERVICES = [
    {
        "key": "interior-design",
        "num": "01",
        "title": "Interior Design",
        "url": "/services/interior-design/",
        "short": "Concept, space planning and 3D visualisation for villas, offices and showrooms.",
        "hero_img": "services/interior-marble-lobby",
        "hero_alt": "Marble entrance lobby with symmetrical joinery and an inlaid stone floor",
        "card_img": "services/interior-curved-living",
        "card_alt": "Contemporary living room with a curved sculptural sofa and marble detailing",
        "seo_title": "Interior Design Company in Dubai | HST Architects",
        "meta": (
            "Interior design in Dubai: consultation, concept development, space planning, "
            "3D visualisation and custom furniture for villas, offices and showrooms."
        ),
        "intro": (
            "We start with how a space will actually be lived in or worked in, then work "
            "backwards through light, circulation, material and detail until the drawings are "
            "precise enough to build from. The team that draws them is the team that builds them."
        ),
        "lede": "Design detailed enough to build from.",
        "outcomes": [
            "A design language your brand or family recognises as theirs",
            "Drawings and schedules detailed enough to price and build accurately",
            "Material palettes chosen against Dubai's heat, humidity and light",
        ],
        "capabilities": [
            {"t": "Design Consultation",
             "d": "We work closely with you to understand the brief, your preferences and how you actually use the space."},
            {"t": "Concept Development & Visualisation",
             "d": "Ideas translated into detailed plans, mood boards and 3D renderings you can sign off before work begins."},
            {"t": "Space Planning & Layout",
             "d": "Circulation, zoning and furniture layouts optimised for how the space works through the day."},
            {"t": "Material Selection & Procurement",
             "d": "Stone, timber, metal and textile schedules sourced from trusted suppliers in the UAE and abroad."},
            {"t": "Custom Furniture & Millwork",
             "d": "Bespoke wardrobes, vanities, reception desks and feature panelling drawn to shop-drawing standard."},
            {"t": "Lighting & Furnishing",
             "d": "Layered lighting schemes plus furniture and fittings specified, procured and installed."},
        ],
        "process_note": "Programme depends on scope. We give you a written one after the first site visit.",
        "faqs": [
            {"q": "How much does interior design cost in Dubai?",
             "a": "It depends on the size of the property, the scope of work and the finish level, so we do not publish a "
                  "rate card. We visit the property first, agree the scope with you, and then issue a written fixed fee "
                  "rather than an open-ended hourly estimate."},
            {"q": "Do you work on apartments as well as villas?",
             "a": "Yes. Our portfolio includes apartment and penthouse redesigns in Dubai Marina alongside villa work in "
                  "Emirates Hills and Jumeirah, plus offices, showrooms and hospitality interiors."},
            {"q": "Can you take a project from design through to construction?",
             "a": "That is our default. HST Architects sits inside HST Group, a licensed building maintenance and "
                  "technical services company, so the team that draws the project also delivers it on site."},
            {"q": "Do you provide 3D renders before we commit?",
             "a": "Yes. Concept development includes detailed plans, mood boards and 3D renderings, so you approve the "
                  "finished look before procurement or demolition begins."},
        ],
        "gallery": [
            ("services/interior-curved-living", "Living room with a curved sofa, marble detailing and a full-height window"),
            ("services/interior-styled-living", "Styled living room with open shelving, layered textiles and warm accent lighting"),
            ("services/interior-kitchen-brass", "Kitchen with a stone island, brass pendants and handleless cabinetry"),
            ("services/interior-corridor-gold", "Feature corridor with concealed cove lighting in warm tones"),
            ("services/interior-bath-marble", "Bathroom clad in book-matched marble with a floating timber vanity"),
            ("services/interior-loft-living", "Loft-style living area with exposed brick, timber floors and linear seating"),
        ],
    },
    {
        "key": "renovation",
        "num": "02",
        "title": "Renovation & Fit-Out",
        "url": "/services/renovation/",
        "short": "Interior fit-out and refurbishment, delivered by the team that drew it.",
        "hero_img": "services/renovation-boardroom",
        "hero_alt": "Completed Dubai boardroom fit-out with a sculptural table and full-height glazing",
        "card_img": "services/renovation-loft-office",
        "card_alt": "Converted loft office with exposed brick, black steel framing and warm timber floors",
        "seo_title": "Renovation & Fit-Out in Dubai | HST Architects",
        "meta": (
            "Interior fit-out and renovation in Dubai: design implementation, construction "
            "management, joinery and technical services for villas and offices."
        ),
        "intro": (
            "Renovation is where design either survives or quietly disappears. HST Group holds a "
            "building maintenance and technical services licence and runs its own site teams, so "
            "the drawings, the joinery, the technical works and the finishing sit under one contract."
        ),
        "lede": "One contract. One team. One point of contact.",
        "outcomes": [
            "A single point of accountability from strip-out to snagging",
            "Full design implementation from final drawings, not a reinterpretation",
            "Programmes planned around occupied buildings where needed",
        ],
        "capabilities": [
            {"t": "Full Design Implementation",
             "d": "Execution of the approved design and drawings by our own team, from demolition through to handover."},
            {"t": "Renovation & Construction Management",
             "d": "Every stage of the renovation overseen in one programme, with progress reported to you as it moves."},
            {"t": "Interior Fit-Out",
             "d": "Partitions, ceilings, flooring, finishes and fixtures delivered as a single package."},
            {"t": "Technical Services",
             "d": "Building services and technical works handled through HST Group's licensed technical services division."},
            {"t": "Bespoke Joinery & Millwork",
             "d": "Wardrobes, kitchens, reception desks and feature panelling fabricated to the approved detail."},
            {"t": "Annual Maintenance Contracts",
             "d": "Post-handover AMC cover for residential and commercial buildings, on an annual or daily basis."},
        ],
        "process_note": "Programme depends on scope. We give you a written one after the first site visit.",
        "faqs": [
            {"q": "Do you handle the construction as well as the design?",
             "a": "Yes. Our comprehensive range of services covers full design implementation by our own team, based on the "
                  "final designs and drawings, so execution follows the design rather than reinterpreting it."},
            {"q": "How long does a villa renovation take in Dubai?",
             "a": "It depends entirely on scope. A single-room refresh and a full strip-out with structural alterations "
                  "are very different programmes. We issue a written programme after surveying the property rather than "
                  "quoting a generic timescale."},
            {"q": "Can you work in an occupied office or home?",
             "a": "Yes. We phase the works and seal off live zones so the space stays usable. Several of our office "
                  "projects were delivered in buildings that stayed in use throughout."},
            {"q": "Do you offer maintenance after the project is finished?",
             "a": "Yes. HST Group provides building maintenance and technical services to residential and commercial "
                  "buildings on an annual or daily operation basis, including annual maintenance contracts."},
        ],
        "gallery": [
            ("services/renovation-industrial-office", "Open-plan workspace with exposed services, timber desking and planting"),
            ("services/renovation-executive-office", "Executive office with a stone desk and floor-to-ceiling city views"),
            ("services/renovation-meeting-room", "Meeting room with a solid timber table, slatted acoustic wall and linear lighting"),
            ("services/renovation-loft-stairs", "Feature steel-and-timber staircase inside a converted industrial space"),
            ("services/renovation-office-seaview", "Refurbished office floor with glazed partitions and waterfront views"),
            ("services/renovation-progress-shell", "Renovation in progress, showing a stripped interior prepared for new works"),
        ],
    },
    {
        "key": "landscaping",
        "num": "03",
        "title": "Landscaping",
        "url": "/services/landscaping/",
        "short": "Gardens, terraces and outdoor rooms designed and built for the Gulf climate.",
        "hero_img": "services/landscape-villa-pool",
        "hero_alt": "Private villa garden at dusk with a lit pool, raised planters and mature palms",
        "card_img": "services/landscape-roof-garden",
        "card_alt": "Roof terrace lounge framed by planting and warm concealed lighting at night",
        "seo_title": "Landscaping Company in Dubai | HST Architects",
        "meta": (
            "Landscape design and construction in Dubai: villa gardens, roof terraces, pergolas, "
            "water features and planting schemes built for the Gulf climate."
        ),
        "intro": (
            "In Dubai a garden is only as good as the months it has to survive. We plan outdoor "
            "spaces around shade, planting and lighting first, so the space is genuinely usable "
            "through the cooler months and still holding together in the heat."
        ),
        "lede": "Outdoor rooms, planned for the climate.",
        "outcomes": [
            "Shade and circulation planned before planting",
            "Hard and soft landscaping detailed as one scheme",
            "Night lighting designed so the garden works after sunset",
        ],
        "capabilities": [
            {"t": "Landscape Design & 3D",
             "d": "Layouts, planting schemes and 3D visuals agreed before anything is dug."},
            {"t": "Garden & Terrace Construction",
             "d": "Level changes, paving, decking, raised planters and built-in seating delivered as one package."},
            {"t": "Pergolas & Shade Structures",
             "d": "Shade structures and outdoor kitchens built into the layout rather than added afterwards."},
            {"t": "Water Features",
             "d": "Reflection pools, cascade walls and water features integrated with the hardscape and lighting."},
            {"t": "Planting & Green Walls",
             "d": "Palms, specimen trees, green walls and ground cover chosen for heat and salinity tolerance."},
            {"t": "Irrigation & Garden Lighting",
             "d": "Irrigation, drainage and low-voltage garden lighting installed with the landscape."},
        ],
        "process_note": "Programme depends on scope. We give you a written one after the first site visit.",
        "faqs": [
            {"q": "Which plants actually survive a Dubai summer?",
             "a": "We build schemes around palms, frangipani, bougainvillea, ficus and hardy ground cover, backed by "
                  "irrigation. Anything specified outside that range is flagged with its real maintenance cost before "
                  "you sign it off."},
            {"q": "Do you design and build the landscape, or only design it?",
             "a": "Both. Our landscape work covers design through to construction, including hardscaping, planting, "
                  "shade structures, water features, irrigation and lighting."},
            {"q": "Can you landscape a roof terrace or balcony?",
             "a": "Yes. Roof terraces are some of our most requested work. The District One roof garden in our portfolio "
                  "is one example, and we check the building's constraints before designing around them."},
            {"q": "Do you offer garden maintenance after handover?",
             "a": "Yes, through HST Group's annual maintenance contracts, which cover residential and commercial "
                  "properties on an annual or daily basis."},
        ],
        "gallery": [
            ("services/landscape-hills-sculpture", "Finished villa garden with sculpture, lawn and mature planting"),
            ("services/landscape-hills-lawn", "Landscaped garden with a shade structure, outdoor kitchen and lawn"),
            ("services/landscape-pergola-lawn", "Pergola over an outdoor dining terrace beside a lawn"),
            ("services/landscape-garden-terrace", "Garden terrace with built-in seating, a barbecue counter and shade structure"),
            ("services/landscape-planters", "Raised planters with mature shrubs framing a private villa garden"),
            ("services/landscape-roof-garden", "Roof terrace lounge lit at night beneath planting"),
        ],
    },
]

# --------------------------------------------------------------------------
# Projects
#
#   year , only where the source profile states one; "" otherwise.
#   area , the sources give no floor areas, so this field is intentionally absent.
#   Every gallery image belongs to the project it sits under.
# --------------------------------------------------------------------------
PROJECTS = [
    # ---------- from the HST profile (years stated in the source) ----------
    {"slug": "springfield-office", "title": "Springfield Office",
     "cat": "Fit-Out", "service": "renovation", "year": "2020", "loc": "Business Bay, Dubai",
     "scope": "Office fit-out, reception joinery, finishes",
     "img": "projects/proj-springfield-sign",
     "alt": "Springfield office reception with a backlit timber feature wall carrying the company name",
     "blurb": "An office fit-out in Business Bay, built around a stone reception counter and a backlit timber signage wall.",
     "gallery": [("projects/proj-springfield-reception", "Reception counter in book-matched stone with warm concealed lighting"),
                 ("projects/proj-springfield-bar", "Kitchen bar with fluted timber panelling and counter stools"),
                 ("projects/proj-springfield-boardroom", "Boardroom with a stone table, joinery wall and integrated screen")]},

    {"slug": "floward-office", "title": "Floward Office",
     "cat": "Fit-Out", "service": "renovation", "year": "2021", "loc": "Business Bay, Dubai",
     "scope": "Office fit-out, joinery, planting, breakout spaces",
     "img": "projects/proj-floward-green",
     "alt": "Floward office reception with a living green wall and timber slat screening",
     "blurb": "A workplace fit-out built around a planted spine that runs from the reception desk to the far studio wall.",
     "gallery": [("projects/proj-floward-lounge", "Breakout lounge with a pool table, library shelving and planting"),
                 ("projects/proj-floward-studio", "Open studio floor with bench desking and glazed meeting rooms"),
                 ("projects/proj-floward-desk", "Reception area with the brand wall and planting behind")]},

    {"slug": "emirates-hills-villa", "title": "Private Villa, Emirates Hills",
     "cat": "Interior", "service": "interior-design", "year": "2022", "loc": "Emirates Hills, Dubai",
     "scope": "Interior design, bespoke joinery, furnishing, lighting",
     "img": "services/interior-bath-marble",
     "alt": "Villa bathroom clad in book-matched marble with a floating timber vanity",
     "blurb": "A private villa interior, detailed around stone, timber and layered lighting.",
     "gallery": [("services/interior-bath-green", "Bathroom in green marble with brass fittings and a walk-in shower"),
                 ("projects/proj-emirates-hills-shower", "Walk-in shower framed in black steel against veined stone")]},

    {"slug": "al-wasl-gym", "title": "Gym Renovation, Al Wasl",
     "cat": "Renovation", "service": "renovation", "year": "2023", "loc": "Al Wasl, Dubai",
     "scope": "Renovation, specialist flooring, technical services, equipment installation",
     "img": "projects/proj-gym-rigs",
     "alt": "Training floor with steel rigs, rubber flooring and exposed ceiling services",
     "blurb": "An interior taken back to structure and rebuilt as a training facility.",
     "gallery": [("projects/proj-gym-cardio", "Cardio zone with treadmills facing full-height glazing"),
                 ("projects/proj-gym-floor", "Free-weights floor with rubber matting and mirrored walls"),
                 ("projects/proj-gym-lounge", "Members lounge with a double-height void and feature stair")]},

    {"slug": "business-bay-private-office", "title": "Private Office, Business Bay",
     "cat": "Interior", "service": "interior-design", "year": "2023", "loc": "Business Bay, Dubai",
     "scope": "Interior design, joinery, lighting, furniture",
     "img": "services/renovation-executive-office",
     "alt": "Executive office with a stone desk and floor-to-ceiling views over Business Bay",
     "blurb": "A single-occupier office where the desk, the meeting room and the view were composed together.",
     "gallery": [("services/renovation-meeting-room", "Meeting room with a solid timber table and slatted acoustic walls"),
                 ("projects/proj-bb-pantry", "Concealed pantry run in dark stone with integrated appliances"),
                 ("projects/proj-bb-powder", "Powder room clad in figured marble with a floating basin")]},

    {"slug": "deira-private-office", "title": "Private Office, Deira",
     "cat": "Interior", "service": "interior-design", "year": "2018", "loc": "Deira, Dubai",
     "scope": "Interior design, reception joinery, lighting, furniture",
     "img": "projects/proj-office-reception",
     "alt": "Office reception with a backlit stone counter and warm timber flooring",
     "blurb": "The earliest project in this portfolio: a private office in Deira, detailed around a backlit stone reception.",
     "gallery": [("projects/proj-office-deira", "Waiting area with lounge seating and planting"),
                 ("projects/proj-office-deira-floor", "Open office floor with glazed offices along the window line")]},

    {"slug": "damac-hills-landscape", "title": "Villa Landscape, Damac Hills",
     "cat": "Landscape", "service": "landscaping", "year": "2023", "loc": "Damac Hills, Dubai",
     "scope": "Landscape design, pergola, planting, garden lighting, outdoor kitchen",
     "img": "services/landscape-pergola-lawn",
     "alt": "Villa garden with a pergola over an outdoor dining terrace beside a lawn",
     "blurb": "A villa plot laid out as three connected outdoor rooms: dining, lawn and a shaded lounge.",
     "gallery": [("services/landscape-garden-terrace", "Outdoor kitchen and barbecue counter under the pergola"),
                 ("services/landscape-planters", "Raised planters with mature shrubs along the boundary wall")]},

    # ---------- from the second profile (no dates stated in the source) ----------
    {"slug": "nbd-building-office", "title": "Office Renovation, NBD Building",
     "cat": "Fit-Out", "service": "renovation", "year": "", "loc": "Dubai",
     "scope": "Strip-out, partitions, ceilings, finishes",
     "img": "projects/proj-nbd-office",
     "alt": "Office floor with glazed partitions, linear lighting and neutral finishes",
     "blurb": "A whole-floor office refurbishment in the NBD Building.",
     "gallery": [("projects/proj-nbd-office-2", "Completed office floor with glazed offices and open desking")]},

    {"slug": "jumeirah-villa", "title": "Private Villa, Jumeirah",
     "cat": "Residential", "service": "renovation", "year": "", "loc": "Jumeirah, Dubai",
     "scope": "Villa renovation, interior design, joinery",
     "img": "services/interior-curved-living",
     "alt": "Villa living room with a curved sofa, marble detailing and full-height glazing",
     "blurb": "A private villa renovated and redesigned around a single open living floor.",
     "gallery": [("projects/proj-villa-jumeirah", "Villa interior with marble flooring and a double-height void")]},

    {"slug": "marina-penthouse", "title": "Penthouse Redesign, Dubai Marina",
     "cat": "Residential", "service": "interior-design", "year": "", "loc": "Dubai Marina",
     "scope": "Penthouse redesign, kitchen renovation, joinery, furnishing",
     "img": "projects/proj-penthouse-marina",
     "alt": "Penthouse kitchen with stone surfaces, dark joinery and concealed lighting",
     "blurb": "A marina penthouse redesigned and renovated, including a full kitchen replacement.",
     "gallery": [("services/interior-corridor-white", "Gallery corridor with an inlaid floor and linear lighting")]},

    {"slug": "ima-gallery-showroom", "title": "IMA Gallery Showroom",
     "cat": "Retail", "service": "interior-design", "year": "", "loc": "Art of Living Mall, Dubai",
     "scope": "Showroom design, display joinery, feature lighting, shopfront",
     "img": "projects/proj-ima-gallery",
     "alt": "IMA Gallery shopfront in polished stone with a backlit signage band",
     "blurb": "A jewellery-box shopfront: dark stone frame, bright interior, product as the only bright thing.",
     "gallery": [("projects/proj-ima-interior", "Gallery interior with sculptural display plinths and pendant lighting")]},

    {"slug": "gama-fashion-showroom", "title": "GAMA Fashion Showroom",
     "cat": "Retail", "service": "interior-design", "year": "", "loc": "Abu Dhabi",
     "scope": "Showroom design, display systems, lighting",
     "img": "projects/proj-gama-showroom",
     "alt": "Fashion showroom with marble flooring, brushed gold detailing and lounge seating",
     "blurb": "A fashion showroom in Abu Dhabi, laid out as a sequence of display rooms rather than a single floor.",
     "gallery": [("projects/proj-gama-retail", "Retail display run with timber shelving and integrated lighting")]},

    {"slug": "dng-furniture-showroom", "title": "DNG Furniture Showroom",
     "cat": "Retail", "service": "renovation", "year": "", "loc": "Al Barsha One, Dubai",
     "scope": "Showroom fit-out, lighting design, display systems",
     "img": "projects/proj-dng-furniture",
     "alt": "Furniture showroom with vignette settings, pendant lighting and a dark feature wall",
     "blurb": "A furniture showroom laid out as a sequence of rooms rather than a warehouse of stock.",
     "gallery": [("projects/proj-dng-progress", "The showroom during fit-out, before finishes were installed")]},

    {"slug": "mehr-o-mah-art-cafe", "title": "Mehr o Mah Art Café",
     "cat": "Hospitality", "service": "interior-design", "year": "", "loc": "Jumeirah 1, Dubai",
     "scope": "Café concept, joinery, lighting, planting, furniture",
     "img": "projects/proj-cafe-greenery",
     "alt": "Art café interior with a suspended greenery canopy and live-edge timber tables",
     "blurb": "A café that reads as a garden: suspended planting overhead, raw timber underfoot, art on every wall.",
     "gallery": [("projects/proj-cafe-terrace", "Café terrace with a red framed façade and timber shopfront"),
                 ("projects/proj-cafe-interior", "Interior seating under the hanging planting canopy")]},

    {"slug": "district-one-roof-garden", "title": "Roof Garden, District One",
     "cat": "Landscape", "service": "landscaping", "year": "", "loc": "District One, Dubai",
     "scope": "Roof landscape, pergola, planting, garden lighting",
     "img": "services/landscape-roof-garden",
     "alt": "Roof garden lounge lit at night beneath a planted pergola",
     "blurb": "A roof slab turned into an outdoor room, with the skyline as the back wall.",
     "gallery": [("projects/proj-district-one-garden", "Roof terrace under construction with the Dubai skyline behind"),
                 ("services/landscape-roof-garden", "Roof terrace lounge lit at night beneath planting")]},

    {"slug": "dubai-hills-landscape", "title": "Dubai Hills Landscape",
     "cat": "Landscape", "service": "landscaping", "year": "", "loc": "Dubai Hills, Dubai",
     "scope": "Landscape design and construction, planting, shade structure, lighting",
     "img": "projects/proj-dubai-hills-lawn",
     "alt": "Landscaped villa garden with a shade structure, lawn and seating",
     "blurb": "A villa garden built from a bare plot: levels, lawn, planting and a shaded seating terrace.",
     "gallery": [("projects/proj-dubai-hills-before", "The plot before works, showing bare ground and boundary walls"),
                 ("projects/proj-dubai-hills-sculpture", "Finished garden with sculpture, planting and stepping stones")]},
]

# --------------------------------------------------------------------------
# 3D visualisation, shown as renders, never as delivered projects
# --------------------------------------------------------------------------
VISUALS = [
    ("renders/render-lounge", "3D visualisation of a lounge with a curved red sofa and integrated media wall"),
    ("renders/render-living", "3D visualisation of an open living and games room in monochrome stone"),
    ("renders/render-workspace", "3D visualisation of an open-plan workspace with bench desking"),
    ("renders/render-gallery", "3D visualisation of a gallery-style retail interior"),
    ("renders/render-villa-night", "3D visualisation of a villa garden at night with reflection pools and uplit palms"),
    ("renders/render-villa-entrance", "3D visualisation of a villa entrance lit at night"),
]

# --------------------------------------------------------------------------
# Portfolio facts, each is countable from PROJECTS above, not asserted
# --------------------------------------------------------------------------
PROCESS = [
    {"n": "01", "t": "Consultation & Site Survey",
     "d": "We visit the property, measure it, and listen to how you actually use it before proposing anything."},
    {"n": "02", "t": "Concept & 3D Design",
     "d": "Mood direction, layouts and 3D renderings. You approve the finished look before anyone orders a tile."},
    {"n": "03", "t": "Drawings & Material Schedules",
     "d": "Final designs, construction drawings and material selections prepared so the site team builds what was agreed."},
    {"n": "04", "t": "Build & Fit-Out",
     "d": "Full design implementation by our own team, managed as one programme with progress reported to you."},
    {"n": "05", "t": "Handover & Aftercare",
     "d": "Joint snagging and handover, with optional annual maintenance cover afterwards."},
]

WHY_US = [
    {"t": "Design and build under one roof",
     "d": "The people who draw the project are the people who deliver it, so design intent survives contact with the site."},
    {"t": "A licensed technical services company",
     "d": "HST Architects sits inside HST Group, a licensed UAE building maintenance and technical services company."},
    {"t": "Residential and commercial",
     "d": "Villas, apartments, offices, showrooms, restaurants and gardens across Dubai and Abu Dhabi."},
    {"t": "Specified for this climate",
     "d": "Materials and planting chosen against Gulf heat, humidity and salinity rather than a European catalogue."},
]

SECTORS = [
    {"t": "Residential", "d": "Villas, apartments and penthouses", "img": "services/interior-curved-living"},
    {"t": "Workplace", "d": "Offices, boardrooms and studios", "img": "services/renovation-industrial-office"},
    {"t": "Retail", "d": "Showrooms and galleries", "img": "projects/proj-ima-gallery"},
    {"t": "Hospitality", "d": "Cafés and restaurants", "img": "projects/proj-cafe-greenery"},
    {"t": "Fitness", "d": "Gyms and training facilities", "img": "projects/proj-gym-rigs"},
    {"t": "Landscape", "d": "Gardens, terraces and roof gardens", "img": "services/landscape-pergola-lawn"},
]

HOME_FAQS = [
    {"q": "What areas of the UAE does HST Architects cover?",
     "a": "We work across Dubai, including Downtown, Business Bay, Emirates Hills, Dubai Marina, Jumeirah, Al Barsha, "
          "Damac Hills and District One, and take projects in Abu Dhabi."},
    {"q": "Do you handle both the design and the construction?",
     "a": "Yes. HST is a design-and-build practice: our services include full design implementation by our own team, "
          "based on the final designs and drawings. We can also build to another consultant's drawings."},
    {"q": "What does a project cost?",
     "a": "It depends on the property, the scope and the finish level, so we do not publish rates. We visit the site, "
          "agree the scope with you in writing, and quote a fixed fee against it."},
    {"q": "How do I start a project with you?",
     "a": "Send us the property details and what you want to change, or call the studio. We arrange a site visit and "
          "follow it with a written scope and fee proposal."},
    {"q": "Do you offer maintenance after handover?",
     "a": "Yes. HST Group provides building maintenance and technical services to residential and commercial buildings "
          "on an annual or daily operation basis, including annual maintenance contracts."},
]

# --------------------------------------------------------------------------
# Per-page SEO
# --------------------------------------------------------------------------
PAGES_SEO = {
    "home": {
        "title": "HST Architects | Interior Design & Landscaping in Dubai",
        "meta": "Dubai design-and-build studio for interiors, renovation and landscaping. "
                "Villas, offices, showrooms and gardens delivered by one team.",
        "h1": "Spaces built to outlast the trend",
    },
    "services": {
        "title": "Services | Interior Design, Fit-Out & Landscaping Dubai",
        "meta": "Three disciplines, one team: interior design, renovation and fit-out, and "
                "landscaping for villas, offices, retail and outdoor spaces in Dubai.",
        "h1": "Three disciplines, one accountable team",
    },
    "projects": {
        "title": "Projects | Dubai Interior, Fit-Out & Landscape Portfolio",
        "meta": "Selected HST Architects projects across Dubai and Abu Dhabi: villa interiors, office "
                "fit-outs, showrooms, hospitality and landscape design.",
        "h1": "Selected work",
    },
    "about": {
        "title": "About HST Architects | Dubai Design & Build Studio",
        "meta": "HST Architects is the design practice inside HST Group, a licensed Dubai "
                "building maintenance and technical services company.",
        "h1": "A studio that signs its own site drawings",
    },
    "contact": {
        "title": "Contact HST Architects | Downtown Dubai Studio",
        "meta": "Talk to HST Architects about your villa, office or garden. Boulevard Plaza Tower 1, "
                "Downtown Dubai. Call +971 50 399 9314 or send your project details.",
        "h1": "Tell us about the space",
    },
}
