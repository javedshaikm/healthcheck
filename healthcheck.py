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
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


username = 'cisco'
password = 'cisco_1234!'
hosts = ['10.10.20.48']
platform = 'cisco_xe'


def send_mail():
	fromaddr = "jfshaism@gmail.com"
	toaddr = "javed.s.m@hotmail.com"
	msg = MIMEMultipart()
	msg['From'] = 'jfshaism@gmail.com'
	msg['To'] = 'javed.s.m@hotmail.com'
	msg['Subject'] = "This is Health check"
	msg.attach(MIMEText(status, 'plain'))	
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "allah@kind")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()


for host in hosts:
	connect = ConnectHandler(device_type=platform, ip=host, username=username, password=password)
	output = connect.send_command('terminal length 0', expect_string=r'#')
	output = connect.send_command('enable',expect_string=r'#')
	host_name = connect.send_command('show run | in hostname',expect_string=r'#')
	interface_status = connect.send_command(f'show ip int brief',expect_string=r'#')
	old_stdout = sys.stdout
	sys.stdout = StringIO
	sys.stdout = old_stdout
	data = pd.read_fwf(StringIO(interface_status),  widths=[23, 16, 3, 7, 22, 8])
	status = " "
	for index, row in data.iterrows():
		if row[4] == 'administratively down' or row[4] == 'down':
			log = (f"\nInterface {row[0]} is down in {host_name}\n")
			status += log
	send_mail()
	
