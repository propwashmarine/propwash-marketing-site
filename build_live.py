from pathlib import Path
from html import escape
import json
import re
import shutil
import subprocess


ROOT = Path(__file__).parent
TEMPLATE = ROOT / "src" / "v4-template.html"
CITY_TEMPLATE = ROOT / "src" / "city-template.html"
MEDIA = Path("/Volumes/Jack's Hard Drive/Propwash/Website Media")
DERIVED = ROOT / "src" / "media-derived"
OUT = ROOT / "assets" / "v4"
DIST = ROOT / "dist"
BASE_URL = "https://propwashmarine.com"

CITY_ORDER = [
    ("stuart", "Stuart"),
    ("jupiter", "Jupiter"),
    ("palm-beach", "Palm Beach"),
    ("delray-beach", "Delray Beach"),
    ("boca-raton", "Boca Raton"),
    ("deerfield-beach", "Deerfield Beach"),
    ("lighthouse-point", "Lighthouse Point"),
    ("pompano-beach", "Pompano Beach"),
    ("fort-lauderdale", "Fort Lauderdale"),
]

# Verified local facts and page-specific copy live here. The builder never fills
# blank local fields or invents place names.
CITY_DATA = {
    "boca-raton": {
        "city": "Boca Raton",
        "county": "Palm Beach County",
        "waterways": ["the Intracoastal Waterway", "Lake Boca Raton", "the Boca Raton Inlet"],
        "marinas": ["The Boca Raton Resort & Club Marina", "Mizner Marina"],
        "ramps": ["Silver Palm Park", "Spanish River Park", "James Rutherford Park"],
        "neighborhoods": ["Royal Palm Yacht & Country Club", "Boca Bayou", "Lake Wyman"],
        "local_note": "Boca runs on 77-plus miles of canals and lakes feeding one of the prettiest inlets on the coast; Silver Palm Park on Palmetto Park Road is the city's public ramp to the Intracoastal.",
        "hero_image": "assets/v4/hero-poster.webp",
        "neighbors": ["delray-beach", "deerfield-beach"],
        "title": "Mobile Boat Detailing in Boca Raton, FL | Propwash Marine",
        "meta_description": "Mobile boat detailing in Boca Raton for boats on Lake Boca, the Intracoastal and local canals, from signature washes to ceramic protection.",
        "intro": [
            "We provide mobile boat detailing for Boca Raton boats along the Intracoastal Waterway, Lake Boca Raton and the Boca Raton Inlet.",
            "We work around marina access, public ramps, private docks, lifts and driveways across the city.",
            "The service plan follows the finish and storage setup, whether the boat needs a single reset or recurring care.",
        ],
        "services_lead": "Boca Raton boats see salt, sun and frequent use in different combinations, so we match the wash, correction and protection to the finish in front of us.",
        "services_heading": "Care shaped around the boat.",
        "process_lead": "A Boca Raton visit starts with clear boat details and ends with documented work, without requiring the owner to wait dockside.",
        "process_heading": "From photos to finish.",
        "services": [
            ("Signature Wash", "A focused exterior service clears salt and surface buildup when a Boca Raton boat needs more than a quick rinse."),
            ("Full Detail", "Brightwork, hatch lips, compartments, seating and interior surfaces receive a thorough condition-based reset."),
            ("Wax Protection", "After cleaning and preparation, machine-applied wax restores depth while adding a practical protective layer."),
            ("Compound + Polish", "Oxidation is corrected in stages, with polishing throughout and wet sanding reserved for finishes that require it."),
            ("Ceramic Coating", "The coating package is selected only after the gelcoat has been evaluated and prepared for long-term protection."),
            ("Maintenance Plans", "Scheduled washes and deeper monthly care keep Boca Raton owners informed through visit photos and service records."),
        ],
        "steps": [
            ("Show us the Boca Raton boat.", "Send its length, make, storage setup and photographs of the finish or problem areas."),
            ("Set the correct scope.", "We review the condition before recommending washing, detailing, correction, protection or a combination."),
            ("Coordinate boat access.", "The crew confirms the marina, ramp, lift or driveway arrangements needed for the scheduled visit."),
            ("See what was completed.", "Finished-work photos and service information are organized in the Owner Portal after the appointment."),
        ],
        "cta_title": "Put your Boca Raton boat on our list.",
        "cta_body": "Send the boat details, where it sits and what you want addressed. We will turn that information into a condition-based quote.",
    },
    "delray-beach": {
        "city": "Delray Beach",
        "county": "Palm Beach County",
        "waterways": ["the Intracoastal Waterway", "Lake Boca"],
        "marinas": ["the Delray Beach City Marina", "Delray Harbor Club Marina"],
        "ramps": ["Knowles Park", "Mangrove Park"],
        "neighborhoods": ["the Marina Historic District", "the Atlantic Avenue corridor"],
        "local_note": "The City Marina sits in the historic Marina District right on the Intracoastal, a short walk off Atlantic Avenue.",
        "hero_image": "assets/v4/gallery1.webp",
        "neighbors": ["boca-raton", "deerfield-beach"],
        "title": "Mobile Boat Detailing in Delray Beach, FL | Propwash Marine",
        "meta_description": "Dockside boat detailing in Delray Beach along the Intracoastal and Lake Boca, including full details, correction, coatings and maintenance.",
        "intro": [
            "We bring dockside boat detailing to Delray Beach boats kept along the Intracoastal Waterway and Lake Boca.",
            "Service is available around the Delray Beach City Marina, Delray Harbor Club Marina and the city's listed launch points.",
            "We assess the actual finish before shaping a one-time service or ongoing care schedule.",
        ],
        "services_lead": "For Delray Beach owners, the starting point is the boat itself: how the finish looks, where it is kept and what it needs before the next run.",
        "services_heading": "Built around your boat.",
        "process_lead": "From the first Delray Beach photo to the final visit record, the scope stays tied to the boat's real condition and access.",
        "process_heading": "How a visit comes together.",
        "services": [
            ("Signature Wash", "This one-time exterior wash removes salt and everyday grime when the boat needs focused attention outside a membership."),
            ("Full Detail", "A full reset reaches brightwork, hatch lips, storage areas, upholstery, interior surfaces, rust marks and staining."),
            ("Wax Protection", "Machine application follows proper surface preparation to leave the gelcoat glossier and better protected."),
            ("Compound + Polish", "We tailor correction to the level of oxidation, polish the finish and wet sand only where the condition calls for it."),
            ("Ceramic Coating", "Preparation is defined first, then the ceramic package is matched to the boat and its expected maintenance."),
            ("Maintenance Plans", "Recurring Delray Beach care combines a chosen wash cadence with visit photos, records and scheduled deeper work."),
        ],
        "steps": [
            ("Begin with your Delray boat.", "Provide the length, make, storage location and useful close-ups of anything that needs attention."),
            ("Receive a tailored recommendation.", "The proposed work reflects the boat's finish rather than a preset package chosen sight unseen."),
            ("Pick a workable visit.", "We arrange access at the Slip, launch area, lift or driveway and arrive with the required equipment."),
            ("Review the Delray result.", "The Owner Portal keeps completed-visit images, invoices and service history together for later reference."),
        ],
        "cta_title": "Tell us about your Delray Beach boat.",
        "cta_body": "Share the vessel, its location and the areas that need work. We will recommend the right scope and follow up with a custom quote.",
    },
    "deerfield-beach": {
        "city": "Deerfield Beach",
        "county": "Broward County",
        "waterways": ["the Intracoastal Waterway", "the Hillsboro Inlet", "the Hillsboro River"],
        "marinas": ["Cove Marina", "Marina One", "Pennell's Marine"],
        "ramps": ["Pioneer Park"],
        "neighborhoods": ["The Cove"],
        "local_note": "A serious offshore-fishing community built around the Hillsboro Inlet; Cove Marina sits on the Intracoastal just south of it, where boats stage before dawn runs.",
        "hero_image": "assets/v4/gallery3.webp",
        "neighbors": ["boca-raton", "lighthouse-point"],
        "title": "Boat Detailing in Deerfield Beach, FL | Propwash Marine",
        "meta_description": "Boat detailing in Deerfield Beach for vessels near the Hillsboro Inlet, Intracoastal and Hillsboro River, with mobile washes and finish care.",
        "intro": [
            "We bring mobile detailing to Deerfield Beach boats around the Intracoastal Waterway, Hillsboro Inlet and Hillsboro River.",
            "Our mobile crew serves boats associated with Cove Marina, Marina One, Pennell's Marine and Pioneer Park access.",
            "Each recommendation accounts for the finish, how the boat is stored and the care it receives between offshore runs.",
        ],
        "services_lead": "Deerfield Beach owners can combine an immediate cleanup with the correction, protection or repeat schedule their boat actually requires.",
        "services_heading": "Ready for the next run.",
        "process_lead": "For a Deerfield appointment, useful photos and access details let us define the work before the crew reaches the boat.",
        "process_heading": "A clearer service path.",
        "services": [
            ("Signature Wash", "A thorough mobile wash handles the salt and deck buildup left behind when the Deerfield boat comes back in."),
            ("Full Detail", "The reset covers exterior details, hatch edges, hardware, seating, compartments and requested interior cleaning."),
            ("Wax Protection", "Prepared surfaces receive machine-applied wax to improve gloss and give the finish an added defense."),
            ("Compound + Polish", "Correction reduces oxidation and restores clarity through a measured compound-and-polish sequence."),
            ("Ceramic Coating", "Ceramic protection begins with the necessary cleaning and correction so the coating is never placed over a neglected surface."),
            ("Maintenance Plans", "Planned visits help a Deerfield Beach boat stay cleaner between outings while giving the owner a photo record each time."),
        ],
        "steps": [
            ("Document the Deerfield boat.", "Send basic specifications, its usual location and photographs that show the overall condition."),
            ("Define what the finish needs.", "We separate immediate cleaning from correction and protection before presenting the recommended scope."),
            ("Confirm the access plan.", "Timing is coordinated around the marina, Pioneer Park, private dock, lift or driveway involved."),
            ("Receive the service record.", "Once complete, the visit is supported by images and account details inside the Owner Portal."),
        ],
        "cta_title": "Get your Deerfield Beach boat ready.",
        "cta_body": "Show us where the boat is kept and what the finish is doing. We will respond with the most useful next service.",
    },
    "pompano-beach": {
        "city": "Pompano Beach",
        "county": "Broward County",
        "waterways": ["the Intracoastal Waterway", "the Hillsboro Inlet"],
        "marinas": ["Sands Harbor Resort & Marina", "Aquamarina Hidden Harbour", "Hillsboro Inlet Marina"],
        "ramps": ["Alsdorf Park"],
        "neighborhoods": [],
        "local_note": "Fast ocean access through the Hillsboro Inlet with no fixed bridges; Alsdorf Park on the NE 14th Street Causeway is the main public ramp.",
        "hero_image": "assets/v4/compound.webp",
        "neighbors": ["lighthouse-point", "fort-lauderdale"],
        "title": "Boat Detailing in Pompano Beach, FL | Propwash Marine",
        "meta_description": "Mobile boat detailing in Pompano Beach near the Hillsboro Inlet and Intracoastal, with wash, polishing, ceramic and recurring care options.",
        "intro": [
            "We detail Pompano Beach boats based along the Intracoastal Waterway and near the Hillsboro Inlet.",
            "We coordinate mobile service for vessels around Sands Harbor Resort & Marina, Aquamarina Hidden Harbour, Hillsboro Inlet Marina and Alsdorf Park.",
            "The work can range from a direct wash to multi-stage finish restoration and scheduled upkeep.",
        ],
        "services_lead": "Pompano Beach boating can put salt back on a clean finish quickly, making the right preparation and care cadence more valuable than a generic package.",
        "services_heading": "Salt handled at the source.",
        "process_lead": "A few accurate details help us plan a Pompano visit around the boat, its access point and the result the owner wants.",
        "process_heading": "Plan it. Clean it. Prove it.",
        "services": [
            ("Signature Wash", "The Signature Wash gives a Pompano Beach boat a deliberate top-to-bottom exterior cleanup after regular use."),
            ("Full Detail", "Detailed attention extends through metalwork, hatches, seating, compartments, staining and selected cabin surfaces."),
            ("Wax Protection", "Wax is machine-applied after preparation to sharpen the reflection and leave a useful sacrificial barrier."),
            ("Compound + Polish", "A staged correction plan addresses dull or oxidized gelcoat before refining it to an even finish."),
            ("Ceramic Coating", "Coating work includes the surface preparation needed for consistent bonding, gloss and maintainability."),
            ("Maintenance Plans", "A repeat Pompano schedule keeps salt and light staining from becoming the next large detailing project."),
        ],
        "steps": [
            ("Introduce the Pompano vessel.", "Tell us the dimensions, model, storage arrangement and the visible issues you want solved."),
            ("Match work to condition.", "Photos guide the initial recommendation for washing, detailing, oxidation removal or protective treatment."),
            ("Arrange the mobile appointment.", "We settle the arrival window and access instructions for the marina, ramp, lift or home location."),
            ("Keep the outcome on file.", "Post-visit documentation gives the owner a clear record of what the Pompano boat received."),
        ],
        "cta_title": "Plan the next Pompano Beach service.",
        "cta_body": "Describe the boat and the result you are after. We will review the condition and prepare a practical quote.",
    },
    "lighthouse-point": {
        "city": "Lighthouse Point",
        "county": "Broward County",
        "waterways": ["the Intracoastal Waterway", "the Hillsboro Inlet"],
        "marinas": ["Lighthouse Point Yacht Club"],
        "ramps": [],
        "neighborhoods": ["the deep-water canal district"],
        "local_note": "A canal-front, deep-water community minutes from the Hillsboro Inlet and its historic lighthouse; the Yacht Club marina handles sport-fishing craft and yachts from 30 to 120 feet.",
        "hero_image": "assets/v4/detailTower.webp",
        "neighbors": ["deerfield-beach", "pompano-beach"],
        "title": "Boat Detailing in Lighthouse Point, FL | Propwash Marine",
        "meta_description": "Dockside boat detailing in Lighthouse Point for canal-front boats near the Intracoastal and Hillsboro Inlet, from washes to finish protection.",
        "intro": [
            "We offer dockside detailing for Lighthouse Point boats throughout the deep-water canal district and along the Intracoastal Waterway.",
            "The service area includes vessels at Lighthouse Point Yacht Club and boats positioned for access to the Hillsboro Inlet.",
            "We shape each visit around surface condition, deck area, access and the owner's preferred level of upkeep.",
        ],
        "services_lead": "Lighthouse Point boats vary from sport-fishing craft to larger yachts, so surface area and condition guide every recommendation.",
        "services_heading": "Attention at every level.",
        "process_lead": "Planning the Lighthouse Point job in advance helps the crew account for dock access, upper structures and the exact finish work involved.",
        "process_heading": "Access through aftercare.",
        "services": [
            ("Signature Wash", "A dedicated exterior wash removes accumulated salt and traffic from a Lighthouse Point boat between larger services."),
            ("Full Detail", "From hatch lips to hardtops, the crew works through the high-touch and easily missed surfaces that define a complete detail."),
            ("Wax Protection", "Properly prepared gelcoat is finished with machine-applied wax for renewed shine and straightforward protection."),
            ("Compound + Polish", "We scale the correction process to the vessel's oxidation, surface area and reachable sections."),
            ("Ceramic Coating", "A boat-specific preparation plan supports ceramic coverage across the selected exterior surfaces."),
            ("Maintenance Plans", "Recurring dockside care gives Lighthouse Point owners a consistent wash rhythm and proof after each completed visit."),
        ],
        "steps": [
            ("Outline the Lighthouse Point boat.", "Length, make, berth details and representative photos establish the starting condition."),
            ("Account for every surface.", "We consider decks, towers, hardtops and finish defects when forming the recommended service."),
            ("Set dockside logistics.", "Access is confirmed with the owner before equipment and crew arrive at the boat."),
            ("Follow the care history.", "Portal records make it easier to review finished visits and plan the vessel's next round of attention."),
        ],
        "cta_title": "Build care around your Lighthouse Point boat.",
        "cta_body": "Send its size, dockage and current condition. We will account for the full surface area before quoting the work.",
    },
    "fort-lauderdale": {
        "city": "Fort Lauderdale",
        "county": "Broward County",
        "waterways": ["the New River", "the Intracoastal Waterway", "the Port Everglades inlet"],
        "marinas": ["Bahia Mar Yachting Center", "Las Olas Marina", "Pier Sixty-Six Marina", "Lauderdale Marina", "Hall of Fame Marina"],
        "ramps": ["Cooley's Landing", "George English Park"],
        "neighborhoods": ["Las Olas Isles", "Seabreeze Boulevard", "Coral Ridge", "Rio Vista"],
        "local_note": "The 'Yachting Capital of the World' and the 'Venice of America,' with 165-plus miles of navigable water and the country's largest in-water boat show every fall.",
        "hero_image": "assets/v4/detailMain.webp",
        "neighbors": ["pompano-beach", "lighthouse-point"],
        "title": "Boat Detailing in Fort Lauderdale, FL | Propwash Marine",
        "meta_description": "Mobile boat detailing in Fort Lauderdale across the New River, Intracoastal and leading marinas, including detailing, correction and coatings.",
        "intro": [
            "We provide Fort Lauderdale boat detailing along the New River, Intracoastal Waterway and Port Everglades inlet.",
            "Our service map reaches the supplied marina locations as well as Las Olas Isles, Coral Ridge, Rio Vista and the Seabreeze Boulevard area.",
            "We quote each boat from its condition and surface area instead of assuming every yacht needs the same package.",
        ],
        "services_lead": "Fort Lauderdale's range of dockage and vessel sizes calls for care that scales from a clean center console to a multi-deck yacht.",
        "services_heading": "Care scaled to the yacht.",
        "process_lead": "Detailed access information keeps a Fort Lauderdale appointment organized across busy marinas, riverfront slips and residential docks.",
        "process_heading": "Organized across the waterfront.",
        "services": [
            ("Signature Wash", "A comprehensive exterior wash resets a frequently used Fort Lauderdale boat without turning the visit into a full detail."),
            ("Full Detail", "The service works systematically across deck surfaces, hardware, hatch channels, seating, storage and requested interior areas."),
            ("Wax Protection", "Machine-applied wax follows cleaning and preparation to bring stronger gloss back to the visible finish."),
            ("Compound + Polish", "Correction intensity is selected after inspection, then refined through polishing for a more uniform appearance."),
            ("Ceramic Coating", "We prepare and coat the agreed surfaces according to the boat's condition, scale and maintenance goals."),
            ("Maintenance Plans", "Fort Lauderdale memberships organize recurring washes, deeper care, scheduling and visit documentation in one plan."),
        ],
        "steps": [
            ("Profile the Fort Lauderdale yacht.", "Share the vessel length, layout, marina or neighborhood and photographs of its present finish."),
            ("Map the work before arrival.", "The quote separates routine cleaning, detailed restoration, correction and protective options."),
            ("Coordinate a complex waterfront.", "We confirm entry, parking, dock and vessel access so the service day begins efficiently."),
            ("Track every finished appointment.", "Owners receive an organized digital history with post-service images and account records."),
        ],
        "cta_title": "Quote your Fort Lauderdale boat properly.",
        "cta_body": "Give us the vessel, marina or dock location and the finish concerns. We will define an appropriate dockside scope.",
    },
    "palm-beach": {
        "city": "Palm Beach",
        "county": "Palm Beach County",
        "waterways": ["the Lake Worth Lagoon", "the Palm Beach (Lake Worth) Inlet", "the Intracoastal Waterway"],
        "marinas": [],
        "ramps": [],
        "neighborhoods": ["the Worth Avenue estate section", "Peanut Island (nearby anchorage)"],
        "local_note": "Palm Beach estates line the Lake Worth Lagoon with private dockage; ocean access runs through the Palm Beach Inlet by the Port of Palm Beach, with Peanut Island a popular anchorage just north.",
        "hero_image": "assets/v4/memberPlatinum.webp",
        "neighbors": ["jupiter", "delray-beach"],
        "title": "Mobile Boat Detailing in Palm Beach, FL | Propwash Marine",
        "meta_description": "Private dockside boat detailing in Palm Beach along the Lake Worth Lagoon and Intracoastal, with full details, correction and protection plans.",
        "intro": [
            "We bring mobile detailing to Palm Beach boats along the Lake Worth Lagoon and Intracoastal Waterway.",
            "Private dockage lines the estates near the Worth Avenue section, while ocean access runs through the Palm Beach (Lake Worth) Inlet by the Port of Palm Beach.",
            "Peanut Island is a nearby anchorage, and every service is planned around the boat's location, condition and care requirements.",
        ],
        "services_lead": "Palm Beach dockside care begins with discretion, access planning and a close look at the surfaces that determine the true scope.",
        "services_heading": "Care that meets the vessel.",
        "process_lead": "For a privately docked Palm Beach boat, clear instructions and advance condition photos keep the service precise from arrival through documentation.",
        "process_heading": "A measured dockside process.",
        "services": [
            ("Signature Wash", "A deliberate exterior cleaning handles salt, dust and surface residue for Palm Beach boats needing immediate presentation care."),
            ("Full Detail", "The detail reaches refined exterior elements, hatch channels, upholstery, storage spaces and agreed interior sections."),
            ("Wax Protection", "Surface preparation and machine-applied wax produce a polished result with an additional layer between the gelcoat and exposure."),
            ("Compound + Polish", "Dullness and oxidation are evaluated section by section before correction brings clarity back to the finish."),
            ("Ceramic Coating", "Selected surfaces receive coating only after the underlying condition has been cleaned, corrected and made ready."),
            ("Maintenance Plans", "A custom Palm Beach cadence combines recurring attention with recorded visits and planned deeper detailing."),
        ],
        "steps": [
            ("Describe the Palm Beach vessel.", "Provide its dimensions, model, private dock arrangement and current-condition imagery."),
            ("Develop a measured scope.", "We identify which areas need cleaning, restoration or protection before finalizing the recommendation."),
            ("Confirm private access.", "Arrival and dock instructions are settled directly so the crew can work without unnecessary interruption."),
            ("Retain a clear record.", "Completion photographs and account documents stay available to the owner through the portal."),
        ],
        "cta_title": "Arrange Palm Beach dockside care.",
        "cta_body": "Tell us where the boat is kept and how you want it presented. We will prepare a scope suited to the vessel.",
    },
    "jupiter": {
        "city": "Jupiter",
        "county": "Palm Beach County",
        "waterways": ["the Jupiter Inlet", "the Loxahatchee River", "the Intracoastal Waterway"],
        "marinas": ["Loggerhead Marina – Jupiter", "Jupiter Pointe Club & Marina"],
        "ramps": ["DuBois Park"],
        "neighborhoods": ["the Jupiter Inlet Lighthouse area", "Jupiter Island", "the Jupiter Sandbar"],
        "local_note": "Run out the Jupiter Inlet to the Gulf Stream, or up the mangrove-lined Loxahatchee River past the historic red lighthouse; the Sandbar near Cato's Bridge is the weekend gathering spot.",
        "hero_image": "assets/v4/covers.webp",
        "neighbors": ["palm-beach", "stuart"],
        "title": "Mobile Boat Detailing in Jupiter, FL | Propwash Marine",
        "meta_description": "Mobile boat detailing in Jupiter around the inlet, Loxahatchee River and Intracoastal, with washes, full details and finish protection.",
        "intro": [
            "We serve Jupiter boats traveling through the Jupiter Inlet, Loxahatchee River and Intracoastal Waterway.",
            "Mobile detailing is available around Loggerhead Marina – Jupiter, Jupiter Pointe Club & Marina and the DuBois Park launch area.",
            "We build the work around how the vessel is used, where it stays and what its finish shows on inspection.",
        ],
        "services_lead": "Jupiter boats move between river, inlet and ocean conditions, making condition-based washing and protection central to the care plan.",
        "services_heading": "River to inlet ready.",
        "process_lead": "The Jupiter service process turns a short set of boat details into a planned visit with an accountable finish record.",
        "process_heading": "Four steps to a ready boat.",
        "services": [
            ("Signature Wash", "A substantial one-time wash clears the residue left by Jupiter outings and restores a cleaner deck-to-hull presentation."),
            ("Full Detail", "Hardware, hatches, upholstery, compartments, staining and chosen interior spaces are addressed as one coordinated service."),
            ("Wax Protection", "Once prepared, the finish is machine-waxed to recover shine and support easier ongoing care."),
            ("Compound + Polish", "We choose the correction sequence from the visible oxidation rather than forcing every Jupiter boat through the same steps."),
            ("Ceramic Coating", "The ceramic scope pairs suitable surface preparation with the protection level selected for the vessel."),
            ("Maintenance Plans", "Recurring Jupiter visits help control salt and staining while keeping service evidence available after every appointment."),
        ],
        "steps": [
            ("Send the Jupiter boat details.", "Length, make, normal location and photos give us the context needed to begin."),
            ("Choose work from evidence.", "We use the visible condition to propose a wash, full detail, correction, coating or maintenance path."),
            ("Schedule around local access.", "The agreed marina, park, private dock, lift or driveway instructions shape the arrival plan."),
            ("Check the work remotely.", "The completed Jupiter visit is supported by images and service records in the Owner Portal."),
        ],
        "cta_title": "Keep your Jupiter boat ready to run.",
        "cta_body": "Send a few useful photos and the vessel's location. We will come back with the care level that fits its condition.",
    },
    "stuart": {
        "city": "Stuart",
        "county": "Martin County",
        "waterways": ["the St. Lucie River", "the St. Lucie Inlet", "the Manatee Pocket", "the Intracoastal Waterway"],
        "marinas": ["Sailfish Marina of Stuart", "MarineMax Stuart", "Finest Kind Marina", "Whiticar Boat Works"],
        "ramps": ["Sandsprit Park"],
        "neighborhoods": ["historic downtown Stuart", "the Riverwalk", "the Manatee Pocket"],
        "local_note": "The 'Sailfish Capital of the World,' with protected water in the no-wake Manatee Pocket and quick ocean access through the St. Lucie Inlet — the Gulf Stream sits about 10 miles out.",
        "hero_image": "assets/v4/blog3.webp",
        "neighbors": ["jupiter", "palm-beach"],
        "title": "Mobile Boat Detailing in Stuart, FL | Propwash Marine",
        "meta_description": "Boat detailing in Stuart around the St. Lucie River, Manatee Pocket and local marinas, including mobile washes, correction and coatings.",
        "intro": [
            "We provide Stuart boat detailing around the St. Lucie River, St. Lucie Inlet, Manatee Pocket and Intracoastal Waterway.",
            "The mobile service area includes Sailfish Marina of Stuart, MarineMax Stuart, Finest Kind Marina, Whiticar Boat Works and Sandsprit Park.",
            "Our recommendation follows the boat's present finish and the care it needs between river time and offshore use.",
        ],
        "services_lead": "Stuart's mix of protected water and quick inlet access puts different demands on a finish, which is why the boat determines the scope.",
        "services_heading": "Prepared for Stuart water.",
        "process_lead": "A Stuart appointment is organized from the first condition photos through the final portal record, with access settled before service day.",
        "process_heading": "Scope, service and record.",
        "services": [
            ("Signature Wash", "A complete exterior wash removes the salt and working grime that collect through regular Stuart boating."),
            ("Full Detail", "The crew resets visible and hidden areas, including brightwork, hatch lips, upholstery, compartments and requested interiors."),
            ("Wax Protection", "Prepared gelcoat is machine-waxed for a deeper finish and a renewable layer of everyday defense."),
            ("Compound + Polish", "Oxidized sections receive the level of compounding, wet sanding and polishing supported by their condition."),
            ("Ceramic Coating", "Coating recommendations account for preparation, boat use and the follow-up maintenance the surface will receive."),
            ("Maintenance Plans", "Ongoing Stuart service keeps the boat on a chosen rhythm and documents the condition after each crew visit."),
        ],
        "steps": [
            ("Give us the Stuart starting point.", "Share the boat size, manufacturer, storage location and images of priority surfaces."),
            ("Separate cleaning from restoration.", "We determine whether the vessel calls for routine care, a deeper reset or corrective finish work."),
            ("Organize the northern visit.", "The crew coordinates marina, ramp or private-property access before traveling to the Stuart location."),
            ("Use the record going forward.", "Visit photographs and account history support future maintenance decisions for the boat."),
        ],
        "cta_title": "Schedule the right Stuart boat service.",
        "cta_body": "Tell us the vessel, where it is and what has changed in the finish. We will recommend the next useful step.",
    },
}


