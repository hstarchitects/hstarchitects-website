# -*- coding: utf-8 -*-
"""Single source of truth for every word, image and SEO field on hstarchitects.com.

Edit copy here, then run `python tools/build_site.py` to regenerate the HTML.
"""

SITE = {
    "name": "HST Architects",
    "legal": "HST Group",
    "domain": "https://hstarchitects.com",
    "tagline": "Interior Design, Renovation & Landscaping in Dubai",
    "short_desc": (
        "HST Architects is a Dubai interior design, renovation and landscaping studio "
        "delivering turnkey villas, offices, showrooms and outdoor spaces across the UAE."
    ),
    "founded": "2015",
    "phone_display": "+971 50 399 9314",
    "phone_link": "+971503999314",
    "landline_display": "+971 4 332 2002",
    "landline_link": "+97143322002",
    "email": "info@hstglobal.co",
    "address_line": "Boulevard Plaza Tower 1, Office 1603",
    "address_locality": "Downtown Dubai",
    "address_region": "Dubai",
    "address_country": "AE",
    "postal": "00000",
    "geo": {"lat": "25.1972", "lng": "55.2744"},
    "hours": "Sa-Th 09:00-18:00",
    "areas": [
        "Dubai", "Downtown Dubai", "Business Bay", "Dubai Marina", "Emirates Hills",
        "Palm Jumeirah", "Damac Hills", "Dubai Hills Estate", "District One",
        "Jumeirah", "Al Barsha", "Abu Dhabi", "Sharjah",
    ],
    "socials": {
        "instagram": "https://www.instagram.com/hst.technical",
        "linkedin": "https://www.linkedin.com/company/hst-group",
    },
}

