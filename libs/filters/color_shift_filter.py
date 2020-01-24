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
    
    
    