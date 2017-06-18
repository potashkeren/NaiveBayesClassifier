import pandas as pd


class DataCleaner:

    discBins = {}
    structureDic = dict()
    numOfBins = 0

    def __init__(self, structure, bins):
        self.structureDic = structure
        self.numOfBins = bins

    # cleaning the train data
    def trainCleaning(self, trainFile):
        trainComplete = self.fillMissingValues(trainFile)
        trainCleaner = self.discretize("train", trainComplete)
        return trainCleaner

    # cleaning the test data
    def testCleaning(self,testFile):
        return self.discretize("test", testFile)

    # Fill missing values in the dataset
    def fillMissingValues(self, train):
        for attribute in self.structureDic:
            if self.structureDic[attribute] == "NUMERIC":
                train[attribute].fillna(float(train[attribute].mean()), inplace=True)
            elif attribute != "class":
                train[attribute].fillna(train[attribute].mode()[0], inplace=True)
        return train

    # Discretisiza the data
    def discretize(self, fileType, file):
        fileDiscretize = file
        for attribute in self.structureDic:
            if self.structureDic[attribute] == "NUMERIC":
                if fileType == "train":
                    self.createBins(fileDiscretize[attribute], attribute)
                fileDiscretize[attribute] = self.binning(fileDiscretize[attribute], self.discBins[attribute])
        return fileDiscretize

    # Create binning array
    def binning(self, col, break_points):
        # if no labels provided, use default labels 0 ... (n-1)
        labels = range(len(break_points) - 1)
        # Binning using cut function of pandas
        colBin = pd.cut(col, bins=break_points, labels=labels, include_lowest=True)
        return colBin

    # Calculate bins according to train file
    def createBins(self, col, attributeName):
        # Define min and max values
        minval = float(col.min())
        maxval = float(col.max())

        interval = float(maxval - minval) / float(self.numOfBins)
        tmpInterval = float(interval + minval)
        cut_points = []
        for i in range(self.numOfBins-1):
            cut_points.append(tmpInterval)
            tmpInterval = float(interval + tmpInterval)

        # create list by adding min and max to cut_points
        break_points = [-float("inf")] + cut_points + [float("inf")]
        self.discBins[attributeName] = break_points

    def reset(self):
        self.structureDic = dict()
        self.discBins= {}
