from fastapi import APIRouter

from app.schemas.roll import RollWidthUpdate
from app.services import roll_service

router = APIRouter()


@router.get("/rolls")
def list_rolls():
    return {"items": roll_service.list_rolls()}


@router.get("/rolls/{roll_id}")
def get_roll(roll_id: int):
    return roll_service.get_roll_detail(roll_id)


@router.patch("/rolls/{roll_id}/width")
def update_roll_width(roll_id: int, body: RollWidthUpdate):
    return roll_service.update_width(roll_id, body.width_cm)
