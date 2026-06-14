"""Offline API tests — no Vertex calls (those are exercised manually).

Covers routing, config shape, validation, and the local-only compress tool.
"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
MC = {"model_name": "gemini-3.5-flash", "temperature": 1.0, "top_p": 0.8, "max_tokens": 4096}


def test_health():
    assert client.get("/api/health").json() == {"status": "ok"}


def test_config_lists_all_tools():
    cfg = client.get("/api/config").json()
    ids = {t["id"] for t in cfg["tools"]}
    # 12 generic + 2 special (dare, images)
    assert len(cfg["tools"]) == 14
    assert {"fine_tune", "json_prompt", "compress", "dare", "images"} <= ids
    assert cfg["default_model"] in cfg["models"]


def test_unknown_tool_404():
    r = client.post("/api/tools/nope", json={"input": "x", "modelConfig": MC})
    assert r.status_code == 404


def test_empty_input_400():
    r = client.post("/api/tools/system_prompt", json={"input": "  ", "modelConfig": MC})
    assert r.status_code == 400
    assert r.json()["code"] == "validation_error"


def test_model_config_accepts_alias_and_name():
    # alias "modelConfig"
    r1 = client.post("/api/tools/compress", json={"input": "the quick brown fox", "modelConfig": MC})
    # python field name "cfg"
    r2 = client.post("/api/tools/compress", json={"input": "the quick brown fox", "cfg": MC})
    assert r1.status_code == 200 and r2.status_code == 200


def test_compress_returns_stats():
    r = client.post(
        "/api/tools/compress",
        json={"input": "the quick brown fox jumps over the lazy dog", "modelConfig": MC},
    )
    assert r.status_code == 200
    meta = r.json()["meta"]
    assert {"original_len", "compressed_len", "reduction_pct"} <= meta.keys()
    assert meta["compressed_len"] <= meta["original_len"]
