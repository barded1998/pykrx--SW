import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from com.core import IPO_SCHEDULE
import xml.etree.ElementTree as et
from pandas import DataFrame, Series
import pandas as pd
import numpy as np
from datetime import datetime
from bs4 import BeautifulSoup

def replace_blank(string: str) -> str:
    characters = "\n\t "
    for x in range(len(characters)):
        string = string.replace(characters[x], "")
    l = "l"
    for x in range(len(characters)):
        string = string.replace(l, " | ")
    return string

def get_ipo_schedule():

    html = IPO_SCHEDULE().fetch()
    soup = BeautifulSoup(html, 'html.parser')
    ipo_schedule = soup.find('table', {'summary': '공모주 청약일정'})

    # column 리스트
    thead = ipo_schedule.find('thead')
    column = thead.find_all('th')
    columnList = []
    for i in range(0, len(column)):
        th = (replace_blank(column[i].text))
        columnList.append(th)

    tbody = ipo_schedule.find('tbody')

    #종목
    td = tbody.find_all('td')

    stockList = []
    scheduleListStart = []
    scheduleListEnd = []
    ipo_price1 = []
    ipo_price2 = []
    comp_rate = []
    manager = []
    analysis = []

    for i in range(0, len(td)):
        d = replace_blank(td[i].text)
        if i % 7 == 0:
            stockList.append(d)
        elif i % 7 == 1:
            date = d.split("~")
            startDate = datetime.strptime(date[0], '%Y.%m.%d')
            endDate = datetime.strptime((str(startDate.year) + date[1]), '%Y%m.%d')
            scheduleListStart.append(startDate)
            scheduleListEnd.append(endDate)
        elif i % 7 == 2:
            ipo_price1.append(d)
        elif i % 7 == 3:
            ipo_price2.append(d)
        elif i % 7 == 4:
            comp_rate.append(d)
        elif i % 7 == 5:
            manager.append(d)
        elif i % 7 == 6:
            analysis.append(d)
    
    df = DataFrame({columnList[0] : stockList, " 시작일" : scheduleListStart , " 종료일" : scheduleListEnd, columnList[2] : ipo_price1,columnList[3] : ipo_price2,columnList[4] : comp_rate,columnList[5] : manager})
    return df

if __name__ == "__main__":
    print(get_ipo_schedule())