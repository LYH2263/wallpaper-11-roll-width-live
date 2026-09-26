"""卷材服务：幅宽写入校验、米/厘米同源序列化、卷材示例测算。

幅宽在库内以米存储（width），对外统一附加 width_cm；列表、详情、
测算台、卷材详情示例均由此处同源产出，禁止各处自行换算。
"""

from fastapi import HTTPException

from app.config import MAX_ROLL_WIDTH_CM
from app.engines.wallpaper_math import roll_count
from app.repositories import rolls as repo
from app.repositories import settings_repo, walls


def get_max_width_cm() -> float:
    raw = settings_repo.get_setting("max_width_cm")
    try:
        return float(raw) if raw is not None else MAX_ROLL_WIDTH_CM
    except (TypeError, ValueError):
        return MAX_ROLL_WIDTH_CM


def serialize_roll(row: dict) -> dict:
    data = dict(row)
    width_m = data.get("width")
    data["width_cm"] = round(float(width_m) * 100, 1) if width_m is not None else None
    return data


def list_rolls() -> list:
    return [serialize_roll(r) for r in repo.list_rolls()]


def get_roll(rid: int):
    row = repo.get_roll(rid)
    return serialize_roll(row) if row else None


def update_width(rid: int, width_cm: float) -> dict:
    """把幅宽（厘米）校验后换算成米写入；失败以 422 回显原因。"""
    if width_cm <= 0:
        raise HTTPException(422, f"幅宽必须为正数，收到 {width_cm} cm")
    max_cm = get_max_width_cm()
    if width_cm > max_cm:
        raise HTTPException(422, f"幅宽不得超过配置上限 {max_cm:g} cm，收到 {width_cm:g} cm")

    if repo.get_roll(rid) is None:
        raise HTTPException(404, "roll not found")

    width_m = width_cm / 100.0
    repo.update_width(rid, width_m)
    row = repo.get_roll(rid)
    return serialize_roll(row)


def example_estimate(roll: dict) -> dict | None:
    """该卷在一面示例墙（默认取第一面有效墙）上的同源 drops/rolls。"""
    wall = next((w for w in walls.list_walls() if w.get("data_quality") != "dirty"), None)
    if not wall:
        return None
    calc = roll_count(
        wall["perimeter"], wall["height"], roll["width"], roll["length"], roll["pattern_cm"]
    )
    return {"wall": {"id": wall["id"], "name": wall["name"]}, **calc}
