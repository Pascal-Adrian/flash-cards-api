from fastapi import HTTPException, APIRouter, Request, Response, Body
from fastapi.security import HTTPBearer
from datetime import datetime, timedelta
from functools import lru_cache
import jwt
import config


@lru_cache()
def get_settings():
    return config.Settings()


setting = get_settings()

security = HTTPBearer()


def create_jwt(role: str) -> str:
    expire = datetime.now() + timedelta(seconds=setting.jwt_expiration)
    payload = {
        "exp": expire,
        "role": role,
        "iss": setting.jwt_issuer,
    }
    return jwt.encode(payload, setting.jwt_secret, algorithm=setting.jwt_algorithm)


def decode_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token, setting.jwt_secret, algorithms=[setting.jwt_algorithm], issuer=setting.jwt_issuer)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidIssuerError:
        raise HTTPException(status_code=401, detail="Invalid token issuer")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def require_role_from_cookie(role: str):
    def dependency(request: Request):
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="No token in cookie")
        payload = decode_jwt(token)
        if payload.get("role") != role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return payload
    return dependency


TokenRouter = APIRouter(
    prefix="/token",
    tags=["token"]
)


@TokenRouter.post("", response_model=dict)
async def get_token(response: Response, secret: str = Body(default=None)):
    if secret == setting.admin_key:
        token = create_jwt("admin")
    elif secret is None:
        token = create_jwt("user")
    else:
        raise HTTPException(status_code=403, detail="Invalid secret for admin")

        # Set token as cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,  # Set to True in production (requires HTTPS)
        samesite="Strict",  # Options: Lax / Strict / None
        max_age=setting.jwt_expiration,  # 60 seconds = 1 minute
        path="/"
    )

    return {"message": "Token set in cookie"}


