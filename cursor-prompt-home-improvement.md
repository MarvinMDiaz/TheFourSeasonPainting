# Cursor Prompt — The Four Season Painting Website

> Paste this entire prompt into Cursor's Composer (Cmd+I or Ctrl+I) to scaffold the project.

---

## PROMPT START

Build a complete, fully responsive website for **The Four Season Painting**, a professional painting contractor. Use **Python Flask** with **Jinja2 templates**, **Tailwind CSS via CDN**, and **Alpine.js via CDN**. The design must closely follow the reference style described in each section below — modern, dark-hero, gold-accent, with floating white form cards and overlapping photo collages.

---

### TECH STACK

- **Framework:** Python Flask
- **Templating:** Jinja2 (built into Flask)
- **Styling:** Tailwind CSS (via CDN `<script>` tag — no build step needed)
- **Interactivity:** Alpine.js (via CDN) — mobile menu, form state, gallery filter
- **Email:** AWS SES via `boto3`
- **Before/After slider:** Vanilla JavaScript
- **Icons:** Font Awesome 6 (via CDN)
- **Fonts:** Google Fonts — `DM Sans` (body) + `Manrope` (headings, bold/black weight)
- **Environment vars:** `python-dotenv`

---

### PROJECT STRUCTURE

```
/app.py                     → Flask app, all routes
/templates
  /base.html                → Shared layout (nav + footer + CDN scripts)
  /index.html               → Home page (all sections)
/static
  /css/custom.css           → Animations and overrides Tailwind can't do
  /js/gallery.js            → Before/after slider logic
  /js/main.js               → Mobile menu, smooth scroll, navbar scroll shadow
  /images/
    /logo.png               → The Four Season Painting logo (convert PDF → PNG)
    /hero-bg.jpg            → Dark painting/job site photo for hero background
    /about-1.jpg            → About section photo 1
    /about-2.jpg            → About section photo 2
    /team-badge.jpg         → Small dark overlay card photo
    /gallery/               → Before/after project images
/.env                       → AWS credentials (never commit)
/requirements.txt
```

---

### GLOBAL DESIGN RULES

Follow these rules across every section:

**Colors (add to Tailwind inline config):**
```js
tailwind.config = {
  theme: { extend: { colors: {
    primary:   '#0a1628',   // deep dark navy — headings, footer bg, hero overlay
    secondary: '#1e3a5f',   // mid dark blue — card borders, section accents
    accent:    '#5bb8f5',   // baby blue — CTAs, highlights, active states, icons
    accentdark:'#2e86c1',   // deeper baby blue — hover states, button hover
    dark:      '#060e1a',   // near-black navy — footer, darkest backgrounds
    lightblue: '#e8f4fd',   // very light baby blue tint — alternating section bg
  }}}
}
```

**Color usage rules:**
- Dark navy (`primary`) everywhere that was previously dark: hero overlay, footer, section headings
- Baby blue (`accent`) everywhere that was previously gold or crimson: CTA buttons, icons, active nav pill, checkmarks, hover states, "Read More" links
- Light blue tint (`lightblue`) for alternating section backgrounds instead of gray
- White cards on `lightblue` backgrounds, `lightblue` cards on white backgrounds
- All text on dark backgrounds: white headings, `text-blue-100` for body text

**Typography:**
- All section headings use a **two-tone pattern**: first line in `text-primary font-black`, second line in `text-accent font-black` (baby blue accent)
- Body text: `text-gray-600` on light backgrounds, `text-blue-100` on dark
- Section label pills: `inline-flex items-center gap-2 bg-lightblue border border-accent/30 rounded-full px-4 py-1 text-sm text-accent font-medium shadow-sm`

**Spacing:**
- Section padding: `py-24 px-6` with inner container `max-w-7xl mx-auto`
- Alternating backgrounds: white → `lightgray` → white → `lightgray`

**Cards:**
- White background, `rounded-2xl`, `shadow-sm hover:shadow-lg`, `border border-gray-100`
- Transition: `transition-all duration-300`

---

### SECTIONS TO BUILD

Build in this order and compose in `index.html`:

> **Section order:** Navbar → Hero → About Us → Services → **Before & After Gallery** → Why Choose Us → Google Reviews → Contact → Footer

---

#### 1. NAVBAR

**CRITICAL: The navbar must be `position: fixed` (not sticky) so it floats transparently over the hero. The hero must be full viewport height with no white gap above it.**

**Overall — the navbar starts TRANSPARENT and only becomes white on scroll:**
```html
<nav x-data="{ open: false, scrolled: false }"
     @scroll.window="scrolled = window.scrollY > 60"
     :class="scrolled ? 'bg-white shadow-md border-b border-gray-100' : 'bg-transparent'"
     class="fixed top-0 left-0 right-0 z-50 transition-all duration-300">
```

This means:
- When the page is at the top: navbar is fully transparent, sitting over the hero image — no white bar visible at all
- Once the user scrolls down 60px: navbar transitions to solid white with shadow

**Three-part layout** using `flex items-center justify-between px-8 py-4 max-w-full`:

- **Left:** Logo image (`/static/images/logo.png`) — **`height: 128px`**, auto width. Use inline style `style="height:128px;width:auto"` to ensure it renders at full size.

