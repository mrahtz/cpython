doctests = """

TypeVarTuple definition (will eventually be in typing.py)

   >>> class _UnpackedTypeVarTuple:
   ...     def __init__(self, name):
   ...         self._name = name
   ...     def __repr__(self):
   ...         return '*' + self._name
   >>> class TypeVarTuple:
   ...     def __init__(self, name):
   ...         self._name = name
   ...         self._unpacked = _UnpackedTypeVarTuple(name)
   ...     def __iter__(self):
   ...         yield self._unpacked

Tests below. (A lot of these currently produce TypeErrors, but that's fine - we'd only get TypeErrors if the syntax has been parsed successfully.)

Summary examples

    >>> from typing import Generic, TypeVar
    >>> DType = TypeVar('DType')
    >>> Shape = TypeVarTuple('Shape')
    >>> class Array(Generic[DType, *Shape]):
    ...     def __abs__(self) -> Array[DType, *Shape]: ...
    ...     def __add__(self, other: Array[DType, *Shape]) -> Array[DType, *Shape]: ...
    Traceback (most recent call last):
        ...
    TypeError: Parameters to Generic[...] must all be type variables or parameter specification variables.

Specification

    >>> Ts = TypeVarTuple('Ts')

    >>> Shape = TypeVarTuple('Shape')
    >>> class Array(Generic[*Shape]): ...
    Traceback (most recent call last):
        ...
    TypeError: Parameters to Generic[...] must all be type variables or parameter specification variables.

    >>> from typing import Tuple
    >>> def __init__(self, shape: Tuple[*Shape]):
    ...     self._shape: Tuple[*Shape] = shape
    Traceback (most recent call last):
        ...
    TypeError: Tuple[t0, t1, ...]: each t must be a type. Got *Shape.
    >>> def get_shape(self) -> Tuple[*Shape]:
    ...     return self._shape
    Traceback (most recent call last):
        ...
    TypeError: Tuple[t0, t1, ...]: each t must be a type. Got *Shape.

Type Variable Tuple Equality

    >>> def foo(arg1: Tuple[*Ts], arg2: Tuple[*Ts]): ...
    Traceback (most recent call last):
        ...
    TypeError: Tuple[t0, t1, ...]: each t must be a type. Got *Ts.

    >>> class Array:
    ...     def __class_getitem__(cls, x):
    ...         pass
    >>> def pointwise_multiply(
    ...    x: Array[*Shape],
    ...    y: Array[*Shape]
    ... ) -> Array[*Shape]: ...

Multiple Type Variable Tuples: Not Allowed

    >>> Ts1 = TypeVarTuple('Ts1')
    >>> Ts2 = TypeVarTuple('Ts2')
    >>> class Array(Generic[*Ts1, *Ts2]): ...
    Traceback (most recent call last):
        ...
    TypeError: Parameters to Generic[...] must all be type variables or parameter specification variables.

Type Concatenation

    >>> from typing import NewType
    >>> Shape = TypeVarTuple('Shape')
    >>> Batch = NewType('Batch', int)
    >>> Channels = NewType('Channels', int)

    >>> def add_batch_axis(x: Array[*Shape]) -> Array[Batch, *Shape]: ...
    >>> def del_batch_axis(x: Array[Batch, *Shape]) -> Array[*Shape]: ...
    >>> def add_batch_channels(
    ...   x: Array[*Shape]
    ... ) -> Array[Batch, *Shape, Channels]: ...

    >>> T = TypeVar('T')
    >>> Ts = TypeVarTuple('Ts')

    >>> def prefix_tuple(
    ...     x: T,
    ...     y: Tuple[*Ts]
    ... ) -> Tuple[T, *Ts]: ...
    Traceback (most recent call last):
        ...
    TypeError: Tuple[t0, t1, ...]: each t must be a type. Got *Ts.

``*args`` as a Type Variable Tuple

    >>> Ts = TypeVarTuple('Ts')
    >>> def args_to_tuple(*args: *Ts) -> Tuple[*Ts]: ...
    Traceback (most recent call last):
        ...
    TypeError: Tuple[t0, t1, ...]: each t must be a type. Got *Ts.

    >>> def foo(*args: Ts): ...
    >>> def foo(*args: Tuple[*Ts]): ...
    Traceback (most recent call last):
        ...
    TypeError: Tuple[t0, t1, ...]: each t must be a type. Got *Ts.

    >>> def foo(**kwargs: *Ts): ...
    Traceback (most recent call last):
        ...
    SyntaxError: invalid syntax

Type Variable Tuples with ``Callable``

    >>> from typing import Any, Callable
    >>> class Process:
    ...     def __init__(
    ...     self,
    ...     target: Callable[[*Ts], Any],
    ...     args: Tuple[*Ts]
    ... ): ...
    Traceback (most recent call last):
        ...
    TypeError: Tuple[t0, t1, ...]: each t must be a type. Got *Ts.

    >>> T = TypeVar('T')
    >>> def foo(f: Callable[[int, *Ts, T], Tuple[T, *Ts]]): ...
    Traceback (most recent call last):
        ...
    TypeError: Tuple[t0, t1, ...]: each t must be a type. Got *Ts.

Aliases
-------

    >>> IntTuple = Tuple[int, *Ts]
    Traceback (most recent call last):
        ...
    TypeError: Tuple[t0, t1, ...]: each t must be a type. Got *Ts.
    >>> NamedArray = Tuple[str, Array[*Ts]]

"""

__test__ = {'doctests' : doctests}

def test_main(verbose=False):
    from test import support
    from test import test_pep646_examples
    support.run_doctest(test_pep646_examples, verbose)

if __name__ == "__main__":
    test_main(verbose=True)
