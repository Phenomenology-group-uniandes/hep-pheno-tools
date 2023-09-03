class LHEFData:
    def __init__(self, version):
        self.version = version
        self.events = []

    def __addEvent__(self, event):
        self.events.append(event)

    def getParticlesByIDs(self, idlist):
        partlist = []
        for event in self.events:
            partlist.extend(event.getParticlesByIDs(idlist))
        return partlist
