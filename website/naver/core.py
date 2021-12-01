import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from comm.webio import Get


class NaverWebIo(Get):
    @property
    def url(self):
        return "http://fchart.stock.naver.com/sise.nhn"

class Sise(NaverWebIo):
    @property
    def uri(self):
        return "/sise.nhn"

    def fetch(self, ticker, count, timeframe='day'):
        """
        :param ticker:
        :param count:
        :param timeframe: day/week/month
        :return:
        """
        result = self.read(symbol=ticker, timeframe=timeframe, count=count, requestType="0")
        return result.text

#포괄적인 주가정보
class NaverWebIo1(Get):
    @property
    def url(self):
        return "https://finance.naver.com/item/main.naver"

#금리
class NaverWebIo2(Get):
    @property
    def url(self):
        return "https://finance.naver.com/marketindex/"

#환율
class NaverWebIo3(Get):
    @property
    def url(self):
        return "https://finance.naver.com/marketindex/exchangeList.naver"


class Info(NaverWebIo1):

    def fetch(self, ticker):
        """
        :param ticker:
        :return:
        """
        result = self.read(code = ticker)
        return result.text

class MarketIndex(NaverWebIo2):
    
    def fetch(self):
        """
        :return:
        """
        result = self.read()
        return result.text

class ExchangeList(NaverWebIo3):
    
    def fetch(self):
        """
        :return:
        """
        result = self.read()
        return result.text

if __name__ == "__main__":
    r = Sise().fetch("006800", 10, "week")
    print(r)
