# -*- coding: utf-8 -*-
import BeautifulSoup
import urllib2
import re
import time
from datetime import datetime, date, timedelta
import mysql.connector
from mysql.connector import errorcode

USERAGENT = 'Mozilla/5.0'
flag = 1
# search fields
searches = []

# read csv file
f = open('list.csv', 'r')
for line in f:
  searches.append(line)
f.close()

#Database
config = {
	'user': 'root',
	'password':'root',
	'host': '127.0.0.1',
	'port': '80',
	'database': 'database',
}
s_table = 'yahoo'

#base url
link1 = 'http://search.yahoo.co.jp/search?p='

def procedure1():
	time.sleep(60)
def procedure2():
	time.sleep(2)
def extractString(start, end, data):
	extractField=start+"(.*?)"+end
	r1=re.compile(extractField)
	r2=r1.search(data)
	if r2:
		result = r2.group(1)
		return float(re.sub('[,]','', result))
	else:
		return 0

while flag == 1:
	try:
		conn = mysql.connector.connect(**config)
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your username or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	if conn.is_connected():
		print('Connected to MySQL database')
	cursor = conn.cursor(buffered=True)
	i=0
	for search in searches:
		url = link1 + search
		req = urllib2.Request(url)
		req.add_header("User-agent", USERAGENT)
		response = urllib2.urlopen(req)
		# print response.info()
		html = response.read()
		soup=BeautifulSoup.BeautifulSoup(html)    
		resultDirty = soup.find(id="inf").text
		response.close()
		# resultDirty = "オレンジで検索した結果　1～10件目 / 約94,400,000件 - 0.32秒"
		print resultDirty.encode('utf_8') 
		resultClear = resultDirty.encode('utf_8')
		count = int(extractString("約", "件", resultClear))
		reqTime = extractString("件 - ", "秒", resultClear)
		today = datetime.now()
		print "result"+str(i)+": " + str(count) + ", " + str(reqTime) + "seconds"
		add_Yahoo = ("INSERT INTO yahoo"
								"(date, keyword, count, sec)"
								"VALUES (%s, %s, %s, %s)")
		data_Yahoo = (today, search, count, reqTime)
		cursor.execute(add_Yahoo, data_Yahoo)
		emp_no = cursor.lastrowid
		conn.commit()
		procedure2()
		i = i+1
	cursor.close()
	conn.close()
	procedure1()
	
	# python3
	# for search in text:
	# url = search
	# req = urllib.request.Request(url)
	# req.add_header("User-agent", USERAGENT)
	# response = urllib.request.urlopen(req)
	# html = response.read()
	# soup=BeautifulSoup(html)    
	# resultDirty = soup.find(name="**")
	# response.close()
	# print(resultDirty)


