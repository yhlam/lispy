from collections import deque

from .reglang import Single, Union, Con, KleeneStar, char_range, union_char


__all__ = ['number', 'symbol', 'quote', 'open_parenthesis',
           'close_parenthesis', 'whitespace', 'token_classes', 'tokenize']


class TokenClass:
    def __init__(self, name, fa):
        self.name = name
        self.fa = fa

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name


digit = char_range('0', '9')
alphabet = Union(char_range('a', 'z'),
                 char_range('A', 'Z'),
                 union_char('?_+-*/'))

number = TokenClass('number', KleeneStar(digit))
symbol = TokenClass('symbol',
                    Con(alphabet, KleeneStar(Union(digit, alphabet))))
quote = TokenClass('quote', Single("'"))
open_parenthesis = TokenClass('open_parenthesis', Single('('))
close_parenthesis = TokenClass('close_parenthesis', Single(')'))
whitespace = TokenClass('whitespace', KleeneStar(union_char(' \t\n')))


token_classes = [number, symbol, quote, open_parenthesis,
                 close_parenthesis, whitespace]


def tokenize(code):
    while code:
        cont = [(token_class, token_class.fa.start_state)
                for token_class in token_classes]
        accept = None

        for i, char in enumerate(code, 1):
            next_cont = deque()
            for token_cls, state in cont:
                next_state = token_cls.fa.next(state, char)
                if next_state is not None:
                    next_cont.append((token_cls, next_state))
                    if next_state.is_final:
                        accept = (i, token_cls)

            if next_cont:
                cont = next_cont
            else:
                break

        if accept is None:
            raise ValueError()
        else:
            i, token_cls = accept
            token = code[:i]
            code = code[i:]
            yield token_cls, token
