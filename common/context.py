import configparser
import re
from common.read_config import config

class Context:

    def replace(self,data):
        """使用正则表达式，将Excel中参数化的值替换为配置文件中读取出来的值"""
        p ='#(.*?)#'
        while re.search(p,data):#判断data中能否根据正则表达式找到匹配的值
            m = re.search(p,data)# 从任意位置开始找，找第一个就返回Match object, 如果没有找到返回None
            g = m.group(1)#找到参数化的key值
            try:
                v = config.get_str('testdata',g)#根据key去配置文件里面取值
            except configparser.NoOptionError as e:
                if hasattr(Context,g):
                    v = getattr(Context,g)
                else:
                    print('找不到值')
                    raise e
            data = re.sub(p,v,data,count=1)#查找并替换Excel中参数化的值
        return data


