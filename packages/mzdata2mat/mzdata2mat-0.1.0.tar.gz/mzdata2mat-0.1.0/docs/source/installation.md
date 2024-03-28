# Installation
## Command
To install `mzdata2mat` into your Python environment, run the following command inside your terminal :
```shell
$ pip install mzdata2mat
```
If you have multiple instances of Python installed, run this command with the chosen Python interpreter to install `mzdata2mat` in the corresponding Python installation :
```shell
$ <pathToPythonApp> -m pip install mzdata2mat
```
When the command terminates, you have successfully installed mzdata2mat !

## Verify the installation
To verfiy if the installation was successful, run in your terminal this command :
```shell
$ mzdata2mat-verify
```
When you will first run this command, node.js will download and install the `mzdata` package from `npm`. This will only happen the first time you run the command. The terminal will show you these lines during the process :
```shell
 Installing 'mzdata' version 'latest'... This will only happen once. 

added 7 packages, and audited 8 packages in 2s

1 package is looking for funding
  run `npm fund` for details

found 0 vulnerabilities

 OK. 
[JSE] 

[JSE] 
```
When it's done, the `mzdata2mat` package will attempt to convert an example `.mzdata.xml` file into a `.mat` file. If everything goes right, you will get this message :
```shell
$ mzdata2mat - Ready to use !
```
The example file (.mzdata.xml) will be copied in the current working directory and the converted file (.mat) will be added as soon as the conversion finishes.

## Troubbleshooting
If an error occurs, this probably means that you do not have __node.js__ installed on your machine or you didn't add it to your PATH.