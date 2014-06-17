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

clearfile = open('elpaso.csv','w+')
clearfile.close()

def scrape():

        sesh = requests.Session()
        sesh.get('http://www.epcad.org/clientdb/?cid=1')

        with open('elpaso.csv','wb') as output:

                for x in range(200000,300000):
                        #sets empty final list and sets flag
                        result = [0] * 7

                        counter = 0
                        print_flag = True

                        #builds url
                        url = 'http://www.epcad.org/clientdb/Property.aspx?prop_id='
                        url = url + str(x)
                        print url

                        #gets source data
                        page = sesh.get(url)
                        soup = BeautifulSoup(page.content, 'html.parser')



                        #parses source for all 'tr' tags
                        data = soup.find_all(['td', 'th'])

                        #print data

                        for i in range(len(data)):
                                #print counter
                                #print result[6]
                                #print data[i]
                                #result.append(strip_tags(str(data[i])).strip())
                                holder = strip_tags(str(data[i])).strip()
                                #print holder
                                if holder == 'No improvements exist for this property.':
                                        print_flag = False
                                        break

                                if holder == 'Residential' or holder == 'Mobile Home':
                                        print_flag = False
                                        break

                                if holder == "Property ID:":
                                    result[0] = strip_tags(str(data[i+1])).strip()
                                    #print holder

                                if holder == "Address:":
                                    result[1] = strip_tags(str(data[i+1])).strip()
                                    #print holder

                                if holder == "State Code:":
                                    result[2] = strip_tags(str(data[i-1])).strip()
                                    #print holder

                                if holder == "Assessed":
                                    result[3] = strip_tags(str(data[i+9])).strip()
                                    #print holder

                                if holder == "Deed Number":
                                    result[4] = strip_tags(str(data[i+2])).strip()
                                    print result[4]

                                if holder == "Living Area:":
                                    if len(strip_tags(str(data[i+1])).strip()[:-5]) > 2:
                                        result[5] = result[5] + float(strip_tags(str(data[i+1])).strip()[:-5])
                                    else:
                                        print_flag = False
                                    #print result [5]

                                if holder == "Year Built":
                                    #print strip_tags(str(data[i+8])).strip()
                                    counter +=1
                                    result[6] = result[6] + int(strip_tags(str(data[i+7])).strip())
                                    #print counter
                                    #print result [6]

                        print print_flag

                        #print x
                        print len(data)

                        if len(data) == 8: continue

                        if len(data) == 45:
                                sesh.get('http://www.epcad.org/clientdb/?cid=1')
                                x -= 1
                                continue

                        if print_flag:
                                #print counter
                                result[6] = result[6] / counter
                                #print len(result)
                                resultfile = csv.writer(output, delimiter=',')
                                resultfile.writerow(result)

scrape()
