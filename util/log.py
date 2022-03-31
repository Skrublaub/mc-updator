import logging
import sys

from typing import Union
from pathlib import Path

def initiate_logger(filename: Union[Path,str] = 'test.log') -> None:
    """
    Holds the basic config for a logger to be used in the program

    Args:
        None

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
        result = func(*args, **kwargs) # decorated function call
        logging.info(f'Exiting {func.__name__} with args: {args} and {kwargs}')
        return result

    return wrap