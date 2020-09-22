from csv import reader

class TupleObject:
    def __init__(self, dataFile):
        with open(dataFile) as handler:
            csvHandler = reader(handler)

            self.list = list(csvHandler)
