from Mode import wenxian_mode
from Mode.ModeBase import ModeBase
from utils import printresult


class Wenjian_mode(ModeBase):
    def __init__(self,f_in):
        super().__init__()
        self.f_in=f_in

    def craw(self):
        idlist=[]
        lines = self.f_in.readlines()
        result=[]
        #print(lines)
        for line in lines:
            wenxian=line.rstrip('\n')
            if wenxian=='':
                continue
            print(wenxian)
            obj_spider=wenxian_mode.Wenxian_mode(wenxian)
            lists=obj_spider.craw(idlist,True)
            if lists:
                for author in lists:
                    printresult(author)
                    result.append(author)
            print('\n\n\n\n')

        return result
