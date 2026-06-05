from pathlib import Path
import sys

# Ensure repo root is importable when tests are executed from other locations
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ml.src.ann_search import get_recommendations
from ml.src.product_lookup import get_product_details


def test_ann_search_returns_ids():
    user_profile = {
        "customer_id": "100001",
        "favorite_product_type": "Top",
        "season": "Spring",
        "age": 30.0,
        "purchase_frequency": 1.0,
        "avg_spend": 25.0,
        "repeat_purchase_ratio": 0.1
    }

    recs = get_recommendations(user_profile, top_k=5)

    assert isinstance(recs, list)
    assert len(recs) <= 5
    if recs:
        # product lookup should return matching details for at least the first result
        details = get_product_details(recs[:2])
        assert isinstance(details, list)
