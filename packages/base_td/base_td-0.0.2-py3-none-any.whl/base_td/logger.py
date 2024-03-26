from datetime import datetime
import os
import sys
import base_td.logger
from base_td.base import Base
from util_py.fs import mkdir
from util_py.log import Logger

root_path = os.path.join(os.path.dirname(__file__), '..')

class LoggerBase(Base):
    def __init__(self):
        Base.__init__(self)
        
        self.logger = None # 日志记录器
        
        self.root_path = None # 项目跟文件夹
        self.data_path = None # 数据文件夹
        self.today_path = None # 今天的文件夹
        self.account_path = None # 账号文件夹
        self.module_path = None # 存放今天该代码数据的文件夹
        self.init_dir()
        
    def init_dir(self):
        self.root_path = root_path
        data_path = os.path.join(root_path, 'data') # 数据文件夹
        today_str = datetime.now().strftime('%Y%m%d') # 今天的字符串代码
        today_path = self.today_path = os.path.join(data_path, today_str) # 今天的文件夹
        mkdir(today_path)

        # stock_account_id = str(config.accounts.us.stock.cash)
        # account_path = self.account_path = os.path.join(today_path, stock_account_id)
        # mkdir(account_path)

        module_path = self.module_path = os.path.join(today_path, self.__class__.__name__)
        mkdir(module_path)
        
    def log(self, kv={}, tag=None, level='info', name=None):
        if not self.logger:
            self.logger = Logger(self.module_path)

        fn_name = sys._getframe().f_back.f_code.co_name if not name else name

        if tag:
            self.logger.log([f'{self.__class__.__name__}.{fn_name}', tag], kv, level)
        else:
            self.logger.log([f'{self.__class__.__name__}.{fn_name}'], kv, level)

    def log_start(self, tag):
        self.log(tag, '------------ START ------------')

    def log_end(self, tag):
        self.log(tag, '------------  END  ------------')

    def update_logger(self):
        self.init_dir()
        self.logger = Logger(self.module_path)