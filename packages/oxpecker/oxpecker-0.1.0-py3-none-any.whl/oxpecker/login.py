"""Module for login to the server."""

import json
import os
from datetime import datetime, timedelta
from json import JSONDecodeError

import requests
import rich_click as click
from requests import codes

from oxpecker import API_ENDPOINTS, API_URL, WORK_DIR
from oxpecker.utils import retry_if_network_error


@click.command()
@click.option("--username", "-u", required=True, help="""Username of the service.""")
@click.option("--password", "-p", required=True, help="""Password of the service.""")
@click.pass_context
@retry_if_network_error()
def login(ctx, username, password):
    """Login to Oxpecker service."""
    if ctx.find_root().params["debug"]:
        click.echo(username)
        click.echo(password)
    r = requests.post(
        f"{API_URL}{API_ENDPOINTS['login']}",
        json={"userName": username, "password": password},
        verify=not ctx.find_root().params["insecure_skip_tls_verify"],
        timeout=15,
    )
    if r.status_code == codes.ok:  # pylint: disable=no-member
        try:
            print(r.json())
        except JSONDecodeError:
            print(r.text)
        expires_in = r.json().get("expiresIn", 0)
        refresh_expires_in = r.json().get("refreshExpiresIn", 0)
        current_time = datetime.now()

        # Convert expiresIn and refreshExpiresIn to local datetime
        token_data = r.json()
        token_data["expiresIn"] = (
            current_time + timedelta(seconds=expires_in)
        ).strftime("%Y-%m-%d %H:%M:%S")
        token_data["refreshExpiresIn"] = (
            current_time + timedelta(seconds=refresh_expires_in)
        ).strftime("%Y-%m-%d %H:%M:%S")

        with open(
            token_file_path := WORK_DIR / "token", mode="w", encoding="utf-8"
        ) as cf:
            json.dump(token_data, cf)
        os.chmod(token_file_path, 0o600)
    else:
        print(f"{r.status_code}: {r.request.method} {r.url}")
        print(r.text)
