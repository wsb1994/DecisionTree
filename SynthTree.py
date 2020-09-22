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



class DTree:
    def __init__(self, data, maxDepth, parentDepth, datasetLength, boundaries, Parent):
        self.thisData = deepcopy(data)
        self.maxDepth = maxDepth
        self.depth = 1 + parentDepth
        self.boundaries = boundaries

        self.indexDiscriminated = -1
        self.entropy = -(math.inf)
        self.gain = -(math.inf)
        # True, False
        self.classifiedAs = None
        self.Leaf = False
        self.Parent = Parent
        self.isBinary = False
        self.children = []

        if self.depth == maxDepth:
            self.Leaf = True
            self.classify(datasetLength)
            return
        else:
            self.determineEntropy(datasetLength)
            self.detectBinary(datasetLength)
            self.Expand(datasetLength, self.depth)
            
    def detectBinary(self, dataSetLength):
        counter = 0
        for i in range(len(self.thisData)):
            if int(self.thisData[i][self.indexDiscriminated]) != 1 or abs(int(self.thisData[i][self.indexDiscriminated])) != 0 :
                counter = counter + float(self.thisData[i][self.indexDiscriminated])
        
        if counter == 0:
            self.isBinary == True
        

    def classify(self, datasetLength):
        count = 0
        for i in self.thisData:
            if int(i[datasetLength-1]) == 1:
                count += 1

        try:
            ratio = count / len(self.thisData)

            if ratio >= .5:
                self.classifiedAs = 1
            else:
                self.classifiedAs = 0
        except:
            self.classifiedAs = self.Parent.classifiedAs

    def Expand(self, datasetLength, parentDepth):
        if self.isBinary == True:
            for i in range(2):
                for j in range(len(self.thisData)):
                    if int(self.thisData[j][self.indexDiscriminated]) == 1:
                        Positive.append(deepcopy(self.thisData[j]))
                    else:
                        Negative.append(deepcopy(self.thisData[j]))
            self.children.append(DTree(deepcopy(Negative),self.maxDepth, self.depth, len(Negative[0]), self.boundaries, self))
            self.children.append(DTree(deepcopy(Positive),self.maxDepth, self.depth, len(Positive[0]), self.boundaries, self))
            return
        if len(self.thisData) == 0:
            return
        if len(self.thisData) == 1:
            self.classify(datasetLength)
            return
        prevboundary = 0
        for boundaryBin in range(len(self.boundaries[self.indexDiscriminated])):
            for entry in range(prevboundary, boundaryBin):
                self.thisData[entry][self.indexDiscriminated] = boundaryBin
            prevboundary = boundaryBin

        for i in range(len(self.boundaries[self.indexDiscriminated])):
            child = []
            for entry in range(len(self.thisData)):
                if int(self.thisData[entry][self.indexDiscriminated]) == i:
                    child.append(self.thisData[entry])
            if child:
                self.children.append(DTree(deepcopy(child),self.maxDepth, self.depth, len(child[0]), self.boundaries, self))

    def determineEntropy(self, datasetLength):
        self.entropy = setEntropy(self.thisData, datasetLength)
        localMaxInformationGain = -(math.inf)
        for i in range(datasetLength-1):
            localEntropies = self.informationGain(i, len(self.boundaries[i]))
            localEntropy = 0
            for j in localEntropies:
                localEntropy = localEntropy + j
            # grab average
            localEntropy = localEntropy/len(localEntropies)

            informationGain = deepcopy(self.entropy) - localEntropy

            if i != datasetLength-1:
                if informationGain > localMaxInformationGain:
                    localMaxInformationGain = informationGain
                    self.indexDiscriminated = deepcopy(i)
        
        if float(localMaxInformationGain) == -0.0:
            localMaxInformationGain = abs(localMaxInformationGain)

        self.gain = localMaxInformationGain

    def informationGain(self, variable, datasetLength):
        count = {}

        for i in range(datasetLength):
            count[int(i)] = 0

        for i in self.thisData:
            length = len(self.thisData[0])-1
            if int(i[length]) == 1:
                count[i[variable]] += 1
        entropy = []
        for i in count:
            entropy.append(calculateEntropy(count[i], len(self.thisData)))
        return entropy


def calculateEntropy(dataPoints, sizeofData):
    intermediate1 = dataPoints / sizeofData
    intermediate2 = dataPoints / sizeofData

    logintermediate1 = 0
    logintermediate2 = 0

    if intermediate1 == 0:
        logintermediate1 = 0
    elif intermediate1 == 1:
        logintermediate1 = 1
    else:
        logintermediate1 = math.log2(intermediate1)

    if intermediate2 == 0:
        logintermediate2 = 0
    elif intermediate2 == 1:
        logintermediate2 = 1
    else:
        logintermediate2 = math.log2(intermediate2)

    entropy = -(intermediate1) * logintermediate1 + \
        -((intermediate2) * logintermediate2)
    if entropy == -0.0:
        entropy = abs(entropy)
    return entropy


def setEntropy(data, datasetLength):
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
    entropy = -(intermediate1) * logintermediate1 - \
        ((intermediate2) * logintermediate2)
    return entropy

def check(tree, dataLength):
    if tree.Leaf == False and tree.thisData:
        for i in tree.children:
            check(i, dataLength)
    if tree.Leaf == True:
        if tree.classifiedAs == 1:
            for i in tree.thisData:
                Positive.append(i)
        else:
            for i in tree.thisData:
                Negative.append(i)
def checkHandler(tree, dataLength):
    check(tree, dataLength)

    PositiveCount = 0
    NegativeCount = 0
    for i in range(len(Positive)):
        if int(Positive[i][dataLength-1]) == 1:
            PositiveCount +=1
    for j in range(len(Negative)):
        if int(Negative[j][dataLength-1]) == 0:
            NegativeCount +=1
    totalAccuracy = PositiveCount + NegativeCount

    totalAccuracy = totalAccuracy/ (len(Negative)+ len(Positive))

    return totalAccuracy