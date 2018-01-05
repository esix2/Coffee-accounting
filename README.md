# Coffee-accounting
A linux-based Python software for kitchen accounting at small companies.
The whole software is based text files. Just for easy reading .xlsx files are generated out the tex files, automatically.

## Requirements
The following softwares and packages are required. Though , it might be still possible to use different verions of other packages, which are comptible with Python 2.7

    python 2.7
    pandas   0.20.1
    openpyxl 1.8.2
    numpy    1.7.1
    keyring  10.3.2
    getent   0.2
 
Also latex including the following are rquired for report functionality

    pdflatex
    csvsimple
    
## Manual installation
    
    sudo apt-get install python2.7
    sudo apt-get install texlive
    sudo apt-get install python-pip
    sudo pip install pandas==0.20.1
    sudo pip install openpyxl==1.8.2
    sudo pip install numpy==1.7.1
    sudo pip install keyring==10.3.2
    sudo pip install getent==0.2
    
    
## Installation with 
Running the following commands in the shell terminal
    
    chmodx +x installer.sh
    ./installer
    
## How to use
After installation. Change to #installation_path/src directory. And execute the command:

    python Coffee.py

The rest is easy, you will see what options you have. Good luck. If you have any question email me under zandi@ti.rwth-aachen.de
    
