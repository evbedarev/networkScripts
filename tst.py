import functools, sys

def with_arguments(deco):
    def wrapper(*dargs, **dkwargs):
        def decorator(func):
            result = deco(func, *dargs, **dkwargs)
            # functools.update_wrapper(result, func)
            return result
        return decorator
    return wrapper

@with_arguments
def trace(func, handle, is_enable, sm_msg):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            # args = tuple(list(args).append(sm_msg))
            args = list(args)
            args.append(sm_msg)
            args = tuple(args)

            print(args)
            print(func.__name__, args, kwargs)
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
        finally:
            print(sm_msg)
    return inner if is_enable else func

@trace(sys.stderr, True, 5)
def identity(x, y):
    "id do nothing useful."
    # a = x/0
    print(x+y)
    return x+y


identity(76)
