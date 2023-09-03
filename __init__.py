from . import analysis_tools
from . import delphes_reader
from . import lhe_reader

__all__ = [
    "analysis_tools",
    "delphes_reader",
    "lhe_reader",
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
    print("Done!")
