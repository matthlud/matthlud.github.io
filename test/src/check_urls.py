def check_urls(urls, timeout=10, max_retries=2):
    import requests
    import logging
    import sys
    from requests.adapters import HTTPAdapter
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
    if retry is not None:
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

    failed_urls = []

    for url in urls:
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
