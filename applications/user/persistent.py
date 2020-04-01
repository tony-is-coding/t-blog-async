from aiomysql.sa import SAConnection
from aiomysql.sa.result import RowProxy
from sqlalchemy import text


async def diff_username(conn: SAConnection, username: str) -> bool:
    proxy = await conn.execute(text(" select id from user_base where username = :username "),
                               dict(username=username))
    result = await proxy.fetchone()
    if result:
        return True
    return False


async def diff_email(conn: SAConnection, email: str) -> bool:
    proxy = await conn.execute(text(" select id from user_base where email = :email "),
                               dict(email=email))
    result = await proxy.fetchone()
    if result:
        return True
    return False


async def get_user_by_username(conn: SAConnection, username: str) -> RowProxy:
    proxy = await conn.execute(text("select id, username, hand_image,email, password from user_base where username "
                                    "=:username "), dict(username=username))
    result = await proxy.first()
    if not result:
        raise ValueError("user does not exist")
    return result
