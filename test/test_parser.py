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

    def test_individual_operations(self):
        tokens = [
                Token(TokenType.NUMBER,1),
                Token(TokenType.END_OF_FILE)
                ]
        res = Parser(tokens).parse()
        self.assertEqual(res.node, 
                NumberNode(Token(TokenType.NUMBER,1))
                )    

        tokens = [
                Token(TokenType.PLUS),
                Token(TokenType.NUMBER,1),
                Token(TokenType.END_OF_FILE)
                ]
        res = Parser(tokens).parse()
        self.assertEqual(res.node, 
                PlusNode(
                    NumberNode(Token(TokenType.NUMBER,1))
                    )
                )

        tokens = [
                Token(TokenType.MINUS),
                Token(TokenType.NUMBER,1),
                Token(TokenType.END_OF_FILE)
                ]
        res = Parser(tokens).parse()
        self.assertEqual(res.node, 
                MinusNode(
                    NumberNode(Token(TokenType.NUMBER,1))
                    )
                )

        tokens = [
                Token(TokenType.NUMBER,1),
                Token(TokenType.PLUS),
                Token(TokenType.NUMBER,2),
                Token(TokenType.END_OF_FILE)
                ]
        res = Parser(tokens).parse()
        self.assertEqual(res.node, 
                AddNode(
                    NumberNode(Token(TokenType.NUMBER,1)),
                    NumberNode(Token(TokenType.NUMBER,2))
                    )
                )

        tokens = [
                Token(TokenType.NUMBER,1),
                Token(TokenType.MINUS),
                Token(TokenType.NUMBER,2),
                Token(TokenType.END_OF_FILE)
                ]
        res = Parser(tokens).parse()
        self.assertEqual(res.node, 
                SubtractNode(
                    NumberNode(Token(TokenType.NUMBER,1)),
                    NumberNode(Token(TokenType.NUMBER,2))
                    )
                )

        tokens = [
                Token(TokenType.NUMBER,1),
                Token(TokenType.MULTIPLICATION),
                Token(TokenType.NUMBER,2),
                Token(TokenType.END_OF_FILE)
                ]
        res = Parser(tokens).parse()
        self.assertEqual(res.node, 
                MultiplyNode(
                    NumberNode(Token(TokenType.NUMBER,1)),
                    NumberNode(Token(TokenType.NUMBER,2))
                    )
                )


        tokens = [
                Token(TokenType.NUMBER,1),
                Token(TokenType.DIVISION),
                Token(TokenType.NUMBER,2),
                Token(TokenType.END_OF_FILE)
                ]
        res = Parser(tokens).parse()
        self.assertEqual(res.node, 
                DivideNode(
                    NumberNode(Token(TokenType.NUMBER,1)),
                    NumberNode(Token(TokenType.NUMBER,2))
                    )
                )

    def test_full_expr(self):
        # 27 + (43 / 36 - 48) * 51
        tokens = [
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
        res = Parser(tokens).parse()
        self.assertEqual(res.node, 
                AddNode(
                    NumberNode(Token(TokenType.NUMBER,27)),
                    MultiplyNode(
                        SubtractNode(
                            DivideNode(
                                NumberNode(Token(TokenType.NUMBER,43)),
                                NumberNode(Token(TokenType.NUMBER,36)),
                                ),
                            NumberNode(Token(TokenType.NUMBER,48))
                            ),
                        NumberNode(Token(TokenType.NUMBER,51))
                        )
                    )
                )
