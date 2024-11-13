import logging
import colorlog

def logger():
    log = logging.getLogger("py-api")
    log.setLevel(logging.INFO)

    #Set logging color to green
    formatter = colorlog.ColoredFormatter(
        '%(asctime)s - %(log_color)s%(levelname)s%(reset)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
    )

    logger = logging.StreamHandler()
    logger.setFormatter(formatter)
    log.addHandler(logger)

    return log
