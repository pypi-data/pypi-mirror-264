from typing import Any, TypeVar

from typing_extensions import Protocol

from agentql.common.driver_settings import ScrollDirection

InteractiveItemTypeT = TypeVar("InteractiveItemTypeT")
"""
A type variable representing the type of interactive items in a web driver session.
Used in type hints where the exact type depends on the specific web driver library used.
"""

PageTypeT = TypeVar("PageTypeT")
"""
A type variable representing the type of a page in a web driver session.
Used in type hints where the exact type depends on the specific web driver library used.
"""


class WebDriver(Protocol[InteractiveItemTypeT, PageTypeT]):
    def locate_interactive_element(self, response_data: dict) -> InteractiveItemTypeT:
        """
        Locates an interactive element in the web page.

        Parameters:

        response_data (dict): The data of the interactive element from the AgentQL response.

        Returns:

        InteractiveItemTypeT: The interactive element.
        """

    async def get_text_content(self, web_element: InteractiveItemTypeT) -> str:
        """
        Gets the text content of the web element.

        Parameters:

        web_element (InteractiveItemTypeT): The web element.

        Returns:

        str: The text content of the web element."""

    async def start_browser(self, user_auth_session: Any = None):
        """Start the browser.

        Parameters:

        user_auth_session (optional): the JSON object that holds user session information
        """

    async def stop_browser(self):
        """Stops/closes the browser."""

    async def open_url(self, url: str):
        """Open URL in the browser."""

    async def get_current_url(self) -> str:
        """Get the URL of the active page."""

    async def prepare_accessiblity_tree(self, lazy_load_pages_count: int) -> dict:
        """Prepare the AT by modifing the dom. It will return the accessibility tree after preparation.

        Parameters:
        lazy_load_pages_count: The number of times to scroll down and up the page.

        Returns:
        dict: AT of the page
        """

    async def get_accessibility_tree(self) -> dict:
        """Returns the up-to-date accessibility tree of the page.

        Returns:
        dict: The accessibility tree of the page.
        """

    async def wait_for_page_ready_state(self, wait_for_network_idle: bool = True):
        """Wait for the page to reach the "Page Ready" or stable state."""

    async def get_user_auth_session(self) -> Any:
        """Returns the current user auth session state.

        Returns:

        The user session state.
        """

    async def get_html(self) -> dict:
        """Returns the original HTML (i.e. without any AgentQL modifications) fetched from the most recently loaded page".

        Returns:

        string: The HTML content of the web page.
        """

    async def scroll_page(self, scroll_direction: ScrollDirection, pixels: int = 720):
        """Scrolls the page up or down.

        Parameters:
        scroll_direction (ScrollDirection): The direction to scroll the page.
        pixels (int): The number of pixels to scroll.
        """

    async def scroll_to_bottom(self):
        """Scrolls the page to the bottom."""

    async def scroll_to_top(self):
        """Scrolls the page to the top."""

    async def get_current_page(self) -> PageTypeT:
        """Returns the current page object.

        Returns:

        PageTypeT: The current page object.
        """
