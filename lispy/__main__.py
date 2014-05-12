import traceback

from .interpreter import Interpreter


if __name__ == '__main__':
    interpreter = Interpreter()
    while True:
        try:
            expr = input('>>> ')
            value = interpreter.interpret(expr)
            print(value)
        except KeyboardInterrupt:
            break
        except Exception:
            traceback.print_exc()
