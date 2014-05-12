import pytest

from lispy.parser import Number, List, Quotation, Symbol
from lispy.evaluator import ismacro
from lispy.builtins import (eq, cons, car, cdr, atom, define, func, cond,
                            add, minus, mult, div, default)


def test_eq():
    assert eq([1, 1])
    assert not eq([1, 2])


def test_cons():
    assert cons([1, List([])]) == List([1])
    list_ = cons([1, cons([2, List([])])])
    assert list_ == List([1, 2])


def test_car():
    assert car([List([Number(1)])]) == Number(1)
    assert car([List([Number(1), Number(2)])]) == Number(1)

    with pytest.raises(IndexError):
        car([List([])])


def test_cdr():
    assert cdr([List([Number(1)])]) == List([])
    assert cdr([List([Number(1), Number(2)])]) == List([Number(2)])
    tail = cdr([List([Number(1), Number(2), Number(3)])])
    assert tail == List([Number(2), Number(3)])


def test_atom():
    assert ismacro(atom)
    assert atom({}, [Number(1)])
    assert atom({}, [Symbol('x')])
    assert not atom({}, [List([Number(1), Number(2)])])
    assert not atom({}, [Quotation(Number(1))])
    assert not atom({}, [Quotation(Symbol('x'))])
    assert not atom({}, [Quotation(List([Number(1), Number(2)]))])


def test_define():
    assert ismacro(define)

    def test(ast, expected, vars_=None):
        vars_ = {} if vars_ is None else vars_
        define(vars_, [Symbol('x'), ast])
        assert vars_['x'] == expected

    test(Symbol('y'), 1, {'y': 1})
    test(Number(1), Number(1))
    test(List([Symbol('+'), Number(1), Number(2)]), Number(3),
         {'+': lambda args: Number(args[0].value + args[1].value)})
    test(Quotation(Symbol('x')), Symbol('x'))
    test(Quotation(Number(1)), Number(1))
    test(Quotation(List([Number(1), Number(2)])), List([Number(1), Number(2)]))


def test_func():
    assert ismacro(func)

    square = func({'*': lambda args: Number(args[0].value * args[1].value)},
                  [List([Symbol('x')]),
                   List([Symbol('*'), Symbol('x'), Symbol('x')])])
    assert square([Number(5)]) == Number(25)


def test_cond():
    assert ismacro(cond)

    value = cond({'True': True,
                  'default': default},
                 [List([Symbol('True'), Number(1)]),
                  List([Symbol('default'), Number(2)])])
    assert value == Number(1)

    value = cond({'False': False,
                  'default': default},
                 [List([Symbol('False'), Number(1)]),
                  List([Symbol('default'), Number(2)])])
    assert value == Number(2)

    value = cond({'False': False,
                  'default': default},
                 [List([Symbol('False'), Number(1)]),
                  List([Symbol('False'), Number(2)]),
                  List([Symbol('default'), Number(3)])])
    assert value == Number(3)


def test_add():
    assert add([]) == Number(0)
    assert add([Number(1)]) == Number(1)
    assert add([Number(1), Number(2)]) == Number(3)
    assert add([Number(1), Number(2), Number(3)]) == Number(6)


def test_minus():
    assert minus([Number(2), Number(1)]) == Number(1)


def test_mult():
    assert mult([]) == Number(1)
    assert mult([Number(1)]) == Number(1)
    assert mult([Number(1), Number(2)]) == Number(2)
    assert mult([Number(1), Number(2), Number(3)]) == Number(6)


def test_div():
    assert div([Number(6), Number(3)]) == Number(2)
