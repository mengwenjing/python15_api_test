import requests
from common.read_config import config

# 进行httprequest有两种方式，一种是使用不同的session进行请求，自己手动传递cookies；另一种是使用同一个session，cookies自动进行传递

class HttpRequest1:

    """方式一：使用不同的session进行请求，手动传递cookies"""

    def request(self,method,url,data=None,json=None,request_cookies=None):#传参：请求方法，接口地址，请求参数，请求cookies

        if type(data) == str:#将data转换为字典
            data = eval(data)

        url = config.get_str('api','pre_url') + url#读取配置文件中的接口地址，再将其与Excel中的url拼接，形成最终的请求地址

        if method.upper() == 'GET':
            res = requests.get(url,params=data,cookies=request_cookies)
        elif method.upper() =='POST':
            if json:
                res = requests.post(url,json=json,cookies=request_cookies)
            else:
                res = requests.post(url,data=data,cookies=request_cookies)
        else:
            res = None
            print('UN-support method')

        return res

class HttpRequest2:

    """方式二：使用同一个session，cookies将自动传递"""

    def __init__(self):#在初始化函数里面打开一个session
        self.session = requests.sessions.session()

    def request(self,method,url,data=None,json=None):

        if type(data) == str:
            data = eval(data)

        url = config.get_str('api','pre_url') + url#读取配置文件中的接口地址，再将其与Excel中的url拼接，形成最终的请求地址

        if method.upper() == 'GET':
            res = self.session.request(method=method,url=url,params=data)
        elif method.upper() == 'POST':
            if json:
                res = self.session.request(method=method,url=url,json=json)
            else:
                res = self.session.request(method=method,url=url,data=data)
        else:
            res = None
            print('Un-support method')

        return res

    def close(self):#关闭session，用完关闭，很重要！
        self.session.close()


if __name__ == '__main__':
    # res = HttpRequest1().request('post','http://test.lemonban.com/futureloan/mvc/api/member/login',
    #                              {"mobilephone":"13125256363","pwd":"123456"})
    # print(res.text)
    # print(res.cookies)
    # res2 = HttpRequest1().request('post','http://test.lemonban.com/futureloan/mvc/api/member/recharge',
    #                               {"mobilephone":"13125256363","amount":10},request_cookies=res.cookies)
    # print(res2.text)
    #
    # session = HttpRequest2()
    #
    # res3 = session.request('post','http://test.lemonban.com/futureloan/mvc/api/member/login',
    #                              '{"mobilephone":"13125256363","pwd":"123456"}')
    # print(res3.json())
    # res4 = session.request('post','http://test.lemonban.com/futureloan/mvc/api/member/recharge',
    #                               {"mobilephone":"13125256363","amount":10})
    # print(res4.json())

    json = {"body":"zaHWxBeSECgrIJIvQD8ksMePpiuZwIM1MroYzGGOmwdnOHlMp+b2e3YgV+qlwwVr"}
    res5 = HttpRequest2().request('post','http://test.17kaojiaoshi.com:3088/user/my_address',json=json)

    print(res5.json())