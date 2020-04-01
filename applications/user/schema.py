from pydantic import BaseModel


class RegisterReq(BaseModel):
    email: str
    username: str
    password: str
    ts: int


class LoginReq(BaseModel):
    username: str
    password: str
    ts: int
