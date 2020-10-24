# -*- coding: utf-8 -*-
"""logger facilities"""
import logging

def get_logging_level(ll):
    """get the logging level if ll is a str"""
    if isinstance(ll, str):
        ll = logging._nameToLevel.get(ll.upper(), None)
    return ll

try:
    from pygraceplot.__config__ import log_level
    log_level = get_logging_level(log_level)
except ImportError:
    log_level = logging.INFO

_hand = logging.StreamHandler()
_format = logging.Formatter(fmt='%(name)7s:%(levelname)8s - %(message)s')
_hand.setFormatter(_format)

_hand.setLevel(log_level)


def create_logger(name: str, level: str = None) -> logging.Logger:
    """create a logger object for recording log
    
    Args:
        name (str) : the name of logger. 
        level (str or int) : level of logger
    """
    logger = logging.getLogger(name)
    if level is not None:
        logger.setLevel(get_logging_level(level))
    else:
        logger.setLevel(log_level)
    return logger


