import time
import os
import pandas as pd
def lastBenefit():
##############################################################
######################## This function calculated indeed the difference between the available cash and the members' credit
##############################################################
##############################################################
 pwd = os.getcwd()
 if pwd  == '/home/zandi/Documents/Kitchen/data/Year_2015/V2/csv':
  benefit = -18.91
 else:
  try:
   LastVersion = FindPreviousVersion()
   os.chdir(LastVersion+'/csv')
   FileName = 'FactsandFigures'
   df = pd.read_csv(FileName)
   benefit = df['Current Cash'] - df['Members Credit'] 
  except:
   benefit=0
 benefit = float(benefit)
 os.chdir(pwd)
 return benefit
def FindPreviousVersion():
        year = int(time.strftime("%Y"))
        pwd = os.getcwd()
        parent = os.path.dirname(pwd)
        if float(parent[len(parent)-1]) == 1:
                parent = os.path.dirname(parent)
                parent = os.path.dirname(parent)
                for version_index in range(1,1001):  ## finds the the oldest version of the last year
                        if os.path.isdir(parent+"/data/Year_"+str(year-1)+"/V"+str(version_index)):
                                PreviousVersion = parent+"/data/Year_"+str(year-1)+"/V"+str(version_index)
                        else:
                                break
        else:
                idx = parent.rfind('/')              ### Find idx of the last "/"
                PreviousVersion = parent[:idx+2] + str(int(parent[idx+2:len(parent)])-1)
        return PreviousVersion

