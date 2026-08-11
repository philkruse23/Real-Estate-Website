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

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_PAGES = os.path.join(ROOT, "src", "pages")
SRC_BLOG = os.path.join(ROOT, "src", "blog")
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


def render_page(src_path, out_path):
    source = read(src_path)
    meta, body = parse_meta(source)

    html = body.replace("{{HEAD}}", build_head(meta))
    html = html.replace("{{NAV}}", build_nav(meta))
    html = html.replace("{{FOOTER}}", build_footer())

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


def build_tree(src_root, out_root):
    # Flat output: about.html -> site_dist/about.html (Cloudflare Pages
    # serves this at the clean URL /about automatically). Blog posts stay
    # flat inside /blog/ per the playbook, no per-post subfolders.
    for dirpath, _dirnames, filenames in os.walk(src_root):
        for filename in filenames:
            if not filename.endswith(".html"):
                continue
            src_path = os.path.join(dirpath, filename)
            rel = os.path.relpath(src_path, src_root)
            out_path = os.path.join(out_root, rel)
            render_page(src_path, out_path)


def main():
    clean_output()
    copy_static()
    build_tree(SRC_PAGES, OUT)
    build_tree(SRC_BLOG, os.path.join(OUT, "blog"))
    print("\nBuild complete ->", OUT)


if __name__ == "__main__":
    main()
