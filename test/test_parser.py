import unittest
from parser_ import Parser
from tokens import Token, TokenType
from nodes import *

class TestParser(unittest.TestCase):

    def test_empty(self):
        tokens = [
                Token(TokenType.END_OF_FILE)
                ]

        parser = Parser(tokens)
        res = parser.parse()

        self.assertEqual(res.node, None)

    def test_factor(self):
        tokens = [
                Token(TokenType.NUMBER,1),
                Token(TokenType.END_OF_FILE)
                ]

        parser = Parser(tokens)
        res = parser.parse()

        self.assertEqual(res.node, 
            NumberNode(Token(TokenType.NUMBER,1))
            )



