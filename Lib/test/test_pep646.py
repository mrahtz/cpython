doctests = """

Setup

    >>> class A:
    ...     def __class_getitem__(cls, x):
    ...         return x
    >>> class B:
    ...     def __iter__(self):
    ...         yield StarredB()
    ...     def __repr__(self):
    ...         return "B"
    >>> class StarredB:
    ...     def __repr__(self):
    ...         return "StarredB"
    >>> b = B()

Slices that are supposed to work, starring our custom B class

    >>> A[*b]
    (StarredB,)
    >>> A[*b, *b]
    (StarredB, StarredB)
    >>> A[b, *b]
    (B, StarredB)
    >>> A[*b, b]
    (StarredB, B)
    >>> A[b, b, *b]
    (B, B, StarredB)
    >>> A[*b, b, b]
    (StarredB, B, B)
    >>> A[b, *b, b]
    (B, StarredB, B)
    >>> A[b, b, *b, b]
    (B, B, StarredB, B)
    >>> A[b, *b, b, b]
    (B, StarredB, B, B)

Slices that are supposed to work, starring a list

    >>> l = [1, 2, 3]
    >>> A[*l]
    (1, 2, 3)
    >>> A[*l, 4]
    (1, 2, 3, 4)
    >>> A[0, *l]
    (0, 1, 2, 3)

Slices that are supposed to work, starring a tuple

    >>> t = (1, 2, 3)
    >>> A[*t]
    (1, 2, 3)
    >>> A[*t, 4]
    (1, 2, 3, 4)
    >>> A[0, *t]
    (0, 1, 2, 3)

Starring an expression (rather than a name) in a slice

    >>> def returns_list():
    ...     return [1, 2, 3]
    >>> A[returns_list()]
    [1, 2, 3]
    >>> A[returns_list(), 4]
    ([1, 2, 3], 4)
    >>> A[*returns_list()]
    (1, 2, 3)
    >>> A[*returns_list(), 4]
    (1, 2, 3, 4)
    >>> A[0, *returns_list()]
    (0, 1, 2, 3)
    >>> A[*returns_list(), *returns_list()]
    (1, 2, 3, 1, 2, 3)

Slices that should fail

    >>> A[:*b]
    Traceback (most recent call last):
        ...
    SyntaxError: invalid syntax
    >>> A[*b:]
    Traceback (most recent call last):
        ...
    SyntaxError: invalid syntax
    >>> A[*b:*b]
    Traceback (most recent call last):
        ...
    SyntaxError: invalid syntax
    >>> A[**b]
    Traceback (most recent call last):
        ...
    SyntaxError: invalid syntax

*args annotated as starred expression

    >>> def foo(*args: *b): pass
    >>> foo.__annotations__
    {'args': (StarredB,)}

Other uses of starred expressions as annotations should fail

    >>> def foo(x: *b): pass
    Traceback (most recent call last):
        ...
    SyntaxError: invalid syntax
    >>> x: *b
    Traceback (most recent call last):
        ...
    SyntaxError: invalid syntax

"""

__test__ = {'doctests' : doctests}

def test_main(verbose=False):
    from test import support
    from test import test_pep646
    support.run_doctest(test_pep646, verbose)

if __name__ == "__main__":
    test_main(verbose=True)
