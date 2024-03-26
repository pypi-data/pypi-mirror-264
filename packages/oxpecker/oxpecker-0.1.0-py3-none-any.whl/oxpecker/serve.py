"""Start websocket connection."""

import ssl

import daemon as py_daemon
import rich_click as click
import websocket

from oxpecker import WORK_DIR, WS_URL, auth
from oxpecker.ws_demo import on_close, on_error, on_message, on_open
from oxpecker.utils import retry_if_network_error


def ws_conn():
    websocket.enableTrace(True)

    ws = websocket.WebSocketApp(
        WS_URL,
        header=auth,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    # FIXME: sikp verify only explicitly.
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


@click.command(help="Connect to the websocket server for bidirectional communication.")
@click.option(
    "--detach/--no-detach",
    is_flag=True,
    help="[Experimental] Connect and put the process in background.",
    default=False,
)
@retry_if_network_error()
def serve(detach):
    """Connect to the websocket server."""
    if detach:
        with py_daemon.DaemonContext(
            pidfile=(WORK_DIR / "serve.pid").open("w"),
            stdout=(WORK_DIR / "serve.out.log").open("w+"),
            stderr=(WORK_DIR / "serve.err.log").open("w+"),
        ) as dc:
            ws_conn()
            click.echo(f"{dc.pidfile} = ")
    else:
        ws_conn()


if __name__ == "__main__":
    serve()  # pylint: disable=no-value-for-parameter
