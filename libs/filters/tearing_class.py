import sys
import os
import random
import statistics
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image, ImageStat, ImageDraw

def _createVerticalBox(img):
    width, height = img.size
    x1 = 0
    y1 = 0 
    x2 = 50
    y2 = height 
    box = (x1, y1, x2, y2)
    return box

def _grayImage(img):
    img_gray = np.zeros((img.shape[0], img.shape[1], img.shape[2]), dtype = 'uint8')
    img_gray[:,:,0] = np.mean(img, axis = 2)
    img_gray[:,:,1] = img_gray[:,:,0]
    img_gray[:,:,2] = img_gray[:,:,0]
    return img_gray

def _capColors(img_gray):
    img_min = np.min(img_gray)
    img_max = np.max(img_gray)
    img_transform = (img_gray - img_min) * 255.0 / (img_max - img_min)
    img_transform = img_transform.astype('uint8')
    return img_transform
    
def _createHist(img, threshold):
    mask = np.where((img[:,:,0] < threshold) & (img[:,:,1] < threshold) & (img[:,:,2] < threshold), 1, 0)
    hist = np.sum(mask, axis=1)
    return hist

def _createZone(hist, img):
    """Crop zone -10px/+10px around tearing"""
    xMax = np.argmax(hist)
    zone = {'min': xMax-10, 'max': xMax+10}
    box = _createBoxHoriz(zone['min'], zone['max'])
    return img.crop(box)

def _createBoxHoriz(yMin, yMax):
    width, height = img.size
    x1 = 0
    y1 = yMin 
    x2 = width
    y2 = yMax 
    box = (x1, y1, x2, y2)
    return box

def _determineLimites(img):
    batchedImg = [] #img en niveau de gris avec lignes batchées par 3px
    diffBetweenLines = []
    
    img = img.convert('LA')
    npImg = np.asarray(img, dtype="int32")
    greyChannel = npImg[:,:,:1]
    Image.fromarray(greyChannel, 'RGB')
    greyChannel = greyChannel.reshape(20, int(720/3), 1*3)
    
    """moyenne des batchs de 5px"""
    for i, line in enumerate(greyChannel):
        batchedLine = []
        for batch in line:
#             print(batch + " ----- " + statistics.mean(batch))
            batchedLine.append(statistics.mean(batch))
        batchedImg.append(batchedLine)
    
    """compare les batchs entre lignes"""
    precedentLine = batchedImg[0]
    for iLine, batchedLine in enumerate(batchedImg):
        batchDiffs = []
        if iLine > 0:
            for ibatch in range(len(batchedLine)):
#                 print(batchedLine[ibatch], precedentLine[ibatch], abs(batchedLine[ibatch] - precedentLine[ibatch]))
                diff = abs(batchedLine[ibatch] - precedentLine[ibatch])
                batchDiffs.append(diff)
            diffBetweenLines.append(statistics.mean(batchDiffs))
        precedentLine = batchedLine
    top_2_idx = np.argsort(diffBetweenLines)[-2:]
    top_2_values = [diffBetweenLines[i] for i in top_2_idx]
#     print(top_2_idx, top_2_values)
#     print(diffBetweenLines)
    return top_2_idx, top_2_values, statistics.median(diffBetweenLines)

def _drawLines(img, limits):
    """Permet de visualiser la zone définie comme teared"""
    width, height = img.size
    draw = ImageDraw.Draw(img)
    draw.line((0, limits[0], img.width, limits[0]), fill=60)
    draw.line((0, limits[1], img.width, limits[1]), fill=60)
    display(img)
    
def _reduceFalsePositive(limitsValues, median):
    limitsValues.sort()
    tresholdMedianH1 = 0.6
    tresholdH1H2 = 0.6
    percentMedianH1 = median/limitsValues[0]
    percentH1H2 = abs(limitsValues[0]/limitsValues[1])
    
    if (median == 0):
        median = 1     
    if (percentMedianH1 < tresholdMedianH1 and percentH1H2 > tresholdH1H2):
        if (median > 1):
            return True
        else: 
            return False
    else:
        return False
    
def _searchH1H2(hist, img):
    """
        - A partir de l'histogramme, on trouve H1-H2
        - On vérifie que ce n'est pas un faux positif en regardant le % de différence entre H et H2 ainsi que 
    """
    zone = _createZone(hist, img)
    limits, limitsValues, median = _determineLimites(zone)
    limits.sort()
    argmax = np.argmax(hist)
    if (argmax < 10):
        argmax += 10
    tearingLimits = [argmax-10+limits[0], argmax-10+limits[1]]    
#     _drawLines(zone, limits)
    category = _reduceFalsePositive(limitsValues, median)
    return tearingLimits, category

def _check(img):
    
    hist = _histLeftColumn(img)

    """Recherche lignes du tearing"""
    limits, category = _searchH1H2(hist, img)
    
    return category