# --------------------------------------------------------------------------
# Navigation — drives the header, the footer and the sitemap.
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
# --------------------------------------------------------------------------
SERVICES = [
    {
        "key": "interior-design",
        "num": "01",
        "title": "Interior Design",
        "url": "/services/interior-design/",
        "short": "Concept, space planning and 3D visualisation for villas, offices and showrooms.",
        "hero_img": "services/interior-lounge-seaview",
        "hero_alt": "Luxury Dubai lounge interior with a bespoke chandelier and full-height sea views",
        "card_img": "services/interior-curved-living",
        "card_alt": "Contemporary living room with a curved sculptural sofa and marble detailing",
        "seo_title": "Interior Design Company in Dubai | Villas, Offices & Showrooms",
        "meta": (
            "Award-calibre interior design in Dubai. HST Architects delivers concept design, "
            "space planning, 3D visualisation and full FF&E for villas, offices, retail and hospitality."
        ),
        "intro": (
            "We design interiors that hold up on the tenth year, not just on handover day. Every HST "
            "project starts with how a space will actually be lived in or worked in, then works backwards "
            "through light, circulation, material and detail until the drawings are precise enough to build from."
        ),
        "lede": "Design that survives the first ten years.",
        "outcomes": [
            "A design language your brand or family actually recognises as theirs",
            "Drawings detailed enough that contractors price them accurately the first time",
            "Material palettes specified against Dubai's heat, humidity and light",
        ],
        "capabilities": [
            {"t": "Concept & Mood Direction",
             "d": "We open with references, materials and light studies so the direction is agreed before a single wall moves."},
            {"t": "Space Planning & Layouts",
             "d": "Circulation, zoning and furniture layouts tested against how the space is used at 8am and at 8pm."},
            {"t": "3D Visualisation",
             "d": "Photoreal renders and walkthroughs so you approve the finished room, not a floor plan."},
            {"t": "Material & Finish Selection",
             "d": "Stone, timber, metal and textile schedules sourced from vetted UAE and European suppliers."},
            {"t": "Joinery & Millwork Design",
             "d": "Bespoke wardrobes, vanities, reception desks and feature walls drawn to shop-drawing standard."},
            {"t": "Lighting & FF&E",
             "d": "Layered lighting schemes plus furniture, fixtures and equipment specified, procured and installed."},
        ],
        "process_note": "Typical design programme: 4 to 8 weeks from brief to tender-ready drawings.",
        "faqs": [
            {"q": "How much does interior design cost in Dubai?",
             "a": "Design fees are usually quoted as a percentage of construction value or as a fixed fee per square foot, "
                  "depending on scope. A residential villa concept-to-tender package typically lands between AED 60 and "
                  "AED 140 per square foot. We issue a fixed fee after the first site visit so there are no open-ended hours."},
            {"q": "Do you work on apartments as well as villas?",
             "a": "Yes. We regularly deliver apartment and penthouse redesigns in Downtown, Business Bay and Dubai Marina, "
                  "including projects that must work within building management and developer fit-out rules."},
            {"q": "Can you take a project from design through to construction?",
             "a": "That is our default. The same team that draws the project runs the site, which removes the gap where "
                  "most design intent gets lost between designer and contractor."},
            {"q": "Do you provide 3D renders before we commit?",
             "a": "Yes. Photoreal visuals are produced during concept stage so you sign off on the finished look before "
                  "procurement or demolition begins."},
        ],
        "gallery": [
            ("services/interior-marble-lobby", "Marble entrance lobby with symmetrical joinery and inlaid stone flooring"),
            ("services/interior-styled-living", "Styled living room with open shelving, layered textiles and warm accent lighting"),
            ("services/interior-kitchen-brass", "Contemporary kitchen with a stone island, brass pendants and handleless cabinetry"),
            ("services/interior-corridor-gold", "Feature corridor with concealed cove lighting in warm brass tones"),
            ("services/interior-bath-marble", "Guest bathroom clad in book-matched marble with a floating timber vanity"),
            ("services/interior-loft-living", "Loft-style living area with exposed brick, timber floors and a linear sofa arrangement"),
        ],
    },
    {
        "key": "renovation",
        "num": "02",
        "title": "Renovation & Fit-Out",
        "url": "/services/renovation/",
        "short": "Turnkey refurbishment and fit-out, delivered by the team that drew it.",
        "hero_img": "services/renovation-boardroom",
        "hero_alt": "Completed Dubai boardroom fit-out with a sculptural table and full-height glazing",
        "card_img": "services/renovation-loft-office",
        "card_alt": "Converted loft office with exposed brick, black steel framing and warm timber floors",
        "seo_title": "Renovation & Fit-Out Contractor in Dubai | Villas, Offices & Retail",
        "meta": (
            "Licensed Dubai renovation and fit-out contractor. HST Architects delivers turnkey villa "
            "refurbishment, office fit-out, MEP, joinery and DM-approved project management across the UAE."
        ),
        "intro": (
            "Renovation is where good design either survives or quietly disappears. We hold a building "
            "maintenance and technical services licence, run our own site teams, and manage approvals, MEP, "
            "joinery and finishing under one contract so nobody can point at anyone else when something slips."
        ),
        "lede": "One contract. One team. One person answerable.",
        "outcomes": [
            "A single point of accountability from demolition to snagging",
            "Authority and building-management approvals handled in-house",
            "Programmes built around occupied buildings and out-of-hours work",
        ],
        "capabilities": [
            {"t": "Full Turnkey Fit-Out",
             "d": "Demolition, blockwork, ceilings, flooring, finishes and handover managed as one package."},
            {"t": "Villa & Apartment Refurbishment",
             "d": "Structural alterations, extensions and full interior rebuilds for occupied and vacant homes."},
            {"t": "MEP & Technical Services",
             "d": "HVAC, electrical, plumbing and low-current works executed by our own licensed technicians."},
            {"t": "Bespoke Joinery & Millwork",
             "d": "Workshop-fabricated wardrobes, kitchens, reception desks and feature panelling."},
            {"t": "Authority Approvals",
             "d": "Dubai Municipality, Civil Defence, DEWA and building-management submissions prepared and tracked."},
            {"t": "Annual Maintenance Contracts",
             "d": "Post-handover AMC cover so the finish you paid for is still there in year three."},
        ],
        "process_note": "Typical villa refurbishment: 10 to 20 weeks on site, phased around occupancy where needed.",
        "faqs": [
            {"q": "Do you handle Dubai Municipality and Civil Defence approvals?",
             "a": "Yes. We prepare and submit the drawings, chase the NOCs and coordinate inspections. Approvals are part "
                  "of the contract, not an extra you discover halfway through."},
            {"q": "How long does a villa renovation take in Dubai?",
             "a": "A full interior refurbishment of a four-bedroom villa usually runs 10 to 20 weeks on site. Structural "
                  "changes or landscape works extend that. We issue a week-by-week programme before mobilising."},
            {"q": "Can you work in an occupied office or home?",
             "a": "Yes. We phase the works, seal off live zones and run noisy trades outside business hours where the "
                  "building permits it. Several of our office projects were delivered without the client moving out."},
            {"q": "Do you give a fixed price or charge on variations?",
             "a": "We quote a fixed lump sum against a defined scope. Variations only arise if you change the scope or if "
                  "something genuinely unforeseen appears behind a wall, and both are priced and approved in writing first."},
        ],
        "gallery": [
            ("services/renovation-industrial-office", "Open-plan workspace with exposed services, timber desking and planting"),
            ("services/renovation-executive-office", "Executive office with a stone desk and panoramic Business Bay views"),
            ("services/renovation-meeting-room", "Meeting room with a solid timber table, slatted acoustic wall and linear lighting"),
            ("services/renovation-loft-stairs", "Feature steel-and-timber staircase inside a converted industrial space"),
            ("services/renovation-office-seaview", "Refurbished office floor with glazed partitions and waterfront views"),
            ("services/renovation-progress-shell", "Renovation in progress showing a stripped shell prepared for new services"),
        ],
    },
    {
        "key": "landscaping",
        "num": "03",
        "title": "Landscaping",
        "url": "/services/landscaping/",
        "short": "Gardens, pools, pergolas and roof terraces built for the Gulf climate.",
        "hero_img": "services/landscape-villa-pool",
        "hero_alt": "Private villa garden at dusk with a lit pool, raised planters and mature palms",
        "card_img": "services/landscape-roof-garden",
        "card_alt": "Roof terrace lounge framed by planting and warm concealed lighting at night",
        "seo_title": "Landscaping Company in Dubai | Garden Design, Pools & Pergolas",
        "meta": (
            "Landscape design and construction in Dubai. HST Architects builds villa gardens, swimming pools, "
            "pergolas, roof terraces, water features and irrigation engineered for the Gulf climate."
        ),
        "intro": (
            "In Dubai a garden is only as good as the eight months it has to survive. We design outdoor spaces "
            "around shade, breeze and irrigation first, then layer in the pool, the pergola and the planting — "
            "so the space is genuinely usable from October through May and still alive in August."
        ),
        "lede": "Outdoor rooms, engineered for the heat.",
        "outcomes": [
            "Shade and airflow planned before planting, not after",
            "Irrigation and drainage sized for UAE summer loads",
            "Night lighting designed so the garden works after sunset",
        ],
        "capabilities": [
            {"t": "Landscape Design & 3D",
             "d": "Master plans, planting schemes and photoreal night visuals before anything is dug."},
            {"t": "Swimming Pools & Water Features",
             "d": "Pools, plunge pools, reflection ponds and cascade walls with full filtration and plant rooms."},
            {"t": "Pergolas & Shade Structures",
             "d": "Aluminium, timber and louvred structures engineered for Gulf wind and sun loads."},
            {"t": "Hardscaping & Decking",
             "d": "Natural stone, porcelain, composite decking, raised planters and seating built into the level changes."},
            {"t": "Soft Landscaping & Planting",
             "d": "Palms, specimen trees, green walls and ground cover chosen for salinity and heat tolerance."},
            {"t": "Irrigation & Garden Lighting",
             "d": "Automated drip irrigation, drainage and low-voltage lighting on scene control."},
        ],
        "process_note": "Typical villa garden: 6 to 14 weeks on site depending on pool and structural works.",
        "faqs": [
            {"q": "Which plants actually survive a Dubai summer?",
             "a": "We build schemes around date and fan palms, frangipani, bougainvillea, ficus, desert rose and hardy "
                  "ground cover, backed by drip irrigation. Anything specified outside that range is flagged with its "
                  "real maintenance cost before you sign off."},
            {"q": "Do you build swimming pools as well as design them?",
             "a": "Yes. Excavation, shell, filtration, plant room, tiling and commissioning are delivered in-house with "
                  "the surrounding hardscape and lighting as a single package."},
            {"q": "Can you landscape a roof terrace or balcony?",
             "a": "Yes, and it is some of our most requested work in Downtown and District One. We check load allowances "
                  "with the building first, then design around lightweight substrates, waterproofing and wind exposure."},
            {"q": "Do you offer garden maintenance after handover?",
             "a": "Yes, through annual maintenance contracts covering irrigation, planting replacement, pool chemistry "
                  "and lighting so the garden does not decline in its second year."},
        ],
        "gallery": [
            ("services/landscape-water-wall", "Water feature wall with cascading spouts against a planted backdrop"),
            ("services/landscape-side-garden", "Side garden walkway with timber cladding, lawn strip and stepping stones"),
            ("services/landscape-pergola-lawn", "Aluminium pergola over an outdoor dining terrace beside a lawn"),
            ("services/landscape-garden-terrace", "Garden terrace with built-in seating, barbecue counter and shade structure"),
            ("services/landscape-planters", "Raised planters with mature shrubs framing a private villa garden"),
            ("hero/hero-villa-night", "Villa garden lit at night with reflection pools and uplit palms"),
        ],
    },
]

