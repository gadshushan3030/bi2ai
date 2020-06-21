from os import getenv


class Environment:
    _bi2ai_env = None

    def __init__(self, env=None):
        if env is None and getenv('BI2AI_ENV') is not None:
            self._bi2ai_env = getenv('BI2AI_ENV').lower()
        else:
            self._bi2ai_env = env

    def get_env(self):
        return self._bi2ai_env
