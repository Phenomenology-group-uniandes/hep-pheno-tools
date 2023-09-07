from . import analysis_tools
from . import delphes_reader
from . import lhe_reader
from . import madgraph_tools

__all__ = [
    "analysis_tools",
    "delphes_reader",
    "lhe_reader",
    "madgraph_tools",
]


def update():
    import os
    import subprocess

    print("Updating the framework from github...")
    subprocess.run(
        "git pull",
        shell=True,
        cwd=os.path.dirname(os.path.abspath(__file__)),
    )
    # install new requirements with low verbosity
    subprocess.run(
        "pip install -r requirements.txt -q",
        shell=True,
        cwd=os.path.dirname(os.path.abspath(__file__)),
    )
    print("Done!")
