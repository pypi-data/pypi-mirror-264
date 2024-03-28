# Introduction 
This is a library containing the shared message formats that the python libraries will use to communicate with the RS applications.

# Using the proejct
## If you are using it in a c++ project:  
- Install as a normal c++ nuget in visual studio. Search for "rsmessages" under Rocscience_Feed. Full wiki on how to do this: https://rocscience.visualstudio.com/Rocscience%20Documentation/_wiki/wikis/Rocscience-Documentation.wiki/1056/Adding-Nuget-Packages-To-Existing-Projects

## If you are using it in a python project:  
- run ```pip install keyring artifacts-keyring```
- Follow the guid here: https://rocscience.visualstudio.com/RS2%202018/_artifacts/feed/Rocscience_Feed/connect/pip or run  
```pip install rsmessages --index-url=https://rocscience.visualstudio.com/RS2%202018/_artifacts/feed/Rocscience_Feed/connect/pip```


# Build and Test
following the steps to this guide: https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives 
1. Install python version 3.11.4
2. Run ```python -m pip install --upgrade build```  
3. Run this command from the same directory where pyproject.toml is located:  
```python -m build```  
a 'dist' folder should be generated with a .whl file. You can then run pip install <.whl> file to install the project

# Deploy
This nuget needs to be deployed in 2 different formats: as a c++ nuget and as a python library
## Deploy as a python library
1. Upgrade the version in pyproject.toml
2. build the library (follow the steps above)
3. run 
```pip install twine keyring artifacts-keyring```
3. Follow the "Project setup" guide from https://rocscience.visualstudio.com/RocShare/_artifacts/feed/Rocscience_Feed/connect/twine
4. Deploy the library using:  
```twine upload -r Rocscience_Feed dist/*```
## Deploy as a c++ nuget
1. Upgrade the version in the nuspec
2. In the folder containing the .nuspec file, run:  
 ```nuget pack```
3. After nuget pack, it will create a nupkg file. Copy the file name into 
```nuget.exe push -Source "Rocscience_Feed" -ApiKey az PACKAGE_NAME```  
The result should resemble something like:  
```nuget.exe push -Source "Rocscience_Feed" -ApiKey az rsmessages.1.0.0.nupkg```

# Contribute
make change to .py file
build and install using steps above. You probably want to do this in a virtual environment 
select the python interpreter you used to install the package
run a <sampleScript>.py which imports and tests the library.
