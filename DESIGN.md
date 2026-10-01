# DESIGN.md — Propwash Marine

Every value in this file comes from the templates and CSS in `src/`
(`v4-template.html`, `city-template.html`, `services-template.html`,
`gallery-template.html`, `faq-template.html`, `membership-template.html`).
When this file and the templates disagree, the templates win. Update this file in the
same change.

All styles are scoped under `#pw-redesign-v3`, which is also the query container
(`container-type:inline-size`). Class names use the `pw-` prefix.

> **Build-time CSS:** `build_live.py` injects additional CSS when it builds the site
> (for example, the coast route graphic in the service-area section). Those styles are
> not in `src/` and are not documented here. Read `build_live.py` before changing
> anything those styles affect.

---

## 1. Visual Theme

Dark, nautical and built like equipment: deep navy, hairline dividers, square
corners, condensed uppercase headlines and real dockside photography under dark
scrims. The feel is a working marine crew, not a luxury spa: direct, confident,
tidy.

- **Mood:** night water, salt and stainless. The page is dark (`color-scheme:dark`),
  and light sections are rare. A light section marks a change of topic, such as the
  services list.
- **Shape:** sharp rectangles (`border-radius:0` on buttons, inputs and panels).
  Structure comes from 1px lines, not shadows or fills.
- **Imagery:** full-bleed photography of real boats and real work, covered by
  navy gradient scrims so the white text stays readable. The homepage hero is a
  looping video. On narrow screens a still image replaces it.
- **Signature details:** numbered kickers (`01 / The right work`), a 26×2px
  electric-blue rule before eyebrows, the skewed hero tagline, the metal-finish
  membership cards, and the oversized PROPWASH footer mark that fills on hover.

---

## 2. Color Roles

### Blue tokens

There is one brand blue. Define it as two tokens:

| Token | Hex | Use |
|---|---|---|
| `--blue` | `#1E90FF` | **The only brand blue**, site-wide: buttons, links, accents, kicker rule, active states |
| `--blue-light` | `#70B8FF` | A tint of `--blue`, **only** for text and links on navy backgrounds |

The current CSS still uses a single `--pw-blue` variable: `#1E90FF` on the homepage and
membership page, `#70B8FF` on the city, services, gallery and FAQ pages. When those pages
are converged, split it into `--blue` and `--blue-light` and keep `--blue` at `#1E90FF`
on every page.

### Brand core

| Role | Token | Hex | Where it is used |
|---|---|---|---|
| Navy (base) | `--pw-navy` | `#0A1A2F` | Page and body background, `theme-color`, input fills, text on blue buttons, light-section text |
| Electric blue (action) | `--blue` (currently `--pw-blue` on the homepage) | `#1E90FF` | Primary CTA fill, kicker rule, hero H1 and tagline accent word, active tab and selector underline, Platinum selection |
| Graphite (surface) | `--pw-panel` (homepage) / `--pw-graphite` (membership) | `#1C2A3A` | Mobile menu, bills and outline-button hover on the homepage; membership tier cards |
| Amber (attention) | `--pw-amber` | `#F5A623` | **Only** the "by invitation" badge (`.pw-memberinvite`, text `#1C160B`) and form error notes (`.pw-formnote.pw-formerror`) |
| Green (confirmed) | `--pw-green` | `#33C48B` | **Only** "yes" marks in the membership comparison table (`.pw-yes`) and "Completed" status in the Slip portal mock (`.pw-completed`) |

### Neutrals and text

The **homepage values** for background, dividers and muted text are canonical. The subpage
templates (city, services, gallery, FAQ, membership) use a different set, listed in
*Legacy subpage values* below.

| Role | Hex | Notes |
|---|---|---|
| Primary text (off-white) | `#F4F8FC` (`--pw-white`) | Never pure white for body text. `#FFFFFF` appears only in the footer mark "P" fill and the selected Platinum pill label |
| Muted text | `#A4B1C0` (`--pw-muted`) | Secondary copy, captions, meta rows |
| Bright secondary text | `#C1CCD8`, `#D5E0EB`, `#D9E3ED` | Hero and intro paragraphs over imagery |
| Hairline | `#2A3A4D` (`--pw-line`) | Section borders, row dividers |
| Stronger hairline | `#425268` | Plan selector, location list, CTA-band tops, city/FAQ grids |
| Input border | `#566779` (quote form), `#526A82` (member form) | |
| Outline button border | `#536073` | |
| Text-link underline | `#627286` | |

