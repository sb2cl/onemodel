import unittest
from onemodel.tokens import Token, TokenType
from onemodel.lexer import Lexer

class TestLexer(unittest.TestCase):
    
    def test_empty(self):
        tokens, error = list(Lexer('<stdin>',"").generate_tokens())
        self.assertEqual(tokens, [Token(TokenType.END_OF_FILE)])
    
    def test_whitespace(self):
        tokens, error = list(Lexer('<stdin>'," \t  \t\t").generate_tokens())
        self.assertEqual(tokens, [Token(TokenType.END_OF_FILE)])

    def test_comment(self):
        tokens, error = list(Lexer('<stdin>',"# This is a comment").generate_tokens())
        self.assertEqual(tokens, [Token(TokenType.END_OF_FILE)])

    def test_newline(self):
        tokens, error = list(Lexer('<stdin>',";\n").generate_tokens())
        self.assertEqual(tokens, [
            Token(TokenType.NEW_LINE),
            Token(TokenType.NEW_LINE),
            Token(TokenType.END_OF_FILE),
            ])

    def test_numbers(self):
        tokens, error = list(Lexer('<stdin>',"123 123.456 123. .456 .").generate_tokens())

        self.assertEqual(tokens, [
            Token(TokenType.NUMBER, 123),
            Token(TokenType.NUMBER, 123.456),
            Token(TokenType.NUMBER, 123.0),
            Token(TokenType.NUMBER, 0.456),
            Token(TokenType.NUMBER, 0.0),
            Token(TokenType.END_OF_FILE),
        ])

    def test_string(self):
        tokens, error = list(Lexer('<stdin>',"\"asdf\"").generate_tokens())

        self.assertEqual(tokens, [
            Token(TokenType.STRING, "asdf"),
            Token(TokenType.END_OF_FILE),
        ])

    def test_identifier(self):
        tokens, error = list(Lexer('<stdin>',"asdf_1234_ VAR").generate_tokens())

        self.assertEqual(tokens, [
            Token(TokenType.IDENTIFIER, "asdf_1234_"),
            Token(TokenType.KEYWORD, "VAR"),
            Token(TokenType.END_OF_FILE),
        ])
    
    def test_operators(self):
        tokens, error = list(Lexer('<stdin>',"+-*/^===!=<<=>>=,").generate_tokens())
        self.assertEqual(tokens, [
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
        ])

    def test_parens(self):
        tokens, error = list(Lexer('<stdin>',"()[]").generate_tokens())
        self.assertEqual(tokens, [
            Token(TokenType.LEFT_PAREN),
            Token(TokenType.RIGHT_PAREN),
            Token(TokenType.LEFT_SQUARE),
            Token(TokenType.RIGHT_SQUARE),
            Token(TokenType.END_OF_FILE),
        ])
    
    def test_all(self):
        tokens, error = list(Lexer('<stdin>',"27 + (43 / 36 - 48) * 51").generate_tokens())
        self.assertEqual(tokens, [
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
        ])
