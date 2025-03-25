import statemonad


state = {}

def is_even(_):
    raise Exception('test')
    """
    Traceback (most recent call last):
    File "[...]\statemonad\statemonadtree\operations\mapmixin.py", line 25, in apply
        result = self.func(value)
    File "[...]\examples\raiseexceptionexample.py", line 7, in is_even
        raise Exception('test')
    Exception: test

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
    File "[...]\main.py", line 2, in <module>
        import examples.raiseexceptionexample
    File "[...]\examples\raiseexceptionexample.py", line 43, in <module>
        state, value = m.apply(state)
                    ~~~~~~~^^^^^^^
    File "[...]\statemonad\statemonad\statemonad.py", line 27, in apply
        return self.child.apply(state)
            ~~~~~~~~~~~~~~~~^^^^^^^
    File "[...]\statemonad\statemonadtree\operations\mapmixin.py", line 31, in apply
        raise StateMonadOperatorException(self.to_operator_exception_message())
    statemonad.exceptions.StateMonadOperatorException: State Monad operator exception caught. See the traceback below for details on the operator call stack.

    StateMonad Operation Traceback (most recent call last):
    File "[...]\main.py", line 2
        import examples.raiseexceptionexample
    File "[...]\examples\raiseexceptionexample.py", line 41
        m = statemonad.from_(3).map(is_even)
    """

m = statemonad.from_(3).map(is_even)

state, value = m.apply(state)