- **Center:** Nav links wrapped in a pill container that also adapts to scroll state:
  - Container: `:class="scrolled ? 'bg-gray-100' : 'bg-white/20 backdrop-blur-sm'" class="rounded-full px-2 py-1.5 flex items-center gap-1"`
  - Each link: `:class="scrolled ? 'text-gray-600 hover:text-gray-900' : 'text-white hover:text-white/80'" class="px-5 py-1.5 rounded-full text-sm font-medium transition"`
  - The **active "Home" link** gets: `bg-white text-gray-900 font-semibold shadow-sm rounded-full` (always white pill)
  - Links: Home, About, Services, Gallery, Reviews — and then `"Contact"` as a **filled solid baby blue pill button** styled differently from the other links: `bg-accent text-white font-semibold px-5 py-1.5 rounded-full hover:bg-accentdark transition` — it sits as the last item inside the nav pill container but looks like a CTA button
  - This replaces the separate right-side Contact Us button — there should be NO separate button on the right side of the navbar at all

- **Right:** Nothing — remove the standalone Contact Us button entirely.

**Mobile (below `md` breakpoint):**
- Hide center nav with `hidden md:flex`
- Show hamburger `fa-bars` on the right with `md:hidden`
- `@click="open = !open"` toggles `x-show="open"` full-width white dropdown

**Hero must add top padding to account for fixed navbar:**
- The hero section itself must have `pt-20` or `padding-top: 80px` so content isn't hidden behind the fixed navbar — BUT the background image must still start from the very top of the viewport (use a wrapper with `min-h-screen relative` and a absolutely positioned background).

Smooth scroll: add `html { scroll-behavior: smooth; }` to `custom.css`.

---

#### 2. HERO

**Layout:** Full viewport height (`min-h-screen`), dark background image with overlay, split content.

**Background:**
- Use `/static/images/hero-bg.jpg` (placeholder: `https://picsum.photos/seed/heropainting/1600/900`)
- Overlay: `bg-gradient-to-r from-black/80 via-black/60 to-black/30`

**Left side (roughly 55% width on desktop):**
- Large heading (white, `text-5xl md:text-7xl font-black leading-tight`) — no icons or avatar circles above it, go straight into the headline:
  ```
  Professional
  Painting Services
  For Every Season
  ```
- Subtext: `"Interior & Exterior Painting — Licensed, Insured & Built to Last"` — `text-gray-300 text-lg mt-4`
- CTA row (`flex items-center gap-6 mt-8 flex-wrap`):
  - Primary button: `"Get a Free Estimate"` — `bg-accent text-white rounded-full px-8 py-4 font-bold text-lg hover:bg-accentdark transition shadow-lg`
  - Secondary: phone icon (`fa-phone`, baby blue) + two lines of text:
    - Line 1: `"Call us Today"` — `text-white/70 text-sm`
    - Line 2: `"703-944-5717"` — `text-white font-bold text-lg`
- Below the CTA row, add a small trust bar (`flex gap-6 mt-6 flex-wrap`):
  - Three items each with a baby blue checkmark icon: `"Free Estimates"` · `"Licensed & Insured"` · `"5-Star Rated"`
  - Each: `text-white/80 text-sm flex items-center gap-2`

**Right side — Floating white form card:**
- `bg-white rounded-3xl shadow-2xl p-8 max-w-md w-full`
- Heading inside card: `"Get Started Now"` — `text-primary font-black text-2xl`
- Subtext: `"Fill out the form and we'll get back to you promptly."`
- Fields (no labels, use placeholder text only): Your Name, Email Address, Phone Number, Message (textarea)
- Submit button: `"Send Message"` — full width, `bg-paintblue text-white rounded-xl py-3 font-bold hover:bg-primary transition`
- This form POSTs to `/contact` via Alpine.js `fetch` — same AWS SES route

**On mobile:** stack vertically, form card below the text, both full width.

---

#### 3. ABOUT US

**Background:** `lightgray`

**Layout:** Two columns on desktop (`lg:grid-cols-2 gap-16 items-center`), stacked on mobile.

**Left — Photo collage:**
- Three photos arranged in an overlapping stack:
  - Large photo behind (full column width, rounded-2xl): painting job site — `https://picsum.photos/seed/paint1/600/400`
  - Smaller photo overlapping bottom-left (positioned absolute, `-translate-x-8 translate-y-8`, `w-2/3`, shadow-xl): `https://picsum.photos/seed/paint2/400/300`
  - Dark navy overlay card (absolute, bottom-right of the collage, `bg-primary text-white rounded-2xl p-5 shadow-xl w-48`):
    - Icon: paint brush (Font Awesome `fa-paint-roller` in gold)
    - Text: `"Painting Excellence"` bold white
    - Subtext: small gray-300 description

**Right — Text content:**
- Pill label: `• About Us` (crimson dot)
- Heading (two-tone): `"Building Trust Through"` (dark) + `"Quality Home Improvement"` (accent baby blue)
- Paragraph (SEO-friendly, use this exact copy):
  ```
  For over 20 years, The Four Season Painting has been the trusted name in home improvement across Northern Virginia. From Burke and Springfield to McLean and Great Falls, our licensed and insured team delivers exceptional results — on time, every time. We proudly serve Burke, Springfield, Fairfax, Clifton, Centreville, Chantilly, Manassas, Alexandria, Lorton, Woodbridge, Dumfries, Stafford, Bristow, Falls Church, Tysons Corner, McLean, and Great Falls.
  ```
- **2-column checklist** (`grid grid-cols-2 gap-3 mt-6`), 8 items each with a baby blue `✓` icon — home improvement focused:
  - Licensed & Insured Contractors, 20+ Years of Experience, Interior & Exterior Experts, Bathroom & Kitchen Remodeling, Electrical & Plumbing Services, Drywall & Finishing, Fence & Carpentry Work, Roof Repair Specialists

