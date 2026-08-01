#!/usr/bin/env python3
"""Generate docsify sidebar and full-text search index from the docs folder.

Run from the repo root:
    python scripts/gen.py

Outputs (into docs/, both gitignored):
    _sidebar.md         - sidebar, one group per folder
    search-index.json   - per-doc plain text used by docs/search.js

Pure standard library, so it runs in CI with no pip dependencies.
"""
import hashlib
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")

# (folder name, sidebar section title)
SECTIONS = [
    ("inbox", "收件箱"),
    ("archived", "存档"),
    ("wastebasket", "废纸篓"),
]

IMG = re.compile(r"!\[[^\]]*\]\([^)]*\)")          # images incl. base64 data URIs
LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")        # [text](url) -> text
WHOLE_LINK = re.compile(r"^\[([^\]]+)\]\([^)]*\)$")  # a line that is only a link
WHOLE_IMG = re.compile(r"^!\[[^\]]*\]\([^)]*\)$")     # a line that is only an image
TAG = re.compile(r"<[^>]+>")                        # html tags
FENCE = re.compile(r"```[\s\S]*?```")               # code fences
ATX = re.compile(r"^#{1,6}\s*", re.M)               # ATX heading markers
WS = re.compile(r"[ \t\u3000]+")
NBLANK = re.compile(r"\n{2,}")


def read(path):
    with open(path, encoding="utf-8-sig") as f:  # tolerate BOM
        return f.read()


TRAILING_DOTS = re.compile(r"\.+$")
CIRCLE_SUFFIX = re.compile(
    r"\s*-\s*(?:哔哩哔哩\s*-\s*)?Circle\s*阅读助手$|\s*-\s*哔哩哔哩$"
)
ESC_PIPE = re.compile(r"\\\|")  # Circle escapes a literal pipe in headings


def first_heading(path):
    """First real heading (ATX / setext / whole-line link) in the doc, or None."""
    lines = read(path).splitlines()
    for i, line in enumerate(lines):
        s = line.strip()
        if not s or WHOLE_IMG.match(s):
            continue
        is_atx = s.startswith("#")
        if is_atx:
            s = s.lstrip("#").strip()
        m = WHOLE_LINK.match(s)
        if m:
            s = m.group(1).strip()
        is_setext = i + 1 < len(lines) and re.match(r"^={3,}$", lines[i + 1].strip())
        if is_atx or is_setext or m:
            return s
    return None


def display_title(path):
    """Article title for the sidebar / search index.

    The filename is Circle-generated from the real article title and is the most
    reliable source (the first line in the doc can be Circle's own wrapper, e.g.
    "[译者序](bilibili...)" or the source-page title for Zhihu exports).
    Only when Circle truncated the filename (ends with "...") do we fall back to
    the first real heading inside the doc.
    """
    stem = os.path.splitext(os.path.basename(path))[0]

    file_title = CIRCLE_SUFFIX.sub("", stem)
    file_title = TRAILING_DOTS.sub("", file_title)
    file_title = file_title.replace("_", " ")
    file_title = WS.sub(" ", file_title).strip()

    if TRAILING_DOTS.search(stem):
        doc = first_heading(path)
        if doc:
            doc = ESC_PIPE.sub("|", doc)
            doc = TRAILING_DOTS.sub("", doc).strip()
            if doc:
                return doc
    return file_title


def plain_text(path):
    text = read(path)
    text = FENCE.sub(" ", text)
    text = IMG.sub(" ", text)
    text = LINK.sub(r"\1", text)
    text = TAG.sub(" ", text)
    text = ATX.sub("", text)
    text = text.replace("\r\n", "\n")
    text = WS.sub(" ", text)
    text = NBLANK.sub("\n", text)
    return text.strip()


def quote_href(path):
    """Keep CJK readable, only encode characters that break URLs."""
    return path.replace(" ", "%20")


def collect():
    entries = {name: [] for name, _ in SECTIONS}
    for name, _ in SECTIONS:
        folder = os.path.join(DOCS, name)
        if not os.path.isdir(folder):
            continue
        for filename in sorted(os.listdir(folder)):
            if not filename.endswith(".md") or filename == "README.md":
                continue
            path = os.path.join(folder, filename)
            rel = f"{name}/{filename}"
            entries[name].append((rel, path))
    return entries


def build_sidebar(entries):
    lines = []
    for name, label in SECTIONS:
        items = entries[name]
        if not items:
            continue
        lines.append(f"- **{label}**")
        for rel, path in items:
            title = display_title(path)
            href = quote_href(rel[:-3])  # strip .md; docsify appends it back
            lines.append(f"  - [{title}]({href})")
    return "\n".join(lines) + "\n"


def build_index(entries):
    return [
        {"path": rel, "title": display_title(path), "text": plain_text(path)}
        for name, _ in SECTIONS
        for rel, path in entries[name]
    ]


def main():
    entries = collect()
    with open(os.path.join(DOCS, "_sidebar.md"), "w", encoding="utf-8") as f:
        f.write(build_sidebar(entries))

    index = {"version": "", "docs": build_index(entries)}
    blob = json.dumps(index, ensure_ascii=False, separators=(",", ":"))
    index["version"] = hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]
    with open(os.path.join(DOCS, "search-index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, separators=(",", ":"))

    total = sum(len(v) for v in entries.values())
    size = os.path.getsize(os.path.join(DOCS, "search-index.json"))
    print(f"generated {total} docs -> docs/_sidebar.md, docs/search-index.json "
          f"(v{index['version']}, {size / 1024 / 1024:.2f} MB)")


if __name__ == "__main__":
    main()
