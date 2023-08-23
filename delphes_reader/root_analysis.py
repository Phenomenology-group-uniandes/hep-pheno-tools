import os
from typing import List, Dict, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import ROOT
from ROOT import (
    TH1F,
    TCanvas,
    THStack,
    TLegend,
    TFile
)
import uproot

from Uniandes_Framework.delphes_reader.particle.abstract_particle import Particle



def generate_csv(dictionary_list :list ,file_name: str) -> None:
    ''' Uses Pandas to create a csv file using all data contained in a list of directories.  
    Parameters:
        dictionary_list (list): It is a list where each member is a dictionary with the structure of get_kinematics_row outputs.
        file_name (string): It is the name that the .csv file will have.
    '''      
    if not all(isinstance(directory_kinematics, dict) for directory_kinematics in dictionary_list):
        raise TypeError("dictionary_list must be a list of dictionaries")
    if not isinstance(file_name, str):
        raise TypeError("file_name must be a string")
    
    Data = pd.DataFrame()

    for dictionary_kinematics in dictionary_list:
        row = pd.DataFrame.from_dict(dictionary_kinematics, orient = "index").T
        Data = pd.concat([Data,row]) 
        Data.reset_index(drop=True, inplace=True)
    Data.to_csv(file_name, index= False)
    

def save_histograms_png(path_to_save: str, dict_hist: Dict[str, TH1F], log_y: bool = False) -> None:
    """Save histograms as .png files.

    Parameters:
        path_to_save: Folder name that will be used to save all histograms as .png files.
        dict_hist: Dictionary that contains all the histograms.
        log_y: If True, the histogram will be plotted using log 10 Y-scale.
    """

    if not isinstance(path_to_save, str):
        raise TypeError("path_to_save must be a string")
    if not all(isinstance(histo, TH1F) for histo in dict_hist.values()):
        raise TypeError("dict_hist must be a dictionary of TH1F")
    if not isinstance(log_y, bool):
        raise TypeError("log_y must be a boolean")
    
    for key, histo in dict_hist.items():
        canvas = ROOT.TCanvas(key, "", 0, 0, 1280, 720)
        canvas.SetGrid()
        if log_y:
            canvas.SetLogy()
        histo.Draw("hist")
        canvas.SaveAs(os.path.join(path_to_save, f"histograms_{key}.png").replace("#", "").replace("{", "").replace("}", "").replace(" ", "_"))       
        
def write_root_file(file_name: str, dict_Hist : Dict[str, TH1F]) -> None:
    """
    This function writes a root file with the histograms contained in a dictionary.
    Parameters:
        file_name (string): It is the name that the .root file will have.
        dict_Hist (dictionary): It is a dictionary where the keys are the names of the histograms and the values are the TH1F histograms .
    """
    if not isinstance(file_name, str):
        raise TypeError("name must be a string")
    if not all(isinstance(histogram, TH1F) for histogram in dict_Hist.values()):
        raise TypeError("dict_Hist must be a dictionary of TH1F histograms")
    
    ROOT_File = TFile.Open(file_name, 'RECREATE')

    [dict_Hist[key].SetName(key) for key in dict_Hist.keys()]
    [dict_Hist[key].Write() for key in dict_Hist.keys()]

    ROOT_File.Close()

def get_root_file_keys(path_root_file: str) -> dict:
    """
    This function returns the keys of the histograms contained in a root file.
    Parameters:
        path_root_file (string): It is the path of the root file.
        
    Returns:
        keys (list): It is a list with the names of the histograms that are in the root file.
    """
    
    file = uproot.open(path_root_file)
    keys = [key.replace(';1', '') for key in file.keys()]
    file.close()
    return keys
    

def read_root_file(path_root_file: str, expected_keys: list) -> dict:
    """
    This function reads a root file and returns a dictionary with the histograms contained in the root file.
    Parameters:
        path_root_file (string): It is the path of the root file.
        expected_keys (list): It is a list with the names of the histograms that are expected to be in the root file.
        
    Returns:
        dictionary: It is a dictionary where the keys are the names of the histograms and the values are the histograms.
    """
    Dict_hist = {}
    File = TFile.TFile.Open(path_root_file, 'READ')
    for key in expected_keys:
        histogram = File.Get(key)
        try: histogram.SetDirectory(0)
        except: pass
        Dict_hist[key] = histogram
    File.Close()
    return Dict_hist
               
def review_holes_in_histograms(Dict_Hist: Dict[str, TH1F]) -> List[str]:
    """
    Returns a list with the names of all histograms with holes contained in a python dictionary (Dict_Hist).
    Parameters:
        Dict_Hist (Dict[str, TH1F]): It is the dictionary that contains all the histograms.
    Return:
        List[str]: List with the names of all histograms with holes.
    """

    if not all(isinstance(histogram, TH1F) for histogram in Dict_Hist.values()):
        raise TypeError("Dict_Hist must be a dictionary of TH1F histograms")
    
    keys_histos_with_holes = []
    for key, histo in Dict_Hist.items():
        if any(histo.GetBinContent(i) == 0 for i in range(1, histo.GetNbinsX()+1)):
            keys_histos_with_holes.append(key)
    return keys_histos_with_holes


def fill_holes_in_histogram(histo, value_to_fill = 10e-4) -> List[str]:
    """
    Fill all the holes contained in a histogram.
    
    Parameters:
        histo (TH1F): histograms with holes.
        value_to_fill (Float): value that will be used to fill the histogram holes.
    Return:
        histo (TH1F): histogram without holes.
    """
    for i in range(1, histo.GetNbinsX()+1): 
        if (histo.GetBinContent(i) == 0 ): histo.SetBinContent(i, value_to_fill)
    return histo


def write_txt_file_with_high_per_bin(file_name :str, Dict_Hist :Dict[str, TH1F]) -> None:
    """
    This function writes a txt file with the number of events per bin of each histogram contained in a dictionary.
    Parameters:
        name (string): It is the name that the .txt file will have.
        Dict_Hist (dictionary): It is a dictionary where the keys are the names of the histograms and the values are the histograms.
    """
    for key in Dict_Hist.keys():
        histo = Dict_Hist[key]
        high_list = [histo.GetBinContent(i) for i in range(1, histo.GetNbinsX())]
        txt_name = f'{file_name}_{key}.dat'
        np.savetxt(txt_name.replace('#', '').replace('{', '').replace('}', '').replace(' ', '_'), high_list)

def extract_branching_ratio_from_param_card(path_paramcard, PID1, PID2):
    """
    This function reads a paramcard file and extracts the Branching ratio that corresponds to PID1 and PID2.
    Parameters:
        path_paramcard (string): It is the path of the paramcard.
        PID1 (float): Particle ID (PID) of particle 1.
        PID2 (float): Particle ID (PID) of particle 2.

    Returns:
        BR (float): Branching Ratio.
    """    
    
    ID1 = str(ID1)
    ID2 = str(ID2)
    with open(f'{path_paramcard}', 'r') as file:
        d = file.readlines()
        position = int(np.where(np.array(d) == '#  BR             NDA  ID1    ID2   ...\n')[0]) # Position of  '#  BR             NDA  ID1    ID2   ...\n' 
    
        for i in range(position, len(d)):
            row = d[i].rstrip().split(" ")
        
            if not (ID1 in row): continue
            if not (ID2 in row): continue
    
            BR = row[3]
            break
            
    return float(BR)