---

#### 4. SERVICES

**Background:** `bg-lightblue` (very light blue tint)

**Header (centered):**
- Pill label: `• Our Services`
- Two-tone heading: `"Transform your space with"` (dark) + `"our expert services"` (accent baby blue)

**Cards grid:** `grid grid-cols-2 lg:grid-cols-4 gap-4 mt-14`

Each card is a **dark image card** with a photo background and gradient overlay:

Card wrapper: `rounded-2xl overflow-hidden relative h-56 group cursor-pointer`

Structure inside each card:
1. Background image: `absolute inset-0 w-full h-full object-cover transition-transform duration-500 group-hover:scale-105`
2. Gradient overlay: `absolute inset-0 bg-gradient-to-t from-[#060e1a]/95 via-[#060e1a]/30 to-transparent`
3. Content block (absolute, bottom): `absolute bottom-0 left-0 right-0 p-4`
   - Icon: Font Awesome, `text-accent text-xl mb-1`
   - Title: `text-white font-bold text-sm leading-snug`
   - Description: `text-white/60 text-xs mt-1 leading-relaxed`

**NOTE — fallback style:** If the client prefers a lighter look, revert to the horizontal card layout (Option C) with `bg-slate-100` icon blocks and baby blue accent bars.

Services (FA icon + stock image URL + title + description):
- Interior & Exterior Painting → `fa-paint-roller` · `https://images.unsplash.com/photo-1562259949-e8e7689d7828?w=800&q=80` — "Premium finishes that protect and beautify your home for years to come."
- Bathroom & Kitchen Remodeling → `fa-sink` · `https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&q=80` — "Full remodels that blend function and beauty — from tile to fixtures, we handle it all."
- Electrical & Plumbing → `fa-bolt` · `https://images.unsplash.com/photo-1621905251189-08b1da9227ef?w=800&q=80` — "Licensed electrical and plumbing work done safely, cleanly, and up to code."
- Fence & Carpentry → `fa-hammer` · `https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80` — "Custom fencing, decks, and carpentry crafted to endure every season."
- Drywall & Finishing → `fa-layer-group` · `https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800&q=80` — "Flawless drywall installation, patching, and finishing for walls that look brand new."
- Roof Repairs → `fa-house` · `https://images.unsplash.com/photo-1632207691143-643e2a9a9361?w=800&q=80` — "Fast, reliable roof repairs before small issues become big ones."
- Fence & Siding Power Wash → `fa-droplet` · `https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=800&q=80` — "Professional power washing to restore your fence and siding to like-new condition."
- Fence & Deck Stain → `fa-brush` · `https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80` — "Expert staining to protect and refresh your deck and fence for years to come."

---

#### 6. WHY CHOOSE US

**Background:** `lightgray`

**Layout:** Two columns on desktop, stacked on mobile — **photos left, stats right** (mirror of About Us).

**Left — Photo collage (same overlapping style as About Us):**
- Two overlapping job site photos
- Dark overlay card at bottom: `bg-dark text-white rounded-2xl p-5` with Font Awesome hardhat icon (gold) + `"Cost Effective Solutions"` bold + short subtext

**Right — Stats and features:**
- Pill label: `• Why Choose Us`
- Two-tone heading: `"Discover why clients trust"` (dark) + `"our expert services"` (gold)
- Short paragraph
- **Stats row** (`grid grid-cols-3 gap-6 mt-8 mb-8 border-t border-b border-gray-200 py-8`):
  - `500+` Projects Completed
  - `300+` Happy Clients  
  - `100%` Client Satisfaction
  - Each: `text-4xl font-black text-primary` + `text-sm text-gray-500` label below
- **Feature list** (3 items, each with a gold `✦` star asterisk icon):
  - Experienced And Skilled Professional Team
  - High Quality Materials For Long Lasting Results
  - Affordable Pricing With No Hidden Charges
- **Rotating circular "Contact Us" badge** (bottom right):
  - SVG circular text path that says "Contact Us • Contact Us • " rotating slowly via CSS `@keyframes spin`
  - Center: gold arrow icon
  - Size: `w-24 h-24`, clicking scrolls to contact section

---

#### 5. BEFORE & AFTER GALLERY

**Background:** white

**Header (centered):**
- Heading: `"Before & After Gallery"` — `text-primary font-black text-4xl`
- Subtext: `"Drag the slider on each project to see the transformation."`

**Filter bar** (`flex gap-3 justify-center flex-wrap mt-8 mb-12`):
- Pills: All | Interior | Exterior | Cabinets | Deck | Commercial
- Active pill: `bg-primary text-white rounded-full px-5 py-2 font-semibold`
- Inactive pill: `bg-white border border-gray-200 text-gray-600 rounded-full px-5 py-2 hover:border-primary hover:text-primary transition`
- Filtering handled by Alpine.js `x-show` based on active category

**Gallery grid** (`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8`):

Each project card:
- `bg-white rounded-2xl overflow-hidden shadow-md hover:shadow-xl transition-all duration-300 border border-gray-100`

