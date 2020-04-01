from sanic import Sanic
from sanic.exceptions import NotFound
from asyncio import TimeoutError

from applications import bpg
from common import middle  # noqa
from common.exceptions.handler import server_500_handler, timeout_handler, server_404_handler

app = Sanic("t-blog-async")
app.blueprint(bpg)

app.error_handler.add(TimeoutError, timeout_handler)
app.error_handler.add(NotFound, server_404_handler)
app.error_handler.add(Exception, server_500_handler)

import asyncio


async def timeout():
    await asyncio.sleep(4)


@app.get("/demo")
async def demo(request):
    task = asyncio.create_task(timeout())
    await asyncio.wait_for(task, 3)


if __name__ == '__main__':
    app.run()
