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
