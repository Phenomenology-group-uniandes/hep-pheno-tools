import numpy as np


def approx_global_sig(sig: np.array, bkg: np.array, N: float = 0.0) -> float:
    """
    Calculates the statistical significance of a signal over background in a
    given dataset using a modified version of the formula
    (S -N sqrt(B))/sqrt(S+B), where S is the number of signalevents, B is the
    number of background events, and N is the expected number of background
    events in the signal region.

    Parameters:
    sig (np.array): 1D array containing the number of signal events in each bin
    of the dataset.
    bkg (np.array): 1D array containing the number of background events in each
    bin of the dataset.
    N (float): Expected number of background events in the signal region.
    Default value is 0.0.

    Returns:
    float: The statistical significance of the signal over background in the
    dataset.
    """
    # check that sig and bkg are numpy arrays
    if not isinstance(sig, np.ndarray):
        raise TypeError("sig must be a numpy array")
    if not isinstance(bkg, np.ndarray):
        raise TypeError("bkg must be a numpy array")

    # check that sig and bkg are 1D arrays
    if sig.ndim != 1:
        raise ValueError("sig must be a 1D array")
    if bkg.ndim != 1:
        raise ValueError("bkg must be a 1D array")

    # check that sig and bkg have the same length
    if len(sig) != len(bkg):
        raise ValueError("sig and bkg must have the same length")

    # check that N is a positive float
    if not isinstance(N, float) or N < 0.0:
        raise ValueError("N must be a positive float")

    # calculate weight factor w for each bin
    w = np.log(1 + sig/bkg)

    # calculate intermediate quantities
    s_w = sig * w
    s_ww = sig * w ** 2
    b_ww = bkg * w ** 2

    # calculate numerator and denominator of modified formula
    num = np.sum(s_w) - N * np.sqrt(np.sum(b_ww))
    den = np.sqrt(np.sum(s_ww + b_ww))

    # calculate statistical significance and return it
    return num / den
