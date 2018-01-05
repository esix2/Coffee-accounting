##### coding: utf-8
import os
import time
import pandas as pd
from GetMoney import GetMoneyKernel
from mailSend import mailSend as snd
def AddNewMember():
	os.system("clear")
	Today =  time.strftime("%d.%m.%Y")
	wish = 'y'
	print "You are about to add a new person!"
	df = pd.read_csv('PeopleList')
	df['Last Termination'] = df['Balance']
	while wish == 'y':
		names= df['Name']
		NewPerson = raw_input("Please, insert the name you wish to be added: ")
		if (len(df[names == NewPerson])) > 0:
			print NewPerson+" already is in the system!"
			key = raw_input("\tWould you like to skip this? [Y/n] ")
			if key == 'n' or key == 'N':
				NewPerson = raw_input("Then, insert the name once more: ")
				email = raw_input("Insert the email address of this person: ")
				FirstMoney = raw_input("Now, insert the start money to go: ")
				try:
					FirstMoney = float(FirstMoney)
				except:
					FirstMoney = 0 
				#NewRow = pd.DataFrame([[NewPerson, FirstMoney, 0]], columns=['Name','Balance','Last Termination'])
				NewRow = pd.DataFrame([[NewPerson, 0, 0,email]], columns=['Name','Balance','Last Termination','Email'])
				df = df.append(NewRow)
			else:
				pass
		else:
			email = raw_input("Insert the email address of this person: ")
			FirstMoney = raw_input("Now, insert the start money to go: ")
			try:
				FirstMoney = float(FirstMoney)
			except:
				FirstMoney = 0 
			NewRow = pd.DataFrame([[NewPerson, 0, 0, email]], columns=['Name','Balance','Last Termination','Email'])
			df = df.append(NewRow)
		df = df.sort_values('Name')
		df.to_csv("PeopleList",index=False,header=True)
		#if FirstMoney > 0:
		sender = "zandi@ti.rwth-aachen.de"
		body = "Dear Colleague "+NewPerson+",\n\nWelcome to our coffee system. You have now "+str(FirstMoney)+"€ in your account. Please enjoy your coffee and do not forget to put a mark on the list (in the kitchen) each time you drink a cup.\n\n"
		body = body + "PS: This message is sent automatically and privately to you. :-)\n\nSincerely Yours,\nYour Coffee Team"
		fileName = "../../../src/Sheriff_of_Nottingham.pdf"
		subject = "Coffee (Welcome)"
		snd(email,subject,body,fileName)
		GetMoneyKernel(NewPerson,FirstMoney, Today)
		os.system("clear")
                key = raw_input("Do you like to add more people? [y/N] ")
                if key == 'y' or key == 'Y':
			pass
                else:
                        wish = 'no'

