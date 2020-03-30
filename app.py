from sanic import Sanic
from applications import bpg
from common import middle  # noqa

app = Sanic("t-blog-async")
app.blueprint(bpg)

if __name__ == '__main__':
    app.run()
