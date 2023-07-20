import logging

DefaultLogger = logging.getLogger('__main__')
DefaultLogger.addHandler(logging.StreamHandler())
DefaultLogger.setLevel(logging.INFO)
