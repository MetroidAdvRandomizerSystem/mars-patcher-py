# Metroid Advance Randomizer System Patcher

This is an open source randomizer patcher for Metroid Fusion and Metroid Zero Mission. It is not intended for standalone use, but rather as a library to help implement plando- or randomizers.  

Here is a list of projects that use this library:
- [Randovania](https://randovania.org/)
- [An Archipelago APWorld](https://github.com/StalledStorm/ArchipelagoMine/wiki/Metroid-Fusion-Setup-Guide)

## Developer Info
Running from source:
- Create a venv: `python -m venv venv`
- Activate the venv:
  - Windows: `call venv\scripts\activate`
  - Unix-based: `source ./venv/bin/activate`
- Install the project as editable: `pip install -e .[tooling]`
- Run: `python -m mars_patcher`

Before running the patcher, you want to initialize the required patches first.
For Fusion those need to be placed into `src/mars_patcher/data/patches/mf_u/asm`.
The easiest way to do that is by running `python pull-assembly-patches.py`, which will fetch the patches from the correct release.
However for development purposes, you may want to create the assembly patches yourself manually and then copy them to that directory.

For Zero Mission it is still a Work-In-Progress.

For non-issues you can make contact with us in the [Fusion Discord Server](https://discord.gg/EmdRzfrH42).
