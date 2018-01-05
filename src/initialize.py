import os
import time
import shutil
import pandas as pd 
from SystemState import SystemState
from CreatePeopleList import CreatePeopleList
import getpass
def initialize():
				username = getpass.getuser()
				empty = True
				year = int(time.strftime("%Y"))
				origin_pwd = os.getcwd()
				pwd = os.path.dirname(origin_pwd)
				for root, dirs, files in os.walk(pwd):
								for dir in dirs:
												if dir.startswith("Year_"):
																empty=False
				if empty:
								pwd = pwd+'/Year_'+str(year)+'/V1/csv'
								os.makedirs(pwd)

								accountantEmail = username+"@ti.rwth-aachen.de"
								os.system("echo \"Name,Balance,Last Termination,Email\" > " + pwd +"/PeopleList")
								os.system("echo \"FFTI,0,0,"+accountantEmail+"\" >> " + pwd +"/PeopleList")
								
#								os.system("echo \"Name\" > " + pwd +"/PeopleExpenditure")
								
#								os.system("echo \"Name,Paid,Balance\" > " + pwd +"/PeopleBalance")

								os.system("echo \"Name,Last Termination,Sum,0,1\" > " + pwd +"/PeoplePayment")
								os.system("echo \"FFTI,0,0,,\" >> " + pwd +"/PeoplePayment")

								pwd = os.path.dirname(origin_pwd)+'/Year_'+str(year)
								os.system("echo \"Commodity,Type,Receipt,Quantity,Price per item,Tip,Total price,Date,Version,Remarks\" > " + pwd +"/ShoppingList")


