##### coding: utf-8
import sys
import pandas as pd
import os
from mailSend import mailSend as snd
from Report import CreatePersonReport
def ObligorReminder():
 df = pd.read_csv('PeopleList')
 df = df[df['Name'] != 'Rudolf Mathar']
 names = df['Name']
 emails = df['Email']
 balance = df['Balance']
 obligor_set = names[balance < 0]
 subj = "Coffee (Please Recharge)"
 for obligor in obligor_set:
  recipient = emails[names == obligor]
  credit = str(float(balance[names == obligor].values))
  tmp = str(recipient.values)
  recipient = str(tmp[2:len(tmp)-2])
  msg = "Dear Colleague "+obligor+", \n\n\nYour current balance for the coffee system is "+credit+"€. You are kindly requested to recharge your account. Please find the attachment"
  files = '../../../../python/Sheriff_of_Nottingham.pdf'
  reportFile = '../../../../python/tmp/'+obligor+'_report.pdf'
  CreatePersonReport(obligor)
  if os.path.isfile(reportFile):
    files = [reportFile,files]
    msg = msg + " for detailed information on your account"
  msg = msg + ".\n\n"
  msg = msg + "PS: This message is sent automatically and privately to you. :-)\n\nSincerely Yours,\nYour Coffee Team"
  snd(recipient,subj, msg,files)
  print (obligor +" was informed via email.\n")
 raw_input("Press any key! ")
