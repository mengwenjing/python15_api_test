import unittest
from ddt import ddt,data
from common.http_request import HttpRequest2
from common.doexcel import DoExcel
from common import contants
from common.domysql import DoMysql
from common.collect_log import MyLog

logger = MyLog().logger(__name__)

@ddt
class TestRegister(unittest.TestCase):

    logger.info('开始执行TestRegister测试类')

    testdata = DoExcel(contants.case_file,'register').read_data()

    @classmethod
    def setUpClass(cls):
        cls.session = HttpRequest2()
        cls.mysql = DoMysql()

    @data(*testdata)
    def testRegister(self,case):

        #将注册手机号在Excel中参数化，方式一：使用字符串替换
        # if case.data.find('register_phone') > -1:
        #     #如果在case.data中找到register_phone，就去数据库找到最大的手机号并+1。
        #     max_phone = self.mysql.fetch_one('select max(mobilephone) from member')[0]#如果返回数据是元组，用索引取值
        #     max_phone = int(max_phone)+1
        #     #把case.data字符串中的register_phone替换为重新赋值的最大手机号，
        #     #replace方法是替换之后返回一个新的字符串，所有要重新定义变量去接收
        #     case.data = case.data.replace('register_phone',str(max_phone))

        #方式二：使用字典的方式，给字典的key重新赋值
        case.data = eval(case.data)
        if case.data.__contains__('mobilephone') and case.data['mobilephone'] == 'register_phone':
            max_phone = self.mysql.fetch_one('select max(mobilephone) from future.member')['max(mobilephone)']#返回数据是字典，用key取值
            max_phone = int(max_phone) + 1
            case.data['mobilephone'] = max_phone

        res = self.session.request(method=case.method,url=case.url,data=case.data)
        logger.info('执行用例是：{}，请求url是：{}'.format(case.title, case.url))
        logger.info('请求数据是：{}'.format(case.data))
        try:
            self.assertEqual(case.expected,res.text)
        except AssertionError as e:
            DoExcel(contants.case_file,'register').write_data(case.case_id+1,res.text,'filed')
            logger.error("断言失败，错误是：{}".format(e))
        else:
            DoExcel(contants.case_file, 'register').write_data(case.case_id + 1, res.text, 'pass')
            logger.info('用例执行成功')
            if res.json()['msg'] == '注册成功':
                new_mobile = self.mysql.fetch_one('select mobilephone from future.member where mobilephone = ' + str(case.data['mobilephone']))
                try:
                    self.assertEqual(str(case.data['mobilephone']),str(new_mobile['mobilephone']))
                    logger.info('注册成功，注册使用手机号是：{}，注册成功的手机号是：{}'.format(case.data['mobilephone'],new_mobile['mobilephone']))
                except AssertionError as e:
                    logger.error('注册手机号错误，错误信息是：{}'.format(e))

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        cls.mysql.close()