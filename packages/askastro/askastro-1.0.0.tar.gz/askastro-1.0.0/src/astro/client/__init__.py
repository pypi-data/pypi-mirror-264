from typing import Union, overload
from typing_extensions import Self
from .openai import AstroClient, AsyncAstroClient
from openai import Client, AsyncClient


class Astro:
    @overload
    def __new__(cls: type[Self], client: "Client") -> "AstroClient":
        ...

    @overload
    def __new__(cls: type[Self], client: "AsyncClient") -> "AsyncAstroClient":
        ...

    def __new__(
        cls: type[Self], client: Union["Client", "AsyncClient"]
    ) -> Union["AstroClient", "AsyncAstroClient"]:
        if isinstance(client, AsyncClient):
            return AsyncAstroClient(client=client)
        return AstroClient(client=client)

    @classmethod
    def wrap(
        cls: type[Self], client: Union["Client", "AsyncClient"]
    ) -> Union["Client", "AsyncClient"]:
        if isinstance(client, AsyncClient):
            return AsyncAstroClient.wrap(client=client)
        return AstroClient.wrap(client=client)
