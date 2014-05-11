from lispy import lexer


def test_empty_list():
    tokens = list(lexer.tokenize('()'))
    assert tokens == [(lexer.open_parenthesis, '('),
                      (lexer.close_parenthesis, ')')]


def test_empty_list_with_whitespace():
    tokens = list(lexer.tokenize('( \t\n)'))
    assert tokens == [(lexer.open_parenthesis, '('),
                      (lexer.close_parenthesis, ')')]


def test_number_list():
    tokens = list(lexer.tokenize('(11 22 33)'))
    assert tokens == [(lexer.open_parenthesis, '('),
                      (lexer.number, '11'),
                      (lexer.number, '22'),
                      (lexer.number, '33'),
                      (lexer.close_parenthesis, ')')]


def test_sum():
    tokens = list(lexer.tokenize('(+ 1 1)'))
    assert tokens == [(lexer.open_parenthesis, '('),
                      (lexer.symbol, '+'),
                      (lexer.number, '1'),
                      (lexer.number, '1'),
                      (lexer.close_parenthesis, ')')]


def test_symbol():
    tokens = list(lexer.tokenize('(abc xyz)'))
    assert tokens == [(lexer.open_parenthesis, '('),
                      (lexer.symbol, 'abc'),
                      (lexer.symbol, 'xyz'),
                      (lexer.close_parenthesis, ')')]


def test_quoted_word():
    tokens = list(lexer.tokenize("'abc"))
    assert tokens == [(lexer.quote, "'"),
                      (lexer.symbol, 'abc')]


def test_quotee_list():
    tokens = list(lexer.tokenize("'(abc 123)"))
    assert tokens == [(lexer.quote, "'"),
                      (lexer.open_parenthesis, '('),
                      (lexer.symbol, 'abc'),
                      (lexer.number, '123'),
                      (lexer.close_parenthesis, ')')]


def test_nested_list():
    tokens = list(lexer.tokenize('(zip (abc xyz) (11 22))'))
    assert tokens == [(lexer.open_parenthesis, '('),
                      (lexer.symbol, 'zip'),
                      (lexer.open_parenthesis, '('),
                      (lexer.symbol, 'abc'),
                      (lexer.symbol, 'xyz'),
                      (lexer.close_parenthesis, ')'),
                      (lexer.open_parenthesis, '('),
                      (lexer.number, '11'),
                      (lexer.number, '22'),
                      (lexer.close_parenthesis, ')'),
                      (lexer.close_parenthesis, ')')]