def require_replace(text: str, old: str, new: str) -> str:
    if old not in text:
        raise RuntimeError(f"Expected source fragment was not found: {old[:120]}")
    return text.replace(old, new)


def save_image(source: Path, destination: Path, longest_side: int = 2000, quality: int = 84) -> None:
    subprocess.run(
        ["sips", "-Z", str(longest_side), "-s", "format", "jpeg", "-s", "formatOptions", str(quality), str(source), "--out", str(destination)],
        check=True,
        stdout=subprocess.DEVNULL,
    )


def render_tokens(template: str, values: dict[str, str]) -> str:
    rendered = template
    for name, value in values.items():
        rendered = rendered.replace("{{" + name + "}}", value)
    unresolved = sorted(set(re.findall(r"{{([A-Z_]+)}}", rendered)))
    if unresolved:
        raise RuntimeError(f"Unresolved city-template tokens: {', '.join(unresolved)}")
    return rendered


def render_city_page(slug: str, data: dict, shared_styles: str) -> str:
    city = data["city"]
    canonical_url = f"{BASE_URL}/boat-detailing-{slug}/"
    intro_html = "".join(f"<p>{escape(sentence)}</p>" for sentence in data["intro"] if sentence)
    services_html = "".join(
        f'<article class="pw-cityservice"><span>{number:02d}</span><h3>{escape(name)}</h3><p>{escape(description)}</p></article>'
        for number, (name, description) in enumerate(data["services"], 1)
    )
    steps_html = "".join(
        f'<article class="pw-citystep"><span>{number:02d}</span><h3>{escape(name)}</h3><p>{escape(description)}</p></article>'
        for number, (name, description) in enumerate(data["steps"], 1)
    )
    if len(data["neighbors"]) != 2:
        raise RuntimeError(f"{slug} must define exactly two verified neighboring city slugs")
    city_names = dict(CITY_ORDER)
    neighbor_links = "".join(
        f'<a href="/boat-detailing-{neighbor_slug}/">Boat detailing in {escape(neighbor_city)}</a>'
        for neighbor_slug, neighbor_city in ((item, city_names[item]) for item in data["neighbors"])
    )

    # The local-work block is intentionally absent when no verified marina or
    # ramp is supplied. Optional facts render only when their CITY_DATA field is set.
    local_block = ""
    if data["marinas"] or data["ramps"]:
        optional_notes = []
        if data["local_note"]:
            optional_notes.append(data["local_note"])
        if data["neighborhoods"]:
            optional_notes.append("We also serve boats around " + ", ".join(data["neighborhoods"]) + ".")
        notes_html = "".join(f"<p>{escape(note)}</p>" for note in optional_notes)
        location_groups = []
        if data["marinas"]:
            marina_items = "".join(f"<li>{escape(marina)}</li>" for marina in data["marinas"])
            location_groups.append(f'<div><h3>Marinas</h3><ul>{marina_items}</ul></div>')
        if data["ramps"]:
            ramp_items = "".join(f"<li>{escape(ramp)}</li>" for ramp in data["ramps"])
            location_groups.append(f'<div><h3>Ramps &amp; launch areas</h3><ul>{ramp_items}</ul></div>')
        local_block = (
            f'<section class="pw-citylocal pw-section pw-wrap"><div><div class="pw-kicker pw-eyebrow pw-muted">Local access</div>'
            f'<h2>Where we work<br> in {escape(city)}.</h2>{notes_html}</div>'
            f'<div class="pw-citylocallists">{"".join(location_groups)}</div></section>'
        )

    business_schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": f"{canonical_url}#business",
        "name": "Propwash Marine Detailing",
        "url": canonical_url,
        "telephone": "+1-561-291-8554",
        "areaServed": city,
        "sameAs": ["https://instagram.com/propwashmarine"],
    }
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": city, "item": canonical_url},
        ],
    }
    hero_image = data["hero_image"]
    return render_tokens(
        CITY_TEMPLATE.read_text(),
        {
            "TITLE": escape(data["title"]),
            "META_DESCRIPTION": escape(data["meta_description"]),
            "CANONICAL_URL": canonical_url,
            "HERO_ABSOLUTE_URL": f"{BASE_URL}/{hero_image}",
            "HERO_SRC": f"../{hero_image}",
            "CITY": escape(city),
            "COUNTY": escape(data["county"]),
            "INTRO_HTML": intro_html,
            "LOCAL_BLOCK": local_block,
            "SERVICES_LEAD": escape(data["services_lead"]),
            "SERVICES_HEADING": escape(data["services_heading"]),
            "SERVICES_HTML": services_html,
            "PROCESS_LEAD": escape(data["process_lead"]),
            "PROCESS_HEADING": escape(data["process_heading"]),
            "STEPS_HTML": steps_html,
            "NEIGHBOR_LINKS": neighbor_links,
            "CTA_TITLE": escape(data["cta_title"]),
            "CTA_BODY": escape(data["cta_body"]),
            "SHARED_STYLES": shared_styles,
            "BUSINESS_SCHEMA": json.dumps(business_schema, separators=(",", ":")),
            "BREADCRUMB_SCHEMA": json.dumps(breadcrumb_schema, separators=(",", ":")),
        },
    )


