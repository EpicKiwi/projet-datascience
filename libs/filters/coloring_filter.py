from app import Filter
from .coloring_class import check

from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model

class ColoringFilter(Filter):
    
    model = None
    
    def check(self, img):
        """
        Vérifie si le problème corrigé par le filtre est présent sur l'image d'entrée

        img : Un tableau Numpy RGB (576, 720, 3) de l'image
        """
        
        return (False, True)[check(img, self.model) <= 0.8]
    
    def load(self, directory):
        """
        Cherge le modèle de la base d'un fichier serialisé

        directory : Chemin vers le dossier contenant le fichier de sauvegarde du modèle
        """
        self.model = load_model(directory+"/pinking_model.h5")
        