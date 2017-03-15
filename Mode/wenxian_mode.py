import re

import requests
from bs4 import BeautifulSoup

from ..Mode.ModeBase import ModeBase
from ..utils import clean


class Wenxian_mode(ModeBase):
    def __init__(self, wenxian):
        super().__init__()
        self.wenxian=wenxian
        self.wenxianparse=self.wenxian.replace(' ','+')
        self.param={
            'numberOfFields':'0',
            'src':'s',
            'clickedLink':'',
            'edit':'',
            'editSaveSearch':'',
            'origin':'searchbasic',
            'authorTab':'',
            'affiliationTab':'',
            'advancedTab':'',
            'scint':'1',
            'menu':'search',
            'tablin':'',
            'searchterm1':self.wenxianparse,
            'field1':'TITLE_ABS_KEY',
            'dateType':'Publication_Date_Type',
            'yearFrom':'Before+1960',
            'yearTo':'Present',
            'loadDate':'7',
            'documenttype':'All',
            'subjects':'LFSC',
            '_subjects':'on',
            'subjects':'HLSC',
            '_subjects':'on',
            'subjects':'PHSC',
            '_subjects':'on',
            'subjects':'SOSC',
            '_subjects':'on',
            'st1':self.wenxianparse,
            'st2':'',
            'sot':'b',
            'sdt':'b',
            'sl':'101',
            's':'TITLE-ABS-KEY%28'+self.wenxianparse+'%29',
            #'sid':0D8A156F36B35369FE6B68BAAA111169.N5T5nM1aaTEF8rE6yKCR3A%3A150
            #searchId:0D8A156F36B35369FE6B68BAAA111169.N5T5nM1aaTEF8rE6yKCR3A%3A150
            #txGid:0D8A156F36B35369FE6B68BAAA111169.N5T5nM1aaTEF8rE6yKCR3A%3A15
            'sort':'plf-f',
            'originationType':'b',
            'rr':''
        }
        self.param2={
            'numberOfFields':'0',
            'src':'s',
            'clickedLink':'',
            'edit':'',
            'editSaveSearch':'',
            'origin':'searchbasic',
            'authorTab':'',
            'affiliationTab':'',
            'advancedTab':'',
            'scint':'1',
            'menu':'search',
            'tablin':'',
            'searchterm1':self.wenxian,
            'field1':'TITLE_ABS_KEY',
            'dateType':'Publication_Date_Type',
            'yearFrom':'Before 1960',
            'yearTo':'Present',
            'loadDate':'7',
            'documenttype':'All',
            'authSubject':'LFSC',
           '_authSubject':'on',
           'authSubject':'HLSC',
            '_authSubject':'on',
            'authSubject':'PHSC',
            '_authSubject':'on',
            'authSubject':'SOSC',
            '_authSubject':'on',
            'st1':self.wenxian,
            'st2':'',
            'sot':'b',
            'sdt':'b',
            'sl':'101',
            's':'TITLE-ABS-KEY({0})'.format(self.wenxian),
            # sid:558EDC31DD2FC5442E4523A31F75350C.N5T5nM1aaTEF8rE6yKCR3A:70
            # searchId:558EDC31DD2FC5442E4523A31F75350C.N5T5nM1aaTEF8rE6yKCR3A:70
            # txGid:558EDC31DD2FC5442E4523A31F75350C.N5T5nM1aaTEF8rE6yKCR3A:7
            'sort':'plf-f',
            'originationType':'b',
            'rr':''
        }

    def craw(self, idlist=[], file_mode=False, file_mode2=False):
        root = 'https://www.scopus.com/results/results.uri'
        ses = requests.session()  # 创建session
        # self.cookies={'__cfduid':'d25851e7ff514b8fca3046cf9c8e55cf31469085559','utt':'12f10d5fb88565141da3b26-62dc09648ecd1875','SCSessionID':'89D7655856FF963E30499A024D6DA640.wsnAw8kcdt7IPYLO0V48gA','AE_SESSION_COOKIE':'1485352605859','AWSELB':'CB9317D502BF07938DE10C841E762B7A33C19AADB1D367F345B575B860B36AFF56B54637219261F5E15C2FEEF95EED131C17F852F9A31AAC5A6BDE3E4B4DACF34F3854CEEBE8C1C5822DD83DDBA9181889D0AB2B98','AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg':'1','AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg':'-1330315163%7CMCIDTS%7C17191%7CMCMID%7C22529406401721819908362310712924935413%7CMCAID%7CNONE%7CMCAAMLH-1485873910%7C11%7CMCAAMB-1485957409%7Chmk_Lq6TPIBMW925SPhw3Q%7CMCOPTOUT-1485359809s%7CNONE','marketing_textzone_hide':'true','CARS_COOKIE':'005200750057007A006C006B004200550037006100460053006E00480066006D005200440063007400450076002F004B006E007A00590036004800330064006C0044002F0059004B0069006A004D0046006E004E0053003200640073004A0059006D004700680059004E0032004D00490039007800750055005300710077005A00350061003200320050004D00510067006600340046007900590068005000370046006D004F002B0070002F0066006B004C00530066003900410074003200390061006700310073002F004C00590034005600540064006D0047006F0056002F0066006500350059006D00690073003200470051004B0055006D0074007A00770061007A003200420046004400510052007400610041003D','acw':'ca84623f2b5d951d76dc605a30aef2db3352953%7C%24%7C29EB86595308230335B230F5B87F37E44AAFD5DD1AF994FFFFAD856F154D52FFFE590B9B5480D4FC7D5D701E7E780DEA28949BC909738D34634F5D557006E182D5F0091F5D794958CD79BE4EF9F39C806D5EC67CCCB7672623E9E98FE6FC8C1BD74FDB647D9EF3765B1001A3D861E41CE408C9B87FB7286D156AB94AE6A74D7E','scopus.machineID':'53540C70B4380702BB2C6622441E0270.euC1gMODexYlPkQec4u1Q', 'javaScript':'true', 'xmlHttpRequest':'true' ,'s_pers':'%20v8%3D1485353552195%7C1579961552195%3B%20v8_s%3DLess%2520than%25201%2520day%7C1485355352195%3B%20c19%3Dsc%253Asearch%253Adocument%2520searchform%7C1485355352200%3B%20v68%3D1485353551950%7C1485355352209%3B' ,'s_sq':'%5B%5BB%5D%5D', 's_cc':'true', 'screenInfo':'768:1366', 's_sess':'%20v31%3D1485352602941%3B%20s_cpc%3D0%3B%20fn%3Dregistration%253Astart%3B%20c21%3Dtitle-abs-key%2528%2520the%2520characteristics%2520and%2520mechanism%2520of%2520the%2520no%2520formation%2520%2520during%2520oxy-steam%2520combustion%2529%3B%20e13%3Dtitle-abs-key%2528%2520the%2520characteristics%2520and%2520mechanism%2520of%2520the%2520no%2520formation%2520%2520during%2520oxy-steam%2520combustion%2529%253A1%3B%20e41%3D1%3B%20s_ppvl%3Dsc%25253Asearch%25253Adocument%252520searchform%252C60%252C60%252C638%252C1366%252C638%252C1366%252C768%252C1%252CP%3B%20s_ppv%3Dsc%25253Asearch%25253Adocument%252520searchform%252C60%252C60%252C638%252C1366%252C638%252C1366%252C768%252C1%252CP%3B'}
        # cookies = requests.utils.cookiejar_from_dict(self.cookies, cookiejar=None, overwrite=True)
        # ses.cookies = cookies
        # ses.proxies={'https':'http://127.0.0.1:1085'}
        s = ses.get(root, params=self.param2, timeout=60)  # 搜索得到文献列表页面
        soup = BeautifulSoup(s.text, 'html.parser')
        # span=soup.find_all('span',class_='docTitle')
        span = soup.find_all('tr', class_='searchArea')
        if len(span) == 0:
            return None
        elif len(span) == 1:
            link = span[0].a['href']
        else:
            bianhao = 0
            links = []
            mark = 0
            link = ''
            nameoffirst = 'if you see me, no result'
            for spans in span:
                spans = spans.td
                bianhao += 1
                links.append(spans.a['href'])
                biaoti = spans.a.text.strip().replace('\n', '')
                if bianhao == 1:
                    nameoffirst = biaoti  # 存下第一篇的标题，用于文件模式
                # 替换掉可能影响判断的字符
                if clean(biaoti)== clean(self.wenxian):
                    mark = 1
                    link = spans.a['href']
                    break
                if file_mode:
                    continue
                tds=spans.parent.parent.find_all('td')
                zuozhemen = tds[1].span.text.strip().replace('\n', '')
                nian = tds[2].text.strip().replace('\n', '')
                # nian = spans.parent.parent.find('div', class_='dataCol4').span.text.strip().replace('\n', '')
                if tds[3].span.a is None:
                    kan = str(tds[3].span.string).strip().replace('\n', '')
                else:
                    kan = tds[3].span.a.text.strip().replace('\n', '')
                if not file_mode:
                    print('编号：' + str(bianhao) + ' 标题：' + biaoti + ' 作者：' + zuozhemen + ' 年份：' + nian + ' 出版刊物：' + kan)
            if mark == 0:
                if not file_mode:
                    link = links[int(input('输入编号：')) - 1]
                else:
                    print(nameoffirst)
                    link = links[0]  # 都不匹配时，文件模式默认选择第一个
        s2 = ses.get(link)  # 进入文章页面
        # fout = open('output4.html', 'w',encoding="UTF-8")
        # fout.write(s2.text)
        soup2 = BeautifulSoup(s2.text, 'html.parser')
        atitles_list = soup2.find('div', id='authorlist')
        if not atitles_list:
            return None
        atitles=atitles_list.find_all('a', title='Show Author Details')
        sum = 0
        authors = []
        for atitle in atitles:
            authorId = re.findall(r'authorId=\w+&', atitle['href'])[0].replace('authorId=', '').replace('&', '')
            sum += 1
            if authorId not in idlist:
                idlist.append(authorId)
                # print('第'+str(sum)+'作者')
                author= self.crawel(ses, authorId, sum)
                if author:
                    authors.append(author)
        return authors
