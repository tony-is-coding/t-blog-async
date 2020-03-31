from sqlalchemy import text
from sanic.response import json

from applications.user.schema import RegisterReq
from common.auth import login_user, UserCache

from common.client import client
from common.utils.crypto import decrypt, encrypt
from config import config


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
    async def check_password(cls, secret: str, ts: int) -> str:
        """
            check if the ts matched the ts substring of secret
            :return  encrypted password
        """
        pub = await decrypt(secret=secret)
        password, tss = pub.split("_")
        if ts != int(tss):
            raise ValueError("ts not matched")
        encrypt_password = await encrypt(password)
        return encrypt_password

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

            password = cls.check_password(body.password, body.ts)
            res = await conn.execute(
                text("insert into user_base(username,password,email) values(:username,:password,:email)"), dict(
                    username=body.username,
                    password=password,
                    email=body.email
                ))
            token = await login_user(user_id=res.lastrowid, user_info=UserCache(
                username=body.username,
                email=body.email,
                head_image=config.DEFAULT_HEAD_IMAGE
            ))

        return json({"token": token})

