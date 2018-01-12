##### coding: utf-8
import numpy as np
import sys
import pandas as pd
import os
import datetime 
import shutil
from splitDate import splitDate
from mailSend import mailSend as snd
def SendReport():
 wish = 'y'
 while wish == 'y':
  df = pd.read_csv('PeopleList')
  names= df['Name'].values
  names= list(names) 
  print "To which one of the following people do you want to send report?"
  for idx in range(len(df)):
   print str(idx+1)+") "+names[idx]
  print "00) Send to all!!!!"
  print ("\n\n\n\n")
  key = raw_input("Please choose a number!\n")
  os.system("clear")
  try:
   to_all = str(key)
   key = int(key)
   if to_all != "00":
    Person = names[key-1]
    CreateAndEmailReport(Person)
   else:
    for Person in names:
     CreateAndEmailReport(Person)
  except:
#   CreateAndEmailReport(Person)
   key1 = raw_input("The choice was invalid. Do you want to abort? [y/N]")
   if key1 == 'y' or key1 == 'Y':
    wish = 'n'
    break
  key = raw_input("Do you want to send report to anyone else? [y/N] ")
  os.system("clear")
  if key == 'y' or key == 'Y':
   pass
  else:
   wish = 'no'
def CreateAndEmailReport(Person):
 df = pd.read_csv('PeopleList')
 df = df[df['Name'] == Person]
 recipient = df['Email']
 balance = str(float(df['Balance']))
 subj = "Coffee (Personal Report)"
 tmp = str(recipient.values)
 recipient = str(tmp[2:len(tmp)-2])
 msg = "Dear Colleague "+Person+", \n\n\n"
 msg = msg + "This email includes your personal record of payments and drinking. Your current balance is "+balance+"€.\n"
 msg = msg + "For detailed information on your account, please find the attachment.\n\n"
 msg = msg + "PS: This message is sent automatically and privately to you. :-)\n\nSincerely Yours,\nYour Coffee Team"
 files = '../../../../python/Sheriff_of_Nottingham.pdf'
 reportFile = '../../../../python/tmp/'+Person+'_report.pdf'
 try:
  CreatePersonReport(Person)
 except:
  print("Report for "+Person+" failed.")
  os.system('echo "'+Person+','+str(datetime.datetime.now())[:19]+'">> report_failure.log')      
 if os.path.isfile(reportFile):
   files = [reportFile,files]
   snd(recipient,subj, msg,files)
   print (Person +" was informed via email.\n")

def CreatePersonReport(Person):
 PayHist,SumPayment = PaymentHist(Person)
 CupHist,SumExpend = DrinkHist(Person)
 Summary = pd.read_csv('PeopleBalance')
 Summary = Summary[Summary['Name']==Person]
 Balance = Summary['Balance'].astype(float).sum()
# if True:
 if SumPayment > 0 or SumExpend > 0:
   tmpBalance = SumPayment-SumExpend
   if np.abs(Balance-tmpBalance) > 1e-6:
    print('The report for '+Person+' is errorneous!')
    raw_input(str(Balance)+', '+str(SumPayment-SumExpend))
   else:
    Header = ['Name','Paid','Balance']
    Summary = Summary[Header]
    Summary['Expenditure'] = SumExpend
    Summary['Paid'] = SumPayment
    Header = ['Name','Paid','Expenditure','Balance']
    Summary = Summary[Header]
    sourceDir = '../../../../python'
    pwd = os.getcwd()
    os.chdir(sourceDir)
    if not(os.path.isdir('tmp')):
     os.mkdir('tmp')
    shutil.copy2('CreateReciept.tex','tmp')
    os.chdir('tmp')
    PayHist.to_csv('PayHist',header=True,index=False)
    CupHist.to_csv('CupHist',header=True,index=False)
    Summary.to_csv('Summary',header=True,index=False)
    os.system("pdflatex CreateReciept.tex >> Hist.log")
    os.rename('CreateReciept.pdf',Person+'_report.pdf')
    os.chdir(pwd)
    os.system('echo "'+Person+','+str(datetime.datetime.now())[:19]+'">> report_success.log')
    print("Report for "+Person+" was successful.")
  
