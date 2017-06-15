from Tkinter import *
import pandas as pd
import numpy as np
import csv

class Classifier:

    train = None
    m = 2
    # dictionary - key: class, value: array [count of class, probability]
    classesData = {}
    # table for the pre-processing, calculate all the train file probability
    attrPro = pd.DataFrame(columns=['classValue', 'Attribute', 'AttributeValue', 'Probability'])
    testClassified = {}

    def __init__(self, testFile):
        self.train = testFile
        self.classProbability()
        self.attributesProbability()

    def classProbability(self):
        classes = self.train["class"].unique()
        countClasses = pd.value_counts(self.train["class"])
        classPro = countClasses / countClasses.sum()
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
                        result = float(numOfShowes + self.m * (1 / atrrCounter)) / (value[0] + self.m)
                        # add the result to the table
                        self.attrPro.loc[len(self.attrPro)] = [key, attribute, atrr, result]


    def classify(self, test):
        index = 1
        for key, value in test.iteritems():
            for classKey, classValue in self.classesData.items():
                probability = self.attrPro[(self.attrPro['classValue'] == classKey) & (self.attrPro['Attribute'] == key) & (self.attrPro['AttributeValue'] == value[index])]['Probability'].values[0]
            index = index+1







