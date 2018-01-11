##### coding: utf-8
import os
import time
import pandas as pd
from personBalance import personBalance
from GetMoney import GetMoneyKernel
from SystemState import SystemState
from mailSend import mailSend as snd
from Report import CreatePersonReport
def RemoveMember():
        os.system("clear")
        print "You are about to remove member(s)!"
	wish = 'y'
        df = pd.read_csv('PeopleList')
	names= df['Name']
        while wish == 'y':
		print "Which member must be removed from the list?"
		for idx in range(len(names)):
			print str(idx+1)+") "+names[idx]
		key = raw_input("Please choose a number! ")
		try:
			key = int(key)
			Quitter = names[key-1]
		except:
			key1 = raw_input("The choice was invalid. Do you want to abort? [y/N]")
			if key1 == 'y' or key1 == 'Y':
				wish = 'n'
				break
		if (len(names[names == Quitter])) == 0:
			print "This guy does not exist any how"
		else:
			os.system("clear")
			key3 = raw_input("Are you sure that "+Quitter+" wants to quit [Y/n]? ")
			if key3 == 'n' or key3 == 'N':
				pass
			else:
				names =  names[names != Quitter]
				names.index = range(len(names))
				TerminateMember(Quitter)
                os.system("clear")
                key = raw_input("Is there anybody else to be removed? [y/N] ")
                if key == 'y' or key == 'Y':
			os.system("clear")
                else:
                        wish = 'no'
	df_tmp = pd.read_csv('PeopleList')
	df_tmp.index = df_tmp['Name']
	df = df_tmp.loc[names] 
	df['Last Termination'] = df['Balance']
	df = df.sort_values('Name')
	df.to_csv("PeopleList_tmp",index=False,header=True)

        df_tmp = pd.read_csv('PeoplePayment')
	df_tmp.index = df_tmp['Name']
	df = df_tmp.loc[names] 
	df.sort_values("Name")
	df.to_csv("PeoplePayment_tmp",index=False,header=True)
#	SystemState('no')
def TerminateMember(Person):
        Today =  time.strftime("%d.%m.%Y")
	Money = personBalance(Person)
	os.system("clear")
	if Money > 0:
		print (Person+" should receive "+str(Money)+u"\u20AC"+" upon termination.")
		in_msg = "You should have received "+str(Money)+ "€ upon termination. If so, your membership is successfully terminated"
		raw_input("Please press any key!")
	elif Money == 0:
		print ("Balance of "+Person+" is currently "+str(Money)+u"\u20AC"+". Termination is successful.")
		in_msg = "Your balance at the time of termination was exactly 0€"
		raw_input("Please press any key!")
	else:
		print ("Balance of "+Person+" is currently "+str(Money)+u"\u20AC"+". S(he) needs to pay "+str(abs(Money))+u"\u20AC"+ " before temination.")
		in_msg = "Your balance at the time of termination was "+str(Money)+ "€. Your membership has ended after you paid  "+str(-Money)+"€"
		raw_input("Please press any key!")
	Money = -Money
        GetMoneyKernel(Person,Money, Today)
	SystemState('no')
	EmailUponiTermination(Person,in_msg)
def EmailUponiTermination(person,in_msg):
		df = pd.read_csv('PeopleList')
		df = df[df['Name'] == person]
		recipient = str(df['Email'].values)
		recipient = str(recipient[2:len(recipient)-2])
		subj = "Coffee (Termination)"
		msg = "Dear Colleague "+person+",\n\nIt was good to have you as a member of our coffee team. "
		msg = msg + "We wish you all the best in future.\n"
		msg = msg+in_msg
		files = "../../../../src/Sheriff_of_Nottingham.pdf"
		reportFile = '../../../../src/tmp/'+person+'_report.pdf'
		CreatePersonReport(person)
		if os.path.isfile(reportFile):
				files = [reportFile,files]
				msg = msg + ".\nFor detailed information on your account, please find the attachment"
		msg = msg + ".\n\n"
		msg = msg + "PS: This message is sent automatically and privately to you. :-)\n\nSincerely Yours,\nYour Coffee Team"
		snd(recipient,subj, msg,files)
		print (person +" was informed via email.\n")
		raw_input("Press any key! ")