def DrinkHist(Person):
 for root, dirs, files in os.walk("../../../"):
  for file in files:
    if (root.find('/csv') != -1) and (file.find("Marks_") != -1):
      FileName = os.path.join(root, file)
      Date = FileName[len(FileName)-10:len(FileName)]
      df = pd.read_csv(FileName)
      df.rename(columns={'Name':'Date','Milch (250ml)':'Milch','Total (euros)':'Sum'},inplace=True)
      prices = df[df['Date'] == 'Price (cents)']
      df = df[df['Date'] == Person]
      Header = ['Date','Kaffee', 'Milchkaffee', 'Cappuccino', 'Espresso','Ristretto','Macchiato', 'Milschaum', 'Milch', 'Sum']
      Version = root[14:18]+root[20:root.find('/',20)] ### Find Year+Vnumber
      if 'V_last' in locals():
       if V_last < Version:
         V_last = Version
         latest_prices = prices
      else:
       V_last = Version
       latest_prices = prices
      if df.index>=0:
        df.rename(columns={'Name': 'Date'}, inplace=True)
        prices.rename(columns={'Name': 'Date'}, inplace=True)
        if len(df.columns) == 9:
          df.loc[df.index,'Ristretto'] = 0
          prices.loc[prices.index,'Ristretto'] = 0
          df = df[Header]
          prices = prices[Header]
        df.loc[df.index,'Date'] = Date
        prices.loc[prices.index,'Date'] = Date
        if 'CupHist' in locals():
          CupHist = CupHist.append(df) 
          PriceHist = PriceHist.append(prices) 
        else:
          CupHist = df
          PriceHist = prices
        CupHist.index = range(0,len(CupHist.index))
 if 'CupHist' in locals():
   if len(CupHist.index) > 1:
    CupHist['Date'] = map(lambda x: datetime.datetime.strptime(x, '%d.%m.%Y').strftime('%Y-%m-%d'),CupHist['Date'])
    PriceHist['Date'] = map(lambda x: datetime.datetime.strptime(x, '%d.%m.%Y').strftime('%Y-%m-%d'),PriceHist['Date'])
    PriceHist = PriceHist.sort_values('Date')
    CupHist = CupHist.sort_values('Date')
   CupHist.index = range(1,len(CupHist.index)+1)
   PriceHist.index = range(1,len(PriceHist.index)+1)

   CupHist = CupHist.loc[:, (CupHist != 0).any(axis=0)] ## removed never used drinks
   PriceHist = PriceHist[CupHist.columns]
   if len(CupHist.columns) > 2:
    PriceHist = PriceHist[CupHist['Sum'] != 0] ## removed empty rows (dates with no drinking)
    CupHist = CupHist[CupHist['Sum'] != 0] ## removed empty rows (dates with no drinking)
 else:
  SumExpend = 0
  CupHist = pd.DataFrame(np.zeros((1,10)),index=range(0,1),columns=Header)
  CupHist['Date'] = str(datetime.datetime.now())[:10]
  if len(latest_prices.columns) == 9:
   latest_prices['Ristretto'] = 0
  latest_prices = latest_prices[Header]
  PriceHist = latest_prices
 if len(CupHist.columns) < 2:
  SumExpend = 0
  CupHist = pd.DataFrame(np.zeros((1,10)),index=range(0,1),columns=Header)
  CupHist['Date'] = str(datetime.datetime.now())[:10]
  if len(latest_prices.columns) == 9:
   latest_prices['Ristretto'] = 0
  latest_prices = latest_prices[Header]
  PriceHist = latest_prices
  

 #####Converting to latex format
 CupHist.index = range(1,len(CupHist.index)+1)
 PriceHist.index = range(1,len(PriceHist.index)+1)
 PriceHist.columns = CupHist.columns
 lastRow = len(CupHist.index)-1
 CupHist.loc[lastRow+2] = CupHist.sum(axis=0)
 CupHist.loc[lastRow+2,'Date'] = '{\large$\sum$}'
 
 idx = CupHist.columns[range(1,len(CupHist.columns)-1)]
 CupHist.loc[:lastRow+1,idx] = '$'+CupHist.loc[:lastRow+1,idx].astype(int).astype(str)+'^{\\times '+PriceHist.loc[:lastRow+1,idx].astype(int).astype(str)+'\cent}$'
 CupHist.loc[lastRow+2,idx] = CupHist.loc[lastRow+2,idx].astype(int)

 idx = CupHist.columns[len(CupHist.columns)-1]
 SumExpend = CupHist.loc[lastRow+2,idx].astype(float)
 CupHist['Sum'] = map(lambda x: format(x,'.2f'),CupHist['Sum'])
 CupHist.loc[:lastRow+2,idx] = CupHist.loc[:lastRow+2,idx].astype(str)+'\scriptsize\EUR'
 CupHist.loc[len(CupHist.index)+1]=CupHist.loc[len(CupHist.index)]
 CupHist.loc[len(CupHist.index)-1,CupHist.columns[:]]=''
 return CupHist,SumExpend

