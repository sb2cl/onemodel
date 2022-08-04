import sys

from onemodel.repl import Repl
from onemodel.onemodel_walker import load_file

def main():
    if len( sys.argv ) > 1:
        filename = sys.argv[1]
        onemodel = load_file(filename)
        sbml = onemodel.get_SBML_string()
        print(sbml)

    else:
        repl = Repl()
        repl.run()

if __name__ == "__main__":
    main()
