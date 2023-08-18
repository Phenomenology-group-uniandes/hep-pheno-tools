import numpy as np


default_hist_bins_dict = {
    "#Delta{R}": [96, 0, 7],
    "#Delta{#eta}": [80, -5, 5],
    "#Delta{#phi}": [52, -3.25, 3.25],
    "#Delta{pT}": [120, 0.0, 1500.0],
    "#Delta{#vec{pT}}": [240, 0.0, 4800.0],
    "#Delta{#vec{p}}": [240, 0.0, 4800.0],
    "MET(GeV)": [80, 0.0, 1000.0],
    "pT_": [160, 0.0, 2000.0],
    "sT(GeV)": [200, 0.0, 4000.0],
    "mT(GeV)": [200, 0.0, 4000.0],
    "#eta_": [80, -5, 5],
    "#phi_": [128, -3.2, 3.2],
    "Energy_": [80, 0.0, 1000.0]
}


def get_hist_bins_by_column(column: np.ndarray) -> list:
    '''Generates the binning for a histogram from a numpy array.
    Parameters:
        column (np.ndarray): 1d numpy array containing the data.
    Returns:
        list: A list containing the number of bins calculated using the
        Sturges rule (1+log2(N)) and the minimum and
        maximum value.
    '''
    if not isinstance(column, np.ndarray):
        raise TypeError("column must be a numpy array")
    if column.ndim != 1:
        raise ValueError("column must be a 1d numpy array")

    bins = [
        int(1 + np.log2(len(column))),
        min(column),
        max(column)
    ]
    return bins
