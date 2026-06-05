from pathlib import Path
import sys
import pytest
import pickle

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.mark.skipif(not (ROOT / 'ml' / 'models' / 'item_store.pkl').exists(), reason="no item_store.pkl")
def test_inspect_item_store_loads():
    p = ROOT / 'ml' / 'models' / 'item_store.pkl'
    with open(p, 'rb') as f:
        data = pickle.load(f)

    assert data is not None