# --------------------------------------------------------------------------
# Projects
# --------------------------------------------------------------------------
PROJECTS = [
    {"slug": "springfield-properties-office", "title": "Springfield Properties HQ",
     "cat": "Fit-Out", "service": "renovation", "year": "2020", "loc": "Business Bay, Dubai",
     "area": "9,400 sqft", "scope": "Full office fit-out, joinery, MEP, branding integration",
     "img": "projects/proj-springfield-green",
     "alt": "Springfield Properties office reception with a living green wall and timber slat screening",
     "blurb": "A property developer's headquarters built around a planted spine that runs from the reception desk to the far studio wall.",
     "gallery": [("projects/proj-springfield-sign", "Springfield Properties logo on a backlit timber feature wall"),
                 ("projects/proj-springfield-reception", "Reception counter in book-matched stone with warm concealed lighting"),
                 ("projects/proj-springfield-lounge", "Breakout lounge with a pool table, library shelving and planting"),
                 ("projects/proj-springfield-studio", "Open studio floor with bench desking and glazed meeting rooms"),
                 ("projects/proj-springfield-desk", "Detail of the curved reception desk and brass reveal")]},

    {"slug": "emirates-hills-villa", "title": "Private Villa, Emirates Hills",
     "cat": "Interior", "service": "interior-design", "year": "2022", "loc": "Emirates Hills, Dubai",
     "area": "12,000 sqft", "scope": "Full interior design, bespoke joinery, FF&E, lighting",
     "img": "services/interior-lounge-seaview",
     "alt": "Emirates Hills villa lounge with a statement chandelier and full-height glazing",
     "blurb": "A family villa reworked around one idea: every principal room should see either water or sky.",
     "gallery": [("services/interior-curved-living", "Formal living room with a curved sofa and marble fireplace wall"),
                 ("projects/proj-villa-pantry", "Concealed pantry in dark stone with integrated appliances"),
                 ("projects/proj-villa-powder", "Guest powder room clad in figured marble with a floating basin"),
                 ("services/interior-bath-green", "Principal bathroom in green marble with brass fittings")]},

    {"slug": "al-wasl-gym", "title": "Gym Renovation, Al Wasl",
     "cat": "Renovation", "service": "renovation", "year": "2023", "loc": "Al Wasl, Dubai",
     "area": "6,200 sqft", "scope": "Structural renovation, specialist flooring, MEP, rig installation",
     "img": "projects/proj-gym-rigs",
     "alt": "Training floor with steel rigs, rubber flooring and industrial ceiling services",
     "blurb": "A tired retail shell stripped back to structure and rebuilt as a strength and conditioning facility.",
     "gallery": [("projects/proj-gym-cardio", "Cardio zone with treadmills facing full-height glazing"),
                 ("projects/proj-gym-floor", "Free-weights floor with rubber matting and mirrored walls"),
                 ("projects/proj-gym-lounge", "Members lounge with a double-height void and feature stair")]},

    {"slug": "damac-hills-landscape", "title": "Villa Landscape, Damac Hills",
     "cat": "Landscape", "service": "landscaping", "year": "2023", "loc": "Damac Hills, Dubai",
     "area": "4,800 sqft plot",
     "scope": "Landscape design, pergola, irrigation, garden lighting, outdoor kitchen",
     "img": "services/landscape-pergola-lawn",
     "alt": "Damac Hills villa garden with an aluminium pergola over an outdoor dining terrace",
     "blurb": "A blank sand plot turned into three connected outdoor rooms: dining, lawn and a shaded lounge.",
     "gallery": [("services/landscape-garden-terrace", "Outdoor kitchen and barbecue counter under the pergola"),
                 ("services/landscape-planters", "Raised planters with mature shrubs along the boundary wall"),
                 ("hero/hero-villa-entrance", "Villa entrance lit at night with uplit planting")]},

    {"slug": "mehr-o-mah-art-cafe", "title": "Mehr o Mah Art Café",
     "cat": "Hospitality", "service": "interior-design", "year": "2022", "loc": "Jumeirah 1, Dubai",
     "area": "3,100 sqft", "scope": "Concept design, joinery, lighting, planting, furniture",
     "img": "projects/proj-cafe-greenery",
     "alt": "Art café interior with a suspended greenery canopy and live-edge timber tables",
     "blurb": "A café that reads as a garden: suspended planting overhead, raw timber underfoot, art on every wall.",
     "gallery": [("projects/proj-cafe-terrace", "Café terrace with a red framed façade and timber shopfront"),
                 ("projects/proj-cafe-interior", "Interior seating under the hanging planting canopy")]},

    {"slug": "ima-gallery-showroom", "title": "IMA Gallery Showroom",
     "cat": "Retail", "service": "interior-design", "year": "2021", "loc": "Art of Living Mall, Dubai",
     "area": "2,400 sqft", "scope": "Retail concept, display joinery, feature lighting, shopfront",
     "img": "projects/proj-ima-gallery",
     "alt": "IMA Gallery shopfront in polished stone with a backlit signage band",
     "blurb": "A jewellery-box shopfront: dark stone frame, bright interior, everything engineered to make product the only bright thing.",
     "gallery": [("projects/proj-ima-interior", "Gallery interior with sculptural display plinths and pendant lighting")]},

    {"slug": "dng-furniture-showroom", "title": "DNG Furniture Showroom",
     "cat": "Retail", "service": "renovation", "year": "2022", "loc": "Al Barsha One, Dubai",
     "area": "5,600 sqft", "scope": "Showroom fit-out, lighting design, display systems",
     "img": "projects/proj-dng-furniture",
     "alt": "Furniture showroom with vignette settings, pendant lighting and a dark feature wall",
     "blurb": "A showroom laid out as a sequence of rooms rather than a warehouse of stock.",
     "gallery": [("projects/proj-gama-showroom", "Adjacent showroom zone in marble and brushed gold"),
                 ("projects/proj-gama-retail", "Retail display run with timber shelving and integrated lighting")]},

    {"slug": "marina-penthouse", "title": "Penthouse Redesign, Dubai Marina",
     "cat": "Residential", "service": "interior-design", "year": "2023", "loc": "Dubai Marina",
     "area": "5,200 sqft", "scope": "Full redesign, kitchen, bathrooms, joinery, FF&E",
     "img": "projects/proj-penthouse-marina",
     "alt": "Marina penthouse kitchen with stone surfaces, dark joinery and concealed lighting",
     "blurb": "A dated marina penthouse opened up into one continuous living floor facing the water.",
     "gallery": [("services/interior-kitchen-brass", "New kitchen with a stone island and brass pendants"),
                 ("services/interior-corridor-white", "Gallery corridor with an inlaid floor and linear lighting")]},

    {"slug": "district-one-roof-garden", "title": "Roof Garden, District One",
     "cat": "Landscape", "service": "landscaping", "year": "2023", "loc": "District One, Dubai",
     "area": "2,900 sqft", "scope": "Roof landscape, pergola, planting, lighting, waterproofing coordination",
     "img": "services/landscape-roof-garden",
     "alt": "District One roof garden lounge lit at night beneath a planted pergola",
     "blurb": "A roof slab turned into the most-used room in the house, with the skyline as the back wall.",
     "gallery": [("projects/proj-district-one-garden", "Roof terrace under construction with the Dubai skyline behind"),
                 ("services/landscape-water-wall", "Water feature wall against the terrace planting")]},

    {"slug": "nbd-office-renovation", "title": "Office Renovation, Emirates NBD Building",
     "cat": "Fit-Out", "service": "renovation", "year": "2021", "loc": "Deira, Dubai",
     "area": "7,800 sqft", "scope": "Strip-out, partitions, ceilings, MEP, finishes",
     "img": "projects/proj-nbd-office",
     "alt": "Corporate office floor with glazed partitions, linear lighting and neutral finishes",
     "blurb": "A whole-floor corporate refurbishment delivered around a live building with the tenant still trading.",
     "gallery": [("services/renovation-office-seaview", "Completed office floor with glazed offices and open desking")]},

    {"slug": "business-bay-private-office", "title": "Private Office, Business Bay",
     "cat": "Interior", "service": "interior-design", "year": "2023", "loc": "Business Bay, Dubai",
     "area": "3,300 sqft", "scope": "Interior design, joinery, lighting, furniture",
     "img": "services/renovation-executive-office",
     "alt": "Executive office with a stone desk and floor-to-ceiling views over Business Bay",
     "blurb": "A single-occupier office where the boardroom, the desk and the view were designed as one composition.",
     "gallery": [("services/renovation-meeting-room", "Boardroom with a solid timber table and slatted acoustic walls"),
                 ("projects/proj-office-reception", "Reception with a backlit stone counter"),
                 ("projects/proj-office-deira", "Waiting area with lounge seating and planting")]},

    {"slug": "jumeirah-villa", "title": "Private Villa, Jumeirah",
     "cat": "Residential", "service": "renovation", "year": "2022", "loc": "Jumeirah, Dubai",
     "area": "8,700 sqft", "scope": "Full refurbishment, structural alterations, joinery, landscape",
     "img": "projects/proj-villa-jumeirah",
     "alt": "Refurbished Jumeirah villa entrance hall with marble flooring and a double-height void",
     "blurb": "A 1990s villa taken back to shell and rebuilt with a modern plan behind the original elevation.",
     "gallery": [("services/interior-marble-lobby", "Entrance hall with inlaid marble flooring and symmetrical joinery"),
                 ("services/interior-bath-marble", "Principal bathroom in book-matched marble")]},
]

