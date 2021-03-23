# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 23:27:36 2021

@author: mtran
"""
from Patient import *
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Enter the file path to the patient here
    foldername = "../../histopathology_dataset/"
    # Enter the patients number here
    patient_id = "8863"
    
    patch_size_px = (50, 50, 3)
    patch_size_mm = (50, 50)
    # Generate a patient wholeslide image
    patient = Patient(foldername, patient_id, patch_size_mm, patch_size_px)
    
    out_image = patient.generate_wholeslide_image(class_vis = False).astype("uint8")
    plt.imshow(out_image)
    plt.show() 
    
    out_image_classes = patient.generate_wholeslide_image(class_vis = True).astype("uint8")
    plt.imshow(out_image_classes)
    plt.show()
    plt.imsave("Images/" + patient_id + ".png", out_image)