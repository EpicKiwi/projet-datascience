import os
import sys
import random
import PIL  
import cv2
from scipy import ndimage, misc
from PIL import Image, ImageFilter
from matplotlib import pyplot as plt
from scipy import ndimage, signal
import numpy as np

from app import Filter


# chemin dossier contenant les images cleans
class ChromaticAberration(filter):

     def __init__(self):
        self.ChromAb = ChromAb()
        
    def check(self, img):
        """
        Vérifie si le problème corrigé par le filtre est présent sur l'image d'entrée

        img : Un tableau Numpy RGB (576, 720, 3) de l'image
        """
        
        return (False, True)[self.chromAb.check_chromAb(img, True) <= self.chromAb.max_limit] 

    def clean(self, img):
        """
        Néttoie l'image du problème corrigé par le filtre

        img : Un tableau Numpy RGB (576, 720, 3) de l'image
        """
        
        return self.chromAb(img, True)
    
    
    DATASET_PATH = os.path.join(os.getcwd(), "input") 

    random_filename = random.choice([
        x for x in os.listdir(DATASET_PATH)
        if os.path.isfile(os.path.join(DATASET_PATH, x))
    ])
    random_image = 'input/' + random_filename 
    new_file = 'output/' + random_filename

    new_jpg = new_file

    addition= cv2.imread(random_image, cv2.IMREAD_UNCHANGED)
    image = addition
    OFFSET = 1

    #permet de simuler une anomalie chromatique en déplacant les calques
    def offsetSetting(R,G,B):
        red_layer = image[:,:,2]
        green_layer = image[:,:,1]
        blue_layer = image[:,:,0]

        if (R == 0):
            addition[: ,: ,2] = red_layer[:,:]
            addition[G*OFFSET: ,G*OFFSET: ,1] = green_layer[:-G*OFFSET,:-G*OFFSET]
            addition[B*OFFSET: ,B*OFFSET: ,0] = blue_layer[:-B*OFFSET,:-B*OFFSET]
            cv2.imwrite(new_jpg,addition) 
        if (G == 0):
            addition[R*OFFSET: ,R*OFFSET: ,2] = red_layer[:-R*OFFSET,:-R*OFFSET]
            addition[: ,: ,1] = green_layer[:,:]
            addition[B*OFFSET: ,B*OFFSET: ,0] = blue_layer[:-B*OFFSET,:-B*OFFSET]
            cv2.imwrite(new_jpg,addition) 

        if (B == 0):
            addition[R*OFFSET: ,R*OFFSET: ,2] = red_layer[:-R*OFFSET,:-R*OFFSET]
            addition[G*OFFSET: ,G*OFFSET: ,1] = green_layer[:-G*OFFSET,:-G*OFFSET]
            addition[: ,: ,0] = blue_layer[:,:]
            cv2.imwrite(new_jpg,addition) 


    offsetSetting(1, 0, 2)
