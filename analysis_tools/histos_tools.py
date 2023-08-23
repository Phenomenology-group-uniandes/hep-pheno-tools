from itertools import product
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ROOT

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
        min(column), max(column)
    ]
    return bins


def _match_hist_bins_dict(
        hist_bins_dict: dict = None, columns: list = None
        ) -> dict:
    new_dict = {
        column: hist_bins_dict[key]
        for column, key in product(columns, hist_bins_dict.keys())
        if key in column
        }
    return new_dict


def make_histograms(
        df: pd.DataFrame,
        integral: float = 1.0,
        hist_bins_dict: dict = None
        ) -> dict:
    '''Creates histograms from the data in a DataFrame using ROOT.
    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        integral (float): The desired integral of the histograms (default =
        1.0).
        hist_bins_dict (dict): A dictionary containing the binning for each
        histogram (default = None).
    Returns:
        dict: A dictionary containing the histograms.
    '''
    if hist_bins_dict is None:
        hist_bins_dict = default_hist_bins_dict
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    if not isinstance(integral, float):
        raise TypeError("integral must be a float")
    if not isinstance(hist_bins_dict, dict):
        raise TypeError("hist_bins_dict must be a dictionary")
    hist_bins_dict = _match_hist_bins_dict(hist_bins_dict, df.columns)

    hist_dict = {}
    for column, in df.columns:
        bins = hist_bins_dict.get(
            column,
            get_hist_bins_by_column(df[column].to_numpy())
            )
        x_axis = column.replace('(', '[').replace(')', ']')
        hist = ROOT.TH1F(
            column,
            f"{x_axis}; Events",
            bins[0],
            bins[1],
            bins[2]
            )
        hist.SetDirectory(0)
        [hist.Fill(dato) for dato in df[column]]
        hist.Scale(
            integral / hist.Integral() if hist.Integral() != 0 else 1.0
            )
        hist_dict[column] = hist

    return hist_dict


def histos_matplotlib(
        Dataset: pd.DataFrame,
        column_key: str,
        log: bool = False,
        c: str = 'blue',
        file_name: str = None,
        nbins: int = 100
        ) -> None:
    ''' Uses matplotlib to create histograms using all data contained in a
    column of a DataFrame.
    Parameters:
        Dataset (DataFrame): It is a DataFrame where each row correspond to a
        different particle and each column to its corresponding kinematic
        variable value.
        column_key (str): It is the key of the column that we want to plot as
        a histogram.
        log (bool): If True, the logarithm of the data will be used.
        c (str): Histogram color.
        file_name (str): File name that would be used to save the plot.
        nbins (int): Bins number.
    '''
    if not isinstance(Dataset, pd.DataFrame):
        raise TypeError("Dataset must be a pandas DataFrame")
    if not isinstance(column_key, str):
        raise TypeError("column_key must be a string")
    if not isinstance(log, bool):
        raise TypeError("log must be a boolean")
    if not isinstance(c, str):
        raise TypeError("c must be a string")
    if not isinstance(file_name, str):
        raise TypeError("file_name must be a string")
    if not isinstance(nbins, int):
        raise TypeError("nbins must be an integer")

    data = Dataset[column_key]
    if log:
        data = np.log10(data)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(data, bins=nbins, color=c, density=True)

    # Ensure latex compatibility from root names
    char_map = {
        '#': '\\',
        '(': '[',
        ')': ']'
        }
    name = '$' + ''.join(char_map.get(c, c) for c in column_key) + '$'

    ax.set_xlabel(name, fontsize=12)
    ax.set_ylabel('A.U', fontsize=12)

    statistics = f'Mean = {data.mean():.3f}, STD = {data.std():.3f}'
    ax.set_title(statistics, loc='right', fontsize=12)

    if file_name:
        fig.savefig(file_name, bbox_inches='tight')

    plt.show()

    return fig, ax
