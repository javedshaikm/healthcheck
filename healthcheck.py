from __future__ import print_function
from netmiko import ConnectHandler
import pandas as pd
import smtplib
import sys
import time
import select
import paramiko
import re
from io import StringIO
import smtplib


username = 'cisco'
password = 'cisco_1234!'
#int_down = r"is administratively down"
#result_file = open(r'D:\\python\\python-cisco-status.txt','r+')
hosts = ['10.10.20.48']
platform = 'cisco_xe'


def send_mail():
	sender = '@gmail.com'
	receivers = ['@hotmail.com']
	try:
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.login("@gmail.com", "")
		server.sendmail(sender, receivers, message)         
		print ('Successfully sent email')
	except SMTPException:
		print ('Error: unable to send email')



for host in hosts:
	connect = ConnectHandler(device_type=platform, ip=host, username=username, password=password)
	output = connect.send_command('terminal length 0', expect_string=r'#')
	output = connect.send_command('enable',expect_string=r'#')
	host_name = connect.send_command('show run | in hostname',expect_string=r'#')
	interface_status = connect.send_command(f'show ip int brief',expect_string=r'#')
	old_stdout = sys.stdout
	sys.stdout = StringIO
	#print(interface_status)
	sys.stdout = old_stdout
	#data = pd.read_fwf('D:\\python\\python-cisco-status.txt',  widths=[23, 16, 3, 7, 22, 8])
	data = pd.read_fwf(StringIO(interface_status),  widths=[23, 16, 3, 7, 22, 8])
	#print(data)
	message = " "
	for index, row in data.iterrows():
		if row[4] == 'administratively down' or row[4] == 'down':
			#print(f"Interface {row[0]} is down in {host_name}")
			log = (f"\nInterface {row[0]} is down in {host_name}\n")
			message += log
	print(message)
	send_mail()
	#	print(row[0])
