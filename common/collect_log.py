#写一个日志类
#结合配置文件 完成 输出的格式 输出的级别的配置

import logging
from logging.handlers import TimedRotatingFileHandler
from common.read_config import config
from common.contants import log_dir

class MyLog:

    #初始化函数里定义日志收集器的名字，收集级别，输出级别，格式，输出渠道
    def logger(self,name):
        collector = name
        collect_level = config.get_str('log','collect_level')
        output_level = config.get_str('log','output_level')
        fmt = config.get_str('log','fmt')
        output = config.get_str('log','output')

        my_log = logging.getLogger(collector)#定义一个日志收集器

        my_log.setLevel(collect_level)#设置收集日志的级别

        #设置日志的输出渠道，输出到控制台或者指定文件
        if  output == 'console':
            ch = logging.StreamHandler()
        else:
            # 定义一个一天换一次日志文件的渠道（每天生成一个新的日志文件），最多保留两个旧的日志文件，也就是说保留两天的日志文件
            ch = TimedRotatingFileHandler(log_dir+output, when='D', interval=1, backupCount=2,encoding='utf-8')

        ch.setLevel(output_level)#设置输出日志的级别

        my_log.addHandler(ch)#给日志添加输出渠道

        formatter = logging.Formatter(fmt)#设置日志输出的格式
        ch.setFormatter(formatter)

        return my_log

if __name__ == '__main__':
    log = MyLog().logger('test')
    log.info('hhhhhhh')
    log.info('xxxxxxx')

