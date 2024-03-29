# mzDataManager

## Presentation
Main class used for converting mzData files into matlab files.

## Definition
```python
class mzDataManager(BaseModel):
    mzDataPath : str = None
    exportPath : str = None
    useDirectory : bool = True
```

## How to use
### With path
```python
manager = mzDataManager(
    mzDataPath = "Some/Path",
    exportPath = "Some/Export/Path",
)
```
The path you specify in those arguments will be stored in the class, so when you use the integrated functions, you only need to specify the relative path to the file.

### Without path
```python
manager = mzDataManager(useDirectory=False)
```
Setting up the class this way will require to specify each time you call a function to give the full path and the export directory.

## Functions

### mzDataXMLread

#### Presentation
This function reads a `.mzData.xml` file and returns a `mzData` structure which can be modified before saving it's data to a `.mat` file (See [mzData](mzData.md) class for further details).

#### Definition
```python
def mzDataXMLread(self@mzDataManager, fileName : str, customDirectory : bool = False)
```

#### How to use
```python
# Considering that mzDataManager class has been intialized before and stored as manager variable

content = manager.mzDataXMLread(
    fileName=Path2File
)
```
<u>Parameters</u>
- If directories were provided in the init process :
    - `fileName` : Relative path of the `mzData.xml` file to read
    - `customDirectory` : Set this parameter to `True` if you provide a full path which is different than the one specified in the init process.
- Otherwise :
    - `fileName` : Full path to the `mzData.xml` file to read
    - `customDirectory` : Does nothing

<u>Outputs</u>
- Outputs a `mzData` class containing the content of the file parsed.

### saveMatfile
#### Presentation
Saves a `mzData` class into a `.mat` file with all metadata included.

#### Definition
```python
def saveMatfile(self@mzDataManager, mzData : mzData, remove : bool = False, dir2Save : str = None, force : bool = False)
```

#### How to use
```python
# Considering that mzDataManager class has been intialized before and stored as manager variable

# Considering also the variable content which is the result of the function mzDataXMLread presented above

manager.saveMatFile(
    mzData=content
)
```
<u>Parameters</u>
- `mzData` : The `mzData` structure to save as a `.mat` file. (See [here](matStructure.md) for the `.mat` file structure)
- `remove` : Should the original file (so the original `.mzData.xml` file) be removed when save is complete ?
- `force` : If a `.mat` file already exists with the same name in the export folder, should it be replaced ? If this parameter is set to `False`, save will be aborted if a file is found.
- If directories were not provided during init process:
    - `dir2save` : Full directory specifying where to save the converted file. If this parameter is set while a directory was specified in the init process, this value is prioritized.

<u>Outputs</u><br>
If function ran correctly, no output, otherwise raises the error.

### convertFile
#### Presentation
All in one function. Reads `mzData.xml` file and automatically saves it into the export folder. No transition to the `mzData` class.

#### Definition
```python
def convertFile(self@mzDataManager, fileName : str, customDirectory : bool = False, dir2Save : str = None, force : bool = False, remove : bool = False)
```

#### How to use
```python
# Considering that mzDataManager class has been intialized before and stored as manager variable

manager.convertFile(
    fileName=FileName
)
```

<u>Parameters</u>
- `fileName` :<br>
    - Should be the full path to the file and it's extension (.mzdata.xml) to convert if no value was given to `mzDataPath` when initializing the class.
    - Otherwise, the file's relative path with it's extension (.mzdata.xml)
- `customDirectory` : Set this parameter to `True` if the `fileName` is in a different path than the one given in configuration.
- `dir2Save`   : Save directory to save the .mat file. If path was given in configuration, it is not needed. This parameter will be prioritised over the path given in configuration (if any).
- `force`      : If a file has the same name in the converted folder, should it be replaced ? (File will not be saved if sibling found in convert folder and this parameter set to `False`.)
- `remove`     : Should the original file be removed when it is saved as `.mat` file ?

<u>Outputs</u><br>
No outputs