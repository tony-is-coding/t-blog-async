from sanic.response import text


async def server_500_handler(request, exception):
    print(request)
    print(exception)
    return text("Oops, Server error", status=500)


async def timeout_handler(request, exception):
    print(request)
    print(exception)
    return text("Oops, timeout error", status=500)


async def server_404_handler(request, exception):
    print(request)
    print(exception)
    return text("Oops, page not found", status=200)
