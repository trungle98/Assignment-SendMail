import logging


class Logger(object):
    def __init__(self):
        print('Logger initialized')
    @staticmethod
    def log():
        logging.basicConfig(filename="log.log",
                            format='%(asctime)s %(message)s',
                            filemode='a')
        return logging.getLogger()

    @staticmethod
    def error_log(msg):
        logging.basicConfig(filename="error_log.log",
                            format='%(asctime)s %(message)s',
                            filemode='a')
        return logging.getLogger().error(msg)