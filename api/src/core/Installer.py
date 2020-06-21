import subprocess
import sys
import importlib


class Install:

    def __init__(self):
        pass

    def package(self, package_name, alias=None, attach=True):
        try:
            importlib.import_module(package_name)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        finally:
            if attach is True:
                if alias is None:
                    globals()[package_name] = importlib.import_module(package_name)
                else:
                    globals()[alias] = importlib.import_module(alias)
