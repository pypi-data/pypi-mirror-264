# setup.py
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

requirements = ["textual[syntax]", "tiktoken", "pyautogen", "aiosqlite"]

version = {}
with open(os.path.join(here, "tinyra/version.py")) as fp:
    exec(fp.read(), version)
__version__ = version["__version__"]

setup(
    name="tinyra",
    version=__version__,
    description="A minimalistic, terminal-based research assistant built with AutoGen.",
    packages=["tinyra"],
    package_data={"tinyra": ["*"]},
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "tinyra = tinyra:run_app",
        ],
    },
)
