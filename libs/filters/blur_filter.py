from app import Filter
from .blur_class import Blur
import Numpy as np

class BlurFilter(Filter):
    
    def __init__(self):
        self.blur = Blur()
        
    def check(self, img):
        """
        Vérifie si le problème corrigé par le filtre est présent sur l'image d'entrée

        img : Un tableau Numpy RGB (576, 720, 3) de l'image
        """
        img = np.interp(img, (0, 1), (0, 255))
        return (False, True)[self.blur.check_blur(img, True) <= self.blur.max_limit] 

    def clean(self, img):
        """
        Néttoie l'image du problème corrigé par le filtre

        img : Un tableau Numpy RGB (576, 720, 3) de l'image
        """
        
        return self.blur(img, True)