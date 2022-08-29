import warnings
from numpy import VisibleDeprecationWarning


class deprecated:
    def __init__(self, reason):
        if not isinstance(reason, str):
            raise ValueError("argument `reason: str` is required")
        self._reason = reason

    def __call__(self, func):
        def decorated_func(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} is deprecated: {self._reason}",
                category=VisibleDeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)

        decorated_func.__name__ = func.__name__
        decorated_func.__doc__ = "deprecated: " + self._reason
        return decorated_func
