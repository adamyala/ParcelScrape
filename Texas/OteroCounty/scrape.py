import requests
from bs4 import BeautifulSoup
import csv
import re

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

clearfile = open('otero2.csv','w+')
clearfile.close()

def scrape():

	count = 0

	url = 'http://qpublic6.qpublic.net/co_otero_display.php?KEY=464310217010&account=114151'

	with open('otero2.csv','wb') as output:
		for x in range(0,10000):

			result = []

			page = requests.get(url)

			soup = BeautifulSoup(page.content)
			#soup = re.sub(r'&(?!amp;)', r'&amp;', soup.text.encode('utf-8'))

			next_link = str(soup.find_all('a')[1])[9:-19]
			
			#print next_link

			next_link =  next_link.replace("amp;","")

			url = next_link
			print url			

			data =  soup.find_all('td')

			for row in data:
				result.append(strip_tags(str(row)))	

			resultfile = csv.writer(output, delimiter=',')
			resultfile.writerow(result)
	
			count+= 1
			print count

scrape()
