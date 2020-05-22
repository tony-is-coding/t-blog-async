import json
from dataclasses import dataclass
from functools import wraps

from sanic.request import Request

from common.tools.generator import get_random_string
from common.core.client import client

USER_EXPIRE = 604800  # 60 * 60 * 24 * 7 ---  7 days expire


@dataclass
class UserInfo:
    username: str
    email: str
    head_image: str


async def login_user(user_id: int, user_info: UserInfo) -> str:
    """
    login user, set session info to redis
    :return: string session id
    """
    token = get_random_string()
    redis_conn = await client.redis_db()

    # 事务
    await redis_conn.set(f"watch_{user_id}", "0")
    redis_conn.watch(f"watch_{user_id}")

    mt = redis_conn.multi_exec()
    mt.setex(f"token_{user_id}", token)
    mt.setex(token, json.dumps(user_info.__dict__))
    redis_conn.delete(f"watch_{user_id}")
    res = await mt.execute()
    if not res:
        return "login failed"
    return token


async def logout_user(user_id):
    redis_conn = await client.redis_db()
    token = await redis_conn.get(f'token_{user_id}', encoding="utf-8")
    if token:
        await redis_conn.delete(f'token_{user_id}')
        await redis_conn.delete(f'{token}')


async def cur_user(token: str) -> UserInfo:
    redis_conn = await client.redis_db()
    user_info = await redis_conn.get(token)
    if not user_info:
        raise ValueError("Oops, login status expired")
    return UserInfo(**json.loads(user_info))


def authorized():
    """
    halt the request
    checkout token
    if is valid then set the UserInfo object to request
    :return:
    """

    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *arg, **kwargs):
            user = await cur_user(request.token)
            setattr(request, "user", user)
            res = await f(request, *arg, **kwargs)
            return res

        return decorated_function

    return decorator
