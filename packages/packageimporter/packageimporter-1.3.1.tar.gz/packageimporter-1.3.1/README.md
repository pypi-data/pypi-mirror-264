# About
## PackageImporter is a simple project for importing projects according to different types (DataScience, Plotting, etc.). It can also be used to install packages and inspect installed packages.
# Installation
## To install PackageImporter, run this command into your terminal (Use Windows Powershell because I love it):
### pip install packageimporter
## For a specific version, run:
### pip install packageimporter=={version}
## To upgrade the exsisting PackageImporter module (which you probably don't):
### pip install --upgrade packageimporter
## note: you can either use python -m pip or py -m pip if it's different. (It may) PackageImporter has only one limitation: Python>=3.6 (Because there are f-strings)

# Usage Example
## from packageimporter import Importer
## Importer.stable.Plotter.plotly.express(alias="i_love_plotly_express")
### This will import plotly.express as i_love_plotly_express (weird alias) and raise an ModuleNotFoundError if plotly.express is not globally installed.

# Update Notes:
## All pip-related modules now use subprocess. Some in 1.3.0 use pip, now they've been converted to subprocess
## Minor bugfixes
## More comments will be added in PackageImporter v1.3.2, currently scheduled May 19th, 2024
## Although PackageImporter v1.3.1 still supports Python 3.6 and 3.7, it'll raise a FutureWarning. (In PackageImporter v1.4.0, we will not support Python 3.6 and 3.7 anymore. So the 1.3.x branch will probably be a LTS for users who LOVE python 3.6 and 3.7)
## Clearer structure for the class Pip
## IMPORTANT NOTE: This, and future 1.3.x releases will not be released to Github because I'm too lazy...(huh)


# Thanks to all,
# JVSCode Development Team