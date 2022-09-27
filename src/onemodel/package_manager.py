import tomli

class PackageManager:

    def __init__(self):
        self.config = None

    def load_toml_file(self):
        with open("onemodel.toml", mode="rb") as fp:
            self.config = tomli.load(fp)

    def dependencies(self):
        return self.config["dependencies"]
