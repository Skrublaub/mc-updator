import logging
import sys

from pathlib import Path

from backend.constants import LOG_FORMAT, LOG_DIR


def initiate_logger(filename: Path | str = LOG_DIR / 'test.log') -> None:
    """
    Holds the basic config for a logger to be used in the program

    Args:
        filename (Path | str): where to save the log file at

    Returns:
        None
    """
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO, filename=filename)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    return


def log_enter_exit(func):
    """
    This is a basic logging function that just marks when a function is
    entered or exited

    Args:
        func (function): The function to be ran

    Returns:
        wrap function below

    """
    def wrap(*args, **kwargs):
        logging.info(f'Entering {func.__name__} with args: {args} and {kwargs}')
        result = func(*args, **kwargs)  # decorated function call
        logging.info(f'Exiting {func.__name__} with args: {args} and {kwargs}')
        return result

    return wrap
