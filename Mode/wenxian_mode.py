import re

import requests
from bs4 import BeautifulSoup

import mythread
from Mode.ModeBase import ModeBase
from utils import clean, tocookiedic


class Wenxian_mode(ModeBase):
    def __init__(self, wenxian):
        super().__init__()
        self.wenxian = wenxian
        self.wenxianparse = self.wenxian.replace(' ', '+')
        self.param = {
            'numberOfFields': '0',
            'src': 's',
            'clickedLink': '',
            'edit': '',
            'editSaveSearch': '',
            'origin': 'searchbasic',
            'authorTab': '',
            'affiliationTab': '',
            'advancedTab': '',
            'scint': '1',
            'menu': 'search',
            'tablin': '',
            'searchterm1': self.wenxianparse,
            'field1': 'TITLE_ABS_KEY',
            'dateType': 'Publication_Date_Type',
            'yearFrom': 'Before+1960',
            'yearTo': 'Present',
            'loadDate': '7',
            'documenttype': 'All',
            'subjects': 'LFSC',
            '_subjects': 'on',
            'subjects': 'HLSC',
            '_subjects': 'on',
            'subjects': 'PHSC',
            '_subjects': 'on',
            'subjects': 'SOSC',
            '_subjects': 'on',
            'st1': self.wenxianparse,
            'st2': '',
            'sot': 'b',
            'sdt': 'b',
            'sl': '101',
            's': 'TITLE-ABS-KEY%28' + self.wenxianparse + '%29',
            # 'sid':0D8A156F36B35369FE6B68BAAA111169.N5T5nM1aaTEF8rE6yKCR3A%3A150
            # searchId:0D8A156F36B35369FE6B68BAAA111169.N5T5nM1aaTEF8rE6yKCR3A%3A150
            # txGid:0D8A156F36B35369FE6B68BAAA111169.N5T5nM1aaTEF8rE6yKCR3A%3A15
            'sort': 'plf-f',
            'originationType': 'b',
            'rr': ''
        }
        self.param2 = {
            'numberOfFields': '0',
            'src': 's',
            'clickedLink': '',
            'edit': '',
            'editSaveSearch': '',
            'origin': 'searchbasic',
            'authorTab': '',
            'affiliationTab': '',
            'advancedTab': '',
            'scint': '1',
            'menu': 'search',
            'tablin': '',
            'searchterm1': self.wenxian,
            'field1': 'TITLE_ABS_KEY',
            'dateType': 'Publication_Date_Type',
            'yearFrom': 'Before 1960',
            'yearTo': 'Present',
            'loadDate': '7',
            'documenttype': 'All',
            'authSubject': 'LFSC',
            '_authSubject': 'on',
            'authSubject': 'HLSC',
            '_authSubject': 'on',
            'authSubject': 'PHSC',
            '_authSubject': 'on',
            'authSubject': 'SOSC',
            '_authSubject': 'on',
            'st1': self.wenxian,
            'st2': '',
            'sot': 'b',
            'sdt': 'b',
            'sl': '101',
            's': 'TITLE-ABS-KEY({0})'.format(self.wenxian),
            # sid:558EDC31DD2FC5442E4523A31F75350C.N5T5nM1aaTEF8rE6yKCR3A:70
            # searchId:558EDC31DD2FC5442E4523A31F75350C.N5T5nM1aaTEF8rE6yKCR3A:70
            # txGid:558EDC31DD2FC5442E4523A31F75350C.N5T5nM1aaTEF8rE6yKCR3A:7
            'sort': 'plf-f',
            'originationType': 'b',
            'rr': ''
        }

    def craw(self, idlist=[], file_mode=False, file_mode2=False):
        root = 'https://www.scopus.com/results/results.uri'
        ses = requests.session()  # 创建session
        # headers='''
        # Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
        # Accept-Encoding:gzip, deflate, sdch, br
        # Accept-Language:zh-CN,zh;q=0.8
        # Cache-Control:max-age=0
        # Connection:keep-alive
        # Cookie:utt=ae21-d89e895055169e22533-0ee84fefcf1d1f09; s_fid=50E6C347250E5AAC-0C139AB0C53B3132; s_lv=1467013717155; s_vi=[CS]v1|2BA69D8C0548862A-60000105C00B6D33[CE]; marketing_textzone_hide=true; sc_overlay_ok=showOverlay_false&ts_2016-12-20T05%3A20%3A16.547; __cfduid=d7cc15e0d48e31d622824bd0af04103cc1496844233; optimizelyEndUserId=oeu1496849785123r0.8224328470025604; optimizelySegments=%7B%22278797888%22%3A%22gc%22%2C%22278846372%22%3A%22false%22%2C%22278899136%22%3A%22none%22%2C%22278903113%22%3A%22direct%22%7D; optimizelyBuckets=%7B%7D; AE_SESSION_COOKIE=1497190047791; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; SCSessionID=92AC087B1D5BB63D99FD19E73EC9A9D2.wsnAw8kcdt7IPYLO0V48gA; AWSELB=CB9317D502BF07938DE10C841E762B7A33C19AADB1DC7D5C89B508CAFB88E936E3D49AEF440C264AF841A42CAF414BCE0A6CD0233CA31AAC5A6BDE3E4B4DACF34F3854CEEBDD31F6E276AFE36C0A317364D95D35C0; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=2096510701%7CMCAID%7C2BA69D8C0548862A-60000105C00B6D33%7CMCIDTS%7C17331%7CMCMID%7C44958662928378730373928888510574225296%7CMCAAMLH-1497448988%7C11%7CMCAAMB-1497938852%7CNRX38WO0n5BH8Th-nqAG_A%7CMCOPTOUT-1497341252s%7CNONE%7CMCSYNCSOP%7C411-17332%7CvVersion%7C2.0.0; CARS_COOKIE=00630079003600670030005600720031003700540033006C004700370059004E0078003900790045005500360032002F00330030005800660076007100660043007900680043007000300077007700380033004B005900480072007A00560037006E00520065004700380050004600310071006A0072006600350042006E0034006900390055004B003300630066006D0032007A004E006C00380049004800730072004B00530045006800710066005600530062004400630047003300660045005100580070004E006C00610032006D00610065006A006100620046006E003400360045003300320079004700610054006A007400620065002F007800390051006500380068004C00370054006E0074004500300067003D; homeAcc_cookie=0045004F006E00720071005500380073006E004A006C0035006500320062004E00440050005900710056006B004E004E006C003300390037005A0045004A004D00680063005A0032004D00700064005000520067004E004C003400770063005000320058004F004A00550051003D003D; s_sq=%5B%5BB%5D%5D; acw=a8e61aed25c77040a739fa79e34860cf67f0gxrqa%7C%24%7CF5C1A58DEAFB042B5C329B60F92386A8C5BC5AFF6370414C613B6FD50E33357BFFA1C4AFDF85601A032E026EEF5C60E57060D15B77680BB35B2791389D9DC89EE755B001AF5A0858787A139BC1C55061; _pendo_meta.7108b796-60e0-44bd-6a6b-7313c4a99c35=1065226270; scopus.machineID=1562093D14B3F7F895202A912E66D61E.wsnAw8kcdt7IPYLO0V48gA; javaScript=true; xmlHttpRequest=true; s_cc=true; screenInfo=820:1024; _pendo_visitorId.7108b796-60e0-44bd-6a6b-7313c4a99c35=ae%3A20783356; _pendo_accountId.7108b796-60e0-44bd-6a6b-7313c4a99c35=ae%3A378034; s_pers=%20c19%3Dsc%253Asearch%253Adocument%2520searchform%7C1497336253417%3B%20v68%3D1497334453181%7C1497336253422%3B%20v8%3D1497334454390%7C1591942454390%3B%20v8_s%3DLess%2520than%25207%2520days%7C1497336254390%3B; s_sess=%20v31%3D1497190047200%3B%20s_cpc%3D0%3B%20e41%3D1%3B%20s_ppvl%3Dsc%25253Asearch%25253Adocument%252520searchform%252C66%252C66%252C691%252C1024%252C691%252C1024%252C820%252C1.25%252CP%3B%20s_ppv%3Dsc%25253Asearch%25253Adocument%252520searchform%252C66%252C66%252C691%252C1024%252C222%252C1024%252C820%252C1.25%252CP%3B
        # Host:www.scopus.com
        # Upgrade-Insecure-Requests:1
        # User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36
        # '''
        # self.useragent='Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        # self.AcceptLanguage='zh-CN,zh;q=0.8'
        # self.Accept='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        # ses.headers={'User-Agent':self.useragent,'Accept-Language':self.AcceptLanguage,'Accept':self.Accept}
        cookiestring='utt=12f10d5fb88565141da3b26-62dc09648ecd1875; marketing_textzone_hide=true; __cfduid=d4124864107ac58c69990d54e262635881500624563; optimizelyEndUserId=oeu1501512825922r0.2211416650696938; SCSessionID=6012A37031CBD44332A14F6F713F34D0.wsnAw8kcdt7IPYLO0V48gA; AE_SESSION_COOKIE=1505177031713; AWSELB=CB9317D502BF07938DE10C841E762B7A33C19AADB1AF3D5952640032C1A896CCAB339470CF2A7F70288AC3AC9656065CBC720053648278FC278415EC1A7924B82E83258A30B103D75FB24F8BCF7D5D1EDD1BDD573B; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=2096510701%7CMCIDTS%7C17421%7CMCMID%7C22529406401721819908362310712924935413%7CMCAID%7CNONE%7CMCAAMLH-1505733891%7C11%7CMCAAMB-1505781831%7Chmk_Lq6TPIBMW925SPhw3Q%7CMCOPTOUT-1505184231s%7CNONE%7CMCSYNCSOP%7C411-17428%7CvVersion%7C2.0.0; CARS_COOKIE=003200780049007A0044004A0058005A006500700075004B004C0056003900610034006A007400570048002F0078003000730054006C0070004F0059006400620034007300490048005000700064004A0050007900440064004E006A0041002B003600420038004B00790061003200580074006800580075007300710078007800370049002B0034006A006200570076004E0053007A00760063002F006B00630074006C0074002F00360047007A0042003500660035005400760047005A0030006E006B004700420035002F0049006B00450067003800360068004E0041005500460057006F002B0065006E002F0072004F0053006C007700500065004500520053002B004D004800440039006C007A006900560045003D; homeAcc_cookie=0045004F006E00720071005500380073006E004A006E00650063003800500041003900380072004C006C0047003100530032006B0036002F0068005500710063006F004800500036007A003400790036002B0055005A004C003400770063005000320058004F004A00550051003D003D; acw=87a3e0ce6747f14c273a32f0cdd4d3a0541bgxrqa%7C%24%7C8D6B7050F3AC86A39A2AFE48C92BA2019EF0F12F7FF4C4B82E81961FCD8565BE569642EC8051D829CF5C612AA87C806737AB0C95311748393FBA44D1BD4E4F2EAFE9C31A29ED2080B6DA1F7CB1786ABB; s_sq=%5B%5BB%5D%5D; _pendo_meta.7108b796-60e0-44bd-6a6b-7313c4a99c35=1953853408; scopus.machineID=53540C70B4380702BB2C6622441E0270.euC1gMODexYlPkQec4u1Q; javaScript=true; optimizelySegments=%7B%22278797888%22%3A%22gc%22%2C%22278846372%22%3A%22false%22%2C%22278899136%22%3A%22none%22%2C%22278903113%22%3A%22direct%22%7D; optimizelyBuckets=%7B%7D; optimizelyPendingLogEvents=%5B%5D; xmlHttpRequest=true; s_pers=%20v8%3D1505177043241%7C1599785043241%3B%20v8_s%3DLess%2520than%25201%2520day%7C1505178843241%3B%20c19%3Dsc%253Asearch%253Adocument%2520searchform%7C1505178843247%3B%20v68%3D1505177042702%7C1505178843258%3B; s_cc=true; screenInfo=768:1366; _pendo_visitorId.7108b796-60e0-44bd-6a6b-7313c4a99c35=_PENDO_T_G979BpyWeUk; _pendo_accountId.7108b796-60e0-44bd-6a6b-7313c4a99c35=ae%3A53666; s_sess=%20v31%3D1505177030277%3B%20s_cpc%3D0%3B%20e41%3D1%3B%20s_ppvl%3Dsc%25253Asearch%25253Adocument%252520searchform%252C58%252C58%252C638%252C1366%252C638%252C1366%252C768%252C1%252CP%3B%20s_ppv%3Dsc%25253Asearch%25253Adocument%252520searchform%252C100%252C58%252C1573%252C1170%252C1573%252C410%252C551%252C2%252CL%3B'
        self.cookies=tocookiedic(cookiestring)
        cookies = requests.utils.cookiejar_from_dict(self.cookies, cookiejar=None, overwrite=True)
        # ses.cookies = cookies
        # ses.proxies={'https':'http://127.0.0.1:1085'}
        s = ses.get(root, params=self.param2, timeout=60)  # 搜索得到文献列表页面
        # fout = open('output3.html', 'w',encoding="UTF-8")
        # fout.write(s.text)
        soup = BeautifulSoup(s.text, 'html.parser')
        span = soup.find_all('span', class_='docTitle')
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
                if clean(biaoti) == clean(self.wenxian):
                    mark = 1
                    link = spans.a['href']
                    break
                if file_mode:
                    continue
                tds = spans.parent.parent.find_all('td')
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
        authors = self.parser.GetAuthorsdromLink(ses, link, idlist)
        return authors