**Slider container** (the before/after reveal — this is the key feature, implement in `gallery.js`):
- Position relative, fixed aspect ratio (`aspect-[4/3]`)
- Before image fills full container
- After image sits on top, clipped by a CSS `clip-path: inset(0 X% 0 0)` where X is driven by slider position
- **"BEFORE" badge**: top-left, `bg-primary/90 text-white text-xs font-bold px-3 py-1 rounded-br-lg`
- **"AFTER" badge**: top-right, `bg-gold/90 text-white text-xs font-bold px-3 py-1 rounded-bl-lg`
- **Divider line**: 2px white vertical line at slider position
- **Handle circle**: `w-10 h-10 bg-white rounded-full shadow-xl border-2 border-gray-200 flex items-center justify-center` — contains `‹ ›` arrows in primary color — centered on divider line
- Touch and mouse drag both supported (see `gallery.js` spec below)

**Below slider — project info:**
- `p-4`
- Project title: `text-primary font-bold text-lg`
- Category + location: `text-gray-400 text-sm` — e.g. `"Exterior — Chicago, IL"`

**Projects data** (define as a Python list in `app.py`, pass to template via `render_template`):
```python
projects = [
  {"id":1,"title":"Interior Painting","category":"Interior","location":"Fairfax, VA","before":"/static/images/gallery/b1.jpeg","after":"/static/images/gallery/b2.jpeg"},
  {"id":2,"title":"Exterior Painting","category":"Exterior","location":"Burke, VA","before":"/static/images/gallery/b3.jpeg","after":"/static/images/gallery/b4.jpeg"},
  {"id":3,"title":"Home Renovation","category":"Interior","location":"Springfield, VA","before":"/static/images/gallery/b5.jpeg","after":"/static/images/gallery/b6.jpeg"},
  {"id":4,"title":"Exterior Refresh","category":"Exterior","location":"Alexandria, VA","before":"/static/images/gallery/b7.jpeg","after":"/static/images/gallery/b8.jpeg"},
  {"id":5,"title":"Room Transformation","category":"Interior","location":"McLean, VA","before":"/static/images/gallery/b9.jpeg","after":"/static/images/gallery/b10.jpeg"},
  {"id":6,"title":"Full Home Repaint","category":"Exterior","location":"Woodbridge, VA","before":"/static/images/gallery/b11.jpeg","after":"/static/images/gallery/b12.jpeg"},
]
```
Pass to template: `render_template('index.html', projects=projects, elfsight_app_id=os.getenv('ELFSIGHT_APP_ID'))`
Render with Jinja2 `{% for project in projects %}` loop.

**`static/js/gallery.js` spec:**
```js
// For each .gallery-card:
// 1. Get the slider handle and after-image overlay
// 2. On mousedown / touchstart on the handle: set dragging = true
// 3. On mousemove / touchmove on the card: if dragging, calculate %
//    position = (clientX - card.left) / card.width * 100
//    clamp between 2 and 98
//    set after-image clip-path: inset(0 {100 - position}% 0 0)
//    set handle left: position%
//    use requestAnimationFrame for performance
// 4. On mouseup / touchend: dragging = false
// 5. Initialize each card at 50% on load
```

---

#### 7. FREE ESTIMATE CTA BANNER

**Placement:** Between Why Choose Us and Google Reviews — this is the conversion moment after the user has seen the work and trust signals.

**Background:** Dark navy (`bg-primary`) with a subtle diagonal paint stroke SVG pattern overlay at low opacity, giving it texture without being distracting.

**Layout:** Full-width, `py-20 px-6`, centered content — single column, everything centered.

**Content:**
- Small label above heading: `"LIMITED TIME"` — `bg-accent text-white text-xs font-bold px-4 py-1 rounded-full uppercase tracking-widest`
- Large heading (white, `text-4xl md:text-5xl font-black text-center`):
  ```
  Get Your Free Estimate Today
  ```
- Subtext (`text-blue-200 text-lg text-center mt-4 max-w-xl mx-auto`):
  `"No obligation, no pressure. We'll come to you, assess the job, and give you a transparent quote — completely free."`
- CTA row (`flex flex-col sm:flex-row items-center justify-center gap-4 mt-10`):
  - Primary button: `"Call 703-944-5717"` with phone icon — `bg-accent text-white rounded-full px-10 py-4 font-bold text-xl hover:bg-accentdark transition shadow-xl`
  - Secondary button: `"Or Fill Out Our Form"` → scrolls to contact — `border-2 border-white/40 text-white rounded-full px-8 py-4 font-semibold hover:bg-white/10 transition`
- Below buttons, three small trust chips in a row (`flex gap-4 justify-center mt-8 flex-wrap`):
  - Each: `bg-white/10 text-white/80 text-sm rounded-full px-4 py-2 flex items-center gap-2`
  - ✓ Free On-Site Estimate &nbsp;·&nbsp; ✓ Response Within 24 Hours &nbsp;·&nbsp; ✓ Licensed & Insured

---

#### 8. GOOGLE REVIEWS

**Background:** `lightblue`

**Header (centered):**
- Pill label: `• What Our Clients Say`
- Two-tone heading: `"What Our Customers"` (dark navy) + `"Are Saying"` (baby blue/accent)

**Elfsight Widget — replace the entire reviews content with this embed:**

Add this script to `<head>` in `base.html` (if not already there):
```html
<script src="https://elfsightcdn.com/platform.js" async></script>
```

Then in the reviews section body, use the Jinja2 variable — NO hardcoded IDs in the HTML:
```html
<div class="elfsight-app-{{ elfsight_app_id }}" data-elfsight-app-lazy></div>
```

