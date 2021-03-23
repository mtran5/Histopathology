# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 12:34:42 2021

@author: mtran
"""
import numpy as np
import glob
import os

class GetDataset(object):
    def get_dataset(foldername, patients):
        '''
        Get the histopathology data
        Returns:
            Data: Array
            Array of patches location
            Label: Array
            Array of labels (0, 1) that correspond to data
        '''
        X = []
        for p in patients:
            X = X + glob.glob(foldername + p + "/*/*.png")
        y = [GetDataset.get_label(x) for x in X]
        return X, y
        
    def get_label(filepath):
        '''
        Get the image label (0 or 1)
        Only called by get_data
        '''
        filename = os.path.basename(filepath)
        patch_name = filename.split(sep = ".")[0]
        class_label = patch_name.split(sep = "_")[4]
        label = int(class_label[-1])
        return label
    