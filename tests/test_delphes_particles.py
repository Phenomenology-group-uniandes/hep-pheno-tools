import pytest
import os
from ..abstract_particle import Particle
from ..delphes_reader.particles import ElectronParticle
from ..delphes_reader.particles import JetParticle
from ..delphes_reader.particles import MetParticle
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


def test_jet_particle(event):
    # Create a JetParticle object
    jet = JetParticle(event, 0)
    # Check that the object attributes were initialized correctly
    assert jet.kind == 'l_jet'
    assert jet.name == 'l_jet_{0}'
    assert jet.b_tag in [0, 1]
    assert jet.tau_tag in [0, 1]
    assert jet.c_tag in [0, 1]
    assert jet.flavor in [0, 1, 2, 3, 4, 5, 22]
    assert isinstance(jet.charge, float)

    # Test the TLV attribute
    assert isinstance(jet.tlv, ROOT.TLorentzVector)
    assert jet.p == pytest.approx(127.211, rel=1e-3)
    assert jet.pt == pytest.approx(122.89, rel=1e-3)
    assert jet.eta == pytest.approx(-0.26433, rel=1e-3)
    assert jet.phi == pytest.approx(-1.5713, rel=1e-3)
    assert jet.m == pytest.approx(4.2627, rel=1e-3)
    assert jet.energy == pytest.approx(127.211, rel=1e-3)


def test_muon_particle(event):
    met_particle = MetParticle(event)
    assert isinstance(met_particle, MetParticle)
    assert met_particle.charge == 0.0
    assert met_particle.name == "MET"
    assert met_particle.kind == "MET"
    # Test the TLV attribute
    assert isinstance(met_particle.tlv, ROOT.TLorentzVector)
    assert met_particle.p == pytest.approx(69.636, rel=1e-3)
    assert met_particle.pt == pytest.approx(69.636, rel=1e-3)
    assert met_particle.energy == pytest.approx(69.636, rel=1e-3)
    assert met_particle.phi == pytest.approx(0.45084, rel=1e-3)
    assert met_particle.eta == pytest.approx(0.0, abs=1e-3)
    assert met_particle.pl == pytest.approx(0.0, abs=1e-3)
    assert met_particle.m == pytest.approx(0.0, abs=1e-3)