source = TEMPLATE.read_text()
head_links = re.search(r"<head>([\s\S]*?)</head>", source).group(1).strip()
styles = re.search(r"<style>([\s\S]*?)</style>", source).group(1)
markup_start = source.index('<div id="pw-redesign-v3">')
markup_end = source.index("<script>", markup_start)
markup = source[markup_start:markup_end].strip()
script = re.search(r"<script>([\s\S]*?)</script>", source).group(1)

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True, exist_ok=True)
(ROOT / "assets" / "logo").mkdir(parents=True, exist_ok=True)
(ROOT / "assets" / "video").mkdir(parents=True, exist_ok=True)

if not (ROOT / "assets" / "logo" / "brandmark.png").exists():
    shutil.copy2(MEDIA / "L01.png", ROOT / "assets" / "logo" / "brandmark.png")
if not (ROOT / "assets" / "logo" / "wordmark.png").exists():
    shutil.copy2(MEDIA / "L02.png", ROOT / "assets" / "logo" / "wordmark.png")
shutil.copy2(MEDIA / "H01.mp4", ROOT / "assets" / "video" / "hero-v4.mp4")

image_sources = {
    "hero": MEDIA / "H02.jpg",
    "signature": DERIVED / "signature.png",
    "detailMain": MEDIA / "S02.jpeg",
    "detailBright": MEDIA / "S02 Brightwork.jpg",
    "detailHatch": DERIVED / "hatch.png",
    "detailInterior": MEDIA / "S02 interior.jpg",
    "detailSeats": MEDIA / "S02 Seats.jpg",
    "detailTop": DERIVED / "hardtop.png",
    "detailTower": MEDIA / "DSC04465 copy.jpg",
    "wax": MEDIA / "S03.JPG",
    "compound": MEDIA / "S04 copy.JPG",
    "ceramic": MEDIA / "S05.jpg",
    "plans": MEDIA / "New Maintenance Plan Photo.JPG",
    "memberSilver": MEDIA / "M01.jpg",
    "memberGold": DERIVED / "member-gold.png",
    "memberPlatinum": MEDIA / "M03.jpg",
    "dashboard": DERIVED / "owner-portal.png",
    "covers": MEDIA / "Covers.jpg",
    "gallery1": MEDIA / "G01.jpg",
    "gallery2": MEDIA / "G02.png",
    "gallery3": MEDIA / "G03.jpeg",
    "gallery4": DERIVED / "shiny-console.png",
    "blog1": MEDIA / "B01.jpg",
    "blog2": MEDIA / "B02.png",
    "blog3": MEDIA / "B03.JPG",
}

