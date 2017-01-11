#!/usr/bin/env python
# coding: utf-8

import logging

def create_logger(log_name):
    stream = logging.StreamHandler()
    stream.setLevel(logging.INFO)
    logfile = logging.FileHandler(log_name, mode='w')
    logfile.setLevel(logging.WARNING)
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(levelname)s %(asctime)s] %(message)s")
    stream.setFormatter(formatter)
    logfile.setFormatter(formatter)

    logger.addHandler(stream)
    logger.addHandler(logfile)

    return logger
