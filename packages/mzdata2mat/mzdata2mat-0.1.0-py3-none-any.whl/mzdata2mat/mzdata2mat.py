from pydantic import BaseModel
from mat4py import savemat
from javascript import require
from javascript.errors import JavaScriptError
from .errors import mzDataError
import os
import shutil
from typing import Any

class mzDataXMLStruct(BaseModel):
    metadata : dict
    times : list[float]
    series : Any

class mzData(BaseModel):
    fileName : str = None
    filePath : str = None
    metadata : dict = None
    mz : list[list[float]] = [[]]
    intensities : list[list[float]] = [[]]
    time : list[float] = []

    def toDict(self):
        tempDict = self.model_dump()
        return {self.fileName.lower().split(".mzdata")[0] : tempDict}

class mzDataManager(BaseModel):
    mzDataPath : str = None
    exportPath : str = None
    mzDataPackage : str = None

    def __init__(self, useDirectory : bool = True, mzDataPath : str = None, exportPath : str = None):
        """Main class for converting .mzData.xml files into .mat files for realeases of Matlab r2019b and newer.
        -> `mzDataPath` : Path to the folder containing the .mzdata.xml files \n
        -> `exportPath` : Path to save the converted .mat files \n
        -> `useDirectory` : Set this parameter to `False` to not use directories and specify them when using the functions.
        
        """
        if useDirectory:
            if os.path.isdir(mzDataPath) and os.path.exists(mzDataPath):
                self.mzDataPath = mzDataPath
            else:
                raise mzDataError("The directory entered for .mzdata.xml files is not valid", 3)
            if os.path.isdir(exportPath) and os.path.exists(exportPath):
                self.exportPath = exportPath
            else:
                raise mzDataError("The directory entered for converted .mat files is not valid")
        super().__init__()
        try:
            self.mzDataPackage = require('mzdata')
        except Exception as e:
            # This error will often be related with node.js not being installed on the target machine.
            raise e

    def mzDataXMLread(self, fileName : str, customDirectory : bool = False):
        """
        Reads mzML files and returns the given object.\n
        -> `fileName` :\n
            -> Should be the full path to the file and it's extension (.mzdata.xml) to convert if no value was given to `mzDataPath` when initializing the class.\n
            -> Otherwise, the file's relative path with it's extension (.mzdata.xml)\n
        -> `customDirectory` : Set this parameter to `True` if the `fileName` is in a different path than the one given in configuration.
        """
        try:
            if self.mzDataPath == None or customDirectory:
                    if os.path.exists(fileName):
                        result = self.mzDataPackage.parseMZ(open(fileName).read())
                    else:
                        raise mzDataError("The path given for the mzData file is not valid.", 10)
            else:
                if os.path.exists(os.path.join(self.mzDataPath, fileName)):
                    result = self.mzDataPackage.parseMZ(open(os.path.join(self.mzDataPath, fileName)).read())
                else:
                    raise mzDataError("The path given for the mzData file is not valid.", 10)
        except JavaScriptError as e:
            raise e
        metadata = {
            'software' : str(result.metadata["software"]),
            'analyser' : str(result.metadata["analyser"]),
            'detector' : str(result.metadata["detector"])
        }
        dataStruct = mzDataXMLStruct(metadata=metadata, times=list(result.times), series=result.series["ms"]["data"])
        returnStruct = mzData()
        totalMasseDataSet = []
        totalIntensityDataSet = []
        for i in dataStruct.series:
            massesDataSet = []
            intensityDataSet = []
            for y in range(len(list(i[0]))):
                massesDataSet.append(i[0][str(y)])
            for z in range(len(list(i[1]))):
                intensityDataSet.append(i[1][str(z)])
            totalMasseDataSet.append(massesDataSet)
            totalIntensityDataSet.append(intensityDataSet)
        returnStruct.mz = totalMasseDataSet
        returnStruct.intensities = totalIntensityDataSet
        returnStruct.time = dataStruct.times
        if customDirectory or self.mzDataPath == None:
            file = fileName
        else:
            file = self.mzDataPath
        returnStruct.filePath = file
        try:
            returnStruct.fileName = file.rsplit("/", 1)[1]
        except IndexError:
            returnStruct.fileName = file.rsplit("\\", 1)[1]
        returnStruct.metadata = dataStruct.metadata
        return returnStruct
    
    def saveMatfile(self, mzData : mzData, remove : bool = False, dir2Save : str = None, force : bool = False):
        """
        Saves a `mzData` structure to a .mat file.\n
        -> `mzData`     : The structure got from `mzMLread` function.\n
        -> `remove`     : Should the original file be removed when it is saved as .mat file ?\n
        -> `dir2Save`   : Save directory to save the .mat file. If path was given in configuration, it is not needed. This parameter will be prioritised over the path given in configuration (if any).\n
        -> `force`      : If a file has the same name in the converted folder, should it be replaced ? (File will not be saved if sibling found in convert folder and this parameter set to `False`.)
        """
        
        if self.exportPath == None or dir2Save != None:
            if os.path.exists(dir2Save):
                saveDir = os.path.join(dir2Save, f"{mzData.fileName.lower().split('.mzdata')[0]}.mat")
            else:
                raise mzDataError("No save directory specified", 4)
        else:
            saveDir = os.path.join(self.exportPath, f"{mzData.fileName.split('.mzdata')[0]}.mat")
        
        if os.path.exists(saveDir):
            if force:
                os.remove(saveDir)
                savemat(saveDir, mzData.toDict())
            else:
                print(f"File {mzData.fileName} skipped because same file exists in export folder and parameter `force` is not set to `True`")
        else:
            savemat(saveDir, mzData.toDict())
        if remove:
            os.remove(os.path.join(mzData.filePath, mzData.fileName))
        return
    
    def convertFile(self, fileName : str, customDirectory : bool = False, dir2Save : str = None, force : bool = False, remove : bool = False):
        """
        Reads mzData.xml file and saves it directly into the folder specified.\n
        -> `fileName` :\n
            -> Should be the full path to the file and it's extension (.mzdata.xml) to convert if no value was given to `mzDataPath` when initializing the class.\n
            -> Otherwise, the file's relative path with it's extension (.mzdata.xml)\n
        -> `customDirectory` : Set this parameter to `True` if the `fileName` is in a different path than the one given in configuration.
        -> `dir2Save`   : Save directory to save the .mat file. If path was given in configuration, it is not needed. This parameter will be prioritised over the path given in configuration (if any).\n
        -> `force`      : If a file has the same name in the converted folder, should it be replaced ? (File will not be saved if sibling found in convert folder and this parameter set to `False`.)
        -> `remove`     : Should the original file be removed when it is saved as .mat file ?\n

        """
        fileContent = self.mzDataXMLread(fileName=fileName, customDirectory=customDirectory)
        self.saveMatfile(mzData=fileContent, remove=remove, dir2Save=dir2Save, force=force)
        return

def verify():
    print("Starting verifying process...")
    try:
        path = os.getcwd()
        testFile = os.path.join(__file__.lower().rsplit("mzdata", 1)[0], "tiny1.mzData.xml")
        print("Creating class... ")
        testClass = mzDataManager(useDirectory=False)
        print("Copying file in current directory...")
        shutil.copyfile(testFile, os.path.join(path, "tiny1.mzData.xml"))
        print("Reading file...")
        value = testClass.mzDataXMLread(os.path.join(path, "tiny1.mzData.xml"))
        print("Saving file...")
        testClass.saveMatfile(value, dir2Save=path)
        print("mzdata2mat - Ready to use !")
    except Exception as e:
        raise e