import copy
import ujson
from decimal import Decimal, ROUND_HALF_UP

from sanic.request import Request


def parser_args(args: dict) -> dict:
    """
    parse form args
    :param args:
    :return:
    """
    args = copy.copy(args)
    for k, v in args.items():
        args[k] = v[0]
    return args


def parser_data(request: Request) -> dict:
    """
    parser form data
    :param request:
    :return:
    """
    if request.form:
        data = parser_args(request.form)
    else:
        data = request.json

    return data


def json_loads(v):
    return ujson.loads(v, precise_float=True)


def json_dumps(v):
    return ujson.dumps(v, ensure_ascii=False)

