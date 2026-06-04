from pathlib import Path
import sys
import json


def test_load_skip_domains_and_is_skipped(tmp_path):
    repo_root = Path(__file__).resolve().parents[2]
    src = repo_root / 'test' / 'src'
    sys.path.insert(0, str(src))

    import link_checker as lc

    base = tmp_path / 'data'
    base.mkdir()
    (base / 'skip_domains.txt').write_text(json.dumps(["example.com", "another.org"]), encoding='utf-8')

    skip = lc.load_skip_domains(base_dir=base)
    assert 'example.com' in skip
    assert lc.is_skipped('https://sub.example.com', skip)
    assert not lc.is_skipped('https://not-listed.com', skip)
