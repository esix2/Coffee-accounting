import numpy as np
import sys
import pandas as pd
import time
import os
import shutil
from handleVersion import handleVersion
def UpdateShoppingList():
 os.system("clear")
        print "You are about to add shopping items!"
        pwd = os.getcwd()
 os.chdir("../..") ## it changes to the parent folder, since shopping list is there
 csvFile = 'ShoppingList'
 xlsFile = csvFile+'.xlsx'
 Header = ['Commodity','Type','Receipt','Quantity','Price per item','Tip','Total price','Date','Version','Remarks']
 for i in range(len(pwd)-1,1,-1):
  if pwd[i] == 'V':
   break
 Version = pwd[i+1]
 wish = 'yes'
 while wish == 'yes':
  df_tmp = getNewShoppingItem(Header,Version)
  if os.path.isfile(csvFile):  ### checks if in the current year any shpooing has been done ot this is the first time
   df = pd.read_csv(csvFile)
   df = df.append(df_tmp, ignore_index=True)
  else:
   df = df_tmp 
  df.to_csv(csvFile,index=False)
  key = raw_input("Do you like to add more items? [y/N] ")
  os.system('clear')
  if key == 'y' or key == 'Y':
   pass
  else:
   wish = 'no'
 os.chdir(pwd)
# ShoppingList_to_excel()
def getNewShoppingItem(Header,Version):
 Index = [0]
 Today =  time.strftime("%d.%m.%Y")
 df_tmp = np.empty((1, len(Header)))
 df_tmp[:] = np.nan
 df_tmp = pd.DataFrame(df_tmp,index=Index,columns=Header)
 for info in Header:
#  os.system('clear')
  if info == 'Commodity':
   print "Commodity: [1/2/3]?"
   print "\t1) Coffee"
   print "\t2) Espresso"
   print "\t3) Milk"
   key = int(raw_input())
   if key == 1:
    df_tmp.loc[Index,info] = 'Coffee'
    tst = 'no-Milk'
   elif key == 2:
    df_tmp.loc[Index,info] = 'Espresso'
    tst = 'no-Milk'
   elif key == 3:
    df_tmp.loc[Index,info] = 'Milk'
    tst = 'Milk'
  elif info == 'Type':
   print "Type (barnd):"
   print "\t1) Tchibo Caffe Crema Vollmu"
   print "\t2) Tchibo Espresso Mailande" 
   print "\t3) Schrimer Cafe Creme Bohne" 
   print "\t4) H-Milch" 
   print "\t5) or else?"
   key = raw_input()
   if key == str(1):
    df_tmp.loc[Index,info] = 'Tchibo Caffe Crema Vollmu'
   elif key == str(2):
    df_tmp.loc[Index,info] = 'Tchibo Espresso Mailander'
   elif key == str(3):
    df_tmp.loc[Index,info] = 'Schrimer Cafe Creme Bohne'
   elif key == str(4):
    df_tmp.loc[Index,info] = 'H-Mlich'
   elif key == str(5):     
    df_tmp.loc[Index,info] = raw_input("\n Please enter the entry!\n")
   else: 
    df_tmp.loc[Index,info] = key
  elif info == 'Remarks':
   print "Remarks:"
   print "\t1) Naanhof"
   print "\t2) Paid to Conni"
   print "\t3) No comment"
#   print "\t4) or insert accordingly?"
   key = raw_input()
   if key == str(1):
    df_tmp.loc[Index,info] = 'Naanhof'
   elif key == str(2):
    df_tmp.loc[Index,info] = 'Paid to Conni'
   else: 
    df_tmp.loc[Index,info] = np.nan

  elif info == 'Total price':
   df_tmp.loc[Index,info] = float(df_tmp.loc[Index,'Quantity']) * float(df_tmp.loc[Index,'Price per item'])+float(df_tmp.loc[Index,'Tip'])
  elif info == 'Price per item':
   if tst == 'Milk':
    print("Enter the price of each box of milk ("+u"\u00A2"+"): ")
    MilkUnitPrice = float(raw_input())/100
    print("Enter the delivery costs ("+u"\u20AC"+"): ")
    try:
        MilkDelivery = float(raw_input())
    except:
        MilkDelivery = 0
    df_tmp.loc[Index,info]  = float(MilkUnitPrice+MilkDelivery/float(df_tmp.loc[Index,'Quantity']))
   else:
    print info+" ("+u"\u20AC"+"): "
    key = raw_input()
    df_tmp.loc[Index,info] = key
  elif info == 'Date':
   key = raw_input("The date of shopping is today [Y/n]? ")
   if key == 'n' or key == 'N':
    Date = raw_input("Please insert the correct date (dd.mm.yyyy): ")
   else:
    Date = Today
   df_tmp.loc[Index,info] = Date
  elif info == 'Tip':
   print info+" ("+u"\u20AC"+"): "
   key = raw_input()
   try:
    df_tmp.loc[Index,info] = float(key)
   except:
    df_tmp.loc[Index,info] = 0
  elif info == 'Version':
   df_tmp.loc[Index,info] = Version 
  else:
   key = raw_input(info+": ")
   try:
    df_tmp.loc[Index,info] = key
   except:
    pass
 return df_tmp
