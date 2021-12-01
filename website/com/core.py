import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from comm.webio import Get


class IPO(Get):
    @property
    def url(self):
        return "http://www.38.co.kr/html/fund/?o=kn"

class IPO_SCHEDULE(IPO):
    
    def fetch(self):
        """
        :return:
        """
        result = self.read()
        return result.text

if __name__ == "__main__":
    r = IPO_SCHEDULE().fetch()
    print(r)
