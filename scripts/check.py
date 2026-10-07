#!/usr/bin/env python3
"""Check built routes, anchors, assets and source/installation contracts."""
import hashlib
import json
import posixpath
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.links = []
        self.titles = 0
        self.h1s = 0
        self.main = 0
        self.lang = None

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.append(values["id"])
        for attr in ("href", "src"):
            if attr in values:
                self.links.append(values[attr])
        self.titles += tag == "title"
        self.h1s += tag == "h1"
        self.main += tag == "main"
        if tag == "html":
            self.lang = values.get("lang")

def check_output(output):
    errors = []
    pages = {}
    for file in sorted(output.rglob("*.html")):
        parser = PageParser()
        parser.feed(file.read_text())
        route = file.relative_to(output).as_posix()
        pages[route] = parser
        duplicate = [key for key, count in Counter(parser.ids).items() if count > 1]
        if duplicate:
            errors.append(f"{route}: duplicate ids {duplicate}")
        if parser.titles != 1 or parser.h1s != 1 or parser.main != 1 or parser.lang != "en":
            errors.append(f"{route}: expected one title/h1/main and lang=en")
    if not pages:
        errors.append("No generated pages")
    for route, parser in pages.items():
        for link in parser.links:
            parsed = urlsplit(link)
            if parsed.scheme or link.startswith("//"):
                if parsed.scheme not in {"https", "http", "mailto", ""}:
                    errors.append(f"{route}: unsafe URL {link}")
                continue
            if parsed.path.startswith("/"):
                errors.append(f"{route}: root-relative link prevents subdirectory hosting: {link}")
                continue
            target = posixpath.normpath(posixpath.join(posixpath.dirname(route), unquote(parsed.path))) if parsed.path else route
            if target.startswith("../") or not (output / target).is_file():
                errors.append(f"{route}: missing target {link}")
            elif parsed.fragment and target in pages and unquote(parsed.fragment) not in pages[target].ids:
                errors.append(f"{route}: missing fragment {link}")
    return errors, len(pages)

def check_content(root):
    errors = []
    data = json.loads((root / "content/modules.json").read_text())
    for m in data["modules"]:
        if not m["module"].endswith("/v4"):
            errors.append(f"{m['id']}: non-v4 component")
        if m["commit"] == "unavailable":
            errors.append(f"{m['id']}: source revision is missing")
        for doc in m["sources"]:
            p = root / "content/sources" / m["id"] / doc["path"]
            if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != doc["sha256"]:
                errors.append(f"{m['id']}: source snapshot hash mismatch {doc['path']}")
        if not (root / "content/modules" / f"{m['id']}.md").is_file():
            errors.append(f"{m['id']}: missing module reference")
        if m["binary"]:
            for method in ("docker", "native"):
                path = root / "content/guides" / m["id"] / f"{method}.md"
                if not path.is_file():
                    errors.append(f"{m['id']}: missing {method} installation")
                    continue
                text = path.read_text()
                for phrase in ("## Prerequisites", "## Verify installation", "## Troubleshooting", "## Stop and remove", "## Sources"):
                    if phrase not in text:
                        errors.append(f"{m['id']}/{method}: missing {phrase}")
                if method == "native":
                    for code in re.findall(r"```(?:sh|bash)\n(.*?)```", text, re.S):
                        if re.search(r"^\s*(?:sudo\s+)?(?:docker\b|make\s+compose|sg docker)", code, re.M):
                            errors.append(f"{m['id']}: native procedure runs Docker")
    for path in (root / "assets").iterdir():
        if path.suffix in {".css", ".js"}:
            if re.search(r"https?://", path.read_text()):
                errors.append(f"{path.name}: runtime asset depends on external origin")
    return errors

def main():
    errors, count = check_output(ROOT / "dist")
    errors += check_content(ROOT)
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    print(f"PASS: {count} pages; internal links, fragments, assets, source hashes and both installation paths checked.")

if __name__ == "__main__":
    main()
