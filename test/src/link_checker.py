"""Lightweight link checker module made importable for testing.

Functions:
- load_skip_domains(base_dir=None)
- is_skipped(url, skip_domains)
- check_urls(urls, timeout=10, max_retries=2)
"""

import requests
import logging
import sys
from requests.adapters import HTTPAdapter
from pathlib import Path
import json
from urllib.parse import urlparse


def load_skip_domains(base_dir=None):
    """Load skip domains from test/skip_domains.txt.

    The new expected format is a JSON array in test/skip_domains.txt. If parsing
    as JSON fails, fall back to the legacy one-domain-per-line format. The
    optional base_dir parameter makes this function testable.
    """
    base = Path(__file__).resolve().parents[1] if base_dir is None else Path(base_dir)
    skip_file = base / 'skip_domains.txt'
    skip_domains = []
    if skip_file.exists():
        try:
            with open(skip_file, 'r', encoding='utf-8') as f:
                content = f.read()
            # Try JSON first (new format)
            try:
                data = json.loads(content)
                if isinstance(data, list):
                    skip_domains = [str(d).strip().lower() for d in data if str(d).strip() and not str(d).strip().startswith('#')]
            except json.JSONDecodeError:
                # Fallback: one domain per line
                skip_domains = [line.strip().lower() for line in content.splitlines() if line.strip() and not line.strip().startswith('#')]
        except Exception:
            logging.warning("Unable to read skip_domains file; proceeding without skiplist")
    return skip_domains


def is_skipped(url, skip_domains):
    try:
        host = urlparse(url).hostname or ''
        host = host.lower()
        for d in skip_domains:
            if host == d or host.endswith('.' + d):
                return True
        return False
    except Exception:
        return False


def check_urls(urls, timeout=10, max_retries=2):
    """Check a list of URLs and exit with non-zero code on failures.

    Uses Retry on the requests session where available, and honors the
    skiplist loaded from test/skip_domains.txt (JSON or legacy format).
    """
    try:
        # urllib3 v1.26+ uses "allowed_methods". Older versions used "method_whitelist".
        from urllib3.util.retry import Retry
        retry_kwargs = {"total": max_retries, "backoff_factor": 0.5, "status_forcelist": [429, 500, 502, 503, 504]}
        try:
            retry = Retry(**retry_kwargs, allowed_methods=frozenset(["GET", "HEAD"]))
        except TypeError:
            # Fallback for older urllib3
            retry = Retry(**retry_kwargs, method_whitelist=frozenset(["GET", "HEAD"]))
    except Exception:
        Retry = None
        retry = None

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    session = requests.Session()
    # Use a browser-like User-Agent and common headers to reduce blocking by anti-bot filters
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://matthlud.github.io/"
    })

    base_dir = Path(__file__).resolve().parents[1]
    skip_domains = load_skip_domains(base_dir=base_dir)

    if retry is not None:
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

    failed_urls = []

    for url in urls:
        # Skip known paywalled or anti-bot domains per skiplist
        if is_skipped(url, skip_domains):
            logging.info(f"Skipping URL (skiplist): {url}")
            continue
        try:
            response = session.get(url, timeout=timeout)
            if 200 <= response.status_code < 300:
                logging.info(f"URL is accessible: {url}")
            else:
                logging.warning(f"URL returned status code {response.status_code}: {url}")
                failed_urls.append((url, response.status_code))
        except requests.exceptions.RequestException as e:
            logging.error(f"Error accessing {url}: {e}")
            failed_urls.append((url, str(e)))
            # continue checking other URLs rather than breaking early

    if failed_urls:
        logging.error("Summary of failed URLs:")
        for u, reason in failed_urls:
            logging.error(f"{u} -> {reason}")
        sys.exit(1)
