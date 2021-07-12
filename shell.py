from lexer import Lexer
from tokens import *

while True:
    text = input('basic > ')
    if text.strip() == "": continue

    lexer = Lexer('<stdin>', text)
    result,error = lexer.generate_tokens()

    if error:
        print(error.as_string())
    elif result:
        print(result)

	#result, error = basic.run('<stdin>', text)

	#if error:
	#	print(error.as_string())
	#elif result:
	#	if len(result.elements) == 1:
	#		print(repr(result.elements[0]))
	#	else:
	#		print(repr(result))