### Section backgrounds (dark to light)

| Hex | Used for |
|---|---|
| `#0B1828` (`--pw-deep`) | Footer, trust strip, proof line, portal frames |
| `#0A1A2F` | Default sections |
| `#0B192A` | Full Detail viewer section |
| `#0D2035` | Membership, process steps, FAQ hero, comparison table |
| `#10243B` | Service-area band, city local section, neighbor links, lead forms |
| `#12263C` | Dock journal |
| `#15283E` | Quote section and closing CTA bands on every page |
| `#E8F1FA` (`--pw-ice`) / `#E8EFF6` / `#EAF3FA` | Light sections: homepage services, subpage service grid, form confirmation |

### Legacy subpage values — converge during redesign

The subpage templates redefine these variables. They are documented so the current
pages can be read correctly. Do not use them in new work. Replace them with the canonical
values above during the redesign.

| Variable | Legacy subpage value | Canonical value |
|---|---|---|
| `--pw-deep` | `#071523` | `#0B1828` |
| `--pw-panel` | `#15283E` | `#1C2A3A` |
| `--pw-line` | `#34465C` | `#2A3A4D` |
| `--pw-muted` | `#A9B8C9` | `#A4B1C0` |
| `--pw-blue` | `#70B8FF` | `#1E90FF` (`--blue`); use `--blue-light` for text and links on navy |

On light sections, text is `#0A1A2F`, secondary text is `#44566A`/`#40546A`, lines are
`#B4C4D4`/`#AEBFD0`, and the link/active blue darkens to `#0969C5` / `#0866BC`.

### Interaction blues

| Hex | Role |
|---|---|
| `#4FA9FF` | Focus outline (`3px solid`, `outline-offset:5px`), CTA hover fill, nav link hover |
| `#70B8FF` | `--blue-light`: text and links on navy only (link hovers, FAQ `+` marks, home-base marker). Never for buttons or fills |
| `#3197FA` | Selected Full Detail thumbnail border and inset underline |

### Membership tier colors (used only in tier contexts)

| Tier | Accent rule / CTA fill | Headline | Mobile pill (selected) |
|---|---|---|---|
| Silver | `#C2D1DB` | `#DCE7ED` | `#C4D4E6`, navy label |
| Gold | `#C8A34A` | `#E8CC87` (card name `#E9D3A9`) | `#D9BC82`, navy label |
| Platinum | `#58A7F6` | `#8EC8FF` | `#1E90FF`, `#FFFFFF` label |

### Scrims and overlays

- Hero video: `linear-gradient(90deg, rgba(5,17,32,.84) 0%, rgba(5,17,32,.53) 50%, rgba(5,17,32,.08) 100%)` stacked with a vertical fade to `#0A1A2F`.
- Subpage heroes: `linear-gradient(90deg, rgba(6,19,33,.96) 0%, rgba(6,19,33,.8) 48%, rgba(6,19,33,.25–.42) 100%)` plus `linear-gradient(0deg, rgba(6,19,33,.86), transparent 50%)`.
- Image captions: bottom fade `linear-gradient(transparent, rgba(10,26,47,.9–.95))` starting at 40–50% height.
- Sticky nav on subpages: `#0A1A2FEF`.

---

## 3. Typography

Loaded from Google Fonts:
`Oswald:wght@400;500;600;700` and `Inter:wght@400;500;600`, `display=swap`.

| Family | Stack | Role |
|---|---|---|
| Oswald | `Oswald, 'Arial Narrow', Arial, sans-serif` | All `h1`–`h3`, tier names, numerals, phone numbers, list items that act as headings. **Always uppercase.** |
| Inter | `Inter, Arial, sans-serif` | Body, UI, labels, eyebrows, buttons |

Base: `font: 400 15px/1.65 Inter`.

### Scale

