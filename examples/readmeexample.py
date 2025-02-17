from typing import override
from dataclassabc import dataclassabc

import statemonad
from statemonad.abc import StateMonadNode
from statemonad.typing import StateMonad


type State = tuple[int, ...]
state = tuple()


def collect_even_numbers(num: int):
    if num % 2 == 0:

        @dataclassabc(frozen=True, slots=True)
        class CollectEvenNumbers(StateMonadNode[State, int]):
            """
            A custom state monad implemented as a dataclass.
            The `apply` methods adds `num` to the state.
            """
            num: int

            @override
            def apply(self, state: State):
                n_state = state + (self.num,)
                return n_state, self.num

        return statemonad.from_node(CollectEvenNumbers(num=num))

    else:
        return statemonad.from_[State](num)


# chain monadic operations using `flat_map`
def example(init):
    return collect_even_numbers(init + 1).flat_map(
        lambda x: collect_even_numbers(x + 1).flat_map(
            lambda y: collect_even_numbers(y + 1).flat_map(
                lambda z: collect_even_numbers(z + 1)
            )
        )
    )


monad: StateMonad[State, int] = example(3)

# Output will be
# StateMonad(flat_map(CollectEvenNumbers(num=4), <lambda>))
print(monad)

# Output will be
# monad=StateMonadImpl(
#   child=FlatMapImpl(
#       child=CollectEvenNumbers(num=4),
#   func=<function example.<locals>.<lambda> at 0x000001A546B53D80>))
print(f"{monad=}")

state, value = monad.apply(state)

print(f"{value=}")  # Output will be value=7
print(f"{state=}")  # Output will be state=(4, 6)