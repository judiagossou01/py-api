import os
import logging
import colorlog

from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv(dotenv_path="src/.env")

def locale_setup():
    """
    Configure multiple loggers: general logs, SQLAlchemy logs, HTTP logs, and error logs.
    """

    log = logging.getLogger("PY-API")
    log.setLevel(logging.DEBUG)

    formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(levelname)s%(reset)s - [%(asctime)s] "%(method)s %(log_color)s%(path)s%(reset)s %(protocol)s" %(status)s -',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )

    # CLI logs manager
    cli_handler = logging.StreamHandler()
    cli_handler.setLevel(logging.DEBUG)
    cli_handler.setFormatter(formatter)
    log.addHandler(cli_handler)

    return log


def prod_setup():
    """
    Configure general production environment logs
    """

    # Logs directory
    log_dir = "logs"

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Logs files
    log_file=os.getenv("APP_LOG_FILE", "logs/app.log")
    sqlalchemy_log_file = os.getenv("SQLALCHEMY_LOG_FILE", "logs/sqlalchemy_logs.log")

    file_formatter = logging.Formatter(
        '[%(asctime)s] - [%(levelname)s] "%(method)s %(path)s %(protocol)s" %(status)s -',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    sqlalchemy_file_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    log = logging.getLogger("PY-API")
    log.setLevel(logging.INFO)

    # Application logs manager
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=3
    )
    file_handler.setFormatter(file_formatter)
    log.addHandler(file_handler)


    # SQLAlchemy logs manager
    sqlalchemy_handler = RotatingFileHandler(
        sqlalchemy_log_file, maxBytes=5 * 1024 * 1024, backupCount=3
    )
    sqlalchemy_handler.setFormatter(sqlalchemy_file_formatter)
    sqlalchemy_handler.setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").addHandler(sqlalchemy_handler)

    return log


def log_message(log, message, extra=None):
    """Log message as INFO in production or DEBUG in local."""

    app_env = os.getenv("APP_ENV", "locale")
    if app_env == "production":
        log.info(message, extra=extra)
    else:
        log.debug(message, extra=extra)


def initialize_logger():
    """Initialize logging according to environment."""

    app_env = os.getenv("APP_ENV", "locale")
    if app_env == "production":
        return prod_setup()
    else:
        return locale_setup()