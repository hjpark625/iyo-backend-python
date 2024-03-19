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
