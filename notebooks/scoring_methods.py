import cv2
from scipy.spatial import distance as dist
import skimage.metrics as sk_metrics

def dist_chebishev(img_a, img_b):
    hist_a = cv2.calcHist([img_a], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist_a = cv2.normalize(hist_a, hist_a).flatten()
    hist_b = cv2.calcHist([img_b], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist_b = cv2.normalize(hist_b, hist_b).flatten()
    return dist.chebyshev(hist_a, hist_b)

def dist_euclidean(img_a, img_b):
    hist_a = cv2.calcHist([img_a], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist_a = cv2.normalize(hist_a, hist_a).flatten()
    hist_b = cv2.calcHist([img_b], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist_b = cv2.normalize(hist_b, hist_b).flatten()
    return dist.euclidean(hist_a, hist_b)

def dist_manathan(img_a, img_b):
    hist_a = cv2.calcHist([img_a], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist_a = cv2.normalize(hist_a, hist_a).flatten()
    hist_b = cv2.calcHist([img_b], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist_b = cv2.normalize(hist_b, hist_b).flatten()
    return dist.cityblock(hist_a, hist_b)

def structural_similarity(img_a, img_b):
    return sk_metrics.structural_similarity(img_a, img_b, multichannel=True)

# Pas d'utilité, si ce n'est d'avoir tout le listing au même endroit
def normalized_rmse(img_a, img_b):
    return sk_metrics.normalized_root_mse(img_a, img_b)

# Pas d'utilité, si ce n'est d'avoir tout le listing au même endroit
def psnr(img_a, img_b):
    return sk_metrics.peak_signal_noise_ratio(img_a, img_b)
    