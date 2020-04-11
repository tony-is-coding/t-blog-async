# from typing import Callable, Any
# import inspect
#
# from sanic import Sanic
# from sanic.response import json
# from sanic.request import Request
#
# app = Sanic("demo")
#
#
# def di(func):
#     async def wrapper(request: Request, *args, **kwargs):
#         res = await func(request, *args, **kwargs)
#         return res
#
#     return wrapper
#
#
# def get_typed_signature(call: Callable) -> inspect.Signature:
#     pass
#
#
# def get_typed_parameter(call: Callable) -> inspect.Parameter:
#     pass
#
#
# def get_typed_annotation(call: Callable) -> Any:
#
#
# @app.get("/hello")
# @di
# async def hello(request):
#     return json({"name": "tony"})
#
#
# if __name__ == '__main__':
#     app.run()


"""
dependence inject， plan to copy from  fast-api frameword
"""
