from ...abstract_particle import Particle
import random

JET_TYPES = {
        "BTag0_TauTag0": "l_jet",
        "BTag1_TauTag0": "b_jet",
        "BTag0_TauTag1": "tau_jet"
}


class JetParticle(Particle):
    ''' Particle class object JetParticle:

        Attributes:

        tlv: TLorentzVector that is defining using Pt, Eta, Phi and Mass.
        charge: Particle charge.
        name: Particle Name (examples: l_jet_1, l_jet_2, etc.).
        type: Particle type (examples: l_jet, b_jet, tau_jet, other_jet).
        b_tag: Particle BTag, it could be 0 or 1.
        tau_tag: Particle TauTag, it could be 0 or 1.
        c_tag: Particle CTag, it could be 0 or 1.
        flavor: Particle flavor, it could be 4 for a charm quark or 5 for a
        bottom quark.

    Methods:
        c_tagging: Determines the CTag attribute based on the Flavor attribute
        and a random number.

    '''

    def __init__(self, event, j):
        ''' Initialize JetParticle extracting attribute values from a delphes
        file (.root) event.

        Parameters:
            event (pyroot.TTree): Delphes event containing particle
            information.
            j (int): Jet index in the Delphes event.

        '''
        super().__init__()
        self.tlv.SetPtEtaPhiM(
            event.GetLeaf("Jet.PT").GetValue(j),
            event.GetLeaf("Jet.Eta").GetValue(j),
            event.GetLeaf("Jet.Phi").GetValue(j),
            event.GetLeaf("Jet.Mass").GetValue(j)
        )
        self.flavor = int(event.GetLeaf("Jet.Flavor").GetValue(j))
        self.c_tag = int(self.c_tagging())
        self.b_tag = int(event.GetLeaf("Jet.BTag").GetValue(j))
        self.tau_tag = int(event.GetLeaf("Jet.TauTag").GetValue(j))
        self.charge = event.GetLeaf("Jet.Charge").GetValue(j)
        self.kind = self._jet_type()
        self.name = f'{self.kind}_{{{j}}}'

    def _jet_type(self):
        ''' Estimates the jet type based on the BTag and TauTag attributes.

        Returns:
            str: particle type.
        '''
        tag = f'BTag{self.b_tag}_TauTag{self.tau_tag}'
        return JET_TYPES.get(tag, "other_jet")

    def c_tagging(self):
        ''' Determines the CTag attribute based on the Flavor attribute and a
        random number.

        For charm jets the method returns 1 with a 70% probability, and for
        all other jets it returns 1 with a 1% probability.

        Returns:
            int: CTag, which could be 0 or 1.
        '''
        random_number = random.random()
        # efficiency of charm tagging
        if (self.flavor == 4 and random_number < 0.7):
            return 1
        # misidentification rate
        elif (self.flavor != 4 and random_number < 0.01):
            return 1
        # no charm tagging
        else:
            return 0
