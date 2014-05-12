from lispy.builtins import (eq, cons, car, cdr, atom, define, func, cond,
                            add, minus, mult, div, default)
from lispy.evaluator import evaluate
from lispy.lexer import tokenize
from lispy.parser import parse


class Interpreter:
    def __init__(self):
        self.vars_ = {
            'eq?': eq,
            'cons': cons,
            'car': car,
            'cdr': cdr,
            'atom?': atom,
            'define': define,
            'func': func,
            'cond': cond,
            'default': default,
            '+': add,
            '-': minus,
            '*': mult,
            '/': div
        }

    def interpret(self, expr):
        tokens = tokenize(expr)
        ast = parse(tokens)
        value = evaluate(ast, self.vars_)
        return value
