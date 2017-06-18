from Tkinter import *
import pandas as pd
import numpy as np
import csv
import operator

class Classifier:

    train = None
    testDF = None
    classification_results = []
    structure = []
    m = 2
    # dictionary - key: class, value: array [count of class, probability]
    classesData = {}
    # table for the pre-processing, calculate all the train file probability
    atrrProDic = dict()
    testClassified = {}
    path = ""
    numOfBins = 0

    def __init__(self, testFile, pathFiles, structure,numOfBins):
        self.train = testFile
        self.path = pathFiles
        self.structure = structure
        self.numOfBins = numOfBins
        self.classProbability()
        self.attributesProbability()

    # Calculate the class probability
    def classProbability(self):
        classes = self.train["class"].unique()
        countClasses = pd.value_counts(self.train["class"])
        classPro = countClasses / (countClasses.sum())
        for cls in classes:
            self.classesData[cls] = [countClasses[cls], classPro[cls]]

    # Calculate attributes probabilities
    def attributesProbability(self):
        # go through all the classes
        for key, value in self.classesData.items():
            attrProbabality = dict()
            # for each attribute in the train file
            for attribute in self.structure:
                if attribute != "class":
                    attrProbabality[attribute] = dict()
                    if self.structure[attribute] == "NUMERIC":
                        for i in range(0, self.numOfBins):
                          # Nc in the formula
                          numOfShowes = len(self.train[(self.train[attribute] == i) & (self.train[self.train.columns[-1]] == key)])
                          # calculate the formula
                          result = float(numOfShowes + self.m * float(1.0 / self.numOfBins)) / float(value[0] + self.m)
                          # add the result to the table
                          attrProbabality[attribute][i] = result
                    else:
                        listatrr = self.structure[attribute]
                        for atrr in listatrr:
                          # Nc in the formula
                          numOfShowes = len(self.train[(self.train[attribute] == atrr) & (self.train[self.train.columns[-1]] == key)])
                          # calculate the formula
                          result = float( numOfShowes+ float(self.m * float(1.0 / listatrr.__len__()))) /float(value[0] + self.m)
                          # add the result to the table
                          attrProbabality[attribute][atrr] = result
            self.atrrProDic[key] = attrProbabality


    # Naive bayes calculation
    def classify(self, test):
        self.classification_results = []
        self.testDF = test
        text_file = open(self.path + "/Output.txt", "w")

        # classify each row in the testFile
        for index in range(0, test.count()[0]):
            classProbList = {}
            # calculate evidence probability for each class
            for classKey, classValue in self.classesData.items():
                multiplier = float(1)
                # multiply the probabilities of all attribute's probability for this evidence by file training
                for key, value in test.iteritems():
                    if key != "class":
                        probability = self.atrrProDic[classKey][key][value[index]]
                        multiplier = float(multiplier) * float(probability)
                # Calculate P(Ci)*P(X | Ci)
                classProb = float(multiplier) * float(classValue[1])
                classProbList[classKey] = float(classProb)
            # classify the record according to the max probability
            maxProb = max(classProbList.iteritems(), key=operator.itemgetter(1))[0]
            text_file.write('%d %s\n' % (index+1, maxProb))
            self.classification_results.append(maxProb)
        text_file.close()
        self.get_accuracy()

    # returns algorithm's accuracy
    def get_accuracy(self):
        hits = int(0)
        test_class = self.testDF["class"]
        classifier_class = self.classification_results
        for i in range(0, self.classification_results.__len__() - 1):
            if test_class[i] == classifier_class[i]:
                hits = hits + 1
        accuracy = "%.3f" % ((float(hits) / float(self.classification_results.__len__())) * 100)
        print (accuracy)

    def reset(self):
        self.train = None
        self.testDF = None
        self.classification_results = []
        self.structure = []
        self.m = 2
        self.classesData = {}
        self.atrrProDic = dict()
        self.testClassified = {}
        self.path = ""
        self.numOfBins = 0












