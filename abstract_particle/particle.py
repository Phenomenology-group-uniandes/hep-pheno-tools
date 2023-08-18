from abc import ABC
from ROOT import (
    TLorentzVector,
    TVector3,
    TVector2,
    TMath
)


class Particle(ABC):
    '''
    Abstract base class for particles in high-energy physics experiments.

    Attributes:
    -----------
    tlv : TLorentzVector
        A TLorentzVector representing the four-momentum of the particle, 
        defined by its transverse momentum (Pt), pseudorapidity (Eta), 
        azimuthal angle (Phi), and mass (M).
    charge : float
        The electric charge of the particle.
    name : str
        The name of the particle, e.g. "#mu", "e", "MET", etc.
    Type : str
        The kind of the particle, e.g. "muon", "electron", "MET", etc.

    Methods:
    --------
    get_charge() -> float:
        Returns the electric charge of the Particle object.

    get_tlv() -> TLorentzVector:
        Returns the 4-momentum of the Particle object as a TLorentzVector.

    get_name() -> str:
        Returns the name of the Particle object.

    set_name(new_name: str) -> None:
        Sets the name of the Particle object to the new name provided as an 
        argument.

    set_good_tag(value: int) -> None:
        Sets the good_tag label of the particle.

    get_good_tag(cuts: dict) -> int:
        Defines and returns a label (good_tag) that indicates if the particle 
        is within the range of kinematic cuts (Pt_min, Pt_max, Eta_min, 
        Eta_max).
        good_tag could have two values:
            1: Particle is within the range of kinematic cuts.
            0: Particle is not within the range of kinematic cuts.
        Parameters:
            cuts (dict): A dictionary containing the values of kinematic cuts.
            It should have the keys "pt_min_cut", "pt_max_cut" (optional), 
            "eta_min_cut" and "eta_max_cut".
        Returns:
        int: good_tag.

    delta_R(v2: Particle) -> float:
        Calculates and returns DeltaR metric between particle (self) and 
        another Particle object (v2).
        Parameters:
            v2 (Particle): Another particle to calculate 
            DeltaR respect to the main particle (self).
        Returns:
            float: DeltaR.

    delta_eta(v2: Particle) -> float:
        Calculates and returns DeltaEta metric between particle (self) and
        another Particle object (v2).
        Parameters:
            v2 (Particle): Another particle to calculate
            DeltaEta respect to the main particle (self).
        Returns:
            float: DeltaEta.

    delta_phi(v2: Particle) -> float:

    Properties:
    --------
    p : float
        Returns the full momentum (P) of the particle, which is the magnitude 
        of the three-momentum vector.

    pl : float
        Returns the longitudinal momentum (P_L) of the particle, which is the
        component of the momentum parallel to the beam direction.

    eta : float
        Returns the pseudorapidity (Eta) of the particle, which is related to
        the polar angle of the momentum vector in the detector frame.

    phi : float
        Returns the azimuthal angle (Phi) of the particle, which is the angle
        between the transverse momentum vector and a reference axis in the 
        transverse plane.

    m : float
        Returns the reconstructed mass (M) of the particle, which is calculated
        from the four-momentum vector.

    energy : float
        Returns the reconstructed energy (E) of the particle, which is the time
        component of the four-momentum vector.

    Notes:
    ------
    This is an abstract base class that cannot be instantiated on its own. It 
    blueprint for subclasses that inherit its attributes and methods. Subclasses
    should implement their own methods according to their specific use case.
    '''
    def __init__(self, **kwargs):
        '''Initializes a new Particle object.

        Keyword Args:
            charge (float): The particle's electric charge (default: 0.0).
            name (str): The particle's name (default: "").
            particle_kind (str): The particle's kind (default: "").

        Raises:
            TypeError: If any of the arguments is of the wrong kind.
        '''
        self.tlv = TLorentzVector(0, 0, 0, 0)
        self.charge = kwargs.get("charge", 0.0)
        self.name = kwargs.get("name", "")
        self.kind = kwargs.get("kind", "")

        if not isinstance(self.tlv, TLorentzVector):
            raise TypeError("tlv must be a TLorentzVector object")
        if not isinstance(self.charge, float):
            raise TypeError("charge must be a float")
        if not isinstance(self.name, str):
            raise TypeError("name must be a string")
        if not isinstance(self.kind, str):
            raise TypeError("kind must be a string")

    def get_charge(self):
        ''' Returns charge (attribute) of particle.
        Returns:
            float: charge.
        '''
        return self.charge

    def get_tlv(self):
        ''' Returns tlv (attribute) of particle (this tlv is definning with Pt,
        Eta, Phi and M).
        Returns:
            TLorentzVector: tlv.
        '''
        return self.tlv

    def get_name(self):
        ''' Returns name (attribute) of particle
        Returns:
            str: name.
        '''
        return self.name

    def set_name(self, new_name: str) -> None:
        '''Sets the name of the Particle object to the new name provided as an 
        argument.
        Args:
            new_name (str): The new name to assign to the particle.
        Returns:
            None
        '''
        self.name = new_name

    @property
    def pt(self) -> float:
        '''Returns the transverse momentum (Pt) of the Particle object.
        Returns:
            float: The transverse momentum (Pt) of the particle.
        '''
        tlv = self.tlv
        return tlv.Pt()

    @property
    def p(self) -> float:
        '''Returns the full momentum (P) of the Particle object.
        Returns:
            float: The full momentum (P) of the particle.
        '''
        return self.tlv.P()

    @property
    def pl(self) -> float:
        '''Returns the longitudinal momentum of the Particle object.

        The longitudinal momentum is calculated using the full momentum (P) and 
        transverse momentum (Pt).

        Returns:
            float: The longitudinal momentum of the particle.
        '''
        p = self.tlv.P()
        pt = self.tlv.Pt()
        return TMath.Sqrt((p - pt) * (p + pt))

    @property
    def eta(self) -> float:
        '''Returns the pseudorapidity (Eta) of the Particle object.

        Returns:
            float: The pseudorapidity (Eta) of the particle.
        '''
        tlv = self.tlv
        return tlv.Eta()

    @property
    def phi(self) -> float:
        '''Returns the azimuthal angle (Phi) of the Particle object.

        Returns:
            float: The azimuthal angle (Phi) of the particle.
        '''
        phi = self.tlv.Phi()
        return phi

    @property
    def m(self) -> float:
        '''Returns the reconstructed mass (M) of the Particle object.

        Returns:
            float: The reconstructed mass (M) of the particle.
        '''
        return self.tlv.M()

    @property
    def energy(self) -> float:
        '''Returns the reconstructed energy of the Particle object.

        Returns:
            float: The reconstructed energy of the particle.
        '''
        return self.tlv.Energy()

    def set_good_tag(self, value):
        ''' Sets the good_tag label of the particle.

        Parameters:
            value (int): good_tag to be set. It should be 0 or 1.
        '''
        if value not in [0, 1]:
            raise ValueError("Error: good_tag value should be 0 or 1.")
        self.good_tag = value

    def get_good_tag(self,cuts):
        ''' Define and returns a label (good_tag) that indicate if particle is 
        within the range of kinematic cuts (Pt_min, Pt_max, Eta_min, Eta_max). 

        good_tag could have two values: 
        1: Particle is within the range of kinematic cuts.
        0: Particle is not within the range of kinematic cuts.

        Parameters:
            cuts (dict): contains the values of kinematic cuts. It should have 
            the keys "pt_min_cut", "pt_max_cut" (optional), "eta_min_cut" and 
            "eta_max_cut".

        Returns:
            float: good_tag.
        '''
        kin_cuts = cuts.get(self.Type)

        pt_min_cut = kin_cuts.get("pt_min_cut")
        pt_max_cut = kin_cuts.get("pt_max_cut")#optional
        eta_min_cut = kin_cuts.get("eta_min_cut")
        eta_max_cut = kin_cuts.get("eta_max_cut")

        pt_cond = (self.pt >= pt_min_cut)
        if pt_max_cut:
            if not (pt_max_cut > pt_min_cut):
                raise Exception("Error: pt_max must be major than pt_min")
            pt_cond = pt_cond and (self.pt <= pt_max_cut)
        eta_cond = (self.eta >= eta_min_cut) and (self.eta <= eta_max_cut)

        if (pt_cond and eta_cond):
            self.set_good_tag(1)
        else:
            self.set_good_tag(0)

        return self.good_tag

    # Delta methods
    def delta_R(self, v2):
        ''' Calculates and returns DeltaR between particle (self) and other 
        object of particle class (v2).
   
        Parameters:
            v2 (Particle): Another particle to calculate DeltaR respect to the 
            main particle (self).

        Returns:
            float: DeltaR.
        '''
        tlv1 = self.tlv
        tlv2 = v2.get_tlv()
        return tlv1.DeltaR(tlv2)

    def delta_eta(self, v2):
        ''' Calculates and returns DeltaEta between particle (self) and other 
        object of particle class (v2).

        Parameters:
            v2 (Particle: Another particle to calculate DeltaEta respect to the 
            main particle (self).

        Returns:
            float: DeltaEta.
        '''
        tlv1 = self.tlv
        tlv2 = v2.get_tlv()
        return (tlv1.Eta() - tlv2.Eta())

    def delta_phi(self, v2):
        ''' Calculates and returns DeltaPhi between particle (self) and other 
        object of particle class (v2).

        Parameters:
            v2 (Particle): Another particle to calculate DeltaPhi respect to 
            the main particle (self).

        Returns:
            float: DeltaPhi.
        '''
        tlv1 = self.tlv
        tlv2 = v2.get_tlv()
        return tlv1.DeltaPhi(tlv2)

    def delta_pt_scalar(self, v2):
        ''' Calculates and returns sDeltaPT (s - scalar) between particle 
        (self) and other object of particle class (v2).

        Parameters:
            v2 (Particle): Another particle to calculate sDeltaPT respect to 
            the main particle (self).

        Returns:
            float: sDeltaPT.
        '''
        tlv1 = self.tlv
        tlv2 = v2.get_tlv()
        return (tlv1.Pt() - tlv2.Pt())

    def delta_pt_vectorial(self, v2):
        ''' Calculates and returns vDeltaPT (v - vectorial) 
        between particle 
        (self) and other object of particle class (v2).

        Parameters:
            v2 (Particle): Another particle,
            the main particle (self).

        Returns:
            float: vDeltaPT.
        '''
        tlv1 = self.tlv
        tlv2 = v2.get_tlv()
        a = TVector2(tlv1.Px(), tlv1.Py())
        b = TVector2(tlv2.Px(), tlv2.Py())
        c = a-b
        return c.Mod()

    def delta_p_vectorial(self, v2):
        ''' Calculates and returns vDeltaP (v - vectorial) between particle 
        (self) and other object of particle class (v2).

        Parameters:
            v2 (Particle): Another particle to calculate vDeltaP respect to the 
            main particle (self).

        Returns:
            float: vDeltaP.
        '''
        tlv1 = self.tlv
        tlv2 = v2.get_tlv()
        a = TVector3(tlv1.Px(), tlv1.Py(), tlv1.Pz())
        b = TVector3(tlv2.Px(), tlv2.Py(), tlv2.Pz())
        c = a-b
        return c.Mag()
