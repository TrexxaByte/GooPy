import os
import re
import requests
import time
from tkinter import messagebox
import subprocess


winuser = os.getlogin()
logpath = 'C:\\Users\\' + winuser + '\\Documents\\GooPy\\'			# Confirm or create directory where files will be written.
if os.path.exists(logpath) is False:
    os.mkdir(logpath)


def chrome_history(path=None):
	'''Parses Google's data file BrowserHistory.json included in personal data. Info is written to a new file formatted with more readability.'''
	cfiles = {}
	filenum = 1
	logfile = 'C:\\Users\\' + winuser + '\\Documents\\GooPy\\ChromeHistory_GooPy.txt'	# File to be written after data is collected.

	# Attempt to find the file in the event the user didn't place the file in the correct location.
	if path == None:
		current = os.path.dirname(__file__)
	else:
		current = os.path.abspath(path)

	dirs = os.listdir(current)
	if 'Chrome' in dirs:
		target = os.path.join(current, 'Chrome')
		files = os.listdir(target)
	elif os.path.basename(current) == 'Chrome':
		target = current
		files = os.listdir(current)
	else:
		messagebox.showerror(title='Files Not Found!', message='Could not find data files... please either supply the path \
to your downloaded Google data or move this script file to the Google "takeout" directory.')
		return

	# If still unable to find the correct file, try whichever file is the largest (more often than not, the largest is the history file).
	fsize = 0
	fname = ''
	for f in files:
	    f = os.path.join(target, f)
		size = os.path.getsize(f)
		(k, v) = os.path.basename(f), round(size / 1024)
		cfiles[str(k)] = str(v) + ' KB'
		if size > fsize:
			fsize = size
			fname = f
		else:
			pass

	# Get file or confirm with user whether they want to try parsing the largest file or quit.
	if 'BrowserHistory.json' in files:
		histfile = files.index('BrowserHistory.json')
		histfile = os.path.join(target, files[histfile])
	elif 'BrowserHistory.json' not in files:
		no_file = messagebox.askyesno(title='Continue?', message='Browser history file could not be found. Continue processing largest file ' + fname + ' instead?')
		if no_file is True:
			histfile = fname
		else:
			return

	# Read the file.
	with open(histfile, encoding='utf-8') as history:
		data = history.read()

	# Locate the pertinent pieces of data and log them as records to be written to file. 
	recs = []
	eof = data.rfind('title') - 20
	etime = 10
	while etime < eof:
		stitle = data.find('title":', etime) + 9
		etitle = data.find('",', stitle)
		title = data[stitle:etitle]

		surl = data.find('url":', etitle) + 7
		eurl = data.find('",', surl)
		url = data[surl:eurl]

		stime = data.find('time_usec":', eurl) + 12
		etime = data.find('\n', stime) - 6
		stamp = time.ctime(int(data[stime:etime]))

		rec = 'Time Stamp:  ' + stamp + '   Page:  ' + title + '\n' + 'Link:   ' + url + '\n' \
		   + '__________________________________________________________________' + '\n\n'
		recs.append(rec)
	
	# Increment the file number if one already exists.
	if os.path.exists(logfile):
		logfile = logfile[:-4] + '_' + str(filenum) + '.txt'
		filenum = int(filenum) + 1

	# Begin writing the data to the file.
	with open(logfile, 'a+', encoding='utf-8') as log:
		for rec in recs:
			log.write(rec + '\n')

	messagebox.showinfo(title='File Complete!', message='Processing is finished. Data file written to Documents folder under the GooPy directory.')



def logins(path=None):
	'''Parses the data file under the Google Account folder found in the download of personal Google data. File typically contains the suffix "SubscriberInfo.html".'''
	
	if path == None:
		current = os.path.curdir()
	else:
		current = path

	content = os.listdir(current)
	actlog = logpath + 'GoogleLogins_GooPy.txt'

	# Start the process of locating the file.
	try:
		if 'Google Account' in content:
			accfile = os.listdir(current + '\\Google Account')
		elif 'Google' in content:
			accfile = os.listdir(current + '\\Google\\Google Account')
		elif 'takeout' in content:
			accfile = os.listdir(current + '\\takeout\\Google\\Google Account')
		else:
			accfile = os.listdir(current)
	except FileNotFoundError:
			messagebox.showerror(title='Google Folders Not Found!', message='Please either supply the path to your Google data or launch/run this from the takeout or Google folder.')
			return

	# Check that the file is in HTML format.
	if accfile[0].endswith('html') is False:
		messagebox.showerror(title='Expected HTML File', message='Google Account activity is an HTML file - could not process the file as it is not HTML.')
		return

	# Open the file and read it.
	acc = current + '\\Google Account\\' + accfile[0]
	with open(acc, encoding='utf-8') as acclog:
		html = acclog.read()

	# Parse the HTML to find regular text.
	page = BeautifulSoup(html)
	logs = page.getText()
	ipadds = []
	recs = []

	# Run a check against the IP addresses found in the login/logout activity of Google account to gather geolocation info.
	net = subprocess.getoutput('ipconfig')

	ipaddress = re.compile(r'\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}')
	datestamp = re.compile(r'\d{4}[-]\d{2}[-]\d{2}')
	timestamp = re.compile(r'\d{2}[:]\d{2}[:]\d{2}')

	lan = re.findall(ipaddress, net)
	ips = re.findall(ipaddress, logs)

	# Eliminate any IP addresses that are confirmed to be from the current system.
	for ip in ips:
		if ip in ipadds:
			continue
		elif ip in lan:
			continue

		ipadds.append(ip)

		stamp = logs.find(ip) - 40
		templog = logs[stamp:]

		get_date = re.search(datestamp, templog)
		date = templog[get_date.start():get_date.end()]
		get_time = re.search(timestamp, templog)
		time = templog[get_time.start():get_time.end()]
		action = templog.find('log', stamp + 40)

		# Run the IP to obtain geolocation information and create log records to write to file.
	for ip in ipadds:
		req = requests.get('https://api.iplocation.net/?ip=' + ip)
		resp = req.json()

		addr = resp['ip']
		host = resp['hostname']
		city = resp['city']
		state = resp['region']
		zipcode = resp['postal']
		country = resp['country']

		rec = 'DATE:  ' + date + '\t TIME:  ' + time + '\n' + 'IP:  {0} \t HOST:  {1} \n CITY: {2}   STATE: {3}    ZIP: {4}    COUNTRY: {5} \n\n\n'.format(addr, host, city, state, zipcode, country)

		recs.append(rec)
		
		# Write the file.
	with open(actlog, 'a+') as act:
		for rec in recs:
			act.write(rec)
