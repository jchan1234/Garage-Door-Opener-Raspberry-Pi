#!/usr/bin/python
import smtplib
import sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] =  to_addr_list
    msg['Subject'] = subject
    body=message
    msg.attach(MIMEText(body,'plain'))
    header  = 'From: %s' % from_addr
    header += 'To: %s' % ','.join(to_addr_list)
    header += 'Cc: %s' % ','.join(cc_addr_list)
    header += 'Subject: %s' % subject
    message = header + message
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    text = msg.as_string()
    problems = server.sendmail(from_addr, to_addr_list, text)
    server.quit()

#sendemail(from_addr    = 'GPI',
#          to_addr_list = '<bell number>@txt.bell.ca',
#          cc_addr_list = '',
#          subject      = '',
#          message      = sys.argv[1],
#          login        = '<gmail id>',
#          password     = '<gmail pwd>')

#sendemail(from_addr    = 'GPI',
#          to_addr_list = '<rogers number>@sms.rogers.com',
#          cc_addr_list = '',
#          subject      = '',
#          message      = sys.argv[1],
#          login        = '<gmail id>',
#          password     = '<gmail pwd>')
