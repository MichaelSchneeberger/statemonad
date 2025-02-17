
# State Monad

**State Monad** is a Python library that encapsulates stateful operations - computations that require an explicit state object to execute - within a monadic structure.

## Features

* Pragmatic Monad: Implements the core concepts of a state monad in a way that is practical and relevant for a Python developpers. It focus on usability rather than strict adherence to mathematical correctness.
* Object-Orgiented Design: State monad operations are built based on Python classes, favoring an object-oriented approach that prioritizes working with objects rather than deeply nested functions.
* Type hinting: The implemented type hinting ensures that types are correctly inferred by type checkers like [pyright](https://github.com/microsoft/pyright).

## Installation

You can install **State Monad** using pip:

```
pip install statemonad
```

## Usage

The state object is a Python object that represents the state in your computations.
Each operation may modify the state and return a new value based on the updated state.
The result is a chain of operations where the state flows through each step, with the **State Monad** keeping the flow clean and organized.

### Example

In this example, we define the function `collect_even_numbers`, a stateful operation that adds the provided number `num` to the state if it is even.

<!-- In this example, we define the function `collect_even_numbers` - representing the stateful operation -, which returns a custome state monad `CollectEvenNumbers` that adds the number to the state if the given number is even, or a default state monad encapsulating the value otherwise.
The `example` function performs monadic operations using the `collect_even_numbers` operator, resulting in a state monad.
Finally, the constructed state monad is applied with an empty tuple as the initial state. -->


``` python
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
```

Defining the state monad `CollectEvenNumbers` as a class allows for a clean and readable representation of the resulting state monad object `monad`.
However, some details of this representation is obscured by the lambda function used with the `flat_map` method.


<!-- ## Enhanced Traceback -->


## References

Here are other Python libraries that implement the state monad, prioritizing correct type hinting over practical usability:

* [https://github.com/dbrattli/OSlash](https://github.com/dbrattli/OSlash/blob/master/oslash/state.py)
* [https://github.com/dry-python/returns](https://github.com/dry-python/returns)
* [https://github.com/jasondelaat/pymonad](https://github.com/jasondelaat/pymonad/blob/release/pymonad/state.py)


<!-- The following example illustrates how a state object `state` is created and used to compute an object `result`:


``` python
def compute_something(state):
    state, val1 = operation1(state)
    state, val2 = operation2(val1, state)
    state, result = operation2(val1, val2, state)
    return state, result

# Create state object used in the preceding computations.
state = init_state()

state, result1 = compute_something(state)
```

If we recompute the object, we can either use the same state object `state`,

``` python
# result2 might be different from result1, that is result1 != result3
state, result2 = compute_something(state)
```

or, we can create a new state object `state` resulting in the same object `result` as before:

``` python
# Create the same state object as before
state = init_state()

# result 1 == result 3
state, result3 = compute_something(state)
```
 -->
