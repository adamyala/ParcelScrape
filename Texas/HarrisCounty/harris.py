# coding=utf-8

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

clearfile = open('harris.csv','w+')
clearfile.close()

def bldg_details(bldg_data):
    total = 0
    avg = 0
    result = []
    for item in bldg_data:
        total = total + int(item[4].replace(",", ""))

    for item in bldg_data:
        avg = avg + int(item[0]) * float(item[4].replace(",", "")) / total

    result.append(total)
    result.append(avg)
    return result

def scrape():

        fileobj = open('harrispins.txt')
        lines = fileobj.readlines()
        fileobj.close()

        with open('harris.csv','wb') as output:

                for x in range(len(lines)):

                    print x

                    print lines[x][:-1]

                    result = []
                    result.append(lines[x][:-1])

                    bldg_data = []

                    url = 'http://www.hcad.org/records/recorddetails.asp?tab=1&card=1&taxyear=2014&acct=' + lines[x][:-1]
                        # 'http://www.hcad.org/records/recorddetails.asp?tab=1&card=1&taxyear=2014&acct=0012340000009'

                    print url

                    page = requests.get(url)
                    soup = BeautifulSoup(page.content, 'html.parser')

                    #parses source for all 'tr' tags
                    parsed = soup.find_all(['td', 'th'])
                    parsed = [strip_tags(str(item)).strip() for item in parsed]

                    data= []

                    for item in parsed:
                        if item != "":
                            data.append(item)

                    # print data

                    testering = []

                    for i in range(len(data)):

                        # print data[i]

                        if data[i] == "Building Details":

                            first_pass = True

                            while data[i+1] != "Building Details (1)":

                                bldg_line = [0] * 5

                                bldg_line[0] = data[i+2]

                                bldg_line[1] = data[i+3]

                                bldg_line[2] = data[i+4]

                                bldg_line[3] = data[i+5]

                                bldg_line[4] = data[i+6]


                                if first_pass:

                                    i += 7

                                    first_pass = False

                                else:

                                    i +=6

                                bldg_data.append(bldg_line)

                                # print bldg_data

                    testering = bldg_details(bldg_data)

                    result.append(testering[0])

                    result.append(testering[1])

                    url = 'http://www.hcad.org/records/Ownership.asp?acct=' + lines[x] +  '&taxyear=2014'

                    # print url

                    #gets source data
                    page = requests.get(url)
                    soup = BeautifulSoup(page.content, 'html.parser')

                    #parses source for all 'tr' tags
                    parsed = soup.find_all(['td', 'th'])
                    parsed = [strip_tags(str(item)).strip() for item in parsed]

                    data = []

                    for item in parsed:

                        if item != "":

                            data.append(item)

                    for i in range(len(data)):

                        if data[i] == "Owner":

                            result.append(data[i+3])

                    resultfile = csv.writer(output, delimiter=',')

                    print result

                    resultfile.writerow(result)


scrape()
