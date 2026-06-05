from pathlib import Path
import sys
import pytest
import pickle

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.mark.skipif(not (ROOT / 'ml' / 'models' / 'item_embeddings.pkl').exists(), reason="no item_embeddings.pkl")
def test_inspect_item_embeddings_loads():
    p = ROOT / 'ml' / 'models' / 'item_embeddings.pkl'
    with open(p, 'rb') as f:
        df = pickle.load(f)

    assert hasattr(df, 'columns')
