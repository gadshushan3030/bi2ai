from os import getenv

'''
    Package name: Environment
    Package name space: core
    Package description: Cross platform environment manager
    Package version: 1.0.0
    Package author: Israel Vainberg
'''


class Environment:
    _bi2ai_env = None

    def __init__(self, env=None):
        if env is None and getenv('BI2AI_ENV') is not None:
            self._bi2ai_env = getenv('BI2AI_ENV').lower()
        else:
            self._bi2ai_env = env

    def get_env(self):
        return self._bi2ai_env
