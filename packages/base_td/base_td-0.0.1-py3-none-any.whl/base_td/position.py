from base_td.logger import LoggerBase
import os
from util_py.fs import mkdir
import json
from munch  import Munch
from pathlib import Path
from datetime import datetime
from base_td.constant import DATE_FMT

class Position(LoggerBase):
    def __init__(self, code, qty=0, date=None):
        LoggerBase.__init__(self)
        self.code = code
        self.qty = qty
        self.date = date or datetime.now().strftime(DATE_FMT)