from utils import load_urls_from_html
from link_checker import check_urls


def main():
    html_path = "index.html"
    urls = load_urls_from_html(html_path)
    # Use a 10s timeout and 2 retries for transient failures
    check_urls(urls, timeout=10, max_retries=2)


if __name__ == "__main__":
    main()
