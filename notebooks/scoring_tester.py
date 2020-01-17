import base_functions as bfun
import matplotlib.pyplot as plt
import numpy as np
import os

class ScoringTester:
    result = []
    image_matching_func = lambda *argv: 1
    
    def __init__(self, folder_path = "../dataset_clean_degraded"):
        self.img_file_path= folder_path
        self.clean_folder = os.path.join(folder_path,'clean')
        self.degraded_folder = os.path.join(folder_path,'degraded')
    
    def get_clean_n_degraded_image(self, img_name):
        clean_path = os.path.join(self.clean_folder, img_name)
        degraded_path = os.path.join(self.degraded_folder, img_name)
        return [bfun.img_path2array(clean_path), bfun.img_path2array(degraded_path)]
    
    def compare_images(self, img_a, img_b, name=""):
        fig = plt.figure(figsize=(20, 4))
        color = ('r', 'g', 'b')
        a = fig.add_subplot(1, 2, 1)
        plt.axis('off')
        plt.title("Image Réference" if len(name) == 0 else name + " Référence")
        plt.imshow(img_a)

        b = fig.add_subplot(1, 2, 2)
        plt.axis('off')
        plt.title(str(self.image_matching_func(img_a, img_b)))
        plt.imshow(img_b)
        
    def show_pics_from_result(self, result = None):
        if result is None:
            result = self.result
            
        result_values_only = [item[0] for item in result]
        for item in result[0:3]:
            self.compare_images(*(self.get_clean_n_degraded_image(item[1])), item[1])
            
        median = np.median([item[0] for item in result])
        closest_to_median_idx = min(range(len(result_values_only)), key=lambda i: abs(result_values_only[i]-median))
        a_bit_before_median = closest_to_median_idx - 2
        a_bit_after_median = closest_to_median_idx + 2

        for item in result[a_bit_before_median:a_bit_after_median]:
            self.compare_images(*(self.get_clean_n_degraded_image(item[1])), "Median " + item[1])

        for item in result[-3:]:
            self.compare_images(*(self.get_clean_n_degraded_image(item[1])), item[1])
            
    def report(self, result = None):
        if result is None:
            result = self.result
        result_values_only = [item[0] for item in result]
        mean = np.mean(result_values_only)
        median = np.median(result_values_only)
        std = np.std(result_values_only)
        print("mean", mean)
        print("median", median)
        print("standard deviation", std)
        plt.hist(result_values_only, bins=256)
        self.show_pics_from_result(result)
        
    def process(self, imgList = None):
        if imgList is None:
            imgList = os.listdir(self.clean_folder)
        
        result = []
        imgList_len = len(imgList)
        
        for idx, name in enumerate(imgList, 1):
            images = self.get_clean_n_degraded_image(name)
            result.append([self.image_matching_func(*images), name])
            print('\r%d/%d comparaisons effectuées' % (idx, imgList_len), end = '')
        
        result.sort()
        self.result = result
        print('\r\n' + str(len(self.result)) + " comparaison effectuées")