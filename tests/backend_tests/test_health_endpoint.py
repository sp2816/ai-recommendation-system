from pathlib import Path
import sys

# Ensure repo root is importable when tests are executed from other locations
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient

from backend.main import app


def test_root_health():
    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert data.get("message") in ("API is working!", "OK")
