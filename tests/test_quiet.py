import ROOT
from ..analysis_tools import Quiet


def test_quiet_ignore_level():
    old_level = ROOT.gErrorIgnoreLevel
    with Quiet(level=2000):
        assert ROOT.gErrorIgnoreLevel == 2000
    with Quiet(level=1000):
        assert ROOT.gErrorIgnoreLevel == 1000
    assert ROOT.gErrorIgnoreLevel == old_level
