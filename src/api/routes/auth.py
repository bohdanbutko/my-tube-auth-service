from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.api.schemas import ProvisionIdentityRequest
from src.application.commands import (
    LoginCommand,
    ProvisionIdentityCommand,
    VerifyTokenCommand,
    login_handler,
    provision_identity_handler,
    verify_token_handler,
)
from src.domain.exceptions import InvalidCredentialsException
from src.domain.value_objects import Token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


@router.post("/identities")
def provision_identity(request: ProvisionIdentityRequest):
    command = ProvisionIdentityCommand.model_validate(request.model_dump())
    result = provision_identity_handler(command)
    return JSONResponse(status_code=201 if result["success"] else 400, content=result)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        command = LoginCommand(email=form_data.username, password=form_data.password)
        result = login_handler(command)
        return JSONResponse(status_code=200, content=result)
    except InvalidCredentialsException:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.get("/verify-token")
def verify_token(token: str = Depends(oauth2_scheme)) -> JSONResponse:
    try:
        command = VerifyTokenCommand(token=token)
        result = verify_token_handler(command)
        return JSONResponse(status_code=200, content=result)
    except InvalidCredentialsException:
        raise HTTPException(status_code=401, detail="Invalid token")
