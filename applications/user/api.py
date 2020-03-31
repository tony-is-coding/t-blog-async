from sanic.response import json

from applications.user.blueprint import blueprint as bp
from applications.user.schema import RegisterReq
from applications.user.service import UserService

from common.utils.parser import parser_data
from common.utils.sign import validate_sign


@bp.post("/user")
@validate_sign
async def register_api(request):
    data = parser_data(request)
    req_body = RegisterReq(**data)
    res = await UserService.register_service(req_body)
    return res


@bp.post("/login")
async def login_api(request):
    pass


@bp.get("/user")
async def user_info_api(request, name: str, age: int):
    return json({
        "name": "tony",
        "age": 24
    })


@bp.patch("/user")
async def update_user_info_api(request):
    pass


@bp.post("/email")
async def email_api(request):
    pass


@bp.put("/password")
async def password_api(request):
    pass
