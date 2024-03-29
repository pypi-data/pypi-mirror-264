from typing import Callable, List


class Transform:
    def __init__(self, fn: Callable, steps: List[Callable] = None):
        if steps is not None:
            self.steps = steps  # test
        else:
            self.steps = [fn]
        """
                if input is None:
            raise ValueError("Input must not be NoneType")
        """
        self.fn = fn

    def __rshift__(self, transform):
        self.steps.append(transform.fn)  # test
        return type(self)(self.fn, self.steps)  # test


def t(x) -> Transform:
    return Transform(x)
