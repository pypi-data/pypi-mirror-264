from base_td.logger import LoggerBase
from datetime import datetime
import os
from util_py.fs import mkdir
import json
from munch  import Munch
from pathlib import Path

class Persistence(LoggerBase):
    def __init__(self, save_path):
        LoggerBase.__init__(self)
        self.save_path = save_path
        mkdir(save_path)

    # 以文件储存对象，持仓和订单    
    def save(self, obj, name, fields=[]):
        if isinstance(obj, list):
            kv = []
            for item in obj:
                if isinstance(item, dict):
                    item = Munch.fromDict(item)
                kv_item = {}
                if not len(fields):
                    fields = item.keys()
                for field in fields:
                    v = getattr(item, field)
                    if isinstance(v, datetime):
                        kv_item[field] = v.strftime('%Y-%m-%d %H:%M:%S+08:00')
                    elif isinstance(v, float) or isinstance(v, int):
                        kv_item[field] = v
                    else:
                        kv_item[field] = str(v)
                kv.append(kv_item)
        else:
            if isinstance(obj, dict):
                obj = Munch.fromDict(obj)
            kv = {}
            if not len(fields):
                fields = obj.keys()
            for field in fields:
                v = getattr(obj, field)
                if isinstance(v, datetime):
                    kv[field] = v.strftime('%Y-%m-%d %H:%M:%S+08:00')
                elif isinstance(v, float) or isinstance(v, int):
                    kv[field] = v
                else:
                    kv[field] = str(v)
        
        ts_file = os.path.join(self.save_path, f'{name}.json')
        with open(ts_file, 'w') as f:
            json.dump(kv, f, indent=4)
        
    def load(self, name):
        file = os.path.join(self.save_path, f'{name}.json')
        if not os.path.isfile(file):
            self.log({ 'file': file }, 'file_not_found')
            return None
        with open(file, 'r') as f:
            return Munch.fromDict(json.load(f))

    def list(self):
        files = os.listdir(self.save_path)
        return [Path(x).stem for x in files]

    def delete(self, names):
        for name in names:
            os.remove(os.path.join(self.save_path, f'{name}.json'))
        self.log(names)