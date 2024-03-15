from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field
from bson import ObjectId


@dataclass
class NearestRoute:
    subwayLine: Optional[list[str]] = field(default_factory=list)
    routeInfo: Optional[str] = None


@dataclass
class OperationTime:
    day: str
    startTime: Optional[str] = None
    endTime: Optional[str] = None


@dataclass
class Coord:
    lat: float
    lng: float


@dataclass
class StoreImages:
    file_path: str
    photoId: ObjectId
    width: int
    height: int


@dataclass
class DetailSchema:
    _id: ObjectId
    name: str
    engName: str
    address: str
    coord: Coord
    updatedAt: datetime
    socialLink: Optional[str] = None
    category: Optional[str] = None
    detailAddress: Optional[str] = None
    nearestRoute: Optional[NearestRoute] = None
    operationTime: list[OperationTime] = field(default_factory=list)
    phoneNumber: Optional[str] = None
    description: Optional[str] = None
    introduce: Optional[str] = None
    concept: list[str] = field(default_factory=list)
    storeImages: list[StoreImages] = field(default_factory=list)


class DetailDTO:
    def __init__(self, detail_data: DetailSchema):
        self._id = str(detail_data["_id"])
        self.name = detail_data["name"]
        self.engName = detail_data["engName"]
        self.social_link = detail_data["socialLink"]
        self.category = detail_data["category"]
        self.address = detail_data["address"]
        self.detail_address = detail_data["detailAddress"]
        self.nearest_route = detail_data["nearestRoute"]
        self.operation_time = detail_data["operationTime"]
        self.introduce = detail_data["introduce"]
        self.phone_number = detail_data["phoneNumber"]
        self.coord = detail_data["coord"]
        self.description = detail_data["description"]
        self.concept = detail_data["concept"]
        self.updated_at = detail_data["updatedAt"].isoformat()
        self.store_images = [
            {
                "file_path": store_image["file_path"],
                "photoId": str(store_image["photoId"]),
                "width": store_image["width"],
                "height": store_image["height"],
            }
            for store_image in detail_data["storeImages"]
        ]


class DetailResponseDTO:
    def __init__(self, detail_dto: DetailDTO):
        self.data = detail_dto

    def to_dict(self):
        return {
            "storeId": self.data._id,
            "name": self.data.name,
            "engName": self.data.engName,
            "socialLink": self.data.social_link,
            "category": self.data.category,
            "address": self.data.address,
            "detailAddress": self.data.detail_address,
            "nearestRoute": self.data.nearest_route,
            "operationTime": self.data.operation_time,
            "introduce": self.data.introduce,
            "phoneNumber": self.data.phone_number,
            "coord": self.data.coord,
            "description": self.data.description,
            "concept": self.data.concept,
            "updatedAt": self.data.updated_at,
            "storeImages": self.data.store_images,
        }

    def to_json_result(self):
        result = self.to_dict()
        return {"data": result}
