from unittest import TestCase
from time import sleep
from selenium import webdriver
from basic.system import system
from basic.dnspage import dnspage
from basic.assist import Tools
from basic.ddi_api import ddi_api
from basic.resource import resource


class RunTest(TestCase, Tools, ddi_api, system, dnspage, resource):
    @classmethod
    def setUpClass(cls):
        cls.get_info()
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get(cls.websites)
        cls.driver.find_element_by_id('loginname').send_keys(cls.username)
        cls.driver.find_element_by_id('password').send_keys(cls.password)
        cls.driver.find_element_by_id('vcoe').send_keys('yamu')
        cls.driver.find_element_by_id('login_btn').click()

    @classmethod
    def tearDownClass(cls):
        sleep(1)
        cls.driver.quit()

    def setUp(self):
        self.exception = set()
        self.path_click('/html/body/div[1]/div[1]/header/div[1]/div/div[3]/div/div/div/ul/li[1]/h2/a')
        print('添加dns节点')
        self.dhs_node_add_dns_node(nodename=self.nodename[0], device=self.devices)
        self.dhs_node_add_dns_node(nodename=self.nodename[1])
        print('为节点%s添加api用户%s' % (self.nodename[0], self.api_user))
        self.add_api_user(self.nodename[0], self.api_user, self.api_password)
        sleep(4)

    def tearDown(self):
        self.authorization_delete_all_domain()
        self.delete_api_user()
        print("删除所有DNS节点")
        self.dns_node_delete_all_node()
        if self.exception:
            raise Exception(self.exception)

    def test_add_auth_domain_with_sepcific_parameter(self):


        url1 = "https://" + self.serverip[0] + ":19393/api/dns/zones"

        print('Step1: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，指定的节点名存在')
        payload1 = {
                    "nodeName": self.nodename[0],
                    "domain": "a1.com"
                    }
        r1 = self.post(url=url1,json=payload1,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code1,res1 = r1
            if not (status_code1 == 200 and res1['code'] == "Success"):
                self.exception.add('Step1: ' + str(res1))
        else:
            self.exception.add('Step1: ' + str(self.api_error))

        print('Step2: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，指定的节点名不存在')
        payload2 = {
            "nodeName": "node33",
            "domain": "a2.com"
        }
        r2 = self.post(url=url1, json=payload2, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code2, res2 = r2
            if not (status_code2 == 400 and res2['code'] == "NodeNotExisted"):
                self.exception.add('Step2: ' + str(res2))
        else:
            self.exception.add('Step2: ' + str(self.api_error))

        print('Step3: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，指定的视图存在')
        payload3 = {
                    "viewName": "default",
                    "domain": "a3.com"
                    }
        r3 = self.post(url=url1, json=payload3, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code3, res3 = r3
            if not (status_code3 == 200 and res3['code'] == "Success"):
                self.exception.add('Step3: ' + str(res3))
        else:
            self.exception.add('Step3: ' + str(self.api_error))

        print('Step4: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，指定的视图不存在')
        payload4 = {
                    "viewName": "view123456",
                    "domain": "a4.com"
                    }
        r4 = self.post(url=url1, json=payload4, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code4, res4 = r4
            if not (status_code4 == 400 and res4['code'] == "ViewNotExisted"):
                self.exception.add('Step4: ' + str(res4))
        else:
            self.exception.add('Step4: ' + str(self.api_error))

        print('Step5: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，输入的备注信息长度在合法范围内')
        payload5 = {
                    "domain": "a5.com",
                    "comment":"子公司内部"
                    }
        r5 = self.post(url=url1, json=payload5, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code5, res5 = r5
            if not (status_code5 == 200 and res5['code'] == "Success"):
                self.exception.add('Step5: ' + str(res5))
        else:
            self.exception.add('Step5: ' + str(self.api_error))

        print('Step6: 用POST方法调用接口https://192.168.6.62:19393/api/dns/zones，输入的备注信息长度超过100个字数')
        payload6 = {
                    "domain": "a6.com",
                    "comment": "a" * 101
                    }
        r6 = self.post(url=url1, json=payload6, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code6, res6 = r6
            if not (status_code6 == 400 and res6['code'] == "InvalidParam"):
                self.exception.add('Step4: ' + str(res6))
        else:
            self.exception.add('Step4: ' + str(self.api_error))
