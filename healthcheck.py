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
password = 'cisco'
hosts = ['10.0.10.100','10.0.10.101']
platform = 'cisco_ios'

def send_mail():
	fromaddr = "@gmail.com"
	toaddr = "@hotmail.com"
	msg = MIMEMultipart()
	msg['From'] = '@gmail.com'
	msg['To'] = '@hotmail.com'
	msg['Subject'] = "This is Health check"
	msg.attach(MIMEText(status, 'plain'))	
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "password")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

status = " "
for host in hosts:
	connect = ConnectHandler(device_type=platform, ip=host, username=username, password=password)
	output = connect.send_command('terminal length 0', expect_string=r'#')
	output = connect.send_command('enable',expect_string=r'#')
	host_name = connect.send_command('show run | in hostname',expect_string=r'#')
	interface_status = connect.send_command(f'show ip int brief',expect_string=r'#')
	old_stdout = sys.stdout
	interface_result = StringIO()
	sys.stdout = interface_result
	sys.stdout = old_stdout
	data = pd.read_fwf(StringIO(interface_status),  widths=[27, 16, 3, 7, 23, 8])
	for index, row in data.iterrows():
		if row[4] == 'administratively down' or row[4] == 'down':
			log = (f"\nInterface {row[0]} is down in {host_name}\n")
			status += log
	
	bgp_status = connect.send_command('show ip bgp summary | be N',expect_string=r'#')
	old_stdout = sys.stdout
	bgp_result = StringIO()
	sys.stdout = bgp_result
	sys.stdout = old_stdout
	bgp_data = pd.read_fwf(StringIO(bgp_status),  delim_whitespace=True, header=None)
	
	for index, row in bgp_data.iterrows():
		if row[9] == 'Down' or row[9] == 'Idle' or row[9] == 'Active':
			bgp = (f"\nNeighbor {row[0]} is down in {host_name}\n")
			status += bgp
send_mail()
	
	
