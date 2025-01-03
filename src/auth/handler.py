import time
import jwt
import re

JWT_SECRET = "clairo"
JWT_ALGORITHM = "HS256"


def sign_jwt(user_id: str):
    payload = {"user_id": user_id, "expires": time.time() + 1800}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return {"access_token": token}


def decode_jwt(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception:
        return {}


def is_polite(user_agent: str):
    regex = r"^pl(e*)z$"
    return bool(re.match(regex, user_agent))
