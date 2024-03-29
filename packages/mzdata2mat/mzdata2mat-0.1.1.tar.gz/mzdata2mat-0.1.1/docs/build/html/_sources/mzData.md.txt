# mzData

## Presentation
This is the Base class which holds all the data collected from a given `mzdata.xml` file. This is the data class used when the `mzDataManager` creates a `.mat` file.<br>
You can create your own instances of this class if your data is not collected from the mzData files.

## Definition
```python
class mzData(BaseModel):
    fileName : str = None
    filePath : str = None
    metadata : dict = None
    mz : list[list[float]] = [[]]
    intensities : list[list[float]] = [[]]
    time : list[float] = []
```

## How to use
There are two ways of creating this class, the first one is the following :
```python
# Class creation
data = mzData()

# The script below could be called anywhere you want, just be sure to fill all necessary data before calling the saveMatfile function from the mzdataManager class.
data.fileName = "sample.mzdata.xml"
data.filePath = "some/path/"
data.metadata = {
    'software' : 'someSoftware',
    'analyser' : 'John Doe',
    'detector' : 'someDetector'
}
data.mz = mzList
data.intensities = intensitiesList
data.time = timeList
```
If you have all informations at the same time, you could use the second way of defining the class :
```python
data = mzData(
    fileName = "sample.mzdata.xml",
    filePath = "some/path/",
    metadata = {
    'software' : 'someSoftware',
    'analyser' : 'John Doe',
    'detector' : 'someDetector'
    },
    mz = mzList,
    intensities = intensitiesList,
    time = timeList
)
```

## Functions
None

## Notes
There is in fact a function called `toDict`, but it is intended to be used by the manager class. The only thing it does is convert the structure into the format needed by the `.mat` format.
