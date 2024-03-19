from datetime import datetime
from typing import Optional, Union
from dataclasses import dataclass
from bson import ObjectId


@dataclass
class User:
    _id: ObjectId
    email: str
    nickname: str
    hashedPassword: str
    createdAt: datetime
    updatedAt: Optional[datetime] = None
    lastLoginAt: Optional[datetime] = None
    refreshToken: Optional[str] = None
    isAdmin: bool = False


@dataclass
class AccessTokenPayload:
    userId: str
    email: str


@dataclass
class RefreshTokenPayload:
    userId: str
    email: str
    hashed_password: str


class UserDTO:
    def __init__(self, auth_data: User):
        self.userId = str(auth_data["_id"])
        self.email = auth_data["email"]
        self.nickname = auth_data["nickname"]
        self.createdAt = (
            auth_data["createdAt"].isoformat()
            if isinstance(auth_data["createdAt"], datetime)
            else auth_data["createdAt"]
        )
        self.updatedAt = (
            auth_data["updatedAt"].isoformat()
            if isinstance(auth_data["updatedAt"], datetime)
            else auth_data["updatedAt"]
        )
        self.lastLoginAt = (
            auth_data["lastLoginAt"].isoformat()
            if isinstance(auth_data["lastLoginAt"], datetime)
            else auth_data["lastLoginAt"]
        )
        self.isAdmin = auth_data["isAdmin"]
        pass


class UserResponseDTO:
    info: dict[str, Union[dict[str, UserDTO], str]]
    accessToken: str
    refreshToken: str

    def __init__(self, user_dto: UserDTO, access_token: str, refresh_token: str):
        self.info = user_dto.__dict__
        self.accessToken = access_token
        self.refreshToken = refresh_token
        pass

    def to_json_result(self) -> dict[str, Union[dict[str, UserDTO], str]]:
        result = self.__dict__
        return {"user": result}
