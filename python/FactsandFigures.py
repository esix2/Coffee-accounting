import numpy as np
import sys
import pandas as pd
import os
from inventoryUpdate import inventoryUpdate 
from lastBenefit import lastBenefit
def FactsandFigures(ifInventory):
	DataHeader = ['Last Version Benefit','Total Income','Current Cash', 'System Expenditure','Inventory Value','Members Credit','System Balance','Security']
	FileName = 'FactsandFigures'

	if os.path.isfile(FileName):
		df = pd.read_csv(FileName)
	else:
		tmp = np.empty((1,len(DataHeader)))
		tmp[:] = 0
		df = pd.DataFrame(tmp, columns=DataHeader,index=[0])

	df['Last Version Benefit'] = lastBenefit()

	tmp_df = pd.read_csv('PeoplePayment') 
	payment = tmp_df['Sum']
	df['Total Income'] = sum(payment)

        pwd = os.getcwd()
        parent = os.path.dirname(pwd) 
	CurrentVersion = int(str(parent[len(parent)-1]))
        os.chdir("../..")
        if float(sum(1 for line in open('ShoppingList'))) >= 2:
		tmp_df = pd.read_csv('ShoppingList') 
		version_col = tmp_df['Version']
		tmp_df = tmp_df[version_col  == CurrentVersion]
		expenditure = tmp_df['Total price']
		df['System Expenditure'] = sum(expenditure)
	else:
		df['System Expenditure'] = 0
        os.chdir(pwd)

	df['Current Cash'] = df['Total Income']-df['System Expenditure']+df['Last Version Benefit']

	if ifInventory=='yes':
		dummy, invenValue = inventoryUpdate()
	else:
		invenValue = df['Inventory Value']
	df['Inventory Value'] = invenValue
	if os.path.isfile('PeopleBalance'):
					tmp_df = pd.read_csv('PeopleBalance') 
					balance = tmp_df['Balance']
					df['Members Credit'] = sum(balance)
					df['System Balance'] = df['Current Cash']+df['Inventory Value']-df['Members Credit']
					if df.loc[0,'System Balance'] < 0:
						df['Security'] = 20
					else:
						df['Security'] = 10
	else:
					df['Security'] = 0
					df['Members Credit'] = 0
					df['System Balance'] = 0
					os.chdir(pwd)
	df.to_csv(FileName,index=False,header=DataHeader)
	df = pd.read_csv(FileName)
	systemState = df
	return systemState
