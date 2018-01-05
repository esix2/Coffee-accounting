import numpy as np
import sys
import pandas as pd
import time
import os
import shutil
import openpyxl as px
from openpyxl import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.styles import Color, Fill, Border, Alignment, Protection, Font
from openpyxl.cell import get_column_letter
from openpyxl.cell import Cell
from UpdatePrices import UpdatePrices

def CountMarks():
	os.system("clear")
	Today =  time.strftime("%d.%m.%Y")
        pwd = os.getcwd()
        if os.path.isdir("../Marks"):  ### checks if any Mark has been counted already or not
                pass
        else:
                os.makedirs("../Marks")

	key = raw_input("You are about to count the marks. The date of desire is today [Y/n]? ")
	if key == 'n' or key == 'N':
		Date = raw_input("Please insert the date (dd.mm.yyyy): ")
	else:
		Date = Today
	#	Date = '28.09.2016'
	os.system("clear")
	xlsFile = "../Marks/"+Date+'.xlsx'
	csvFile = "Marks_"+ Date
	df_PeopleList = pd.read_csv('PeopleList')
	People = df_PeopleList['Name'].values
#	People = ['Alireza Zamani', 'Ehsan Zandi']
	People.sort()
	NumberofPeople = len(People)
	os.system("clear")
	if os.path.isfile(csvFile):
		df = pd.read_csv(csvFile,index_col=0)
		Drinks = df.columns
		Drinks = Drinks[:len(Drinks)-1]
		##################################################
		##################################################
		key = raw_input("Do you wish to correct some entries? [Y/n]? ")
		if key == 'n' or key == 'N':
			wish = 'n'
		else:
			wish = 'y'
		os.system("clear")
		key = raw_input("Is the guarantee percent 10 [Y/n]? ")
		os.system("clear")
		if key == 'n' or key == 'N':
			guarantee = int(raw_input("Please insert the gurantee percent: "))
		else:
			guarantee = 10 ### in percent
		prices = UpdatePrices(Date,Drinks,guarantee)
		while wish == 'y':
			names= list(People) 
			print "Which one of the following people do you want to correct?"
			for idx in range(NumberofPeople):
				print str(idx+1)+") "+names[idx]
			print ("\n\n\n\n")
			key = int(raw_input("Please choose a number!\n"))
			os.system("clear")
			try:
				Person = names[key-1]
				getPersonMarks(Person,Drinks,df)
			except:
				key1 = raw_input("The choice was invalid. Do you want to abort? [y/N]")
				if key1 == 'y' or key1 == 'Y':
					wish = 'n'
					break
			key = raw_input("Is there anyone else else to be corrected? [y/N] ")
			os.system("clear")
			if key == 'y' or key == 'Y':
				pass
			else:
				wish = 'no'
		##################################################
		##################################################
	else:
		os.chdir("../../../src")
		df_drink = pd.read_csv('CoffeeList',sep='\t')
		os.chdir(pwd)
		Drinks = df_drink['Drink']
		NumberofDrinks = len(Drinks)
		key = raw_input("Is the guarantee percent 10 [Y/n]? ")
		if key == 'n' or key == 'N':
			guarantee = int(raw_input("Please insert the gurantee percent: "))
		else:
			guarantee = 10 ### in percent
		prices = UpdatePrices(Date,Drinks,guarantee)
		Header = np.hstack(('Name',Drinks))
		cups = np.empty((NumberofPeople, NumberofDrinks))
		cups[:] = 0
		df = pd.DataFrame(cups,index=People,columns=Drinks)
		for name in People:
			getPersonMarks(name,Drinks,df)
		Prices = pd.DataFrame(prices,columns=Drinks,index=[len(People)+1])
		Prices['Name'] = 'Price (cents)'
		Prices = Prices[Header]

		df['Name'] = People
		df = df[Header]
		df.index  = range(1,len(df)+1)
		df = df.append(Prices,ignore_index=False)
		df.to_csv(csvFile,header=True,index=False)
		df = pd.read_csv(csvFile,index_col=0)

	New_col = np.empty((1+NumberofPeople,1))
	New_col[:] = np.nan
	idx_i = 0
	for name in People:
		tmp = 0
		idx_j = 0
		for drink in Drinks:
			tmp = df.loc[name,drink]*prices[0][idx_j] + tmp
			idx_j += 1
		New_col[idx_i][0] = tmp/100.
		idx_i += 1

	df["Total (euros)"] = New_col
	df.loc['Price (cents)','Kaffee':'Milch (250ml)'] = prices

	df.to_csv(csvFile,header=True,index=True)

def getPersonMarks(name,Drinks,df):
		os.system('clear')
		NumberofDrinks = len(Drinks)
		key1 = raw_input("Do you like to skipe " + name+" [y/N]? ")
		os.system('clear')
		if key1 == 'y' or key1 == 'Y':
			pass
		else:
			if name == 'FFTI':
				st_cups = np.empty((1, NumberofDrinks))
				st_cups[:] = 0
				student_tmp = pd.DataFrame(st_cups,index=['0'],columns=Drinks)
				gu_cups = np.empty((1, NumberofDrinks))
				gu_cups[:] = 0
				guest_tmp = pd.DataFrame(gu_cups,index=['0'],columns=Drinks)
				print 'Student Assistants'
				for drink in Drinks:
					if key1 == 'y' or key1 == 'Y':
						break 
					else:
						key = raw_input("\t"+drink+": ")
						try:
							student_tmp.loc['0',drink] = int(key)
						except :
							if key == "s":
								student_tmp.loc['0',drink] = 0
								break
							else:
								student_tmp.loc['0',drink] = 0
				print 'Guests' 
				for drink in Drinks:
					if key1 == 'y' or key1 == 'Y':
						break 
					else:
						key = raw_input("\t"+drink+": ")
						try:
							 guest_tmp.loc['0',drink] = int(key) 
						except :
							if key == "s":
								guest_tmp.loc['0',drink] = 0
								break
							else:
								guest_tmp.loc['0',drink] = 0

				for drink in Drinks:
						
					df.loc[name,drink] = guest_tmp.loc['0',drink] +  student_tmp.loc['0',drink]
#				input("something")

			else:
				print "You can skip at any point by insrting s+break!"
				print name
				for drink in Drinks:
					if key1 == 'y' or key1 == 'Y':
						break 
					else:
						key = raw_input("\t"+drink+": ")
						try:
							df.loc[name,drink] = int(key)
						except :
							if key == "s":
								df.loc[name,drink] = 0
								break
							else:
								df.loc[name,drink] = 0
		return df
