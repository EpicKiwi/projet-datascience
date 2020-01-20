import cv2
import matplotlib.pyplot as plt
import numpy as np
import operator
import os
import pandas as pd

def analayse_image(img):
    fig = plt.figure(figsize=(20, 4))
    color = ('r', 'g', 'b')
    a = fig.add_subplot(1, 2, 1)
    plt.axis('off')
    plt.title("Image")
    plt.imshow(img)    
    
    b = fig.add_subplot(1, 2, 2)
    for i,col in enumerate(color):
        histr = cv2.calcHist([img],[i],None,[256],[0,256])
        plt.title("Histogramme")
        plt.plot(histr,color = col)
    plt.show()
    
    
def img_path2array(path):
    return cv2.cvtColor(cv2.imread(path, 10), cv2.COLOR_BGR2RGB)

def get_labelized_images_name(label, csv_path = os.path.join("..", "dataset_problems.csv")):
    data = pd.read_csv(csv_path, sep=";")
    return data[data[label] >= 1]['file']