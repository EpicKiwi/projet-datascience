from app import CleanApp
from filters.denoise_filter import DummyFilter

cli = CleanApp()

cli.add_filter("denoise", DenoiseFilter)

cli.run()