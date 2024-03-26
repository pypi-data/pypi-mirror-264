import time
from typing import Union

from playwright.sync_api import Error, Frame, Locator, Page, StorageState, sync_playwright
from playwright_stealth import StealthConfig, stealth_sync

from agentql.async_api.web.network_monitor import PageActivityMonitor
from agentql.common.driver_constants import RENDERER, USER_AGENT, VENDOR
from agentql.common.driver_settings import ProxySettings, ScrollDirection, StealthModeConfig
from agentql.common.errors import (
    AccessibilityTreeError,
    ElementNotFoundError,
    NoOpenBrowserError,
    NoOpenPageError,
    OpenUrlError,
)
from agentql.common.html_constants import HTML_ROLE_MAPPING
from agentql.common.js_snippets.snippet_loader import load_js
from agentql.common.utils import ensure_url_scheme
from agentql.sync_api.web.web_driver import WebDriver

from .web_driver import WebDriver


class PlaywrightWebDriver(WebDriver[Locator, Page]):
    def __init__(self, headless=True, proxy: ProxySettings = None) -> None:
        self._playwright = None

        self._browser = None
        """The current browser. Only use this to close the browser session in the end."""

        self._context = None
        """The current browser context. Use this to open a new page"""

        self._current_page = None
        """The current page that is being interacted with."""

        self._original_html = None
        """The page's original HTML content, prior to any AgentQL modifications"""

        self._headless = headless
        """Whether to run browser in headless mode or not."""

        self._proxy = proxy

        self._page_monitor = None

        self._current_tf_id = None

        self._stealth_mode_config = None

    def locate_interactive_element(self, response_data: dict) -> Locator:
        """
        Locates an interactive element in the web page.

        Parameters:

        response_data (dict): The data of the interactive element from the AgentQL response.

        Returns:

        Locator: The interactive element.
        """
        tf623_id = response_data.get("tf623_id")
        if not tf623_id:
            raise ElementNotFoundError("tf623_id")
        iframe_path = response_data.get("attributes", {}).get("iframe_path")
        return self.find_element_by_id(tf623_id, iframe_path)

    @property
    def is_headless(self) -> bool:
        """Returns whether the browser is running in headless mode or not."""
        return self._headless

    def get_text_content(self, web_element: Locator) -> str:
        """
        Returns the text content of the web element.

        Parameters:

        web_element (Locator): The web element to get the text content from.

        Returns:

        str: The text content of the web element.
        """
        return web_element.text_content()

    def start_browser(self, user_auth_session: StorageState = None):
        """
        Starts a new browser session and set user session state (if there is any).

        Parameters:
        user_auth_session (optional): The user auth session state to use.
        """
        self._start_browser(
            headless=self._headless, user_auth_session=user_auth_session, proxy=self._proxy
        )

    def stop_browser(self):
        """Closes the current browser session."""
        if self._context:
            self._context.close()
            self._context = None
        if self._browser:
            self._browser.close()
            self._browser = None
        if self._playwright:
            self._playwright.stop()
            self._playwright = None

    def enable_stealth_mode(
        self,
        webgl_vendor: str = VENDOR,
        webgl_renderer: str = RENDERER,
        nav_user_agent: str | None = USER_AGENT,
    ):
        """Enable the Stealth Mode and set the stealth mode configuration.
        Ideally parameters values should match some real values to avoid detection.
        To get a realistic examples, you can use browser fingerprinting websites such as https://bot.sannysoft.com/ and https://pixelscan.net/

        Parameters:
        webgl_vendor (str): The WebGL vendor to use.
        webgl_renderer (str): The WebGL renderer to use.
        nav_user_agent (str): The navigator user agent to use.
        """
        self._stealth_mode_config = StealthModeConfig(
            vendor=webgl_vendor, renderer=webgl_renderer, nav_user_agent=nav_user_agent
        )

    def open_url(self, url: str):
        """
        Opens a new page and navigates to the given URL.
        """
        if not self._browser:
            raise NoOpenBrowserError()
        self._open_url(url)

    def get_current_url(self) -> str:
        """Get the URL of the active page."""
        if not self._current_page:
            raise NoOpenPageError()
        return self._current_page.url

    def get_html(self) -> dict:
        """Returns the original HTML (i.e. without any AgentQL modifications) fetched from the most recently loaded page".

        Returns:

        string: The HTML content of the web page.
        """
        if not self._current_page:
            raise ValueError('No page is open. Make sure you call "open_url()" first.')
        return self._original_html

    def get_current_page(self) -> Page:
        """Returns the current page.

        Returns:

        Page: The current page.
        """
        if not self._current_page:
            raise ValueError('No page is open. Make sure you call "open_url()" first.')
        return self._current_page

    def open_html(self, html: str):
        """
        Opens a new page and loads the given HTML content.
        """
        if not self._browser:
            raise NoOpenBrowserError()
        self._current_page = self._context.new_page()
        self._current_tf_id = 0
        self._current_page.set_content(html)

    def prepare_accessiblity_tree(self, lazy_load_pages_count: int = 3) -> dict:
        """Prepare the AT by modifing the dom. It will return the accessibility tree after waiting for page to load and dom modification.

        Parameters:
        lazy_load_pages_count: The number of times to scroll down and up the page.

        Returns:
        dict: AT of the page
        """
        if not self._current_page:
            raise NoOpenPageError()

        self._original_html = self._current_page.content()
        self._page_scroll(pages=lazy_load_pages_count)

        accessibility_tree = None
        try:
            accessibility_tree = self._get_page_accessibility_tree(self._current_page)
            self._process_iframes(accessibility_tree)
            self._post_process_accessibility_tree(accessibility_tree)

        except Exception as e:
            raise AccessibilityTreeError() from e

        return accessibility_tree

    def get_accessibility_tree(self) -> dict:
        """Returns the up-to-date accessibility tree of the page.

        Returns:
        dict: The accessibility tree of the page.
        """
        try:
            accessibility_tree = self._get_page_accessibility_tree(self._current_page)
            self._process_iframes(accessibility_tree)
        except Exception as e:
            raise AccessibilityTreeError() from e

        return accessibility_tree

    def get_user_auth_session(self) -> StorageState:
        """Returns the user auth session state of the browser."""
        if not self._browser:
            raise NoOpenBrowserError()
        return self._context.storage_state()

    def wait_for_page_ready_state(self, wait_for_network_idle: bool = True):
        """Wait for the page to reach the "Page Ready" or stable state."""
        if not self._page_monitor:
            self._page_monitor = PageActivityMonitor()
        else:
            # Reset the network monitor to clear the logs
            self._page_monitor.reset()

        # Add event listeners to track DOM changes and network activities
        self._add_page_event_listeners()

        # Wait for the page to reach the "Page Ready" state
        self._determine_load_state(self._page_monitor, wait_for_network_idle)

        # Remove the event listeners to prevent overwhelming the async event loop
        self._remove_page_event_listeners()

    def scroll_page(self, scroll_direction: ScrollDirection, pixels: int = 720):
        """Scrolls the page up or down.

        Parameters:
        scroll_direction (ScrollDirection): The direction to scroll the page.
        pixels (int): The number of pixels to scroll.
        """
        if not self._current_page:
            raise NoOpenPageError()

        delta_y = pixels if scroll_direction == ScrollDirection.DOWN else -pixels
        self._current_page.mouse.wheel(delta_x=0, delta_y=delta_y)

    def scroll_to_bottom(self):
        """Scrolls the page to the bottom."""
        if not self._current_page:
            raise NoOpenPageError()

        self._current_page.evaluate(load_js("scroll_to_bottom"))

    def scroll_to_top(self):
        """Scrolls the page to the top."""
        if not self._current_page:
            raise NoOpenPageError()

        self._current_page.evaluate(load_js("scroll_to_top"))

    def _post_process_accessibility_tree(self, accessibility_tree: dict):
        """Post-process the accessibility tree by removing node's attributes that are Null."""
        if "children" in accessibility_tree and accessibility_tree.get("children") is None:
            del accessibility_tree["children"]

        for child in accessibility_tree.get("children", []):
            self._post_process_accessibility_tree(child)

    def _process_iframes(
        self,
        page_accessibility_tree: dict = None,
        *,
        iframe_path: str = "",
        frame: Frame = None,
    ):
        """
        Recursively retrieves the accessibility trees for all iframes in a page or frame.

        Parameters:
            iframe_path (str): The path of the iframe in the frame hierarchy.
            frame (Frame): The frame object representing the current frame.
            page_accessibility_tree (dict): The accessibility tree of the page.

        Returns:
            None
        """
        if frame is None:
            iframes = self._current_page.query_selector_all("iframe")
        else:
            frame = frame.content_frame()
            if not frame:
                return
            iframes = frame.query_selector_all("iframe")

        for iframe in iframes:
            iframe_id = iframe.get_attribute("tf623_id")
            iframe_path_to_send = ""
            if iframe_path:
                iframe_path_to_send = f"{iframe_path}."
            iframe_path_to_send = f"{iframe_path_to_send}{iframe_id}"
            iframe_accessibility_tree = self._get_frame_accessibility_tree(
                iframe, iframe_path_to_send
            )

            self._merge_iframe_tree_into_page(
                iframe_id, page_accessibility_tree, iframe_accessibility_tree
            )

            self._process_iframes(
                iframe_path=iframe_path_to_send,
                frame=iframe,
                page_accessibility_tree=page_accessibility_tree,
            )

    def _get_page_accessibility_tree(self, context: Union[Page, Frame]) -> dict:
        """
        Retrieves the accessibility tree for the given page.

        Returns:
            dict: The accessibility tree for the page.
        """
        result = context.evaluate(
            load_js("generate_accessibility_tree"),
            {
                "currentGlobalId": self._current_tf_id,
                "roleTagMap": HTML_ROLE_MAPPING,
                "processIFrames": False,
            },
        )

        self._current_tf_id = result.get("lastUsedId")

        return result.get("tree")

    def _get_frame_accessibility_tree(self, frame: Frame, iframe_path) -> dict:
        """
        Retrieves the accessibility tree for a given frame.

        Parameters:
            frame (Frame): The frame for which to retrieve the accessibility tree.
            iframe_path: The path of the iframe within the frame.

        Returns:
            dict: The accessibility tree for the frame.
        """
        frame_context = frame.content_frame()

        if not frame_context:
            return {}

        self._set_iframe_path(context=frame_context, iframe_path=iframe_path)
        accessibility_tree = self._get_page_accessibility_tree(frame_context)

        return accessibility_tree

    def _merge_iframe_tree_into_page(
        self, iframe_id, accessibility_tree: dict, iframe_accessibility_tree: dict
    ):
        """
        Stitches the iframe accessibility tree with the page accessibility tree.

        Parameters:
            iframe_id (str): The ID of the iframe.
            accessibility_tree (dict): The accessibility tree of the page.
            iframe_accessibility_tree (dict): The accessibility tree of the iframe.

        Returns:
            None
        """
        children = accessibility_tree.get("children", [])
        if children is None:
            return
        for child in children:
            attributes = child.get("attributes", {})
            if "tf623_id" in attributes and attributes["tf623_id"] == iframe_id:
                if not child.get("children"):
                    child["children"] = []
                child["children"].append(iframe_accessibility_tree)
                break
            self._merge_iframe_tree_into_page(iframe_id, child, iframe_accessibility_tree)

    def _apply_stealth_mode_to_page(self, page: Page):
        """Applies stealth mode to the given page.

        Parameters:
        page (Page): The page to which stealth mode will be applied.
        """
        # Only mask User Agent in headless mode to avoid detection for headless browsers
        mask_user_agent = self._headless

        stealth_sync(
            page,
            config=StealthConfig(
                vendor=self._stealth_mode_config["vendor"],
                renderer=self._stealth_mode_config["renderer"],
                # nav_user_agent will only take effect when navigator_user_agent parameter is True
                nav_user_agent=self._stealth_mode_config["nav_user_agent"],
                navigator_user_agent=mask_user_agent,
            ),
        )

    def _open_url(self, url: str):
        """Opens a new page and navigates to the given URL. Initialize the storgage state if provided.

        Parameters:

        url (str): The URL to navigate to.
        storgate_state_content (optional): The storage state with which user would like to initialize the browser.

        """

        self._current_page = None
        url = ensure_url_scheme(url)

        try:
            page = self._context.new_page()
            if self._stealth_mode_config is not None:
                self._apply_stealth_mode_to_page(page)
            self._current_tf_id = 0
            page.goto(url, wait_until="domcontentloaded")
        except Exception as e:
            raise OpenUrlError() from e

        self._current_page = page

    def _set_iframe_path(self, context: Union[Page, Frame], iframe_path=None):
        """
        Sets the iframe path in the given context.

        Parameters:
            context (Page | Frame): The context in which the DOM will be modified.
            iframe_path (str, optional): The path to the iframe. Defaults to None.
        """
        context.evaluate(
            load_js("set_iframe_path"),
            {"iframe_path": iframe_path},
        )

    def _page_scroll(self, pages=3):
        """Scrolls the page down first and then up to load all contents on the page.

        Parameters:

        pages (int): The number of pages to scroll down.
        """
        if pages < 1:
            return

        if self._stealth_mode_config is None:
            delta_y = 10000
            for _ in range(pages):
                self._current_page.mouse.wheel(delta_x=0, delta_y=delta_y)
                time.sleep(0.1)

            time.sleep(1)
            delta_y = -10000
            for _ in range(pages):
                self._current_page.mouse.wheel(delta_x=0, delta_y=delta_y)
                time.sleep(0.1)
        else:
            for _ in range(pages):
                self.scroll_to_bottom()
                time.sleep(0.1)

            time.sleep(1)
            for _ in range(pages):
                self.scroll_to_top()
                time.sleep(0.1)

    def _start_browser(
        self,
        user_auth_session=None,
        headless=True,
        proxy: ProxySettings = None,
    ):
        """Starts a new browser session and set storage state (if there is any).

        Parameters:

        user_session_extras (optional): the JSON object that holds user session information
        headless (bool): Whether to start the browser in headless mode.
        load_media (bool): Whether to load media (images, fonts, etc.) or not.
        """
        ignored_args = ["--enable-automation", "--disable-extensions"]
        args = [
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-blink-features=AutomationControlled",
        ]
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(
            headless=headless, proxy=proxy, args=args, ignore_default_args=ignored_args
        )
        self._current_tf_id = 0
        self._context = self._browser.new_context(
            user_agent=USER_AGENT,
            storage_state=user_auth_session,
        )

    def _get_frame_context(self, iframe_path: str = None) -> Union[Frame, Page]:
        """
        Returns the frame context for the given iframe path.

        Parameters:
            iframe_path (str): The path of the iframe within the frame.

        Returns:
            Frame | Page: The frame context for the given iframe path.
        """
        if not iframe_path:
            return self._current_page
        iframe_path_list = iframe_path.split(".")
        frame_context = self._current_page
        for iframe_id in iframe_path_list:
            frame_context = frame_context.frame_locator(f"[tf623_id='{iframe_id}']")
        return frame_context

    def find_element_by_id(self, tf623_id: str, iframe_path: str = None) -> Locator:
        """
        Finds an element by its TF ID within a specified iframe.

        Args:
            tf623_id (str): The generated tf id of the element to find.
            iframe_path (str): The path to the iframe containing the element.

        Returns:
            Locator: The located element.

        Raises:
            ElementNotFoundError: If the element with the specified TF ID is not found.
        """
        try:
            element_frame_context = self._get_frame_context(iframe_path)
            return element_frame_context.locator(f"[tf623_id='{tf623_id}']")
        except Exception as e:
            raise ElementNotFoundError(tf623_id) from e

    def _determine_load_state(
        self,
        monitor: PageActivityMonitor,
        timeout_seconds=14,
        wait_for_network_idle=True,
    ):
        start_time = time.time()

        while True:
            if wait_for_network_idle:
                try:
                    last_updated_timestamp = self._current_page.evaluate(
                        load_js("get_last_dom_change")
                    )
                # If the page is navigating, the evaluate function will raise an error. In this case, we wait for the page to load.
                except Error:
                    while True:
                        if self._page_monitor.get_load_status() or time.time() - start_time > 6:
                            break
                        time.sleep(0.2)
                    last_updated_timestamp = time.time()

                if monitor.check_conditions(last_active_dom_time=last_updated_timestamp):
                    break
            else:
                if self._page_monitor.get_load_status():
                    break
            if time.time() - start_time > timeout_seconds:
                break
            time.sleep(0.1)

    def _add_page_event_listeners(self):
        self._current_page.on("request", self._page_monitor.track_network_request)
        self._current_page.on("requestfinished", self._page_monitor.track_network_response)
        self._current_page.on("requestfailed", self._page_monitor.track_network_response)
        self._current_page.on("load", self._page_monitor.track_load)

        try:
            self._current_page.evaluate(load_js("add_dom_change_listener"))
        # If the page is navigating, the evaluate function will raise an error. In this case, we wait for the page to load.
        except Error:
            start_time = time.time()
            while True:
                if self._page_monitor.get_load_status() or time.time() - start_time > 6:
                    break
                time.sleep(0.2)

    def _remove_page_event_listeners(self):
        self._current_page.remove_listener("request", self._page_monitor.track_network_request)
        self._current_page.remove_listener(
            "requestfinished", self._page_monitor.track_network_response
        )
        self._current_page.remove_listener(
            "requestfailed", self._page_monitor.track_network_response
        )
        self._current_page.remove_listener("load", self._page_monitor.track_load)
        self._current_page.evaluate(load_js("remove_dom_change_listener"))