asset_urls = {
    "brandmark": "assets/logo/brandmark.png",
    "wordmark": "assets/logo/wordmark.png",
    "video": "assets/video/hero-v4.mp4",
}

for key, path in image_sources.items():
    legacy_name = "hero-poster.webp" if key == "hero" else f"{key}.webp"
    legacy = ROOT / "assets" / "v3" / legacy_name
    if key not in {"plans", "gallery4"} and legacy.exists():
        filename = legacy_name
        shutil.copy2(legacy, OUT / filename)
    else:
        filename = f"{key}.jpg"
        save_image(path, OUT / filename, 1800 if key == "plans" else 2200, 82)
    asset_urls[key] = f"assets/v4/{filename}"

markup = require_replace(
    markup,
    '<div class="pw-reviewbar"><span>MOCKUP V4 / FINAL CONTENT REVIEW</span><div class="pw-reviewactions"><button class="pw-motion" id="pw-motion" type="button" aria-pressed="true"><span>◉</span> Motion on</button><button class="pw-motion" id="pw-preview-confirmation" type="button">Preview confirmation</button></div></div>',
    '<button class="pw-motion" id="pw-motion" type="button" aria-pressed="true" hidden><span>◉</span> Motion on</button><button class="pw-motion" id="pw-preview-confirmation" type="button" hidden>Preview confirmation</button>',
)
markup = markup.replace("preload=\"auto\"", "preload=\"metadata\"")
markup = markup.replace("Captured from the current My Slip portal for this design review.", "Your real service history, visit photos and payments in one place.")
markup = markup.replace("Run hard. Look right. / V4 design concept for approval", "Run hard. Look right. / South Florida Dockside Detailing")

