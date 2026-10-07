#!/usr/bin/env python3
"""Render checked-in documentation to a self-contained static website."""
import html
import json
import posixpath
import re
import shutil
import hashlib
import zipfile
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

import markdown

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"
CONTENT = ROOT / "content"

def relative(current, target):
    return posixpath.relpath(target, posixpath.dirname(current) or ".")

def source_route(module_id, path):
    return f"sources/{module_id}/{posixpath.splitext(path)[0]}.html"

def markdown_render(text):
    md = markdown.Markdown(extensions=["fenced_code", "tables", "toc", "sane_lists"],
                           extension_configs={"toc": {"permalink": "#", "toc_depth": "2-3"}})
    body = md.convert(text)
    return body, md.toc, md.toc_tokens

def load_pages():
    inventory = json.loads((CONTENT / "modules.json").read_text())
    modules = inventory["modules"]
    if len({m["id"] for m in modules}) != len(modules):
        raise ValueError("Duplicate component id")
    pages = {}
    for folder, prefix in [("pages", ""), ("modules", "modules/"), ("guides", "how-to/")]:
        for path in sorted((CONTENT / folder).rglob("*.md")):
            route = prefix + path.relative_to(CONTENT / folder).with_suffix(".html").as_posix()
            text = path.read_text()
            title_match = re.search(r"^# (.+)$", text, re.M)
            if not title_match:
                raise ValueError(f"Missing title: {path}")
            if route in pages:
                raise ValueError(f"Duplicate route: {route}")
            pages[route] = {"title": title_match[1], "text": text, "source": None}
    for m in modules:
        for doc in m["sources"]:
            path = CONTENT / "sources" / m["id"] / doc["path"]
            route = source_route(m["id"], doc["path"])
            text = path.read_text()
            title = re.search(r"^# (.+)$", text, re.M)
            pages[route] = {"title": title[1] if title else doc["path"], "text": text,
                            "source": {"module": m, "doc": doc}}
    pages["404.html"] = {"title": "Page not found", "text": "# Page not found\n\nThis address does not point to a documentation page.\n\n[Return to the introduction](index.html) · [Browse modules](modules/index.html) · [Find an installation guide](how-to/index.html)", "source": None}
    return inventory, pages

def rewrite_links(body, route, page, pages):
    def replace(match):
        attr, value = match[1], html.unescape(match[2])
        parsed = urlsplit(value)
        if parsed.scheme:
            if parsed.scheme not in {"https", "http", "mailto"}:
                raise ValueError(f"Unsafe URL scheme on {route}: {parsed.scheme}")
            return match[0]
        if not parsed.path or value.startswith("//"):
            return match[0]
        if page["source"]:
            source = page["source"]
            m, doc = source["module"], source["doc"]
            source_path = posixpath.normpath(posixpath.join(posixpath.dirname(doc["path"]), unquote(parsed.path)))
            target = source_route(m["id"], source_path)
            if target in pages and attr == "href":
                value = relative(route, target)
                if parsed.fragment:
                    value += "#" + parsed.fragment
            else:
                value = f"{m['repository']}/{'raw' if attr == 'src' else 'blob'}/{m['commit']}/{quote(source_path, safe='/')}"
                if parsed.fragment:
                    value += "#" + parsed.fragment
        else:
            # Curated docs use site-root relative destinations without a leading slash.
            target = unquote(parsed.path)
            if target not in pages and not target.startswith(("assets/", "downloads/")):
                raise ValueError(f"Unknown curated link on {route}: {value}")
            value = relative(route, target)
            if parsed.fragment:
                value += "#" + parsed.fragment
        return f'{attr}="{html.escape(value, quote=True)}"'
    return re.sub(r'(href|src)="([^"]+)"', replace, body)

def navigation(route, modules):
    groups = [("Start here", [("index.html", "Introduction"), ("getting-started.html", "Getting started")]),
              ("System architecture", [("architecture/index.html", "Overview & workflows"), ("architecture/security.html", "Security model"), ("architecture/configuration.html", "Configuration"), ("architecture/frontend.html", "Frontend architecture"), ("architecture/dependencies.html", "Dependencies")]),
              ("Explore the platform", [("modules/index.html", "Module directory"), ("how-to/index.html", "Installation guides"), ("how-to/native-prerequisites.html", "Native prerequisites")])]
    active_module = next((m for m in modules if route == f"modules/{m['id']}.html" or route.startswith(f"how-to/{m['id']}/") or route.startswith(f"sources/{m['id']}/")), None)
    if active_module:
        m = active_module
        links = [(f"modules/{m['id']}.html", f"{m['name']} reference")]
        if m["binary"]:
            links += [(f"how-to/{m['id']}/docker.html", "Install with Docker"), (f"how-to/{m['id']}/native.html", "Install without Docker")]
        groups.append(("In this module", links))
    result = []
    for label, links in groups:
        result.append(f'<div class="nav-group"><p class="nav-label">{html.escape(label)}</p>')
        for target, title in links:
            active = ' aria-current="page"' if target == route else ""
            result.append(f'<a href="{relative(route, target)}"{active}>{html.escape(title)}</a>')
        result.append("</div>")
    return "".join(result)

