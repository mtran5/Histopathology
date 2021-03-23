# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 12:48:26 2021

@author: mtran
"""

import sys
sys.path.insert(1, '../')
from data_utils import *
import numpy as np
import glob

if __name__ == "__main__":
    foldername = "../../../histopathology_dataset/"
    seed = 42
    
    patient_path = glob.glob(foldername + "*")
    patients = [os.path.basename(p) for p in patient_path]
    
    # Sampling the dataset by patients (cluster sampling)
    # This is done so that bias are not introduced
    
    np.random.seed(seed)
    np.random.shuffle(patients)

    train_test_split = 0.25
    
    train_patients = patients[:int(len(patients) * train_test_split)]
    test_patients = patients[int(len(patients) * train_test_split):]
    
    X_train, y_train = GetDataset.get_dataset(foldername, train_set)
    X_test, y_test  = GetDataset.get_dataset(foldername, test_set)