from typing import Optional

import typer

from service_sdk.client import Client
from service_sdk.service import DEFAULT_SERVICE_HOST, DEFAULT_SERVICE_PORT

cli = typer.Typer()


@cli.command()
def ping(host: str = DEFAULT_SERVICE_HOST, port: str = DEFAULT_SERVICE_PORT):
    result = Client(host=host, port=port).ping()
    print(result)


@cli.command("exit")
def exit_service(
        host: str = DEFAULT_SERVICE_HOST, port: str = DEFAULT_SERVICE_PORT, force: Optional[bool] = None, wait: Optional[bool] = None
):
    result = Client(host=host, port=port).exit(force=force, wait=wait)
    print(result)


@cli.command()
def stop_all(
        host: str = DEFAULT_SERVICE_HOST, port: str = DEFAULT_SERVICE_PORT, force: Optional[bool] = None, wait: Optional[bool] = None
):
    Client(host=host, port=port).stop_all(force=force, wait=wait)


@cli.command()
def kill(host: str = DEFAULT_SERVICE_HOST, port: str = DEFAULT_SERVICE_PORT):
    result = Client(host=host, port=port).kill_service()
    print(result)


@cli.command()
def start(host: str = DEFAULT_SERVICE_HOST, port: str = DEFAULT_SERVICE_PORT):
    result = Client(host=host, port=port).start_worker()
    print(result)


@cli.command()
def stop(uid: str, host: str = DEFAULT_SERVICE_HOST, port: str = DEFAULT_SERVICE_PORT):
    result = Client(host=host, port=port).stop_worker(uid=uid)
    print(result)


if __name__ == "__main__":
    cli()
