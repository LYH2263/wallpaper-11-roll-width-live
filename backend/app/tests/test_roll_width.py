import pytest


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "app.db"
    import app.config as config
    import app.db as db
    monkeypatch.setattr(config, "DB_PATH", db_path)
    monkeypatch.setattr(db, "DB_PATH", db_path)
    from app import seed
    seed.init_db()
    from fastapi.testclient import TestClient
    import app.main as main
    with TestClient(main.app) as c:
        yield c


def test_width_cm_same_source_as_width_m(client):
    items = client.get("/api/rolls").json()["items"]
    r1 = next(r for r in items if r["id"] == 1)
    assert r1["width"] == 0.53
    assert r1["width_cm"] == 53.0


def test_patch_width_writes_cm_as_m_and_detail_example_recomputes(client):
    before = client.get("/api/rolls/1").json()
    assert before["example"]["drops"] == 31
    assert before["example"]["rolls"] == 11

    resp = client.patch("/api/rolls/1/width", json={"width_cm": 70})
    assert resp.status_code == 200
    body = resp.json()
    assert body["width"] == pytest.approx(0.7)
    assert body["width_cm"] == 70.0

    after = client.get("/api/rolls/1").json()
    # 16m 周长 / 0.7m 幅宽 = 23 条；每卷 3 条 → 8 卷
    assert after["example"]["drops"] == 23
    assert after["example"]["rolls"] == 8


def test_non_positive_width_rejected_with_reason(client):
    for bad in (0, -3):
        resp = client.patch("/api/rolls/1/width", json={"width_cm": bad})
        assert resp.status_code == 422
        assert "正数" in resp.json()["detail"]
    assert client.get("/api/rolls/1").json()["width"] == 0.53


def test_width_over_limit_rejected_with_reason(client):
    resp = client.patch("/api/rolls/1/width", json={"width_cm": 200})
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert "上限" in detail and "150" in detail
    assert client.get("/api/rolls/1").json()["width"] == 0.53


def test_patch_unknown_roll_404(client):
    assert client.patch("/api/rolls/999/width", json={"width_cm": 60}).status_code == 404


def test_saved_history_keeps_snapshot_after_width_change(client):
    saved = client.post(
        "/api/estimate", json={"wall_id": 1, "roll_id": 1, "save": True}
    ).json()
    assert saved["drops"] == 31 and saved["rolls"] == 11

    client.patch("/api/rolls/1/width", json={"width_cm": 70})

    re_run = client.get("/api/estimate?wall_id=1&roll_id=1").json()
    assert re_run["drops"] == 23 and re_run["rolls"] == 8
    assert re_run["roll"]["width_cm"] == 70.0

    runs = client.get("/api/runs").json()["items"]
    snap = next(r for r in runs if r["wall_id"] == 1 and r["roll_id"] == 1)
    assert snap["result"]["drops"] == 31
    assert snap["result"]["rolls"] == 11
