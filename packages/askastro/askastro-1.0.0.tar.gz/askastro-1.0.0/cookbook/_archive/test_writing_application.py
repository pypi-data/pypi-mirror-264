from pathlib import Path

import astro
import astro.tools
import astro.tools.filesystem
import astro.tools.python
import astro.tools.shell
from astro.beta.applications import Application
from pydantic import BaseModel, Field

astro.settings.log_level = "DEBUG"
astro.settings.llm_model = "gpt-4"


class TestWriterState(BaseModel):
    files_info: dict[str, str] = Field(
        default_factory=dict,
        description=(
            "A place to record notes about specific files, including any details e.g."
            ' {"path/to/file.py": "Main entrypoint"}'
        ),
    )
    tests_passing: bool = False


ROOT_DIR = Path(astro.__file__).parents[2]

test_app = Application(
    name="TestWriter",
    description=f"""
        You are responsible for writing and maintaining the unit tests for the
        Astro library, located at {ROOT_DIR}. You may only modify files inside
        {ROOT_DIR}. Astro's tests are all stored in `tests/` and can be run
        with `pytest` from the directory root. 
        
        The user will give you instructions on what functionality to test or how
        to modify tests. When you write tests, you will need to ensure that the
        work and meet the user's expectation. Remember, you are an expert Python
        developer and you strive to write complete, readable, tests. You believe
        tests are the best form of documentation. Do not write tests that
        already exist, make sure you are adding valuable and interesting tests
        to the codebase.
        """,
    state=TestWriterState(),
    tools=[
        astro.tools.filesystem.ListFiles(root_dir=ROOT_DIR),
        astro.tools.filesystem.ReadFile(root_dir=ROOT_DIR),
        astro.tools.filesystem.ReadFiles(root_dir=ROOT_DIR),
        astro.tools.filesystem.WriteFiles(
            root_dir=ROOT_DIR, require_confirmation=False
        ),
        astro.tools.python.Python(require_confirmation=False),
        astro.tools.shell.Shell(
            require_confirmation=False, working_directory=ROOT_DIR
        ),
    ],
)
