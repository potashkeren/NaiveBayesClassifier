
from Tkinter import *
import tkFileDialog
import pandas as pd
import numpy as np
import tkMessageBox
import math
import Classifier

from scipy.stats import mode

class NaiveBayesClassifier:

    # data members
    master = None
    filePath = ""
    numOfBins = 0
    train = None
    test = None
    structureArr = []
    structureFile = None
    classifier = None

    def __init__(self, master):

        self.master = master
        master.title("Naive Bayes Classifier")
        master.geometry("500x300")

        # init buttons, labels and entries
        self.labelPath = Label(master, text="Directory Path:")
        self.entryPath = Entry(master, width=50)
        self.browse_button = Button(master, text="Browse", width=10, command=self.askopenfile)
        self.browse_button.pack()

        self.labelDiscBins = Label(master, text="Discretization Bins:")
        vcmd = master.register(self.validate)   # we have to wrap the command
        self.entryDiscBins = Entry(master, width=20, validate="key", validatecommand=(vcmd, '%P'))

        self.build_button = Button(master, text="Build", width=20, command=self.build)
        self.build_button.pack()
        self.labelErr = Label(master, text="")

        self.classify_button = Button(master, text="Classify", width=20, command=self.classify)
        self.classify_button.pack()

        self.close_button = Button(master, text="Exit", width=10, command=master.quit)
        self.close_button.pack()

        # Define grid
        master.grid_rowconfigure(0, weight=2)
        master.grid_rowconfigure(1, weight=1)
        master.grid_rowconfigure(2, weight=1)
        master.grid_rowconfigure(3, weight=1)
        master.grid_rowconfigure(4, weight=1)
        master.grid_rowconfigure(5, weight=1)
        master.grid_rowconfigure(6, weight=1)
        master.grid_rowconfigure(7, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_columnconfigure(2, weight=1)
        master.grid_columnconfigure(3, weight=2)

        # LAYOUT
        self.labelPath.grid(row=1, column=0, sticky=E)
        self.entryPath.grid(row=1, column=1, columnspan=2, sticky=W)
        self.browse_button.grid(row=1, column=3, sticky=W)

        self.labelDiscBins.grid(row=2, column=0, sticky=E)
        self.entryDiscBins.grid(row=2, column=1, sticky=W)

        self.labelErr.grid(row=4, column=1, columnspan=2)
        self.build_button.grid(row=5, column=1, columnspan=2)
        self.classify_button.grid(row=6, column=1, columnspan=2)
        self.close_button.grid(row=7, column=1, columnspan=2)

    def askopenfile(self):
        self.filePath = tkFileDialog.askdirectory()
        self.entryPath.delete(0, END)
        self.entryPath.insert(0, self.filePath)

    def build(self):
        if self.validate(self.entryDiscBins.get()):

            # load train file, test file and structure file

            # self.structureFile = pd.read_csv(self.entryPath.get() + "/Structure.txt")
            # print self.structureFile

            self.structureFile = open(self.entryPath.get() + "/Structure.txt")
            lines = self.structureFile.read().splitlines()
            for line in lines:
                self.structureArr.append(line.split(" "))
            self.train = pd.read_csv(self.entryPath.get() + "/train.csv")
            self.fillMissingValues()
            self.discretize()
            self.classifier = Classifier.Classifier(self.train)
            tkMessageBox.showinfo("Build Message", "Building classifier using train-set is done!")

    def discretize(self):
        for arr in self.structureArr:
            if arr[2] == "NUMERIC":
                self.train[arr[1]] = self.binning(self.train[arr[1]])

    def validate(self, new_text):
        if not new_text:  # the field is being cleared
            self.labelErr['text'] = "Please enter a number"
            return False
        try:
            self.numOfBins = int(new_text)
            self.labelErr['text'] = ""
            return True
        except ValueError:
            self.labelErr['text'] = "Invalid input - Please enter a number"

    def fillMissingValues(self):
        for arr in self.structureArr:
            if arr[2] == "NUMERIC":
                self.train[arr[1]].fillna(self.train[arr[1]].mean(), inplace=True)
            elif arr[1] != "class":
                self.train[arr[1]].fillna(self.train[arr[1]].mode()[0], inplace=True)

    def binning(self, col):

        # Define min and max values
        minval = col.min()
        maxval = col.max()

        # cut_points = np.histogram(col, bins=self.numOfBins, range=None, normed=False, weights=None, new=None)
        interval = float(maxval - minval) / float(self.numOfBins)
        tmpInterval = float(interval + minval)
        cut_points = []
        while tmpInterval < maxval:
            cut_points.append(tmpInterval)
            tmpInterval = interval + tmpInterval

        # create list by adding min and max to cut_points
        break_points = [-float("inf")] + cut_points + [float("inf")]
        # if no labels provided, use default labels 0 ... (n-1)
        labels = range(len(cut_points)+1)
        # Binning using cut function of pandas
        colBin = pd.cut(col, bins=break_points, labels=labels, include_lowest=True)
        return colBin

    def classify(self):
        self.test = pd.read_csv(self.entryPath.get() + "/test.csv")

root = Tk()
my_gui = NaiveBayesClassifier(root)
root.mainloop()


