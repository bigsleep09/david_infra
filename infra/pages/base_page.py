import logging


from typing import Callable, TypeVar


import allure


from infra.helpers.utils import LogLevel, log_message, take_screenshot


from playwright.sync_api import Page


T = TypeVar('T')
class BasePage:

    def __init__(self, page: Page) -> None:
        """
        This function initializes an object with a specified page and creates a logger for the object's
        class name.

        :param page: The `page` parameter in the `__init__` method is of type `Page`. It is used to
        initialize an instance of the class with a specific page object
        """
        self.page = page
        self.logger = logging.getLogger(self.__class__.__name__)

    def safe_execute(self, action: Callable[..., T], action_name: str, *args) -> T:
        """
        The `safe_execute` function logs and executes an action, handling any exceptions that occur and taking a
        screenshot in case of failure.

        :param action: it is a function that can take any number of arguments and return a value of type T

        :param action_name: string that represents the name of the action being executed. It is used for logging and
        error messages to identify the action that was attempted to be executed

        :return: the result of executing the `action` function with the
        provided arguments `args`.
        """
        action_with_args = "with arguments" if not args else ""
        try:
            log_message(
                logger=self.logger,
                message=f"Executing action {action_name} {action_with_args}",
                log_level=LogLevel.INFO,
            )
            return action(*args)
        except Exception as e:
            log_message(
                logger=self.logger,
                message=f"FAILED to execute action ***{action_name}*** {action_with_args} :: ERROR: {e}",
                log_level=LogLevel.ERROR,
            )
            take_screenshot(page=self.page, name=action_name)
            raise

    @allure.step("Navigate to URL: {url}")
    def navigate(self, url: str) -> None:
        """
        The function `navigate` takes a URL as input and safely executes the page navigation to that URL.

        :param url: string that represents the URL of the webpage that the browser should navigate to
        """
        self.safe_execute(self.page.goto, "navigate", url)

    @allure.step("Refresh the current page")
    def refresh(self) -> None:
        """
        The `refresh` function is used to reload a web page safely.
        """
        self.safe_execute(self.page.reload, "refresh")

    @allure.step("Navigate back")
    def go_back(self) -> None:
        """Navigate to the previous page in history."""
        self.safe_execute(self.page.go_back, "go_back")

    @allure.step("Navigate forward")
    def go_forward(self) -> None:
        """Navigate to the next page in history."""
        self.safe_execute(self.page.go_forward, "go_forward")