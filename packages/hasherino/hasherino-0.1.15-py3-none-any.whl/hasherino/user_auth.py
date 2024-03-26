import asyncio
import logging
import ssl
from pathlib import Path
from random import randint
from typing import Callable
from webbrowser import open as wb_open

import certifi
from aiohttp import ClientSession, TCPConnector, web

# Field from implicit grant flow used to prevent CSRF attacks
_STATE = str(randint(1, 100_000_000))

_token = ""
_error = ""

__all__ = ["request_oauth_token"]


class _WebServerContextManager:
    def __init__(self) -> None:
        self._runner: web.AppRunner

    async def __aenter__(self):
        app = web.Application()
        app.add_routes(
            [web.get("/", _home_callback), web.get("/auth", _browser_redirect_callback)]
        )
        self._runner = web.AppRunner(app)
        await self._runner.setup()
        site = web.TCPSite(self._runner, "localhost", 17563)
        await site.start()

    async def __aexit__(self, exc_type, exc, tb):
        await self._runner.shutdown()
        await self._runner.cleanup()


async def _is_valid_token(token: str) -> bool:
    if not token:
        return False

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = TCPConnector(ssl=ssl_context)

    async with ClientSession(connector=conn) as session:
        async with session.get(
            "https://id.twitch.tv/oauth2/validate",
            headers={"Authorization": f"OAuth {token}"},
        ) as response:
            return response.status == 200


async def _browser_redirect_callback(request: web.Request) -> web.Response:
    """
    Gets state and token passed by _home_callback js code
    """
    logging.info("Running auth callback")

    global _token

    state = request.rel_url.query.get("state")
    _token = request.rel_url.query.get("access_token")

    if state != _STATE:
        _error = f"Invalid state provided: {state}"
        return web.Response(text=_error)

    if not _token:
        _error = "No token found."
        return web.Response(text=_error)

    return web.Response(text="Authenticated. You may close this tab.")


async def _home_callback(_: web.Request) -> web.Response:
    """
    Sends URL parameters passed by twitch as fragments(readable client-side only) to the auth route
    """
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>Hasherino Token</title>
</head>
<body>
    <div id="result"></div>

    <script>
        function extractFragmentParams() {
            const fragment = window.location.hash.substr(1);
            const params = new URLSearchParams(fragment);
            
            const accessToken = params.get('access_token');
            const state = params.get('state');
            
            if (accessToken && state) {
                const apiUrl = `http://localhost:17563/auth?access_token=${accessToken}&state=${state}`;
                fetch(apiUrl)
                    .then(response => response.text())
                    .then(result => {
                        // Display the fetched result in the HTML
                        const resultDiv = document.getElementById('result');
                        resultDiv.textContent = result;
                    })
                    .catch(error => console.error('Error:', error));
            } else {
                console.log('Access token or state not found in fragment.');
            }
        }
        
        extractFragmentParams();
    </script>
</body>
</html>
    """
    return web.Response(text=html, content_type="text/html")


async def request_oauth_token(app_id: str, existing_token: str = "") -> str:
    """
    Validate existing token or ask user to authenticate with twitch and provide a new one.

    Raises Exception if an issue occurs while getting the token
    """
    if await _is_valid_token(existing_token):
        logging.info("Provided token is valid, returning")
        return existing_token

    headers = {
        "client_id": app_id,
        "redirect_uri": "http://localhost:17563",
        "response_type": "token",
        "scope": "chat:edit chat:read user:manage:chat_color",
        "state": _STATE,
    }
    url_formatted_headers = "&".join(
        f"{header}={value}" for header, value in headers.items()
    )

    # Open user's default web browser to request the OAuth token
    url = f"https://id.twitch.tv/oauth2/authorize?{url_formatted_headers}"
    wb_open(url)

    logging.info(f"Waiting for twitch OAuth token from URL: {url}")

    async with _WebServerContextManager():
        while not _token and not _error:
            await asyncio.sleep(1)

        if _error:
            raise Exception(_error)

        logging.info("Returning found token")
        return _token