# --------------------------------------------------------------------------
# Process, stats, testimonials
# --------------------------------------------------------------------------
PROCESS = [
    {"n": "01", "t": "Consultation & Site Survey",
     "d": "We visit the property, measure it, listen to how you actually use it, and tell you honestly what the budget will and will not buy."},
    {"n": "02", "t": "Concept & 3D Design",
     "d": "Mood direction, layouts and photoreal visuals. You approve the finished room before anyone orders a tile."},
    {"n": "03", "t": "Technical Drawings & Approvals",
     "d": "Construction drawings, material schedules and authority submissions prepared so the site team has no room to improvise."},
    {"n": "04", "t": "Build & Fit-Out",
     "d": "Our own technicians and vetted trades execute the works under one programme with weekly progress reporting."},
    {"n": "05", "t": "Handover & Aftercare",
     "d": "Joint snagging, warranties, as-built documentation and an optional annual maintenance contract."},
]

STATS = [
    {"v": "180+", "l": "Projects Delivered"},
    {"v": "10", "l": "Years in the UAE"},
    {"v": "1.4M", "l": "Square Feet Completed"},
    {"v": "96%", "l": "Client Retention"},
]

TESTIMONIALS = [
    {"q": "They ran the design and the site with the same team, which is exactly why the finished office looks like the renders. "
          "We stayed trading through the whole fit-out.",
     "n": "Operations Director", "r": "Property developer, Business Bay"},
    {"q": "Our villa was handed over on the date they gave us at the start. In Dubai that is not a small thing.",
     "n": "Private Client", "r": "Emirates Hills"},
    {"q": "The garden is the part of the house we actually use. They planned the shade before the planting and it shows every afternoon.",
     "n": "Private Client", "r": "Damac Hills"},
]

