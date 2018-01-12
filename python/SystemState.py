import sys
import os
import pandas as pd
from openpyxl.workbook import Workbook
from ShoppingList_to_excel import ShoppingList_to_excel 
from PeopleBalance_to_excel import PeopleBalance_to_excel 
from PeoplePayment_to_excel import PeoplePayment_to_excel 
from FactsandFigures_to_excel import FactsandFigures_to_excel
from FactsandFigures import FactsandFigures
from UpdatePeopleState import UpdatePeopleState
from Marks2Xls import Marks2Xls
def SystemState(inArg):
	df = pd.read_csv('PeopleList') 
	num_members = len(df)
	if num_members > 1:
				ifEmail = inArg
				ifInventory = inArg
				os.system("clear")
				Marks2Xls()
				UpdatePeopleState(ifEmail)
				FactsandFigures(ifInventory)

				xlsFile = '../Accounts.xlsx'
				wb = Workbook()
				wb.remove_sheet(wb.get_active_sheet())

				wb.add_sheet(PeoplePayment_to_excel(),index=2)
				ws1 = wb.get_sheet_by_name('Sheet1')
				ws1.title = 'Members Payment'

				wb.add_sheet(PeopleBalance_to_excel(),index=2)
				ws2 = wb.get_sheet_by_name('Sheet1')
				ws2.title = 'Members Balance'

				wb.add_sheet(ShoppingList_to_excel(),index=3)
				ws3 = wb.get_sheet_by_name('Sheet1')
				ws3.title = 'Shopping List'

				wb.add_sheet(FactsandFigures_to_excel(),index=4)
				ws4 = wb.get_sheet_by_name('Sheet1')
				ws4.title = 'System State'

				wb.save(xlsFile)
				os.system('cp '+xlsFile+' ~/.Coffee.xlsx')
