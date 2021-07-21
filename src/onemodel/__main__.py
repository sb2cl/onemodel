if __name__ == '__main__':
    from onemodel import interpreter
    from onemodel.utils.setup_input_history import setup_input_history

    setup_input_history()

    while True:
        text = input('onemodel > ')
        if text.strip() == "": continue

        result, error = interpreter.run('<stdin>', text)
        
        if error:
            print(error.as_string())
        elif result:
            if len(result.elements) == 1:
                print(repr(result.elements[0]))
            else:
                print(repr(result))
