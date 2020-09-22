import Tuple
import SynthTree
from copy import deepcopy
import operator 
import math
global Positive
global Negative

Positive = []
Negative = []

binsize = 11
dataLength = 3

def discretizer(Data, DataSetLength, BinSize):
    totalBoundaries = []
    for k in range(DataSetLength-1):
        for e in range(len(Data)):
            Data[e][k] = float(Data[e][k])
    for i in range(DataSetLength-1):
        binBoundaries = []
        
        Data.sort(key=operator.itemgetter(i))
        localmax = float(Data[len(Data) - 1][i])
        localmin = float(Data[0][i])
        localCheck = abs(localmax - localmin)

        if (float(localCheck) == 1.0):
            binBoundaries.append(0)
            binBoundaries.append(1)
            totalBoundaries.append(deepcopy(binBoundaries))
            continue

        boundary = len(Data)/ BinSize
        localbin = BinSize - 1

        for j in range(localbin):
            binBoundaries.append(int(math.ceil(boundary * (j + 1))))
        binBoundaries.append(len(Data))

        prevboundary = 0
        for boundaryBin in range(len(binBoundaries)):
            for entry in range(prevboundary, binBoundaries[boundaryBin]):
                Data[entry][i] = int(boundaryBin)
            prevboundary = binBoundaries[boundaryBin]
        totalBoundaries.append(deepcopy(binBoundaries))
    return totalBoundaries
def getBoundaries(boundaries, dataSetLength, data):
        
            for column in range(dataSetLength-1):
                for localBound in range(len(boundaries[column])):
                       boundaries[column][localBound] = data[localBound][column]
            

data1 = Tuple.TupleObject('synthetic-1.csv')
data1Reference = deepcopy(data1)

data2 = Tuple.TupleObject('pokemonStats.csv')
data2.list.pop(0)
data2Reference = deepcopy(data2)

boundaries = discretizer(data1.list, dataLength, binsize)
getBoundaries(boundaries, dataLength, data1Reference.list)

boundaries2 = discretizer(data2.list, 45, binsize)
getBoundaries(boundaries2, 45, data2Reference.list)

SynthTree1 = SynthTree.DTree(data1.list, 2, -1, dataLength, boundaries, None)
SynthTree2 = SynthTree.DTree(data2.list, 3, -1, 45, boundaries2, None)

accuracy = SynthTree.checkHandler(SynthTree1, dataLength)
SynthTree.Positive = []
SynthTree.Negative = []
accuracy2 = SynthTree.checkHandler(SynthTree2, 45)

print(accuracy)
print(accuracy2)


