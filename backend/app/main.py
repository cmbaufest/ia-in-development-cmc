from fastapi import FastAPI, HTTPException, status
from jose import JWTError

from app.auth import (
    ACCESS_TOKEN_EXPIRE_SECONDS,
    authenticate_user,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.models import LoginRequest, RefreshRequest, TokenResponse

app = FastAPI(
    title="JWT Authentication API",
    description="FastAPI backend with JWT authentication using passlib[bcrypt].",
    version="0.1.0",
)


@app.post("/token", response_model=TokenResponse, summary="Login and obtain JWT tokens")
def login(request: LoginRequest):
    """
    Authenticate with username and password.

    - **username**: admin
    - **password**: admin123

    Returns an access token (valid for 300 seconds) and a refresh token.
    """
    user = authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user["username"]})
    refresh_token = create_refresh_token(data={"sub": user["username"]})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
    )


@app.post(
    "/token/refresh",
    response_model=TokenResponse,
    summary="Refresh access token using a refresh token",
)
def refresh_token(request: RefreshRequest):
    """
    Exchange a valid refresh token for a new access token and refresh token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(request.refresh_token)
        if payload.get("type") != "refresh":
            raise credentials_exception
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    access_token = create_access_token(data={"sub": username})
    new_refresh_token = create_refresh_token(data={"sub": username})

    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
    )
