import re

import requests
from bs4 import BeautifulSoup

import mythread
from utils import printresult


class HtmlParser():
    def GetAuthorId(self, s):
        def Getid(spannode):
            authorId = re.findall(r'authorId=\w+&', spannode.a['href'])[0].replace('authorId=', '').replace('&', '')
            return authorId

        soup = BeautifulSoup(s.text, 'html.parser')
        span = soup.find_all('span', class_='docTitle')
        if len(span) == 0:
            return None
        if len(span) == 1:
            authorId = Getid(span[0])
            return authorId
        # 输出找到的所有人,选择。
        # 这一块暂时未改动成api
        if len(span) > 1:
            bianhao = 0
            for spans in span:
                bianhao += 1
                name = spans.a.text
                fathernode = spans.parent.parent.parent
                danwei = fathernode.find('div', class_='dataCol5').text.replace('\n', '')
                diqu = fathernode.find('div', class_='dataCol6').text.replace('\n', '')
                country = fathernode.find('div', class_='dataCol7').text.replace('\n', '')
                fangxiang = fathernode.find('div', class_='dataCol4').text.replace('\n', '').strip()
                print('编号：' + str(bianhao) + ' 姓名：' + name + ' 单位：' + danwei + ' 地区：' + diqu + ' 国家：' + country)
                print('方向：' + fangxiang)
                if bianhao >= 10:
                    break
            i = input('输入选择的编号：').strip()
            return Getid(span[int(i) - 1])

    def GetAuthorMessage(self, s2):
        # fout = open('output2.html', 'w',encoding="UTF-8")
        # fout.write(s2.text)
        # soup2 = BeautifulSoup(s2.text, 'html.parser')
        # soup2=BeautifulSoup(open('output.html','r',encoding="UTF-8"),'html.parser')
        soup2 = BeautifulSoup(s2.text, 'html.parser')
        namesec = soup2.find_all('div', class_='nameSection')
        if not namesec:
            return None
        span2 = namesec[0].find_all('div', class_='authAffilcityCounty')
        namejihe = namesec[0].h1.text.replace(namesec[0].h1.span.text, '').replace('\n', '').split(',')
        name = namejihe[-1].strip() + ' ' + namejihe[0]
        WenxinNum = soup2.find('a', id='docCntLnk').text.strip()
        area = str(span2[0].text).replace('\n', ' ').strip()

        lishi = soup2.find('div', class_='hisPubyear').text.replace('\n', '').strip()

        ArticlesLink = soup2.find_all('div', class_='authorResultsOptionalLinks')[0].a['href']
        return WenxinNum, name, area, ArticlesLink, lishi

    def GetArticles(self, s3):
        # fout2 = open('output2.html', 'w',encoding="UTF-8")
        # fout2.write(s3.text)
        # soup3=BeautifulSoup(open('output2.html','r',encoding="UTF-8"), 'html.parser',from_encoding="UTF-8")
        soup3 = BeautifulSoup(s3.text, 'html.parser')
        # spanarticle=soup3.find_all('span',class_='docTitle')
        spanarticle = soup3.find_all('tr', class_='searchArea')
        list = []
        for article in spanarticle:
            article = article.find_all('td')[0]
            linka = article.a['href']
            # 得到年份
            # 节点变动
            nian = article.parent.parent.find_all('td')[2].text.replace('\n', '')
            # nian=article.parent.parent.find('div',class_='dataCol4').span.text.replace('\n','')
            list.append([linka, nian])
        return list

    def GetEmail(self, s4):
        # fout3 = open('output3.html', 'w',encoding="UTF-8")
        # fout3.write(s4.text)
        # soup4=BeautifulSoup(open('output3.html','r',encoding="UTF-8"), 'html.parser',from_encoding="UTF-8")
        soup4 = BeautifulSoup(s4.text, 'html.parser')
        highlight = soup4.find_all('span', class_='ScopusTermHighlight')
        if not highlight:
            highlight = soup4.find_all('span', class_='bg-primary')
        # 解析名字缩写
        if not highlight:
            return None, None
        a = highlight[0].text.split(',')
        a.reverse()
        suoxie = ' '.join([i.strip() for i in a])
        # print("缩写："+suoxie)
        # 节点变动
        node = highlight[0].parent.parent.parent
        emailnotparse = node.find('a', class_='correspondenceEmail')
        if emailnotparse:
            if node.find_all('li'):
                raise Exception('邮箱节点出错')
        return emailnotparse, suoxie

    def GetAuthorsdromLink(self, ses, link, idlist):
        s2 = ses.get(link)  # 进入文章页面
        # fout = open('output4.html', 'w',encoding="UTF-8")
        # fout.write(s2.text)
        soup2 = BeautifulSoup(s2.text, 'html.parser')
        atitles_list = soup2.find('section', id='authorlist')
        if not atitles_list:
            return None
        atitles = atitles_list.find_all('a', title='Show Author Details')
        if not atitles:
            atitles = atitles_list.find_all('a', title='显示作者详情')
        sum = 0
        authors = []
        threads = []
        for atitle in atitles:
            authorId = re.findall(r'authorId=\w+&', atitle['href'])[0].replace('authorId=', '').replace('&', '')
            sum += 1
            if authorId not in idlist:
                idlist.append(authorId)
                # print('第'+str(sum)+'作者')
                try:
                    t = mythread.MyThread(ses, authorId, sum)
                    threads.append(t)
                # author=t.get_result()
                #     # author= self.crawel(ses, authorId, sum)
                except requests.exceptions.ReadTimeout:
                    continue
                    # if author:
                    #     authors.append(author)

        for t in threads:
            try:
                t.setDaemon(True)
                t.start()
                # author= self.crawel(ses, authorId, sum)
            except requests.exceptions.ReadTimeout:
                continue
        for t in threads:
            t.join()
        for t in threads:
            author = t.get_result()
            if author:
                printresult(author)
                authors.append(author)
        return authors
