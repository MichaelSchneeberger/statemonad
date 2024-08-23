from dataclassabc import dataclassabc

import statemonad
from statemonad.abc import StateMonadNode
from statemonad.typing import StateMonad


type State = tuple[int, ...]
state = tuple()


def collect_even_numbers(num: int):
    """
    This function encapsulates the given number within a state monad
    and saves it to the state if the number is even.
    """

    if num % 2 == 0:

        @dataclassabc(frozen=True)
        class CollectEvenNumbers(StateMonadNode[State, int]):
            num: int

            def apply(self, state: State):
                n_state = state + (self.num,)
                return n_state, self.num

        return statemonad.from_node(CollectEvenNumbers(num=num))

    else:
        return statemonad.from_[State](num)


def flat_map_func(z):
    raise Exception('test')
    """
    Traceback (most recent call last):
    File "[...]\statemonad\statemonadtree\operations\flatmapmixin.py", line 21, in apply
        result = self.func(value).apply(state)
                ^^^^^^^^^^^^^^^^
    File "[...]\examples\raiseexceptionexample.py", line 35, in flat_map_func
        raise Exception('test')
    Exception: test

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
    File "[...]\main.py", line 2, in <module>
        import examples.raiseexceptionexample
    File "[...]\examples\raiseexceptionexample.py", line 47, in <module>
        state, value = example(3).apply(state)
                    ^^^^^^^^^^^^^^^^^^^^^^^
    File "[...]\statemonad\statemonad\statemonad.py", line 28, in apply
        return self.child.apply(state)
            ^^^^^^^^^^^^^^^^^^^^^^^
    File "[...]\statemonad\statemonadtree\operations\flatmapmixin.py", line 21, in apply
        result = self.func(value).apply(state)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "[...]\statemonad\statemonad\statemonad.py", line 28, in apply
        return self.child.apply(state)
            ^^^^^^^^^^^^^^^^^^^^^^^
    File "[...]\statemonad\statemonadtree\operations\flatmapmixin.py", line 21, in apply
        result = self.func(value).apply(state)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "[...]\statemonad\statemonad\statemonad.py", line 28, in apply
        return self.child.apply(state)
            ^^^^^^^^^^^^^^^^^^^^^^^
    File "[...]\statemonad\statemonadtree\operations\flatmapmixin.py", line 27, in apply
        raise StateMonadOperatorException(
    statemonad.exceptions.StateMonadOperatorException: State Monad operator exception caught. See the traceback below for details on the operator call.

    StateMonad Operation Traceback (most recent call last):
    File "[...]\main.py", line 2
        import examples.raiseexceptionexample
    File "[...]\examples\raiseexceptionexample.py", line 47
        state, value = example(3).apply(state)
    File "[...]\statemonad\statemonad\statemonad.py", line 28
        return self.child.apply(state)
    File "[...]\statemonad\statemonadtree\operations\flatmapmixin.py", line 21
        result = self.func(value).apply(state)
    File "[...]\statemonad\statemonad\statemonad.py", line 28
        return self.child.apply(state)
    File "[...]\statemonad\statemonadtree\operations\flatmapmixin.py", line 21
        result = self.func(value).apply(state)
    File "[...]\examples\raiseexceptionexample.py", line 42
        lambda y: collect_even_numbers(y + 1).flat_map(flat_map_func)
    """
    return collect_even_numbers(z + 1)

# do some monadic operations using `flat_map`
def example(init):
    return collect_even_numbers(init + 1).flat_map(
        lambda x: collect_even_numbers(x + 1).flat_map(
            lambda y: collect_even_numbers(y + 1).flat_map(flat_map_func)
        )
    )


state, value = example(3).apply(state)
