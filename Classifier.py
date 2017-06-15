from Tkinter import *
import pandas as pd
import numpy as np
import csv
import operator

class Classifier:

    train = None
    testDF = None
    classification_results = []
    m = 2
    # dictionary - key: class, value: array [count of class, probability]
    classesData = {}
    # table for the pre-processing, calculate all the train file probability
    attrPro = pd.DataFrame(columns=['classValue', 'Attribute', 'AttributeValue', 'Probability'])
    testClassified = {}
    path = ""

    def __init__(self, testFile, pathFiles):
        self.train = testFile
        self.path = pathFiles
        self.classProbability()
        self.attributesProbability()


    def classProbability(self):
        classes = self.train["class"].unique()
        countClasses = pd.value_counts(self.train["class"])
        classPro = countClasses / (countClasses.sum())
        for cls in classes:
            self.classesData[cls] = [countClasses[cls], classPro[cls]]

    def attributesProbability(self):
        # for each attribute in the train file
        for attribute in self.train:
            if attribute != "class":
                # go through all the classes
                for key, value in self.classesData.items():
                    # get the unique values for each attribute
                    atrrValues = self.train[attribute].unique()
                    for atrr in atrrValues:
                        # p in the formula
                        atrrCounter = self.train[attribute].unique().size
                        # Nc in the formula
                        numOfShowes = len(self.train[(self.train[attribute] == atrr) & (self.train[self.train.columns[-1]] == key)])
                        # calculate the formula
                        result = float(numOfShowes + self.m * float(1 / atrrCounter)) / float(value[0] + self.m)
                        # add the result to the table
                        self.attrPro.loc[len(self.attrPro)] = [key, attribute, atrr, result]


    def classify(self, test):
        self.testDF = test
        for index in range(0, test.count()[0]):
            classProbList = {}
            for classKey, classValue in self.classesData.items():
                multiplier = float(1)
                for key, value in test.iteritems():
                    if key != "class":
                        probabiRow = self.attrPro[(self.attrPro['classValue'] == classKey) & (self.attrPro['Attribute'] == key) & (self.attrPro['AttributeValue'] == value[index])]['Probability']
                        if probabiRow.empty:
                            probability = 0
                        else:
                            probability =float(probabiRow.values[0])
                        multiplier = float(multiplier) * float(probability)
                # Calculate P(Ci)*P(X | Ci)
                classProb = float(multiplier) * float(classValue[1])
                classProbList[classKey] = float(classProb)
            # classify the record according to the max probability
            maxProb = max(classProbList.iteritems(), key=operator.itemgetter(1))[0]
            self.writeToFile(maxProb, index + 1)
            self.classification_results.append(maxProb)
        print self.get_accuracy()

    def writeToFile(self, classify, index):
        text_file = open(self.path + "/Output.txt", "a")
        text_file.write('%d %s \n' %(index, classify))
        text_file.close()

    def get_accuracy(self):
        hits = int(0)
        test_class = self.testDF["class"]
        classifier_class = self.classification_results
        for i in range(0, self.classification_results.__len__() - 1):
            if test_class[i] == classifier_class[i]:
                hits = hits + 1
        accuracy = "%.3f" % ((float(hits) / float(self.classification_results.__len__())) * 100)
        return accuracy











