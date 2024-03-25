from typing import TYPE_CHECKING, Callable, Optional, Union

from openai import AssistantEventHandler, AsyncAssistantEventHandler
from pydantic import BaseModel, Field, PrivateAttr, field_validator
from rich.prompt import Confirm, Prompt

import astro.utilities.openai
import astro.utilities.tools
from astro.beta.assistants.handlers import PrintHandler
from astro.tools.assistants import AssistantTool
from astro.types import Tool
from astro.utilities.asyncio import (
    ExposeSyncMethodsMixin,
    expose_sync_method,
    run_sync,
)
from astro.utilities.logging import get_logger

from .threads import Thread

if TYPE_CHECKING:
    from .runs import Run


logger = get_logger("Assistants")

NOT_PROVIDED = "__NOT_PROVIDED__"


def default_run_handler_class() -> (
    type[Union[AssistantEventHandler, AsyncAssistantEventHandler]]
):
    return PrintHandler


class Assistant(BaseModel, ExposeSyncMethodsMixin):
    """
    The Assistant class represents an AI assistant that can be created, deleted,
    loaded, and interacted with.

    Attributes:
        id (str): The unique identifier of the assistant. None if the assistant
                  hasn't been created yet.
        name (str): The name of the assistant.
        model (str): The model used by the assistant.
        metadata (dict): Additional data about the assistant.
        file_ids (list): List of file IDs associated with the assistant.
        tools (list): List of tools used by the assistant.
        instructions (str): Instructions for the assistant.
    """

    id: Optional[str] = None
    name: str = "Assistant"
    description: Optional[str] = None
    model: str = Field(None, validate_default=True)
    instructions: Optional[str] = Field(None, repr=False)
    tools: list[Union[AssistantTool, Callable]] = []
    file_ids: list[str] = []
    metadata: dict[str, str] = {}
    # context level tracks nested assistant contexts
    _context_level: int = PrivateAttr(0)

    default_thread: Thread = Field(
        default_factory=Thread,
        repr=False,
        description="A default thread for the assistant.",
    )

    @field_validator("model", mode="before")
    def default_model(cls, model):
        if model is None:
            model = astro.settings.openai.assistants.model
        return model

    def clear_default_thread(self):
        self.default_thread = Thread()

    def get_tools(self) -> list[AssistantTool]:
        return [
            (
                tool
                if isinstance(tool, Tool)
                else astro.utilities.tools.tool_from_function(tool)
            )
            for tool in self.tools
        ]

    def get_instructions(self, thread: Thread = None) -> str:
        return self.instructions or ""

    @expose_sync_method("say")
    async def say_async(
        self,
        message: str,
        file_paths: Optional[list[str]] = None,
        thread: Optional[Thread] = None,
        event_handler_class: type[
            Union[AssistantEventHandler, AsyncAssistantEventHandler]
        ] = NOT_PROVIDED,
        **run_kwargs,
    ) -> "Run":
        thread = thread or self.default_thread

        if event_handler_class is NOT_PROVIDED:
            event_handler_class = default_run_handler_class()

        # post the message
        user_message = await thread.add_async(message, file_paths=file_paths)

        from astro.beta.assistants.runs import Run

        run = Run(
            # provide the user message as part of the run to print
            messages=[user_message],
            assistant=self,
            thread=thread,
            event_handler_class=event_handler_class,
            **run_kwargs,
        )
        result = await run.run_async()

        return result

    def __enter__(self):
        return run_sync(self.__aenter__())

    def __exit__(self, exc_type, exc_val, exc_tb):
        return run_sync(self.__aexit__(exc_type, exc_val, exc_tb))

    async def __aenter__(self):
        # if this is the outermost context and no ID is set, create the assistant
        if self.id is None and self._context_level == 0:
            await self.create_async(_auto_delete=True)

        self._context_level += 1
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._context_level > 0:
            self._context_level -= 1

        # If this is the outermost context, delete the assistant
        if self._context_level == 0:
            await self.delete_async()

        return False

    @expose_sync_method("create")
    async def create_async(self, _auto_delete: bool = False):
        if self.id is not None:
            raise ValueError(
                "Assistant has an ID and has already been created in the OpenAI API."
            )
        client = astro.utilities.openai.get_openai_client()
        response = await client.beta.assistants.create(
            **self.model_dump(
                include={"name", "model", "metadata", "file_ids", "metadata"}
            ),
            tools=[tool.model_dump() for tool in self.get_tools()],
            instructions=self.get_instructions(),
        )
        self.id = response.id

        # assistants are auto deleted if their context level reaches 0,
        # so we disable that behavior by initializing the context level to 1
        if not _auto_delete:
            self._context_level = 1

    @expose_sync_method("delete")
    async def delete_async(self):
        if not self.id:
            raise ValueError("Assistant has no ID and doesn't exist in the OpenAI API.")
        client = astro.utilities.openai.get_openai_client()
        await client.beta.assistants.delete(assistant_id=self.id)
        self.id = None

    @classmethod
    def load(cls, assistant_id: str, **kwargs):
        return run_sync(cls.load_async(assistant_id, **kwargs))

    @classmethod
    async def load_async(cls, assistant_id: str, **kwargs):
        client = astro.utilities.openai.get_openai_client()
        response = await client.beta.assistants.retrieve(assistant_id=assistant_id)
        assistant = cls(**(response.model_dump() | kwargs))
        # set context level to 1 so the assistant is never auto-deleted
        assistant._context_level = 1
        return assistant

    @expose_sync_method("chat")
    async def chat_async(self, initial_message: str = None, **kwargs):
        # send an initial message, if provided
        if initial_message is not None:
            await self.say_async(initial_message, **kwargs)
        while True:
            try:
                message = None
                while not message:
                    message = Prompt.ask("[bold green]Your message[/]")
                    # if the user types exit, ask for confirmation
                if message in ["exit", "!exit", ":q", "!quit"]:
                    if Confirm.ask("[red]Are you sure you want to exit?[/]"):
                        break
                    continue
                # if the user types exit -y, quit right away
                elif message == "exit -y":
                    break
                await self.say_async(message, **kwargs)
            except KeyboardInterrupt:
                break

    def pre_run_hook(self):
        pass

    def post_run_hook(self, run: "Run"):
        pass
