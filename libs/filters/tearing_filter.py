from app import Filter
from .tearing_class import _check

class TearingFilter(Filter):
        
    def check(self, img):
        """
        Vérifie si le problème corrigé par le filtre est présent sur l'image d'entrée

        img : Un tableau Numpy RGB (576, 720, 3) de l'image
        """
        
        return check(img)