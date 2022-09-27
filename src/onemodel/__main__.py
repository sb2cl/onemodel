import sys

from onemodel.repl import Repl
from onemodel.onemodel_walker import load_file
from onemodel.package_manager import PackageManager

def main():
    if len( sys.argv ) > 1:
        cmd = sys.argv[1]

        if cmd == "run":
            filename = sys.argv[2]
            onemodel = load_file(filename)
            sbml = onemodel.get_SBML_string()
            print(sbml)

        if cmd == "install":
            pm = PackageManager()
            pm.load_toml_file()
            pm.install_dependencies()

            print("Installed dependencies")

    else:
        repl = Repl()
        repl.run()

if __name__ == "__main__":
    main()
