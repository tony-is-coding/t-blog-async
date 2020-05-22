import hashlib
import random
import threading
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


def id_generator():
    """snow flake unique id"""
    # 无锁
    # 计算快
    # 每秒计算 100W次
    shard_id = 15
    seq = 15
    start_epoch = 1585658821524000
    return (int(time.time() * 1000000) - start_epoch) << 54 | shard_id << 4 | seq


NUM = 0
LOOK = threading.Lock()  # mutex lock


def new_id_generator():
    """
    13位时间戳(毫秒级)
    4位 (机器编号 + 进程编号)(0-9999) 提供最多10000个进程(需要为每一个进程提供一个编号)
    3位自增序号(0-999)

    更新版本更加清晰的雪花式算法
    1. 加入锁机制防止进程内多线程并发竞争
    2. 思路清晰更加容易懂
    3. 单进程每秒提供100W个不重复ID
    """
    server_id = 99
    process_id = 99
    global NUM
    LOOK.acquire()
    if NUM == 1000:
        NUM = 0
    union_id = int(f"{(int(time.time() * 1000)):#013d}{server_id:#02d}{process_id:#02d}{NUM:#03d}")
    NUM += 1
    LOOK.release()
    return union_id


if __name__ == "__main__":

    res = dict()
    st = time.time()
    for i in range(1000000):
        # print(int(time.time() * 1000000))
        uid = id_generator()
        if res.get(uid) is not None:
            print(i)
            break
        res[uid] = 1
    print("spend:", time.time() - st)
