#!/usr/bin/env python3
""" filtered_logger file """
import re
from typing import List


def filter_datum(fields: List[str],
                 redaction, message, separator):
    """ function called filter_datum that returns
    the log message obfuscated """
    string = message
    for el in fields:
        pattern = r"{}=.+?{}".format(el, separator)
        string = re.sub(pattern, "{}={}{}".format(el,
                                                  redaction,
                                                  separator), string)

    return string
