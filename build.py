#!/usr/bin/env python3
"""
Build script for Phil Kruse Real Estate site.

Reads source pages from src/pages and src/blog, injects the shared
head/nav/footer partials, and writes finished static HTML into
the output folder (default: site_dist), plus copies css/js/images.

Cloudflare Pages build command:  python build.py
Build output directory:          site_dist
"""

import os
import re
import shutil
import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_PAGES = os.path.join(ROOT, "src", "pages")
SRC_BLOG = os.path.join(ROOT, "src", "blog")
CONTENT_POSTS = os.path.join(ROOT, "content", "posts")
PARTIALS = os.path.join(ROOT, "src", "partials")
OUT = os.path.join(ROOT, "site_dist")

NAV_KEYS = ["home", "about", "lakefront", "blog", "charities", "contact"]


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


KNOWN_META_KEYS = ["TITLE", "DESC", "PATH", "NAV", "SCHEMA"]


def parse_meta(source):
    """Pull the <!--META ... --> block off the top of a page source file.

    Values can span multiple lines (e.g. SCHEMA holds a whole <script>
    JSON-LD block) -- everything up to the next known KEY: line belongs
    to the current key.
    """
    match = re.search(r"<!--META\s*(.*?)-->", source, re.DOTALL)
    meta = {}
    if match:
        block = match.group(1).strip("\n")
        key_pattern = re.compile(r"^(" + "|".join(KNOWN_META_KEYS) + r"):\s?(.*)$")
        current_key = None
        for line in block.split("\n"):
            m = key_pattern.match(line)
            if m:
                current_key = m.group(1)
                meta[current_key] = [m.group(2)]
            elif current_key:
                meta[current_key].append(line)
        meta = {k: "\n".join(v).strip() for k, v in meta.items()}
        source = source[match.end():].lstrip("\n")
    return meta, source


def build_head(meta):
    head = read(os.path.join(PARTIALS, "head.html"))
    head = head.replace("{{TITLE}}", meta.get("TITLE", "Phil Kruse Real Estate"))
    head = head.replace("{{META_DESC}}", meta.get("DESC", ""))
    head = head.replace("{{CANONICAL_PATH}}", meta.get("PATH", "/"))
    head = head.replace("{{SCHEMA}}", meta.get("SCHEMA", ""))
    return head


def build_nav(meta):
    nav = read(os.path.join(PARTIALS, "nav.html"))
    active = meta.get("NAV", "").strip().lower()
    for key in NAV_KEYS:
        placeholder = "{{NAV_%s}}" % key.upper()
        nav = nav.replace(placeholder, 'aria-current="page"' if key == active else "")
    return nav


def build_footer():
    return read(os.path.join(PARTIALS, "footer.html"))


# ---------------------------------------------------------------------------
# Markdown blog posts (content/posts/*.md) -- written by Sveltia CMS or by
# hand. Each file has --- frontmatter --- followed by a Markdown body.
# ---------------------------------------------------------------------------

