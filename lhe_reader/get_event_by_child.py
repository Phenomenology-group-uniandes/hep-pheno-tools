from .event import Event
from .lhe_particle import LHEParticle as Particle


def get_event_by_child(child):
    lines = child.text.strip().split('\n')
    event_header = lines[0].strip()
    num_part = int(event_header.split()[0].strip())
    e = Event(num_part)
    for i in range(1, num_part+1):
        part_data = lines[i].strip().split()
        if (int(part_data[1]) != 1):
            continue

        p = Particle(
            int(part_data[0]),  # pdg-id
            float(part_data[12]),  # spin
            float(part_data[6]),  # px
            float(part_data[7]),  # py
            float(part_data[8]),  # pz
            float(part_data[9]),  # E
            float(part_data[10])  # m
        )
        e.__addParticle__(p)
    return e
