from pydantic import BaseModel


class RollWidthUpdate(BaseModel):
    width_cm: float
