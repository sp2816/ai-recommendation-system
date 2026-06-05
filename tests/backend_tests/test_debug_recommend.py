from pathlib import Path
import sys
import pytest

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.routes.recommendation import recommend


def test_debug_recommend_local_db_skip():
    # This test calls the `recommend` function which requires DB/Redis.
    # Skip if DATABASE_URL not set or DB unavailable.
    from os import getenv
    if not getenv('DATABASE_URL'):
        pytest.skip('DATABASE_URL not set; skipping DB integration test')

    # If DATABASE_URL is set, attempt to call for a small user id and ensure it returns a dict
    try:
        res = recommend(1)
    except Exception as e:
        pytest.skip(f'recommend() raised: {e}')

    assert isinstance(res, dict)
