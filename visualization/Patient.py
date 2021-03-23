# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 22:40:36 2021

@author: mtran
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 18:26:37 2021

@author: mtran
"""
import itertools
import operator
import os, glob
import numpy as np 
import cv2

class Patient(object):
    # Host all Images that belongs to a single patient
    def __init__(self, 
                 foldername, 
                 patient_ID,
                 patch_size_mm,
                 patch_size_px):
        '''
        Initialize a WholeSlide class
        Read all image slides within it that meets requirements
        Parameters
        ----------
        foldername : STRING
            The folder location of the whole slide image
        patient_num: STRING
            The designated number for the patient
        segment_size_px: int
            The size of the images in pixels
            
        Returns
        -------
        None.

        '''
        assert os.path.isdir(foldername), "Folder does not exist"
        self.foldername = foldername
        self.patient_ID = patient_ID
        self.patch_size_px = patch_size_px 
        self.patch_size_mm = patch_size_mm
        self.AbsoluteReferences = None
        
        # Initializing by reading the folder
        self.PatchesFileNames = self.read_folder() #List of patches that are contained
        self.PatchesDict_unorganized = self.generate_patches_dict(self.PatchesFileNames) # Dictionary that consists of patches and their locations
        self.PatchesDict = self.organize_patches_dict(self.PatchesDict_unorganized)
        self.register_patches_segment(self.PatchesDict)

    def read_folder(self):
        '''
        Read all images in the folder
        Returns a list of all files in a folder that meets filename requirements and is of the correct extension 
        See assert_filename for the correct format of assert_filename
        '''
        # This will traverse all subfolder images
        files = map(os.path.basename, glob.glob(self.foldername + "/" + self.patient_ID + "/*/*.png"))
        out = [f for f in files if self.assert_filename(f)]
        return out
    
    def assert_filename(self, fname):
        '''
        Assert if the file is appropriately named
        Correct format is u_idx_x_y_class.png
        Where y is the y-mm coordinates
        x is the x-mm coordinates
        Both u and x don't have to be four characters long. But they must be the same length and positive integers
        u_idx is the patient ID. This can be any alphanumeric combinations
        ext is the desired extension name
        Inputs:
            - fname: file name
        Output:
            - Boolean that is True when the file is correct format and correct extension and False otherwise
        '''
        f = fname.split(sep = ".")
        if len(f) != 2:
            return False
        file_name, file_ext = f[0], f[1]
        if file_ext != "png":
            return False
        p = file_name.split(sep = "_")
        if len(p) != 5:
            return False
        return True
    
    def get_info(self, fname):
        '''
        Return the information that is extracted from the patches' names
        Inputs:
            fname: Name of the image patch
        Returns:
            yy: y-coordinates of the image patch
            xx: x-coordinates of the image patch
            patch_class: class of the image patch (0 or 1)
        '''
        f = fname.split(sep = ".")
        file_name = f[0]
        p = file_name.split(sep = "_")
        _, _, xx, yy, patch_class =  p[0], p[1], p[2], p[3], p[4]
        xx = int(xx[1:])
        yy = int(yy[1:])
        patch_class = patch_class[-1]
        return yy, xx, patch_class      
    
    def generate_patches_dict(self, files):
        out = []
        for fname in files:
            yy, xx, patch_class = self.get_info(fname)
            I_dict = { "Patch Name" : fname,
                       "Coor_mm" : (yy, xx),
                       "Coor_px" : (0, 0),
                       "Class" : patch_class}
            out.append(I_dict)
        return out   

    def organize_patches_dict(self, patches_dict):
        # Organize a list of image patches
        # Each dictionary items will be grouped into a list of lists
        # All patches of the same column will be grouped into one list
        
        # Sort by y coordinates first, then by x coordinates
        list_sorted = sorted(patches_dict, key = operator.itemgetter('Coor_mm'))
        # Use groupby() to group all ImageSegment of the same row into one list
        row_grouped = itertools.groupby(list_sorted, lambda x : x['Coor_mm'][0])
        # Generate a list of list
        out = [[item for item in data] for (key, data) in row_grouped]
        self.AbsoluteReferences = out[0][0]  #Get the absolute references for (0,0) coordinates
        return out
    
    def register_patches_segment(self, patches_dict):
        # Using a sorted list of list generated by organize_patches_dict
        # Convert the mm coordinates to actual relational indices
        for row in patches_dict:
            for patch in row:
                coor_px = self.mm_to_px_coordinates(patch["Coor_mm"])
                patch.update({"Coor_px" : coor_px}) 
        return patches_dict

    def mm_to_px_coordinates(self, coordinates):
        # Simply convert a mm coordinates to px coordinates
        # First "normalize" the mm coordinates to the absolute reference image
        normalized = tuple(map(lambda a,b,c: int((a-b)/c), coordinates, self.AbsoluteReferences["Coor_mm"], self.patch_size_mm))
        out = (normalized[0] * self.patch_size_px[0], normalized[1] * self.patch_size_px[1])
        return out
    
    def generate_wholeslide_image(self, class_vis = False):
        '''
        Generate a large image consist of all patches together
        Input:
            class_vis: Boolean
            If set to True, 1 class will become red and 0 class will become blue
        '''
        
        # Get the top, bottom, leftmost, and rightmost pixels
        top_px = min(self.PatchesDict_unorganized, key = lambda f: f["Coor_px"][0])["Coor_px"][0]
        bottom_px = max(self.PatchesDict_unorganized, key = lambda f: f["Coor_px"][0])["Coor_px"][0]
        bottom_px += self.patch_size_px[0]
        
        leftmost_px = min(self.PatchesDict_unorganized, key = lambda f: f["Coor_px"][1])["Coor_px"][1]
        rightmost_px = max(self.PatchesDict_unorganized, key = lambda f: f["Coor_px"][1])["Coor_px"][1]
        rightmost_px += self.patch_size_px[1]
        
        # Create the large image where everything goes 
        H = bottom_px - top_px
        W = rightmost_px - leftmost_px
        hh, ww, D = self.patch_size_px
        
        print("Top: {0}, Bottom {1}, Leftmost {2}, RightMost {3}".format(top_px, bottom_px, leftmost_px, rightmost_px))
        
        # Put our image patches into the large matrix
        out = np.zeros((H, W, D))
        for r in self.PatchesDict:
            for I in r:
                M = cv2.imread(self.foldername + "/" + self.patient_ID + "/" + I["Class"] + "/" + I["Patch Name"])
                if M.shape != self.patch_size_px: continue
                yy, xx = I["Coor_px"]
                
                if class_vis:
                    if I["Class"] == "0":
                        M[:,:,0] = M[:,:,0] * 0.8 + 0.2
                    if I["Class"] == "1":
                        M[:,:,2] = M[:,:,2] * 0.8 + 0.2
                
                #print("xx = " + str(xx))
                #print("xx_pos = " + str(xx - leftmost_px + ww))
                out[yy - top_px: yy - top_px + hh, xx - leftmost_px: xx - leftmost_px + ww, :] = M[:,:,:]
        return(out)    
            