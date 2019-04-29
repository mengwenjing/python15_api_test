import unittest
from ddt import ddt,data
from common.http_request import HttpRequest2
from common.doexcel import DoExcel
from common import contants
from common.collect_log import MyLog
from common.context import Context

logger = MyLog().logger(__name__)#定义一个以当前文件名命名的日志收集器，来收集日志

@ddt
class TestLogin(unittest.TestCase):

    logger.info('开始执行TestLogin测试类')

    testdata = DoExcel(contants.case_file,'login').read_data()

    @classmethod
    def setUpClass(cls):
        cls.session = HttpRequest2()

    @data(*testdata)
    def testLogin(self,case):
        case.data = Context().replace(case.data)
        res = self.session.request(method=case.method,url=case.url,data=case.data)
        logger.info('执行用例是：{}，请求url是：{}'.format(case.title, case.url))
        logger.info('请求数据是：{}'.format(case.data))
        try:
            self.assertEqual(case.expected,res.text)
        except AssertionError as e:
            DoExcel(contants.case_file,'login').write_data(case.case_id+1,res.text,'failed')
            logger.error('断言出错，错误信息是：{}'.format(e))
        else:
            DoExcel(contants.case_file,'login').write_data(case.case_id+1,res.text,'pass')
            logger.info('用例执行成功')

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
