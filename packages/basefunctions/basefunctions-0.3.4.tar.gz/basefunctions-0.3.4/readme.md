# Introduction 
simple library to have some commonly used functions for everyday purpose. 
The functions include some convenience functions for file handling as well 
as a threadpool class with automatic retry and timeout functionality.  

# Getting Started
There are the following functionalities in this lib:
- database - some convienience functions for sql handling
- filefunctions - some convienience functions for file handling
- threadpool - a threadpool class with message system

# Installing
pip install basefunctions

# Usage

## Using convenience file functions
import basefunctions as bf

bf.get_current_directory()
/Users/neutro2/

## Using threadpool class
see example.py file for a concrete usage of the threadpool class

# Build and Test
1. Install virtual environment 
python3 -m venv .venv
source .venv/bin/activate
pip install build
pip install twine
pip install pytest

2. Build a package:
python3 -m build

3. Run the testcases  
pip install -e .
cd tests
pytest

4. Upload the package to pypi.org
python3 -m twine upload dist/*

# Project Homepage
https://dev.azure.com/neuraldevelopment/basefunctions

# Contribute
If you find a defect or suggest a new function, please send an eMail to neutro2@outlook.de
