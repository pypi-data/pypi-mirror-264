import json
import os
import tempfile
from dataclasses import dataclass

from argklass.cache import load_resource
from argklass.command import Command

from uetools.core.conf import find_project
from uetools.core.options import projectfield


def namespace_from_name(name: str):
    namespace = []

    for c in name:
        if c.isupper():
            namespace.append(c)

    return "".join(namespace)


class NewPlugin(Command):
    """Create a new plugin from a template"""

    name: str = "new"

    @dataclass
    class Arguments:
        plugin: str  # Plugin's name"
        project: str = projectfield()  # project's name
        dry: bool = False

    @staticmethod
    def execute(args):
        from cookiecutter.main import cookiecutter

        project = find_project(args.project)
        project_dir = os.path.dirname(project)

        template = load_resource(__name__, "templates/PluginTemplate/cookiecutter.json")

        assert os.path.exists(template)
        template = os.path.dirname(template)
        assert os.path.exists(template)

        configfile = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)

        config = {
            "default_context": {
                "plugin_name": args.plugin,
                # "plugin_namespace": namespace_from_name(args.plugin),
            }
        }

        print(json.dumps(config, indent=2))

        if args.dry:
            return 0

        json.dump(config, configfile)
        configfile.flush()

        plugin_dir = os.path.join(project_dir, "Plugins")
        assert os.path.exists(plugin_dir)

        kwargs = dict(
            no_input=True,
            config_file=configfile.name,
            overwrite_if_exists=True,
            output_dir=plugin_dir,
        )

        cookiecutter(
            template,
            **kwargs,
        )

        # Windows have permission issues on reading a temporary files
        configfile.close()
        os.remove(configfile.name)


COMMANDS = NewPlugin
