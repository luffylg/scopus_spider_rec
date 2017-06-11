# coding:utf-8
import time
from Mode.ModeBase import ModeBase
from threading import Thread


class MyThread(Thread):
    def __init__(self, ses, AuthorID, bianhao=0):
        Thread.__init__(self)
        self.ses = ses
        self.AuthorID = AuthorID
        self.bianhao = bianhao
        self.result = None

    def run(self):
        self.result = ModeBase().crawel(self.ses, self.AuthorID, self.bianhao)

    def get_result(self):
        return self.result
