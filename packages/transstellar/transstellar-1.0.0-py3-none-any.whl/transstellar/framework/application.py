import logging
import os
from typing import Type

from injector import Injector
from selenium.webdriver import ChromeOptions, Remote
from selenium.webdriver.remote.webdriver import WebDriver

from .module import Module


class Application:
    container: Injector
    testrun_uid: str
    driver: WebDriver
    options: any
    e2e_enabled: bool = False
    closed: bool = False

    def __init__(self, request, testrun_uid, options=None):
        logging.info("Creating application")

        self.testrun_uid = testrun_uid
        self.container = Injector()
        self.options = options

        self.__configure_log__(request.config)

    def init_e2e(self):
        if self.e2e_enabled:
            return

        self.e2e_enabled = True

        self.driver = self.__init_driver__()

    def is_e2e_enabled(self):
        return self.e2e_enabled

    def get(self, key: any):
        return self.container.get(key)

    def register_module(self, module_class: Type[Module]):
        module = module_class(self)
        self.container.binder.bind(module_class, module)

    def close(self):
        if self.closed:
            return

        logging.info("Closing application")

        if self.is_e2e_enabled():
            self.driver.quit()
            logging.info("Driver closed")

        self.closed = True

        logging.info("Application closed")

    def __configure_log__(self, config):
        worker_id = os.environ.get("PYTEST_XDIST_WORKER")
        if worker_id is not None:
            with open(file=f"logs/pytest_{worker_id}.log", mode="w", encoding="utf-8"):
                pass

            logging.basicConfig(
                format=config.getini("log_file_format"),
                filename=f"logs/pytest_{worker_id}.log",
                level=config.getini("log_file_level"),
            )

    def __init_driver__(self) -> WebDriver:
        logging.info("Initializing driver")
        selenium_cmd_executor = os.environ.get(
            "SELENIUM_CMD_EXECUTOR", "http://selenium:4444/wd/hub"
        )
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = Remote(command_executor=selenium_cmd_executor, options=options)
        driver.implicitly_wait(5)
        logging.info("Driver initialized")

        return driver
