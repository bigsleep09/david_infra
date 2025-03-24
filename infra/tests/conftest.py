import os
import pathlib
import shutil
from venv import logger
import allure

import pytest

from infra.helpers.utils import LogLevel, log_message
from playwright.sync_api import BrowserContext, Page, sync_playwright


@pytest.fixture(scope="session", params=["chromium", "firefox", "webkit"])
def browser(request: pytest.FixtureRequest):
    """Fixture to launch Playwright browser based in the parameterized browser"""
    browser_name = request.param
    log_message(
        logger=logger,
        message=f"Launching browser {browser_name}",
        log_level=LogLevel.INFO,
    )
    headless = request.config.getoption("--headed")
    with sync_playwright() as p:
        browser_instance = getattr(p, browser_name).launch(
            headless=not headless, args=["--start-maximized"]
        )
        yield browser_instance
        log_message(
            logger=logger,
            message=f"Closing browser {browser_name}",
            log_level=LogLevel.INFO,
        )
        browser_instance.close()


@pytest.fixture(scope="session")
def context(browser):
    context: BrowserContext = browser.new_context(record_video_dir="videos")
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    page: Page = context.new_page()
    yield page
    page.close()

PLAYWRIGHT_EXTENSION_VIDEO = ".webm"
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item: pytest.TestReport):
    yield

    try:
        # Check if the test failed

        if item.rep_call.failed:
            # Video directory path

            video_dir = pathlib.Path("videos")

            # Check if the directory exists and has files

            if video_dir.exists() and video_dir.is_dir():
                for file in video_dir.iterdir():
                    if file.is_file() and file.suffix == PLAYWRIGHT_EXTENSION_VIDEO:
                        log_message(
                            logger=logger,
                            message=f"Attaching video {file.name} to Allure report.",
                            log_level=LogLevel.INFO,
                        )
                        # Attach video to Allure report

                        allure.attach.file(
                            source=file,
                            name=f"Failed Test Video - {item.nodeid}",
                            attachment_type=allure.attachment_type.WEBM,
                        )
                    else:
                        log_message(
                            logger=logger,
                            message="No video file found in the specified directory.",
                            log_level=LogLevel.INFO,
                        )
            else:
                log_message(
                    logger=logger,
                    message="Video directory does not exist or is empty.",
                    log_level=LogLevel.ERROR,
                )
    except Exception as e:
        log_message(
            logger=logger,
            message=f"Error attaching video: {e}",
            log_level=LogLevel.ERROR,
        )



@pytest.fixture(scope="session", autouse=True)
def cleanup_videos():
    """Cleanup video files before running tests"""
    if os.path.exists("videos"):
        shutil.rmtree("videos")
    yield