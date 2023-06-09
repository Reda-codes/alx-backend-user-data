#!/usr/bin/env python3
""" filtered_logger file """
import re
from typing import List
import logging
import os
import mysql.connector

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format method """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """ function filter_datum"""
    for el in fields:
        message = re.sub(r"{}=.+?{}".format(el, separator),
                         "{}={}{}".format(el, redaction, separator), message)
    return message


def get_logger() -> logging.Logger:
    """ function get_logger """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ get_db function """
    return mysql.connector.connect(
                    user=os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root'),
                    password=os.environ.get('PERSONAL_DATA_DB_PASSWORD', ''),
                    host=os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost'),
                    database=os.environ.get('PERSONAL_DATA_DB_NAME'))


def main():
    """ main function """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    result = cursor.fetchall()
    for row in result:
        message = "name={}; email={}; phone={}; ssn={}; password={}; ip={}; last_login={}; user_agent={};".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        log_record = logging.LogRecord("my_logger", logging.INFO,
                                       None, None, message, None, None)
        formatter = RedactingFormatter(PII_FIELDS)
        formatter.format(log_record)
        print(formatter.format(log_record))

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
