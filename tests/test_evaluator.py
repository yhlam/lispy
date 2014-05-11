from functools import reduce

from lispy.parser import List, Quotation, Number, Symbol
from lispy.evaluator import evaluate, macro, ismacro


def test_number():
    value = evaluate(Number(123), {})
    assert value == 123


def test_number_list():
    value = evaluate(Quotation(List([Number(11), Number(22), Number(33)])), {})
    assert value == List([Number(11), Number(22), Number(33)])


def test_quote_word():
    value = evaluate(Quotation(Symbol('abc')), {})
    assert value == Symbol('abc')


def test_sum():
    vars_ = {'+': lambda numbers: reduce(lambda a, b: a + b, numbers, 0)}
    value = evaluate(List([Symbol('+'), Number(1), Number(1), Number(1)]),
                     vars_)
    assert value == 3


def test_nested_evaluation():
    vars_ = {
        '+': lambda numbers: reduce(lambda a, b: a + b, numbers, 0),
        '*': lambda numbers: reduce(lambda a, b: a * b, numbers, 1),
    }
    value = evaluate(List([Symbol('+'),
                           List([Symbol('*'),
                                 List([Symbol('+'), Number(1), Number(1)]),
                                 List([Symbol('+'), Number(2), Number(2)]),
                                 List([Symbol('+'), Number(3), Number(3)]),
                                 ]),
                           Number(4),
                           Number(5)
                           ]),
                     vars_)
    assert value == 57


def test_macro():
    @macro
    def f():
        pass
    assert ismacro(f)


def test_macro_evaluation():
    ast = Quotation(List([Number(11), Number(22), Number(33)]))

    @macro
    def define(vars_, ast):
        name, value = ast
        vars_[name.identifier] = value
    vars_ = {'define': define}

    evaluate(List([Symbol('define'), Symbol('list'), ast]), vars_)
    assert vars_['list'] == ast
