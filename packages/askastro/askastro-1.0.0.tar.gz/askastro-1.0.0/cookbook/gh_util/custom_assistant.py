from gh_util.api import functions  # pip install gh-util
from astro.beta.applications import Application
from pydantic import BaseModel, Field


class Memory(BaseModel):
    notes: list[str] = Field(default_factory=list)


octocat = Application(
    name="octocat",
    state=Memory(),
    tools=[f for f in functions if f.__name__ != "run_git_command"],
)

# $ astro assistant register cookbook/gh_util/custom_assistant.py:octocat

# > what's the latest release of kozmoai/astro?

# see https://github.com/kozmoai/astro/pull/875