markup = require_replace(
    markup,
    '<section id="pw-area" class="pw-area pw-section pw-wrap"><div><div class="pw-kicker pw-eyebrow pw-muted">07 / Our stretch of coast</div><h2>South Florida.<br> At your Slip.</h2><p>Based in Boca Raton. Mobile detailing from Stuart to Fort Lauderdale, at your Slip, lift or driveway. Just outside that stretch? Ask us.</p></div><div><div class="pw-locationlist">',
    '<section id="pw-area" class="pw-area pw-section pw-wrap"><div><div class="pw-kicker pw-eyebrow pw-muted">07 / Our stretch of coast</div><h2>South Florida.<br> At your Slip.</h2><p>Based in Boca Raton. Mobile detailing from Stuart to Fort Lauderdale, at your Slip, lift or driveway. Just outside that stretch? Ask us.</p><div class="pw-coastroute" aria-hidden="true"><span class="pw-routetrack"><i></i></span><b style="--pw-stop:0%"></b><b style="--pw-stop:51%"></b><b style="--pw-stop:100%"></b></div></div><div><div class="pw-locationlist">',
)
city_location_links = "".join(
    f'<div><a href="/boat-detailing-{slug}/"><strong class="{"pw-homebase" if slug == "boca-raton" else ""}">{escape(city)}</strong><small>{escape(CITY_DATA[slug]["county"])}</small></a></div>'
    for slug, city in CITY_ORDER
)
markup = require_replace(markup, "<!-- PW_CITY_LINKS -->", city_location_links)

