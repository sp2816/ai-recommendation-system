from pathlib import Path
import sys
import pytest
import pickle

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.mark.skipif(not (ROOT / 'ml' / 'models' / 'redis_users.pkl').exists(), reason="no redis_users.pkl")
def test_inspect_redis_users_loads():
    p = ROOT / 'ml' / 'models' / 'redis_users.pkl'
    with open(p, 'rb') as f:
        data = pickle.load(f)

    assert isinstance(data, dict)
