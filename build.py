#!/usr/bin/env python3
"""Assemble index.html from src/shell.html + src/sections/*.html.

Section files are HTML with two shorthands:
  ```lang title=optional     fenced code, escaped automatically
  `inline`                   inline code, escaped automatically
src/favicon.svg is copied to the site root alongside it.
Run: python3 build.py
"""
import html, pathlib, re, shutil, sys

root = pathlib.Path(__file__).parent
FENCE = re.compile(r"^```(\w+)(?: title=([^\n]+))?\n(.*?)^```[ \t]*$", re.M | re.S)
INLINE = re.compile(r"`([^`\n]+)`")
PLAIN = {"http", "text"}


def code_block(m):
    lang, title, body = m.group(1), m.group(2), m.group(3).rstrip("\n")
    cls = "nohighlight" if lang in PLAIN else f"language-{lang}"
    head = f'<div class="code-head"><span>{html.escape(title or lang)}</span></div>'
    return f'<div class="code">{head}<pre><code class="{cls}">{html.escape(body, quote=False)}</code></pre></div>'


def convert(src):
    out, pos = [], 0
    for m in FENCE.finditer(src):
        out.append(INLINE.sub(lambda i: f"<code>{html.escape(i.group(1), quote=False)}</code>", src[pos:m.start()]))
        out.append(code_block(m))
        pos = m.end()
    out.append(INLINE.sub(lambda i: f"<code>{html.escape(i.group(1), quote=False)}</code>", src[pos:]))
    return "".join(out)


sections = "\n".join(convert(p.read_text(encoding="utf-8")) for p in sorted((root / "src" / "sections").glob("*.html")))
page = (root / "src" / "shell.html").read_text(encoding="utf-8").replace("<!--SECTIONS-->", sections)

# sanity checks: unique ids, internal links resolve
ids = re.findall(r'\sid="([^"]+)"', page)
dupes = {i for i in ids if ids.count(i) > 1}
missing = {h for h in re.findall(r'href="#([^"]+)"', sections) if h not in ids}
if dupes or missing:
    sys.exit(f"duplicate ids: {dupes}\nbroken links: {missing}")

(root / "index.html").write_text(page, encoding="utf-8")
shutil.copyfile(root / "src" / "favicon.svg", root / "favicon.svg")
print(f"index.html  {len(page) / 1024:.0f} KB  {page.count('class=\"topic\"')} topics")
