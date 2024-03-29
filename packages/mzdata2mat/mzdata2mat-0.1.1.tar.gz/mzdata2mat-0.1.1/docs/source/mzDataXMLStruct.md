# mzDataXMLStruct

## Presentation
Internal class, do not use it to store data. Consider using [mzData](mzData.md) class instead.

## Definition
```python
class mzDataXMLStruct(BaseModel):
    metadata : dict
    times : list[float]
    series : Any
```
## How to use
```python
value = mzDataXMLStruct(
    metadata = someDict,
    times = listOfTimes,
    series = series
)
```

## Functions
None

## Notes
This is an __internal__ class, it shouldn't be used to store mz values. This class is automatically populated when parsing a `.mzData.xml` file and is private.

Consider using [mzData](mzData.md) class to store your mz and intensities values.