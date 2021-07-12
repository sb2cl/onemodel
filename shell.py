from lexer import Lexer
from parser_ import Parser

while True:
    text = input('basic > ')
    if text.strip() == "": continue

    lexer = Lexer('<stdin>', text)
    result,error = lexer.generate_tokens()

    parser = Parser(result)
    res = parser.parse()

    if res.error:
        print(res.error.as_string())
    elif res.node:
        print(res.node)

	#result, error = basic.run('<stdin>', text)

	#if error:
	#	print(error.as_string())
	#elif result:
	#	if len(result.elements) == 1:
	#		print(repr(result.elements[0]))
	#	else:
	#		print(repr(result))
