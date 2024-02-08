#!/usr/bin/env python3
""" filtered_logger.py """
import re
import logging


def filter_datum(fields, redaction, message, separator):
    """ filter_datum returns the log message obfuscated """
    for field in fields:
        message = re.sub(f"{field}=[^{separator}]*",
                         f"{field}={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    logging.basicConfig(format='')

    def __init__(self, fields=None):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        if fields is None:
            self.fields = []
        else:
            self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        format = logging.Formatter.format(self, record)
        format = filter_datum(self.fields, self.REDACTION, format, self.SEPARATOR)
        return format
    