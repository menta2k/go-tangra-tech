import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

build = load("build")
check = load("check")

class SiteContractTests(unittest.TestCase):
    def test_all_generated_routes_and_fragments_resolve(self):
        errors, count = check.check_output(ROOT / "dist")
        self.assertEqual([], errors)
        self.assertGreaterEqual(count, 100)

    def test_source_hashes_and_method_completeness(self):
        self.assertEqual([], check.check_content(ROOT))

    def test_deep_routes_work_under_subdirectory_hosting(self):
        self.assertEqual("../../modules/lcm.html", build.relative("how-to/lcm/native.html", "modules/lcm.html"))
        self.assertEqual("../../assets/site.css", build.relative("how-to/lcm/native.html", "assets/site.css"))
        self.assertEqual("../../../architecture/index.html", build.relative("sources/lcm/docs/operations.html", "architecture/index.html"))

    def test_source_relative_links_retain_commit_provenance(self):
        inv, pages = build.load_pages()
        route = "sources/lcm/README.html"
        result = build.rewrite_links('<a href="docs/operations.md">ops</a><a href="cmd/lcmsvc/main.go">source</a>', route, pages[route], pages)
        self.assertIn('href="docs/operations.html"', result)
        m = next(m for m in inv["modules"] if m["id"] == "lcm")
        self.assertIn(f"/blob/{m['commit']}/cmd/lcmsvc/main.go", result)

    def test_checker_detects_broken_fragments_and_duplicate_ids(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "index.html").write_text('<html lang="en"><title>x</title><main><h1>x</h1><p id="repeat"></p><p id="repeat"></p><a href="#missing">x</a></main></html>')
            errors, count = check.check_output(p)
            self.assertEqual(1, count)
            self.assertTrue(any("duplicate ids" in e for e in errors))
            self.assertTrue(any("missing fragment" in e for e in errors))

    def test_checker_detects_missing_assets_and_root_relative_links(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "index.html").write_text('<html lang="en"><title>x</title><main><h1>x</h1><script src="missing.js"></script><a href="/modules/lcm.html">LCM</a></main></html>')
            errors, _ = check.check_output(p)
            self.assertTrue(any("missing target" in e for e in errors))
            self.assertTrue(any("root-relative" in e for e in errors))

    def test_renderer_rejects_unsafe_link_protocol(self):
        with self.assertRaises(ValueError):
            build.rewrite_links('<a href="javascript:alert(1)">bad</a>', "index.html", {"source": None}, {})

    def test_title_and_source_labels_are_escaped(self):
        inventory = json.loads((ROOT / "content/modules.json").read_text())
        rendered = build.layout("getting-started.html", {"title": '<img src=x onerror="alert(1)">', "source": None}, "<h1>title</h1><p>body</p>", "", inventory["modules"])
        self.assertIn('&lt;img src=x onerror=&quot;alert(1)&quot;&gt;', rendered)
        self.assertNotIn('<img src=x', rendered)

    def test_install_routes_exist_for_every_service_and_no_framework_image(self):
        inventory, pages = build.load_pages()
        for m in inventory["modules"]:
            if m["binary"]:
                self.assertIn(f"how-to/{m['id']}/docker.html", pages)
                self.assertIn(f"how-to/{m['id']}/native.html", pages)
            else:
                self.assertIsNone(m["image"])
                self.assertNotIn(f"how-to/{m['id']}/docker.html", pages)

    def test_base_stack_exceptions_are_explicit(self):
        inventory, _ = build.load_pages()
        for m in inventory["modules"]:
            if m["id"] in {"scheduler", "sms-gw", "asterisk"}:
                self.assertIsNone(m["stack_service"])
            if m["id"] == "portal":
                self.assertEqual("gateway", m["stack_service"])
                self.assertEqual("shell", m["build_tags"])

if __name__ == "__main__":
    unittest.main()
