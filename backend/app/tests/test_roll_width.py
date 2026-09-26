from fastapi.testclient import TestClient

from app.engines.wallpaper_math import roll_count


def test_width_list_and_detail_share_source(client: TestClient):
    listing = client.get("/api/rolls").json()["items"]
    first = next(r for r in listing if r["data_quality"] == "clean")
    detail = client.get(f"/api/rolls/{first['id']}").json()
    # 列表、详情同源：width_cm 均由库内米值换算
    assert detail["width_cm"] == first["width_cm"] == round(first["width"] * 100, 6)
    # 详情示例与引擎对同一组参数结果一致
    expected = roll_count(
        detail["example"]["perimeter_m"],
        detail["example"]["height_m"],
        detail["width"],
        detail["length"],
        detail["pattern_cm"],
    )
    assert detail["example"]["drops"] == expected["drops"]
    assert detail["example"]["rolls"] == expected["rolls"]


def test_width_write_recalculates_example(client: TestClient):
    rid = 1  # 素色53: 0.53m x 10m
    before = client.get(f"/api/rolls/{rid}").json()
    assert before["width_cm"] == 53.0

    r = client.patch(f"/api/rolls/{rid}/width", json={"width_cm": 70})
    assert r.status_code == 200
    after = r.json()
    assert after["width_cm"] == 70.0
    assert after["width"] == 0.70
    # 示例随新幅宽变化：幅宽变大，幅数与卷数不增
    assert after["example"]["drops"] < before["example"]["drops"]
    assert after["example"]["rolls"] <= before["example"]["rolls"]
    expected = roll_count(
        after["example"]["perimeter_m"],
        after["example"]["height_m"],
        0.70,
        after["length"],
        after["pattern_cm"],
    )
    assert after["example"]["drops"] == expected["drops"]
    assert after["example"]["rolls"] == expected["rolls"]

    # 测算台再测同一面墙，结果与新幅宽同源
    est = client.get("/api/estimate", params={"wall_id": 1, "roll_id": rid}).json()
    assert est["roll"]["width_cm"] == 70.0
    assert est["drops"] == roll_count(16.0, 2.7, 0.70, 10.0, 0)["drops"]


def test_reject_non_positive_and_over_limit(client: TestClient):
    for bad in (0, -53):
        r = client.patch("/api/rolls/1/width", json={"width_cm": bad})
        assert r.status_code == 422
        assert "正数" in r.json()["detail"]
    r = client.patch("/api/rolls/1/width", json={"width_cm": 200.01})
    assert r.status_code == 422
    assert "上限" in r.json()["detail"]
    # 拒绝后库内值不变
    assert client.get("/api/rolls/1").json()["width_cm"] == 53.0


def test_saved_history_keeps_snapshot_after_width_change(client: TestClient):
    saved = client.post(
        "/api/estimate", json={"wall_id": 1, "roll_id": 1, "save": True}
    ).json()
    old_drops, old_rolls = saved["drops"], saved["rolls"]

    assert client.patch("/api/rolls/1/width", json={"width_cm": 106}).status_code == 200

    runs = client.get("/api/runs").json()["items"]
    snapshot = runs[0]["result"]
    assert snapshot["drops"] == old_drops
    assert snapshot["rolls"] == old_rolls

    # 新一次测算按新幅宽，与历史快照不同
    fresh = client.get("/api/estimate", params={"wall_id": 1, "roll_id": 1}).json()
    assert fresh["drops"] != old_drops
