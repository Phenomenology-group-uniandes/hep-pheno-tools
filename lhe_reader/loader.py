from ..delphes_reader.loader import DelphesLoader


class LHE_Loader(DelphesLoader):
    def __init__(self, name_signal, path=None):
        super().__init__(name_signal, path, glob='**/*.lhe.gz')
