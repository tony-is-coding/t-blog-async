from sanic.request import Request
from sanic.response import json

from applications.user.blueprint import blueprint as bp
from applications.user.schema import RegisterReq, LoginReq
from applications.user.service import UserService
from common.auth import authorized

from common.utils.parser import parser_data
from common.utils.sign import validate_sign


@bp.post("/user")
@validate_sign
async def register(request):
    data = parser_data(request)
    req = RegisterReq(**data)
    res = await UserService.register_service(req)
    return res


@bp.post("/login")
async def login(request):
    data = parser_data(request)
    req = LoginReq(**data)
    res = await UserService.login_service(req)
    return res


@bp.get("/logout")
@authorized()
async def logout(request: Request):
    user = request.user


@bp.get("/user")
async def user_info(request, name: str, age: int):
    return json({
        "name": "tony",
        "age": 24
    })


@bp.patch("/user")
async def update_user_info(request):
    pass


@bp.put("/email")
async def change_email(request):
    pass


@bp.put("/password")
async def change_password(request):
    pass


