import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import smtplib
from email.mime.text import MIMEText
import email.mime.application
#import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
#from email.Utils import COMMASPACE, formatdate
from email import Encoders
import keyring
import getpass
#import getent
def mailSend(recipient,subject,body,files):
	###### To get the username automatically from the computer
	username = getpass.getuser()
	username = str(keyring.get_password('coffee', 'username'))
	password = str(keyring.get_password('coffee', 'password'))
	if username == 'None':
		username = str(raw_input("Please insert your logging name for the mail server: "))
		keyring.set_password('coffee', "username",username)
	if username == 'None':
		username = str(raw_input("Please insert your logging name for the mail server: "))
		keyring.set_password('coffee', "username",username)
	if str(password) == 'None':
		password = getpass.getpass("Please insert your mail server password. It will be stored in your keyring:")
		keyring.set_password('coffee', "password",password)

	###### To get the first and sir name of sender automatically from the computer
#	MyName = getent.passwd(username).gecos[0:len(getent.passwd(username).gecos)-3]
	###### The sender name of desire
	MyName = "Ti Coffee Team"
	###### email domail
	domain = "ti.rwth-aachen.de"
	sender = username+"@"+domain
	msg = MIMEMultipart()
	msg['Subject'] = subject
	msg['From']= MyName+" <"+sender+">"
	msg['To'] = recipient
	#msg.attach( MIMEText(body) )
	msg.attach( MIMEText(body.encode('utf-8'), 'plain', 'utf-8')) 
	
	for fileName in files:
		if type(files) is not list:
			fileName = files
		part = MIMEBase('application', "octet-stream")
		part.set_payload( open(fileName,"rb").read() )
		Encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(fileName))
		msg.attach(part)
		if type(files) is not list:
			break	
#	s = smtplib.SMTP("mail.ti.rwth-aachen.de:25")
	s = smtplib.SMTP("mail.ti.rwth-aachen.de:587")
	s.ehlo()
	s.starttls()
	s.login(username,password)
	try:
				if subject != "test":
							s.sendmail(sender, recipient, msg.as_string())
	except:
				raw_input("Email was not sent to "+recipient+ ". Please check the email address!")
	s.quit()

