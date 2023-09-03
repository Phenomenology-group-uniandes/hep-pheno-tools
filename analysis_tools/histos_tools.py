import os
from itertools import product
from typing import List, Dict, Tuple

import numpy as np
import pandas as pd
import uproot
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

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

char_map = {
    '#': '\\',
    '(': '[',
    ')': ']'
    }

char_map_path = {
  "#": "",
  "{": "",
  "}": "",
  " ": "_"
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
    name = '$' + ''.join(char_map.get(c, c) for c in column_key) + '$'

    ax.set_xlabel(name, fontsize=12)
    ax.set_ylabel('A.U', fontsize=12)

    statistics = f'Mean = {data.mean():.3f}, STD = {data.std():.3f}'
    ax.set_title(statistics, loc='right', fontsize=12)

    if file_name:
        fig.savefig(file_name, bbox_inches='tight')

    plt.show()

    return fig, ax


def overlap_root_histos(
        kinematic_variable: str,
        dict_histos: Dict[str, Dict[str, ROOT.TH1F]],
        alpha: float = 0.05,
        stack: bool = False,
        log_scale: bool = False, grid: bool = False,
        y_range: Tuple[float, float] = (1, 100)
        ) -> Tuple[ROOT.THStack, ROOT.TCanvas, ROOT.TLegend]:
    '''Uses ROOT to overlap histograms using all kinematic variable's
    histograms contained in a dictionary.
    Parameters:
        kinematic_variable (str): Name of the kinematic variable. It must be
        also the key to access the corresponding histograms inside dict_histos.
        dict_histos (dict): Directory that contains all the histograms. This
        dictionary should have keys with the name of the signals, and each
        signal should have other dictionaries with the same structure as an}
        output of make_histograms.
        alpha (float): Histogram transparency. It must be between 0 and 1.
        stack (bool): If True, the plot of histograms will consider a Stack
        between them.
        log_scale (bool): If True, the histogram will be plotted using log10
        scale.
        grid (bool): If True, the canvas will plot a grid in the graphic.
    Returns:
        tuple of THStack, TCanvas, and TLegend objects.
    '''

    if not isinstance(kinematic_variable, str):
        raise TypeError("kinematic_variable must be a string")
    if not isinstance(dict_histos, dict):
        raise TypeError("dict_histos must be a dictionary")
    if not isinstance(alpha, float):
        raise TypeError("alpha must be a float")
    if not isinstance(stack, bool):
        raise TypeError("stack must be a boolean")
    if not isinstance(log_scale, bool):
        raise TypeError("log_scale must be a boolean")
    if not isinstance(grid, bool):
        raise TypeError("grid must be a boolean")
    if not 0 <= alpha <= 1:
        raise ValueError("alpha must be between 0 and 1")

    canvas = ROOT.TCanvas('', '', 600, 400)
    legend = ROOT.TLegend(0.6, .8, 0.89, .89)
    legend.SetNColumns(4)
    legend.SetLineWidth(1)

    histos = ROOT.THStack('hist', '')

    for i, (signal, histo_dict) in enumerate(dict_histos.items()):
        if histo_dict:
            histo = histo_dict[kinematic_variable]
            histo.SetLineColor(i + 1)
            histo.SetFillColorAlpha(i + 1, alpha)
            histo.SetLineWidth(2)
            histo.SetDirectory(0)
            histos.Add(histo)
            legend.AddEntry(histo, signal)

    x_axis = "".join(char_map.get(c, c) for c in kinematic_variable)

    if stack:
        histos.Draw("hist")
        histos.SetTitle(f'; {x_axis}; Events')
    else:
        histos.Draw("histnostack")
        histos.SetTitle(f'; {x_axis}; A.U')

    if log_scale:
        canvas.SetLogy()
    histos.SetMinimum(y_range[0])
    histos.SetMaximum(y_range[1])

    if grid:
        canvas.SetGrid()

    canvas.Draw()
    legend.Draw('same')

    return histos, canvas, legend


def sum_histos(histo_list: List[ROOT.TH1F], substract=False) -> ROOT.TH1F:
    '''Sums histograms in a list using ROOT library.
    Parameters:
        histo_list (List[TH1F]): List of histograms to be summed.
    Return:
        TH1F: Histogram with the sum of all histograms in histo_list.
    '''
    # Check that histo_list is a list of TH1F
    if not all(isinstance(histo, ROOT.TH1F) for histo in histo_list):
        raise TypeError("histo_list must be a list of TH1F")

    # Check that all histograms have the same number of bins and bin width
    bin_width = histo_list[0].GetBinWidth(0)
    nbins = histo_list[0].GetNbinsX()
    x_low = histo_list[0].GetBinLowEdge(1)
    x_up = histo_list[0].GetBinLowEdge(nbins) + bin_width

    def check_bins(h):
        A = h.GetNbinsX() != nbins
        B = np.isclose(h.GetBinWidth(0), bin_width)
        C = np.isclose(h.GetBinLowEdge(1), x_low)
        D = np.isclose(h.GetBinLowEdge(nbins) + h.GetBinWidth(0), x_up)
        return A or not B or not C or not D

    if any(check_bins(h) for h in histo_list):
        raise ValueError("All histograms must have the same binning")

    # Initialize result histogram with bin information
    xlow = histo_list[0].GetBinLowEdge(1)
    xup = histo_list[0].GetBinLowEdge(nbins) + bin_width
    result = ROOT.TH1F('sum', 'sum', nbins, xlow, xup)
    result.SetDirectory(0)

    if substract:
        result.Add(histo_list[0])
        for n in range(1, len(histo_list)):
            result.Add(histo_list[n], -1.0)
    else:
        # Sum histograms and errors
        for histo in histo_list:
            result.Add(histo)

    return result


def get_histos_with_holes(Dict_Hist: Dict[str, ROOT.TH1F]) -> List[str]:
    """
    Returns a list with the names of all histograms with holes contained in a
    python dictionary (Dict_Hist).
    Parameters:
        Dict_Hist (Dict[str, TH1F]): It is the dictionary that contains all
        the histograms.
    Return:
        List[str]: List with the names of all histograms with holes.
    """

    if not all(isinstance(h, ROOT.TH1F) for h in Dict_Hist.values()):
        raise TypeError("Dict_Hist must be a dictionary of TH1F histograms")

    def count_zeros(histo):
        add = 0
        for i in range(1, histo.GetNbinsX()+1):
            if (histo.GetBinContent(i) == 0):
                add += 1
        return add
    hist_with_holes = {
        key: count_zeros(histo)
        for key, histo in Dict_Hist.items()
        if count_zeros(histo) > 0
    }
    return hist_with_holes


def fill_histogram_holes_Fix_value(histo, value_to_fill=10e-4) -> List[str]:
    """
    Fill all the holes contained in a histogram.

    Parameters:
        histo (TH1F): histograms with holes.
        value_to_fill (Float): value that will be used to fill the histogram
        holes.
    Return:
        histo (TH1F): histogram without holes.
    """
    for i in range(1, histo.GetNbinsX()+1):
        if (histo.GetBinContent(i) == 0):
            histo.SetBinContent(i, value_to_fill)
    return histo


def fill_histogram_holes_interp1d(hist):
    """
    Uses linear interpolation to fill holes in a TH1F histogram.
    """
    # Extract the histogram data as a numpy array
    hist_data = np.array(
        [hist.GetBinContent(i) for i in range(1, hist.GetNbinsX()+1)]
    )

    # Replace bin-high = 0 values with NaN values
    hist_data[hist_data == 0] = np.nan

    # Identify the missing values in the array
    missing_values = np.isnan(hist_data)

    # Create an interpolator for the non-missing values
    x = np.arange(len(hist_data))
    y = hist_data[~missing_values]
    f = interp1d(x[~missing_values], y, kind='linear')

    # Use the interpolator to fill in the missing values
    hist_data[missing_values] = f(x[missing_values])

    # Replace the NaN values with 0
    hist_data[np.isnan(hist_data)] = 0

    # Update the histogram with the interpolated data
    for i in range(1, hist.GetNbinsX()+1):
        hist.SetBinContent(i, hist_data[i-1])

    return hist


def save_histograms_png(
        path_to_save: str,
        dict_hist: Dict[str, ROOT.TH1F],
        log_y: bool = False
        ) -> None:
    """Save histograms as .png files.

    Parameters:
        path_to_save: Folder name that will be used to save all histograms as
        .png files.
        dict_hist: Dictionary that contains all the histograms.
        log_y: If True, the histogram will be plotted using log 10 Y-scale.
    """

    if not isinstance(path_to_save, str):
        raise TypeError("path_to_save must be a string")
    if not all(isinstance(histo, ROOT.TH1F) for histo in dict_hist.values()):
        raise TypeError("dict_hist must be a dictionary of TH1F")
    if not isinstance(log_y, bool):
        raise TypeError("log_y must be a boolean")

    for key, histo in dict_hist.items():
        canvas = ROOT.TCanvas(key, "", 0, 0, 1280, 720)
        canvas.SetGrid()
        if log_y:
            canvas.SetLogy()
        histo.Draw("hist")
        path = os.path.join(path_to_save, f"histograms_{key}.png")
        path = "".join(char_map_path.get(c, c) for c in path)
        canvas.SaveAs()


def write_root_file(file_name: str, dict_Hist: Dict[str, ROOT.TH1F]) -> None:
    """
    This function writes a root file with the histograms contained in a dict.
    Parameters:
        file_name (string): It is the name that the .root file will have.
        dict_Hist (dictionary): It is a dictionary where the keys are the names
        of the histograms and the values are the TH1F histograms .
    """
    if not isinstance(file_name, str):
        raise TypeError("name must be a string")
    if not all(isinstance(h, ROOT.TH1F) for h in dict_Hist.values()):
        raise TypeError("dict_Hist must be a dictionary of TH1F histograms")

    ROOT_File = ROOT.TFile.Open(file_name, 'RECREATE')

    [dict_Hist[key].SetName(key) for key in dict_Hist.keys()]
    [dict_Hist[key].Write() for key in dict_Hist.keys()]

    ROOT_File.Close()


def get_root_file_keys(path_root_file: str) -> dict:
    """
    This function returns the keys of the histograms contained in a root file.
    Parameters:
        path_root_file (string): It is the path of the root file.

    Returns:
        keys (list): It is a list with the names of the histograms that are in
        the root file.
    """
    file = uproot.open(path_root_file)
    keys = [key.replace(';1', '') for key in file.keys()]
    file.close()
    return keys


def read_root_file(path_root_file: str, expected_keys: list) -> dict:
    """
    This function reads a root file and returns a dictionary with the histos
    contained in the root file.
    Parameters:
        path_root_file (string): It is the path of the root file.
        expected_keys (list): It is a list with the names of the histograms
        that are expected to be in the root file.

    Returns:
        dictionary: It is a dictionary where the keys are the names of the
        histograms and the values are the histograms.
    """
    Dict_hist = {}
    File = ROOT.TFile.ROOT.TFile.Open(path_root_file, 'READ')
    for key in expected_keys:
        histogram = File.Get(key)
        try:
            histogram.SetDirectory(0)
        except AttributeError:
            pass
        Dict_hist[key] = histogram
    File.Close()
    return Dict_hist
