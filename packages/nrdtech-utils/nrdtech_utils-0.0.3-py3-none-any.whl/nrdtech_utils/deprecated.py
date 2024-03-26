import warnings
import functools


def deprecated(obj_or_message=None, *, additional_message=None):
    def decorator(obj):
        message = additional_message
        if isinstance(obj_or_message, str) and additional_message is None:
            message = obj_or_message

        if isinstance(obj, type):  # Check if it's a class
            return _deprecated_class(obj, message)
        elif callable(obj):  # Check if it's a callable (function/method)
            return _deprecated_func(obj, message)
        else:
            raise TypeError(
                "Deprecated decorator can only be used with classes or functions"
            )

    if callable(obj_or_message):
        return decorator(obj_or_message)
    return decorator


def _deprecated_class(cls, message):
    @functools.wraps(cls)
    def new_cls(*args, **kwargs):
        _emit_deprecation_warning(cls.__name__, message)
        return cls(*args, **kwargs)

    return new_cls


def _deprecated_func(func, message):
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        _emit_deprecation_warning(func.__name__, message)
        return func(*args, **kwargs)

    return new_func


def _emit_deprecation_warning(name, message):
    full_message = f"{name} is deprecated"
    if message:
        full_message += f". {message}"
    warnings.simplefilter("always", DeprecationWarning)  # turn off filter
    warnings.warn(full_message, category=DeprecationWarning, stacklevel=2)
    warnings.simplefilter("default", DeprecationWarning)  # reset filter
