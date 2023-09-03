import pandas as pd


def generate_dataframe(dictionary_list: list, file_name: str) -> None:
    if not all(isinstance(d, dict) for d in dictionary_list):
        raise TypeError("dictionary_list must be a list of dictionaries")
    if not isinstance(file_name, str):
        raise TypeError("file_name must be a string")

    Data = pd.DataFrame()
    for dictionary_kinematics in dictionary_list:
        row = pd.DataFrame.from_dict(dictionary_kinematics, orient="index").T
        Data = pd.concat([Data, row])
        Data.reset_index(drop=True, inplace=True)
    return Data
