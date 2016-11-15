from flask import Flask,flash,render_template
from lxml import html
import sqlite3
import requests
import urlparse
import sys
app = Flask(__name__)
@app.route("/")
def process():
	conn = sqlite3.connect('data.db')            #review is not scrapped as of now
	conn.execute('''CREATE TABLE info               
       	(id integer primary key,
       	appName           char,
	compName           char,
       	downloads         char,
       	version           char,
       	priced            char);''')
       	conn.close()
	with open('list.txt','r') as r:
		for line in r:	
			page = requests.get(urlparse.urljoin("https://play.google.com/", line))
			tree = html.fromstring(page.content)
											
			appName = tree.xpath('//title[@id="main-title"]/text()')     #Name of the app
			if not appName: 
				return "Process completed"
			compName = tree.xpath('//span[@itemprop="name"]/text()')     #This will extract company's name:
			prices = tree.xpath('//span[@class="display-price"]/text()') #price of apps 
			address = tree.xpath('//div[@class="content physical-address"]/text()') #Address of the developer
			version= tree.xpath('//div[@itemprop="softwareVersion"]/text()') #Current Version
			numDown = tree.xpath('//div[@itemprop="numDownloads"]/text()') #number of downloads
			with sqlite3.connect("data.db") as con:
    				cur = con.cursor()							 
   				cur.execute("INSERT INTO info (appName,compName,downloads,version,priced) VALUES (?,?,?,?,?)",(str(appName),str(compName),str(numDown),str(version),str(prices[1])) )
	    			con.commit()
	return "Hello World!"
if __name__ == "__main__":
    app.run()
