#!/usr/bin/env python3
""" filtered_logger file """
import re
from typing import List


def filter_datum(fields: List[str],
                 redaction, message, separator):
    """ function filter_datum"""
    for el in fields:
        pattern = r"{}=.+?{}".format(el, separator)
        message = re.sub(pattern,
                        "{}={}{}".format(el, redaction, separator), message)
    return message
