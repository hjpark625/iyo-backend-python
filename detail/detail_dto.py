from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field
from bson import ObjectId


@dataclass
class NearestRoute:
    subwayLine: list[str] = None
    routeInfo: str = None


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
    socialLink: Optional[str] = None
    category: Optional[str] = None
    address: str
    detailAddress: Optional[str] = None
    nearestRoute: Optional[NearestRoute] = None
    operationTime: OperationTime = field(default_factory=OperationTime)
    phoneNumber: Optional[str] = None
    coord: Coord
    description: Optional[str] = None
    introduce: Optional[str] = None
    concept: list[str]
    updatedAt: datetime
    storeImages: StoreImages = field(default_factory=StoreImages)
