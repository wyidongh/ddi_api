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
        print('为节点%s添加api用户%s' % (self.nodename[0], self.api_user))
        self.add_api_user(self.nodename[0], self.api_user, self.api_password)
        sleep(4)

    def tearDown(self):
        self.authorization_delete_all_domain()
        self.delete_api_user()

        if self.exception:
            raise Exception(self.exception)

    def test_add_auth_record_AAAA_result_validation_check(self):


        print('Step1: 点击【域管理】在node1下的default视图，添加域test.com')
        domain1 = "test.com"
        ns_name1 = "ns." + domain1
        self.authorization_add_standard_domain(domainname=domain1, nodename=self.nodename[0], viewname='default',
                                               ns_name=ns_name1, ns_ip=self.serverip[0])


        url1 = "https://" + self.serverip[0] + ":19393/api/dns/records"

        print('Step2: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加AAAA类型记录解析结果正确')
        payload2 = {"domain":domain1,
                    "host":"j1",
                    "type":"AAAA",
                    "result":{"data":"1111:2222:3333:4444:aaaa:6666:ffff:eeee"}
                    }
        r2 = self.post(url=url1, json=payload2, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code2, res2 = r2
            if not (status_code2 == 200 and res2['code'] == "Success"):
                self.exception.add('Step2: ' + str(res2))
        else:
            self.exception.add('Step2: ' + str(self.api_error))



        print('Step3: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加AAAA类型记录解析结果正确')
        payload3 = {"domain":domain1,
                    "host":"j2",
                    "type":"AAAA",
                    "result":{"data":"::"}
                    }
        r3 = self.post(url=url1, json=payload3, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code3, res3 = r3
            if not (status_code3 == 200 and res3['code'] == "Success"):
                self.exception.add('Step3: ' + str(res3))
        else:
            self.exception.add('Step3: ' + str(self.api_error))


        print('Step4: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加AAAA类型记录解析结果正确')
        payload4 = {"domain":domain1,
                    "host":"j3",
                    "type":"AAAA",
                    "result":{"data":"1111::ff"}
                    }
        r4 = self.post(url=url1, json=payload4, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code4, res4 = r4
            if not (status_code4 == 200 and res4['code'] == "Success"):
                self.exception.add('Step4: ' + str(res4))
        else:
            self.exception.add('Step4: ' + str(self.api_error))


        print('Step5: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加AAAA类型记录解析结果不合法，超过8段')
        payload5 = {"domain":domain1,
                    "host":"j4",
                    "type":"AAAA",
                    "result":{"data":"1111:2222:3333:4444:aaaa:6666:7777:8888:9999"}
                    }
        r5 = self.post(url=url1, json=payload5, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code5, res5 = r5
            if not (status_code5 == 400 and res5['code'] == "InvalidParam"):
                self.exception.add('Step5: ' + str(res5))
        else:
            self.exception.add('Step5: ' + str(self.api_error))

        print('Step6: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加AAAA类型记录解析结果不合法')
        payload6 = {"domain":domain1,
                    "host":"j6",
                    "type":"AAAA",
                    "result":{"data":"-1111:2222:3333:4444:aaaa:6666:gefd:eeee"}
                    }
        r6 = self.post(url=url1, json=payload6, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code6, res6 = r6
            if not (status_code6 == 400 and res6['code'] == "InvalidParam"):
                self.exception.add('Step6: ' + str(res6))
        else:
            self.exception.add('Step6: ' + str(self.api_error))

        print('Step7: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加AAAA类型记录解析结果不合法，有多个缩写符号')
        payload7 = {"domain":domain1,
                    "host":"j7",
                    "type":"AAAA",
                    "result":{"data":"11::22::"}
                    }
        r7 = self.post(url=url1, json=payload7, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code7, res7 = r7
            if not (status_code7 == 400 and res7['code'] == "InvalidParam"):
                self.exception.add('Step7: ' + str(res7))
        else:
            self.exception.add('Step7: ' + str(self.api_error))
