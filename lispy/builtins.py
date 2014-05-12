from collections import ChainMap
from functools import reduce

from lispy.parser import Number, Symbol, List
from lispy.evaluator import macro, evaluate


def eq(args):
    a, b = args
    return a == b


def cons(args):
    head, tail = args
    return List([head] + tail.elements)


def car(args):
    list_, = args
    return list_.elements[0]


def cdr(args):
    list_, = args
    return List(list_.elements[1:])


@macro
def atom(vars_, args):
    arg, = args
    return arg.__class__ in (Number, Symbol)


@macro
def define(vars_, args):
    name, ast = args
    identifier = name.identifier
    value = evaluate(ast, vars_)
    vars_[identifier] = value


@macro
def func(vars_, args):
    arglist, definition = args
    arglist = arglist.elements

    def f(fargs):
        locals_ = {sym.identifier: arg for sym, arg in zip(arglist, fargs)}
        envs = ChainMap(locals_, vars_)
        return evaluate(definition, envs)

    return f


@macro
def cond(vars_, args):
    for arg in args:
        condition, expr = arg.elements
        if evaluate(condition, vars_):
            return evaluate(expr, vars_)


default = True


def add(args):
    return reduce(lambda a, b: Number(a.value + b.value), args, Number(0))


def minus(args):
    a, b = args
    return Number(a.value - b.value)


def mult(args):
    return reduce(lambda a, b: Number(a.value * b.value), args, Number(1))


def div(args):
    a, b = args
    return Number(a.value / b.value)
