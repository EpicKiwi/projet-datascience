from app import CleanApp
from filters.dummy_filter import DummyFilter

cli = CleanApp()

cli.add_filter("dummy", DummyFilter)

cli.run()