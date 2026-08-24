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

## Adding a new blog post — superseded, see "Blog CMS" section below

(This section used to describe manually duplicating HTML files. That's no
longer how blog posts work — see the "Blog CMS (Sveltia CMS)" section
further down for the current process, either via the CMS at `/admin` once
set up, or by manually adding a `.md` file to `content/posts/` in the
meantime.)

## Contact form — ✅ live

The contact form in `src/pages/contact.html` is wired to Web3Forms (free
forever, 250 submissions/month). Submissions arrive directly by email —
no dashboard or login needed.

To also auto-add contact form submissions to the ConvertKit list: set up a
free Zapier account, create a Zap with trigger "New Submission" in
Web3Forms → action "Create or Update Subscriber" in Kit/ConvertKit,
mapping Name/Email/Phone. Optionally tag these as "Contact Form Lead" to
distinguish from newsletter-only subscribers.

## SEO checklist before launch

- [x] Meta titles/descriptions on every page
- [x] Open Graph + Twitter Card tags
- [x] JSON-LD structured data (Home, About, Lakefront Specialty, blog posts)
- [x] Auto-generated sitemap.xml (regenerates every build, includes new blog posts automatically)
- [x] robots.txt pointing to the sitemap
- [x] Google Business Profile already set up — double check its website link points
      to iamphilkruse.com once the domain switch happens, not the old SiteGround URL
- [ ] **Add real, descriptive alt text to every image once real photos replace
      placeholders** — especially blog post images. Empty alt text on
      placeholders is fine for now, but this needs to be done for every real
      image that goes up (accessibility + image search ranking).

## Lead magnets (in progress — not yet built)

Plan: separate free downloadable guides, each with its own ConvertKit
form/automation (distinct from the general Friday newsletter signup), so
subscribers can be tagged by which guide they downloaded:

1. **Buyer's Guide** (general, not lakefront-specific) — homepage "Buyers" card
2. **Seller's Guide** (general, not lakefront-specific) — homepage "Sellers" card
3. **Lakefront Buying & Selling Guide** — homepage "Lake Lovers" card AND the
   button on the Lakefront Specialty page — covers both buyers and sellers on
   the water in one PDF

**Still needed before these can go live:**
- VA to design all three PDF flyers/guides (content + layout)
- Three separate ConvertKit forms + automations set up (one per guide) so each
  delivers the correct PDF automatically on signup and tags the subscriber
  accordingly — ask Claude for help setting these up in ConvertKit once the
  PDF content exists
- Once each ConvertKit embed code exists, swap it into the matching placeholder
  buttons (currently linking to `#`) in `src/pages/index.html` and
  `src/pages/lakefront-specialty.html`

**Future idea (not built, just logged):** a scroll-triggered or time-delayed
popup promoting the free Lakefront Guide as visitors read the Lakefront
Specialty page. Would need a JS modal + trigger logic + the ConvertKit
integration above. Revisit once the guide itself exists.

## Lake chain blog posts (needed for Lakefront Specialty page)

The "Phil's Preferred Lake Chains" section on the Lakefront Specialty page
has three buttons — Conway Chain of Lakes, Winter Park Chain of Lakes, Butler
Chain of Lakes — that currently link to `#` (placeholder). These need to
point to three real blog posts, one per chain, once written or migrated from
the old WordPress content. **Reminder: get this done, either by Claude or
the VA, before launch** — see `src/pages/lakefront-specialty.html` for the
exact spot to update once the post URLs exist.

## ConvertKit form cleanup (action needed in ConvertKit, not in this code)

The embedded newsletter form (data-uid 04b1973276) currently shows a
redundant "First Name / Last Name" field alongside the main "Name" field,
plus three unnecessary checkboxes. Fix this directly in ConvertKit: Grow →
Landing Pages & Forms → edit the form → remove the duplicate name field and
the three checkboxes, rename "Name" to "First & Last Name." No code change
needed here — the embed pulls live from ConvertKit.

## Blog CMS (Sveltia CMS) — for your VA

Blog posts are no longer edited as raw HTML files. They're simple Markdown
files with a small metadata header, stored in `content/posts/`, and the
build script automatically turns each one into a fully styled page AND adds
it to both the blog listing page and the homepage's "Here's the Latest for
Orlando" section — no manual card-editing required anywhere.

**For your VA:** once the one-time setup below is done, she'll use a simple
web-based editor at `iamphilkruse.com/admin` — log in, click "New Blog
Posts," fill in a title, category, one-sentence teaser, cover photo, and
write the post in a normal rich-text box (no HTML). Clicking "Publish"
automatically saves it to GitHub and the live site rebuilds within about a
minute. No GitHub, no raw code, ever.

**One-time setup (you, not the VA — takes about 15-20 minutes):**

1. Deploy the free OAuth bridge to Cloudflare Workers: go to
   github.com/sveltia/sveltia-cms-auth, and either fork it or follow its
   README to deploy it to your Cloudflare account (Workers & Pages → Create
   → import from this GitHub repo). Once deployed, note the Worker's URL —
   it'll look like `https://sveltia-cms-auth.<something>.workers.dev`.
2. In GitHub, go to Settings → Developer settings → OAuth Apps → New OAuth
   App. Set the Homepage URL to `https://www.iamphilkruse.com` and the
   Authorization callback URL to `<your Worker URL>/callback`. Save, then
   copy the Client ID and generate/copy a Client Secret.
3. Back in Cloudflare, open your deployed Worker's settings → Variables, and
   add the Client ID and Client Secret as environment variables (the exact
   variable names are in the sveltia-cms-auth README).
4. Open `admin/config.yml` in this repo and replace
   `https://REPLACE-WITH-YOUR-WORKER.workers.dev` with your actual Worker
   URL from step 1.
5. Go to `iamphilkruse.com/admin`, click "Login with GitHub," and confirm
   you can see the Blog Posts collection. Ask Claude for help if anything
   doesn't connect — screenshots of any error are the fastest way to debug it.

Once this works, only people you've given GitHub repo access to can log in
and publish — give your VA "Write" access to the repo on GitHub
(Settings → Collaborators) so she can log into the CMS too.

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
