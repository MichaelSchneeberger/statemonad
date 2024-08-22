from abc import ABC, abstractmethod

from statemonad.stateapplicative import StateApplicative


class StateMonadNode[State, U](StateApplicative[State, U], ABC):
    """
    Inherit from this class to create a custom state monad.

    A state monad encapsulates both state and computation, represented as nodes in a tree-like structure. 
    Each node corresponds to an operation that transforms the state and produces a value. 

    This tree grows dynamically as operations are applied to the state monad, where each operation 
    extends the computation by adding new nodes to the tree. When the `apply` method is called on 
    the root node, the state is propagated through the entire tree, threading it through all 
    operations and producing the final result.

    Usage of this class allows for composing complex stateful computations in a functional way.
    """
    
    pass


class SingleChildStateMonadNode[State, U, ChildU](StateMonadNode[State, U]):
    """
    Represents a state monad node with a single child.
    """

    @property
    @abstractmethod
    def child(self) -> StateMonadNode[State, ChildU]: ...


class TwoChildrenStateMonadNode[State, U, L, R](StateMonadNode[State, U]):
    """
    Represents a state monad node with two children.
    """

    @property
    @abstractmethod
    def left(self) -> StateMonadNode[State, L]: ...

    @property
    @abstractmethod
    def right(self) -> StateMonadNode[State, R]: ...
