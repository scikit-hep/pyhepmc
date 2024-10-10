import warnings
from typing import Callable, Any
from importlib.metadata import version
from packaging.version import Version


CURRENT_VERSION = Version(version("pyhepmc"))


class deprecated:
    def __init__(self, reason: str, removal: str = ""):
        assert isinstance(reason, str)
        self.reason = reason
        self.removal = Version(removal) if removal else None

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        category: Any = DeprecationWarning
        extra = ""
        if self.removal and CURRENT_VERSION < self.removal:
            extra = f" and will be removed in version {self.removal}"
        msg = f"{func.__name__} is deprecated{extra}: {self.reason}"

        def decorated_func(*args: Any, **kwargs: Any) -> Any:
            warnings.warn(msg, category=category, stacklevel=2)
            return func(*args, **kwargs)

        decorated_func.__name__ = func.__name__
        decorated_func.__doc__ = msg
        return decorated_func
