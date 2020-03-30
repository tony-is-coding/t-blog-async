import copy

from sanic.request import Request


def parser_args(args: dict):
    args = copy.copy(args)
    for k, v in args.items():
        args[k] = v[0]
    return args


def parser_data(request: Request):
    if request.form:
        data = parser_args(request.form)
    else:
        data = request.json

    return data
