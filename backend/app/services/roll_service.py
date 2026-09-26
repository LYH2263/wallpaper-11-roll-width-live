"""Roll profile service: width writes validated here, examples computed from the same engine as estimates."""

import math

from fastapi import HTTPException

from app.config import MAX_ROLL_WIDTH_CM
from app.engines.wallpaper_math import roll_count
from app.repositories import rolls as repo

# 卷材详情页示例 drops/rolls 使用的示例墙面（米），与测算台共用 roll_count 引擎
EXAMPLE_PERIMETER_M = 10.0
EXAMPLE_HEIGHT_M = 2.7


def _example(roll: dict) -> dict:
    calc = roll_count(
        EXAMPLE_PERIMETER_M,
        EXAMPLE_HEIGHT_M,
        roll["width"],
        roll["length"],
        roll["pattern_cm"],
    )
    return {"perimeter_m": EXAMPLE_PERIMETER_M, "height_m": EXAMPLE_HEIGHT_M, **calc}


def _serialize(roll: dict) -> dict:
    return {**roll, "width_cm": round(roll["width"] * 100.0, 6), "example": _example(roll)}


def public_roll(roll: dict) -> dict:
    """列表/测算台等场景共用的卷材字段，width_cm 唯一换算出口。"""
    return {**roll, "width_cm": round(roll["width"] * 100.0, 6)}


def get_roll_detail(roll_id: int) -> dict:
    roll = repo.get_roll(roll_id)
    if not roll:
        raise HTTPException(404, "roll not found")
    return _serialize(roll)


def list_rolls() -> list[dict]:
    return [public_roll(r) for r in repo.list_rolls()]


def update_width(roll_id: int, width_cm: float) -> dict:
    roll = repo.get_roll(roll_id)
    if not roll:
        raise HTTPException(404, "roll not found")
    if not math.isfinite(width_cm) or width_cm <= 0:
        raise HTTPException(422, f"幅宽须为正数（厘米），收到 {width_cm}")
    if width_cm > MAX_ROLL_WIDTH_CM:
        raise HTTPException(422, f"幅宽不得超过配置上限 {MAX_ROLL_WIDTH_CM:g}cm，收到 {width_cm:g}cm")
    repo.update_width(roll_id, width_cm / 100.0)
    return get_roll_detail(roll_id)