Full section HTML:
```html
<section id="reviews" class="py-24 px-6 bg-lightblue">
  <div class="max-w-7xl mx-auto">
    <!-- Section header -->
    <div class="text-center mb-12">
      <span class="inline-flex items-center gap-2 bg-white border border-accent/30 rounded-full px-4 py-1 text-sm text-accent font-medium shadow-sm mb-4">
        • What Our Clients Say
      </span>
      <h2 class="text-4xl font-black text-primary">What Our Customers
        <span class="text-accent">Are Saying</span>
      </h2>
    </div>
    <!-- Elfsight Google Reviews Widget — ID loaded from .env via Flask -->
    <div class="elfsight-app-{{ elfsight_app_id }}" data-elfsight-app-lazy></div>
  </div>
</section>
```

**In `app.py` the index route must pass the variable:**
```python
@app.route('/')
def index():
    return render_template('index.html',
        projects=projects,
        elfsight_app_id=os.getenv('ELFSIGHT_APP_ID')
    )
```

---

#### 8. CONTACT SECTION

**Layout:** Full-width section with a dark background image overlay (workers/painting job site), split into left text + right floating form card.

**Background:**
- Image: `https://picsum.photos/seed/contactbg/1600/900`
- Overlay: `bg-black/65`
- Full section `min-h-[600px]` with flex layout

**Left side:**
- Pill label: `Contact Now` — styled as `inline-flex items-center gap-2 bg-white/10 border border-white/20 backdrop-blur-sm rounded-full px-4 py-1.5 text-sm text-white font-medium`
  - Replace the `•` dot with a **pulsing green live indicator**:
    ```html
    <span class="relative flex h-2.5 w-2.5">
      <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
      <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-green-500"></span>
    </span>
    Contact Now
    ```
  - This uses Tailwind's built-in `animate-ping` for the pulsing halo effect — a bright green solid dot with a radiating green ring, universally recognized as "live/active"
  - Apply this same pulsing dot pattern to ALL section pill labels that currently use a `•` bullet — it ties the whole site together
- Two-tone heading (white + gold):
  - `"Let's connect for your"` (white)
  - `"painting project"` (gold)
- Subtext in `text-gray-300`
- Two info cards at bottom (`flex gap-4 mt-10`):
  - Each: `bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl px-5 py-4 flex items-center gap-3`
  - Card 1: phone icon (accent baby blue) + `"Call For a Free Estimate"` white bold + `"703-944-5717"` in accent (baby blue)
  - Card 2: email icon (accent baby blue) + `"Email Us Anytime"` white bold + `"info@fourseasonpainting.com"` in accent (baby blue)

**Right side — Floating white form card:**
- `bg-white rounded-3xl shadow-2xl p-10 max-w-lg w-full`
- Heading: `"Get in touch "` (dark) + `"with us"` (gold) — `text-3xl font-black`
- Horizontal rule `<hr class="my-4 border-gray-100">`
- Form grid (`grid grid-cols-2 gap-4`):
  - Row 1: First Name | Last Name
  - Row 2: Email Address | Phone Number
  - Row 3 (full width `col-span-2`): Message textarea
- All inputs: `border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-gold/40 w-full`
- Submit button: `"Send A Message →"` — `w-full bg-dark text-white rounded-full py-4 font-bold text-base hover:bg-primary transition mt-2`
- Alpine.js handles fetch POST to `/contact`, shows success/error state

