import operator
from functools import reduce
from typing import Tuple

import scipy.special

from prompt_mac_calculator.utilities.cache import cacheable_factorial


def binomial(top: int, btm: int) -> int:
    return scipy.special.comb(top, btm, exact=True)


@cacheable_factorial
def factorial(val: int) -> int:
    return scipy.special.factorial(val, exact=True)


def multinomial(top: int, btm: Tuple[int]) -> int:
    if sum(btm) != top:
        raise ValueError('denominator indices must sum up to the numerator value')
    try:
        return factorial(top) // reduce(operator.mul, map(factorial, btm))
    except RuntimeWarning as ex:
        raise ValueError(f'Multinomial {top} over {btm} calculation warning: {ex}')


def inclusive_range(begin: int, end: int) -> range:
    return range(begin, end + 1)
