import random
import os
import operator

from PIL import Image, ImageDraw, ImageEnhance

import numpy as np
import cv2
import matplotlib.pyplot as plt
import pandas as pd

from .base_functions import calc_rows_hue_aggregation


def check(img, model):
    short_to_predict = []
    
    hsvImage = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    to_predict = (calc_rows_hue_aggregation(hsvImage[:128], np.median, 0))
    short_to_predict.append(to_predict)
    short_to_predict = np.array(short_to_predict)

    result = model.predict(short_to_predict)
    return result[0][0]