import re

import requests
from bs4 import BeautifulSoup

import mythread
from Mode.ModeBase import ModeBase
from utils import clean


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
        # self.useragent='Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        # self.AcceptLanguage='zh-CN,zh;q=0.8'
        # self.Accept='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        # ses.headers={'User-Agent':self.useragent,'Accept-Language':self.AcceptLanguage,'Accept':self.Accept}
        self.cookies={'utt':'ae21-d89e895055169e22533-0ee84fefcf1d1f09','s_fid':'50E6C347250E5AAC-0C139AB0C53B3132','s_lv':'1467013717155','s_vi':'[CS]v1|2BA69D8C0548862A-60000105C00B6D33[CE]','marketing_textzone_hide':'true','sc_overlay_ok':'showOverlay_false&ts_2016-12-20T05%3A20%3A16.547','AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg':'1','__cfduid':'d7cc15e0d48e31d622824bd0af04103cc1496844233','AUTH_TOKEN_COOKIE':'53476e4a4868744a326a383d','AE_SESSION_COOKIE':'1496844237706','AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg':'2096510701%7CMCAID%7C2BA69D8C0548862A-60000105C00B6D33%7CMCIDTS%7C17325%7CMCMID%7C44958662928378730373928888510574225296%7CMCAAMLH-1497448988%7C11%7CMCAAMB-1497448988%7CNRX38WO0n5BH8Th-nqAG_A%7CMCOPTOUT-1496851388s%7CNONE%7CMCSYNCSOP%7C411-17332%7CvVersion%7C2.0.0','SCSessionID':'CF48EFA2A9F3BA643C6B1CA75E50DE1D.wsnAw8kcdt7IPYLO0V48gA','AWSELB':'CB9317D502BF07938DE10C841E762B7A33C19AADB1E385A4AB5EDB223EF6A16D7ACDA1FDF2693A2E48656F90DA014122D2781180E2A31AAC5A6BDE3E4B4DACF34F3854CEEB9BA32B6009E144A216C8C33143191020','CARS_COOKIE':'00630079003600670030005600720031003700540033006C004700370059004E0078003900790045005500360032002F00330030005800660076007100660043007900680043007000300077007700380033004B005900480072007A00560037006E00520065004700380050004600310071006A0072006600350042006E0034006900390055004B003300630066006D0032007A004E006C00380049004800730072004B00530045006800710066005600530062004400630047003300660045005100580070004E006C00610032006D00610065006A006100620046006E003400360045003300320079004700610054006A007400620065002F007800390051006500380068004C00370054006E0074004500300067003D','homeAcc_cookie':'0045004F006E00720071005500380073006E004A006C0035006500320062004E00440050005900710056006B004E004E006C003300390037005A0045004A004D00680063005A0032004D00700064005000520067004E004C003400770063005000320058004F004A00550051003D003D','acw':'db8798e28f23d54b8e1a7a416fdd74465e85gxrqa%7C%24%7CECBEE8912148BF5253B92465830A4DC09821B4B77BA73763B7687F01E3EA1C26826E91DEB23EE816A91AD84A6DB7E0C0A5FAEA8555C952265B2791389D9DC89EA22D525A2BDF1584903695140E8C179EA122676CBE98E60C10B1D490FCC5DDB2','s_sq':'%5B%5BB%5D%5D','screenInfo':'820:1024','_pendo_meta.7108b796-60e0-44bd-6a6b-7313c4a99c35':'3947206600','_pendo_visitorId.7108b796-60e0-44bd-6a6b-7313c4a99c35':'ae%3A20783356','_pendo_accountId.7108b796-60e0-44bd-6a6b-7313c4a99c35':'ae%3A53666','scopus.machineID':'1562093D14B3F7F895202A912E66D61E.wsnAw8kcdt7IPYLO0V48gA','javaScript':'true','xmlHttpRequest':'true','s_pers':'%20v8%3D1496848481616%7C1591456481616%3B%20v8_s%3DLess%2520than%25201%2520day%7C1496850281616%3B%20c19%3Dsc%253Asearch%253Adocument%2520searchform%7C1496850281618%3B%20v68%3D1496848481319%7C1496850281628%3B','s_cc':'true','s_sess':'%20v31%3D1495463577844%3B%20s_cpc%3D0%3B%20c21%3Dtitle-abs-key%2528investigation%2520of%2520the%2520ballistic%2520performance%2520of%2520ultra%2520high%2520molecular%2520weight%2520polyethylene%2520composite%2520panels%2529%3B%20e13%3Dtitle-abs-key%2528investigation%2520of%2520the%2520ballistic%2520performance%2520of%2520ultra%2520high%2520molecular%2520weight%2520polyethylene%2520composite%2520panels%2529%253A1%3B%20s_ppvl%3Dsc%25253Asearch%25253Adocument%252520searchform%252C51%252C50%252C811%252C1024%252C691%252C1024%252C820%252C1.25%252CP%3B%20e41%3D1%3B%20s_ppv%3Dsc%25253Asearch%25253Adocument%252520searchform%252C51%252C51%252C811%252C1024%252C162%252C1024%252C820%252C1.25%252CP%3B'}
        cookies = requests.utils.cookiejar_from_dict(self.cookies, cookiejar=None, overwrite=True)
        ses.cookies = cookies
        # ses.proxies={'https':'http://127.0.0.1:1085'}
        s = ses.get(root, params=self.param2, timeout=60)  # 搜索得到文献列表页面
        # fout = open('output3.html', 'w',encoding="UTF-8")
        # fout.write(s.text)
        soup = BeautifulSoup(s.text, 'html.parser')
        span=soup.find_all('span',class_='docTitle')
        if not span:
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
        atitles_list = soup2.find('section', id='authorlist')
        if not atitles_list:
            return None
        atitles=atitles_list.find_all('a', title='Show Author Details')
        if not atitles:
            atitles=atitles_list.find_all('a', title='显示作者详情')
        sum = 0
        authors = []
        threads=[]
        for atitle in atitles:
            authorId = re.findall(r'authorId=\w+&', atitle['href'])[0].replace('authorId=', '').replace('&', '')
            sum += 1
            if authorId not in idlist:
                idlist.append(authorId)
                # print('第'+str(sum)+'作者')
                try:
                    t=mythread.MyThread(ses, authorId, sum)
                    threads.append(t)
                #     author=t.get_result()
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
                authors.append(author)
        return authors
