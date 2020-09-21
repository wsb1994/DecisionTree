import math
import operator
from enum import Enum
from copy import deepcopy
from collections import defaultdict
global Positive
global Negative

Positive = []
Negative = []
class Variable(Enum):
    X = 0
    Y = 1
    Label = 2


# category number that was used to previously dig
previously_used = {}
class classifier:
    def __init__(self):
        self.positive = []
        self.negative = []

class DTree:
    def __init__(self, data, maxDepth, parentDepth, binSize, datasetLength):
        self.thisData = deepcopy(data)
        self.maxDepth = maxDepth
        self.depth = 1 + parentDepth

        self.indexDiscriminated = -1
        self.entropy = -(math.inf)

        # True, False
        self.classifiedAs = None

        self.Leaf = False
        self.bin = None

        self.children = []
        self.binBoundaries = []
        self.bin = data

        if self.depth == maxDepth:
            self.Leaf = True
            # calculateEntropy(self.bin, datasetLength)
            self.classify(datasetLength)
        else:
            self.discriminate(self.thisData, binSize, datasetLength)
            self.entropy = calculateEntropy(self.thisData, datasetLength)
            self.calculateInformationGain(self.thisData, datasetLength)

    def classify(self, datasetLength):
        TrueVal = calculateProbability(self.bin, datasetLength, True)
        FalseVal = calculateProbability(self.bin, datasetLength, False)

        if TrueVal >= FalseVal:
            self.classifiedAs = "+"
        else:
            self.classifiedAs = "-"

    def calculateInformationGain(self, data, datasetLength):
        childEntropies = []

        for i in range(len(self.children)):
            variable = calculateEntropy(deepcopy(self.children[i].bin), datasetLength)
            childEntropies.append(variable)

    def binaryDiscriminate(self, theData, discriminator):
        previously_used[discriminator] = 1
        Negative = []
        Positive = []
        for i in range(2):
            for j in range(len(theData)):
                if theData[j][discriminator] == 1:
                    Positive.append(deepcopy(theData[j]))
                else:
                    Negative.append(deepcopy(theData[j]))
        self.children.append(Negative)
        self.children.append(Positive)

    def discriminate(self, theData, binSize, datasetLength):
        localDiscriminator = -1
        localDifference = 0
        for i in range(datasetLength - 1):
            # skip it if it's been used before
            if i in previously_used:
                if previously_used[i] == 1:
                    continue

            localmax = -math.inf
            localmax = math.inf

            theData.sort(key=operator.itemgetter(i))
            localmax = float(theData[len(theData) - 1][i])
            localmin = float(theData[0][i])

            localCheck = abs(localmax - localmin)

            if (localCheck > localDifference):
                localDiscriminator = i

        if (float(localCheck) == 1.0):
            self.binBoundaries.append(0)
            self.binBoundaries.append(1)

            self.binaryDiscriminate(theData, localDiscriminator)
            return

        boundary = len(theData) / binSize
        localBin = binSize - 1

        for i in range(localBin):
            self.binBoundaries.append(int(math.ceil(boundary * (i + 1))))
        self.binBoundaries.append(len(theData))

        prevboundary = 0
        for boundaryBin in range(len(self.binBoundaries)):
            for entry in range(prevboundary, self.binBoundaries[boundaryBin]):
                theData[entry][localDiscriminator] = boundaryBin
            prevboundary = self.binBoundaries[boundaryBin]

        for i in range(len(self.binBoundaries)):
            child = []
            for entry in range(len(theData)):
                if int(theData[entry][localDiscriminator]) == i:
                    child.append(theData[entry])
            self.children.append(DTree(deepcopy(child), self.maxDepth, deepcopy(self.depth), binSize, datasetLength))





def calculateProbability(data, datasetLength, which):
    p = {}
    p[0] = 0
    p[1] = 0

    for i in range(len(data)):
        if int(data[i][datasetLength - 1]) == 0:
            p[0] += 1
        if int(data[i][datasetLength - 1]) == 1:
            p[1] += 1

    probabilityT = p[1] / len(data)
    probabilityF = p[0] / len(data)

    if which:
        return probabilityT
    else:
        return probabilityF


def calculateEntropy(data, datasetLength):
    _entropy = {}
    _entropy[0] = 0
    _entropy[1] = 0

    for i in range(len(data)):
        if int(data[i][datasetLength - 1]) == 0:
            _entropy[0] += 1
        if int(data[i][datasetLength - 1]) == 1:
            _entropy[1] += 1

    intermediate1 = _entropy[0] / len(data)
    intermediate2 = _entropy[1] / len(data)

    logintermediate1 = 0
    logintermediate2 = 0

    if intermediate1 == 0:
        logintermediate1 = 0
    else:
        logintermediate1 = math.log2(intermediate1)

    if intermediate2 == 0:
        logintermediate2 = 0
    else:
        logintermediate2 = math.log2(intermediate2)
    entropy = -(intermediate1) * logintermediate1 - ((intermediate2) * logintermediate2)
    return entropy

def check(tree, dataLength):
    if tree.Leaf == False:
        for i in tree.children:
            check(i, dataLength)
    if tree.Leaf == True:
        if tree.classifiedAs == "+":
            for i in tree.bin:
                Positive.append(i)
        else:
            for i in tree.bin:
                Negative.append(i)
def returnCheck():
    classified = classifier()
    classified.positive = deepcopy(Positive)
    classified.negative = deepcopy(Negative)

    return classified

def ListProb(list, dataLength):
    positive = 0
    negative = 0

    for i in list:
        if int(i[dataLength-1]) == 1:
            positive +=1

    percentage = float(positive/len(list))
    return percentage