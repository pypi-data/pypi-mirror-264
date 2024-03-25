import sys
from urllib.parse import ParseResult, urlparse

from .element import Element


class BasePage(Element):
    XPATH_CURRENT = "//body"

    def get_page(self, page_class):
        if self.app:
            return page_class(self.app)

        return page_class(self.app)

    def get_page_from_module(self, module, page_class):
        return getattr(sys.modules[module], page_class)(self.app)

    def get_current_url(self) -> ParseResult:
        return urlparse(self.app.driver.current_url)