markup = require_replace(
    markup,
    '</footer></div>\n<section id="pw-membership-page"',
    '</footer><nav class="pw-mobileactions" aria-label="Quick actions"><a href="tel:+15612918554">Call</a><a href="https://propwash.base44.app/login" target="_blank" rel="noopener">Client login</a><a href="#pw-quote">Get a quote</a></nav></div>\n<section id="pw-membership-page"',
)

markup = require_replace(
    markup,
    '<form id="pw-quote-form" class="pw-form">',
    '<form id="pw-quote-form" class="pw-form" name="quote-request" method="POST" action="/thank-you.html" data-netlify="true" netlify-honeypot="bot-field" enctype="multipart/form-data"><input type="hidden" name="form-name" value="quote-request"><label class="pw-hp" aria-hidden="true">Leave this field empty<input name="bot-field" tabindex="-1" autocomplete="off"></label>',
)
markup = require_replace(
    markup,
    '<button class="pw-cta" id="pw-preview-request" type="button">Preview request </button>',
    '<button class="pw-cta" id="pw-preview-request" type="submit">Send request</button>',
)
markup = markup.replace(
    'FORM PREVIEW / Nothing is sent or saved. Try the flow with sample details. For same-day or urgent requests, call us.',
    'Send the request and we will follow up with the right scope for your boat. For same-day or urgent work, call us.',
)
markup = markup.replace('Quote flow preview', 'Quote request').replace('This is a design preview. Nothing has been sent.', 'Your request is ready to submit.')
markup = markup.replace('MOCKUP / No request was sent', 'Propwash Marine Detailing')

markup = require_replace(
    markup,
    '<form id="pw-member-form" class="pw-memberform pw-wrap">',
    '<form id="pw-member-form" class="pw-memberform pw-wrap" name="membership-inquiry" method="POST" action="/thank-you.html" data-netlify="true" netlify-honeypot="bot-field"><input type="hidden" name="form-name" value="membership-inquiry"><input type="hidden" id="pw-member-plan" name="membership_plan" value="Platinum"><label class="pw-hp" aria-hidden="true">Leave this field empty<input name="bot-field" tabindex="-1" autocomplete="off"></label>',
)
markup = markup.replace('Inquiry preview', 'Membership inquiry').replace('This design preview sends and stores nothing.', 'Your membership request is ready to submit.')
member_names = {
    "pw-member-length": "boat_length",
    "pw-member-make": "make_model",
    "pw-member-location": "boat_location",
    "pw-member-storage": "storage",
    "pw-member-cadence": "wash_cadence",
    "pw-member-goals": "care_goals",
    "pw-member-first": "first_name",
    "pw-member-last": "last_name",
    "pw-member-phone": "phone",
    "pw-member-email": "email",
    "pw-member-source": "referral_source",
    "pw-member-notes": "notes",
}
for field_id, field_name in member_names.items():
    markup = re.sub(rf'(id="{re.escape(field_id)}")(?![^>]*\bname=)', rf'\1 name="{field_name}"', markup)

markup = require_replace(
    markup,
    '<button class="pw-cta" id="pw-member-preview" type="button">Preview inquiry </button>',
    '<button class="pw-cta" id="pw-member-preview" type="submit">Request membership</button>',
)

script = script.replace("const assets=__PW_ASSETS__;", "const assets=" + json.dumps(asset_urls, separators=(",", ":")) + ";")
script = script.replace(
    "root.querySelectorAll('[data-pw-img]').forEach(img=>{img.src=assets[img.dataset.pwImg];});",
    "root.querySelectorAll('[data-pw-img]').forEach(img=>{img.src=assets[img.dataset.pwImg];img.decoding='async';if(!img.closest('.pw-v2hero')&&!img.closest('.pw-logo'))img.loading='lazy';});",
)

