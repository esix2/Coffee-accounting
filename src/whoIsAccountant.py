import pandas as pd
import os
import getpass
import getent
from mailSend import mailSend as snd
def whoIsAccountant():
				pwd = os.getcwd
				FileName = 'accountant_info'
				username = getpass.getuser()
				MyName = getent.passwd(username).gecos[0:len(getent.passwd(username).gecos)-3]
				if os.path.isfile(FileName):
								df = pd.read_csv(FileName)
								accountantName = str(df.loc[0,'Name'])
								accountantEmail = str(df.loc[0,'Email'])
								if accountantName != MyName:
#												print("The accountant info is wrong!")
												print("Accountant name: "+accountantName)
												print("Accountant email: "+accountantEmail)
												key = raw_input("Do you want to change it [y/N]? ")
												if key == 'y' or key == 'Y':
																getAccountantInfo()
				else:
								print("The accountant info is missing!")
								getAccountantInfo()

def getAccountantInfo():
				Name = raw_input("Please insert the name of the accountant: ")
				Email = raw_input("Please insert the email of the accountant: ")
				email_wrong = True
				subj = "Accountant updated"
				while email_wrong:
								msg = "The name of account: "+Name+"\n"
								msg = msg + "The Email of account: "+Email+"\n\n\n"
								msg = msg + "If this is wrong. Do it again."
								try:
												snd(Email,subj,msg,[])
												email_wrong = False
								except:
												os.system("clear")
												Email = raw_input("The email was invalid! Please a valid one: ")
				os.system("echo \"Name,Email\" > accountant_info")
				os.system("echo \""+Name+","+Email+"\" >> accountant_info")
