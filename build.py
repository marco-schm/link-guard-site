#!/usr/bin/env python3
"""Builds the Link Guard landing page.

Usage: build.py <checkout> <output dir>

<checkout> is the repository root (or a `git archive` of it) containing `src/`. Every
HTML page gets the fonts, the stylesheet and the shared header, footer and logo inlined,
because the site's Content-Security-Policy allows no external stylesheets and no
scripts.
"""
import shutil
import sys
from pathlib import Path

MARKERS = ("/* @fonts */", "/* @css */", "<!-- @symbol -->", "<!-- @header -->", "<!-- @footer -->")


def fail(message):
    print(f"build.py: {message}", file=sys.stderr)
    sys.exit(1)


def main(checkout: Path, out: Path) -> None:
    src = checkout / "src"
    if out.exists():
        fail(f"{out} already exists")
    read = lambda path: (src / path).read_text(encoding="utf-8").strip()
    parts = {
        "/* @fonts */": read("fonts/fonts.css"),
        "/* @css */": read("site.css"),
        "<!-- @symbol -->": read("partials/symbol.html"),
        "<!-- @header -->": read("partials/header.html"),
        "<!-- @footer -->": read("partials/footer.html"),
    }
    pages = sorted(p for p in src.rglob("*.html") if "partials" not in p.relative_to(src).parts)
    if not pages:
        fail("no pages found")
    out.mkdir(parents=True)
    for page in pages:
        text = page.read_text(encoding="utf-8")
        for marker in MARKERS:
            if text.count(marker) != 1:
                fail(f"{page.relative_to(src)}: expected {marker} exactly once")
            text = text.replace(marker, parts[marker])
        if "<!-- @" in text or "/* @" in text:
            fail(f"{page.relative_to(src)}: unknown marker left")
        target = out / page.relative_to(src)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    shutil.copytree(src / "assets", out / "assets")
    (out / "fonts").mkdir()
    shutil.copyfile(src / "fonts" / "OFL.txt", out / "fonts" / "OFL.txt")
    shutil.copyfile(src / "favicon.ico", out / "favicon.ico")
    for name in ("robots.txt", "sitemap.xml"):
        shutil.copyfile(src / name, out / name)
    print(f"built {len(pages)} pages")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        fail("usage: build.py <checkout> <output dir>")
    main(Path(sys.argv[1]), Path(sys.argv[2]))
