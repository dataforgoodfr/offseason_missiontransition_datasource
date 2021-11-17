import logging
import sys


def get_logger(name):
    """Returns a logger formated

    Parameters
    ----------
    name : str
        Name for logging

    Returns
    -------
    logging.Logger
        Logger formated
    """

    root = logging.getLogger(name)
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    root.addHandler(handler)

    return root
