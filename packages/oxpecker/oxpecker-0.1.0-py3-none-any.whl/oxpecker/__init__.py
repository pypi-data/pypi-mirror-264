"""Basic setup for oxpecker package."""
import datetime
import json
import logging
import os
import shutil
from functools import partial
from pathlib import Path

import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

try:
    API_URL = f'https://{os.environ["OXPECKER_HOST"]}:{os.environ["OXPECKER_PORT"]}/oxpecker/api/v1/'
    WS_URL = f'wss://{os.environ["OXPECKER_HOST"]}:{os.environ["OXPECKER_PORT"]}/oxpecker-client-connect'
except KeyError:
    logging.warning(
        "OXPECKER_HOST or OXPECKER_PORT environment variable is not set; many commands would not work."
    )
    API_URL = ""
    WS_URL = ""

API_ENDPOINTS = {
    "login": "auth/login",
    "upload": "files/upload",
    "task_create": "tasks",
    "task_list": "tasks/search",
    "file_check": "files/check-exist",
    "task_inspect": "tasks",
}

LANGUAGES = [
    "c",
    "cpp",
    "csharp",
    "go",
    "java",
    "kotlin",
    "javascript",
    "typescript",
    "python",
    "ruby",
    "swift",
]

WORK_DIR = Path("~/.oxpecker").expanduser()
WORK_DIR.mkdir(parents=True, exist_ok=True)

if not (CODEQL_EXE := shutil.which("codeql")):
    logging.warning("`codeql` is not found; many commands would not work.")

try:
    auth = {"Authorization": (token := os.environ.get("OXPECKER_TOKEN"))}
    if not token:
        with open(WORK_DIR / "token", encoding="utf-8") as tf:
            auth = {"Authorization": f"Bearer {json.load(tf)['accessToken']}"}
except (OSError, FileNotFoundError):
    logging.warning(
        "Oxpecker token not found; many commands would not work.\n"
        "Use `oxpecker login` to get the token.\n"
    )
    auth = {"Authorization": "INVALID TOKEN"}


class OxpeckerAuthSession(requests.Session):
    """Session class for Oxpecker that handles automatic token refresh."""

    def request(self, *args, **kwargs):
        self.refresh_token_if_needed()
        self.request = partial(super().request, timeout=15)
        return self.request(*args, **kwargs)

    def refresh_token_if_needed(self):
        """Refresh the session token if it is close to expiring."""
        with open(WORK_DIR / "token", encoding="utf-8") as token_file:
            token_data = json.load(token_file)
        token_expiry_str = token_data.get("expiresIn")
        if token_expiry_str:
            token_expiry = datetime.datetime.strptime(
                token_expiry_str, "%Y-%m-%d %H:%M:%S"
            )
            if (token_expiry - datetime.datetime.now()).total_seconds() < 30:
                self.refresh_access_token(token_data["refreshToken"])

    def refresh_access_token(self, refresh_token):
        """Refresh the access token using the provided refresh token."""
        refresh_url = f"{API_URL}auth/exchange-token"
        r = requests.post(
            refresh_url, json={"refreshToken": refresh_token}, verify=False, timeout=15
        )  # Consider the security implications of verify=False
        if r.status_code == requests.codes.ok:  # pylint: disable=no-member
            new_token_data = r.json()
            current_time = datetime.datetime.now()
            # Convert expiresIn and refreshExpiresIn to local datetime
            expires_in = new_token_data.get("expiresIn", 0)
            refresh_expires_in = new_token_data.get("refreshExpiresIn", 0)
            new_token_data["expiresIn"] = (
                current_time + datetime.timedelta(seconds=expires_in)
            ).strftime("%Y-%m-%d %H:%M:%S")
            new_token_data["refreshExpiresIn"] = (
                current_time + datetime.timedelta(seconds=refresh_expires_in)
            ).strftime("%Y-%m-%d %H:%M:%S")
            with open(WORK_DIR / "token", mode="w", encoding="utf-8") as cf:
                json.dump(new_token_data, cf)
            self.headers.update(
                {"Authorization": f"Bearer {new_token_data['accessToken']}"}
            )


session = OxpeckerAuthSession()
session.headers.update(auth)
