from fastapi import APIRouter

router = APIRouter()


@router.get("/pins")
def get_pins():
    return {"message": "pins testing"}
