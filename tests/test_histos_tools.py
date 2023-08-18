import pytest
import numpy as np
from ..analysis_tools.histos_tools import (
    get_hist_bins_by_column
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
