from app import Filter
import pickle
from keras.models import model_from_yaml

class DenoiseFilter(Filter):

	detector = None
	cleaner = None

	def load(self, directory):
		with open(directory+"/detection-model.pickle", "rb") as f:
			self.detector = pickle.loads(f.read())

		with open(directory+"/correction-architecture.yml", "r") as f:
			self.cleaner = model_from_yaml(f.read())

		self.cleaner.load_weights(directory+"/correction-weights.h5")

	def check(self, img):
		return True