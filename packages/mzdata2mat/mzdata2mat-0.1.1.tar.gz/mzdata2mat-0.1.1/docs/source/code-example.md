# Example Code
This page gives two examples on how to use the package. More examples will be added in the future.

## In two lines
You can acheive the conversion with only two lines of code :

```python
from mzdata2mat import mzDataManager

mzDataManager(useDirectory=False).convertFile(<path2mzDataFile>, <path2folder2save>)

```
## More detailled example

```python

# Here we import the main class used for the conversion.
1 from mzdata2mat import mzDataManager

# We initialize the class
# If all mzData files are stored in the same directory, we can specify the parameter `mzDataPath` instead of `useDirectory`.
2 converterAgent = mzDataManager(useDirectory=False)

3 path2mzDataFile : str = "path/to/stored/files"

4 someDirectory : str = "path/to/save/file/"

# Now we can call the mzDataXMLread function to read the .mzData.xml file:
5 data = converterAgent.mzDataXMLread(fileName=path2mzDataFile)

# The data we've got from the previous function can be saved to a .mat file with the saveMatfile funtion:
6 converterAgent.saveMatfile(mzData=data, dir2save=someDirectory)

```