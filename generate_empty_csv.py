from os import listdir
from os.path import isfile, join, dirname
import pandas as pd

dirname = dirname(__file__)

FILES_PATH = join(dirname, "dataset_clean_degraded/clean")
OUTPUT_PATH = join(dirname, "dataset_problems.csv")

files = sorted([f for f in listdir(FILES_PATH) if isfile(join(FILES_PATH, f))])

dataframe = pd.DataFrame()
dataframe["file"] = files
dataframe.to_csv(OUTPUT_PATH, index=False)