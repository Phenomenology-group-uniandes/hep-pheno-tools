class Event:
    def __init__(self, num_particles):
        self.num_particles = num_particles
        self.particles = []

    def __addParticle__(self, particle):
        self.particles.append(particle)

    def getParticlesByIDs(self, idlist):
        partlist = [p for p in self.particles if p.pdgid in idlist]
        return partlist
