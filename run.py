# 通过loader来加载整个模块的用例
import unittest
import HTMLTestRunner
from common import contants

suite = unittest.TestSuite()
loader = unittest.TestLoader()
discover = unittest.defaultTestLoader.discover(contants.case_dir,'test_*.py')

with open(contants.report_dir + '/qianchengdaiAPI_testreport.html','wb+') as file:
    runner =HTMLTestRunner.HTMLTestRunner(stream=file,verbosity=3,title='前程贷接口测试报告',
                                          description='注册登录充值加标审核投标接口的测试报告',tester = '夜莺')
    runner.run(discover)