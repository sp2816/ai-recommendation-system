from pathlib import Path
import sys
import pytest
import requests

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_get_live_recs_skip_if_unavailable():
    url = 'http://127.0.0.1:8000/recommend/1'
    try:
        r = requests.get(url, timeout=3)
    except Exception as e:
        pytest.skip(f'Could not reach local API: {e}')

    assert r.status_code == 200
    data = r.json()
    assert 'recommendations' in data