def topology():
    return '''<div class="topology" role="img" aria-label="Browsers connect to the Portal gateway. It uses Auth for user authorization and routes to modules through the secure service mesh. LCM issues mesh identities.">
<div class="topology-label">THE CONNECTED PLATFORM</div>
<div class="topology-client">Browser &amp; API clients</div><div class="topology-arrow" aria-hidden="true">↓ HTTPS</div>
<div class="topology-gateway"><span>PUBLIC EDGE</span><strong>Portal / Gateway</strong><small>Registry · API proxy · UI shell</small></div>
<div class="topology-arrow" aria-hidden="true">↓ SPIFFE · mTLS · policy</div>
<div class="topology-row"><div><strong>Auth</strong><small>Identity &amp; access</small></div><div><strong>LCM</strong><small>Mesh certificates</small></div></div>
<div class="topology-modules"><span>Inventory</span><span>IPAM</span><span>Paperless</span><span>Signing</span><span>HR</span><span>+ 9 services</span></div>
<p>Independent modules. A shared security foundation.</p></div>'''

def homepage(route):
    return f'''<section class="hero"><div class="hero-copy"><p class="eyebrow"><span class="status-dot"></span> GO-TANGRA / V4 DOCUMENTATION</p>
<h1>One platform.<br><span>Every system connected.</span></h1>
<p class="hero-description">A modular platform for infrastructure, operations and business workflows. Understand the architecture. Choose your modules. Build on a secure foundation.</p>
<div class="hero-actions"><a class="button primary" href="{relative(route, 'getting-started.html')}">Get started <span aria-hidden="true">↗</span></a><a class="button secondary" href="{relative(route, 'architecture/index.html')}">Explore the architecture <span aria-hidden="true">→</span></a></div>
<div class="hero-facts"><span><strong>17</strong> services</span><span><strong>2</strong> installation paths</span><span><strong>v4</strong> secure foundation</span></div></div>{topology()}</section>'''

