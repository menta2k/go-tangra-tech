# Documentation Data Model

## Component inventory (`content/modules.json`)

Each component contains unique `id`, human `name`, `category`, `summary`, `checkout`, canonical repository URL, actual Go module path, local `commit`, `tag`, `go_version`, `toolchain`, service `binary` (null for framework), `ui_dir`, `build_tags`, configuration reference path, bootstrap support and syntax, admin address, image, platform-stack presence, required/optional dependencies, source document metadata and guide validation state.

A component has many source documents and a module reference. Installable components have exactly two installation pages. The framework is consumed as a Go module and has no service image. SDKs, UI kit and optional contrib packages are documented as consumed libraries rather than standalone services.

Validation: unique lowercase ids; no legacy Go major; every imported file has relative source path, SHA-256 and commit; do not serialize credentials or config values from real deployments. Git tags are informational and not proof of image publication.

## Page

Fields: route, title, description, section, Markdown body, optional component id and source citation. Routes are unique relative HTML files with stable heading ids. Pages use a shared layout and link to related reference/guide pages. Unknown page output is `404.html`.

## Source snapshot

Fields: component id, original repository-relative path, commit, SHA-256, snapshot route. Only explicit documentation and API descriptions may be imported; no .env, secrets, private keys or arbitrary configuration snapshots. Source-relative links target imported snapshots when available, otherwise the canonical repository at the recorded commit.

## Installation validation

States: source-reviewed → environment-tested → release-approved. Initially source-reviewed. Only actual isolated deployment results may advance the state. Record environment, versions, command outcome and tester in feature validation evidence. A successful site build cannot advance installation state.
