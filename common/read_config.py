from configparser import RawConfigParser
from common import contants

class ReadConfig:
    """读取配置文件"""
    def __init__(self):
        self.config = RawConfigParser()
        self.config.read(contants.global_conf_file,encoding='utf-8')#先读取global.conf文件
        switch = self.config.getboolean('switch','on')#global.conf文件中的switch如果是true就去读取online.conf，相反就去读取test.conf
        if switch:
            self.config.read(contants.online_conf_file,encoding='utf-8')
        else:
            self.config.read(contants.test_conf_file,encoding='utf-8')

    def get_str(self,section,option):
        return self.config.get(section,option)

    def get_int(self,section,option):
        return self.config.getint(section,option)

    def get_float(self,section,option):
        return self.config.getfloat(section,option)

    def get_bool(self,section,option):
        return self.config.getboolean(section,option)

    def write(self,section,option,value):
        self.config.set(section,option,value)
        with open(contants.test_conf_file,'w') as f:
            self.config.write(f)


config = ReadConfig()#在这个模块中实例化一个对象，下次可以直接调用该模块中的该对象

if __name__ == '__main__':
    config.write('testdata','bb','ccc')