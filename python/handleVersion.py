import os
import time
import shutil
import pandas as pd 
from SystemState import SystemState
from CreatePeopleList import CreatePeopleList
def handleVersion(CreateVersion):
    yearChange = False
    year = int(time.strftime("%Y"))
    pwd = os.getcwd()
    pwd = os.path.dirname(pwd)
    if os.path.isdir(pwd+"/data/Year_"+str(year)):  ### Checks if the year has chaned. This means year has not changed!
        for version_index in range(1,1001): ## finds the oldest version in the current year
            if os.path.isdir(pwd+"/data/Year_"+str(year)+"/V"+str(version_index)):
                OldVersion = pwd+"/data/Year_"+str(year)+"/V"+str(version_index)
                 NewVersion = pwd+"/data/Year_"+str(year)+"/V"+str(version_index+1)
            else:
                break
    else:  ### This means year has changed!
        os.system("clear")
        key = raw_input("The year has turned into "+str(year)+"! Would you like to excute this task for "+str(year-1)+"? [y/N] ")
        if key == 'y' or key == 'Y':
            for version_index in range(1,1001): ## finds the oldest version in the current year
                if os.path.isdir(pwd+"/data/Year_"+str(year-1)+"/V"+str(version_index)):
                    OldVersion = pwd+"/data/Year_"+str(year-1)+"/V"+str(version_index)
                    NewVersion = pwd+"/data/Year_"+str(year-1)+"/V"+str(version_index+1)
                else:
                    break
        else:
            yearChange = True
            os.makedirs(pwd+"/data/Year_"+str(year))
            for version_index in range(1,1001):  ## finds the the oldest version of the last year
                if os.path.isdir(pwd+"/data/Year_"+str(year-1)+"/V"+str(version_index)):
                    OldVersion = pwd+"/data/Year_"+str(year-1)+"/V"+str(version_index)
                else:
                    break
            NewVersion = pwd+"/data/Year_"+str(year)+"/V1"
    df = pd.read_csv(OldVersion+'/csv/PeopleList') 
    num_members = len(df)
    if num_members > 1:
        if (yearChange):
            handleYearChange(pwd,NewVersion,OldVersion)
            CreateVersion = False
        elif (CreateVersion):
            os.makedirs(NewVersion+'/csv')
            shutil.copy(OldVersion+'/csv/PeopleList',NewVersion+'/csv/')
        else:
            NewVersion = OldVersion
    else:
        NewVersion = OldVersion
# print OldVersion
# raw_input(NewVersion)
    return NewVersion, OldVersion, CreateVersion
def handleYearChange(pwd,NewVersion,OldVersion):
    os.makedirs(NewVersion+'/csv')
    shutil.copy(OldVersion+'/csv/PeopleList',NewVersion+'/csv/')
    os.chdir(NewVersion+'/csv')
    df = pd.read_csv('PeopleList')
    df['Last Termination'] = df['Balance']
    df.to_csv("PeopleList",index=False,header=True)
    parent = os.path.dirname(NewVersion) 
    os.system("echo \"Commodity,Type,Receipt,Quantity,Price per item,Tip,Total price,Date,Version,Remarks\" > " + parent +"/ShoppingList")
    ListBottomKey=True
    CreatePeopleList(ListBottomKey)
    os.chdir(pwd)
