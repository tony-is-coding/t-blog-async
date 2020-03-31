import hashlib
import random
import time
from datetime import datetime

try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    import warnings

    warnings.warn('A secure pseudo-random number generator is not available '
                  'on your user. Falling back to Mersenne Twister.')
    using_sysrandom = False

global_char = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def get_random_string(length=12, allowed_chars=global_char):
    """
    Return a securely generated random string.

    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value.

    log_2((26+26+10)^12) =~ 71 bits
    """
    if not using_sysrandom:
        from config import config

        random.seed(
            hashlib.sha256(
                ('%s%s%s' % (random.getstate(), time.time(), config.TOKEN_SECRET_KEY)).encode()
            ).digest()
        )
    return ''.join(random.choice(allowed_chars) for _ in range(length))


def id_generator(t: datetime, shard_id=0, seq=0):
    start_epoch = 1585658821524
    res = int(datetime.timestamp(t) * 1000000 - start_epoch * 1000) << 8 | shard_id << 4 | seq
    return res
