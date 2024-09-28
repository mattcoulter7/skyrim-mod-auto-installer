def test():
    from skyrim_mod_auto_installer.install_manager import run_mod_collection_installer

    run_mod_collection_installer(
        collection_url="https://next.nexusmods.com/skyrimspecialedition/collections/63guk8",
        max_concurrent_tabs_per_browser_instance=1,
        max_concurrent_tabs_per_browser_instance=12,
    )
