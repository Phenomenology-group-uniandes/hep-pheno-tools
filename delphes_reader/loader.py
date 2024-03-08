import csv
import os
from pathlib import Path
from urllib.request import urlopen

from ROOT import TChain


class DelphesLoader:
    """
    Class to load the delphes root outputs

    Attributes
    ----------
    name : str
        Name of the signal to load
    xs : str
        Cross section of the signal
    Forest : list
        List of the delphes root outputs

    Methods
    -------
    set_glob(glob: str) -> None
        Set the glob to search the delphes root outputs
    get_glob() -> str
        Get the glob to search the delphes root outputs
    get_nevents() -> int
        Get the number of events in the delphes root outputs
    """

    # Constructor
    def __init__(
        self,
        name_signal: str,
        path: str = os.path.join("hep_pheno_tools", "SimulationsPaths.csv"),
        is_bkg: bool = False,
        **kwargs,
    ) -> None:
        """
        Parameters
        ----------
        name_signal : str
            Name of the signal to load
        path : str
            Path to the simulation root outputs
        """

        # Name of the signal
        self.name = name_signal

        if is_bkg:
            # Path to the simulation root outputs
            data = self._read_path(path)

            # verify dictionary path
            try:
                self._path_to_signal = data[self.name][0]  # Path
            except KeyError:
                raise Exception(f"Error: {self.name} Signal not defined")

            # Extract Cross Section
            self.xs = data[self.name][1]
        else:
            if os.path.exists(path):
                self._path_to_signal = path
            else:
                raise Exception(f"Error: {path} not found")

        # Get the delphes root outputs
        self.Forest = self._get_forest(kwargs.get("glob", "**/*.root"))

        load = self.name + " imported with "
        load += str(len(self.Forest)) + " trees!\n"
        load += self._path_to_signal
        print(load, flush=True)

    # path reader to simulation root outputs
    def _read_path(self, path: str) -> dict:
        """
        Read the path to the simulation root outputs

        parameters
        ----------
        path : str
            Path to the simulation root outputs

        returns
        -------
        dict
            Dictionary with the path to the simulation root outputs
        """
        url_protocols = ["http://", "https://", "ftp://", "ftps://"]

        if any(path.startswith(p) for p in url_protocols):
            f = urlopen(path)
            reader = csv.reader(f.read().decode("utf-8").splitlines())
        else:
            if not os.path.exists(path):
                raise Exception(f"Error: {path} not found")
            f = open(path, "r")
            reader = csv.reader(f.read().splitlines())

        data = {row[0]: row[1:] for row in reader if len(row) > 0}
        f.close()
        return data

    # Set and get glob to search the delphes root outputs
    def set_glob(self, glob: str) -> None:
        """
        Set the glob to search the delphes root outputs

        parameters
        ----------
        glob : str
            Glob to search the delphes root outputs
        """
        self._glob = glob

    def get_glob(self) -> str:
        """
        Get the glob to search the delphes root outputs when glob is defined.
        if glob is not defined, set the default glob to '**/*.root' and return
        it

        returns
        -------
        str
            Glob to search the delphes root outputs
        """
        return self._glob

    # Get the delphes root outputs
    def _get_forest(self, glob: str = None) -> list:
        """
        Get the delphes root outputs

        parameters
        ----------
        glob : str,
            Glob to search the delphes root outputs, by default None

        returns
        -------
        list
            Ordered list with the delphes root outputs
        """

        self.set_glob(glob)

        def natural_sort(list):
            import re

            def convert(text):
                if text.isdigit():
                    return int(text)
                else:
                    return text.lower()

            def alphanum_key(key):
                return [convert(c) for c in re.split("([0-9]+)", key)]

            return sorted(list, key=alphanum_key)

        path_root = Path(self._path_to_signal)
        forest = [root_file.as_posix() for root_file in path_root.glob(glob)]
        return natural_sort(forest)

    def get_nevents(self, Forest: list = None) -> int:
        """
        Get the number of events in the delphes root outputs when Forest isn't
        None. if Forest is None, use the default Forest and return the number
        of events.

        parameters
        ----------
        Forest : list, optional
            List with the delphes root outputs, by default None

        returns
        -------
        int
            Number of events in the delphes root outputs
        """
        if Forest is None:
            Forest = self.Forest
        self.nevents = 0
        for i, job in enumerate(Forest):
            tree = TChain("Delphes;1")
            tree.Add(job)
            self.nevents += tree.GetEntries()
        return self.nevents

    def get_unfied_root_tree(self):
        if self.get_nevents() >= 2**24:
            raise Exception(
                "You cannot load more than 2^24 events in a single tree, ROOT limitation"
            )
        tree = TChain("Delphes;1")
        for job in self.Forest:
            tree.Add(job)
        return tree
