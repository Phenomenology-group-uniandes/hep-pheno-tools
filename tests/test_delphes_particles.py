import pytest
import os
from ..abstract_particle import Particle
from ..delphes_reader.particles import ElectronParticle
from ..analysis_tools import Quiet

import ROOT


@pytest.fixture
def event():
    with Quiet():
        tree = ROOT.TChain("Delphes")
        tree.Add(
            os.path.join(os.getcwd(), "tests", "data", "delphes_test.root")
            )
        return next(iter(tree))


def test_electron_particle(event):
    # Initialize an ElectronParticle object
    electron = ElectronParticle(event, 0)

    # Test that the object is a Particle
    assert isinstance(electron, Particle)

    # Test the TLV attribute
    assert isinstance(electron.tlv, ROOT.TLorentzVector)
    assert electron.p == pytest.approx(187.9219, rel=1e-3)
    assert electron.pt == pytest.approx(187.90409, rel=1e-3)
    assert electron.eta == pytest.approx(-0.01377586, rel=1e-3)
    assert electron.phi == pytest.approx(2.29576, rel=1e-3)
    assert electron.m == pytest.approx(0.000511, rel=1e-3)
    assert electron.energy == pytest.approx(187.9219, rel=1e-3)
    # Test the Charge attribute
    assert electron.charge == 1

    # Test the Name attribute
    assert electron.name == "e"

    # Test the Type attribute
    assert electron.kind == "electron"
