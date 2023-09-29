from ...abstract_particle import Particle


class PhotonParticle(Particle):
    def __init__(self, event, j):
        super().__init__()
        self.tlv.SetPtEtaPhiM(
            event.GetLeaf("Photon.PT").GetValue(j),
            event.GetLeaf("Photon.Eta").GetValue(j),
            event.GetLeaf("Photon.Phi").GetValue(j),
            event.GetLeaf("Photon.Mass").GetValue(j),
        )
        self.charge = 0
        self.kind = "photon"
        self.name = f"{self.kind}_{{{j}}}"

        self.isolation = event.GetLeaf("Photon.IsolationVar").GetValue(j)