| Element | Font | Size | Weight | Line height | Tracking |
|---|---|---|---|---|---|
| Homepage hero tagline (`.pw-v2herotagline`) | Oswald | `clamp(44px, 8.6cqw, 96px)` | 600 | 1.03 | -.015em, `skewX(-5deg)`, accent line in `#1E90FF` |
| Homepage hero H1 (`.pw-v2herocopy h1`) | Inter | `clamp(14px, 1.7cqw, 17px)` | 600 | 1.5 | .14em, blue, uppercase (the SEO line, set small above the tagline) |
| Subpage H1 | Oswald | city `clamp(56px,8.2cqw,100px)`; services/gallery `clamp(52px,7.6cqw,92px)`; FAQ `clamp(50px,7.4cqw,88px)`; membership `clamp(48px,7.2cqw,84px)` | 500 | 1.01–1.04 | -.025em |
| H2 | Oswald | `clamp(36px, 5.3cqw, 62px)` | 500 | 1.1 | -.015em |
| Closing CTA H2 | Oswald | `clamp(38–48px, 5.4–6.8cqw, 64–80px)` | 500 | 1.05–1.1 | |
| H3 | Oswald | 24px (range 19–45px by component) | 500 | 1.25 | |
| Step / display numerals | Oswald | 38–43px | 400 | 1 | color `#74869B` / `#7590AB` |
| Phone number | Oswald | 31–32px | 400 | 1 | |
| Body | Inter | 15px | 400 | 1.65–1.8 | |
| Secondary body | Inter | 12–14px | 400 | 1.75–1.85 | |
| Eyebrow (`.pw-eyebrow`) | Inter | 11px | 500 | 1.6 | .16em, uppercase |
| CTA label (`.pw-cta`) | Inter | 12px | 600 | 1.4 | .075em, uppercase |
| Nav links | Inter | 10px | 400 | — | .08em, uppercase |
| Breadcrumbs | Inter | 10px | 400 | — | .08em, uppercase |
| Notes and fine print | Inter | 11px | 400 | 1.75 | The template raises these small labels to 11px |

Rules:
- Headings are Oswald and uppercase every time. Body text is Inter and sentence case.
- Large display type uses negative tracking. Small uppercase Inter uses wide tracking (.07–.27em).
- Scale headings with container units (`cqw`) inside `clamp()`, not viewport units.
- Headlines break with `<br>` into short, deliberate lines ("Salt never / sleeps. / Neither do we.").

---

## 4. Components

### Buttons and links
- **Primary CTA** `.pw-cta`: blue `#1E90FF` fill and border, navy text, `padding:15px 22px`, `min-height:50px`, 12px/600 uppercase, `.075em`, followed by a `.pw-arrow` span. On hover the fill changes to `#4FA9FF` and the button rises `translateY(-2px)` over `.2s`. Square corners.
- **Outline CTA** `.pw-cta.pw-outline`: transparent, off-white text, `#536073` border. On hover it fills with the panel color.
- **Nav CTA**: `padding:12px 17px`, `min-height:44px`, 10px.
- **Text link** `.pw-textlink`: inline, 12px/500, 1px bottom border `#627286`, `min-height:44px`.
- **Quote CTA label:** always "Get a free quote", everywhere it appears: buttons, nav, hero,
  footer, mobile menu and form labels.
- Other labels in use: "Request a quote", "Explore the work", "Tell us the boat", "See membership plans", "Compare the tiers", "Send request".

### Kicker / eyebrow
`.pw-kicker` puts a 26×2px `--blue` bar before a numbered eyebrow:
`01 / The right work`, `02 / Full Detail, up close`, `03 / A higher standard of care`, and so on.
Home sections are numbered in order.

### Navigation
Logo lockup (brandmark 73×53 plus wordmark 194px, 9px tagline tracked .27em), centered
uppercase 10px links, "Client login" with an underline, and a compact blue CTA. The nav is 106px tall on the homepage,
with a `#F4F8FC25` bottom rule. Below 800px the links collapse into a bordered `Menu +` button
that opens a two-column `.pw-mobilemenu` on the panel color.

### Hero
- **Homepage:** full-bleed looping video (`pw-v2hero`) with the scrim, a small blue H1, the
  skewed Oswald tagline, a 15px intro (max 520px), two CTAs, and a bottom row with a
  pause-video control (`#0A1A2F8F` fill, translucent border).
- **Subpages:** `.pw-cityhero` photo hero, 520–660px tall, content aligned to the bottom,
  breadcrumbs → kicker → H1 → intro → actions.

### Trust strip (`.pw-v2trust`)
Four columns on `#0B1828` separated by `#344256` rules: an Oswald 20px uppercase label plus
a 10px `#A6B8CC` line (such as "Marina-approved", "We come to you"). Two by two below 600px.

