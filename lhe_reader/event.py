from ROOT import TLorentzVector

from .lhe_particle import LHEParticle


class Event:
    def __init__(self, num_particles):
        self.num_particles = num_particles
        self.particles = []

    def __addParticle__(self, particle):
        self.particles.append(particle)

    def getParticlesByIDs(self, idlist):
        partlist = [p for p in self.particles if p.pdgid in idlist]
        return partlist

    def getMissingET(self, idlist: list = [12, 14, 16, -12, -14, -16]):
        met_list = self.getParticlesByIDs(idlist)
        met_pdgid = 0
        met_spin = 0
        met_px = sum([p.px for p in met_list])
        met_py = sum([p.py for p in met_list])
        met_pz = 0  # Is Missing ET
        met_e = sum([p.e for p in met_list])
        met_mass = TLorentzVector(met_px, met_py, met_pz, met_e).M()
        met = LHEParticle(met_pdgid, met_spin, met_px, met_py, met_pz, met_e, met_mass)
        return met
