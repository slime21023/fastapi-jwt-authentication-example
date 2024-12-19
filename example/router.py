from fastapi import APIRouter, Request, Depends, HTTPException, Security, Form, Query
from fastapi.security import OAuth2PasswordRequestForm
import example.schema as schema
from example.security import (
    access_security,
    verify_password,
    hash_password,
    create_verify_token,
    decode_verify_token,
)
from example.database import async_session_maker, Account
from example.exceptions import NotImplementedException
from fastapi_jwt import JwtAuthorizationCredentials
import sqlalchemy
import structlog

auth = APIRouter()
logger = structlog.get_logger()


@auth.post("/jwt/login", name="auth:login", response_model=schema.AccessTokenSuccess)
async def jwt_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    username = form_data.username
    password = form_data.password

    async with async_session_maker() as session:
        result = await session.execute(
            sqlalchemy.select(Account).where(Account.name == username).first()
        )

        hashed_password = result["hashed_password"]
        if not verify_password(password, hashed_password):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        subject = {
            "username": result["name"],
            "role": result["role"],
            "email": result["email"],
        }
        access_token = access_security.create_access_token(subject=subject)
        refresh_token = access_security.create_refresh_token(subject=subject)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }


@auth.post(
    "/jwt/refresh", name="auth:refresh", response_model=schema.RefreshTokenSuccess
)
async def jwt_refresh(
    credentials: JwtAuthorizationCredentials = Security(access_security),
):
    access_token = access_security.create_access_token(subject=credentials.subject)
    return {"access_token": access_token, "token_type": "bearer"}


@auth.post("/register", name="auth:register", response_model=schema.RegisterSuccess)
async def register(
    name: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
):
    try:
        async with async_session_maker() as session:
            account = Account(
                name=name,
                email=email,
                hashed_password=hash_password(password),
                role="user",
                is_active=True,
                is_verified=False,
            )
            session.add(account)
            await session.commit()
    except Exception as e:
        logger.error("register error", error=e)
        raise HTTPException(status_code=400, detail="User already exists")

    return {"message": "Successfully registered"}


@auth.post("/request-verify-token", name="auth:request-verify-token", status_code=201)
async def request_verify_token(
    verify_request: schema.VerifyRequest,
):
    verify_input = verify_request.model_dump()
    verify_token = create_verify_token(
        {
            "email": verify_input["email"],
            "name": verify_input["name"],
        }
    )
    print(f"verify_token: {verify_token}")


@auth.post("/verify", name="auth:verify", status_code=204)
async def verify(
    token: str = Query(...),
):
    try:
        verify_data = decode_verify_token(token)
        async with async_session_maker() as session:
            await session.execute(
                sqlalchemy.update(Account)
                .where(
                    Account.email == verify_data["email"],
                    Account.name == verify_data["name"],
                )
                .values(is_verified=True)
            )

            return
    except Exception as e:
        logger.error("verify error", error=e)
        raise HTTPException(status_code=400, detail="Invalid token")


@auth.post(
    "/forget-password",
    name="auth:forget-password",
    response_model=schema.ForgetPasswordSuccess,
    status_code=200,
)
async def forget_password(
    request: Request,
):
    raise NotImplementedException()


@auth.post("/reset-password", name="auth:reset-password", status_code=204)
async def reset_password(
    request: Request,
):
    raise NotImplementedException()