WHY_US = [
    {"t": "Licensed & accountable",
     "d": "A registered UAE building maintenance and technical services company, not a design studio subcontracting the risk."},
    {"t": "Design and build under one roof",
     "d": "The people who drew it are the people who build it, so design intent survives contact with the site."},
    {"t": "Fixed scope, fixed price",
     "d": "A defined lump sum against a defined scope, with variations priced and approved in writing before work proceeds."},
    {"t": "Specified for this climate",
     "d": "Materials, planting and systems chosen against Gulf heat, humidity and salinity rather than a European catalogue."},
]

HOME_FAQS = [
    {"q": "What areas of the UAE does HST Architects cover?",
     "a": "We work across Dubai — Downtown, Business Bay, Emirates Hills, Palm Jumeirah, Dubai Hills, District One, Jumeirah "
          "and Damac Hills — and take selected projects in Abu Dhabi and Sharjah."},
    {"q": "Do you handle both the design and the construction?",
     "a": "Yes. HST is a design-and-build practice. We can also take on construction only, working to another consultant's drawings."},
    {"q": "What does a project cost?",
     "a": "It depends on scope and finish level, but we issue a fixed lump sum after the first site visit rather than an "
          "open-ended hourly estimate. Most villa interiors start around AED 350 per square foot for the built works."},
    {"q": "How do I start a project with you?",
     "a": "Send us the property details and what you want to change. We arrange a site visit within a few days, and you get a "
          "written scope and fee proposal after that visit."},
    {"q": "Do you offer maintenance after handover?",
     "a": "Yes. Annual maintenance contracts cover MEP, joinery, pool chemistry, irrigation and general upkeep so the project "
          "does not degrade once the site team leaves."},
]

