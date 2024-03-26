import copy
import json
import logging
import os
from typing import Callable, Generic, List, Literal

import requests

from agentql.common.api_constants import GET_AGENTQL_ENDPOINT, SERVICE_URL
from agentql.common.errors import (
    AgentQLServerError,
    AgentQLServerTimeoutError,
    APIKeyError,
    AttributeNotFoundError,
    UnableToClosePopupError,
)
from agentql.common.syntax.parser import Parser
from agentql.sync_api.popup import Popup
from agentql.sync_api.web import InteractiveItemTypeT, PageTypeT, WebDriver

from .response_proxy import AQLResponseProxy

log = logging.getLogger("agentql")

RESPONSE_ERROR_KEY = "detail"


class Session(Generic[InteractiveItemTypeT, PageTypeT]):
    """A synchronous session with a AgentQL service."""

    def __init__(self, web_driver: WebDriver[InteractiveItemTypeT, PageTypeT]):
        """Initialize the session.

        Parameters:

        web_driver (WebDriver): The web driver that will be used in this session.
        """

        self._api_key = os.getenv("AGENTQL_API_KEY")
        if not self._api_key:
            raise APIKeyError(
                "API key not provided. Please set the environment variable 'AGENTQL_API_KEY' with your API key."
            )
        self._web_driver = web_driver
        self._event_listeners = {}
        self._check_popup = False

    @property
    def current_page(self) -> PageTypeT:
        """Get the current page."""
        return self._web_driver.get_current_page()

    @property
    def driver(self) -> WebDriver[InteractiveItemTypeT, PageTypeT]:
        """Get the web driver"""
        return self._web_driver

    def get_user_auth_session(self):
        """Get the user authentication session."""
        return self._web_driver.get_user_auth_session()

    def query(
        self,
        query: str,
        timeout: int = 500,
        lazy_load_pages_count: int = 0,
        wait_for_network_idle: bool = True,
    ) -> AQLResponseProxy[InteractiveItemTypeT]:
        """Query the web page tree for elements that match the AgentQL query.

        Parameters:

        query (str): The query string.
        timeout (optional): Optional timeout value for the connection with backend api service.
        lazy_load_pages_count (optional): The number of pages to scroll down and up to load lazy loaded content.
        wait_for_network_idle (optional): Whether to wait for the network to be idle before querying the page.

        Returns:

        dict: AgentQL Response (Elements that match the query)
        """
        log.debug(f"querying {query}")

        parser = Parser(query)
        query_tree = parser.parse()

        self._web_driver.wait_for_page_ready_state(wait_for_network_idle)

        accessibility_tree = self._web_driver.prepare_accessiblity_tree(
            lazy_load_pages_count=lazy_load_pages_count
        )

        # Check if there is a popup in the page before sending the agentql query
        if self._check_popup:
            popup_list = self._detect_popup(accessibility_tree, [])
            if popup_list:
                self._handle_popup(popup_list)

        response = self._query(query, accessibility_tree, timeout)

        # Check if there is a popup in the page after receiving the agentql response
        if self._check_popup:
            # Fetch the most up-to-date accessibility tree
            accessibility_tree = self._web_driver.get_accessibility_tree()

            popup_list = self._detect_popup(accessibility_tree, popup_list)
            if popup_list:
                self._handle_popup(popup_list)

        return AQLResponseProxy[InteractiveItemTypeT](response, self._web_driver, query_tree)

    def stop(self):
        """Close the session."""
        log.debug("closing session")
        self._web_driver.stop_browser()

    def on(self, event: Literal["popup"], callback: Callable[[dict], None]):
        """Emitted when there is a popup on the page. The callback function will be invoked with the popup object as the argument. Passing None as the callback function will disable popup detections."""
        self._event_listeners[event] = callback
        if callback:
            self._check_popup = True
        else:
            self._check_popup = False

    def _query(self, query: str, accessibility_tree: dict, timeout: int) -> dict:
        """Make Request to AgentQL API.

        Parameters:

        query (str): The query string.
        accessibility_tree (dict): The accessibility tree.
        timeout (int): The timeout value for the connection with backend api service

        Returns:

        dict: AgentQL response in json format.
        """
        try:
            page_url = self._web_driver.get_current_url()
            request_data = {
                "query": f"{query}",
                "accessibility_tree": accessibility_tree,
                "metadata": {"url": page_url},
            }
            url = os.getenv("AGENTQL_API_HOST", SERVICE_URL) + GET_AGENTQL_ENDPOINT
            log.debug(f"Making request to {url}")
            headers = {"X-API-Key": self._api_key}
            response = requests.post(
                url, json=request_data, headers=headers, timeout=timeout, allow_redirects=True
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.ReadTimeout):
                raise AgentQLServerTimeoutError() from e
            if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 401:
                raise APIKeyError(
                    "Invalid or expired API key provided. Please set the environment variable 'AGENTQL_API_KEY' with a valid API key."
                ) from e
            error_code = e.response.status_code if e.response is not None else None
            server_error = e.response.content.decode("utf-8") if e.response is not None else None
            if server_error:
                try:
                    server_error_json = json.loads(server_error)
                    if isinstance(server_error_json, dict):
                        server_error = server_error_json.get(RESPONSE_ERROR_KEY)
                except ValueError:
                    raise AgentQLServerError(server_error, error_code) from e
            raise AgentQLServerError(server_error, error_code) from e

    def _detect_popup(self, tree: dict, known_popups: List[Popup]) -> List[Popup]:
        """Detect if there is a popup in the page. If so, create a Popup object and add it to the popup dict.

        Parameters:

        tree (dict): The accessibility tree.
        known_popups (list): The list of known popups.

        Returns:
        popups (list): The list of popups.
        """
        tree_role = tree.get("role", "")
        tree_name = tree.get("name", "")
        popup_list = []
        if tree_role == "dialog":
            popup = Popup(copy.deepcopy(tree), tree_name, self._close_popup)

            # Avoid adding existing popup to the dict and double handle the popup
            if known_popups:
                for popup_object in known_popups:
                    if popup_object.name() != popup.name():
                        popup_list.append(popup)
            else:
                popup_list.append(popup)

            return popup_list

        if "children" in tree:
            for child in tree.get("children", []):
                popup_list = popup_list + self._detect_popup(child, known_popups)

        return popup_list

    def _handle_popup(self, popups: List[Popup]):
        """Handle the popup. If there is a popup in the list, and there is an event listener, emit the popup event by invoking the callback function.

        Parameters:

        popups (list): The list of popups to handle."""
        if popups and "popup" in self._event_listeners and self._event_listeners["popup"]:
            self._event_listeners["popup"](popups)

    def _close_popup(self, tree: dict):
        """Close the popup.

        Parameters:

        popup (Popup): The popup to close.
        """
        query = """
            {
                popup {
                    close_btn
                }
            }
        """
        parser = Parser(query)
        query_tree = parser.parse()
        try:
            response = self._query(query, tree, 500)
            agentql_response = AQLResponseProxy[InteractiveItemTypeT](
                response, self._web_driver, query_tree
            )
            agentql_response.popup.close_btn.click()
        except (AgentQLServerError, AttributeNotFoundError) as e:
            raise UnableToClosePopupError() from e
