from typing import Dict

cache: Dict[str, Dict] = {}


def cacheable(func):
    """A simple cache implementation as many parts of the sum are repetitive."""
    def inner(*args, **kwargs):
        # if len(kwargs) != 0:
        #     raise NotImplementedError('`kwargs` not supported by cache')
        cached_values = cache.get(repr(func))
        cached = cached_values.get(args, None)
        if cached is None:
            cached = func(*args, **kwargs)
            cached_values[args] = cached
        return cached

    cache[repr(func)] = {}
    return inner


factorial_cache: Dict[int, int] = {}


def cacheable_factorial(func):
    """A simple cache implementation as many parts of the sum are repetitive."""
    def inner(*args, **kwargs):
        cached = factorial_cache.get(args, None)
        if cached is None:
            cached = func(*args, **kwargs)
            factorial_cache[args] = cached
        return cached

    return inner