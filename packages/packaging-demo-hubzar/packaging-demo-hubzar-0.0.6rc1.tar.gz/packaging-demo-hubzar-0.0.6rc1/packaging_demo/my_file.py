"""exercise file"""

import numpy as np

from packaging_demo.my_folder.my_nested_file import CONSTANT as CONSTANT2
from packaging_demo.my_other_file import CONSTANT

MY_ARRAY = np.array([1, 2, 3])
STRING_EXAMPLE = 'example string "a" '
print(MY_ARRAY)

print(CONSTANT)
print(CONSTANT2)


def add_number(a: int, b: int, c: int) -> int:
    """Return the sum of three numbers"""
    return sum([a, b, c])
