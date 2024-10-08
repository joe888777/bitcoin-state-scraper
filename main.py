import requests
from bs4 import BeautifulSoup
import datetime
import pytz
import csv
import json
import model
import utils

# a timestamp I'd like to convert
my_timestamp = datetime.datetime.now()

# create both timezone objects
old_timezone = pytz.timezone("US/Eastern")
new_timezone = pytz.timezone("US/Pacific")

# two-step process
localized_timestamp = old_timezone.localize(my_timestamp)
new_timezone_timestamp = localized_timestamp.astimezone(new_timezone)

# or alternatively, as an one-liner
new_timezone_timestamp = old_timezone.localize(my_timestamp).astimezone(new_timezone) 

url = "https://bitinfocharts.com/top-100-richest-bitcoin-addresses.html"



user_agent = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'


def normalize(data, typeNames):
    count = 0
    newData = []
    for row in data:
        if len(row) == 0:
            continue
        if row[0] == typeNames[0]:
            count += int(row[1])
        if row[0] == typeNames[1]:
            count += int(row[1])
        if row[0] == typeNames[2]:
            count += int(row[1])
        if row[0] == typeNames[3] or row[0] == typeNames[4]:
            count += int(row[1])
        if row[0] == typeNames[5]:
            count += int(row[1])
            newData.append(["0.001 ~ 1", count, new_timezone_timestamp])
            count = 0
        if row[0] == typeNames[6]:
            count += int(row[1])
            newData.append(["1 ~ 10", count, new_timezone_timestamp])
            count = 0
        if row[0] == typeNames[7]:
            count += int(row[1])
            newData.append(["10 ~ 100", count, new_timezone_timestamp])
            count = 0
        if row[0] == typeNames[8]:
            count += int(row[1])
        if row[0] == typeNames[9]:
            count += int(row[1])
        if row[0] == typeNames[10]:
            count += int(row[1])
        if row[0] == typeNames[11]:
            count += int(row[1])
            newData.append(["100 up", count, new_timezone_timestamp])

    return newData

def main():
    header = {
        'User-Agent': user_agent,
        'cookie': "lc-acbjp=en; i18n-prefs=USD;"
    }

    r = requests.session().get(url, headers=header)
    html = r.text

    soup = BeautifulSoup(html, 'html5lib')
    tables = soup.find_all('table')
    table = tables[0]
    data = []
    for tr in table.find_all('tr'):
        td = tr.find_all('td')
        row = [i.text for i in td]
        data.append(row)

    # data 2 csv
    # types mean 10^n
    types = [-9999, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
    typeNames = [
        "(0 - 0.00001)",
        "[0.00001 - 0.0001)",
        "[0.0001 - 0.001)",
        "[0.001 - 0.01)",
        "[0.01 - 0.1)",
        "[0.1 - 1)",
        # type 1
        "[1 - 10)",
        "[10 - 100)",
        # type 2
        "[100 - 1000)",
        "[1,000 - 10,000)",
        "[10,000 - 100,000)",
        "[100,000 - 1,000,000)",
        #type 3
    ]

    ## type 1: 0.001 ~ 1
    ## type 2: 1 ~ 10
    ## type 3: 10 ~ 100
    ## type 4: 100 up
    latestSerailArray = model.get_latest_bitcoin_serial();
    latestSerail = 0;
    if (latestSerailArray != None):
        for btc_info in latestSerailArray:
            latestSerail = btc_info.serial;
    print(latestSerail)
    data = normalize(data, typeNames=typeNames)
    for row in data:
        if len(row) == 0:
            continue
        
        name = row[0]
        addresses = int(row[1])
        model.create_bitcoin_info(name, addresses, serial=latestSerail+1)
    with open('test.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(normalize(data, typeNames=typeNames))

if __name__ == '__main__':
    main()