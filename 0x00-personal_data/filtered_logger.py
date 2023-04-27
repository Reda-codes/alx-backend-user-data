#!/usr/bin/env python3
""" filtered_logger file """
import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """ function filter_datum"""
    for el in fields:
        message = re.sub(r"{}=.+?{}".format(el, separator),
                         "{}={}{}".format(el, redaction, separator), message)
    return message
