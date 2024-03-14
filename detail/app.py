from fastapi import APIRouter, HTTPException
from detail.detail_dto import DetailResponseDTO, DetailDTO
from database.database import Database

router = APIRouter()


@router.get("/detail/{storename}")
def get_detail(storename: str):
    if not storename or storename.strip() == "":
        raise HTTPException(
            status_code=404, detail={"message": "storename is required"}
        )
    client = Database(db_name="iyo", table_name="details")
    db = client.get_collection()

    detail_data = db.find_one({"engName": storename})

    detail_dto = DetailDTO(detail_data)
    response_dto = DetailResponseDTO(detail_dto)

    return response_dto.to_json_result()
