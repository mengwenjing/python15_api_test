import unittest
from ddt import ddt,data
from common.http_request import HttpRequest2
from common.doexcel import DoExcel
from common.contants import case_file
from common.context import Context
from common.domysql import DoMysql
from common.collect_log import MyLog

logger = MyLog().logger(__name__)

@ddt
class TestInvest(unittest.TestCase):

    logger.info('开始执行TestInvest测试类')

    testdata = DoExcel(case_file,'invest').read_data()

    @classmethod
    def setUpClass(cls):
        cls.session = HttpRequest2()
        cls.mysql = DoMysql()

    @data(*testdata)
    def testInvest(self,case):
        case.data = Context().replace(case.data)#使用正则表达式，将Excel中参数化的值替换为配置文件中读取出来的值
        if case.sql is not None:
            case.sql = Context().replace(case.sql)
        if case.title == '成功竞标':
            before_leaveamount = self.mysql.fetch_one(case.sql)['leaveamount']
            logger.info('成功竞标前，用户余额是：{}'.format(before_leaveamount))

        res = self.session.request(method=case.method,url=case.url,data=case.data)
        logger.info('执行用例是：{}，请求url是：{}'.format(case.title, case.url))
        logger.info('请求数据是：{}'.format(case.data))
        try:
            self.assertEqual(case.expected,int(res.json()["code"]))
        except AssertionError as e:
            DoExcel(case_file,'invest').write_data(case.case_id+1,res.text,'failed')
            logger.error("断言失败,错误信息是：{}".format(e))
        else:
            DoExcel(case_file,'invest').write_data(case.case_id+1,res.text,'pass')
            logger.info('用例执行成功')
            if res.json()['msg'] == '加标成功':
                loadId = self.mysql.fetch_one(case.sql)['id']
                setattr(Context,'loanId',str(loadId))
                logger.info('成功加标的ID是：{}'.format(getattr(Context,'loanId')))
            if res.json()['msg'] == '竞标成功':
                loan_amount = int(eval(case.data)['amount'])
                after_leaveamount = self.mysql.fetch_one(case.sql)['leaveamount']
                logger.info('成功竞标的ID是：{}，竞标金额是：{}，竞标成功后账户余额是{}'.format(eval(case.data)['loanId'],loan_amount,after_leaveamount))
                try:
                    self.assertEqual(before_leaveamount-loan_amount,after_leaveamount)
                    logger.info('竞标成功后，账户余额正确')
                except AssertionError as e:
                    logger.error('投标成功后，账户余额错误,错误信息是：{}'.format(e))

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        cls.mysql.close()