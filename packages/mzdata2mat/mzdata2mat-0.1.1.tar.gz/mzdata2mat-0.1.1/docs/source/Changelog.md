
# Changelog

## Version `0.1.0`
### Key elements of this release
- Removed usage of deprecated packages (PyExecJS)
- Added new dependant package (JSPyBridge)
- __Added Windows 11 compatibility__
- __Extended compatibility__ to python versions between `3.9` and `3.12` !
- Added metadata to the mat file created. Contents :
    - software
    - analyser
    - detector
- Added function `convertFile` which converts directly the mzData file into matlab file without calling `mzDataXMLread` and `saveMatfile` separatly.
- Created the `errors` module which contains the possible exceptions.
- Added debug elements to the CLI (`mzdata2mat-verify`) which prints into the console the verify status.
- Reduced package's size
- __Opened a GitHub__ for the package. If you encounter any bug, open an issue there.
- __New documentation__ available on [mzdata2mat.readthedocs.io](https://mzdata2mat.readthedocs.io). Go check it out !
- Added this changelog to keep track of the new realeases and changes.
- Various improvements & bug fixes

### Release date : 03/27/2024

## Version `0.0.1` to `0.0.22`
### Key elements of those releases
- First release of the software
- macOS only compatible
- Python version required : `3.12`
- CLI for verifying successful intallation : `mzdata2mat-verify`
- Bug fixes and improvements

### Release date : 03/21/2024
