"""
Usage example of Astro with Azure OpenAI

If you'll be using Azure OpenAI exclusively, you can set the following env vars in your environment, `~/.astro/.env`, or `.env`:
```bash

ASTRO_PROVIDER=azure_openai
ASTRO_AZURE_OPENAI_API_KEY=<your-api-key>
ASTRO_AZURE_OPENAI_ENDPOINT="https://<your-endpoint>.openai.azure.com/"
ASTRO_AZURE_OPENAI_API_VERSION=2023-12-01-preview # or latest

Note that you MUST set the LLM model name to be your Azure OpenAI deployment name, e.g.
ASTRO_CHAT_COMPLETIONS_MODEL=<your Azure OpenAI deployment name>
```
"""

from enum import Enum

import astro
from astro.settings import temporary_settings
from pydantic import BaseModel


class Sentiment(Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"


class Location(BaseModel):
    city: str
    state: str
    country: str


@astro.fn
def list_fruits(n: int = 3) -> list[str]:
    """generate a list of fruits"""


with temporary_settings(
    provider="azure_openai",
    azure_openai_api_key="...",
    azure_openai_api_version="...",
    azure_openai_endpoint="...",
    chat_completion_model="<your Azure OpenAI deployment name>",
):
    fruits = list_fruits()
    location = astro.model(Location)("windy city")
    casted_location = astro.cast("windy city", Location)
    extracted_locations = astro.extract("I live in Chicago", Location)
    sentiment = astro.classify("I love this movie", Sentiment)

print(fruits)
print(location, casted_location, extracted_locations)
print(sentiment)
