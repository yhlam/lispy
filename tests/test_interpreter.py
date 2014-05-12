from lispy.interpreter import Interpreter
from lispy.parser import List, Number


def test_eq():
    interpreter = Interpreter()
    assert interpreter.interpret('(eq? 1 1)')
    assert not interpreter.interpret('(eq? 1 2)')
    assert interpreter.interpret('(eq? (+ 1 1) 2)')


def test_cons():
    interpreter = Interpreter()
    assert interpreter.interpret("(cons 1 '())") == List([1])
    assert interpreter.interpret("(cons 1 (cons 2 '()))") == List([1, 2])


def test_car():
    interpreter = Interpreter()
    assert interpreter.interpret("(car '(1))") == Number(1)
    assert interpreter.interpret("(car '(1 2))") == Number(1)


def test_cdr():
    interpreter = Interpreter()
    assert interpreter.interpret("(cdr '(1))") == List([])
    assert interpreter.interpret("(cdr '(1 2))") == List([Number(2)])
    tail = interpreter.interpret("(cdr '(1 2 3))")
    assert tail == List([Number(2), Number(3)])


def test_atom():
    interpreter = Interpreter()
    assert interpreter.interpret("(atom? 1)")
    assert interpreter.interpret("(atom? x)")
    assert not interpreter.interpret("(atom? (1 2))")
    assert not interpreter.interpret("(atom? '1)")
    assert not interpreter.interpret("(atom? 'x)")
    assert not interpreter.interpret("(atom? '(1 2))")


def test_define():
    interpreter = Interpreter()
    interpreter.interpret('(define x 1)')
    assert interpreter.interpret('x') == 1


def test_func():
    interpreter = Interpreter()
    interpreter.interpret('(define square (func (x) (* x x)))')
    assert interpreter.interpret('(square 5)') == 25


def test_cond():
    interpreter = Interpreter()
    value = interpreter.interpret('(cond ((eq? 1 1) 1)'
                                  '      (default 2))')
    assert value == 1

    value = interpreter.interpret('(cond ((eq? 1 2) 1)'
                                  '      (default 2))')
    assert value == 2

    value = interpreter.interpret('(cond ((eq? 1 2) 1)'
                                  '      ((eq? 1 3) 2)'
                                  '      (default 3))')
    assert value == 3


def test_add():
    interpreter = Interpreter()
    assert interpreter.interpret('(+)') == 0
    assert interpreter.interpret('(+ 1)') == 1
    assert interpreter.interpret('(+ 1 2)') == 3
    assert interpreter.interpret('(+ 1 2 3)') == 6


def test_minus():
    interpreter = Interpreter()
    assert interpreter.interpret('(- 2 1)') == 1
    assert interpreter.interpret('(- 6 4)') == 2


def test_mult():
    interpreter = Interpreter()
    assert interpreter.interpret('(*)') == 1
    assert interpreter.interpret('(* 1)') == 1
    assert interpreter.interpret('(* 1 2)') == 2
    assert interpreter.interpret('(* 1 2 3)') == 6


def test_div():
    interpreter = Interpreter()
    assert interpreter.interpret('(/ 6 3)') == 2
