from utils import load_urls_from_html
from check_urls import check_urls


def main():
    html_path = "index.html"
    urls = load_urls_from_html(html_path)
    check_urls(urls)


if __name__ == "__main__":
    main()
