import numpy as np


def extract_branching_ratio_from_param_card(path_paramcard, PID1, PID2):
    """
    This function reads a paramcard file and extracts the Branching ratio that
    corresponds to PID1 and PID2.
    Parameters:
        path_paramcard (string): It is the path of the paramcard.
        PID1 (float): Particle ID (PID) of particle 1.
        PID2 (float): Particle ID (PID) of particle 2.

    Returns:
        BR (float): Branching Ratio.
    """
    key = '#  BR             NDA  ID1    ID2   ...\n'

    ID1 = str(PID1)
    ID2 = str(PID2)
    with open(f'{path_paramcard}', 'r') as file:
        d = file.readlines()
        position = int(np.where(np.array(d) == key)[0])
        for i in range(position, len(d)):
            row = d[i].rstrip().split(" ")
            if not (ID1 in row):
                continue
            if not (ID2 in row):
                continue
            BR = row[3]
            break
    return float(BR)
