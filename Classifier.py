from Tkinter import *
import pandas as pd
import numpy as np
import csv

class Classifier:

    train = None

    def __init__(self, testFile):
        self.train = testFile
        self.train.to_csv('C:\Users\Keren\Desktop\output.csv', index=False)
        # print self.train




