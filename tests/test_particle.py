import pytest
from ROOT import TLorentzVector
from ..abstract_particle import Particle


@pytest.fixture
def particle():
    return Particle(charge=-1.0, name="e-", kind="electron")


def test_particle_creation(particle):
    assert isinstance(particle, Particle)
    assert isinstance(particle.tlv, TLorentzVector)
    assert particle.charge == -1.0
    assert particle.name == "e-"
    assert particle.kind == "electron"


def test_set_good_tag(particle):
    particle.set_good_tag(1)
    assert particle.good_tag == 1
    with pytest.raises(ValueError):
        particle.set_good_tag(2)
    with pytest.raises(ValueError):
        particle.set_good_tag(-1)


def test_get_good_tag(particle):
    particle.set_good_tag(1)
    assert particle.get_good_tag(None) == 1


def test_pt(particle):
    particle.tlv.SetPtEtaPhiM(50, 1.5, 0.5, 0.5)
    assert particle.pt == 50


def test_p(particle):
    particle.tlv.SetPtEtaPhiM(5, 0.97545, 0.95055, 0.5)
    assert particle.p == pytest.approx(7.5734, rel=1e-5)


def test_pl(particle):
    particle.tlv.SetPtEtaPhiM(5, 0.97545, 0.95055, 0.5)
    assert particle.pl == pytest.approx(5.6883, rel=1e-5)


def test_eta(particle):
    particle.tlv.SetPtEtaPhiM(5, 0.97545, 0.95055, 0.5)
    assert particle.eta == pytest.approx(0.97545, rel=1e-5)


def test_phi(particle):
    particle.tlv.SetPtEtaPhiM(5, 0.97545, 0.95055, 0.5)
    assert particle.phi == pytest.approx(0.95055, rel=1e-5)


def test_m(particle):
    particle.tlv.SetPtEtaPhiM(5, 0.97545, 0.95055, 0.5)
    assert particle.m == pytest.approx(0.5, rel=1e-5)


def test_energy(particle):
    particle.tlv.SetPtEtaPhiM(5, 0.97545, 0.95055, 0.5)
    assert particle.energy == pytest.approx(7.5899, rel=1e-5)


def test_get_charge(particle):
    assert particle.get_charge() == -1.0


def test_get_name(particle):
    assert particle.get_name() == "e-"


def test_set_name(particle):
    particle.set_name("positron")
    assert particle.name == "positron"


def test_delta_eta(particle):
    particle1 = Particle(charge=1.0, name="p", particle_type="proton")
    particle1.tlv.SetPtEtaPhiM(5, 0.97545, 0.95055, 0.5)
    particle2 = Particle(charge=-1.0, name="p", particle_type="proton")
    particle2.tlv.SetPtEtaPhiM(5, 1.3316, -2.19199, 0.5)

    assert particle1.delta_eta(particle2) == pytest.approx(-0.35615, rel=1e-5)
    assert particle2.delta_eta(particle1) == pytest.approx(0.35615, rel=1e-5)


def test_delta_phi(particle):
    particle1 = Particle(charge=1.0, name="p", particle_type="proton")
    particle1.tlv.SetPtEtaPhiM(5, 0.97545, 0.95055, 0.5)
    particle2 = Particle(charge=-1.0, name="p", particle_type="proton")
    particle2.tlv.SetPtEtaPhiM(5, -0.35615, -2.19199, 0.5)

    assert particle1.delta_phi(particle2) == pytest.approx(-3.14064, rel=1e-5)
    assert particle2.delta_phi(particle1) == pytest.approx(3.14064, rel=1e-5)


def test_delta_r(particle):
    particle1 = Particle(charge=1.0, name="p", particle_type="proton")
    particle1.tlv.SetPtEtaPhiM(5.09902, 1.236, 0.876, 0.5)
    particle2 = Particle(charge=-1.0, name="p", particle_type="proton")
    particle2.tlv.SetPtEtaPhiM(5.09902, -1.236, -2.265, 0.5)

    assert particle1.delta_R(particle2) == pytest.approx(3.99708, rel=1e-5)
    assert particle2.delta_R(particle1) == pytest.approx(3.99708, rel=1e-5)


def test_delta_pt_scalar(particle):
    assert particle.delta_pt_scalar(particle) == pytest.approx(0.0, rel=1e-5)


def test_delta_pt_vectorial(particle):
    assert particle.delta_pt_vectorial(particle) == pytest.approx(0.0)


def test_delta_p_vectorial(particle):
    assert particle.delta_p_vectorial(particle) == pytest.approx(0.0)
