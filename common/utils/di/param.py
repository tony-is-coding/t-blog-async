from typing import Callable


class Depends:
    def __init__(self, dependency: Callable = None, *, use_cache: bool = True):
        self.dependency = dependency
        self.use_cache = use_cache
