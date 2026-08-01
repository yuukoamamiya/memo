#!/usr/bin/env python3
"""Generate docsify sidebar and full-text search index from the docs folder.

Run from the repo root:
    python scripts/gen.py

Outputs (into docs/, both gitignored):
    _sidebar.md         - sidebar, one group per folder
    search-index.json   - per-doc plain text used by docs/search.js

Pure standard library, so it runs in CI with no pip dependencies.
"""
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


FORMAT_CHARS = re.compile(r"[*_`<>\[\]|=]")  # markdown-ish chars -> distrust as title


def title_of(path):
    """First heading (ATX / setext / whole-line link); else first clean line; else filename."""
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
        if not FORMAT_CHARS.search(s) and len(s) <= 60:
            return s
        return os.path.splitext(os.path.basename(path))[0]
    return os.path.splitext(os.path.basename(path))[0]


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
            title = title_of(path)
            href = quote_href(rel[:-3])  # strip .md; docsify appends it back
            lines.append(f"  - [{title}]({href})")
    return "\n".join(lines) + "\n"


def build_index(entries):
    index = []
    for name, _ in SECTIONS:
        for rel, path in entries[name]:
            index.append({"path": rel, "title": title_of(path), "text": plain_text(path)})
    return index


def main():
    entries = collect()
    with open(os.path.join(DOCS, "_sidebar.md"), "w", encoding="utf-8") as f:
        f.write(build_sidebar(entries))
    with open(os.path.join(DOCS, "search-index.json"), "w", encoding="utf-8") as f:
        json.dump(build_index(entries), f, ensure_ascii=False, separators=(",", ":"))
    total = sum(len(v) for v in entries.values())
    size = os.path.getsize(os.path.join(DOCS, "search-index.json"))
    print(f"generated {total} docs -> docs/_sidebar.md, docs/search-index.json ({size / 1024 / 1024:.2f} MB)")


if __name__ == "__main__":
    main()
