import numpy as np
from PIL import Image
import matplotlib as plt
from skimage.util import random_noise
from skimage.color import rgb2hsv, hsv2rgb
from skimage.filters import gaussian
from IPython.display import display
from os import listdir
from os.path import isfile, join
from sklearn.dummy import DummyRegressor
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error, make_scorer
from sklearn.linear_model import SGDRegressor
from sklearn.multioutput import MultiOutputRegressor
from keras.models import Sequential
from keras.layers import Dense
from multiprocessing import Pool

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

DATASETS_PATH = "../labs/noise-filter/"
source_path = DATASETS_PATH+"clean_base"
isolated_out = DATASETS_PATH+"noisy_isolated"
result_out = join(DATASETS_PATH, "denoised.png")

def apply_noise(imga):
    imga = np.rot90(imga)

    imghla = rgb2hsv(imga)
    imgsat = imghla[:,:,2]
    imgsat = random_noise(imgsat,mode='gaussian', seed=RANDOM_STATE, var=0.01)
    imghla[:,:,2] = imgsat
    imga = hsv2rgb(imghla)

    imga = gaussian(imga, sigma=(1.3,0), multichannel=True)
    imga = np.rot90(imga, -1)
    return imga

def infer_metadata(filenames):
    full_filename = np.char.split(filenames, ".")
    full_filename = np.array([i[0] for i in full_filename])
    meta = np.char.split(full_filename,"_")
    meta = np.array([np.array(i) for i in meta])
    return meta

def get_data(images_filenames):
    X = []
    y = []
    
    metadata_list = infer_metadata(images_filenames)
    
    source_uniq = np.unique(metadata_list[:,0])
    source_img_dict = dict()
    print("Loading Source images 0/{} images".format(source_uniq.shape[0]), end="", flush=True)
    for i, source_img in enumerate(source_uniq):
        img = Image.open(join(source_path, source_img+".jpg"))
        source_img_dict[source_img] = np.interp(np.array(img).astype("float64"), (0,255), (0,1))
        print("\rLoading Source images {}/{} images".format(i+1,source_uniq.shape[0]), end="", flush=True)
    
    print("")
    
    loaded = 0
    print("Loading data {}/{} images".format(loaded,images_filenames.shape[0]), end="", flush=True)
    for meta, filename in zip(metadata_list, images_filenames):
        img = Image.open(join(isolated_out, filename))
        imga = np.interp(np.array(img).astype("float64"), (0,255), (0,1))
        X += [imga.flatten()]
        y += [source_img_dict[meta[0]][int(meta[1]), int(meta[2])]]
        loaded += 1
        if loaded % 10 == 0 :
            print("\rLoading data {}/{} images".format(loaded,images_filenames.shape[0]), end="", flush=True)
        
    return (np.array(X), np.array(y))

def predict_image(reg, imga, single_input=False, n_neighbours=20):
    predicted = np.zeros(imga.shape)
    inp = np.zeros((
        imga.shape[0] + (2*n_neighbours),
        imga.shape[1] + (2*n_neighbours),
        3
    ))
    inp[n_neighbours:-n_neighbours, n_neighbours:-n_neighbours, :] = imga
    for x in range(n_neighbours,inp.shape[0]-(n_neighbours*2)):
        for y in range(n_neighbours,inp.shape[1]-(n_neighbours*2)):
            out = inp[
                x-n_neighbours:x+n_neighbours,
                y-n_neighbours:y+n_neighbours
            ]
            predicted[x-n_neighbours][y-n_neighbours] = reg.predict(np.array([out.flatten()]))[0]
    return predicted

def save_img(imga, path):
    Image.fromarray(np.interp(imga,(0,1), (0,255)).astype("uint8")).save(path)

print("")
print("Neural Network Denoiser training")
print("")

img = Image.open(DATASETS_PATH+"clean_base/000000000071.jpg")
imga = np.interp(np.array(img).astype("float64"), (0,255), (0,1))
imgn = apply_noise(imga)

pixel_files = [f for f in listdir(isolated_out) if isfile(join(isolated_out, f))]

shuffled_files = np.random.permutation(pixel_files)
train_batch = shuffled_files[:75_000]

X, y = get_data(train_batch)

print("")
print("Training model")
print("")

model = Sequential([
    Dense(20, input_shape=(4800,), activation="relu"),
    Dense(20, activation='relu'),
    Dense(3, activation="relu")
])
model.compile(optimizer='sgd',
              loss='mean_squared_error',
              metrics=['mean_squared_error'])
model.summary()

model.fit(X, y, epochs=20)

save_image(predict_image(reg, imgn), result_out)

print("")
print("Finished, Image saved in {}".format(result_out))