**Flask contact route** in `app.py`:
```python
import boto3, os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

ses = boto3.client(
    'ses',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

LOGO_URL = "https://thefourseaonpainting.s3.us-east-1.amazonaws.com/logo-white.png"

def build_owner_email(data):
    name = f"{data.get('first_name','')} {data.get('last_name','')}".strip()
    phone = data.get('phone', 'Not provided')
    return f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f4f6f9;font-family:'Helvetica Neue',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f6f9;padding:40px 0;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">
        <!-- Header -->
        <tr>
          <td style="background:#0a1628;padding:32px 40px;text-align:center;">
            <img src="{LOGO_URL}" alt="The Four Season Painting" style="height:72px;width:auto;">
          </td>
        </tr>
        <!-- Accent bar -->
        <tr><td style="background:#5bb8f5;height:4px;"></td></tr>
        <!-- Body -->
        <tr>
          <td style="padding:40px;">
            <h2 style="margin:0 0 8px;color:#0a1628;font-size:22px;font-weight:700;">New Quote Request</h2>
            <p style="margin:0 0 28px;color:#64748b;font-size:14px;">A visitor submitted the contact form on your website.</p>
            <table width="100%" cellpadding="0" cellspacing="0">
              <tr>
                <td style="padding:12px 0;border-bottom:1px solid #f1f5f9;">
                  <span style="color:#94a3b8;font-size:12px;text-transform:uppercase;letter-spacing:0.05em;">Name</span><br>
                  <span style="color:#0f172a;font-size:15px;font-weight:600;">{name}</span>
                </td>
              </tr>
              <tr>
                <td style="padding:12px 0;border-bottom:1px solid #f1f5f9;">
                  <span style="color:#94a3b8;font-size:12px;text-transform:uppercase;letter-spacing:0.05em;">Email</span><br>
                  <a href="mailto:{data['email']}" style="color:#5bb8f5;font-size:15px;font-weight:600;text-decoration:none;">{data['email']}</a>
                </td>
              </tr>
              <tr>
                <td style="padding:12px 0;border-bottom:1px solid #f1f5f9;">
                  <span style="color:#94a3b8;font-size:12px;text-transform:uppercase;letter-spacing:0.05em;">Phone</span><br>
                  <span style="color:#0f172a;font-size:15px;font-weight:600;">{phone}</span>
                </td>
              </tr>
              <tr>
                <td style="padding:12px 0;">
                  <span style="color:#94a3b8;font-size:12px;text-transform:uppercase;letter-spacing:0.05em;">Message</span><br>
                  <p style="color:#0f172a;font-size:15px;margin:8px 0 0;line-height:1.6;">{data['message']}</p>
                </td>
              </tr>
            </table>
            <a href="mailto:{data['email']}" style="display:inline-block;margin-top:32px;background:#0a1628;color:#ffffff;text-decoration:none;padding:14px 32px;border-radius:50px;font-size:14px;font-weight:700;">Reply to {data.get('first_name','Client')}</a>
          </td>
        </tr>
        <!-- Footer -->
        <tr>
          <td style="background:#f8fafc;padding:24px 40px;text-align:center;border-top:1px solid #e2e8f0;">
            <p style="margin:0;color:#94a3b8;font-size:12px;">This message was sent via the contact form on <strong>thefourseasonpainting.com</strong></p>
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>
"""

def build_client_email(data):
    name = data.get('first_name', 'there')
    return f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f4f6f9;font-family:'Helvetica Neue',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f6f9;padding:40px 0;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.08);">
        <!-- Header -->
        <tr>
          <td style="background:#0a1628;padding:32px 40px;text-align:center;">
            <img src="{LOGO_URL}" alt="The Four Season Painting" style="height:72px;width:auto;">
          </td>
        </tr>
        <!-- Accent bar -->
        <tr><td style="background:#5bb8f5;height:4px;"></td></tr>
        <!-- Body -->
        <tr>
          <td style="padding:40px;">
            <h2 style="margin:0 0 16px;color:#0a1628;font-size:22px;font-weight:700;">Thanks, {name}! We got your message.</h2>
            <p style="margin:0 0 16px;color:#475569;font-size:15px;line-height:1.7;">We appreciate you reaching out to <strong>The Four Season Painting</strong>. Our team will review your request and get back to you within <strong>24 hours</strong>.</p>
            <p style="margin:0 0 32px;color:#475569;font-size:15px;line-height:1.7;">In the meantime, feel free to browse our work or give us a call if your project is urgent.</p>
            <table cellpadding="0" cellspacing="0">
              <tr>
                <td style="padding-right:12px;">
                  <a href="https://thefourseasonpainting.com/gallery" style="display:inline-block;background:#0a1628;color:#ffffff;text-decoration:none;padding:14px 28px;border-radius:50px;font-size:14px;font-weight:700;">View Our Work</a>
                </td>
                <td>
                  <a href="tel:+17034771631" style="display:inline-block;background:#f8fafc;border:1px solid #e2e8f0;color:#0a1628;text-decoration:none;padding:14px 28px;border-radius:50px;font-size:14px;font-weight:700;">(703) 477-1631</a>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <!-- Footer -->
        <tr>
          <td style="background:#f8fafc;padding:24px 40px;text-align:center;border-top:1px solid #e2e8f0;">
            <p style="margin:0 0 4px;color:#94a3b8;font-size:12px;">The Four Season Painting · Northern Virginia</p>
            <p style="margin:0;color:#cbd5e1;font-size:11px;">You're receiving this because you submitted a form on our website.</p>
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>
"""

@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    required = ['first_name', 'email', 'message']
    if not all(data.get(f) for f in required):
        return jsonify({'error': 'Missing required fields'}), 400
    ses.send_email(
        Source=os.getenv('FROM_EMAIL'),
        Destination={'ToAddresses': [os.getenv('CONTACT_EMAIL')]},
        Message={
            'Subject': {'Data': f"New Quote Request — {data.get('first_name','')} {data.get('last_name','')}".strip()},
            'Body': {'Html': {'Data': build_owner_email(data)}}
        }
    )
    ses.send_email(
        Source=os.getenv('FROM_EMAIL'),
        Destination={'ToAddresses': [data['email']]},
        Message={
            'Subject': {'Data': 'We received your message — The Four Season Painting'},
            'Body': {'Html': {'Data': build_client_email(data)}}
        }
    )
    return jsonify({'success': True})
```

`.env` — all sensitive values live here, never hardcoded anywhere:
```
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
CONTACT_EMAIL=owner@yourcompany.com
FROM_EMAIL=noreply@yourdomain.com
ELFSIGHT_APP_ID=8e611f74-545e-4cef-873c-1c3fbed409cc
```

`.gitignore` must include:
```
.env
venv/
__pycache__/
*.pyc
```

---

#### 9. FOOTER

**Background:** `bg-dark` (near-black `#111827`) with a very subtle dark grid or dot pattern overlay (CSS background-image pattern, low opacity)

**Layout:** `grid grid-cols-1 md:grid-cols-4 gap-12 py-16 px-6 max-w-7xl mx-auto`

**Column 1 — Brand:**
- Logo image (white version or full color on dark)
- Tagline: `"Professional painting services designed to transform your space with quality, creativity, and precision."` — `text-gray-400 text-sm mt-4 leading-relaxed`
- Social icons row (`flex gap-3 mt-6`): Pinterest, Twitter/X, Facebook, Instagram — each in a `w-10 h-10 bg-gray-800 rounded-full flex items-center justify-center text-gray-400 hover:bg-gold hover:text-white transition` circle

**Column 2 — Quick Links:**
- `"Quick Links"` heading in `text-white font-bold mb-5`
- List: Home, About Us, Services, Gallery, Blog, Contact Us — each `text-gray-400 hover:text-gold text-sm py-1 transition flex items-center gap-2 before:content-['•'] before:text-gold`

