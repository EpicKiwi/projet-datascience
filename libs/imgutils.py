import cv2

def img_path2array(path):
    return cv2.cvtColor(cv2.imread(path, 10), cv2.COLOR_BGR2RGB)

def img_array2file(path, array):
	cv2.imwrite(path, cv2.cvtColor(array, cv2.COLOR_RGB2BGR))