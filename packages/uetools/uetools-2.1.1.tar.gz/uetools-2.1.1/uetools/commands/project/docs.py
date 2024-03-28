import os
from dataclasses import dataclass
from typing import Optional

from argklass.command import Command

from uetools.core.conf import find_project
from uetools.core.options import projectfield

COOKIECUTTER = "https://github.com/kiwi-lang/UEDocs"


class Docs(Command):
    """Add a Sphinx + Doxygen documentation to a project"""

    name: str = "docs"

    @dataclass
    class Arguments:
        # fmt: off
        project : str = projectfield() # name of your project
        no_input: bool = False           # Do not show user prompts
        config  : Optional[str] = None   # Configuration file used to initialize the project (json)
        # fmt: on

    @staticmethod
    def execute(args):
        from cookiecutter.main import cookiecutter

        uproject = find_project(args.project)
        folder = os.path.dirname(uproject)

        os.chdir(folder)
        cookiecutter(
            COOKIECUTTER,
            no_input=args.no_input,
            config_file=args.config,
            overwrite_if_exists=True,
        )

        return 0


COMMANDS = Docs
