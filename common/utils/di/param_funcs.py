from typing import Callable, Any
from . import param


def Depends(  # noqa: N802
        dependency: Callable = None, *, use_cache: bool = True
) -> Any:
    return param.Depends(dependency=dependency, use_cache=use_cache)
