def check_urls(urls):
    import requests
    import logging

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                logging.info(f"URL is accessible: {url}")
            else:
                logging.warning(f"URL returned status code {response.status_code}: {url}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error accessing {url}: {e}")