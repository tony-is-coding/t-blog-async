import aioredis
from aiomysql import sa
from functools import lru_cache

from config import config as cf

config_dict = dict(
    minsize=cf.MINSIZE,
    maxsize=cf.MINSIZE,
    host=cf.HOST,
    port=cf.PORT,
    user=cf.USER,
    password=cf.PASSWORD,
    db=cf.DB,
    autocommit=False)


class Client:

    @staticmethod
    @lru_cache(maxsize=10000)
    async def mysql_db() -> sa.engine:
        engine = await sa.create_engine(**config_dict)
        return engine

    @staticmethod
    @lru_cache(maxsize=10000)
    async def redis_db() -> aioredis.ConnectionsPool:
        redis_client = await aioredis.create_redis_pool("redis://127.0.0.1/1")
        return redis_client


client = Client()


# ping/pong test
async def ping_mysql():
    engine = await client.mysql_db()
    async with engine.acquire() as conn:
        proxy = await conn.execute("select * from user_base")
        result = await proxy.fetchone()
        print(result.email)
        print(type(result))
    engine.close()
    await engine.wait_closed()


async def ping_redis():
    redis_db = await client.redis_db()
    await redis_db.set("name", "tony")
    value = await redis_db.get("name")
    print(value)
    redis_db.close()
    await redis_db.wait_closed()


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(ping_mysql())
    # loop.run_until_complete(ping_redis())
