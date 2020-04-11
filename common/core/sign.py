import hashlib
from functools import wraps

from sanic.request import Request

from config.config import SIGN_KEY


def sha256_sign(val) -> str:
    """
    SHA256 sign
    """
    try:
        m = hashlib.sha256()
        m.update(val.encode('utf-8'))
        return m.hexdigest()
    except Exception as e:
        raise e


def make_sign(params: dict) -> str:
    """signature"""
    sign_key = SIGN_KEY
    data = sorted(params.items(), key=lambda d: d[0], reverse=False)
    data_str = '&'.join(
        ['%s=%s' % (k.strip(), str(vl).strip()) for (k, vl) in data])
    return sha256_sign(sign_key + data_str)
