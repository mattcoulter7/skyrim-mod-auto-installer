# Skyrim Mod Auto Installer
Automatically install Skyrim Special Edition / Anniversary Edition mods, instead of having to manually going 1 by 1. Doesn't require premium NexusMods account!

![image](https://github.com/user-attachments/assets/1a8bcebc-b7e0-42ff-aebd-6d23a55fbcc9)

## Usage
**Before Running** 
1. Ensure that you have Google Chrome Installed.
2. Ensure that you are running Windows (_this is not tested for other OS_).
3. Ensure that your Google Chrome is already logged in to Nexus Mods. If not, you can do so here: https://www.nexusmods.com/skyrimspecialedition/
4. **Important** Ensure that you have checked the check box to automatically open Vortex when you Slow Download a mod from Nexus Mods. 
5. Download the zip file from the latest release: https://github.com/mattcoulter7/skyrim-mod-auto-installer/releases/, then unzip it.

**Let's install the mods**
1. Find the collection you want to install, have a browse here: https://next.nexusmods.com/skyrimspecialedition/collections?sortBy=total_downloads
2. Copy the link of the collection you want to download. For example, Gate To Sovngarde would be this one: "https://next.nexusmods.com/skyrimspecialedition/collections/qdurkx"
3. Run the .exe
4. Paste the link into the first prompt\
Prompt: _Please enter the URL to the Skyrim Special Edition mod collection ..._
5. (Optional) If you want to adjust the max concurrent tabs, do so in the second prompt:\
Prompt: _Please enter the maximum number of concurrent tabs per browser ..._

---

# Contributing
I am open to contributing to this project, it is just for personal use so far so don't expect a high level of response. You may fork it if you want to make further changes.

## Development
### Development Environment Setup
1. Ensure you have python 3.9.X installed: `python --version`
2. Ensure pip is installed: `python -m ensurepip`
3. Ensure pip is installed on the latest version: `python -m pip install --upgrade pip`
4. Ensure poetry is installed: `pip install poetry`
5. Install dependencies: `poetry install --with dev`
6. You can immediately try running it with `python app.py`, or check the various Launch commands in .vscode

### Run tests
All of the test scripts are locales under the `./tests` directory. Tests can be ran by running this script from python environment.
```bash
pytest
```
