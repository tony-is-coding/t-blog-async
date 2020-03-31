import hashlib
from functools import wraps

from config.config import SIGN_KEY


def sha256_sign(val) -> str:
    """
    SHA256签名
    """
    try:
        m = hashlib.sha256()
        m.update(val.encode('utf-8'))
        return m.hexdigest()
    except Exception as e:
        raise e


def make_sign(params: dict) -> str:
    """参数签名"""
    sign_key = SIGN_KEY
    data = sorted(params.items(), key=lambda d: d[0], reverse=False)
    data_str = '&'.join(
        ['%s=%s' % (k.strip(), str(vl).strip()) for (k, vl) in data])
    return sha256_sign(sign_key + data_str)


def validate_sign(func):
    async def wrapper(*args, **kwargs):
        # TODO: 签名加密临时取消
        # real_sign = make_sign(param)
        # if real_sign != sign:
        #     raise_400("参数签名验证失败")
        res = await func(*args, **kwargs)
        return res

    return wrapper
