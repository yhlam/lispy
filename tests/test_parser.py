import pytest

from lispy.lexer import (number, symbol, quote,
                         open_parenthesis, close_parenthesis)
from lispy.parser import (parse, List, Quotation, Number, Symbol)


def test_empty_list():
    ast = parse([(open_parenthesis, '('), (close_parenthesis, ')')])
    assert ast == List([])


def test_number_list():
    ast = parse([(quote, "'"),
                 (open_parenthesis, '('),
                 (number, '11'),
                 (number, '22'),
                 (number, '33'),
                 (close_parenthesis, ')')])
    assert ast == Quotation(List([Number(11), Number(22), Number(33)]))


def test_sum():
    ast = parse([(open_parenthesis, '('),
                 (symbol, '+'),
                 (number, '1'),
                 (number, '1'),
                 (close_parenthesis, ')')])
    assert ast == List([Symbol('+'), Number(1), Number(1)])


def test_symbol():
    ast = parse([(open_parenthesis, '('),
                 (symbol, 'abc'),
                 (symbol, 'xyz'),
                 (close_parenthesis, ')')])
    assert ast == List([Symbol('abc'), Symbol('xyz')])


def test_quote_word():
    ast = parse([(quote, "'"), (symbol, 'abc')])
    assert ast == Quotation(Symbol('abc'))


def test_quote_list():
    ast = parse([(quote, "'"),
                 (open_parenthesis, '('),
                 (symbol, 'abc'),
                 (number, '123'),
                 (close_parenthesis, ')')])
    assert ast == Quotation(List([Symbol('abc'), Number(123)]))


def test_nested_list():
    ast = parse([(open_parenthesis, '('),
                 (symbol, 'zip'),
                 (open_parenthesis, '('),
                 (symbol, 'abc'),
                 (symbol, 'xyz'),
                 (close_parenthesis, ')'),
                 (quote, "'"),
                 (open_parenthesis, '('),
                 (number, '11'),
                 (number, '22'),
                 (close_parenthesis, ')'),
                 (close_parenthesis, ')')])
    assert ast == List([Symbol('zip'),
                        List([Symbol('abc'), Symbol('xyz')]),
                        Quotation(List([Number(11), Number(22)]))])


def test_multiple_expr():
    with pytest.raises(SyntaxError):
        parse([(number, '11'),
               (number, '22'),
               (number, '33')])


def test_no_open_parenthesis():
    with pytest.raises(SyntaxError):
        parse([(symbol, '+'),
               (number, '1'),
               (number, '1'),
               (close_parenthesis, ')')])


def test_no_close_parenthesis():
    with pytest.raises(SyntaxError):
        parse([(open_parenthesis, '('),
               (symbol, '+'),
               (number, '1'),
               (number, '1')])
