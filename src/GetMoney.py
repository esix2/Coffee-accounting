##### coding: utf-8
import numpy as np
import sys
import pandas as pd
import time
import os
import shutil
import openpyxl as px
from mailSend import mailSend as snd
from Report import CreatePersonReport
from openpyxl import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.styles import Color, Fill, Border, Alignment, Protection, Font
from openpyxl.cell import get_column_letter
from openpyxl.cell import Cell
#from UpdatePrices import UpdatePrices
from UpdatePeopleState import PeopleAccount
def GetMoney():
	os.system("clear")
        print "You are about to collect money from member(s)!"
	Today =  time.strftime("%d.%m.%Y")
        pwd = os.getcwd()
	wish = 'y'
	while wish == 'y':
		df = pd.read_csv('PeopleList')
		names= df['Name'].values
		names= list(names) 
		print "Which one of the following people wants to pay?"
		for idx in range(len(df)):
			print str(idx+1)+") "+names[idx]
		print ("\n\n\n\n")
		key = raw_input("Please choose a number!\n")
		os.system("clear")
		try:
			key = int(key)
			Person = names[key-1]
			print Person+": insert the money ("+u"\u20AC"+"): "
			Money = raw_input()
			#Money = raw_input("Now, insert the money ("+u"\u20AC"+"): ")
		except:
			key1 = raw_input("The choice was invalid. Do you want to abort? [y/N]")
			if key1 == 'y' or key1 == 'Y':
				wish = 'n'
				break
		keyDate = raw_input("Today is the actual date of payment [Y/n]? ")
		if keyDate == 'n' or keyDate == 'N':
			Date = raw_input("Please insert the date (dd.mm.yyyy): ")
		else:
			Date = Today
		GetMoneyKernel(Person, Money, Date)
		PeopleAccount()
		EmailUponRecharge(Person,Money)
		key = raw_input("Does anyone else to pay? [y/N] ")
		os.system("clear")
		if key == 'y' or key == 'Y':
			pass
		else:
                        wish = 'no'
def GetMoneyKernel(Person, Money, Date):
	df = pd.read_csv('PeopleList')
	lastTerm= list(df.loc[df['Name'] == Person,'Last Termination'])
	AllNames= list(df['Name'].values)
	if os.path.isfile('PeoplePayment'):
		df = pd.read_csv('PeoplePayment')
		names= list(df['Name'].values)
		try:
			names.index(Person)
		except:
                        new_row = np.empty((1,len(df.columns)))
                        new_row[:] = np.nan
                        NewRow = pd.DataFrame(new_row, columns=df.columns)
                        NewRow['Name'] = Person
                        NewRow['Last Termination'] = lastTerm
                        NewRow['Sum'] = lastTerm
                        df = df.append(NewRow,ignore_index=True)
			df = df.sort_values('Name')
			df.index = range(0,len(df))
			names= df['Name'].values
			names= list(names) 
		Person_idx = names.index(Person)
		additionalColumn = 'y'
		for idx in range(0,len(df.columns)-4,2):
			if abs(df.loc[Person_idx,str(idx)]) >= 0:
				pass
			else:
				additionalColumn = 'n'
				df.loc[Person_idx,str(idx)] = Money 
				df.loc[Person_idx,str(idx+1)] = Date
				break
		if additionalColumn == 'y':
			idx += 1
			tmp = np.empty((len(names),1))
			tmp[:] = np.nan
			df[str(idx+1)] = tmp
			df.loc[Person_idx,str(idx+1)] = Money 

			tmp = np.empty((len(names),1))
			tmp[:] = np.nan
			df[str(idx+2)] = tmp
			df.loc[Person_idx,str(idx+2)] = Date
	else:
		df = pd.read_csv('PeopleList')
		lastTerm= df['Last Termination']
		names= list(df['Name'].values)
		Person_idx = names.index(Person)
		tmp = np.empty((len(names),5))
		tmp[:] = np.nan
		df = pd.DataFrame(tmp,index=range(0,len(names)),columns=['Name','Last Termination', 'Sum', 0 ,1])
		df.loc[Person_idx,0] = Money
		df.loc[Person_idx,1] = Date
		df['Name'] = names
		df['Last Termination'] = lastTerm
		df['Sum'] = lastTerm
	df.loc[Person_idx,'Sum'] = float(Money) + df.loc[Person_idx,'Sum']
	df.to_csv('PeoplePayment',index=False,header=True)
def EmailUponRecharge(person,amount):
	df = pd.read_csv('PeopleList')
	df = df[df['Name'] == person]
	recipient = str(df['Email'].values)
	recipient = str(recipient[2:len(recipient)-2])
	credit = str(float(df['Balance'].values))
	subj = "Coffee (Recharge Successful)"
	msg = "Dear Colleague "+person+",\n\nMany thanks to you for recharging your account. Now an amount of "
	msg = msg + str(amount)+ "€ is deposited into your account.\nYour current balance is "+str(credit)+"€"
	files = "../../../src/Sheriff_of_Nottingham.pdf"
	reportFile = '../../../src/tmp/'+person+'_report.pdf'
	CreatePersonReport(person)
	if os.path.isfile(reportFile):
		files = [reportFile,files]
		msg = msg + ". For detailed information on your account, please find the attachment"
	msg = msg + ".\n\n"
	msg = msg + "PS: This message is sent automatically and privately to you. :-)\n\nSincerely Yours,\nYour Coffee Team"
	snd(recipient,subj, msg,files)
	print (person +" was informed via email.\n")
        raw_input("Press any key! ")
