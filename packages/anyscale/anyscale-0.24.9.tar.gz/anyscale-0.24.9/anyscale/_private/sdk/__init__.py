from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Type, Union


_LAZY_SDK_SINGLETONS: Dict[str, Callable] = {}


def inject_sdk_singleton(key: str, sdk_cls: Type) -> Callable[[Callable], Callable]:
    """Decorator to automatically inject an `_sdk` arg into the wrapped function.

    The arguments to this class are a unique key for the singleton and its type
    (the constructor will be called with no arguments).
    """

    def _inject_typed_sdk_singleton(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            if key not in _LAZY_SDK_SINGLETONS:
                _LAZY_SDK_SINGLETONS[key] = sdk_cls()

            return f(*args, _sdk=_LAZY_SDK_SINGLETONS[key], **kwargs)

        return wrapper

    return _inject_typed_sdk_singleton
