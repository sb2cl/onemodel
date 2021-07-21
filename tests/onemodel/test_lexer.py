from onemodel.tokens import Token, TokenType
from onemodel.lexer import Lexer

def test_empty():
    tokens, error = list(Lexer('<stdin>',"").generate_tokens())
    assert tokens == [Token(TokenType.END_OF_FILE)]

def test_whitespace():
    tokens, error = list(Lexer('<stdin>'," \t  \t\t").generate_tokens())
    assert tokens == [Token(TokenType.END_OF_FILE)]

def test_comment():
    tokens, error = list(Lexer('<stdin>',"# This is a comment").generate_tokens())
    assert tokens == [Token(TokenType.END_OF_FILE)]

def test_newline():
    tokens, error = list(Lexer('<stdin>',";\n").generate_tokens())
    assert tokens == [
            Token(TokenType.NEW_LINE),
            Token(TokenType.NEW_LINE),
            Token(TokenType.END_OF_FILE)
            ]

def test_numbers():
    tokens, error = list(Lexer('<stdin>',"123 123.456 123. .456 .").generate_tokens())
    assert tokens == [
            Token(TokenType.NUMBER, 123),
            Token(TokenType.NUMBER, 123.456),
            Token(TokenType.NUMBER, 123.0),
            Token(TokenType.NUMBER, 0.456),
            Token(TokenType.NUMBER, 0.0),
            Token(TokenType.END_OF_FILE)
            ]

def test_string():
    tokens, error = list(Lexer('<stdin>',"\"asdf\"").generate_tokens())
    assert tokens == [
        Token(TokenType.STRING, "asdf"),
        Token(TokenType.END_OF_FILE),
        ]

def test_identifier():
    tokens, error = list(Lexer('<stdin>',"asdf_1234_ VAR").generate_tokens())
    assert tokens == [
        Token(TokenType.IDENTIFIER, "asdf_1234_"),
        Token(TokenType.KEYWORD, "VAR"),
        Token(TokenType.END_OF_FILE),
        ]

def test_operators():
    tokens, error = list(Lexer('<stdin>',"+-*/^===!=<<=>>=,").generate_tokens())
    assert tokens == [
        Token(TokenType.PLUS),
        Token(TokenType.MINUS),
        Token(TokenType.MULTIPLICATION),
        Token(TokenType.DIVISION),
        Token(TokenType.POWER),
        Token(TokenType.IS_EQUAL),
        Token(TokenType.EQUAL),
        Token(TokenType.NOT_EQUAL),
        Token(TokenType.LESS_THAN),
        Token(TokenType.LESS_EQUAL_THAN),
        Token(TokenType.GREATER_THAN),
        Token(TokenType.GREATER_EQUAL_THAN),
        Token(TokenType.COMMA),
        Token(TokenType.END_OF_FILE),
        ]

def test_parens():
    tokens, error = list(Lexer('<stdin>',"()[]").generate_tokens())
    assert tokens == [
        Token(TokenType.LEFT_PAREN),
        Token(TokenType.RIGHT_PAREN),
        Token(TokenType.LEFT_SQUARE),
        Token(TokenType.RIGHT_SQUARE),
        Token(TokenType.END_OF_FILE),
        ]

def test_all():
    tokens, error = list(Lexer('<stdin>',"27 + (43 / 36 - 48) * 51").generate_tokens())
    assert tokens == [
        Token(TokenType.NUMBER, 27),
        Token(TokenType.PLUS),
        Token(TokenType.LEFT_PAREN),
        Token(TokenType.NUMBER, 43),
        Token(TokenType.DIVISION),
        Token(TokenType.NUMBER, 36),
        Token(TokenType.MINUS),
        Token(TokenType.NUMBER, 48),
        Token(TokenType.RIGHT_PAREN),
        Token(TokenType.MULTIPLICATION),
        Token(TokenType.NUMBER, 51),
        Token(TokenType.END_OF_FILE),
        ]
