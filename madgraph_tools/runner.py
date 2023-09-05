import os
import subprocess
MG5_PATH = os.path.join(os.sep, 'Collider', "MG5_aMC_v3_1_0", "bin", "mg5_aMC")


def run_mg5(scriptfile: str, MG5_PATH: str = MG5_PATH) -> subprocess.Popen:
    if not os.path.exists(MG5_PATH):
        raise FileNotFoundError(f"Path to MG5 not found: {MG5_PATH}")
    if not os.path.exists(scriptfile):
        raise FileNotFoundError(f"Path to scriptfile not found: {scriptfile}")

    return subprocess.Popen(
        [MG5_PATH, scriptfile],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        check=True
        )
