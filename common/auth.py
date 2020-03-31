import json
from dataclasses import dataclass

from common.generator import get_random_string
from common.client import client

USER_EXPIRE = 604800  # 60 * 60 * 24 * 7 ---  7天登录过期


@dataclass
class UserCache:
    username: str
    email: str
    head_image: str


async def login_user(user_id: int, user_info: UserCache) -> str:
    """
    login user, set session info to redis
    :return: string session id
    """
    token = get_random_string()
    redis_conn = await client.redis_db()

    # 事务封锁
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
    token = await redis_conn.get(f'token_{user_id}')
    if token:
        await redis_conn.delete(f'token_{user_id}')
        await redis_conn.delete(f'{token.decode()}')
