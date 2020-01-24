from app import CleanApp
from filters.denoise_filter import DenoiseFilter
from filters.blur_filter import BlurFilter
from filters.bw_filter import BWFilter
from filters.coloring_filter import ColoringFilter
from filters.tearing_filter import TearingFilter

cli = CleanApp()

cli.add_filter("bw", BWFilter)
cli.add_filter("tearing", TearingFilter) #ONLY RECONNAISANCE
cli.add_filter("denoise", DenoiseFilter)
cli.add_filter("blur", BlurFilter)
cli.add_filter("coloring", ColoringFilter) #ONLY RECONNAISANCE

cli.run()