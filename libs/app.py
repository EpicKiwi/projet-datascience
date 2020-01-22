import cli.app
import imgutils
from os.path import join, basename
import pathlib

class Filter:

	def check(self, img):
		"""
		Vérifie si le problème corrigé par le filtre est présent sur l'image d'entrée

		img : Un tableau Numpy RGB (576, 720, 3) de l'image
		"""
		return True

	def clean(self, img):
		"""
		Néttoie l'image du problème corrigé par le filtre

		img : Un tableau Numpy RGB (576, 720, 3) de l'image
		"""
		return img

	def train(self, training_batch, temp_dir):
		"""
		Entraine le filtre sur un ensemble d'images d'entrée

		img : Un tableau Numpy RGB (*, 576, 720, 3) du batch d'images
		"""
		pass

	def save(self, directory):
		"""
		Sauvegarde l'entrainement du filtre dans un fichier serialisé

		directory : Chemin vers le dossier où sauvegarder le modèle
		"""
		pass

	def load(self, directory):
		"""
		Cherge le modèle de la base d'un fichier serialisé

		directory : Chemin vers le dossier contenant le fichier de sauvegarde du modèle
		"""
		pass

class CleanApp(cli.app.CommandLineApp):

	filters = []

	def __init__(self):
		super().__init__(name="VHS CLI", description="Clean an image numerized from a VHS", reraise=(Exception))

		self.add_param("-o", "--output", help="Output directory for cleaned images", default=".")
		self.add_param("-m", "--models", help="Directory where model files are stored", default="models")
		self.add_param("file", help="Files to clean", nargs='+')

	def add_filter(self, name, filter, help=None):
		"""
		Ajoute un nouveau filtre à la chaine de filtres

		name   : Nom du filtre
		filter : Sous classe de app.Filter représentant le filtre qui sera instanciée à l'éxécution de la fonction
		help   : Une courte chaine de carractère expliquant le but du filtre
		"""
		name = name.lower()
		self.filters += [(name,filter())]

		self.add_param("--no-{}".format(name), action="store_true", default=False,
			help="Include {} filter in the cleaning chain".format(name))
		self.add_param("--force-{}".format(name), action="store_true", default=False,
			help="Force {} filter to operate".format(name))

	def main(self):

		params = self.params.__dict__

		pathlib.Path(params["output"]).mkdir(parents=True, exist_ok=True)

		print("{} : {}".format(self.name, self.description))

		print("Loading filters")
		
		for filname, fil in self.filters:
			print("Loading {} filter".format(filname))
			fil.load(join(params["models"], filname))

		for filepath in params["file"]:
			print("\n - Cleaning {}".format(filepath))
			image = imgutils.img_path2array(filepath)

			current_img = image
			for filname, fil in self.filters:

				if params["no_{}".format(filname)]:
					print("   User skipped {} filter".format(filname))
					continue

				need_apply = fil.check(current_img)

				if not params["force_{}".format(filname)] and not need_apply:
					print("   Not using {} filter".format(filname))
					continue

				print("   Applying {} filter".format(filname) + (" (forced)" if params["force_{}".format(filname)] else ""))
				current_img = fil.clean(current_img)

			outpath = join(params["output"], basename(filepath))
			imgutils.img_array2file(outpath, current_img)
			print("   Result saved at {}".format(outpath))


	def post_run(self, returned):
		if isinstance(returned, Exception):
			raise returned

		super().post_run(returned)
