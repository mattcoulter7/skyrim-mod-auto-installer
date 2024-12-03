import pytest
import os


@pytest.mark.parametrize(
    "collection_url, max_tab_concurrency",
    [
        ("https://next.nexusmods.com/skyrimspecialedition/collections/63guk8", 1),
    ]
)
def test_cli_via_subprocess(
    collection_url: str,
    max_tab_concurrency: int,
):
    stdout = os.popen(
        f"poetry run mclib_browser_automation --collection-url {collection_url} --max-tab-concurrency {max_tab_concurrency}"
    ).read()

    assert "" in stdout
