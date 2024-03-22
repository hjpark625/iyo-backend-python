import os
from bcrypt import checkpw
from jwt import encode, decode
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from dotenv import load_dotenv
from datetime import datetime, timedelta
from bson import ObjectId
from database.database import Database
from auth.auth_dto import AccessTokenPayload, RefreshTokenPayload, UserDTO


load_dotenv()
users_db = Database(db_name="iyo", table_name="users")


def check_password(password: str, hashed: str) -> bool:
    encoded_password = password.encode("utf-8")
    encoded_hashed = hashed.encode("utf-8")
    is_same = checkpw(password=encoded_password, hashed_password=encoded_hashed)

    return is_same


def generate_access_token(user_dto: AccessTokenPayload) -> str:
    origin_info = user_dto.__dict__

    exp_time = datetime.now() + timedelta(minutes=30)

    access_token_payload = {
        "userId": origin_info["userId"],
        "email": origin_info["email"],
        "exp": exp_time,
    }

    access_token = encode(
        payload=access_token_payload, key=os.getenv("JWT_SECRET"), algorithm="HS256"
    )

    return access_token


def generate_refresh_token(user_dto: RefreshTokenPayload) -> str:
    origin_info = user_dto.__dict__

    exp_time = datetime.now() + timedelta(days=7)

    refresh_token_payload = {
        "userId": origin_info["userId"],
        "email": origin_info["email"],
        "isAdmin": origin_info["isAdmin"],
        "exp": exp_time,
    }

    refresh_token = encode(
        payload=refresh_token_payload, key=os.getenv("JWT_SECRET"), algorithm="HS256"
    )

    return refresh_token


def check_refresh_token(refresh_token: str):
    try:
        decoded_refresh_token = decode(
            refresh_token, key=os.getenv("JWT_SECRET"), algorithms=["HS256"]
        )
    except ExpiredSignatureError:
        raise ExpiredSignatureError("토큰이 만료되었습니다.")
    except InvalidTokenError:
        raise InvalidTokenError("토큰이 유효하지 않습니다.")

    return decoded_refresh_token


def revalidate_access_token(refresh_token: str) -> str:
    decoded_refresh_token = check_refresh_token(refresh_token=refresh_token)

    user_data = users_db.get_collection()
    user = user_data.find_one(filter={"_id": ObjectId(decoded_refresh_token["userId"])})

    if not user:
        raise Exception("사용자 정보가 없습니다.")

    user_dto = UserDTO(user)

    refresh_token_in_db = user["refreshToken"]

    if refresh_token != refresh_token_in_db:
        raise ("토큰 정보가 일치하지 않습니다.")

    access_token = generate_access_token(user_dto)

    return access_token
