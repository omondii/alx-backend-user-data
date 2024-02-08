#!/usr/bin/env python3
""" filtered_logger.py """
import re
import logging
import sys


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


    def __init__(self, fields=None):
        """ Initialize the formatter class """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        if fields is None:
            self.fields = []
        else:
            self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Formats the logs according to specified criteria """
        format = logging.Formatter.format(self, record)
        format = filter_datum(self.fields, self.REDACTION,
                              format, self.SEPARATOR)
        return format
    
    def get_logger():
        """ Returns a Logging.logger object """
        logger =logging.getLogger("user_data")
        logger.setLevel(logging.INFO)

        stream_handler = logging.StreamHandler(sys.stdout)
        formatter = RedactingFormatter()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        logger.propagate = False
