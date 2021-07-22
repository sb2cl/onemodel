if __name__ == '__main__':
    from sys import argv
    from onemodel.repl import Repl

    repl = Repl()

    # If no arguments are passed
    if len(argv) < 2:
        # Run the interpreter repl
        repl.run()
    elif argv[1] == 'lexer':
        repl.run_lexer()
    elif argv[1] == 'parser':
        repl.run_parser()
