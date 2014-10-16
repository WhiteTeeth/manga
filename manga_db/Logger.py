# coding=utf-8
__author__ = 'BaiYa'

import logging
import logging.config

init = False
if not init:
    logging.config.fileConfig("logging.conf")
    init = True
logger = logging.getLogger('root')
fileLogger = logging.getLogger('file')

def debug(msg):
    logger.debug(msg)
    fileLogger.debug(msg)

def info(msg):
    logger.info(msg)
    fileLogger.info(msg)

def warn(msg):
    logger.warning(msg)
    fileLogger.warning(msg)

def error(msg):
    logger.error(msg)
    fileLogger.error(msg)

def critical(msg):
    logger.critical(msg)
    fileLogger.critical(msg)

if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warn message")
    logger.error("error message")
    logger.critical("critical message")
