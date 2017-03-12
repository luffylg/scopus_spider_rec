from Mode import keyword_mode
from Mode import wenjian_mode
from Mode import wenxian_mode
from Mode import zuozhe_mode
from utils import *

class Main:
    def init_print(self, count=5):
        print()
        print('编号1为人名模式，编号2为文献模式，编号3为文件模式，编号4为按发表数排列输出的文件模式，编号5为模糊文献模式，输入exit退出')
        flag = input('输入编号：').strip()
        if flag == str(1):
            # 通过输入人名查找审稿人
            # 形如'hong, weirong'姓在前，不带逗号的姓在后
            xing, ming = seperatename(input("人名: ").split(','))
            obj_spider = zuozhe_mode.ZuozheMode(xing, ming)
            result=obj_spider.craw()
            if not result:
                print("找不到人")
            else:
                printresult(result)

        elif flag == str(2):
            wenxian = input('文献标题：').strip()
            if wenxian == 'exit':
                exit()
            obj_spider = wenxian_mode.Wenxian_mode(wenxian)
            results=obj_spider.craw()
            print(wenxian)
            if not results:
                print("找不到文献")
            else:
                for result in results:
                    printresult(result)
                    print('\n\n\n\n')
        elif flag == str(3):
            print('*************************')
            print('读取spider.txt...')
            # 通过读取分行写好需要爬的文献名，循环爬取审稿人信息，输出文档。
            with open('spider.txt', 'r',encoding='utf-8') as f_in:# 不加encoding会出现UnicodeDecodeError: 'gbk' codec can't decode byte 0x80 in position
                # 传入文件对象
                obj_spider = wenjian_mode.Wenjian_mode(f_in)
                obj_spider.craw()
        elif flag == str(4):

            # authors = wenjian_mode2()
            filename=input('输入形如A-17-00000或者纯编号的文件名:')
            if re.match(r'\d+',filename):
                filename='A-17-'+filename
            message=input('输入需要过滤的字段，以分号分割:')
            print('*************************')
            print('读取spider.txt...')
            with open('spider.txt', 'r', encoding='utf-8') as f_in:
                obj_spider = wenjian_mode.Wenjian_mode(f_in)
                authors=obj_spider.craw()
                # 以文献数大小排序
                authors = sorted(authors, key=lambda author: int(author["wenxin"]), reverse=True)
                print('*************************')
                print("\n\n\n\n排序后")
                with open('{0}.txt'.format(filename),'w',encoding='utf-8') as out:
                    for author in authors:
                        if infilter(author,message):
                            continue
                        print('文献数：' + author["wenxin"] + ' ' + author['lishi'])
                        print(author['AuthorName'])
                        print("缩写：" + author['suoxie'])
                        print(author['area'])
                        print(author['email'])
                        # print('<a href=\''+email+'\'>'+email+'></a>')
                        print('年份: ' + author['nian'] + '\n')
                        print('\n\n')
                        writefile(out,author)
                        out.write('\n\n\n\n')


        elif flag == str(5):
            wenxian = input('文献模糊标题或关键字：').strip()
            if wenxian == 'exit':
                exit()
            filename = input('输入形如A-17-00000或者纯编号的文件名:')
            if re.match(r'\d+', filename):
                filename = 'A-17-' + filename
            message = input('输入需要过滤的字段，以分号分割:')
            obj_spider = keyword_mode.Keyword_mode(wenxian)
            authors = obj_spider.craw()
            authors = sorted(authors, key=lambda author: int(author["wenxin"]), reverse=True)
            print("\n\n结果：")
            with open('{0}.txt'.format(filename), 'w', encoding='utf-8') as out:
                for author in authors:
                    if infilter(author, message):
                        continue
                    print('文献数：' + author["wenxin"] + ' ' + author['lishi'])
                    print(author['AuthorName'])
                    print("缩写：" + author['suoxie'])
                    print(author['area'])
                    print(author['email'])
                    # print('<a href=\''+email+'\'>'+email+'></a>')
                    print('年份: ' + author['nian'] + '\n')
                    print('\n\n')
                    writefile(out, author)
                    out.write('\n\n\n\n')
        else:
            if count == 1:
                print('五次错误输入，程序退出')
                return
            print('输入不符合要求，重新输入')
            self.init_print(count-1)


if __name__ == '__main__':
    Main().init_print()
