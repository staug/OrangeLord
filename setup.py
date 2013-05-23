# An advanced setup script to create multiple executables and demonstrate a few
# of the features available to setup scripts
#
# hello.py is a very simple "Hello, world" type script which also displays the
# environment in which the script runs
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

import sys
import pygame._view
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
        Executable("Game.py", base=base)
]


buildOptions = dict(
        compressed = True,
        includes = ["pygame", "shelve", "configparser", "sys", "ast", "math", "random"],
        path = sys.path,
        include_files=["resources"])

setup(
        name = "OrangeLord",
        version = "0.7",
        description = "OrangeLord Dungeon",
        options = dict(build_exe = buildOptions),
        executables = executables)