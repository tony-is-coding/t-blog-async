from time import time

from sqlalchemy import text
from sanic.response import json

from applications.user.persistent import diff_username, diff_email, get_user_by_username
from applications.user.schema import RegisterReq, LoginReq
from common.auth import login_user, UserInfo, logout_user
from common.client import client
from common.utils.crypto import decrypt, encrypt
from config import config


class UserService:

    @classmethod
    async def validate_ts(cls, secret: str, ts: int) -> str:
        """
        check if the ts matched the ts substring of secret password str

        :param
            secret: the secret string, format: encrypt(password_ts)
            ts:  the bind timestamp
        :return  encrypted password
        """
        public = await decrypt(secret=secret)
        password, tss = public.split("_")
        if ts != int(tss):
            raise ValueError("ts not matched")
        if ts - int(time()) > 3:  # 3 second expire
            raise TimeoutError("ts is not valid")
        encrypt_password = await encrypt(password)
        return encrypt_password

    @classmethod
    async def check_password(cls, secret: str, ts: int, en_pwd: str) -> bool:
        """
        compare password
        """
        if cls.validate_ts(secret, ts) == en_pwd:
            return True
        return False

    @classmethod
    async def register_service(cls, body: RegisterReq) -> json:
        """
            # TODO: handler error
            register user by email and username
            :param body: RegisterReq object
            :return: json object
        """
        engine = await client.mysql_db()
        async with engine.acquire() as conn:
            exist_username = await diff_username(conn, body.username)
            if exist_username:
                print("exist username")
            exist_email = await diff_email(conn, body.email)
            if exist_email:
                print("exist email")

            password = cls.validate_ts(body.password, body.ts)
            res = await conn.execute(
                text("insert into user_base(username,password,email) values(:username,:password,:email)"), dict(
                    username=body.username,
                    password=password,
                    email=body.email
                ))
            token = await login_user(user_id=res.lastrowid, user_info=UserInfo(
                username=body.username,
                email=body.email,
                head_image=config.DEFAULT_HEAD_IMAGE
            ))

        return json({"token": token})

    @classmethod
    async def login_service(cls, body: LoginReq) -> json:
        engine = await client.mysql_db()

        async with engine.acquire() as conn:
            user = await get_user_by_username(conn, body.username)
            if not cls.check_password(body.password, body.ts, user.password):
                raise ValueError("password is not valid")
            token = await login_user(
                user_id=user.id,
                user_info=UserInfo(
                    username=user.username,
                    email=user.email,
                    head_image=user.head_image
                ))
        return json({"token": token})

    @staticmethod
    async def logout_service(user_id: int) -> json:
        """
        user logout

        :return json
        """
        await logout_user(user_id=user_id)
        return json({"msg": "ok"})
