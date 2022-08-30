import warnings
from numpy import VisibleDeprecationWarning
import typing as _tp


class deprecated:
    def __init__(self, reason: str):
        if not isinstance(reason, str):
            raise ValueError("argument `reason: str` is required")
        self._reason = reason

    def __call__(self, func: _tp.Callable[..., _tp.Any]) -> _tp.Callable[..., _tp.Any]:
        def decorated_func(*args: _tp.Any, **kwargs: _tp.Any) -> _tp.Any:
            warnings.warn(
                f"{func.__name__} is deprecated: {self._reason}",
                category=VisibleDeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)

        decorated_func.__name__ = func.__name__
        decorated_func.__doc__ = "deprecated: " + self._reason
        return decorated_func
