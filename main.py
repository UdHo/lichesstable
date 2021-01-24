from downloader.downloader import get_data
from processor.processdata import Processor
from printer.printer import Printer

data = get_data()
statistics = Processor(data).get_player_statistics()
printer = Printer(data, statistics)
printer.print_player_table()