def layout(route, page, body, toc, modules):
    e = html.escape
    title = page["title"]
    nav = navigation(route, modules)
    source = page["source"]
    provenance = ""
    if source:
        m, doc = source["module"], source["doc"]
        provenance = f'<div class="source-note">Source reference · {e(m["name"])} · <code>{e(m["commit"][:12])}</code><br><a href="{e(doc["url"])}">View {e(doc["path"])} at the recorded revision ↗</a></div>'
    title_block = "" if route == "index.html" else f'<div class="page-heading"><p class="eyebrow">GO-TANGRA / {e("SOURCE REFERENCE" if source else route.split("/")[0].removesuffix(".html").replace("-", " ").upper())}</p><h1>{e(title)}</h1><p class="page-meta">V4 documentation · source snapshot 05 October 2026</p></div>'
    # Title is supplied by the layout; preserve source headings below it.
    body = re.sub(r"<h1[^>]*>.*?</h1>", "", body, count=1, flags=re.S)
    hero = homepage(route) if route == "index.html" else ""
    toc_html = f'<aside class="page-toc" aria-label="On this page"><p class="nav-label">On this page</p>{toc}</aside>' if toc and '<li>' in toc and route != "index.html" else ""
    inline_toc = f'<details class="inline-toc"><summary>On this page</summary>{toc}</details>' if toc_html else ""
    description = "Go-Tangra v4 architecture, module references and Docker/native installation guides."
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)} · Go-Tangra</title><meta name="description" content="{description}"><meta name="color-scheme" content="light"><link rel="icon" href="{relative(route, 'assets/favicon.svg')}" type="image/svg+xml"><link rel="stylesheet" href="{relative(route, 'assets/site.css')}"><script src="{relative(route, 'assets/site.js')}" defer></script></head>
<body><a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><a class="brand" href="{relative(route, 'index.html')}"><span class="brand-mark" aria-hidden="true">T</span><span>go-tangra<span class="brand-sub"> / docs</span></span></a>
<nav class="header-nav" aria-label="Main navigation"><a href="{relative(route, 'architecture/index.html')}">Architecture</a><a href="{relative(route, 'modules/index.html')}">Modules</a><a href="{relative(route, 'how-to/index.html')}">How-to</a></nav>
<div class="header-tools"><span class="version-pill">v4</span><button type="button" class="search-toggle" hidden aria-expanded="false" aria-controls="site-search">Search docs <span aria-hidden="true">⌕</span></button></div></header>
<section id="site-search" class="search-panel" hidden aria-label="Documentation search" data-index="{relative(route, 'assets/search.json')}" data-root="{relative(route, 'index.html').removesuffix('index.html')}"><label for="search-input">Search documentation</label><input id="search-input" type="search" placeholder="Module, architecture, installation…" autocomplete="off"><p id="search-status" role="status" aria-live="polite"></p><ul id="search-results"></ul></section>
<details class="mobile-menu"><summary>Documentation navigation</summary><nav aria-label="Mobile documentation">{nav}</nav></details>
<div class="site-layout"><aside class="sidebar"><nav aria-label="Documentation">{nav}</nav><div class="sidebar-note"><span class="status-dot"></span> Built for operators.<br>Open for builders.</div></aside>
<main id="main" tabindex="-1">{hero}<div class="reading-layout"><article class="prose">{title_block}{provenance}{inline_toc}{body}</article>{toc_html}</div></main></div>
<footer class="site-footer"><a class="brand footer-brand" href="{relative(route, 'index.html')}">go-tangra</a><span>Modular by design. Connected by trust.</span><a href="{relative(route, 'modules/platform.html')}">Source &amp; version information →</a></footer>
</body></html>'''

def build():
    inventory, pages = load_pages()
    rendered = {}
    index = []
    for route, page in pages.items():
        body, toc, tokens = markdown_render(page["text"])
        rendered[route] = (body, toc)
        # Give search readable context without indexing every copied code example.
        terms = re.findall(r"^#{1,3} (.+)$", page["text"], re.M)
        index.append({"title": page["title"], "url": route, "section": route.split("/")[0], "terms": " ".join(terms)})
    # Normalize upstream GitHub-style fragments to renderer ids where possible.
    ids = {route: set(re.findall(r' id="([^"]+)"', body)) for route, (body, _) in rendered.items()}
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets")
    package_compose(ROOT / "deploy/compose", OUT / "downloads")
    (OUT / "assets/search.json").write_text(json.dumps(index, ensure_ascii=False))
    for route, page in pages.items():
        body, toc = rendered[route]
        body = rewrite_links(body, route, page, pages)
        if page["source"]:
            def normalize(match):
                href = html.unescape(match[1])
                parsed = urlsplit(href)
                if parsed.scheme or not parsed.fragment:
                    return match[0]
                target = posixpath.normpath(posixpath.join(posixpath.dirname(route), parsed.path)) if parsed.path else route
                anchors = ids.get(target, set())
                fragment = parsed.fragment
                if fragment not in anchors:
                    # GitHub sometimes preserves a dash Python-Markdown removes.
                    candidates = [a for a in anchors if a.replace("-", "") == fragment.replace("-", "")]
                    if len(candidates) == 1:
                        href = href.rsplit("#", 1)[0] + "#" + candidates[0]
                    else:
                        # Preserve the exact upstream anchor as an external citation.
                        m, doc = page["source"]["module"], page["source"]["doc"]
                        rel_source = unquote(parsed.path)
                        href = doc["url"] + "#" + fragment if not rel_source else m["repository"] + "/blob/" + m["commit"] + "/" + target.removeprefix(f"sources/{m['id']}/").removesuffix(".html") + ".md#" + fragment
                return 'href="' + html.escape(href, quote=True) + '"'
            body = re.sub(r'href="([^"]+)"', normalize, body)
        dest = OUT / route
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(layout(route, page, body, toc, inventory["modules"]))
    print(f"Built {len(pages)} HTML pages for {len(inventory['modules'])} components in {OUT}")

def package_compose(source, destination):
    """Package only reviewed files, never private .env files or deployment state."""
    destination.mkdir(parents=True, exist_ok=True)
    for directory in sorted(source.iterdir()):
        if not directory.is_dir():
            continue
        manifest = json.loads((directory / "bundle.json").read_text())
        with zipfile.ZipFile(destination / f"{directory.name}.zip", "w", zipfile.ZIP_DEFLATED) as archive:
            for name, digest in sorted(manifest["files"].items()):
                path = Path(name)
                if path.is_absolute() or ".." in path.parts or name == ".env" or path.suffix in {".key", ".kek", ".pem"}:
                    raise ValueError(f"Unsafe Compose bundle file: {name}")
                file = directory / path
                if file.is_symlink() or not file.is_file():
                    raise ValueError(f"Missing/unsafe Compose bundle file: {file}")
                data = file.read_bytes()
                if hashlib.sha256(data).hexdigest() != digest:
                    raise ValueError(f"Compose bundle changed without review: {file}")
                dest = destination / directory.name / path
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
                entry = zipfile.ZipInfo(f"{directory.name}/{name}", date_time=(2026, 10, 5, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.external_attr = 0o100644 << 16
                archive.writestr(entry, data)

if __name__ == "__main__":
    build()
