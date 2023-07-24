import jwt
import sentry_sdk
from fastapi import Header, HTTPException

from friendlyeats.settings import SECRET_KEY


def verify_token(authorization: str = Header(default=None)) -> dict:  # noqa B00B
    """
    https://egcoder.com/posts/django-rest-framework-custom-jwt-authentication/
    https://habr.com/ru/post/538040/
    """
    if not authorization:
        detail = "Authentication credentials were not provided."

        sentry_sdk.capture_message(detail)
        raise HTTPException(status_code=401, detail=detail)

    auth_header = authorization.split()
    if len(auth_header) != 2:
        detail = "Malformed token."

        sentry_sdk.capture_message(detail)
        raise HTTPException(status_code=401, detail=detail)

    prefix, expected_prefix = auth_header[0], "Bearer"
    if prefix.lower() != expected_prefix.lower():
        detail = "Bearer not given in header."

        sentry_sdk.capture_message(detail)
        raise HTTPException(status_code=401, detail=detail)

    token = auth_header[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception as exc:
        detail = f"Unable to decode token: {str(exc)}"

        sentry_sdk.capture_message(detail)
        raise HTTPException(status_code=401, detail=detail)

    return payload


async def get_auth_user(authorization: str = Header(default=None)) -> dict:  # noqa B008
    payload = verify_token(authorization=authorization)

    if payload["role"] != "user":
        detail = f"Token has invalid role: {payload['role']}"

        sentry_sdk.capture_message(detail)
        raise HTTPException(status_code=401, detail=detail)

    return payload


async def get_auth_service(authorization: str = Header(default=None)) -> dict:  # noqa B008
    payload = verify_token(authorization=authorization)

    if payload["role"] != "service":
        detail = f"Token has invalid role: {payload['role']}"

        sentry_sdk.capture_message(detail)
        raise HTTPException(status_code=401, detail=detail)

    return payload
