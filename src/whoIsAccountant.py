import os
import getpass
import keyring
from mailSend import mailSend as snd
def whoIsAccountant():
				email = str(keyring.get_password("coffee","email"))
				try:
						snd(email,"test","this is a test",[])
				except:
						print("The accountant info is missing!")
						getAccountantInfo()

def getAccountantInfo():
				email_wrong = True
				subj = "Accountant updated"
				while email_wrong:
								name = str(raw_input("Please insert your complete name: "))
								keyring.set_password("coffee","name",name)

								email = str(raw_input("Please insert your email address: "))
								keyring.set_password("coffee","email",email)

								username = str(raw_input("Please insert your logging name for the mail server: "))
								keyring.set_password("coffee","username",username)

								password = str(getpass.getpass("Please insert your mail server password. It will be stored in your keyring: "))
								keyring.set_password("coffee","password",password)

								msg = "The name of accountant: "+name+"\n"
								msg = msg + "The Email of accountant: "+email+"\n\n\n"
								msg = msg + "If this is wrong. Do it again."
								try:
												snd(email,subj,msg,[])
												email_wrong = False
								except:
												os.system("clear")
												email = raw_input("Something was wrong! Please give valid entires: ")