### Service accordion
Items separated by lines, each with a number, an Oswald 23px name and a `+` mark (turns
`#0969C5` when open). It sits on the ice background. The open panel (`.pw-servicepanel`,
`#D7E4F0`) pairs a 250px image with copy.

### Full Detail viewer
A large figure (min 540px) with a caption scrim beside a two-column thumbnail grid.
Thumbnails are `#14283E` with a `#394D64` border. When selected they get a `#3197FA`
border and a 3px inset underline.

### Before/after comparison
Clip-path split image, 2px off-white divider, a 48px blue circular handle with a 4px
off-white ring, square BEFORE/AFTER labels on navy, and an invisible range input for
control.

### Membership cards (`.pw-metal`)
Three cards with metal-gradient fills (`linear-gradient(140deg, …)`) and a 1px tinted
border. A diagonal sheen sweeps across on hover and the card lifts `-5px`. The selected
card gets a 4px bottom bar in the tier color and a soft shadow. The Oswald name is set at
`clamp(32px,4.15cqw,47px)`. Below 600px the cards become a sticky row of tier-colored pills
(3px radius).

### Membership tier grid (subpage)
Three graphite `#1C2A3A` cells on a 1px `--pw-line` gap grid. Platinum carries the amber
"by invitation" badge (9px, .12em, uppercase, 600).

### Comparison tables
12px cells, `13–16px` padding, `#34465C` row rules, header `#D9E5F2`/500, row heads
`#AFBFD1`–`#C4D1DE`. Green `#33C48B` 600 marks only affirmative cells. Tables sit in a
horizontal-scroll wrapper with `min-width:510–540px`.

### Owner Portal / My Slip frames
`.pw-slipshell` and `.pw-realportal` are deep-navy frames with a `#425268`/`#45586D` border and
the site's only large shadows (`0 25px 70px #020A1466`, `0 22px 65px #0004`). The slip shell
tilts `perspective(1300px) rotateY(-5deg)` and flattens on hover. Tabs are 11px with a 2px
blue underline when active.

### Gallery
Homepage: a large main image (min 450px, zooms 1.04 on hover) beside a two-by-two thumbnail
grid with a cursor-following blue radial spotlight (`rgba(30,144,255,.16)`). Gallery page:
a three-column grid, 290px images, **4px radius** with a `#21374F` border, and Oswald 16px
captions over a bottom scrim.

### FAQ
Native `<details>`. The homepage uses 13px summaries with a `+`/`−` in `#B8C9DC`. The FAQ page
uses Oswald 22px uppercase summaries with a `#70B8FF` `+`/`–`, 14px answers in `#C3D0DE`,
and a max width of 740px.

### Forms
Two-column field grid (one column below 400px on the homepage, below 700px for the member
form). Labels are 11px in `#CED9E5`. Inputs are square, 1px `#566779` border, navy fill,
`padding:12px 13px`, `min-height:48px`, 14px text (16px below 700px). Placeholders are
`#96A6B9` at 12px. A progress row sits on top ("Step 1 of 2" style, bold current step).
Notes are 11px `#A9B8CA`, and errors switch to amber. The confirmation panel has a
`#526A83` border, and the full confirmation page uses the light `#EAF3FA` surface.
Member forms tint the focus border and CTA with the tier color.

### Closing CTA band
Used on every page: `#15283E`, `#425268` top rule, two-column grid (`1fr .8fr`), large H2
and 14px copy on the left, contact block on the right (Oswald 31px phone, 12px links,
`#53687D` rule).

### Footer
Deep navy, three-column top (`1.4fr 1fr 1fr`), 11px link lists with eyebrow headers,
9–11px legal row. The oversized PROPWASH SVG mark starts as a `#33465C` stroke outline. On
footer hover it fills left to right (P white, W `#1E90FF`) over `.9s cubic-bezier(.4,0,.2,1)`
with a single sheen sweep.

### Chips
Neighbor-city and member-city links are bordered `#52667B` boxes, `padding:11–12px 15px`,
11px. On hover the border and text turn blue.

---

## 5. Layout

- **Gutters:** `.pw-wrap` uses `padding-left/right: 4.5%`. The full-bleed trust strip and proof line use percentages as well.
- **Section rhythm:** `.pw-section` padding is 112px top and bottom above 700px and 40px at ≤700px. Section heads sit 56px above their content (24px on mobile).
- **Section heads:** `.pw-sectionhead` is a flex row with the H2 on the left and a short muted
  paragraph (max 265–310px) on the right, aligned to the bottom. It stacks at ≤700px.
