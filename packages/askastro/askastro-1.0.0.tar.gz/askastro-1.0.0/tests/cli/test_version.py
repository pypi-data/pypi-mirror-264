import pytest
from typer.testing import CliRunner


@pytest.mark.no_llm
def test_astro_version_command():
    """Test the astro version command."""
    from astro.cli import app

    runner = CliRunner()
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "Version:" in result.output
    assert "Python version:" in result.output
    assert "OS/Arch:" in result.output
