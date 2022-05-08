from downloader.downloader import get_data
from processor.processdata import Processor
from printer.printer import Printer

if __name__ == "__main__":
    print("get_data\n")
    data = get_data()
    print("statistics\n")
    statistics = Processor(data).get_player_statistics()
    print("print\n")
    printer = Printer(data, statistics)
    printer.print_player_table()
