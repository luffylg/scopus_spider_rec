import re


def tocookiedic(cookiestring):
    lis = cookiestring.split('; ')
    res = {}
    for items in lis:
        itm = items.split('=')
        res[itm[0]] = itm[1]
    return res


def seperatename(namelist):
    # 获取姓和名
    namelist.reverse()
    name = ' '.join([i.strip() for i in namelist])
    namelists = name.strip().split()
    xing = namelists[-1]
    namelists.pop()
    ming = " ".join(namelists)
    return xing, ming


def strip_email_protection(s):
    # 解密邮件地址
    fp = re.findall(r'email-protection#[A-Za-z0-9]+', s)
    # parse email
    fp = fp[0].replace('email-protection#', '')
    # print(fp)

    r = int(fp[:2], 16)
    email = ''.join([chr(int(fp[i:i + 2], 16) ^ r) for i in range(2, len(fp), 2)])
    # m = re.sub(r'<a class="__cf_email__".*?</a>', email, s)
    # #strip <script>
    # m = re.sub('<script.*?</script>', '', s, flags = re.DOTALL)
    return email


def clean(s):
    return s.lower().replace(' ', '').replace('.', '').replace(',', '').replace('-', '')


def printresult(result):
    if result['bianhao'] != 0:
        print('第' + str(result['bianhao']) + '作者')
    print('文献数：' + result['wenxin'] + ' ' + result['lishi'])
    print(result['AuthorName'])
    print("缩写：" + result['suoxie'])
    print(result['area'])
    print(result['email'])
    print('年份: ' + result['nian'] + '\n')


def writefile(out, result):
    out.write('文献数：' + result['wenxin'] + ' ' + result['lishi'] + '\n')
    out.write(result['AuthorName'] + '\n')
    out.write("缩写：" + result['suoxie'] + '\n')
    out.write(result['area'] + '\n')
    out.write(result['email'] + '\n')
    out.write('年份: ' + result['nian'] + '\n')


def infilter(author, message):
    message=message+';serbia;Malaysia;Algeria;iran;india'
    if not message:
        return False
    filte = re.compile(r';|；').split(message)
    for s in filte:
        if not s:
            continue
        if s.lower().strip() in author['area'].lower():
            return True
    return False


if __name__ == '__main__':
    print(tocookiedic(
        'utt=ae21-d89e895055169e22533-0ee84fefcf1d1f09; s_fid=50E6C347250E5AAC-0C139AB0C53B3132; s_lv=1467013717155; s_vi=[CS]v1|2BA69D8C0548862A-60000105C00B6D33[CE]; marketing_textzone_hide=true; sc_overlay_ok=showOverlay_false&ts_2016-12-20T05%3A20%3A16.547; __cfduid=d7cc15e0d48e31d622824bd0af04103cc1496844233; optimizelyEndUserId=oeu1496849785123r0.8224328470025604; optimizelySegments=%7B%22278797888%22%3A%22gc%22%2C%22278846372%22%3A%22false%22%2C%22278899136%22%3A%22none%22%2C%22278903113%22%3A%22direct%22%7D; optimizelyBuckets=%7B%7D; AE_SESSION_COOKIE=1497190047791; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; SCSessionID=92AC087B1D5BB63D99FD19E73EC9A9D2.wsnAw8kcdt7IPYLO0V48gA; AWSELB=CB9317D502BF07938DE10C841E762B7A33C19AADB1DC7D5C89B508CAFB88E936E3D49AEF440C264AF841A42CAF414BCE0A6CD0233CA31AAC5A6BDE3E4B4DACF34F3854CEEBDD31F6E276AFE36C0A317364D95D35C0; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=2096510701%7CMCAID%7C2BA69D8C0548862A-60000105C00B6D33%7CMCIDTS%7C17331%7CMCMID%7C44958662928378730373928888510574225296%7CMCAAMLH-1497448988%7C11%7CMCAAMB-1497938852%7CNRX38WO0n5BH8Th-nqAG_A%7CMCOPTOUT-1497341252s%7CNONE%7CMCSYNCSOP%7C411-17332%7CvVersion%7C2.0.0; CARS_COOKIE=00630079003600670030005600720031003700540033006C004700370059004E0078003900790045005500360032002F00330030005800660076007100660043007900680043007000300077007700380033004B005900480072007A00560037006E00520065004700380050004600310071006A0072006600350042006E0034006900390055004B003300630066006D0032007A004E006C00380049004800730072004B00530045006800710066005600530062004400630047003300660045005100580070004E006C00610032006D00610065006A006100620046006E003400360045003300320079004700610054006A007400620065002F007800390051006500380068004C00370054006E0074004500300067003D; homeAcc_cookie=0045004F006E00720071005500380073006E004A006C0035006500320062004E00440050005900710056006B004E004E006C003300390037005A0045004A004D00680063005A0032004D00700064005000520067004E004C003400770063005000320058004F004A00550051003D003D; s_sq=%5B%5BB%5D%5D; acw=a8e61aed25c77040a739fa79e34860cf67f0gxrqa%7C%24%7CF5C1A58DEAFB042B5C329B60F92386A8C5BC5AFF6370414C613B6FD50E33357BFFA1C4AFDF85601A032E026EEF5C60E57060D15B77680BB35B2791389D9DC89EE755B001AF5A0858787A139BC1C55061; _pendo_meta.7108b796-60e0-44bd-6a6b-7313c4a99c35=1065226270; scopus.machineID=1562093D14B3F7F895202A912E66D61E.wsnAw8kcdt7IPYLO0V48gA; javaScript=true; xmlHttpRequest=true; s_cc=true; screenInfo=820:1024; _pendo_visitorId.7108b796-60e0-44bd-6a6b-7313c4a99c35=ae%3A20783356; _pendo_accountId.7108b796-60e0-44bd-6a6b-7313c4a99c35=ae%3A378034; s_pers=%20c19%3Dsc%253Asearch%253Adocument%2520searchform%7C1497336253417%3B%20v68%3D1497334453181%7C1497336253422%3B%20v8%3D1497334454390%7C1591942454390%3B%20v8_s%3DLess%2520than%25207%2520days%7C1497336254390%3B; s_sess=%20v31%3D1497190047200%3B%20s_cpc%3D0%3B%20e41%3D1%3B%20s_ppvl%3Dsc%25253Asearch%25253Adocument%252520searchform%252C66%252C66%252C691%252C1024%252C691%252C1024%252C820%252C1.25%252CP%3B%20s_ppv%3Dsc%25253Asearch%25253Adocument%252520searchform%252C66%252C66%252C691%252C1024%252C222%252C1024%252C820%252C1.25%252CP%3B'))
