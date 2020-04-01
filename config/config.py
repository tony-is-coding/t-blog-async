# from decouple import config
from decouple import AutoConfig
from pathlib import Path

DEBUG = True

if DEBUG:
    path = Path(__file__).resolve().parent / 'local'
else:
    path = Path(__file__).resolve().parent / 'dev'
if not path.exists():
    path = ''
config = AutoConfig(search_path=path)

# app
APP_HOST = config("APP_HOST", "", cast=str)
APP_PORT = config("APP_PORT", "", cast=int)

# cache-redis
SESSION_REDIS = config("SESSION_REDIS", "", cast=str)
USER_REDIS = config("USER_REDIS", "", cast=str)
CONFIG_REDIS = config("CONFIG_REDIS", "", cast=str)
ADMIN_USER_REDIS = config("ADMIN_USER_REDIS", "", cast=str)

MINSIZE = config("DB_MINSIZE", 10, cast=int)
MAXSIZE = config("DB_MAXSIZE", 10, cast=int)
HOST = config("DB_HOST", "127.0.0.1", cast=str)
PORT = config("DB_PORT", 3306, cast=int)
USER = config("DB_USER", "root", cast=str)
PASSWORD = config("DB_PASSWORD", "", cast=str)
DB = config("DB", "", cast=str)

# user
TOKEN_SECRET_KEY = config("TOKEN_SECRET_KEY", "", cast=str)

# param sign key
SIGN_KEY = config("SIGN_KEY", "nymiPvtx3vkfevXUbdJnBNuU97EtBKQp", cast=str)

# default head image
DEFAULT_HEAD_IMAGE = config("DEFAULT_HEAD_IMAGE","xxx",cast=str)