def parse_frontmatter(source):
    """Split a file into (frontmatter dict, markdown body)."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", source, re.DOTALL)
    if not match:
        return {}, source
    fm_block, body = match.group(1), match.group(2)
    meta = {}
    for line in fm_block.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            meta[key.strip()] = val.strip().strip('"').strip("'")
    return meta, body


def markdown_to_html(md):
    """Minimal Markdown -> HTML converter covering what Sveltia's markdown
    widget produces: headers, bold/italic, links, paragraphs, lists."""
    lines = md.replace("\r\n", "\n").split("\n")
    html_parts = []
    para_buffer = []
    list_buffer = []

    def flush_para():
        if para_buffer:
            text = " ".join(para_buffer).strip()
            if text:
                html_parts.append(f"<p>{inline(text)}</p>")
            para_buffer.clear()

    def flush_list():
        if list_buffer:
            items = "".join(f"<li>{inline(i)}</li>" for i in list_buffer)
            html_parts.append(f"<ul>{items}</ul>")
            list_buffer.clear()

    def inline(text):
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
        text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)
        return text

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            flush_para()
            flush_list()
            continue
        h_match = re.match(r"^(#{1,3})\s+(.*)$", line)
        if h_match:
            flush_para()
            flush_list()
            level = len(h_match.group(1)) + 1  # markdown h1 -> page h2, etc.
            level = min(level, 4)
            html_parts.append(f"<h{level}>{inline(h_match.group(2))}</h{level}>")
            continue
        if line.startswith("- "):
            flush_para()
            list_buffer.append(line[2:])
            continue
        flush_para() if list_buffer else None
        flush_list()
        para_buffer.append(line)

    flush_para()
    flush_list()
    return "\n".join(html_parts)


def format_display_date(date_str):
    try:
        d = datetime.datetime.strptime(date_str[:10], "%Y-%m-%d")
        return d.strftime("%B %-d, %Y") if os.name != "nt" else d.strftime("%B %d, %Y")
    except ValueError:
        return date_str


def build_markdown_posts():
    """Reads content/posts/*.md, renders each into a full blog post page
    (same visual template as the rest of the site), returns metadata for
    the blog listing page and the sitemap."""
    posts = []
    if not os.path.isdir(CONTENT_POSTS):
        return posts

    for filename in sorted(os.listdir(CONTENT_POSTS)):
        if not filename.endswith(".md"):
            continue
        slug = filename[:-3]
        source = read(os.path.join(CONTENT_POSTS, filename))
        meta, body_md = parse_frontmatter(source)

        title = meta.get("title", "Untitled Post")
        date = meta.get("date", "")
        category = meta.get("category", "Blog")
        teaser = meta.get("teaser", "")
        image = meta.get("image", "/images/blog-placeholder.jpg")
        display_date = format_display_date(date)
        body_html = markdown_to_html(body_md)

        schema = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "author": {{ "@type": "Person", "name": "Phil Kruse" }},
  "datePublished": "{date}",
  "image": "https://www.iamphilkruse.com{image}",
  "publisher": {{ "@type": "Organization", "name": "Phil Kruse Real Estate" }}
}}
</script>'''

        page_meta = {
            "TITLE": f"{title} | Phil Kruse Blog",
            "DESC": teaser,
            "PATH": f"/blog/{slug}",
            "NAV": "blog",
            "SCHEMA": schema,
        }

        page_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
{{{{HEAD}}}}
</head>
<body>
{{{{NAV}}}}

<main>
  <article class="section--tight section" style="padding-top: var(--space-5);">
    <div class="wrap" style="max-width: 780px;">
      <span class="eyebrow">{category}</span>
      <h1>{title}</h1>
      <p class="post-card__meta" style="margin-bottom: var(--space-3);">By Phil Kruse · {display_date}</p>

      <div class="post-card__img" style="margin-bottom: var(--space-3); aspect-ratio: 16/9;">
        <img src="{image}" alt="{title}">
      </div>

      <div style="font-size: 1.08rem;">
        {body_html}
      </div>

      <div class="card" style="margin-top: var(--space-4);">
        <h3>Thinking About Buying or Selling on the Water?</h3>
        <p>Let's talk about what's next.</p>
        <a href="/contact" class="btn btn--gold">Get In Touch</a>
      </div>
    </div>
  </article>
</main>

{{{{FOOTER}}}}
</body>
</html>'''

        html = page_html.replace("{{HEAD}}", build_head(page_meta))
        html = html.replace("{{NAV}}", build_nav(page_meta))
        html = html.replace("{{FOOTER}}", build_footer())

        out_path = os.path.join(OUT, "blog", f"{slug}.html")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print("built: blog/%s.html" % slug)

        posts.append({
            "slug": slug, "title": title, "date": date,
            "display_date": display_date, "category": category,
            "teaser": teaser, "image": image,
        })

    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def render_post_cards(posts, limit=None):
    items = posts[:limit] if limit else posts
    if not items:
        return '<p class="lede">New posts coming soon.</p>'
    cards = []
    for p in items:
        cards.append(f'''<a href="/blog/{p['slug']}" class="post-card">
          <div class="post-card__img"><img src="{p['image']}" alt=""></div>
          <span class="post-card__meta">{p['category']} · {p['display_date']}</span>
          <h3>{p['title']}</h3>
          <p>{p['teaser']}</p>
        </a>''')
    return '<div class="grid-3">\n        ' + "\n        ".join(cards) + '\n      </div>'


def render_page(src_path, out_path, extra_replacements=None):
    source = read(src_path)
    meta, body = parse_meta(source)

    html = body.replace("{{HEAD}}", build_head(meta))
    html = html.replace("{{NAV}}", build_nav(meta))
    html = html.replace("{{FOOTER}}", build_footer())
    if extra_replacements:
        for token, value in extra_replacements.items():
            html = html.replace(token, value)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("built:", os.path.relpath(out_path, OUT))


def clean_output():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)


def copy_static():
    for folder in ("css", "js", "images"):
        src = os.path.join(ROOT, folder)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(OUT, folder))
    robots = os.path.join(ROOT, "robots.txt")
    if os.path.isfile(robots):
        shutil.copy(robots, os.path.join(OUT, "robots.txt"))


def build_sitemap(built_paths):
    base = "https://www.iamphilkruse.com"
    urls = []
    for path in built_paths:
        rel = os.path.relpath(path, OUT).replace(os.sep, "/")
        if os.path.basename(rel) == "index.html":
            dirname = os.path.dirname(rel)
            clean = "/" + dirname if dirname else ""
        else:
            clean = "/" + rel[:-5]  # strip .html
        urls.append(base + clean if clean else base + "/")

    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>',
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in sorted(set(urls)):
        xml_lines.append(f"  <url><loc>{url}</loc></url>")
    xml_lines.append("</urlset>")

    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(xml_lines) + "\n")
    print("built: sitemap.xml (%d URLs)" % len(set(urls)))


def build_tree(src_root, out_root, extra_replacements=None):
    # Flat output: about.html -> site_dist/about.html (Cloudflare Pages
    # serves this at the clean URL /about automatically).
    built = []
    for dirpath, _dirnames, filenames in os.walk(src_root):
        for filename in filenames:
            if not filename.endswith(".html"):
                continue
            src_path = os.path.join(dirpath, filename)
            rel = os.path.relpath(src_path, src_root)
            out_path = os.path.join(out_root, rel)
            render_page(src_path, out_path, extra_replacements)
            built.append(out_path)
    return built


def main():
    clean_output()
    copy_static()

    posts = build_markdown_posts()
    post_cards_html = render_post_cards(posts)
    home_cards_html = render_post_cards(posts, limit=3)

    built = []
    built += build_tree(SRC_PAGES, OUT, {"{{RECENT_POST_CARDS}}": home_cards_html})
    built += build_tree(SRC_BLOG, os.path.join(OUT, "blog"), {"{{POST_CARDS}}": post_cards_html})
    built += [os.path.join(OUT, "blog", f"{p['slug']}.html") for p in posts]

    build_sitemap(built)
    print("\nBuild complete ->", OUT)


if __name__ == "__main__":
    main()
