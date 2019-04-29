import unittest
from ddt import ddt,data
from common.http_request import HttpRequest2
from common.doexcel import DoExcel
from common.contants import case_file
from common.context import Context
from common.collect_log import MyLog
from common.domysql import DoMysql

logger = MyLog().logger(__name__)

@ddt
class TestAdd(unittest.TestCase):

    logger.info('开始执行TestAdd测试类')

    testdata = DoExcel(case_file,'add').read_data()

    @classmethod
    def setUpClass(cls):
        cls.session = HttpRequest2()
        cls.mysql = DoMysql()

    @data(*testdata)
    def testInvest(self,case):
        case.data = Context().replace(case.data)#使用正则表达式，将Excel中参数化的值替换为配置文件中读取出来的值
        res = self.session.request(method=case.method,url=case.url,data=case.data)
        logger.info('执行用例是：{}，请求url是：{}'.format(case.title, case.url))
        logger.info('请求数据是：{}'.format(case.data))
        try:
            self.assertEqual(case.expected,int(res.json()["code"]))
        except AssertionError as e:
            DoExcel(case_file,'add').write_data(case.case_id+1,res.text,'failed')
            logger.error("断言失败，错误信息是：{}".format(e))
        else:
            DoExcel(case_file,'add').write_data(case.case_id+1,res.text,'pass')
            logger.info('用例执行成功')
            if res.json()['msg'] == '加标成功':
                case.sql = Context().replace(case.sql)
                loadId = self.mysql.fetch_one(case.sql)['id']
                setattr(Context, 'loanId', str(loadId))

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        cls.mysql.close()