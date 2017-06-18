import pandas as pd
import tkMessageBox


class FilesHandler:

    train = None
    test = None
    path = ""
    numOfBins = 0
    structureFile = None
    structureDic = dict()
    errorLabel = None

    def __init__(self,):
        i=0

    def createStstructureDic(self, file):
        lines = file.read().splitlines()
        structureArr = []
        for line in lines:
            structureArr.append(line.split(" "))
        for attribute in structureArr:
            if attribute[2] == "NUMERIC":
                self.structureDic[attribute[1]] = attribute[2]
            else:
                atrrList = attribute[2].replace("{", "").replace("}", "").split(",")
                self.structureDic[attribute[1]] = atrrList
        return self.structureDic
