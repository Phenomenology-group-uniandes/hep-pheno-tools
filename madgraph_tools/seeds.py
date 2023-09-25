import numpy as np
from pathlib import Path


# function to generate different random seeds
def get_new_seed(seeds, max_seed=100000):
    """
    Function to generate different random seeds

    Description:
    ------------
    This function generates a random seed that is not in the list of seeds that
    are passed as an argument.

    Parameters:
    ----------
        seeds: list of seeds
        max_seed: maximum seed value

    return:
    -------
    new seed
    """
    if len(seeds) == max_seed:
        raise Exception("No more seeds available")
    while True:
        seed = np.random.randint(1, max_seed+1)
        if not (seed in seeds):
            break
    seeds.append(seed)
    return seeds[-1]


def get_seed_from_banner(banner_file_path: str) -> int:
    """
    Function to get the seed from the banner file

    Description:
    ------------
    This function gets the seed from the banner file
    example of line in the banner file:
      4160 = iseed ! rnd seed (0=assigned automatically=default))
    which must be returned as 4160

    Parameters:
    ----------
        banner_file_path: path to the banner file

    return:
    -------
    seed
    """
    with open(banner_file_path, "r") as f:
        seed_line = [line for line in f.readlines() if "iseed" in line][0]
    seed = int(seed_line.split("=")[0].strip())
    return seed


def get_seeds_from_mg5_output_folder(mg5_output_folder: str) -> list:
    """
    Function to get the seeds from the mg5 output folder

    Description:
    ------------
    This function gets the seeds from the mg5 output folder,
    all the banner files are in Events subfolder, and have the subfix
    *banner.txt We use glob to get all the banner files and then we get the
    seed from each banner file.

    Parameters:
    ----------
        mg5_output_folder: path to the mg5 output folder

    return:
    -------
    list of seeds
    """
    banner_files = list(
        Path(mg5_output_folder).glob("Events/run_*/*banner.txt")
        )
    return [get_seed_from_banner(b) for b in banner_files]
