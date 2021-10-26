# Configuration for the Logger

# Importing Libraries
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import pathlib
import logging
import sys
import os


PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent.parent
FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s —"
    "%(funcName)s:%(lineno)d - %(processName)s - %(threadName)s - %(message)s ")
LOG_DIR = PACKAGE_ROOT / 'logs'
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / 'logs'



def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    console_handler.setLevel(logging.DEBUG)
    return console_handler


def get_file_handler(logger_name='dummy'):
    file_handler = TimedRotatingFileHandler(
        LOG_FILE.as_posix() + logger_name + '.logs', when='midnight', encoding='utf-8')
    file_handler.setFormatter(FORMATTER)
    file_handler.setLevel(logging.DEBUG)
    return file_handler


def get_logger(*, logger_name):
    """Get logger with prepared handlers."""
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler(logger_name=logger_name))
    logger.propagate = True
    return logger


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'dev-0001'
    SERVER_PORT = 8083


class ProductionConfig(Config):
    DEBUG = False
    SERVER_PORT = os.environ.get('PORT', 8083)


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True