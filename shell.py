from lexer import Lexer
from parser_ import Parser
from interpreter import Interpreter

while True:
    text = input('basic > ')
    if text.strip() == "": continue

    lexer = Lexer('<stdin>', text)
    result,error = lexer.generate_tokens()

    parser = Parser(result)
    res = parser.parse()


    if res.error:
        print(res.error.as_string())

    if not res.node: continue

    interpreter = Interpreter()
    value = interpreter.visit(res.node)
    print(value)
