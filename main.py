from Tkinter import *
import tkFileDialog
import pandas as pd
import tkMessageBox
import Classifier


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
    discBins = {}
    wasBuilt = False

    # Initialize the GUI
    def __init__(self, master):

        self.master = master
        master.title("Naive Bayes Classifier")
        master.geometry("650x300")

        # init buttons, labels and entries
        self.labelPath = Label(master, text="Directory Path:")
        self.entryPath = Entry(master, width=70)
        self.browse_button = Button(master, text="Browse", width=10, command=self.askopenfile)
        self.browse_button.pack()

        self.labelDiscBins = Label(master, text="Discretization Bins:")
        self.entryDiscBins = Entry(master, width=20, validate="key")

        self.build_button = Button(master, text="Build", width=20, command=self.build)
        self.build_button.pack()
        self.labelErr = Label(master, text="", fg="red", font="Verdana 10 bold")

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

        self.labelErr.grid(row=4, column=0, columnspan=4, sticky=W)
        self.build_button.grid(row=5, column=1, columnspan=2)
        self.classify_button.grid(row=6, column=1, columnspan=2)
        self.close_button.grid(row=7, column=1, columnspan=2)

    # Build button was clicked
    def build(self):
        try:
            self.train = pd.read_csv(self.entryPath.get() + "/train.csv")
            if self.validate(self.entryDiscBins.get()):
                # load train file, test file and structure file
                self.structureFile = open(self.entryPath.get() + "/Structure.txt")
                lines = self.structureFile.read().splitlines()
                for line in lines:
                    self.structureArr.append(line.split(" "))
                self.toLowerCase("train")
                self.fillMissingValues()
                self.discretize("train")
                self.classifier = Classifier.Classifier(self.train, self.entryPath.get())
                self.wasBuilt = True
                tkMessageBox.showinfo("Build Message", "Building classifier using train-set is done!")
        except Exception, e:
            tkMessageBox.showinfo("Error Message", "Something went wrong:\n" + str(e))

    # Clasify button was clicked
    def classify(self):
     try:
         if self.wasBuilt:
            self.test = pd.read_csv(self.entryPath.get() + "/test.csv")
            self.toLowerCase("test")
            self.discretize("test")
            self.classifier.classify(self.test)
            tkMessageBox.showinfo("Classify Message", "Classifying the test-set to the chosen path is done!")
            self.reset()
         else:
            tkMessageBox.showinfo("Error Message", "Please build before Classifying")
     except Exception, e:
         tkMessageBox.showinfo("Error Message", "Something went wrong:\n" + str(e))

    # Fill missing values in the dataser
    def fillMissingValues(self):
        for arr in self.structureArr:
            if arr[2] == "NUMERIC":
                self.train[arr[1]].fillna(float(self.train[arr[1]].mean()), inplace=True)
            elif arr[1] != "class":
                self.train[arr[1]].fillna(self.train[arr[1]].mode()[0], inplace=True)

    # Discretisiza the data
    def discretize(self, file):
        for attribute in self.structureArr:
            if attribute[2] == "NUMERIC":
                if file == "train":
                    self.createBins(self.train[attribute[1]], attribute[1])
                    self.train[attribute[1]] = self.binning(self.train[attribute[1]], self.discBins[attribute[1]])
                else:
                    self.test[attribute[1]] = self.binning(self.test[attribute[1]], self.discBins[attribute[1]])

    # Create binning array
    def binning(self, col, break_points):
        # if no labels provided, use default labels 0 ... (n-1)
        labels = range(len(break_points)-1)
        # Binning using cut function of pandas
        colBin = pd.cut(col, bins=break_points, labels=labels, include_lowest=True)
        return colBin

    # Calculate bins for tarin
    def createBins(self, col, attributeName):
        # Define min and max values
        minval = float(col.min())
        maxval = float(col.max())

        interval = float(maxval - minval) / float(self.numOfBins)
        tmpInterval = float(interval + minval)
        cut_points = []
        while tmpInterval < maxval:
            cut_points.append(tmpInterval)
            tmpInterval = float(interval + tmpInterval)

        # create list by adding min and max to cut_points
        break_points = [-float("inf")] + cut_points + [float("inf")]
        self.discBins[attributeName] = break_points

    # Trnadfer dataset to lowercase
    def toLowerCase(self, file):
        for arr in self.structureArr:
            if arr[2] != "NUMERIC" and arr[2] != "class":
                if file == "train":
                    self.train[arr[1]] = self.train[arr[1]].str.lower()
                else:
                    self.test[arr[1]] = self.test[arr[1]].str.lower()

    # Open file dialog openrer
    def askopenfile(self):
        self.filePath = tkFileDialog.askdirectory()
        self.entryPath.delete(0, END)
        self.entryPath.insert(0, self.filePath)

    # Validate input
    def validate(self, new_text):
        if not new_text:  # the field is being cleared
            self.labelErr['text'] = "Please enter a number"
            return False
        try:
            self.numOfBins = int(new_text)
            # check validate number
            if self.numOfBins < 2:
                self.labelErr['text'] = "The number for \"Discretization Bins\" should be bigger than 1"
                return False
            elif self.numOfBins > self.train.count()[0]:
                self.labelErr['text'] = "\"Discretization Bins\" shouldn't be higher then the number of records"
                return False
            # if the numer is valid
            else:
                self.labelErr['text'] = ""
                return True

        except ValueError:
            self.labelErr['text'] = "Invalid input - Please enter a number"

    # Reset global variables
    def reset(self):
        # reseet data members
        self.master = None
        self.filePath = ""
        self.numOfBins = 0
        self.train = None
        self.test = None
        self.structureArr = []
        self.structureFile = None
        self.classifier = None
        self.discBins = {}
        self.wasBuilt = False

root = Tk()
my_gui = NaiveBayesClassifier(root)
root.mainloop()


