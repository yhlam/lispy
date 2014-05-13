from collections import namedtuple

from .lexer import number, symbol, quote, open_parenthesis, close_parenthesis


__all__ = ['List', 'Quotation', 'Number', 'Symbol', 'parse']


class List(namedtuple('List', 'elements')):
    def __str__(self):
        return '({})'.format(' '.join(str(elem) for elem in self.elements))


class Quotation(namedtuple('Quotation', 'expr')):
    def __str__(self):
        return "'" + str(self.expr)


class Number(namedtuple('Number', 'value')):
    def __str__(self):
        return str(self.value)


class Symbol(namedtuple('Symbol', 'identifier')):
    def __str__(self):
        return str(self.identifier)


def parse(tokens):
    token_iter = iter(tokens)
    expr = [_parse_next(token_cls, token, token_iter)
            for token_cls, token in token_iter]

    if len(expr) > 1:
        raise SyntaxError('Multiple expressions but not wrapped in list')

    return expr[0]


def _parse_number(token, tail):
    return Number(int(token))


def _parse_symbol(token, tail):
    return Symbol(token)


def _parse_quotation(token, tail):
    token_cls, token = next(tail)
    expr = _parse_next(token_cls, token, tail)
    return Quotation(expr)


def _parse_list(token, tail):
    elements = []

    for token_cls, token in tail:
        if token_cls == close_parenthesis:
            break
        expr = _parse_next(token_cls, token, tail)
        elements.append(expr)
    else:
        raise SyntaxError('Unmatched open parenthesis')

    return List(elements)


_parsers = {
    number: _parse_number,
    symbol: _parse_symbol,
    quote: _parse_quotation,
    open_parenthesis: _parse_list
}


def _parse_next(token_cls, token, tail):
    parser = _parsers.get(token_cls)
    if not parser:
        raise SyntaxError('Encounter unexpected token: {}'.format(token))
    return parser(token, tail)
