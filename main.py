from Tkinter import *
import tkFileDialog
import pandas as pd
import tkMessageBox
from Classifier import *
from FilesHandler import *
from DataCleaner import *
import os


class NaiveBayesClassifier:

    # data members
    master = None
    filePath = ""
    numOfBins = 0
    train = None
    test = None
    structureFile = None
    wasBuilt = False
    structureDic = {}
    fileHandler = None
    classifier = None
    dataCleaner = None

    # Initialize the GUI
    def __init__(self, master):
        self.master = master
        master.title("Naive Bayes Classifier")
        master.geometry("650x300")

        # <editor-fold desc="init buttons, labels and entries">
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
        #</editor-fold>
        # Define grid
        self.gridDefinition(master)
        # layout the controls in the grid
        self.controlsLayout()

    # <editor-fold desc="Gui Functions">
    def controlsLayout(self):
        self.labelPath.grid(row=1, column=0, sticky=E)
        self.entryPath.grid(row=1, column=1, columnspan=2, sticky=W)
        self.browse_button.grid(row=1, column=3, sticky=W)
        self.labelDiscBins.grid(row=2, column=0, sticky=E)
        self.entryDiscBins.grid(row=2, column=1, sticky=W)
        self.labelErr.grid(row=4, column=0, columnspan=4, sticky=W)
        self.build_button.grid(row=5, column=1, columnspan=2)
        self.classify_button.grid(row=6, column=1, columnspan=2)
        self.close_button.grid(row=7, column=1, columnspan=2)

    def gridDefinition(self, master):
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
    # </editor-fold>

    # Build button was clicked
    def build(self):
        #try:
            self.train = pd.read_csv(self.entryPath.get() + "/train.csv")
            if self.validate(self.entryDiscBins.get()):
                # load train file, test file and structure file
                if (os.path.getsize(self.entryPath.get() + "/Structure.txt") == 0):
                    raise Exception("The structure file is empty")
                self.structureFile = open(self.entryPath.get() + "/Structure.txt")
                self.fileHandler = FilesHandler()
                self.structureDic = self.fileHandler.createStstructureDic(self.structureFile)
                self.dataCleaner = DataCleaner(self.structureDic, self.numOfBins)
                self.toLowerCase("train")
                self.train = self.dataCleaner.trainCleaning(self.train)
                self.classifier = Classifier(self.train, self.entryPath.get(), self.structureDic, self.numOfBins)
                self.wasBuilt = True
                tkMessageBox.showinfo("Build Message", "Building classifier using train-set is done!")
        #except Exception as e:
        #   tkMessageBox.showinfo("Error Message", "Something went wrong:\n" + str(e))

    # Clasify button was clicked
    def classify(self):
     try:
         if self.wasBuilt:
            self.test = pd.read_csv(self.entryPath.get() + "/test.csv")
            self.toLowerCase("test")
            self.test = self.dataCleaner.testCleaning(self.test)
            self.classifier.classify(self.test)
            tkMessageBox.showinfo("Classify Message", "Classifying the test-set to the chosen path is done!")
            sys.exit(0)
         else:
            tkMessageBox.showinfo("Error Message", "Please build before Classifying")
     except Exception as e:
         tkMessageBox.showinfo("Error Message", "Something went wrong:\n" + str(e))

    # Trnasfer dataset to lowercase
    def toLowerCase(self, file):
        for attribute in self.structureDic:
            if self.structureDic[attribute] != "NUMERIC" and attribute != "class":
                if file == "train":
                    self.train[attribute] = self.train[attribute].str.lower()
                else:
                    self.test[attribute] = self.test[attribute].str.lower()

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
            if self.numOfBins < 1:
                self.labelErr['text'] = "The number for \"Discretization Bins\" should be bigger than 0"
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


root = Tk()
my_gui = NaiveBayesClassifier(root)
root.mainloop()

