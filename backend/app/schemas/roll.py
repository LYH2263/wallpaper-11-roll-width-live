from pydantic import BaseModel


class RollWidthPatch(BaseModel):
    # 幅宽，单位：厘米
    width_cm: float
