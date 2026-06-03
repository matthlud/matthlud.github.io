# Copilot instructions for matthlud.github.io

This file gives Copilot sessions focused, repository-specific guidance so suggestions and automated changes are relevant.

## Quick commands (build / test / lint)
- No build system or JS toolchain: site is plain static HTML (index.html) + assets/. To preview locally:
  - Serve locally: `python -m http.server 8000` and open `http://localhost:8000` (run from repo root).

- Tests (URL accessibility check):
  - Install dependencies (recommended in a venv):
    ```bash
    cd test
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    ```
  - Run the full URL check (same as CI):
    ```bash
    python test/src/main.py
    ```
  - Run the checker for a single URL (quick smoke):
    ```bash
    python -c "from test.src.check_urls import check_urls; check_urls(['https://example.com'])"
    ```

- Lint: none configured in this repository.

## High-level architecture (big picture)
- This is a user GitHub Pages repository (username.github.io) containing a static site (root `index.html`) and `assets/` for images and icons.
- Link-health tooling lives under `test/`:
  - `test/src/utils.py` — parses HTML and extracts external `http(s)` links using BeautifulSoup.
  - `test/src/check_urls.py` — uses `requests` (+ retry/HTTPAdapter) to verify links and exits non‑zero on failures.
  - `test/src/main.py` — default entry point: reads `index.html` and runs the checker.
- CI: `.github/workflows/url_check.yml` runs the checker nightly on `ubuntu-latest` with Python 3.8.

## Key conventions and repo-specific patterns
- Tests expect to be run from the repository root and default to `index.html` (see `test/src/main.py: html_path = "index.html"`). If HTML is moved, update `main.py` or pass a different path when invoking the utilities.
- Only absolute `http`/`https` links are checked. Relative links, anchors, `mailto:`, etc., are ignored (see `load_urls_from_html`).
- `check_urls` logs results and calls `sys.exit(1)` when there are failures; CI relies on this non-zero exit code to mark the run as failed.
- A skiplist is available at `test/skip_domains.txt` (one domain per line). Domains in that file are skipped during CI runs to avoid failures caused by paywalled or anti-bot protected sites. Edit that file to customize behavior.
- The checker uses retries for transient server errors (429, 5xx). Consider adjusting `timeout` and `max_retries` in `check_urls` for flaky external services.
- The workflow installs dependencies from `test/requirements.txt` — any dependency added there should be compatible with Python 3.8 (or update the workflow if changing the runtime).

## Where to look
- Site content: `index.html`, `assets/`
- Link-checker: `test/README.md`, `test/src/{main,utils,check_urls}.py`, `test/requirements.txt`
- CI: `.github/workflows/url_check.yml`

## Assistant integration notes
- No other AI-assistant configuration files were found (e.g., CLAUDE.md, AGENTS.md, .cursorrules). Add repo-specific assistant rules here if needed.
- When Copilot edits content related to link-checks, prefer small, surgical changes: update `test/src/main.py` path if `index.html` moves, or add dependencies to `test/requirements.txt` and update the workflow to install them.

---

(Generated from README.md and test/README.md to help future Copilot sessions understand how to run and modify tooling.)
