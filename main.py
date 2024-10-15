import requests
from bs4 import BeautifulSoup
import datetime
import pytz
import csv
import json
import model
import utils
from enum import Enum
from config import settings

# a timestamp I'd like to convert

class DataAttr(Enum):
    BTC_DELTA = "btc_delta"
    USD_DELTA = "usd_delta"
    HOLDER_DELTA = "holder_delta"
    HOLDER_COUNT = "holder_count"
    BTC_COUNT = "btc_count"
    USD_COUNT = "usd_count"

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
    holderCount = 0
    btcCount = 0
    usdCount = 0
    newData = []

    for row in data:
        if len(row) == 0:
            continue

        holders = int(row[1])
        print(row[3])
        btcs = row[3].split()[0].replace(',', '')
        btcs = float(btcs)

        usds = row[4].replace('$', '').replace(',', '')
        usds = float(usds)

        if (row[0] == typeNames[0] or
                row[0] == typeNames[1] or
                row[0] == typeNames[2] or
                row[0] == typeNames[3] or
                row[0] == typeNames[4]):
            holderCount += holders
            btcCount += btcs
            usdCount += usds
        elif row[0] == typeNames[5]:
            holderCount += holders
            btcCount += btcs
            usdCount += usds
            newData.append(["0.001 ~ 1", holderCount, btcCount, usdCount, new_timezone_timestamp])
            holderCount = 0
            btcCount = 0
            usdCount = 0
        elif row[0] == typeNames[6]:
            holderCount += holders
            btcCount += btcs
            usdCount += usds
            newData.append(["1 ~ 10", holderCount,  btcCount, usdCount, new_timezone_timestamp])
            holderCount = 0
            btcCount = 0
            usdCount = 0
        elif row[0] == typeNames[7]:
            holderCount += holders
            btcCount += btcs
            usdCount += usds
            newData.append(["10 ~ 100", holderCount,  btcCount, usdCount, new_timezone_timestamp])
            holderCount = 0
            btcCount = 0
            usdCount = 0
        elif (row[0] == typeNames[8] or
            row[0] == typeNames[9] or
            row[0] == typeNames[10]):
            holderCount += holders
            btcCount += btcs
            usdCount += usds
        elif row[0] == typeNames[11]:
            holderCount += holders
            btcCount += btcs
            usdCount += usds
            newData.append(["100 up", holderCount,  btcCount, usdCount, new_timezone_timestamp])

    return newData


def getDeltaStr(delta: int):
    if delta >= 0:
        return f"增加 {delta}"
    return f"減少 {-1*delta}"
def getTagretReport(dateData, date):
    # dates = list(data.keys())
    # for date in dates:
    type1DeltaStr = getDeltaStr(round(dateData["0.001 ~ 1"][DataAttr.BTC_DELTA.value],2))
    type2DeltaStr = getDeltaStr(round(dateData["1 ~ 10"][DataAttr.BTC_DELTA.value] + dateData["10 ~ 100"][DataAttr.BTC_DELTA.value], 2))
    type3DeltaStr = getDeltaStr(round(dateData["100 up"][DataAttr.BTC_DELTA.value], 2))
    string = f"""
{date} BTC 持有數量統計
小散戶（0~1）: *{type1DeltaStr}*
散戶（1~100）: *{type2DeltaStr}*
巨鯨 （100+）: *{type3DeltaStr}*
"""
    return string

def report(allData):
    if len(allData) == 0:
        print("illegal data length")
        return

    dates = list(allData.keys())
    dates = dates[::-1]

    for date in dates:
        dateData = allData[date]
        # print(dateData)
        reportString = getTagretReport(dateData, date)
        print(reportString)
        utils.sendMessage(
            settings.CHAT_ID,
            reportString,
            settings.BOT_TOKEN,
        );

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
        "[100 - 1,000)",
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
        
        type = row[0] #[0~0.0001]
        addresses = row[1] #holders
        btc_count = row[2] #btcs
        usd_count = row[3] #usds

        # print(f"{type}| {addresses} | {btc_count} | {usd_count}")

        model.create_bitcoin_info({
            "type": type,
            "holder_count": addresses,
            "serial": latestSerail+1,
            "btc_count": btc_count,
            "usd_count": usd_count
        })
    # report btc state
    data = model.getDataByDaysDesc(1)
    report(data);

if __name__ == '__main__':
    main()