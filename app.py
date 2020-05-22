from asyncio import TimeoutError
import asyncio

from sanic import Sanic
from sanic.exceptions import NotFound

from applications import bpg
from common.exceptions.handler import server_500_handler, timeout_handler, server_404_handler

app = Sanic("t-blog-async")
app.blueprint(bpg)

app.error_handler.add(TimeoutError, timeout_handler)
app.error_handler.add(NotFound, server_404_handler)
app.error_handler.add(Exception, server_500_handler)


async def timeout():
    await asyncio.sleep(4)


@app.get("/demo")
async def demo(request):
    task = asyncio.create_task(timeout())
    await asyncio.wait_for(task, 3)


if __name__ == '__main__':
    app.run()
