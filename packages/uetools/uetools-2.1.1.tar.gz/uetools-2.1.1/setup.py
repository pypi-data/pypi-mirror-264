from pathlib import Path

from setuptools import find_packages, setup

with open("uetools/core/__init__.py") as file:
    for line in file.readlines():
        if "version" in line:
            version = line.split("=")[1].strip().replace('"', "")
            break

extras_require = {
    "ml": [
        "msgpack",
        "numpy",
        "gym",
    ],
}
extras_require["all"] = sorted(set(sum(extras_require.values(), [])))

setup_kwargs = dict(
    name="uetools",
    version=version,
    description="Tools for Unreal Engine",
    long_description=(Path(__file__).parent / "README.rst").read_text(),
    author="Pierre Delaunay",
    author_email="pierre@delaunay.io",
    license="BSD-3-Clause",
    url="https://uetools.readthedocs.io",
    packages=[
        "uetools.jinga2",
        "uetools.rl",
        "uetools.core",
        "uetools.commands",
        "uetools.commands.editor",
        "uetools.commands.engine",
        "uetools.commands.game",
        "uetools.commands.plugin",
        "uetools.commands.project",
        "uetools.commands.test",
        "uetools.commands.uat",
        "uetools.commands.ubt",
        "uetools.commands.gitlab",
        "uetools.format",
        "uetools.plugins.gamekit",
    ],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    zip_safe=True,
    setup_requires=["setuptools"],
    install_requires=[
        "appdirs",
        "colorama",
        "cookiecutter",
        "GitPython",
        "hjson",
        "importlib_resources",
        "tqdm",
        "argklass>=1.4.4",
    ],
    extras_require=extras_require,
    python_requires=">=3.8",
    # Deprecated
    # namespace_packages=["uetools", "uetools.plugins"],
    entry_points={
        "console_scripts": [
            "uecli = uetools.core.cli:main_force",
            "ueui = uetools.ui.main:main",
        ],
        "UECLICommands": [
            "ml = uetools.plugins.ml:ML",
            "cpp = uetools.plugins.cpp:CPP",
        ],
    },
    package_data={
        "uetools": [
            "uetools/templates/.*",
            "uetools/commands/editor/templates/.*",
            "uetools/commands/plugin/templates/.*",
            "uetools/commands/project/templates/.*",
            "uetools/core/data/.*",
        ]
    },
    include_package_data=True,
)

if __name__ == "__main__":
    setup(**setup_kwargs)
