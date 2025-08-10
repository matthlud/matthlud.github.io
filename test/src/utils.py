def load_urls_from_html(file_path):
    """Extracts external URLs from the provided HTML file."""
    from bs4 import BeautifulSoup

    urls = []
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        for a_tag in soup.find_all('a', href=True):
            url = a_tag['href']
            if url.startswith('http'):
                urls.append(url)
    return urls