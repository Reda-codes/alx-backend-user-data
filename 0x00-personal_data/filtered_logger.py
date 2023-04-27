#!/usr/bin/env python3
""" filtered_logger file """
import re


def filter_datum(fields, redaction, message, separator):
    string = message
    for el in fields:
        pattern = r"{}=.+?{}".format(el, separator)
        string = re.sub(pattern, "{}={}{}".format(el, redaction, separator), string)

    return string
