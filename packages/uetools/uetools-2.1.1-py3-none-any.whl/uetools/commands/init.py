import os
from dataclasses import dataclass
from typing import Optional

from argklass.command import Command

from uetools.commands.engine.add import EngineAdd
from uetools.core.conf import CONFIG, CONFIGNAME, load_conf, save_conf


class Init(Command):
    """Initialize the configuration file with unreal engine folders

    Attributes
    ----------
    engine: str
        Path to the unreal engine folder (C:/opt/UnrealEngine/Engine)

    project: str
        Path to the unreal project folder (C:/Projects)

    version: str
        Engine version

    Examples
    --------

    .. code-block:: console

       uecli init --engine C:/opt/UnrealEngine/Engine --projects C:/opt/Projects

    """

    name: str = "init"

    # fmt: off
    @dataclass
    class Arguments:
        engine : Optional[str] = None  # Path to the unreal engine folder (C:/opt/UnrealEngine/Engine)
        project: Optional[str] = None  # Path to the unreal project folder (C:/Projects)
        version: Optional[str] = None  # Unreal Engine Version (5.1)
    # fmt: on

    @staticmethod
    def execute(args):
        """Initialize the engine and projects folders"""
        config = os.path.join(CONFIG, CONFIGNAME)
        conf = {}

        project_paths = conf.get("project_path", [])
        default_engine = "/UnrealEngine/Engine"
        default_project = os.path.abspath(os.path.join("..", default_engine))

        if os.path.exists(config):
            conf = load_conf()
            project_paths = conf.get("project_path", [])
            if isinstance(project_paths, str):
                project_paths = [project_paths]

            default_engine = conf.get("engine_path", default_engine)
            if len(project_paths) != 0:
                default_project = project_paths[0]

        if args.engine is None:
            engine_path = input(f"Engine Folder [{default_engine}]: ")
        else:
            engine_path = args.engine

        if args.project is None:
            project_folder = input(f"Project Folder [{default_project}]: ")
        else:
            project_folder = args.project

        engine_path = engine_path or default_engine
        project_folder = project_folder or default_project

        project_paths.append(project_folder)

        conf["engine_path"] = engine_path
        conf["project_path"] = list(set(project_paths))

        EngineAdd.addengine(conf, args.version, engine_path)

        save_conf(conf)
        print(f"Updated Engine paths inside `{config}`")
        return 0


COMMANDS = [Init]
