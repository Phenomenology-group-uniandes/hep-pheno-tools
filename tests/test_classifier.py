import pytest
import ROOT
import os
from ..delphes_reader.classifier import (
    jets_NAMES_DIC,
    DEFAULT_CUTS,
    get_met,
    get_muons,
    get_electrons,
    get_unified,
    get_leptons,
    get_jets,
    get_good_particles,
    get_good_jets,
    get_good_leptons
)
from ..delphes_reader.particles import (
    MetParticle,
    MuonParticle,
    ElectronParticle
)
from ..analysis_tools import Quiet


@pytest.fixture
def event():
    with Quiet():
        tree = ROOT.TChain("Delphes")
        tree.Add(
            os.path.join(os.getcwd(), "tests", "data", "delphes_test.root")
            )
        return next(iter(tree))


@pytest.fixture
def tree():
    with Quiet():
        tree = ROOT.TChain("Delphes")
        tree.Add(
            os.path.join(os.getcwd(), "tests", "data", "delphes_test.root")
            )
        return tree


def test_get_met(event):
    met = get_met(event)
    assert isinstance(met, MetParticle)


def test_get_muons(event):
    muons = get_muons(event)
    assert isinstance(muons, list)
    assert all(isinstance(muon, MuonParticle) for muon in muons)
    assert all(muons[i].pt >= muons[i+1].pt for i in range(len(muons)-1))
    assert len(muons) == event.Muon.GetEntries()


def test_get_electrons(event):
    electrons = get_electrons(event)
    assert isinstance(electrons, list)
    assert all(
        isinstance(electron, ElectronParticle) for electron in electrons
        )
    assert all(
        electrons[i].pt >= electrons[i+1].pt for i in range(len(electrons)-1)
        )
    assert len(electrons) == event.Electron.GetEntries()


def test_get_unified(event):
    muons = get_muons(event)
    electrons = get_electrons(event)
    unified = get_unified({"muon": muons, "electron": electrons})
    assert set(unified.keys()) == set(["all"])
    assert all(
        unified["all"][i].pt >= unified["all"][i+1].pt
        for i in range(len(unified["all"])-1)
        )
    n_muons = event.Muon.GetEntries()
    n_electrons = event.Electron.GetEntries()
    assert len(unified["all"]) == n_muons + n_electrons
    assert all(p in unified["all"] for p in muons)
    assert all(p in unified["all"] for p in electrons)


def test_get_leptons(event):
    leptons = get_leptons(event)
    assert set(leptons.keys()) == set(["muon", "electron"])

    n_muons = event.Muon.GetEntries()
    n_electrons = event.Electron.GetEntries()
    assert len(get_unified(leptons)["all"]) == n_muons + n_electrons


def test_get_jets(event):
    jets = get_jets(event)
    assert set(jets.keys()) == set(["l_jet", "b_jet", "tau_jet", "other_jet"])
    assert len(get_unified(jets)["all"]) == event.Jet.GetEntries()


def pretest_get_good_particles(event, kinematic_cuts=None):
    muons = get_muons(event)
    electrons = get_electrons(event)
    jets = get_jets(event)

    good_particles = get_good_particles(
        {
            "muon": muons,
            "electron": electrons,
            "l_jet": jets["l_jet"],
            "b_jet": jets["b_jet"],
            "tau_jet": jets["tau_jet"],
            "other_jet": jets["other_jet"]
        },
        kinematic_cuts
    )

    if kinematic_cuts is None:
        kinematic_cuts = DEFAULT_CUTS

    part_keys = ["muon", "electron", "l_jet", "b_jet", "tau_jet", "other_jet"]

    assert set(good_particles.keys()) == set(part_keys)

    for key in part_keys:
        assert all(
          p.pt > kinematic_cuts[key].get("pt_min_cut")
          for p in good_particles[key]
          )

        assert all(
            p.pt < kinematic_cuts[key].get("pt_max_cut", 1e10)
            for p in good_particles[key]
            )

        assert all(
            abs(p.eta) > kinematic_cuts[key].get("eta_min_cut")
            for p in good_particles[key]
            )

        assert all(
            abs(p.eta) < kinematic_cuts[key].get("eta_max_cut")
            for p in good_particles[key]
            )

    all_good_particles = get_unified(good_particles)["all"]
    for i in range(len(all_good_particles)):
        for j in range(i+1, len(all_good_particles)):
            assert all_good_particles[i].delta_R(all_good_particles[j]) >= 0.3


def test_get_good_particles_tree(tree):
    list(map(pretest_get_good_particles, tree, [None]*tree.GetEntries()))

    cut = {
        "pt_min_cut": 100.,
        "pt_max_cut": 500.,
        "eta_min_cut": -1.8,
        "eta_max_cut": +1.8
        }
    kinematic_cuts = {
        "muon": cut,
        "electron": cut,
        "l_jet": cut,
        "b_jet": cut,
        "tau_jet": cut,
        "other_jet": cut
    }
    list(map(
        pretest_get_good_particles, tree, [kinematic_cuts]*tree.GetEntries())
        )


def test_get_good_leptons(tree):
    for event in tree:
        good_leptons = get_good_leptons(event)

        # Check name of leptons
        assert all(lepton.name.startswith("lep_") for lepton in good_leptons)

        # Check that have a unique name
        assert len(
            set(lepton.name for lepton in good_leptons)
            ) == len(good_leptons)

        # Check that are sorted by pt
        assert all(
            good_leptons[i].pt >= good_leptons[i+1].pt
            for i in range(len(good_leptons)-1)
            )

        # Check that name is sorted by pt
        assert all(
            good_leptons[i].name < good_leptons[i+1].name
            for i in range(len(good_leptons)-1)
            )

        # Check that comes from electrons or muons
        assert all(
            lepton.kind == "electron" or lepton.kind == "muon"
            for lepton in good_leptons
            )


def pretest_good_jets(good_jets):
    for key in good_jets.keys():
        assert all(
            jet.name.startswith(jets_NAMES_DIC[key]+"_")
            for jet in good_jets[key]
        )
        assert len(
            set(jet.name for jet in good_jets[key])
            ) == len(good_jets[key])
        assert all(
            good_jets[key][i].pt >= good_jets[key][i+1].pt
            for i in range(len(good_jets[key])-1)
            )
        assert all(
            good_jets[key][i].name < good_jets[key][i+1].name
            for i in range(len(good_jets[key])-1)
            )
        assert all(jet.kind == key for jet in good_jets[key])


def test_get_good_jets(tree):
    [pretest_good_jets(get_good_jets(event)) for event in tree]
