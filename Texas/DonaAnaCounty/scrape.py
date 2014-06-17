import requests
import pprint
from bs4 import BeautifulSoup
import csv

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

clearfile = open('dona2.csv','w+')
clearfile.close()

def scrape():

	sesh = requests.Session()

	with open('dona2.csv','wb') as output:

		for x in range(109781,300000):

			result = []
			print_flag = True

			url = 'http://www.donaanacounty.org/assessor/prop_search/account/'
			url = url + str(x) + '/1'
			print url

			page = sesh.get(url)
			soup = BeautifulSoup(page.content)

			data = soup.find_all('td')
			for row in data:
				result.append(strip_tags(str(row)).strip())
				holder = strip_tags(str(row)).strip()
				#print holder
				#if holder == 'No improvements exist for this property.':
				#	print_flag = False
				#print row
			#pp = pprint.PrettyPrinter(indent=4)
			#pp.pprint(data)

			#print len(result)
			#print result
			#print print_flag
			if len(result) > 6:
				#if print_flag:
				print len(result)
				#if '<tr><td>No improvements exist for this property.</td></tr>' in data:
				#print 'skipped'
				resultfile = csv.writer(output, delimiter=',')
				resultfile.writerow(result)

scrape()
