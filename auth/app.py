from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from auth.auth_dto import UserDTO, UserResponseDTO
from database.database import Database
from enums.http_status import HttpStatus

router = APIRouter(prefix="/auth")
users_db = Database(db_name="iyo", table_name="users")


class UserBody(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(login_info: UserBody):
    user_dict = login_info.__dict__
    if not user_dict["email"] or not user_dict["password"]:
        raise HTTPException(
            status_code=HttpStatus.BAD_REQUEST.value,
            detail={"message": "이메일 또는 비밀번호가 없습니다."},
        )
    user_data = users_db.get_collection()

    user = user_data.find_one({"email": user_dict["email"]})
    if not user:
        raise HTTPException(
            status_code=HttpStatus.NOT_FOUND.value,
            detail={"message": "사용자 정보가 없습니다."},
        )

    user_dto = UserDTO(user)
    response_dto = UserResponseDTO(user_dto, "access_token", "refresh_token")

    return response_dto.to_json_result()


# @router.post("/register")
# def register():
#     return {"message": "register"}


@router.post("/logout")
def logout():
    return {"message": "logout"}
