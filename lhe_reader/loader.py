from ..delphes_reader.loader import DelphesLoader
from . import get_event_by_child, readLHEF


class LheLoader(DelphesLoader):
    def __init__(self, name_signal, path=None, is_bkg=False, **kwargs):
        super().__init__(name_signal, path, glob="**/*.lhe.gz", is_bkg=is_bkg, **kwargs)

    def get_unified_lhe_tree(self):
        return sum((list(map(get_event_by_child, readLHEF(tree))) for tree in self.Forest), [])
