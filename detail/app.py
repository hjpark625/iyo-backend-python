from fastapi import APIRouter, HTTPException
from detail.detail_dto import DetailResponseDTO, DetailDTO
from database.database import Database
from enums.http_status import HttpStatus

router = APIRouter()


@router.get("/detail/{storename}")
def get_detail(storename: str):
    if not storename or storename.strip() == "":
        raise HTTPException(
            status_code=HttpStatus.NOT_FOUND.value,
            detail={"message": "상점 이름 정보가 없습니다."},
        )
    client = Database(db_name="iyo", table_name="details")
    db = client.get_collection()

    detail_data = db.find_one({"engName": storename})

    if not detail_data:
        raise HTTPException(
            status_code=HttpStatus.NOT_FOUND.value,
            detail={"message": "상점 정보가 없습니다."},
        )

    detail_dto = DetailDTO(detail_data)
    response_dto = DetailResponseDTO(detail_dto)

    return response_dto.to_json_result()
