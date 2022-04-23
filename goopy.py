from bs4 import BeautifulSoup
import os
import re
import requests
import time
from tkinter import messagebox


winuser = os.getlogin()

def chrome_history(path=None):
	cfiles = {}
	filenum = 1
	logfile = 'C:\\Users\\' + winuser + '\\Documents\\GooPy\\ChromeHistory_GooPy.txt'

	if os.path.exists(os.path.dirname(logfile)) is False:
		os.mkdir(os.path.dirname(logfile))

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

	if 'BrowserHistory.json' in files:
		histfile = files.index('BrowserHistory.json')
		histfile = os.path.join(target, files[histfile])
	elif 'BrowserHistory.json' not in files:
		no_file = messagebox.askyesno(title='Continue?', message='Browser history file could not be found. Continue processing largest file ' + fname + ' instead?')
		if no_file is True:
			histfile = fname
		else:
			return

	with open(histfile, encoding='utf-8') as history:
		data = history.read()
	
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

		rec = 'Time Stamp:  ' + stamp + '   Page:  ' + title + '\n' + 'Link:     ' + url + '\n' \
		   + '__________________________________________________________________' + '\n\n'
		recs.append(rec)

	if os.path.exists(logfile):
		logfile = logfile[:-4] + '_' + str(filenum) + '.txt'
		filenum = int(filenum) + 1
	
	with open(logfile, 'a+', encoding='utf-8') as log:
		for rec in recs:
			log.write(rec + '\n')

	messagebox.showinfo(title='File Complete!', message='Processing is finished. Data file written to Documents folder under the GooPy directory.')



def logins(path=None):
	current = os.path.curdir
	content = os.listdir(current)
	try:
		if 'Google Account' in content:
			accfile = os.listdir(os.path.curdir + '\\Google Account')
		elif 'Google' in content:
			accfile = os.listdir(os.path.curdir + '\\Google\\Google Account')
		elif 'takeout' in content:
			accfile = os.listdir(os.path.curdir + '\\takeout\\Google\\Google Account')
		else:
			accfile = os.listdir(os.path.curdir)
	except FileNotFoundError:
			messagebox.showerror(title='Google Folders Not Found!', message='Please either supply the path to your Google data or launch/run this from the takeout or Google folder.')
			return

	if accfile[0].endswith('html') is False:
		messagebox.showerror(title='Expected HTML File', message='Google Account activity is an HTML file - could not process the file as it is not HTML.')
		return

	with open(accfile[0], encoding='utf-8') as acc:
		html = acc.read()

	page = BeautifulSoup(html)
	logs = page.getText(separator='     ')

	ipadds = []
	logs = []
	ipaddress = re.compile(r'\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}')
	ips = re.findall(ipaddress, logs)
	for ip in ips:
		if ip in ipadds:
			pass
		else:
			ipadds.append(ip)

	for ip in ipadds:
		req = requests.get('http://ipinfo.io/json')
		resp = req.json()

		addr = resp['ip']
		host = resp['hostname']
		city = resp['city']
		state = resp['region']
		zipcode = resp['postal']
		country = resp['country']

		rec = ' IP:  {0} \t HOST:  {1} \n CITY: {2}   STATE: {3}    ZIP: {4}    COUNTRY: {5}'.format(ip, host, city, state, zipcode, country)
		logs.append(rec)
	