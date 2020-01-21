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


def get_normalized_gray_image(path):
    img = img_path2array(path)
    img_gray = np.zeros((img.shape[0], img.shape[1], img.shape[2]), dtype = 'uint8')
    
    img_gray[:,:,0] = np.mean(img, axis = 2)
    img_gray[:,:,1] = img_gray[:,:,0]
    img_gray[:,:,2] = img_gray[:,:,0]
    
    img_min = np.min(img_gray)
    img_max = np.max(img_gray)
    
    img_normalized = (img_gray - img_min) * 255.0 / (img_max - img_min)
    img_normalized = img_normalized.astype('uint8')
    return img_normalized

def get_blackpix_by_line(img, threshold): # threshold below 40 for black pixel search
    mask = np.where((img[:,:,0] < threshold) & (img[:,:,1] < threshold) & (img[:,:,2] < threshold), 1, 0)
    hist = np.sum(mask, axis=1)
    plt.plot(hist)
    
def get_whitepix_by_line(img, threshold): # threshold above  210 for white pixel search
    mask = np.where((img[:,:,0] > threshold) & (img[:,:,1] > threshold) & (img[:,:,2] > threshold), 1, 0)
    hist = np.sum(mask, axis=1)
    plt.plot(hist)