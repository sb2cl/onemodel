import unittest
from parser_ import Parser
from tokens import Token, TokenType

class TestParser(unittest.TestCase):

    def test_empty(self):
        result = [
                Token(TokenType.END_OF_FILE)
                ]

        parser = Parser(result)
        res = parser.parse()

        self.assertEqual(res.node, None)