- **Grids are asymmetric:** `1.45fr 1fr` (hero head), `.93fr 1.07fr` (services), `1.35fr 1fr`
  (gallery), `1.15fr .85fr` (plan panel), `.72fr 1.28fr` (portal), `1fr .8fr` (CTA bands).
  Even three- and four-column grids are for peers (plans, steps, trust).
- **Dividers over gaps:** peer grids often use `gap:1px` on a line-colored background, or
  shared `border-top/left` plus per-cell `border-right/bottom`, to draw a ruled table.
- **Measure:** intro copy max 520–650px. FAQ answers max 740px. Forms max 680–860px.
- **Depth:** flat by default. Shadows are only for floating product frames (portal, slip
  shell) and the selected membership card.
- **Radius:** 0. The only exceptions are gallery-page tiles (4px), mobile tier pills (3px), the
  comparison handle and portal bullet dots (circles).
- **Motion:** see section 6.

---

## 6. Motion

### Feel
Subtle and premium. Motion should be noticed only if you look for it. It confirms that the
page is alive and well made; it never performs. The reference is Freeman Boatworks
(freemanboatworks.com, inspected September 2026): one quiet fade-and-rise as content
enters, images that fade rather than fly, and no hover theatrics.

**What Freeman does (measured, not copied):** a Squarespace site with no animation library
(no GSAP, Lenis or AOS). Its site-wide "fade / flex / ease" setting moves each element from
`opacity:0; translateY(18px)` to its resting state over `0.5s cubic-bezier(0.19, 1, 0.22, 1)`,
triggered once as the element scrolls into view, with a ~15ms stagger between neighbors.
Images fade in without moving. Text links and buttons change color over `0.6s` on the same
curve. There is no parallax, no hover lift or zoom, no looping animation and no hero video,
and the header simply scrolls away.

### Tokens

| Token | Value | Use |
|---|---|---|
| `--ease-soft` | `cubic-bezier(0.19, 1, 0.22, 1)` | Default for everything that moves: fast start, very long soft landing |
| `--ease-fade` | `cubic-bezier(0.4, 0, 0.2, 1)` | Opacity-only fades and color changes |
| `--dur-reveal` | `700ms` | Section fade-and-rise |
| `--dur-image` | `900ms` | Image fade-in and settle zoom |
| `--dur-hover` | `300ms` | Hover lifts, color and border changes |
| `--rise` | `16px` | Reveal travel distance. Never more than 24px |

Durations are slower than Freeman's 0.5s on purpose. The curve spends most of its time
settling, so 700ms still feels calm rather than sluggish.

### Allowed
- **Section reveal:** opacity 0→1 and `translateY(var(--rise))`→0 over `--dur-reveal` with
  `--ease-soft`. It triggers once, when about 15% of the element is visible, and never replays.
  A group of siblings (cards, steps, thumbnails) may stagger by 60ms, up to 4 items. Items after
  that appear with the last step.
- **Image entrance:** fade in over `--dur-image`. Hero or feature images may also settle from
  `scale(1.04)` to `scale(1)` over the same duration.
- **Parallax:** background photography only, `transform` only, at most 32px of travel across
  the image's time on screen. Off below 700px and on touch devices.
- **Hover lift:** cards and buttons rise `translateY(-2px)` over `--dur-hover`. Images inside a
  card may zoom to at most `scale(1.03)` over 600ms. Color and border changes use `--dur-hover`
  with `--ease-fade`.
- **State changes** (accordions, tabs, form steps): the section reveal, shortened to 350ms.

### Never
- Bouncing, overshoot or elastic easing (no curve with values outside 0–1).
- Spinning, rotating, pulsing or blinking.
- Anything that keeps moving on its own: infinite loops, ambient drift, marquees, auto-advancing
  carousels.
- Several things animating at once. One reveal group at a time; nothing else moves while a
  section reveals.
- Motion that delays reading or tapping: no hidden-until-animated hero text, no entrance on
  content already on screen at load, no delay on `:active` or tap feedback, no scroll-jacking
  or smooth-scroll libraries.
- Animating layout properties (`width`, `height`, `top`, `margin`). Use `transform` and
  `opacity` only, and never `transition: all`.