**Column 3 — Our Services:**
- `"Our Services"` heading
- List: Interior & Exterior Painting, Bathroom & Kitchen Remodeling, Electrical & Plumbing, Fence & Carpentry, Drywall & Finishing, Roof Repairs

**Column 4 — Newsletter:**
- Styled card: `bg-gray-800 rounded-2xl p-6`
- Heading: `"Subscribe For Latest Updates"` — `text-white font-bold`
- Email input + arrow button: `flex mt-4` — input `flex-1 bg-transparent border border-gray-600 rounded-l-xl px-4 py-3 text-sm text-white placeholder-gray-500 focus:outline-none`, button `bg-gold text-white px-4 rounded-r-xl hover:bg-yellow-600 transition` with `→` icon
- Subtext: `"Subscribe to our newsletter to receive the latest updates."` in `text-gray-400 text-xs mt-3`

**Bottom bar** (`border-t border-gray-800 mt-8 pt-8 flex justify-between items-center text-sm text-gray-500`):
- Left: `"Copyright © 2026 All Rights Reserved."`
- Right: `"Privacy Policy • Terms & Conditions"` (links)

---

### BASE TEMPLATE CDN LINKS

In `templates/base.html` `<head>`:
```html
<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = {
    theme: { extend: { colors: {
      primary:    '#0a1628',   // deep dark navy
      secondary:  '#1e3a5f',   // mid dark blue
      accent:     '#5bb8f5',   // baby blue
      accentdark: '#2e86c1',   // deeper baby blue
      dark:       '#060e1a',   // near-black navy
      lightblue:  '#e8f4fd',   // light blue tint
    }}}
  }
</script>
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800;900&family=DM+Sans:wght@400;500;600&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="{{ url_for('static', filename='css/custom.css') }}"/>
```

In `custom.css`:
```css
body { font-family: 'DM Sans', sans-serif; }
h1, h2, h3, h4 { font-family: 'Manrope', sans-serif; }

/* Rotating contact badge */
@keyframes spin-slow { to { transform: rotate(360deg); } }
.spin-slow { animation: spin-slow 8s linear infinite; }

/* Gallery slider */
.gallery-after { clip-path: inset(0 50% 0 0); transition: none; }

/* ─── SCROLL ANIMATIONS ─────────────────────────────────────────── */
/* Base hidden state — applied via JS before element enters viewport */
.reveal {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.55s ease, transform 0.55s ease;
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Stagger delay helpers — add to child elements in a grid */
.reveal-delay-1 { transition-delay: 0.08s; }
.reveal-delay-2 { transition-delay: 0.16s; }
.reveal-delay-3 { transition-delay: 0.24s; }
.reveal-delay-4 { transition-delay: 0.32s; }
.reveal-delay-5 { transition-delay: 0.40s; }
.reveal-delay-6 { transition-delay: 0.48s; }
.reveal-delay-7 { transition-delay: 0.56s; }
.reveal-delay-8 { transition-delay: 0.64s; }
```

In `main.js` — add the IntersectionObserver that drives all scroll animations:
```js
// Scroll reveal — triggers .reveal elements as they enter the viewport
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target); // animate once only
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```

**How to apply across sections — rules:**
- Every **section heading + pill label**: wrap in a `<div class="reveal">` — animates the whole header block together
- Every **card in a grid**: add `reveal` + `reveal-delay-N` (N = card index 1–8) — creates the stagger effect
- Every **image or photo collage**: add `reveal` to the image wrapper
- Every **CTA block or banner**: add `reveal` to the container
- Do NOT add `reveal` to the navbar, hero, or footer — these should be immediately visible
- Do NOT add `reveal` to individual text lines inside cards — only to the card itself

---

### PAGE LOAD PRELOADER

Add a full-screen preloader that plays once per session on page load.

