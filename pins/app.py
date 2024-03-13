"""Pins API Router"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/pins")
def get_pins():
    """Get Map Pins Data"""
    return {"message": "pins testing"}
