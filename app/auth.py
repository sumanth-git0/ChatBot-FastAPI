from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
import httpx

from app.schemas.user import UserCreate

from .settings import KEYCLOAK_ADMIN_PASSWORD, KEYCLOAK_ADMIN_USERNAME, KEYCLOAK_API_URL, KEYCLOAK_REALM, KEYCLOAK_CLIENT_ID, KEYCLOAK_ISSUER, KEYCLOAK_JWKS_URL, KEYCLOAK_TOKEN_URL
from jose import jwt, JWTError
import httpx


security = HTTPBearer()
jwks = None


async def get_keycloak_admin_token():
    data = {
        "grant_type": "password",
        "client_id": "admin-cli",
        "username": KEYCLOAK_ADMIN_USERNAME,
        "password": KEYCLOAK_ADMIN_PASSWORD,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(KEYCLOAK_TOKEN_URL, data=data, headers=headers)
        resp.raise_for_status()
        return resp.json()["access_token"]


async def create_keycloak_user(user: UserCreate):
    token = await get_keycloak_admin_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "username": user.email,
        "email": user.email,
        "firstName": user.name,
        "enabled": True,
        "emailVerified": False,
        "credentials": [
          {
            "type": "password",
            "value": user.password,
            "temporary": False
          }
        ]
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{KEYCLOAK_API_URL}/admin/realms/{KEYCLOAK_REALM}/users",
            json=payload,
            headers=headers,
        )

    if resp.status_code not in (201, 204):
        raise Exception(f"Keycloak user creation failed: {resp.text}")

    # Location header contains user id
    return resp.headers["Location"].split("/")[-1]

async def set_keycloak_password(user_id: str, password: str):
    token = await get_keycloak_admin_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "type": "password",
        "value": password,
        "temporary": False,
    }

    async with httpx.AsyncClient() as client:
        resp = await client.put(
            f"{KEYCLOAK_API_URL}/admin/realms/{KEYCLOAK_REALM}/users/{user_id}/reset-password",
            json=payload,
            headers=headers,
        )

    resp.raise_for_status()




async def get_jwks():
    global jwks
    if jwks is None:
        async with httpx.AsyncClient() as client:
            resp = await client.get(KEYCLOAK_JWKS_URL)
            resp.raise_for_status()
            jwks = resp.json()
    return jwks


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        jwks = await get_jwks()

        payload = jwt.decode(
            token,
            jwks,
            algorithms=["RS256"],
            audience=KEYCLOAK_CLIENT_ID,
            issuer=KEYCLOAK_ISSUER,
        )

        return {
            "sub": payload.get("sub"),
            "username": payload.get("preferred_username"),
            "email": payload.get("email"),
            "roles": payload.get("realm_access", {}).get("roles", []),
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
