from app import Filter
from bw_class as bw

class BWFilter(Filter):
        
    def check(self, img):
        """
        Vérifie si le problème corrigé par le filtre est présent sur l'image d'entrée

        img : Un tableau Numpy RGB (576, 720, 3) de l'image
        """
        h_median = bw.detectionScratchLineMedian(img)
        h_std = bw.detectionScratchLineStd(img)
        
        return (False, True)[h_median and h_std] 

    def clean(self, img):
        """
        Néttoie l'image du problème corrigé par le filtre

        img : Un tableau Numpy RGB (576, 720, 3) de l'image
        """
        h_median = detectionScratchLineMedian(img)
        img_solved = defectCorrection(h_median, img)
        
        h_std = detectionScratchLineStd(img)
        img_solved_v2 = defectCorrection(h_std, img_solved)
        
        return img_solved_v2