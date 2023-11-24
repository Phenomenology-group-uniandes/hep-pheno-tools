from . import Particle


def get_kinematics_row(particles: list) -> dict:
    """Extracts main kinematic variables of a particle (or more) and returns a
    dictionary with them.

    Parameters:
        particles (list): any number of Particle objects.

    Returns:
        dict: contains main kinematic variables.
    """
    if not isinstance(particles, list):
        raise TypeError("Particles must be a list of Particle objects")

    if any(not isinstance(particle, Particle) for particle in particles):
        raise TypeError("Particles must be a list of Particle objects")

    row = {}
    for i, particle in enumerate(particles):
        # Save main kinematic variables
        name = particle.name
        row[f"pT_{{{name}}}(GeV)"] = particle.pt
        row[f"#eta_{{{name}}}"] = particle.eta
        row[f"#phi_{{{name}}}"] = particle.phi
        row[f"Energy_{{{name}}}(GeV)"] = particle.energy
        row[f"Mass_{{{name}}}(GeV))"] = particle.m

        # Calculate Delta Functions with other particles
        for j in range(i + 1, len(particles)):
            co_particle = particles[j]
            co_name = co_particle.name
            suffix = f"_{{{name}{co_name}}}"

            row[f"#Delta{{R}}{suffix}"] = particle.delta_R(co_particle)
            row[f"#Delta{{#eta}}{suffix}"] = particle.delta_eta(co_particle)
            row[f"#Delta{{#phi}}{suffix}"] = particle.delta_phi(co_particle)

            dpt1 = particle.delta_pt_scalar(co_particle)
            dpt2 = particle.delta_pt_vectorial(co_particle)
            dp = particle.delta_p_vectorial(co_particle)
            row[f"#Delta{{pT}}{suffix}(GeV)"] = dpt1
            row[f"#Delta{{#vec{{pT}}}}{suffix}(GeV)"] = dpt2
            row[f"#Delta{{#vec{{p}}}}{suffix}(GeV)"] = dp
    return row
