import os
from bcrypt import checkpw
from jwt import encode
from dotenv import load_dotenv
from datetime import datetime, timedelta
from auth.auth_dto import AccessTokenPayload


load_dotenv()


def check_password(password: str, hashed: str) -> bool:
    encoded_password = password.encode("utf-8")
    encoded_hashed = hashed.encode("utf-8")
    is_same = checkpw(password=encoded_password, hashed_password=encoded_hashed)

    return is_same


def generate_access_token(access_token_payload: AccessTokenPayload):
    origin_info = access_token_payload.__dict__

    exp_time = datetime.now() + timedelta(minutes=30)

    access_token_payload = {
        "userId": origin_info["userId"],
        "email": origin_info["email"],
        "exp": exp_time,
    }

    access_token = encode(
        payload=access_token_payload, key=os.getenv("JWT_SECRET"), algorithm="HS256"
    )

    print(access_token)

    return access_token
