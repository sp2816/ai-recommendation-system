from pathlib import Path
import sys

# Ensure repo root is importable when tests are executed from other locations
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ml.src.ann_search import get_recommendations
from ml.src.product_lookup import get_product_details


def test_smoke_integration_pipeline():
    user_profile = {
        "customer_id": "100001",
        "favorite_product_type": "Top",
        "season": "Spring",
        "age": 30.0,
        "purchase_frequency": 1.0,
        "avg_spend": 25.0,
        "repeat_purchase_ratio": 0.1
    }

    # Should run without raising and return a list of ids
    rec_ids = get_recommendations(user_profile, top_k=10)
    assert isinstance(rec_ids, list)
    assert len(rec_ids) <= 10

    # Fetch details for a couple of items (if present)
    if rec_ids:
        details = get_product_details(rec_ids[:3])
        assert isinstance(details, list)
