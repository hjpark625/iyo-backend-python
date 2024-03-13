"""Detail API Router"""

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/detail/{storename}")
def get_detail(storename: str):
    """Get Map pins Data"""
    if not storename or storename.strip() == "":
        raise HTTPException(
            status_code=404, detail={"message": "storename is required"}
        )
    print(not storename)
    return {"message": f"you've been searched for {storename}"}
