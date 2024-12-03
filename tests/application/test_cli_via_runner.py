import pytest

from typer.testing import CliRunner
from skyrim_mod_auto_installer.application.cli import main  # Adjust based on your actual module name

runner = CliRunner()


@pytest.mark.parametrize(
    "collection_url, max_tab_concurrency",
    [
        ("https://next.nexusmods.com/skyrimspecialedition/collections/63guk8", 1),
    ]
)
def test_cli_via_runner(
    collection_url: str,
    max_tab_concurrency: int,
):
    # Run the CLI command with the given parameters
    result = runner.invoke(
        main,
        [
            "--collection-url", collection_url,
            "--max-tab-concurrency", str(max_tab_concurrency),
        ]
    )

    assert result.exit_code == 0
