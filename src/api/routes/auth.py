from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.api.schemas import RegisterUserRequest
from src.application.commands import RegisterUserCommand, register_user_handler
from src.application.commands import LoginCommand, login_handler
from src.application.commands import VerifyTokenCommand, verify_token_handler
from src.domain.value_objects import Token
from src.domain.exceptions import InvalidCredentialsException

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/register")
def register(request: RegisterUserRequest):
    command = RegisterUserCommand(email=request.email, password=request.password)
    result = register_user_handler(command)
    return JSONResponse(status_code=201 if result["success"] else 400, content=result)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        command = LoginCommand(email=form_data.username, password=form_data.password)
        result = login_handler(command)
        return JSONResponse(status_code=200, content=result)
    except InvalidCredentialsException:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.get("/login/google")
def login_with_google():
    google_auth_url = "https://accounts.google.com/o/oauth2/auth"
    client_id = "fake"  # TODO: Replace with actual client ID
    redirect_uri = "http://localhost:8000/api/v1/google/callback"
    scope = "email"
    response_type = "code"
    return RedirectResponse(
        url=f"{google_auth_url}?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&response_type={response_type}"
    )


@router.get("/google/callback")
def google_callback(code: str) -> JSONResponse:
    if not code:
        raise HTTPException(status_code=400, detail="Invalid code")
    return JSONResponse(
        status_code=200,
        content={"message": "Google login successful", "code": code},
    )


@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)) -> JSONResponse:
    # In a real application, you would invalidate the token here
    # For now, we'll just return a success message
    return JSONResponse(
        status_code=200, content={"message": "User logged out successfully"}
    )


@router.post("/refresh-token")
def refresh_token(token: str = Depends(oauth2_scheme)) -> JSONResponse:
    # In a real application, you would validate the refresh token and issue a new access token
    # For now, we'll just return a dummy token
    return JSONResponse(
        status_code=200,
        content={"access_token": "new_token_would_be_generated", "token_type": "bearer"},
    )


@router.get("/verify-token")
def verify_token(token: str = Depends(oauth2_scheme)) -> JSONResponse:
    try:
        command = VerifyTokenCommand(token=token)
        result = verify_token_handler(command)
        return JSONResponse(status_code=200, content=result)
    except InvalidCredentialsException:
        raise HTTPException(status_code=401, detail="Invalid token")
