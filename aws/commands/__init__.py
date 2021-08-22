import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(filename='mainLog.txt')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s %(thread)d %(threadName)s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
