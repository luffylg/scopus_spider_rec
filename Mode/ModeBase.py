import html_parser
from utils import strip_email_protection


class ModeBase(object):
    def __init__(self):
        self.parser = html_parser.HtmlParser()
        self.cookies={}

    def crawel(self, ses, AuthorID, bianhao=0):
        s2 = ses.get('https://www.scopus.com/authid/detail.uri', params={'authorId': AuthorID})  # 获取作者详细信息页面
        message = self.parser.GetAuthorMessage(s2)  # 获取详细信息
        wenxin = message[0]
        AuthorName = message[1]
        area = message[2]
        lishi = message[4]
        if int(wenxin) < 10:  # 文献数少于10，直接返回
            # print('文献数为'+wenxin+'，不符合要求')
            # return AuthorName,area,lishi,email,suoxie,nian,wenxin
            # print('文献数：'+wenxin+' '+lishi)
            return None
        # print(AuthorName)
        # print(area)
        Articlelink = message[3]  # 获取作者所有文章页面链接
        s3 = ses.get(Articlelink, timeout=60)  # 获取作者所有文章页面
        Articles = self.parser.GetArticles(s3)  # 获得所有文章链接及年份列表
        for lists in Articles:
            result = {}
            link = lists[0]
            nian = lists[1]
            s4 = ses.get(link, timeout=60)  # 获取文章详细信息页面
            emailnotparse, suoxie = self.parser.GetEmail(s4)  # 得到加密的邮件地址
            if emailnotparse is not None:
                result['AuthorName']=AuthorName
                result['bianhao']=bianhao
                result['wenxin']=wenxin
                result['AuthorName']=AuthorName
                result['suoxie']=suoxie
                result['area']=area
                result['lishi']=lishi
                email = emailnotparse.get('href').replace('mailto:', '').strip()
                # 网站变动，不需要解析邮件，可以直接获取
                if 'email-protection' in email:
                    email = strip_email_protection(emailnotparse['href'])
                result['email']=email
                result['nian']=nian
                return result
        return None
        # print("没找到邮箱")
