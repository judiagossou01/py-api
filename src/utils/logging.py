import os
import logging
import colorlog

from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

def setup():
    """
    Configure multiple loggers: general logs, SQLAlchemy logs, HTTP logs, and error logs.
    """

    load_dotenv(dotenv_path="src/.env")

    # Logs directory
    log_dir = "logs"

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Logs files
    sqlalchemy_log_file = os.getenv("SQLALCHEMY_LOG_FILE", "logs/sqlalchemy_logs.log")
    http_log_file = os.getenv("HTTP_LOG_FILE", "logs/http_logs.log")
    error_log_file = os.getenv("ERROR_LOG_FILE", "logs/error_logs.log")

    log = logging.getLogger("PY-API")
    log.setLevel(logging.INFO)

    file_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    # CLI logs manager
    """
    cli_handler = logging.StreamHandler()
    cli_handler.setLevel(logging.INFO)
    cli_formatter = colorlog.ColoredFormatter(
        '%(asctime)s - %(log_color)s%(levelname)s%(reset)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    cli_handler.setFormatter(cli_formatter)
    log.addHandler(cli_handler)
    """

    # SQLAlchemy logs manager
    sqlalchemy_handler = RotatingFileHandler(
        sqlalchemy_log_file, maxBytes=5 * 1024 * 1024, backupCount=3
    )
    sqlalchemy_handler.setFormatter(file_formatter)
    sqlalchemy_handler.setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").addHandler(sqlalchemy_handler)

    # HTTP logs manager
    http_handler = RotatingFileHandler(
        http_log_file, maxBytes=5 * 1024 * 1024, backupCount=3
    )
    http_handler.setFormatter(file_formatter)
    http_handler.setLevel(logging.INFO)
    logging.getLogger("http.server").addHandler(http_handler)

    # Error logs manager
    error_handler = RotatingFileHandler(
        error_log_file, maxBytes=5 * 1024 * 1024, backupCount=3
    )
    error_handler.setFormatter(file_formatter)
    error_handler.setLevel(logging.ERROR)
    log.addHandler(error_handler)

    return log
