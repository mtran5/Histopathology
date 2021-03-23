# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 23:27:36 2021

@author: mtran
"""
from Patient import *
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Enter the file path to the patient here
    file_path = "../../histopathology_dataset/"
    # Enter the patients number here
    patient_id = ""
    
    patch_size_px = (256, 256, 3)
    # Generate a patient wholeslide image
    patient = Patient(file_path + patient_id, patch_size_px)
    
    out_image = patient.generate_wholeslide_image()
    plt.imshow(out_image)
    plt.show()