script = require_replace(
    script,
    """const gallery={gallery1:['Dockside ready','Deep reflection along the waterfront'],gallery2:['Wherever you are','At the trailer, lift or Slip—we bring professional care to wherever the boat sits.'],gallery3:['Brightwork in focus','Brightwork, transom and engines brought back into focus'],gallery4:['Console clarity','A clean helm, polished stainless and a finish that catches the light.']};
root.querySelectorAll('[data-gallery]').forEach(btn=>btn.addEventListener('click',()=>{root.querySelectorAll('[data-gallery]').forEach(b=>b.setAttribute('aria-pressed',String(b===btn)));const key=btn.dataset.gallery;byId('pw-gallery-feature').src=assets[key];byId('pw-gallery-feature').alt=gallery[key][0]+' from the Propwash work gallery';byId('pw-gallery-name').textContent=gallery[key][0];byId('pw-gallery-detail').textContent=gallery[key][1];animate(byId('pw-gallery-feature'));}));""",
    """const gallery={gallery1:['Dockside ready','Deep reflection along the waterfront'],gallery2:['Wherever you are','At the trailer, lift or Slip—we bring professional care to wherever the boat sits.'],gallery3:['Brightwork in focus','Brightwork, transom and engines brought back into focus'],gallery4:['Console clarity','A clean helm, polished stainless and a finish that catches the light.']};
const galleryDrift={gallery1:['1.4%','-.5%'],gallery2:['-1.1%','.6%'],gallery3:['.8%','-.8%'],gallery4:['-1.3%','-.3%']};
root.querySelectorAll('[data-gallery]').forEach(btn=>btn.addEventListener('click',()=>{root.querySelectorAll('[data-gallery]').forEach(b=>b.setAttribute('aria-pressed',String(b===btn)));const key=btn.dataset.gallery,feature=byId('pw-gallery-feature');feature.src=assets[key];feature.alt=gallery[key][0]+' from the Propwash work gallery';feature.style.setProperty('--pw-drift-x',galleryDrift[key][0]);feature.style.setProperty('--pw-drift-y',galleryDrift[key][1]);feature.style.animation='none';requestAnimationFrame(()=>{feature.style.animation='';});byId('pw-gallery-name').textContent=gallery[key][0];byId('pw-gallery-detail').textContent=gallery[key][1];animate(feature);}));""",
)

enhancements = """
const areaSection=byId('pw-area');
if('IntersectionObserver' in window){new IntersectionObserver(entries=>{if(entries[0]?.isIntersecting){areaSection.classList.add('pw-route-visible');}},{threshold:.3}).observe(areaSection);}else{areaSection.classList.add('pw-route-visible');}
"""
script = require_replace(script, "\n})();", "\n" + enhancements + "\n})();")

old_quote = """function completePreview(){if(![...contact.querySelectorAll('input,select,textarea')].every(el=>el.reportValidity()))return;const request=byId('pw-interest').value;byId('pw-request-summary').textContent=byId('pw-length').value+' ft boat · '+request+'. Your boat details and contact information would accompany this request.';step(3);}
byId('pw-preview-request').addEventListener('click',completePreview);
form.addEventListener('submit',e=>{e.preventDefault();if(!contact.hidden)completePreview();});"""
new_quote = """form.addEventListener('submit',e=>{if(contact.hidden){e.preventDefault();byId('pw-next').click();return;}const valid=[...contact.querySelectorAll('input,select,textarea')].every(el=>el.reportValidity());if(!valid){e.preventDefault();return;}boat.querySelectorAll('input,select').forEach(el=>el.disabled=false);const send=byId('pw-preview-request');send.disabled=true;send.firstChild.textContent='Sending ';});"""
script = require_replace(script, old_quote, new_quote)

old_member = """byId('pw-member-next').addEventListener('click',()=>{if([...byId('pw-member-step1').querySelectorAll('input,select,textarea')].every(el=>el.reportValidity()))memberStep(2);});byId('pw-member-prev').addEventListener('click',()=>memberStep(1));byId('pw-member-preview').addEventListener('click',()=>{if([...byId('pw-member-step2').querySelectorAll('input,select,textarea')].every(el=>el.reportValidity()))memberStep(3);});byId('pw-member-restart').addEventListener('click',()=>memberStep(1));byId('pw-member-form').addEventListener('submit',e=>e.preventDefault());"""
new_member = """byId('pw-member-next').addEventListener('click',()=>{if([...byId('pw-member-step1').querySelectorAll('input,select,textarea')].every(el=>el.reportValidity()))memberStep(2);});byId('pw-member-prev').addEventListener('click',()=>memberStep(1));byId('pw-member-restart').addEventListener('click',()=>memberStep(1));byId('pw-member-form').addEventListener('submit',e=>{if(!byId('pw-member-step1').hidden){e.preventDefault();byId('pw-member-next').click();return;}const valid=[...byId('pw-member-step2').querySelectorAll('input,select,textarea')].every(el=>el.reportValidity());if(!valid){e.preventDefault();return;}byId('pw-member-plan').value=byId('pw-member-selected').textContent;byId('pw-member-step1').querySelectorAll('input,select,textarea').forEach(el=>el.disabled=false);const send=byId('pw-member-preview');send.disabled=true;send.firstChild.textContent='Sending ';});"""
script = require_replace(script, old_member, new_member)