### Reduced motion
Always respect `prefers-reduced-motion: reduce`, and keep the `.pw-still` switch working the
same way:
- No transforms at all: no rise, zoom, parallax or hover lift.
- Content appears at full opacity immediately; a fade of 150ms or less is acceptable.
- The hero video shows its poster image and does not play.
- Color and focus changes still happen, without transitions.

Reveal styles must be applied by script. If the script fails or never runs, all content is
visible. In the template this is `.pw-reveal` / `.pw-in-view`: each direct child of a `#pw-main`
section reveals once, card groups (`.pw-steps`, `.pw-v2plans`, `.pw-journalgrid`,
`.pw-gallerychoices`, `.pw-moments`, `.pw-portalfeatures`) stagger their children, and anything
already on screen at load never animates.

### Current site vs this standard
The live homepage predates this section. These pieces break the rules above and should be
replaced during the redesign:

| Current | Rule it breaks |
|---|---|
| Hero image `pw-ocean-drift`, 18s infinite (scale 1.02→1.09) | Constantly moving |
| Gallery `pw-finish-drift`, 13s infinite (injected by `build_live.py`) | Constantly moving |
| Metal card −5px lift with a diagonal sheen sweep | Lift above 2px; several effects at once |
| Slip shell `rotateY(-5deg)` tilt that flattens on hover | Rotation |
| Footer mark fill and single sheen sweep on hover | Large decorative motion |
| `pw-in` starting at opacity .2, over .35s/.75s `ease-out` | Use the tokens above |

The coast-route line in the service-area section (injected by `build_live.py`, 1.55s, plays
once on scroll) already fits, but should move to `--ease-soft`.

### Future (not now)
A large, cinematic moving hero video. When it comes, it must still follow this section: a
poster image first, a visible pause control, the poster only under reduced motion, no autoplay
below 700px, and no text that waits for the video before it can be read.

---

## 7. Do's and Don'ts

### Do
- Use navy `#0A1A2F` as the base and switch between the documented section shades to separate bands.
- Keep electric blue for action and emphasis: CTAs, the kicker rule, active states, one accent
  word in a headline.
- Set every heading in uppercase Oswald and all running text in Inter.
- Put a scrim under any text that sits on a photo.
- Use real Propwash photography of boats, details and work in progress.
- Number home sections with the `NN / Label` kicker.
- Keep tap targets at least 44px tall (nav links, text links, tabs, menu button).
- Keep the 3px `#4FA9FF` focus outline on every interactive element.
- Keep the tier colors (silver, gold, platinum) inside membership contexts.

### Don't
- Don't use amber for decoration. It means "by invitation" or "error" and nothing else.
- Don't use green for decoration. It means "yes" or "completed".
- Don't round buttons, inputs or panels, and don't add drop shadows to cards.
- Don't use pure white `#FFFFFF` for body text. Use `#F4F8FC`.
- Don't introduce new fonts, weights beyond those loaded, or colors not listed here.
- Don't use viewport breakpoints (`@media (max-width)`) for layout. Use `@container`.
- Don't autoplay the hero video on narrow containers. The still image replaces it at ≤700px.
- Don't use stock photography or illustrations.

---

## 8. Responsive Behavior

Layout responds to the width of `#pw-redesign-v3` through **container queries**. The only
`@media` queries are for reduced motion.

| Container width | Changes |
|---|---|
| ≤1000px | Client login hidden. Metal card padding tightens |
| ≤900px | Nav gaps shrink. Section padding 62px. Hero and image heights reduce. Portal features stack |
| ≤800px | Nav links collapse to the `Menu +` button. Subpage grids go to two columns (services, steps, gallery). Local and CTA bands stack |
| ≤700px | Hero video hidden and still image shown. Hero, service, result, plan, portal, gallery, area, FAQ and quote grids go to one column. Steps go two by two. Inputs go to 16px. Section padding 52px. Slip shell stops tilting |
| ≤600px | Nav CTA hidden. Logo shrinks (brandmark 55×42, wordmark 160px). Tagline is `10.1cqw`. Trust strip is two by two. Membership cards become a sticky tier-pill row. Member band is 240px tall |
| ≤520px | Subpage nav is 79px. Subpage grids go to one column. H1 is `clamp(40px,12cqw,52px)` (city 42–50px). City hero content is reordered so the first CTA comes earlier |
| ≤430px | Service panel image 215px. Detail viewer 390px. Member-nav brandmark hidden |
| ≤400px | Proof line becomes rows with right-aligned values. Quote form is one column. Image-count label hidden |
| ≤370px | Smallest logo (brandmark 45×36, wordmark 146px). Tagline is `10.6cqw`. Smallest CTA (9px) |

