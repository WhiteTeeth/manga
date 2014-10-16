# coding=utf-8
__author__ = 'BaiYa'

import logging
import logging.config

if __name__ != '__main__':

    logger = logging.getLogger()
    #set loghandler
    file = logging.FileHandler("qqxml.log")
    logger.addHandler(file)
    #set console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    console.setFormatter(formatter)
    logger.addHandler(console)

    #set formater
    #formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    file.setFormatter(formatter)
    #set log level
    logger.setLevel(logging.NOTSET)

if __name__ == '__main__':
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger("main")

    logger.setLevel(logging.DEBUG)
    logger.debug("debug message")
    logger.info("info message")
    logger.warn("warn message")
    logger.error("error message")
    logger.critical("critical message")

    # for i in range(0,10):
    #     logger.info(str(i))