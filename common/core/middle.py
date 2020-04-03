from applications import bpg


# 请求拦截
@bpg.middleware("request")
async def request_hijack(request):
    print("received a request")
    print(request)


__all__ = [None]
