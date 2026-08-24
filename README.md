# Phil Kruse Real Estate — Website

A fast, static, mobile-first website. Built as plain HTML/CSS/JS with a small
Python build script that injects a shared header, nav, and footer into every
page — so updating navigation, tracking, or the newsletter box means editing
one file, not every page.

## What's built

- **Home** (`src/pages/index.html`)
- **About** (`src/pages/about.html`)
- **Lakefront Specialty** (`src/pages/lakefront-specialty.html`)
- **Charities** (`src/pages/charities.html`)
- **Contact** (`src/pages/contact.html`) — form + direct contact info
- **Blog** (`src/blog/index.html` listing + `src/blog/sample-post.html` template)
- Shared design system: `css/styles.css` (your navy `#203873` / gold `#a97b58`
  palette, Anton/Lora/Inter type system, mobile nav, buttons, cards)
- Shared partials: `src/partials/head.html` (meta/SEO/GA4), `nav.html`, `footer.html`
  (includes the Friday newsletter box)

Every page currently has real structure with **`[PLACEHOLDER: ...]`** text
marking where your actual content goes. Nothing is lorem ipsum — it's all
labeled so you know exactly what to replace.

## Before this goes live — things that need your input

1. **Photos** — replace the placeholder images in `/images/`:
   `hero-lake.jpg`, `hero-lakefront.jpg`, `phil-headshot.jpg`,
   `blog-placeholder.jpg` (one per post), `social-share.jpg`
2. **Copy** — fill in remaining `[PLACEHOLDER: ...]` items. Your About page,
   homepage stats, and Charities page now have your real bio, story, and
   New Image Youth Center info already in place.
3. ~~**Kit (ConvertKit) embed**~~ — done. The Friday newsletter box on the
   homepage now uses your live Kit embed (`data-uid="04b1973276"`).
4. **Contact form backend** — the contact form needs somewhere to send
   submissions since this is a static site. Easiest option: sign up at
   [formspree.io](https://formspree.io), get a form endpoint, and paste it
   into the `action="..."` attribute in `src/pages/contact.html`.
5. **Real domain, email, phone** — search the codebase for `iamphilkruse.com`
   and the placeholder phone/email and replace with real values.
6. **Google Analytics** — replace `G-XXXXXXXXXX` in `src/partials/head.html`
   with your real GA4 Measurement ID.
7. **Charities** — the New Image Youth Center card is filled in; duplicate
   the second `<div class="card">` block in `src/pages/charities.html` for
   any other causes you support.
8. **Social links** — in `src/partials/footer.html`, replace the three
   `href="#"` placeholders (Instagram, Facebook, LinkedIn) with your real
   profile URLs.
9. **License number** — the footer has a `[State/License #]` placeholder
   required by most state real estate boards; fill in your actual license
   number (check with your state board on any other required disclosures
   now that the brokerage name has been removed).

## Account setup (your part — ~15 minutes)

1. **GitHub** — create a free account at github.com, create a new repository
   (e.g. `phil-kruse-website`), and push this folder to it.
2. **Cloudflare** — create a free account at cloudflare.com → **Workers and
   Pages → Create application → Pages → Connect to Git** → select your repo.
3. **Build settings:**
   - Production branch: `main`
   - Build command: `python build.py`
   - Build output directory: `site_dist`
4. Click **Save and Deploy**. Cloudflare gives you a `.pages.dev` preview URL
   within about 60 seconds.
5. **Custom domain** — in the Cloudflare Pages project, go to **Custom
   Domains → Set up a custom domain**, enter your domain, and follow the DNS
   instructions.

Once connected, every push to GitHub automatically redeploys the live site.

## How the build works

`build.py` reads every `.html` file in `src/pages/` and `src/blog/`, pulls a
small `<!--META ... -->` block off the top of each one (title, description,
canonical path, which nav item is active, and optional schema markup),
injects the shared head/nav/footer, and writes finished pages into
`site_dist/`. CSS, JS, and images are copied over as-is. Cloudflare Pages
serves `.html` files at clean URLs automatically (`about.html` → `/about`),
so don't worry about `.html` showing up in links.

## Adding a new blog post (for your VA)

1. Duplicate `src/blog/sample-post.html`, rename it to something like
   `src/blog/your-post-slug.html`.
2. Update the `<!--META-->` block at the top: `TITLE`, `DESC`, and `PATH`
   (e.g. `/blog/your-post-slug`).
3. Replace the placeholder headline, date, category, and body content.
4. Open `src/blog/index.html`, copy one `<a class="post-card">` block, and
   add it to the **top** of the list with the new post's title, link, image,
   and teaser line.
5. Commit and push to GitHub — Cloudflare deploys it automatically.

No coding required beyond editing text inside the existing HTML tags.

## Lead magnets (in progress — not yet built)

Plan: three separate free downloadable guides, each with its own ConvertKit
form/automation (distinct from the general Friday newsletter signup), so
subscribers can be tagged by which guide they downloaded:

1. **Buyer's Guide** (general, not lakefront-specific) — homepage "Buyers" card
2. **Seller's Guide** (general, not lakefront-specific) — homepage "Sellers" card
3. **Lakefront Buying & Selling Guide** — homepage "Lake Lovers" card, covers
   both buyers and sellers in two sections/columns within one PDF

**Still needed before these can go live:**
- VA to design all three PDF flyers/guides (content + layout)
- Three separate ConvertKit forms + automations set up (one per guide) so each
  delivers the correct PDF automatically on signup and tags the subscriber
  accordingly — ask Claude for help setting these up in ConvertKit once the
  PDF content exists
- Once each ConvertKit embed code exists, swap it into the matching homepage
  card (currently placeholder buttons — see `src/pages/index.html`)

## Domain strategy

Primary domain: **iamphilkruse.com**

Additional domains redirect (301) to the Lakefront Specialty page, since
they all describe the same thing — this consolidates them under one page
instead of splitting traffic and SEO signal across variations:

| Domain | Redirects to |
|---|---|
| orlandolakes.com | iamphilkruse.com/lakefront-specialty |
| orlandolakefront.com | iamphilkruse.com/lakefront-specialty |
| orlandolakefrontspecialist.com | iamphilkruse.com/lakefront-specialty |
| lakefrontorlando.com | iamphilkruse.com/lakefront-specialty |
| lakefronthomesorlando.com | iamphilkruse.com/lakefront-specialty |

These redirects are set up in Cloudflare (DNS + Redirect Rules or Bulk
Redirects), not in this codebase — each domain needs its own Cloudflare
zone with nameservers pointed at Cloudflare, then a 301 redirect rule to
the target URL above. They're worth having for brand protection and
direct type-in traffic; they won't meaningfully move the needle on search
rankings by themselves — that comes from the content on iamphilkruse.com.

## Local guardrail

When asking Claude Code to make a change, say something like:
> "Only edit `src/pages/about.html`. Do not change anything else."

This keeps edits contained to the file you actually mean to change.
