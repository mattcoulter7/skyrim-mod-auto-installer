# skyrim-mod-auto-installer
Automatically install skyrim mods instaed of having to manually going 1 by 1. Doesn't require premium NexusMods account.

## Usage
TODO

---

# Development
## Development Environment Setup
1. Ensure you have python 3.12.5 installed: `python --version`
2. Ensure pip is installed: `python -m ensurepip`
3. Ensure pip is installed on the latest version: `python -m pip install --upgrade pip`
4. Ensure poetry is installed: `pip install poetry`
5. Install dependencies: `poetry install --with dev`

## Run tests
All of the test scripts are locales under the `./tests` directory. Tests can be ran by running this script from python environment.
```bash
pytest
```

The tests can also be executed from a docker container. This is useful if your environment variables use container names.
```bash
docker compose -f docker-compose.yml up --build
```

The container will only start executing the test when you connect your debugger to it, so you can debug inside of the tests. To do that, run the `Docker Test Debug` launch command in vscode.
