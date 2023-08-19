import pytest
import numpy as np
import pandas as pd
import ROOT
from ..analysis_tools.histos_tools import (
    get_hist_bins_by_column,
    make_histograms
)


def test_get_hist_bins_by_column():
    # Test that the function raises a TypeError if column is not a numpy array
    with pytest.raises(TypeError):
        get_hist_bins_by_column([1, 2, 3])

    # Test that the function raises a ValueError if column is not 1d
    with pytest.raises(ValueError):
        get_hist_bins_by_column(np.array([[1, 2], [3, 4]]))

    # Test that the function returns the correct bins for a case with all zeros
    zeros_array = np.zeros(100)
    assert get_hist_bins_by_column(zeros_array) == [7, 0.0, 0.0]

    # Test that the function returns the correct bins for a simple case
    column = np.array([i for i in range(20+1)])
    bins = get_hist_bins_by_column(column)
    assert bins == [5, 0, 20]

    # Test that the function returns the correct bins for a case with
    # negative values
    column = np.array([-10, -5, 0, 5, 10])
    bins = get_hist_bins_by_column(column)
    assert bins == [3, -10, 10]

    # Test that the function returns the correct bins for a case with
    # repeated values
    column = np.array([1, 2, 3, 3, 4, 5, 5, 5, 6, 7, 8, 9, 10])
    bins = get_hist_bins_by_column(column)
    assert bins == [4, 1, 10]


def test_make_histograms_with_default_bins():
    # Test that the function returns a dictionary
    df = pd.DataFrame({
        'x': [1, 2, 3, 3, 4, 5, 5, 5, 6, 7, 8, 9, 10],
        'y': [1, 2, 3, 3, 4, 5, 5, 5, 6, 7, 8, 9, 10]}
        )
    hist_dict = make_histograms(df)
    assert isinstance(hist_dict, dict)

    # Test that the function returns histograms
    assert any([isinstance(hist, ROOT.TH1F) for hist in hist_dict.values()])

    # Test that the function returns the correct number of histograms
    assert len(hist_dict) == 2

    # Test that the function returns histograms with the correct names
    assert 'x' in hist_dict
    assert 'y' in hist_dict

    # Test that the function returns histograms with the correct number of bins
    assert hist_dict['x'].GetNbinsX() == 4
    assert hist_dict['y'].GetNbinsX() == 4

    # Test that the function returns histograms with the correct integral
    assert pytest.approx(hist_dict['x'].Integral()) == 1.0
    assert pytest.approx(hist_dict['y'].Integral()) == 1.0


def test_make_histograms_with_custom_bins():
    # Test that the function returns histograms with the correct number of bins
    df = pd.DataFrame({'x': [1, 2, 3, 4], 'y': [4, 5, 6, 7]})
    hist_bins_dict = {'x': [5, 0, 10], 'y': [5, 0, 10]}
    hist_dict = make_histograms(df, hist_bins_dict=hist_bins_dict)
    assert hist_dict['x'].GetNbinsX() == 5
    assert hist_dict['y'].GetNbinsX() == 5

    # Test that the function returns histograms with the correct integral
    assert hist_dict['x'].Integral() == 1.0
    assert hist_dict['y'].Integral() == 1.0


def test_make_histograms_with_non_numeric_bins():
    # Test that the function raises a TypeError if hist_bins_dict values are
    # not numeric
    df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    hist_bins_dict = {'x': [5, 0, 10], 'y': ['a', 'b', 'c']}
    with pytest.raises(TypeError):
        make_histograms(df, hist_bins_dict=hist_bins_dict)


def test_make_histograms_with_non_dataframe_input():
    # Test that the function raises a TypeError if df is not a pandas DataFrame
    with pytest.raises(TypeError):
        make_histograms([1, 2, 3])


def test_make_histograms_with_non_float_integral():
    # Test that the function raises a TypeError if integral is not a float
    df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    with pytest.raises(TypeError):
        make_histograms(df, integral='a')
