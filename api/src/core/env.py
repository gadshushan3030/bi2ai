from os import getenv

if getenv('PY_ENV') is not None:
    BI2AI_ENV = getenv('BI2AI_ENV').lower()
else:
    BI2AI_ENV = 'dev'


