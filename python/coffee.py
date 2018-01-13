#!/usr/bin/python
import sys 
import os
import signal
import shutil
from CreatePeopleList import CreatePeopleList
from handleVersion  import handleVersion
from RemoveMember import RemoveMember
from AddNewMember import AddNewMember
from CountMarks import CountMarks 
from GetMoney import GetMoney
from UpdateShoppingList import UpdateShoppingList
from SystemState import SystemState
from ObligorReminder import ObligorReminder
from Report import SendReport
from initialize import initialize
from whoIsAccountant import whoIsAccountant 
from whoIsAccountant import getAccountantInfo


# callback function handler for SIGINT
def signal_handler(signal, frame):
	print('You pressed Ctrl+C!')
	sys.exit(0)

def main():
#	NewVersion, OldVersion, versionKey = handleVersion(False)
	pwd = os.getcwd()
	wish = 'y'
#	key = raw_input("Are you sure that new version is not required [y/N]? ")
	initialize()
	whoIsAccountant()
	os.system("clear")
	old_versionKey = False
	ListBottomKey = True ##### If True, adds the list of drink one more time at the bottom of the list
	while wish == 'y':
		print "Choose a task to be done: [1-10], or press Enter to quit!"
		print "\t 1) Add a member"
		print "\t 2) Remove a member"
		print "\t 3) Count the marks"
		print "\t 4) Get money"
		print "\t 5) Shopping update"
		print "\t 6) Report for individuals"
		print "\t 7) Regular update"
		print "\t 8) Notify the obligors by Email"
		print "\t 9) Update the marks' list"
		print "\t10) Update the accountant info"

		key = raw_input()
		try:
						key = int(key)
		except:
						key =  100
		os.system("clear")
		if key == 1 or key == 2:
			if old_versionKey == False:
				versionKey = True
			else:
				versionKey = False
		else:
				versionKey = False
		if key == 1:
			NewVersion, OldVersion, versionKey = handleVersion(versionKey)
			if versionKey:
				os.chdir(OldVersion+"/csv")
				SystemState('no')
				if OldVersion != NewVersion:
								shutil.copy(OldVersion+'/csv/PeopleList',NewVersion+'/csv/')
			os.chdir(NewVersion+"/csv")
			AddNewMember()
			SystemState('no')
			CreatePeopleList(ListBottomKey)
			old_versionKey = True
			versionKey = False
		elif key == 2:
			NewVersion, OldVersion, versionKey = handleVersion(versionKey)
			os.chdir(OldVersion+"/csv")
			RemoveMember()
			if OldVersion != NewVersion:
							os.rename(OldVersion+'/csv/PeopleList_tmp',NewVersion+'/csv/PeopleList')
							if versionKey:
								os.remove(OldVersion+'/csv/PeoplePayment_tmp')
							else:
								os.rename(OldVersion+'/csv/PeoplePayment_tmp',NewVersion+'/csv/PeoplePayment')
			os.chdir(NewVersion+"/csv")
			CreatePeopleList(ListBottomKey)
			#SystemState('no')
			old_versionKey = True
			versionKey = False
		else:
			NewVersion, OldVersion, versionKey = handleVersion(False)
#			old_versionKey = versionKey
			os.chdir(NewVersion+"/csv")
			if key == 3:
				CountMarks()
				SystemState('no')
			elif key == 4:
				GetMoney()
			elif key == 5:
				UpdateShoppingList()
			elif key == 6:
				#print "This function is not embedded yet!"
				SendReport()
				#input("test")
			elif key == 7:
				SystemState('yes')
			elif key == 8:
				key_email = raw_input("Shall people with negative balance be informed via email [y/N]? ")
				if key_email == 'y' or key_email == 'Y':
					ObligorReminder()
			elif key == 9:
				CreatePeopleList(ListBottomKey)
				os.system("clear")
			elif key == 10:
				getAccountantInfo()
				os.system("clear")
			else:
				print('here')
				os.system("clear")

		os.chdir(pwd)
		key_update = key
		os.system("clear")

                key = raw_input("Is there any other task? [y/N]? ")
                os.system("clear")
                if key == 'y' or key == 'Y':
                        pass
                else:
			wish = 'no'
                        if key_update != 8:
				NewVersion, OldVersion, versionKey = handleVersion(False)
				os.chdir(NewVersion+"/csv")
				SystemState('no')
				os.chdir(pwd)

if __name__ == "__main__":
   # register signal handler for SIGINT / CTRL + c
    signal.signal(signal.SIGINT, signal_handler)
    os.system("clear")
    print("This program needs to close all your Libreoffice open documents! Otherwise, some of the xlsx files will not be updated!")
    key = raw_input("Do you want to close them? [Y/n] ")
    if key == 'n' or key == 'N':
        pass
    else:
        os.system("killall soffice.bin")
    main()
    os.system("clear")
