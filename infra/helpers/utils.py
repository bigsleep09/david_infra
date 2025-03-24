from enum import Enum
from logging import Logger
from venv import logger

import allure

from playwright.sync_api import Page

# The class `LogLevel` defines an enumeration for different log levels in Python.
class LogLevel(Enum):
    
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    
def log_message(logger: Logger, message: str, log_level: LogLevel, attach_to_allure: bool = True):
    """
    The function `log_message` logs a message with a specified log level and optionally attaches it to
    Allure report.
    
    :param logger: The `logger` parameter is an instance of a logging object that is used to log
    messages at various levels such as DEBUG, INFO, WARNING, ERROR, and CRITICAL. It is typically
    provided by a logging library like Python's `logging` module
    
    :param message: The `message` parameter is a string that represents the log message that you want to
    log using the provided `logger` object at the specified `log_level`
    
    :param log_level: The `log_level` parameter in the `log_message` function is used to specify the
    severity level of the log message being logged. It is an enum type `LogLevel` which typically
    represents different levels of logging such as DEBUG, INFO, WARNING, ERROR, and CRITICAL. The
    
    :param attach_to_allure: The `attach_to_allure` parameter in the `log_message` function is a boolean
    parameter with a default value of `True`. This parameter determines whether the log message should
    be attached to an Allure report. If `attach_to_allure` is set to `True`, the log message will,
    defaults to True
    """
    
    if log_level == LogLevel.DEBUG:
        logger.debug(msg=message)
    elif log_level == LogLevel.INFO:
        logger.info(msg=message)
    elif log_level == LogLevel.WARNING:
        logger.warning(msg=message)
    elif log_level == LogLevel.CRITICAL:
        logger.critical(msg=message)
    elif log_level == LogLevel.ERROR:
        logger.error(msg=message)
    if attach_to_allure:
        allure.attach(
            message,
            name=f"Log: {log_level.value.upper()} ::",
            attachment_type=allure.attachment_type.TEXT,
        )

def take_screenshot(page: Page, name: str):
    """
    The function `take_screenshot` captures a screenshot of a web page using the provided `Page` object
    and attaches it to an allure report with the specified name.
    
    :param page: expected to be an object representing a web page.
    :param name: string that represents the name or title of the screenshot being taken. 

    :return: `screenshot_data` if the screenshot capture is successful. Otherwise a Log message is added to the report and it returns a `None`
    """
    
    try:
        screenshot_data = page.screenshot(type="png")
        allure.attach(body=screenshot_data, name=name, attachment_type=allure.attachment_type.PNG)
        return screenshot_data
    except Exception as e:
        log_message(
            logger=logger, message=f"ERROR: take_screenshot FAILED :: {e}", log_level=LogLevel.ERROR
        )
        return None