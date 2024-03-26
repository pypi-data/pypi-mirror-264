import logging
import os
from colorlog import ColoredFormatter

def getLogger(name):

    # Create a logger object
    logger = logging.getLogger(name)
    logger.setLevel(os.environ.get("LOG_LEVEL", "WARNING"))

    if not logger.handlers:

        # Create a console handler
        console_handler = logging.StreamHandler()

        # Set the format for the console handler using ColoredFormatter
        formatter = ColoredFormatter(
#            "%(log_color)s%(levelname)-8s%(reset)s %(log_color)s%(message)s%(reset)s",
            "%(levelname)-8s %(log_color)s%(message)s%(reset)s",
            datefmt=None,
            reset=True,
            log_colors={
                'DEBUG':    'cyan',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'red,bg_white',
            },
            secondary_log_colors={
                'message': {
                    'DEBUG':    'cyan',
                    'INFO':     'green',
                    'WARNING':  'yellow',
                    'ERROR':    'red',
                    'CRITICAL': 'red,bg_white',
                }
            },            style='%'
        )

        # Add formatter to the console handler
        console_handler.setFormatter(formatter)

        # Add console handler to the logger
        logger.addHandler(console_handler)

    return logger