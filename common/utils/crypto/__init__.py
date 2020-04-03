import os
import base64

import rsa
import aiofiles


async def encrypt(public: str) -> str:
    content = public.encode('utf8')
    path = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/") + "/public_key"
    async with aiofiles.open(path, "r") as f:
        binary = await f.read()
        key = binary.encode("utf-8")
    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(key)
    crypto = rsa.encrypt(content, pubkey)
    return base64.b64encode(crypto).decode('utf8')


async def decrypt(secret: str) -> str:
    """
    :param secret: secret string
    :return: public str
    >>>  a = await decrypt(secret)
    >>>  print(a)
    """
    path = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/") + "/private_key"
    async with aiofiles.open(path, 'r') as f:
        binary = await f.read()
        key = binary.encode("utf-8")
    try:
        secret = base64.b64decode(secret)
        private_key = rsa.PrivateKey.load_pkcs1(key, format='PEM')
        con = rsa.decrypt(secret, private_key)
        return con.decode("utf-8")
    except UnicodeEncodeError:
        ...  # TODO: deal error catch and hand
