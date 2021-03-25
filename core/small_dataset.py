# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 13:30:47 2021

@author: mtran
"""


import sys
from data_utils import *
import numpy
from distutils.dir_util import copy_tree

if __name__ == "__main__":
    
    # Your foldername goes here
    # This is the folder that contains the dataset of patients
    foldername = "../../histopathology_dataset/"
    seed = 42
    
    patient_path = glob.glob(foldername + "*")
    patients = [os.path.basename(p) for p in patient_path]
    
    # Sampling the dataset by patients (cluster sampling)
    # This is done so that bias are not introduced
    
    np.random.seed(seed)
    np.random.shuffle(patients)

    train_test_split = 0.8
    train_patients = patients[:int(len(patients) * train_test_split)]
    test_patients = patients[int(len(patients) * train_test_split):]
    
    # Generate a small dataset of train data for better prototyping
    train_patients = train_patients[:25]
    
    X_train, y_train = GetDataset.get_dataset(foldername, train_patients)
    X_test, y_test  = GetDataset.get_dataset(foldername, test_patients)
    
    # Get the class distribution from the small dataset
    print("Positive classes percentage in train data {:2.2%}.".format(sum(y_train)/len(y_train)))
    
    # Using shutil to copy and paste the small dataset
    # CAREFUL: Only use this code once
    '''
    for patient in train_patients:
        print("Copying {0}...".format(patient))
        src_file = foldername + patient
        dst_file = "../../histopathology_small/" + patient
        if os.path.exists(dst_file):
            continue
        copy_tree(src_file, dst_file)
    '''