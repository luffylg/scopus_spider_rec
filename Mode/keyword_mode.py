import re
import requests
from bs4 import BeautifulSoup

from Mode.wenxian_mode import Wenxian_mode
from utils import printresult


class Keyword_mode(Wenxian_mode):
    def craw(self, idlist=[], file_mode=False, file_mode2=False):
        root = 'https://www.scopus.com/results/results.uri'
        ses = requests.session()  # 创建session
        # ses.proxies={'https':'http://127.0.0.1:1085'}
        s = ses.get(root, params=self.param2, timeout=60)  # 搜索得到文献列表页面
        soup = BeautifulSoup(s.text, 'html.parser')
        # span=soup.find_all('span',class_='docTitle')
        span = soup.find_all('tr', class_='searchArea')
        if len(span) == 0:
            print("找不到文献")
            return None
        else:
            authors = []
            atitles = []
            for spans in span:
                biaoti = spans.a.text.strip().replace('\n', '')
                print(biaoti)
                spans = spans.td
                link = spans.a['href']
                some_authors = self.parser.GetAuthorsdromLink(ses, link, idlist)
                if not some_authors:
                    continue
                authors.extend(some_authors)
        return authors
