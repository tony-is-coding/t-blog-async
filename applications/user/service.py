from typing import Tuple

from sqlalchemy import text
from sanic.response import json

from applications.user.schema import RegisterReq

from common.client import client
from common.utils.crypto import decrypt

class UserService:

    @classmethod
    async def diff_username(cls, conn, username: str) -> bool:
        proxy = await conn.execute(text(" select id from user_base where username = :username "),
                                   dict(username=username))
        result = await proxy.fetchone()
        if result:
            return True
        return False

    @classmethod
    async def diff_email(cls, conn, email: str) -> bool:
        proxy = await conn.execute(text(" select id from user_base where email = :email "),
                                   dict(email=email))
        result = await proxy.fetchone()
        if result:
            return True
        return False

    @classmethod
    async def register_service(cls, body: RegisterReq):
        engine = await client.mysql_db()
        async with engine.acquire() as conn:
            exist_username = await cls.diff_username(conn, body.username)
            if exist_username:
                print("exist username")
            exist_email = await cls.diff_email(conn, body.email)
            if exist_email:
                print("exist email")

            # password check
            # sign check

        return json({"name": body.username, "age": 24})
