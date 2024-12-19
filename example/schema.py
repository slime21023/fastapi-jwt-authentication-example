from pydantic import BaseModel


class AccessTokenSuccess(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenSuccess(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterSuccess(BaseModel):
    message: str = "Successfully registered"


class ForgetPasswordSuccess(BaseModel):
    message: str = "Forget password sent"


class VerifyRequest(BaseModel):
    email: str
    name: str