**HTML** — first child of `<body>` in `base.html`:
```html
<div id="preloader" style="position:fixed;inset:0;background:#0a1628;z-index:9999;display:flex;align-items:center;justify-content:center;">
  <svg id="preloaderSvg" viewBox="0 0 400 340" width="400" height="340" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <filter id="plGlow"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      <linearGradient id="plHandle" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="#b8904a"/>
        <stop offset="50%" stop-color="#e8c490"/>
        <stop offset="100%" stop-color="#c8a06a"/>
      </linearGradient>
      <linearGradient id="plBristle" x1="1" y1="0" x2="0" y2="0">
        <stop offset="0%" stop-color="#5bb8f5"/>
        <stop offset="100%" stop-color="#3a9de0"/>
      </linearGradient>
    </defs>

    <!-- Four season arc segments (quarter circle each, ~154px) -->
    <!-- Yellow: top→right | Blue: right→bottom | Green: bottom→left | Pink: left→top -->
    <path id="plArc0" d="M 200 72 A 98 98 0 0 1 298 170" fill="none" stroke="#ffcc00" stroke-width="6" stroke-linecap="round" filter="url(#plGlow)" style="stroke-dasharray:154;stroke-dashoffset:154;"/>
    <path id="plArc1" d="M 298 170 A 98 98 0 0 1 200 268" fill="none" stroke="#5bb8f5" stroke-width="6" stroke-linecap="round" filter="url(#plGlow)" style="stroke-dasharray:154;stroke-dashoffset:154;"/>
    <path id="plArc2" d="M 200 268 A 98 98 0 0 1 102 170" fill="none" stroke="#4cbe6c" stroke-width="6" stroke-linecap="round" filter="url(#plGlow)" style="stroke-dasharray:154;stroke-dashoffset:154;"/>
    <path id="plArc3" d="M 102 170 A 98 98 0 0 1 200 72"  fill="none" stroke="#e8558a" stroke-width="6" stroke-linecap="round" filter="url(#plGlow)" style="stroke-dasharray:154;stroke-dashoffset:154;"/>

    <!-- Logo — fades in after brush completes circle -->
    <g id="plLogo" opacity="0" style="transition:opacity 0.7s ease;">
      <image href="{{ url_for('static', filename='images/logo-white.png') }}" x="120" y="90" width="160" height="160"/>
    </g>

    <!-- Brush — tip at origin, leads the stroke at 38° holding angle -->
    <g id="plBrush" opacity="0">
      <ellipse cx="2" cy="0" rx="5" ry="3.5" fill="#5bb8f5" opacity="0.95"/>
      <path d="M0,0 L-22,-5.5 L-24,0 L-22,5.5 Z" fill="url(#plBristle)"/>
      <path d="M-4,-2.5 L-21,-4 L-21,4 L-4,2.5" fill="rgba(255,255,255,0.1)"/>
      <line x1="-3" y1="-2" x2="-20" y2="-2.5" stroke="rgba(255,255,255,0.25)" stroke-width="0.8"/>
      <rect x="-30" y="-6" width="10" height="12" rx="1.5" fill="#b8c4cc"/>
      <rect x="-29" y="-6" width="2.5" height="12" fill="rgba(255,255,255,0.25)"/>
      <rect x="-30" y="-1" width="10" height="2" fill="rgba(0,0,0,0.15)"/>
      <rect x="-82" y="-5" width="54" height="10" rx="2.5" fill="url(#plHandle)"/>
      <line x1="-80" y1="-2" x2="-32" y2="-2" stroke="rgba(0,0,0,0.12)" stroke-width="1"/>
      <line x1="-80" y1="1.5" x2="-32" y2="1.5" stroke="rgba(255,255,255,0.18)" stroke-width="0.7"/>
      <rect x="-84" y="-4.5" width="4" height="9" rx="2" fill="#a07030"/>
    </g>
  </svg>
</div>
```

**JS** — add to `main.js` (runs on DOMContentLoaded):
```js
(function() {
  if (sessionStorage.getItem('preloaderSeen')) {
    document.getElementById('preloader').style.display = 'none';
    return;
  }
  const TAU=Math.PI*2, cx=200, cy=170, r=98, SEG=154;
  function pt(a){ return {x:cx+r*Math.cos(a-Math.PI/2), y:cy+r*Math.sin(a-Math.PI/2)}; }
  function ease(t){ return t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2; }
  const arcs=[0,1,2,3].map(i=>document.getElementById('plArc'+i));
  const brush=document.getElementById('plBrush');
  const logo=document.getElementById('plLogo');
  const pre=document.getElementById('preloader');
  const dur=2200; let start=null;
  function tick(ts){
    if(!start) start=ts;
    const raw=Math.min((ts-start)/dur,1), prog=ease(raw);
    const angle=prog*TAU, p=pt(angle);
    const holdAngle=(angle*180/Math.PI)+90-38;
    brush.style.opacity='1';
    brush.setAttribute('transform',`translate(${p.x},${p.y}) rotate(${holdAngle})`);
    const seg=Math.min(Math.floor(prog*4),3), segProg=(prog*4)%1;
    for(let i=0;i<4;i++){
      if(i<seg) arcs[i].style.strokeDashoffset='0';
      else if(i===seg) arcs[i].style.strokeDashoffset=SEG*(1-segProg);
      else arcs[i].style.strokeDashoffset=SEG;
    }
    if(raw<1){ requestAnimationFrame(tick); }
    else {
      arcs.forEach(a=>a.style.strokeDashoffset='0');
      brush.style.transition='opacity 0.5s ease';
      brush.style.opacity='0';
      setTimeout(()=>logo.style.opacity='1', 400);
      setTimeout(()=>{
        pre.style.transition='opacity 0.7s ease';
        pre.style.opacity='0';
        setTimeout(()=>{ pre.style.display='none'; sessionStorage.setItem('preloaderSeen','1'); }, 700);
      }, 2000);
    }
  }
  setTimeout(()=>requestAnimationFrame(tick), 300);
})();
```

---

### RESPONSIVENESS

- Mobile-first using Tailwind responsive prefixes
- Hero: stack text above form card on mobile (`flex-col lg:flex-row`)
- About / Why Choose Us: stack photos above text on mobile
- Services: 1 col → 2 col → 3 col
- Gallery: 1 col → 2 col → 3 col
- Footer: 1 col → 4 col
- Contact: stack left above form card on mobile

---

### WHAT TO DO FIRST

1. Set up the project:
   ```bash
   mkdir four-season-painting && cd four-season-painting
   python -m venv venv && source venv/bin/activate
   pip install flask boto3 python-dotenv
   pip freeze > requirements.txt
   ```
2. Create `app.py` with the `/` route and `/contact` route
3. Create `templates/base.html` with all CDN links and `{% block content %}{% endblock %}`
4. Create `templates/index.html` extending base — build each section top to bottom
5. Add `.env` and `.gitignore` (add `.env` to it immediately)
6. Create `static/js/gallery.js` with the before/after slider logic
7. Run with `flask run` and iterate section by section
8. Wire up the `/contact` route last once AWS credentials are ready

---

## PROMPT END
