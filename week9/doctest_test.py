"""a simple module

>>> add(1, 10)
11
"""


def add(x: float, y: float) -> float:
    """Function that adds two numbers.

    >>> add(1, 2)
    3

    >>> add(1, -2)
    -1

    Args:
        x (float): first number
        y (float): second number

    Returns:
        float: the result of the addition
    """
    return x + y


# if __name__ == "__main__":
#     import doctest

#     doctest.testmod(verbose=True)
