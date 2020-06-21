import os
import importlib

'''
    Package name: Import
    Package name space: core
    Package description: Dynamic module loader (bound to a name space)
    Package version: 1.0.0
    Package author: Israel Vainberg
'''


class Import:
    _namespace = 'com.biai'

    def __init__(self, namespace=None):
        self.namespace = namespace
        if self.namespace is None:
            self.namespace = self._namespace
        self.abs_path = os.path.dirname(os.path.realpath(__file__))

    def load_module(self, module_name, class_name=None):
        module_object = importlib.import_module(f"{self.namespace}.{module_name}.main")
        if class_name is not None:
            return getattr(module_object, class_name)
        return module_object
