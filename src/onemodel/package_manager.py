import os
import tomli
import shutil
from git import Repo

def install_dependencies():
    pm = PackageManager()
    pm.load_toml_file()
    pm.install_dependencies()

class PackageManager:

    def __init__(self):
        self.config = None

    def load_toml_file(self):
        with open("onemodel.toml", mode="rb") as fp:
            self.config = tomli.load(fp)

        print('Load "onemodel.toml".')

    def dependencies(self):
        return self.config["dependencies"]

    def install_dependencies(self):

        shutil.rmtree("./lib/")

        for name, url in self.dependencies().items():
            Repo.clone_from(url, f"lib/{name}")
            print(f'Installed {url} as "{name}"')

        print("All dependencies installed.")
