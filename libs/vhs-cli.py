from app import CleanApp
from filters.denoise_filter import DummyFilter

cli = CleanApp()

cli.add_filter("denoise", DenoiseFilter)
cli.add_filter("blur", BlurFilter)
cli.add_filter("bw", BWFilter)

cli.run()