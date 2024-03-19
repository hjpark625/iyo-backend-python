from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from datetime import datetime
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from typing import Union
from auth.auth_dto import UserDTO, UserResponseDTO
from database.database import Database
from enums.http_status import HttpStatus
from auth.utils import (
    check_password,
    generate_access_token,
    generate_refresh_token,
    revalidate_access_token,
)

router = APIRouter(prefix="/auth")
users_db = Database(db_name="iyo", table_name="users")


class UserBody(BaseModel):
    email: str
    password: str


# TODO: 내부의 패스워드 체크, 토큰 발급 로직을 서비스 레이어로 분리해야함
@router.post("/login")
def login(login_info: UserBody):
    # body의 유저 정보를 객체로 변환
    user_dict = login_info.__dict__
    # 유저 정보가 없을 경우 에러 발생시킨다.
    if not user_dict["email"] or not user_dict["password"]:
        raise HTTPException(
            status_code=HttpStatus.BAD_REQUEST.value,
            detail={
                "status_code": HttpStatus.BAD_REQUEST.value,
                "message": "이메일 또는 비밀번호를 입력해주세요",
            },
        )
    # 유저의 전체 정보를 데이터베이스에서 가져온다.
    user_data = users_db.get_collection()

    # body의 이메일을 토대로 유저 정보를 가져온다.
    user = user_data.find_one(filter={"email": user_dict["email"]})

    # 유저 정보가 없을때 에러를 발생시킨다.
    if not user:
        raise HTTPException(
            status_code=HttpStatus.NOT_FOUND.value,
            detail={
                "status_code": HttpStatus.NOT_FOUND.value,
                "message": "사용자 정보가 없습니다.",
            },
        )

    # 패스워드가 일치하지 않을때 에러를 발생시킨다.
    if not check_password(user_dict["password"], user["hashedPassword"]):
        raise HTTPException(
            status_code=HttpStatus.UNAUTHORIZED.value,
            detail={
                "status_code": HttpStatus.UNAUTHORIZED.value,
                "message": "비밀번호가 일치하지 않습니다.",
            },
        )

    user_dto = UserDTO(user)

    # 토큰들을 생성한다.
    access_token = generate_access_token(user_dto=user_dto)
    refresh_token = generate_refresh_token(user_dto=user_dto)

    # 생성된 refresh_token은 데이터베이스에 저장하면서 로그인한 시간을 토대로 마지막로그인 데이터 필드를 업데이트한다.
    user_data.find_one_and_update(
        filter={"email": user_dict["email"]},
        update={"$set": {"refreshToken": refresh_token, "lastLoginAt": datetime.now()}},
    )

    response_dto = UserResponseDTO(
        user_dto=user_dto,
        access_token=access_token,
        refresh_token=refresh_token,
    )

    return response_dto.to_json_result()


# @router.post("/register")
# def register():
#     return {"message": "register"}


@router.post("/logout")
def logout():
    return {"message": "logout"}


@router.post("/revalidate")
def revalidate_token(authorization: Union[str, None] = Header(default=None)):
    print(authorization)
    if not authorization:
        raise HTTPException(
            status_code=HttpStatus.BAD_REQUEST.value,
            detail={
                "status_code": HttpStatus.BAD_REQUEST.value,
                "message": "토큰이 없습니다.",
            },
        )

    token_type = authorization.split(" ")[0]
    if token_type != "Bearer":
        raise HTTPException(
            status_code=HttpStatus.FORBIDDEN.value,
            detail={
                "status_code": HttpStatus.FORBIDDEN.value,
                "message": "Bearer 토큰형태가 아닙니다.",
            },
        )

    refresh_token = authorization.split(" ")[1]

    try:
        new_access_token = revalidate_access_token(refresh_token=refresh_token)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=HttpStatus.UNAUTHORIZED.value,
            detail={
                "status_code": HttpStatus.UNAUTHORIZED.value,
                "message": "토큰이 만료되었습니다.",
            },
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=HttpStatus.UNAUTHORIZED.value,
            detail={
                "status_code": HttpStatus.UNAUTHORIZED.value,
                "message": "토큰이 유효하지 않습니다.",
            },
        )

    return {"accessToken": new_access_token}
