import random
import os, os.path
import cv2
import numpy as np

import scipy.misc
import scipy.signal
from PIL import Image, ImageFilter
from ISR.models import RDN, RRDN

class Blur:
    
    def __init__(self, path = None, max_limit = 180, log = False):
        self.log = log
        self.path = path
        self.max_limit = max_limit
        self.img = None
        self.img_blur = None
        self.img_unblur = None
        
    def recognize(self, file_name = "_.jpg"):
        if(file_name != "" and (file_name.__contains__('.jpg') or file_name.__contains__('.png'))):
            if(self.path != None):
                value = self.check_blur(self.path+file_name)
            else:
                value = self.check_blur()
                
            if(self.log):
                print('Score : '+str(value))
                
            return ('Clean', 'Blur')[value <= self.max_limit] 
        else:
            if(self.log):
                print("Missing file name (with extension - .jpg or .png)")
                
            return 'Problem'
            
    def recognize_path(self, random_number = 10, contains_name = False):
        if(self.path == None):
            print("self.path is undefined")
            return None
        
        moy, to_moy, checkB, checkC, fals = 0, 0, 0, 0, 0
        for i in range(0, int(random_number)):
            r = get_random_file(self.path)
            value = check_blur(r)
            to_moy = to_moy + value
            if((value <= max_limit and not contains_name) or (value <= max_limit and contains_name and r.__contains__('Blur'))):
                checkB = 1 + checkB
            else :
                if((value > max_limit and not contains_name) or (value > max_limit and contains_name and not r.__contains__('Blur'))):
                    checkC = 1 + checkC
                else :
                    fals = 1 + fals
                    moy = value + moy
                    if(self.log):
                        if(value <= max_limit):
                            print('GO-Blur:'+d+' : '+str(int(value))+' : '+r)
                        else:
                            print('NO-Clean:'+d+' : '+str(int(value))+' : '+r)
                            
        print('Check Blur : '+str(checkB)+'/'+str(nbr_image*2)+' | Check Clean : '+str(checkC)+'/'+str(nbr_image*2)+' | False : '+str(fals)+'/'+str(nbr_image*2) + ' - '+str(int(fals/(nbr_image*2)*100))+'% | Moyenne : '+str(int(moy/(fals+1)))+'/'+str(int(to_moy/(nbr_image*2))))
    
    def unblur(self, img = None):
        if(img == None):
            img = self.img_blur
           
        if(self.log):
            print('GANS work')
            
        model = RRDN(weights='gans')
        sr_img = model.predict(np.array(img))
                
        if(self.log):
            print('Scale work')
            
        scale_percent = 25
        width = int(sr_img.shape[1] * scale_percent / 100)
        height = int(sr_img.shape[0] * scale_percent / 100)
        sr_img = cv2.resize(sr_img, (width, height), interpolation = cv2.INTER_NEAREST)

        self.img_unblur = sr_img
        
        return sr_img

    def check_blur(self, img = None):
        if(img == None):
            img = self.img_blur
            
        if(img.ndim == 3):
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        return cv2.Laplacian(img, cv2.CV_64F).var()
        

    def get_random_file(self, folder):
        r = random.choice(os.listdir(DIR_DATASET+folder))
        while(not r.__contains__('.jpg')):
            r = random.choice(os.listdir(DIR_DATASET+folder))
        r = folder+r
        return r
    
    def load(self, img):
        self.img = Image.open(img)
        self.img_blur = np.array(self.img)
    
    def blur(self):
        self.img_blur = np.array(self.img.filter(ImageFilter.BLUR))
    
    def show_ori(self):
        display(self.img)
        
    def show_blur(self):
        display(Image.fromarray(self.img_blur))
        
    def show_unblur(self):
        display(Image.fromarray(self.img_unblur))
        
    def save_img(self, img, filename = "output.jpg"):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imwrite(filename, img)
        
    def clear(self, path = None, max_limit = 180, log = False):
        self.log = log
        self.path = path
        self.max_limit = max_limit
        self.img = None
        self.img_blur = None
        self.img_unblur = None