def PaymentHist(Person):
 for root, dirs, files in os.walk("../../../"):
  for file in files:
     if file.endswith("PeoplePayment"):
      FileName = os.path.join(root, file)
      df = pd.read_csv(FileName)
      df = df[df['Name'] == Person]
      if df.index>=0:
        df = df.dropna(axis=1, how='any', thresh=None, subset=None, inplace=False)
        Version = root[14:18]+root[20:root.find('/',20)] ### Find Year+Vnumber
        if 'V_oldest' in locals():
         if V_oldest > Version:
           V_oldest = Version
           firstMoney = df.loc[df.index,'Last Termination']
        else:
         V_oldest = Version
         firstMoney = df.loc[df.index,'Last Termination']
         
                
        df = df.drop(['Name','Last Termination', 'Sum'], axis=1)
        Payed =  df[df.columns[range(0,len(df.columns),2)]].transpose()
        Dates = df[df.columns[range(1,len(df.columns),2)]].transpose()
        Dates.columns = ['Date']
        Dates.index = range(1,1+len(df.columns)/2)
        Payed.columns = ['Payed']
        Payed.index = range(1,1+len(df.columns)/2)
        PayHist_tmp = Payed.join(Dates)
        if 'PayHist' in locals():
         PayHist=PayHist.append(PayHist_tmp)
        else:
         PayHist = PayHist_tmp

 PayHist = PayHist[PayHist['Payed']!= 0]
 if len(PayHist.index) > 1: 
  PayHist['Date'] = map(lambda x: datetime.datetime.strptime(x, '%d.%m.%Y').strftime('%Y-%m-%d'),PayHist['Date'])
  PayHist = PayHist.sort_values('Date')
 PayHist.index = range(1,len(PayHist.index)+1)
 
 if len(PayHist.index) > 0:
  firstDate = PayHist.loc[1,'Date']
  firstMoney = list(firstMoney.loc[firstMoney.index])[0]
  if firstMoney != 0:
   firstMoney_df = pd.DataFrame(np.zeros((1,2)),index=range(0,1),columns=['Payed','Date'])
   firstMoney_df['Payed'] = firstMoney
   firstMoney_df['Date'] = 'Before'#+firstDate
   PayHist = firstMoney_df.append(PayHist)
 
  PayHist = PayHist.append(pd.DataFrame(np.zeros((1,2)),index=range(0,1),columns=['Payed','Date']))
  PayHist.index = range(1,len(PayHist.index)+1)
  ### To make all payment of the the same width. i.e., being adding zeros before integer part and 2 decimal points
  PayHist['Payed'] = map(lambda x: format(x,'.2f'),PayHist['Payed'])
#  num_digits = int(np.log10(np.abs(PayHist['Payed']).max()))+1  
#  PayHist['Payed'] = map(lambda x: str(int(x)).zfill(num_digits)+format(float(round((x-int(x))*100)/100),'.2f')[1:],PayHist['Payed'])

  SumPayment = np.sum(PayHist['Payed'].astype(float))
  PayHist.loc[len(PayHist)] = [format(SumPayment,'.2f'), '{\large$\sum$}']
  PayHist['Payed'] = PayHist['Payed'].astype(str)+'\scriptsize\EUR'
  PayHist = PayHist[['Date','Payed']]
  PayHist.loc[len(PayHist.index)+1]=PayHist.loc[len(PayHist.index)]
  PayHist.loc[len(PayHist.index)-1,PayHist.columns[:]]=''
 elif Person == "Halil Alper Tokel":
  SumPayment = 7.42
  PayHist = pd.DataFrame(np.zeros((3,2)),index=range(0,3),columns=['Date', 'Payed'])
  PayHist['Payed'] =  str(SumPayment)+'\scriptsize\EUR'
  PayHist.loc[0,'Date'] = 'Befor 2015-05-21'
  PayHist.loc[2,'Date'] = '{\large$\sum$}'
  PayHist.loc[1] = ''
 else:
  SumPayment = 0
  PayHist = pd.DataFrame(np.zeros((3,2)),index=range(0,3),columns=['Date','Payed'])
  PayHist.loc[0,'Date'] = 'Until '+str(datetime.datetime.now())[:10]
  PayHist.loc[2,'Date'] = '{\large$\sum$}'
  PayHist.loc[1] = ''
  PayHist.loc[:,'Payed'] = '0.00\scriptsize\EUR'
 return PayHist,SumPayment