live_css = """
html{scroll-behavior:smooth;background:#0A1A2F}
body{margin:0;background:#0A1A2F;overflow-x:hidden}
#pw-redesign-v3{width:100%;min-height:100vh}
#pw-redesign-v3 .pw-hp{position:absolute!important;width:1px!important;height:1px!important;overflow:hidden!important;clip:rect(0 0 0 0)!important;white-space:nowrap!important}
#pw-redesign-v3 .pw-v2hero .pw-nav{position:relative;z-index:3}
#pw-redesign-v3 .pw-locationlist>div>a{display:flex;gap:25px;justify-content:space-between;align-items:center;width:100%}
#pw-redesign-v3 .pw-locationlist>div>a:hover strong{color:#70B8FF}
#pw-redesign-v3 .pw-cta:disabled{opacity:.7;cursor:wait;transform:none}
#pw-redesign-v3 .pw-metal{overflow:hidden;isolation:isolate;transform-style:preserve-3d}
#pw-redesign-v3 .pw-metal:before{pointer-events:none}
#pw-redesign-v3 .pw-metal[aria-pressed=true]{box-shadow:0 17px 46px rgba(0,0,0,.22),inset 0 1px rgba(255,255,255,.2)}
#pw-redesign-v3 .pw-coastroute{position:relative;height:46px;margin:34px 0 2px;max-width:440px}
#pw-redesign-v3 .pw-routetrack{position:absolute;left:0;right:0;top:21px;height:2px;background:#425C76;overflow:hidden}
#pw-redesign-v3 .pw-routetrack i{display:block;width:100%;height:100%;background:linear-gradient(90deg,#70B8FF,#D9EBFA);transform:scaleX(0);transform-origin:left;transition:transform 1.55s cubic-bezier(.2,.75,.2,1)}
#pw-redesign-v3 .pw-coastroute b{position:absolute;left:var(--pw-stop);top:15px;width:14px;height:14px;border:2px solid #91A8C0;background:#10243B;border-radius:50%;transform:translateX(-50%) scale(.7);transition:transform .35s .2s,background .35s}
#pw-redesign-v3 .pw-coastroute b:first-of-type{transform:translateX(0) scale(.7)}
#pw-redesign-v3 .pw-coastroute b:last-of-type{transform:translateX(-100%) scale(.7)}
#pw-redesign-v3 .pw-area.pw-route-visible .pw-routetrack i{transform:scaleX(1)}
#pw-redesign-v3 .pw-area.pw-route-visible .pw-coastroute b{background:#70B8FF;transform:translateX(-50%) scale(1)}
#pw-redesign-v3 .pw-area.pw-route-visible .pw-coastroute b:first-of-type{transform:translateX(0) scale(1)}
#pw-redesign-v3 .pw-area.pw-route-visible .pw-coastroute b:last-of-type{transform:translateX(-100%) scale(1)}
#pw-redesign-v3 .pw-gallerymain img{--pw-drift-x:1.2%;--pw-drift-y:-.5%;animation:pw-finish-drift 13s ease-in-out infinite alternate;transform-origin:center}
#pw-redesign-v3 .pw-gallerymain:hover img{animation-duration:7s}
@keyframes pw-finish-drift{from{transform:scale(1.035) translate(0,0)}to{transform:scale(1.075) translate(var(--pw-drift-x),var(--pw-drift-y))}}
#pw-redesign-v3 .pw-mobileactions{display:none}
#pw-redesign-v3.pw-still .pw-routetrack i{transition:none;transform:scaleX(1)}
#pw-redesign-v3.pw-still .pw-coastroute b{transition:none;background:#70B8FF}
#pw-redesign-v3.pw-still .pw-gallerymain img{animation:none;transform:scale(1.035)}
@container(max-width:700px){
 #pw-redesign-v3 #pw-home-view{padding-bottom:62px}
 #pw-redesign-v3 .pw-mobileactions{position:fixed;z-index:50;display:grid;grid-template-columns:.72fr 1fr 1.2fr;left:0;right:0;bottom:0;min-height:58px;background:#081728F5;border-top:1px solid #4A6077;box-shadow:0 -12px 30px rgba(1,9,18,.3);backdrop-filter:blur(13px)}
 #pw-redesign-v3 .pw-mobileactions a{display:grid;place-items:center;min-height:58px;padding:8px 6px;border-right:1px solid #344A61;color:#E9F2FA;font-size:10px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;text-align:center}
 #pw-redesign-v3 .pw-mobileactions a:last-child{border-right:0;background:#2F91E8;color:#07192D}
}
@media(prefers-reduced-motion:reduce){#pw-redesign-v3 .pw-routetrack i,#pw-redesign-v3 .pw-coastroute b{transition:none}#pw-redesign-v3 .pw-gallerymain img{animation:none!important}}
"""

faq_schema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question", "name": "Do I need to be there?", "acceptedAnswer": {"@type": "Answer", "text": "No. Give us access and we handle it. Photos land in your Owner Portal after the visit."}},
        {"@type": "Question", "name": "How long does a Full Detail take?", "acceptedAnswer": {"@type": "Answer", "text": "Timing depends on length, condition and the work needed. We confirm the schedule when we quote the boat."}},
        {"@type": "Question", "name": "Wax or ceramic?", "acceptedAnswer": {"@type": "Answer", "text": "The right choice depends on the boat's finish, use and maintenance plan. Surface preparation comes first."}},
        {"@type": "Question", "name": "How often should we schedule a wash?", "acceptedAnswer": {"@type": "Answer", "text": "We match the cadence to how the boat is stored and used. Silver offers weekly, bi-weekly or monthly washes. Gold and Platinum offer a custom cadence."}},
    ],
}

business_schema = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "@id": "https://propwashmarine.com/#business",
    "name": "Propwash Marine Detailing",
    "description": "Mobile and dockside boat detailing across South Florida.",
    "url": "https://propwashmarine.com/",
    "telephone": "+1-561-291-8554",
    "image": "https://propwashmarine.com/assets/v4/hero-poster.webp",
    "areaServed": ["Stuart", "Boca Raton", "Fort Lauderdale"],
    "sameAs": ["https://instagram.com/propwashmarine"],
}

document = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>South Florida Mobile Boat Detailing | Propwash Marine</title>
<meta name="description" content="Dockside boat detailing from Stuart to Fort Lauderdale. Signature washes, Full Details, correction, wax, ceramic coating and recurring maintenance plans.">
<link rel="canonical" href="https://propwashmarine.com/">
<meta name="theme-color" content="#0A1A2F">
<meta property="og:type" content="website">
<meta property="og:title" content="South Florida Mobile Boat Detailing | Propwash Marine">
<meta property="og:description" content="Salt never sleeps. Neither do we. Dockside boat detailing from Stuart to Fort Lauderdale.">
<meta property="og:image" content="https://propwashmarine.com/assets/v4/hero-poster.webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{head_links}
<style>{styles}{live_css}</style>
<script type="application/ld+json">{json.dumps(business_schema, separators=(",", ":"))}</script>
<script type="application/ld+json">{json.dumps(faq_schema, separators=(",", ":"))}</script>
</head>
<body>
{markup}
<script>{script}</script>
</body>
</html>
'''

(ROOT / "index.html").write_text(document)

city_outputs = []
for slug, data in CITY_DATA.items():
    city_directory = ROOT / f"boat-detailing-{slug}"
    if city_directory.exists():
        shutil.rmtree(city_directory)
    city_directory.mkdir(parents=True)
    city_document = render_city_page(slug, data, styles)
    city_file = city_directory / "index.html"
    city_file.write_text(city_document)
    city_outputs.append(city_directory)

sitemap_entries = [
    f"  <url><loc>{BASE_URL}/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>"
]
sitemap_entries.extend(
    f"  <url><loc>{BASE_URL}/boat-detailing-{slug}/</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>"
    for slug in CITY_DATA
)
sitemap = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "\n".join(sitemap_entries)
    + "\n</urlset>\n"
)
(ROOT / "sitemap.xml").write_text(sitemap)

if DIST.exists():
    shutil.rmtree(DIST)
(DIST / "assets" / "logo").mkdir(parents=True)
(DIST / "assets" / "video").mkdir(parents=True)
shutil.copytree(OUT, DIST / "assets" / "v4")
for filename in ("brandmark.png", "wordmark.png", "favicon.png", "favicon-32x32.png", "favicon-16x16.png", "apple-touch-icon.png", "favicon.ico"):
    shutil.copy2(ROOT / "assets" / "logo" / filename, DIST / "assets" / "logo" / filename)
for filename in ("hero-v4.mp4",):
    shutil.copy2(ROOT / "assets" / "video" / filename, DIST / "assets" / "video" / filename)
for filename in ("index.html", "thank-you.html", "robots.txt", "sitemap.xml", "_redirects"):
    shutil.copy2(ROOT / filename, DIST / filename)
for city_directory in city_outputs:
    shutil.copytree(city_directory, DIST / city_directory.name)
print(f"Built {ROOT / 'index.html'} ({len(document.encode()):,} bytes)")
print(f"Built {len(city_outputs)} city landing page(s): {', '.join(path.name for path in city_outputs)}")
print(f"Created {len(image_sources)} optimized production images and the full hero video")
print(f"Prepared deployable folder at {DIST}")
