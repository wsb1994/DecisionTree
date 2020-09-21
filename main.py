import Tuple
import SynthTree
binsize = 5
dataLength = 3

data1 = Tuple.TupleObject('synthetic-1.csv')
data2 = Tuple.TupleObject('synthetic-2.csv')
data3 = Tuple.TupleObject('synthetic-3.csv')
data4 = Tuple.TupleObject('synthetic-4.csv')


# max depth of 2, parent depth of -1 since the root doesn't count, bins size 5, data set length (3)
synth1 = SynthTree.DTree(data1.list, 2, -1, 5, dataLength)
SynthTree.check(synth1, 3)
bigCheck1 = SynthTree.returnCheck()
print(SynthTree.ListProb(bigCheck1.positive, dataLength))
SynthTree.Positive = []
SynthTree.Negative = []

synth2 = SynthTree.DTree(data2.list, 2, -1, 11, dataLength)
SynthTree.check(synth2, 3)
bigCheck2 = SynthTree.returnCheck()
print(SynthTree.ListProb(bigCheck2.positive, dataLength))
SynthTree.Positive = []
SynthTree.Negative = []

synth3 = SynthTree.DTree(data3.list, 2, -1, 6, dataLength)
SynthTree.check(synth3, 3)
bigCheck3 = SynthTree.returnCheck()
print(SynthTree.ListProb(bigCheck3.positive, dataLength))
SynthTree.Positive = []
SynthTree.Negative = []

synth4 = SynthTree.DTree(data3.list, 2, -1, 8, dataLength)
SynthTree.check(synth4, 3)
bigCheck4 = SynthTree.returnCheck()
print(SynthTree.ListProb(bigCheck4.positive, dataLength))
SynthTree.Positive = []
SynthTree.Negative = []



synth4 = SynthTree.DTree(data1.list, 2, -1, binsize, dataLength)