Mobile rules: hero `<br>` breaks inside body copy are hidden, horizontal-scroll wrappers
keep tables readable, and nothing should cause a horizontal page scroll.

---

## 9. Voice and Copy Rules

These rules apply to every string on the site, including alt text, meta descriptions,
button labels and form notes.

1. **We, us, our (confirmed).** The company always speaks in the first-person plural. Never "I", "me"
   or "my", and never the company name in the third person ("Propwash offers…"). Address
   the owner directly as "you/your".
2. **"Full Detail" and "Slip" are always capitalized**, including in running text, alt text
   and headings ("at your Slip", "My Slip", "a separately quoted Full Detail").
3. **No prices.** No dollar figures, rates or discounts in copy (including "starting at").
   Work is custom quoted, and the copy says so ("Every plan is custom quoted", "We quote it
   straight"). "Free quote" is allowed. Never call a service or feature "free".
4. **No superlatives or stock marketing language.** No "best", "premier", "top-rated",
   "world-class", "unmatched", "luxury experience", "second to none", and so on. Say what we do
   and how.
5. **No BBB claims** or third-party accreditation badges we cannot show.

**How the site sounds:** short, plain declaratives, often in pairs. It is specific about process
and honest about limits.
- "Salt never sleeps. Neither do we."
- "We handle the wash, the correction and the coating. You handle the throttle."
- "Preparation first. Ceramic second."
- "We never coat over oxidation or wax."
- "We watch the forecast and move the visit rather than rush the job."

Service and plan names are proper nouns: Signature Wash, Full Detail, Wax Protection,
Compound + Polish, Ceramic Coating, Maintenance Plans, Trip Ready, Freshwater Rinse,
Silver, Gold, Platinum, Owner Portal, My Slip.

Service area wording: "Based in Boca Raton. Mobile detailing from Stuart to Fort
Lauderdale, at your Slip, lift or driveway."

---

## 10. Agent Prompt Guide

Paste this when asking an agent to build or change a Propwash page:

> Build inside `#pw-redesign-v3` using the existing `pw-` classes and the tokens in DESIGN.md.
> Base background navy `#0A1A2F`, text `#F4F8FC`, muted `#A4B1C0`, hairlines `#2A3A4D`,
> deep `#0B1828` (homepage values are canonical; the subpage set is legacy).
> `--blue` `#1E90FF` is the only brand blue: buttons, links, accents, active states.
> `--blue-light` `#70B8FF` only for text and links on navy. Graphite `#1C2A3A` for card
> surfaces. Amber `#F5A623` only for the invitation badge and form errors. Green `#33C48B` only for yes/completed marks.
> Headings in Oswald, uppercase, weight 500 (600 for hero), tight negative tracking,
> sized with `clamp(…cqw…)`. Body in Inter 15px/1.65. Eyebrows 11px uppercase .16em
> behind a 26×2px blue rule with a `NN / Label` number. Square corners, 1px rules, no
> card shadows. Photos under navy gradient scrims. Section padding 80/62/52px, gutters 4.5%.
> Responsive with `@container` at 900/800/700/600/520px. Motion is subtle: one fade-and-rise
> per section (700ms, `cubic-bezier(0.19, 1, 0.22, 1)`, 16px), 2px hover lifts, nothing that
> loops, bounces or spins. Respect reduced motion.
> Copy: the company speaks as we/us/our and addresses the owner as you/your. Capitalize "Full Detail" and "Slip". Quote CTA is always
> "Get a free quote". No dollar figures, rates or discounts, and never call a service or
> feature "free". No superlatives or stock marketing phrases, no BBB claims. Short, plain, specific sentences.

Quick checks before shipping:
- [ ] Every color used appears in section 2.
- [ ] Headings are Oswald uppercase. Body text is Inter.
- [ ] Amber and green appear only in their single roles.
- [ ] No `border-radius` beyond the listed exceptions.
- [ ] Tap targets are at least 44px, the focus outline is intact, and reduced motion is honored.
- [ ] Motion follows section 6: nothing loops, bounces or spins, and nothing moves at once with a reveal.
- [ ] Copy passes all five voice rules in section 9.
