from pathlib import Path
import sys


def test_load_urls_from_html(tmp_path):
    html = '<html><body><a href="http://example.com/page">Example</a><a href="/internal">Internal</a></body></html>'
    index = tmp_path / 'index.html'
    index.write_text(html, encoding='utf-8')

    # Add test/src to sys.path so we can import the utility directly
    repo_root = Path(__file__).resolve().parents[2]
    src = repo_root / 'test' / 'src'
    sys.path.insert(0, str(src))

    from utils import load_urls_from_html

    urls = load_urls_from_html(str(index))
    assert urls == ['http://example.com/page']
