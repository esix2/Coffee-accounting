import os
import time
import datetime
import pandas as pd
import numpy as np
from splitDate import splitDate
def UpdatePrices(Date,current_drinks,guarantee):
        pwd = os.getcwd()
 Coff_price, Esp_price, Milk_price = StockPrices(Date) 
        os.chdir("../../../../python")
        df = pd.read_csv('ingredients')
        os.chdir(pwd)
        b = np.divide(1,4500.) ## wight (kg) of one ml in the coffee machine
        SchaumSec = 5 ## Volum of 1 second Milchschaum
        MilchSec = 7 ## Volum of 1 second Milch
        drinks = df['Drink'].values
 df.index = drinks
 df = df.drop(list(set(drinks)-set(current_drinks)))
 numDrinks = len(current_drinks)
 df.index = range(numDrinks)
        DrinksPrices = np.empty((1,numDrinks))
        DrinksPrices[:] = 0
        for idx in range(numDrinks):
                tmp = Coff_price*b*df.loc[idx,'Coffee(ml)']+ Esp_price*b*df.loc[idx,'Espresso(ml)']+ Milk_price*(SchaumSec*df.loc[idx,'Milchschaum(sec)']+MilchSec*df.loc[idx,'Milch(sec)'])/1000
                DrinksPrices[0][idx] = np.ceil(100*tmp*(1+guarantee/100.))
 return DrinksPrices 

def StockPrices(Date):
        pwd = os.getcwd()
        os.chdir("../..") ## it changes to the parent folder, since shopping list is there
        csvFile = 'ShoppingList'
# if float(sum(1 for line in open(csvFile))) >= 1:
# if os.path.isfile(csvFile):
 df = pd.read_csv(csvFile) 
 Commodity = df['Commodity']
 Milk = df[Commodity == 'Milk']
 Coff = df[Commodity == 'Coffee']
 Esp = df[Commodity == 'Espresso']
# else:   ## There is no shopping in the new year, the prices must borrowed from last year
 year = int(time.strftime("%Y"))
 os.chdir("../")
 parent = os.getcwd()
 os.chdir(pwd)
 try:
     df_lastYear = pd.read_csv(parent+"/data/Year_"+str(year-1)+"/"+csvFile)
 except:
     pass

 if float(len(Milk)) == 0:
     if 'df_lastYear' in locals():
      Commodity = df_lastYear['Commodity']
      Milk = df_lastYear[Commodity == 'Milk']
      Milk.index = range(0,len(Milk))
      idx = len(Milk)-1
      Milk_price = Milk.loc[idx,'Total price'] / Milk.loc[idx,'Quantity']
     else:
      Milk_price = 0
 else:
  Milk.index = range(0,len(Milk))
  date_col = list(Milk['Date'].values)
  idx = max(SortDate_of_Shopping(date_col,Date)-1,0)
  Milk_price = Milk.loc[idx,'Total price'] / Milk.loc[idx,'Quantity']



 if float(len(Esp)) == 0:
     if 'df_lastYear' in locals():
      Commodity = df_lastYear['Commodity']
      Esp = df_lastYear[Commodity == 'Espresso']
      Esp.index = range(0,len(Esp))
      idx = len(Esp)-1
      Esp_price = Esp.loc[idx,'Total price'] / Esp.loc[idx,'Quantity']
     else:
      Esp_price = 0
 else:
  Esp.index = range(0,len(Esp))
  date_col = list(Esp['Date'].values)
  idx = max(SortDate_of_Shopping(date_col,Date)-1,0)
  Esp_price = Esp.loc[idx,'Total price'] / Esp.loc[idx,'Quantity']


 if float(len(Coff)) == 0:
     if 'df_lastYear' in locals():
      Commodity = df_lastYear['Commodity']
      Coff = df_lastYear[Commodity == 'Coffee']
      Coff.index = range(0,len(Coff))
      idx = len(Coff)-1
      Coff_price = Coff.loc[idx,'Total price'] / Coff.loc[idx,'Quantity']
     else:
      Coff_price = 0
 else:
  Coff.index = range(0,len(Coff))
  date_col = list(Coff['Date'].values)
  idx = max(SortDate_of_Shopping(date_col,Date)-1,0)
  Coff_price = Coff.loc[idx,'Total price'] / Coff.loc[idx,'Quantity']
 return Coff_price, Esp_price, Milk_price

def SortDate_of_Shopping(dates,Date):
 dates.extend([Date])
#        dates.sort(key=splitDate,reverse=False)
#        dates.sort(key=sorting)
 sorted(dates, key=lambda x: datetime.datetime.strptime(x, '%d.%m.%Y'))
        return dates.index(Date)
 
