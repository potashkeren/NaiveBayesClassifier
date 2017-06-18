import pandas as pd
import tkMessageBox


class FilesHandler:

    structureDic = dict()

    def __init__(self,):
        i=0

    def createStstructureDic(self, file):
        self.structureDic = dict()
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
