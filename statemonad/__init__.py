from collections.abc import Iterable

from statemonad.statemonad.statemonad import StateMonad as _StateMonad
from statemonad.statemonad.from_ import from_ as _from_, get as _get
from statemonad.statemonad.init import init_state_monad as _init_state_monad

from_ = _from_
get = _get
put = from_(None).put

init_state_monad = _init_state_monad


def zip[State, U](
    others: Iterable[_StateMonad[State, U]],
):
    """
    Combine multiple state monads into a single monad that evaluates each
    one and returns their result as a tuple.

    This function takes an iterable of state monads and produces a new state monad
    that, when applied to a state, runs each of the original monads in sequence
    with the same initial state. The final state is derived from the sequence, and
    the result is a tuple of all the values produced by the monads.

    Example:
    ``` python
    m1, m2, m3 = from_(1), from_(2), from_(3)

    state, value = zip((m1, m2, m3)).apply(state)

    print(value)  # Output will be (1, 2, 3)
    ```
    """

    others = iter(others)
    try:
        current = next(others).map(lambda v: (v,))
    except StopIteration:
        return from_[State](tuple[U]())
    else:
        for other in others:
            current = current.zip(other).map(lambda v: v[0] + (v[1],))
        return current
