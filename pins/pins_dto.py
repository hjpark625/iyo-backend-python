from detail.detail_dto import DetailSchema
from dataclasses import dataclass
from bson import ObjectId


@dataclass
class PinData:
    _id: ObjectId
    lat: float
    lng: float
    name: str
    engName: str


class PinDTO:
    def __init__(self, detail_data: DetailSchema):
        self._id = str(detail_data["_id"])
        self.lat = detail_data["coord"]["lat"]
        self.lng = detail_data["coord"]["lng"]
        self.name = detail_data["name"]
        self.engName = detail_data["engName"]


class PinsResponseDTO:
    def __init__(self, pins_dto: list[PinDTO]):
        self.pins = pins_dto

    def to_list_dict(self):
        return [
            {
                "storeId": pin._id,
                "lat": pin.lat,
                "lng": pin.lng,
                "name": pin.name,
                "engName": pin.engName,
            }
            for pin in self.pins
        ]

    def to_json_result(self):
        result = self.to_list_dict()
        return {"pins": result}
