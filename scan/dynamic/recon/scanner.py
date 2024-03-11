from common import config

class Scanner:

    def __init__(self, thread_cnt=config.MAX_THREADS):
        self.thread_cnt = thread_cnt
        self.result = {}
        self.request_cnt = 0
        self.success_cnt = 0

    def init_result(self):
        self.result = {}
        self.request_cnt = 0
        self.success_cnt = 0

