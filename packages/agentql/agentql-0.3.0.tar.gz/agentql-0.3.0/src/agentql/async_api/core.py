"""
This module is an entrypoint to AgentQL service
"""

import logging
from typing import Any

from agentql.async_api.web import (
    InteractiveItemTypeT,
    PageTypeT,
    PlaywrightWebDriver,
    WebDriver,
)

from .session import Session

log = logging.getLogger(__name__)


async def start_async_session(
    url: str,
    *,
    web_driver: WebDriver[InteractiveItemTypeT, PageTypeT] = PlaywrightWebDriver(),
    user_auth_session: Any = None,
) -> Session[InteractiveItemTypeT, PageTypeT]:
    """Start a new asynchronous AgentQL session.

    Parameters:

    url (str): The URL to start the session with.
    web_driver (optional): The web driver to use. Defaults to Playwright web driver.
    user_auth_session (optional): The user authentication session.

    Returns:

    Session: The new session.
    """
    log.debug(f"Starting asynchronous session with {url}")

    await web_driver.start_browser(user_auth_session=user_auth_session)
    await web_driver.open_url(url)
    session = Session[InteractiveItemTypeT, PageTypeT](web_driver)
    return session
