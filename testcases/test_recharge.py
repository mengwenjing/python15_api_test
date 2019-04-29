import unittest
from ddt import ddt,data
from common.http_request import HttpRequest2
from common.doexcel import DoExcel
from common import contants
from common.context import Context
from common.domysql import DoMysql
from common.collect_log import MyLog

logger = MyLog().logger(__name__)

@ddt
class TestRecharge(unittest.TestCase):

    logger.info('开始执行TestRecharge测试类')

    testdata = DoExcel(contants.case_file,'recharge').read_data()

    @classmethod
    def setUpClass(cls):
        cls.session = HttpRequest2()
        cls.mysql = DoMysql()

    @data(*testdata)
    def testRecharge(self,case):
        case.data = Context().replace(case.data)
        if case.title == '充值成功':
            case.sql = Context().replace(case.sql)
            before_leaveamount = self.mysql.fetch_one(case.sql)['leaveamount']
            logger.info('用例开始执行前，账户余额是：{}'.format(before_leaveamount))
        res = self.session.request(method=case.method,url=case.url,data=case.data)
        logger.info('执行用例是：{}，请求url是：{}'.format(case.title,case.url))
        logger.info('请求数据是：{}'.format(case.data))
        try:
            self.assertEqual(case.expected,res.json()['msg'])
        except AssertionError as e:
            DoExcel(contants.case_file,'recharge').write_data(case.case_id+1,res.text,'failed')
            logger.error('断言失败，报错信息{}'.format(e))
        else:
            DoExcel(contants.case_file, 'recharge').write_data(case.case_id + 1, res.text, 'pass')
            logger.info('用例执行成功')
            if res.json()['msg'] == '充值成功':
                after_leaveamount = self.mysql.fetch_one(case.sql)['leaveamount']
                logger.info('充值成功后，账户余额是：{}'.format(after_leaveamount))
                recharge_amount = eval(case.data)['amount']
                try:
                    self.assertEqual(before_leaveamount+recharge_amount,after_leaveamount)
                    logger.info('充值成功后,账户余额正确')
                except AssertionError as e:
                    logger.info('充值成功后，账户余额错误。错误是{}'.format(e))

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        cls.mysql.close()