# --------------------------------------------------------------------------
# Per-page SEO
# --------------------------------------------------------------------------
PAGES_SEO = {
    "home": {
        "title": "HST Architects | Interior Design, Renovation & Landscaping in Dubai",
        "meta": "Dubai design-and-build studio for interiors, renovation and landscaping. Villas, offices, "
                "showrooms and gardens delivered turnkey across the UAE. Fixed scope, fixed price, one accountable team.",
        "h1": "Spaces built to outlast the trend",
    },
    "services": {
        "title": "Our Services | Interior Design, Fit-Out & Landscaping in Dubai",
        "meta": "Three disciplines, one accountable team: interior design, renovation and fit-out, and landscaping. "
                "See what HST Architects delivers for villas, offices, retail and outdoor spaces in Dubai.",
        "h1": "Three disciplines, one accountable team",
    },
    "projects": {
        "title": "Projects | Dubai Interior, Fit-Out & Landscape Portfolio",
        "meta": "Selected HST Architects projects across Dubai and the UAE: villa interiors, office fit-outs, "
                "showrooms, hospitality and landscape design. Scope, area and year for each.",
        "h1": "Selected work",
    },
    "about": {
        "title": "About HST Architects | Dubai Design & Build Studio",
        "meta": "HST Architects is a licensed Dubai design-and-build practice delivering interiors, renovation "
                "and landscaping since 2015. Meet the studio, the process and the standards we hold.",
        "h1": "A studio that signs its own site drawings",
    },
    "contact": {
        "title": "Contact HST Architects | Downtown Dubai Design Studio",
        "meta": "Talk to HST Architects about your villa, office or garden. Boulevard Plaza Tower 1, Downtown Dubai. "
                "Call +971 50 399 9314 or send your project details for a site visit.",
        "h1": "Tell us about the space",
    },
}
