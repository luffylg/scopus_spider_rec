import re


def seperatename(namelist):
    #获取姓和名
    namelist.reverse()
    name = ' '.join([i.strip() for i in namelist])
    namelists=name.strip().split()
    xing=namelists[-1]
    namelists.pop()
    ming=" ".join(namelists)
    return xing, ming

def strip_email_protection(s):
    #解密邮件地址
    fp = re.findall(r'email-protection#[A-Za-z0-9]+', s)
    #parse email
    fp = fp[0].replace('email-protection#','')
    # print(fp)

    r = int(fp[:2], 16)
    email = ''.join([chr(int(fp[i:i+2], 16) ^ r) for i in range(2, len(fp), 2)])
    # m = re.sub(r'<a class="__cf_email__".*?</a>', email, s)
    # #strip <script>
    # m = re.sub('<script.*?</script>', '', s, flags = re.DOTALL)
    return email

def clean(s):
    return s.lower().replace(' ', '').replace('.', '').replace(',', '').replace('-','')

def printresult(result):
    if result['bianhao'] != 0:
        print('第' + str(result['bianhao'] ) + '作者')
    print('文献数：' + result['wenxin']  + ' ' + result['lishi'])
    print(result['AuthorName'])
    print("缩写：" + result['suoxie'])
    print(result['area'])
    print(result['email'])
    print('年份: ' + result['nian'] + '\n')

def writefile(out,result):
    out.write('文献数：' + result['wenxin'] + ' ' + result['lishi']+'\n')
    out.write(result['AuthorName'] + '\n')
    out.write("缩写：" + result['suoxie'] + '\n')
    out.write(result['area'] + '\n')
    out.write(result['email'] + '\n')
    out.write('年份: ' + result['nian'] + '\n')

def infilter(author,message):
    if not message:
        return False
    filte=re.compile(r';|；').split(message)
    for s in filte:
        if s.lower().strip() in author['area'].lower():
            return True
    return False
