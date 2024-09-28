DEFAULT_MOD_COLLECTION = "https://next.nexusmods.com/skyrimspecialedition/collections/63guk8"


if __name__ == "__main__":
    from skyrim_mod_auto_installer.install_manager import run_mod_collection_installer

    collection_url = input(
        f"Please enter the URL to the Skyrim Special Edition mod collection you wish to download (default \"{DEFAULT_MOD_COLLECTION}\"): "
    ) or DEFAULT_MOD_COLLECTION

    try:
        max_tabs = int(input(
            "Please enter the maximum number of concurrent tabs per browser instance (default is 12): "
        ) or 12)
    except ValueError:
        print("Invalid input, using the default value of 12.")
        max_tabs = 12

    run_mod_collection_installer(
        collection_url=collection_url,

        # currently this is capped as there seems to be issues when using 2+ web drivers concurrently
        # seems like chrome doesn't allow multiple debugging ports or something. I suspect this is
        # the case as we can't debug when we start selenium driver with chrome already open. This is
        # why we need to close all of the chrome.exe processes first.
        max_browser_instances=1,

        # can increase this to however many your computer can handle. these are tabs in a single browser
        # more tabs doesn't necessarily mean a faster download as there is ultimately a lock which requires
        # the tab to be active in order to do anything.
        max_concurrent_tabs_per_browser_instance=max_tabs,
    )
