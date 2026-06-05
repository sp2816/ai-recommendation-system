from pathlib import Path
import sys
import pytest

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pickle
from ml.src.ann_search import get_recommendations


@pytest.mark.skipif(not (ROOT / 'ml' / 'models' / 'redis_users.pkl').exists(), reason="no redis_users.pkl")
def test_analyze_recs_runs():
    p = ROOT / 'ml' / 'models' / 'redis_users.pkl'
    with open(p, 'rb') as f:
        users = pickle.load(f)

    # pick any user profile
    if not users:
        pytest.skip("redis_users.pkl empty")

    user_profile = next(iter(users.values()))

    recs = get_recommendations(user_profile, top_k=50)
    assert isinstance(recs, list)
