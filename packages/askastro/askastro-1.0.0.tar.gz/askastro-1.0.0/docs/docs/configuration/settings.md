# Settings

Astro makes use of Pydantic's `BaseSettings` to configure, load, and change behavior.

## Environment Variables
All settings are configurable via environment variables like `ASTRO_<setting name>`.

Please set Astro specific settings in `~/.astro/.env`. One exception being `OPENAI_API_KEY`, which may be as a global env var on your system and it will be picked up by Astro.

!!! example "Setting Environment Variables"
    For example, in your `~/.astro/.env` file you could have:
    ```shell
    ASTRO_LOG_LEVEL=INFO
    ASTRO_CHAT_COMPLETIONS_MODEL=gpt-4
    ASTRO_OPENAI_API_KEY='sk-my-api-key'
    ```
    Settings these values will let you avoid setting an API key every time. 

## Runtime Settings
A runtime settings object is accessible via `astro.settings` and can be used to access or update settings throughout the package.

!!! example "Mutating settings at runtime"
    For example, to access or change the LLM model used by Astro at runtime:
    ```python
    import astro

    astro.settings.openai.chat.completions.model = 'gpt-4'
    ```

## Settings for using Azure OpenAI models
_Some_ of Astro's functionality is supported by Azure OpenAI services.

After setting up your Azure OpenAI account and deployment, set these environment variables in your environment, `~/.astro/.env`, or `.env` file:

```bash
ASTRO_PROVIDER=azure_openai
ASTRO_AZURE_OPENAI_API_KEY=<your-api-key>
ASTRO_AZURE_OPENAI_ENDPOINT="https://<your-endpoint>.openai.azure.com/"
ASTRO_AZURE_OPENAI_API_VERSION=2023-12-01-preview # or latest

ASTRO_CHAT_COMPLETIONS_MODEL=<your azure openai deployment name>
```

Note that the chat completion model must be your Azure OpenAI deployment name.