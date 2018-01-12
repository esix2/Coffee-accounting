import sys
import pandas as pd
import time
import os
from UpdatePrices import *
def inventoryUpdate():
	Today =  time.strftime("%d.%m.%Y")
	stockList = ['Coffee', 'Espresso','Milk']
	stockPrice = pd.DataFrame(list(StockPrices(Today)) ,index=stockList,columns=['Commodity'])
	packNumber = pd.DataFrame(np.zeros((1,len(stockList))),columns=stockList,index=['Commodity'])
	inventoryValue = 0
	for commodity in stockList:
		os.system("clear")
		key = raw_input (commodity+": How many packs are in the stock? ")
		correct = 'y'
		while correct == 'y':
			try:
				packNumber[commodity] = int(key)
				correct = 'n'
			except:
				os.system("clear")
				key1 = raw_input (" There is no "+ commodity + " in the stock! Is that correct [Y/n]? ")
				if key1 == 'n' or key1 == 'N':
					os.system("clear")
					key = raw_input (commodity+": Insert correct number of packs: ")
				else:
					packNumber[commodity] = 0
					correct = 'n'
		inventoryValue = packNumber[commodity]*stockPrice.loc[commodity] + inventoryValue
	os.system("clear")
	inventoryValue = inventoryValue['Commodity']
	return packNumber, inventoryValue

#	prices = pd.DataFrame(prices,columns=Drinks,index=[len(People)+1])
#	prices['Name'] = 'Price (cents)'
#	prices = prices[Header]

