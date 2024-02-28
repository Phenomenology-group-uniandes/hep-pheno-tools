import numpy as np

from ..abstract_particle import Particle


class LHEParticle(Particle):
    def __init__(self, pdgid, spin, px=0, py=0, pz=0, energy=0, mass=0):
        self.pdgid = pdgid
        typep = abs(pdgid)
        if (typep == 2) or (typep == 4) or (typep == 6):
            charge = np.sign(pdgid) * 2.0 / 3.0
        elif (typep == 1) or (typep == 3) or (typep == 5):
            charge = -np.sign(pdgid) * 1.0 / 3.0
        elif (typep == 11) or (typep == 13) or (typep == 15):
            charge = -np.sign(pdgid)
        else:
            charge = 0.0

        super().__init__(charge=float(charge))
        self.px = px
        self.py = py
        self.pz = pz
        # self.energy = energy
        self.tlv.SetPxPyPzE(px, py, pz, energy)
        self.mass = mass
        self.spin = spin
