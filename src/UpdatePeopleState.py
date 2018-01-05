import numpy as np
import sys
import pandas as pd
import os
import datetime 
from fnmatch import fnmatch
from splitDate import splitDate
from ObligorReminder import ObligorReminder
def UpdatePeopleState(ifEmail):
	PeopleExpenditure()
	PeopleAccount()
        if ifEmail == 'yes':
		key = raw_input("Shall people with negative balance be informed via email [y/N]? ")
		if key == 'y' or key == 'Y':
			ObligorReminder()

def PeopleExpenditure():
	df = pd.read_csv('PeopleList')
#	os.system("rm *~")
#	os.system("clear")
	names= df['Name'].values
	Dates = FindcsvMarks()
	tmp = np.empty((len(names),len(Dates)))
	tmp[:] = 0 
	df = pd.DataFrame(tmp,index=names,columns=Dates) 
	for d in Dates:
		df_tmp = pd.read_csv('Marks_'+ d)
		df_tmp = df_tmp.loc[0:len(df_tmp)-2]
		name_tmp = df_tmp['Name'].values
		df_tmp = df_tmp['Total (euros)'].values
		df.loc[name_tmp,d] = df_tmp
	df['Name'] = names
	df = df[['Name']+Dates] 
	df.to_csv('PeopleExpenditure',header=True,index=False)
	if len(Dates) == 0:
		CreatePeopleExpenditure()

def PeopleAccount():
	df = pd.read_csv('PeopleList')
	num_members = len(df)
	if num_members >0:
					if os.path.isfile('PeoplePayment'):
						pass
					else:
						CreatePeoplePayment()
					df = pd.read_csv('PeoplePayment')
					paid = df['Sum']
					df = pd.read_csv('PeopleExpenditure')
				#	nam = df['Name']
					Dates = FindcsvMarks()
					Header = np.hstack(('Name','Paid', Dates,'Balance'))
					tmp = np.empty((len(df),1))
					tmp[:] = 0 
				
					df['Paid'] = paid
					df['Balance'] = tmp
					df = df[Header]
				
				
					df['Balance'] = df['Paid']-df[Dates].sum(axis=1)
					df.to_csv('PeopleBalance',header=True,index=False)
				
				
					tmp_balance = df['Balance'] 
					df = pd.read_csv('PeopleList')
					df['Balance'] = tmp_balance
					df.to_csv('PeopleList',header=True,index=False)



def FindcsvMarks():
        pwd = os.getcwd()
	Files  = filter(lambda x: fnmatch(x,'Marks_*'),os.listdir(pwd))
	for idx in range(len(Files)):
		f = Files[idx]
		Files[idx] = f.split('_',1).pop() 
		pass 
	Files.sort(key=splitDate,reverse=True)
	Dates = Files
	return Dates

def CreatePeopleExpenditure():
	df = pd.read_csv('PeopleList')
	names= df['Name'].values
	Dates = ['00.00.0000']
	tmp = np.empty((len(names),len(Dates)))
	tmp[:] = 0 
	df = pd.DataFrame(tmp,index=names,columns=Dates) 
	df['Name'] = names
	df = df[['Name']+Dates] 
	df.to_csv('PeopleExpenditure',header=True,index=False)
def CreatePeoplePayment():
        df = pd.read_csv('PeopleList')
        lastTerm= df['Last Termination']
        names= list(df['Name'].values)
        tmp = np.empty((len(names),5))
        tmp[:] = np.nan
        df = pd.DataFrame(tmp,index=range(0,len(names)),columns=['Name','Last Termination', 'Sum', 0 ,1])
        df['Name'] = names
        df['Last Termination'] = lastTerm
        df['Sum'] = lastTerm
        df.to_csv('PeoplePayment',index=False,header=True)
   
