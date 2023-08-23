from ...abstract_particle import Particle
from ROOT import TLorentzVector


class MetParticle(Particle):
    ''' Particle class object METParticle:

        Attributes:

        TLV: TLorentzVector that is definning using Pt, Eta, Phi and M.
        Charge: Particle charge (0.0).
        Name: Particle Name (MET).
        Type: Particle type (MET).
    '''
    def __init__(self, event):
        ''' Initialize METParticle extracting attribute values from a delphes
        file (.root) event.'''
        super().__init__()
        self.tlv = TLorentzVector(0, 0, 0, 0)
        n_met = event.MissingET.GetEntries()
        partMet = TLorentzVector()
        for j in range(n_met):
            partMet.SetPtEtaPhiM(
                event.GetLeaf("MissingET.MET").GetValue(j),
                0.00,  # ensures that we are over the x-y plane
                event.GetLeaf("MissingET.Phi").GetValue(j),
                0.00
            )
            self.tlv += partMet
        self.charge = 0.0
        self.name = "MET"
        self.kind = "MET"
