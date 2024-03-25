import sys
import typer
from rich.console import Console
from typing import Optional
from astro.client.openai import AsyncAstroClient
from astro.types import StreamingChatResponse
from astro.utilities.asyncio import run_sync
from astro.utilities.openai import get_openai_client
from astro.beta.assistants import Assistant
from astro.cli.threads import threads_app
from astro.cli.assistants import assistants_app, say as assistants_say

import platform

from typer import Context, Exit, echo

from astro import __version__

app = typer.Typer(no_args_is_help=True)
console = Console()
app.add_typer(threads_app, name="thread")
app.add_typer(assistants_app, name="assistant")
app.command(name="say")(assistants_say)


@app.command()
def version(ctx: Context):
    if ctx.resilient_parsing:
        return
    echo(f"Version:\t\t{__version__}")
    echo(f"Python version:\t\t{platform.python_version()}")
    echo(f"OS/Arch:\t\t{platform.system().lower()}/{platform.machine().lower()}")
    raise Exit()


if __name__ == "__main__":
    app()
