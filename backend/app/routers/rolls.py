from fastapi import APIRouter, HTTPException
from app.schemas.roll import RollWidthPatch
from app.services import roll_service

router = APIRouter()


@router.get("/rolls")
def list_rolls():
    return {"items": roll_service.list_rolls()}


@router.get("/rolls/{roll_id}")
def get_roll(roll_id: int):
    roll = roll_service.get_roll(roll_id)
    if not roll:
        raise HTTPException(404)
    return {**roll, "example": roll_service.example_estimate(roll)}


@router.patch("/rolls/{roll_id}/width")
def patch_roll_width(roll_id: int, body: RollWidthPatch):
    return roll_service.update_width(roll_id, body.width_cm)
