import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from naver.core import *
import xml.etree.ElementTree as et
from pandas import DataFrame, Series
import pandas as pd
import numpy as np
from datetime import datetime
from bs4 import BeautifulSoup

# fromdate, todate, isin
def get_market_ohlcv_by_date(fromdate, todate, ticker):
    strtd = datetime.strptime(fromdate, '%Y%m%d')
    lastd = datetime.strptime(todate, '%Y%m%d')
    today = datetime.now()
    elapsed = today - strtd
    xml = Sise().fetch(ticker, elapsed.days)

    result = []
    try:
        for node in et.fromstring(xml).iter(tag='item'):
            row = node.get('data')
            result.append(row.split("|"))

        cols = ['날짜', '시가', '고가', '저가', '종가', '거래량']
        df = DataFrame(result, columns=cols)
        df = df.set_index('날짜')
        df.index = pd.to_datetime(df.index, format='%Y%m%d')
        df = df.astype(np.int32)
        return df.loc[(strtd <= df.index) & (df.index <= lastd)]
    except et.ParseError:
        return DataFrame()

#빈칸을 없애는 함수
def replace_blank(string: str) -> str:
    characters = "\n\t "
    for x in range(len(characters)):
        string = string.replace(characters[x], "")
    l = "l"
    for x in range(len(characters)):
        string = string.replace(l, " | ")
    return string
    
#
def get_invest_info(ticker: str):

    html = Info().fetch(ticker)
    soup = BeautifulSoup(html, 'html.parser')
    marketInfo = soup.find('div', {'id': 'tab_con1'})

    index = marketInfo.find_all('th')
    indexList = []

    for i in range(0, len(index)):
        th = (replace_blank(index[i].text))
        indexList.append(th)

    indexList[6] = '외국인소진율(B/A)'
    indexList[9] = 'PER | EPS'
    indexList[10] = '추정PER | EPS'
    indexList[11] = 'PBR | BPS'
    indexList[12] = '배당수익률'

    value = marketInfo.find_all('td')
    valueList = []
    for i in range(0, len(value)):
        td = (replace_blank(value[i].text))
        valueList.append(td)

    series = Series(valueList, indexList)
    return series

def get_market_index():

    html = MarketIndex().fetch()
    soup = BeautifulSoup(html, 'html.parser')
    interestInfo = soup.find('table', {'summary': '국제시장 환율 리스트'})

    thead = interestInfo.find('thead')
    column = thead.find_all('th')
    columnList = []
    for i in range(0, len(column)):
        th = (replace_blank(column[i].text))
        columnList.append(th)

    typeList = []
    interestList =[]
    fluctuationList = []

    tbody = interestInfo.find('tbody')
    th = tbody.find_all('th')

    for i in range(0, len(th)):
        t = (replace_blank(th[i].text))
        typeList.append(t)

    td = tbody.find_all('td')

    for i in range(0, len(td)):
      if i % 2 == 0:
          interestList.append(replace_blank(td[i].text))
      else :
          fluctuationList.append(replace_blank(td[i].text))
    return DataFrame({columnList[0] : typeList, columnList[1] : interestList,columnList[2] : fluctuationList})
  
def get_exchange_list():

    html = ExchangeList().fetch()
    soup = BeautifulSoup(html, 'html.parser')
    marketInfo = soup.find('table', {'summary': '환전 고시 환율 리스트'})

    tbody = marketInfo.find('tbody')
    currency = tbody.find_all('td', {'class':'tit'})
    currencyList = []
    for i in range(0, len(currency)):
        th = (replace_blank(currency[i].text))
        currencyList.append(th)

    sale = tbody.find_all('td', {'class':'sale'})
    saleList = []
    for i in range(0, len(sale)):
        s = (replace_blank(sale[i].text))
        saleList.append(s)
    
    rateByDollar = []
    dollar = tbody.find_all('td')
    for i in range(0, len(dollar)):
        if i % 7 == 6 :
            rateByDollar.append(replace_blank(dollar[i].text))
    return DataFrame({"통화명" : currencyList, "매매기준율": saleList, "미화환산율" : rateByDollar})

if __name__ == "__main__":
    print(get_invest_info("005930"))
    print(get_exchange_list())
    print(get_market_index())