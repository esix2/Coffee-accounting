# Coffee-accounting
A linux-based Python software for kitchen accounting at small companies.
The whole software is based text files. Just for easy reading .xlsx files are generated out the tex files, automatically.

## Requirements
The following softwares and packages are required. Though , it might be still possible to use different verions of other packages, which are comptible with Python 2.7

    python 2.7
    python-setuptools
    pandas   0.20.1
    openpyxl 1.8.2
    xlsxwriter 0.9.6
    numpy    1.7.1
    keyring  10.3.2
    
Also latex including the following are rquired for report functionality

    pdflatex
    csvsimple
    
## Manual installation
Download the repo to your installation_path, then

    cd installation_path
    python2.7 -m virtualenv venv
    pip install -r requirements.txt   
    
    
## Installation with script
Running the following commands in the shell terminal
    
    ./installer
    
## How to use

first way: 
    
    cd installation_path
    source /venv/bin/activate
    cd python/
    python coffee.py
        
second way:

    cd installation_path
    ./coffee

The rest is easy, you will see what options you have. Good luck. If you have any question email me under zandi@ti.rwth-aachen.de
    
