import pytest
import numpy as np
from ..analysis_tools.power_tests import approx_global_sig


def test_approx_global_sig_with_valid_input():
    # Test that the function returns a float
    sig = np.array([1, 2, 3])
    bkg = np.array([4, 5, 6])
    assert isinstance(approx_global_sig(sig, bkg), float)

    # Test that the function returns the correct value
    assert pytest.approx(approx_global_sig(sig, bkg), 0.01) == 1.33


def test_approx_global_sig_with_non_numpy_input():
    # Test that the function raises a TypeError if sig is not a numpy array
    sig = [1, 2, 3]
    bkg = np.array([4, 5, 6])
    with pytest.raises(TypeError):
        approx_global_sig(sig, bkg)

    # Test that the function raises a TypeError if bkg is not a numpy array
    sig = np.array([1, 2, 3])
    bkg = [4, 5, 6]
    with pytest.raises(TypeError):
        approx_global_sig(sig, bkg)


def test_approx_global_sig_with_invalid_input():
    # Test that the function raises a ValueError if sig and bkg are not 1D
    sig = np.array([[1, 2], [3, 4]])
    bkg = np.array([[5, 6], [7, 8]])
    with pytest.raises(ValueError):
        approx_global_sig(sig, bkg)

    # Test error raised if sig and bkg have different lengths
    sig = np.array([1, 2, 3])
    bkg = np.array([4, 5])
    with pytest.raises(ValueError):
        approx_global_sig(sig, bkg)

    # Test that the function raises a ValueError if N is not a positive float
    sig = np.array([1, 2, 3])
    bkg = np.array([4, 5, 6])
    N = -1.0
    with pytest.raises(ValueError):
        approx_global_sig(sig, bkg, N)
