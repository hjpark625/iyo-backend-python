from fastapi import APIRouter
from database.database import Database
from pins.pins_dto import PinsResponseDTO, PinDTO


router = APIRouter()


@router.get("/pins")
def get_pins():
    client = Database(db_name="iyo", table_name="details")
    db = client.get_collection()
    whole_detail_data = db.find()
    pins_data = []

    for detail_data in whole_detail_data:
        pin_dto = PinDTO(detail_data=detail_data)
        pins_data.append(pin_dto)

    response_dto = PinsResponseDTO(pins_data)

    return response_dto.to_json_result()
