from sanic import Sanic
from sanic.response import text
from common.utils.doc import summary

app = Sanic("doc-demo")


# Oops! badly error still not handed
# Swagger Open-Api need being install
@app.get("/hello")
@summary
async def foo():
    return text("bar...")


if __name__ == '__main__':
    app.run()
