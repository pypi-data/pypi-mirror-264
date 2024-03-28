# Matlab saving structure

When you use the function `safeMatfile` from the `mzDataManager` class, it saves it's content to a `.mat` file in the export directory. Here are the details on the structure created by this function in the exported file :

`sample.mat`
- sample (name of file without `.mat`)
    - `fileName` : From which file this data was extracted
    - `filePath` : Where was located the file
    - `metadata`
        - software
        - analyser
        - detector
    - `mz`
    - `intensities`
    - `time`

This is basically a copy of the `mzData` class but all data is united inside one variable which is the file name. It makes easier the import part where you can keep track of all samples whithin their own variable with the same structure.