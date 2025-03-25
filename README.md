
# StateMonad

**StateMonad** is a Python library that encapsulates stateful operations - computations that require an explicit state object to execute - within a monadic structure.

## Features

* Functional Purity: The state monad allows functions to access and modify shared state without relying on global variables, thereby preserving functional purity.
* Compositionality: By abstracting the state-passing mechanism, the state monad allows easy integration with other libraries that also rely on stateful computations.
* Type hinting: The implemented type hinting ensures that types are correctly inferred by type checkers like [pyright](https://github.com/microsoft/pyright).
* Enhanced Exception handling: When an error is raised within the stateful computation, the traceback includes not only the standard error information but also the traceback to the point where the state monad was created.
* Pragmatic Monad: Implements the core concepts of a state monad in a way that is practical and relevant for Python developpers. It focus on usability rather than strict adherence to mathematical correctness.
<!-- * Object-Orgiented Design: StateMonad operations are built based on Python classes, favoring an object-oriented approach that prioritizes working with objects rather than deeply nested functions. -->

## Installation

You can install **StateMonad** using pip:

```
pip install statemonad
```

## Usage

The state object is a Python object that represents the state in your computations.
Each operation may modify the state and return a new value based on the updated state.
The result is a chain of operations where the state flows through each step, with the **StateMonad** keeping the flow clean and organized.

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

state, value = monad.apply(state)

print(f"{value=}")  # Output will be value=7
print(f"{state=}")  # Output will be state=(4, 6)
```

A state monad implemented as a class (like `CollectEvenNumbers`) provides a clean string representation when printing the state monad object `monad`.
``` python
# Output will be
# StateMonad(flat_map(CollectEvenNumbers(num=4), <lambda>))
print(monad)

# Output will be
# monad=StateMonadImpl(
#   child=FlatMapImpl(
#       child=CollectEvenNumbers(num=4),
#   func=<function example.<locals>.<lambda> at 0x000001A546B53D80>))
print(f"{monad=}")
```
However, some details of this representation is still obscured by the lambda function used with the `flat_map` method.



## Operations

- **from_**: Creates a state monad that returns a fixed values while leaving the state unchanged.
    ``` python
    m = statemonad.from_(3)
    ```
- **map**: Applies the provided function to the monad's value.
- **flat_map**: Applies the provided function to the monad's value, producing a new state monad, and flattens the result.
- **zip**: Combines multiple state monads into a single monad that evaluates each one and returns their result as a tuple.
    ``` python
    m = statemonad.zip((m1, m2, m3))
    ```
- **get**: Retrieves the current state as the monad's value.
    ``` python
    m = m.get()
    ```
- **put**: Updates the state with the provided value.
    ``` python
    m = m.put(state={})
    ```



## Enhanced Exception handling

Consider the following use case:

``` python
def is_even(_):
    raise Exception('unexpected exception')

# create the state monad
m = statemonad.from_(3).map(is_even)

# run the computation based on the information contained inside the state object
state, value = m.apply(state)
```

Here, the first instruction defines the stateful operation, but does not immediately execute it.
Instead, it returns a state monad, deferring computation until the `apply` method is called in the second instruction
However, this delayed evaluation introduces a debugging challenge — if an unexpected exception occurs inside the stateful operation, the traceback points to the apply call rather than the original location where the operation was defined. 
This makes it difficult to pinpoint the source of the issue.

To improve debugging, **StateMonad** enhances exception messages by augmenting the traceback. When an error occurs during execution, the traceback not only includes standard error details but also tracks where the state monad was originally created:
```
statemonad.exceptions.StateMonadOperatorException: State Monad operator exception caught. See the traceback below for details on the operator call stack.

StateMonad Operation Traceback (most recent call last):
File "[...]\main.py", line 2
    import examples.raiseexceptionexample
File "[...]\examples\raiseexceptionexample.py", line 41
    m = statemonad.from_(3).map(is_even)
```
This feature aids in identifying the root cause of errors more efficiently.


## References

Several state monad implementations exist in Python, such as:
* [https://github.com/dbrattli/OSlash](https://github.com/dbrattli/OSlash/blob/master/oslash/state.py)
* [https://github.com/dry-python/returns](https://github.com/dry-python/returns)
* [https://github.com/jasondelaat/pymonad](https://github.com/jasondelaat/pymonad/blob/release/pymonad/state.py)

However, these implementations tend to be unnecessary complex, as they attempt to directly translate functional programming concepts into Python -- a language that only weakly supports types through type hinting.
