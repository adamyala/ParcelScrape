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

clearfile = open('hudsp.csv','w+')
clearfile.close()

def scrape():

	sesh = requests.Session()
	sesh.get('https://propaccess.trueautomation.com/ClientDB/PropertySearch.aspx?cid=97')

	with open('hudsp.csv','wb') as output:

		for x in range(16906,16907):

			result = []
			print_flag = True

			url = 'https://propaccess.trueautomation.com/ClientDB/Property.aspx?prop_id='
			url = url + str(x)
			print url

			page = sesh.get(url)
			soup = BeautifulSoup(page.content)

			data = soup.find_all('table')
			holder = strip_tags(str(data[4])).strip().split(',')[0]
			#data = soup.find_all('td')
			
			#for row in data:
			#	result.append(strip_tags(str(row)).strip())
			#holder = strip_tags(str(data)).strip().split(',')[0]
			print holder
			if holder != '[RESIDENTIAL':
				for row in data:
					result.append(strip_tags(str(row)).strip())
					print_flag = False
				#print row
			#pp = pprint.PrettyPrinter(indent=4)
			#pp.pprint(data)

			print len(result)
			print result
			print print_flag
			if len(result) > 6:
				if print_flag:
					print len(result)
				#if '<tr><td>No improvements exist for this property.</td></tr>' in data:
				#print 'skipped'
					resultfile = csv.writer(output, delimiter=',')
					resultfile.writerow(result)

scrape()
