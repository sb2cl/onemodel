import unittest
from tokens import Token, TokenType
from lexer import Lexer

class TestLexer(unittest.TestCase):
    
    def test_empty(self):
        tokens, error = list(Lexer('<stdin>',"").generate_tokens())
        self.assertEqual(tokens, [Token(TokenType.END_OF_FILE)])
    
    def test_whitespace(self):
        tokens, error = list(Lexer('<stdin>'," \t\n  \t\t\n\n").generate_tokens())
        self.assertEqual(tokens, [Token(TokenType.END_OF_FILE)])

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
    
    def test_operators(self):
        tokens, error = list(Lexer('<stdin>',"+-*/").generate_tokens())
        self.assertEqual(tokens, [
            Token(TokenType.PLUS),
            Token(TokenType.MINUS),
            Token(TokenType.MULTIPLICATION),
            Token(TokenType.DIVISION),
            Token(TokenType.END_OF_FILE),
        ])

    def test_parens(self):
        tokens, error = list(Lexer('<stdin>',"()").generate_tokens())
        self.assertEqual(tokens, [
            Token(TokenType.LEFT_PAREN),
            Token(TokenType.RIGHT_PAREN),
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
