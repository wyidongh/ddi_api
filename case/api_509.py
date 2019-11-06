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
        print("删除所有DNS节点")
        self.dns_node_delete_all_node()
        if self.exception:
            raise Exception(self.exception)

    def test_add_auth_record_CNAME_NS_MX_result_validation_check(self):


        print('Step1: 点击【域管理】在node1下的default视图，添加域test.com')
        domain1 = "test.com"
        ns_name1 = "ns." + domain1
        self.authorization_add_standard_domain(domainname=domain1, nodename=self.nodename[0], viewname='default',
                                               ns_name=ns_name1, ns_ip=self.serverip[0])


        url1 = "https://" + self.serverip[0] + ":19393/api/dns/records"

        print('Step2: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加CNAME类型记录解析结果正确，且解析结果指向本域存在的域名')
        payload2 = {
                    "domain": domain1,
                    "host": "k1",
                    "type": "CNAME",
                    "result": {"data": "www.test.com"}
                    }
        r2 = self.post(url=url1, json=payload2, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code2, res2 = r2
            if not (status_code2 == 200 and res2['code'] == "Success"):
                self.exception.add('Step2: ' + str(res2))
        else:
            self.exception.add('Step2: ' + str(self.api_error))



        print('Step3: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加CNAME类型记录解析结果正确，且解析结果非本域的域名')
        payload3 = {
                    "domain": domain1,
                    "host": "k2",
                    "type": "CNAME",
                    "result": {"data": "www.qq.com"}
                    }
        r3 = self.post(url=url1, json=payload3, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code3, res3 = r3
            if not (status_code3 == 200 and res3['code'] == "Success"):
                self.exception.add('Step3: ' + str(res3))
        else:
            self.exception.add('Step3: ' + str(self.api_error))


        print('Step4: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加CNAME类型记录解析结果正确，解析结果指向本域不存在的域名')
        """
        2.2.1版本以后支持添加CNAME解析结果为本域不存在的域名
        """


        print('Step5: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加CNAME类型记录解析结果域名不合法')
        payload5 = {
                    "domain": domain1,
                    "host": "k3",
                    "type": "CNAME",
                    "result": {"data": "_-www123.host.com"}
                    }
        r5 = self.post(url=url1, json=payload5, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code5, res5 = r5
            if not (status_code5 == 400 and res5['code'] == "InvalidParam"):
                self.exception.add('Step5: ' + str(res5))
        else:
            self.exception.add('Step5: ' + str(self.api_error))

        print('Step6: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加NS类型记录解析结果域名合法')
        payload6 = {
                    "domain": domain1,
                    "host": "l1",
                    "type": "NS",
                    "result": {"data": "ns.test.com"}
                    }
        r6 = self.post(url=url1, json=payload6, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code6, res6 = r6
            if not (status_code6 == 200 and res6['code'] == "Success"):
                self.exception.add('Step6: ' + str(res6))
        else:
            self.exception.add('Step6: ' + str(self.api_error))

        print('Step7: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加NS类型记录解析结果域名不合法')
        payload7 = {
                    "domain": domain1,
                    "host": "l2",
                    "type": "NS",
                    "result": {"data": "_-ns.test.com"}
                    }
        r7 = self.post(url=url1, json=payload7, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code7, res7 = r7
            if not (status_code7 == 400 and res7['code'] == "InvalidParam"):
                self.exception.add('Step7: ' + str(res7))
        else:
            self.exception.add('Step7: ' + str(self.api_error))

        print('Step8: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加MX类型记录解析结果优先级和域名都合')
        payload8 = {
            "domain": domain1,
            "host": "m1",
            "type": "MX",
            "result": {"preference": 0, "data": "mail.test.com"}
        }
        r8 = self.post(url=url1, json=payload8, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code8, res8 = r8
            if not (status_code8 == 200 and res8['code'] == "Success"):
                self.exception.add('Step8: ' + str(res8))
        else:
            self.exception.add('Step8: ' + str(self.api_error))

        print('Step9: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加MX类型记录解析结果优先级和域名都合法')
        payload9 = {
            "domain": domain1,
            "host": "m2",
            "type": "MX",
            "result": {"preference": 10, "data": "mail.test.com"}
        }
        r9 = self.post(url=url1, json=payload9, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code9, res9 = r9
            if not (status_code9 == 200 and res9['code'] == "Success"):
                self.exception.add('Step9: ' + str(res9))
        else:
            self.exception.add('Step9: ' + str(self.api_error))

        print('Step10: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加MX类型记录解析结果优先级和域名都合法')
        payload10 = {
            "domain": domain1,
            "host": "m33",
            "type": "MX",
            "result": {"preference": 65535, "data": "mail.test.com"}
        }
        r10 = self.post(url=url1, json=payload10, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code10, res10 = r10
            if not (status_code10 == 200 and res10['code'] == "Success"):
                self.exception.add('Step10: ' + str(res10))
        else:
            self.exception.add('Step10: ' + str(self.api_error))

        print('Step11: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加MX类型记录解析结果优先级不合法，域名合法')
        payload11 = {
            "domain": domain1,
            "host": "m3",
            "type": "MX",
            "result": {"preference": 65535, "data": "mail.test.com"}
        }
        r11 = self.post(url=url1, json=payload11, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code11, res11 = r11
            if not (status_code11 == 200 and res11['code'] == "Success"):
                self.exception.add('Step11: ' + str(res11))
        else:
            self.exception.add('Step11: ' + str(self.api_error))

        print('Step12: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加MX类型记录解析结果优先级不合法，域名合法')
        payload12 = {
            "domain": domain1,
            "host": "m4",
            "type": "MX",
            "result": {"preference": 65536, "data": "mail.test.com"}
        }
        r12 = self.post(url=url1, json=payload12, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code12, res12 = r12
            if not (status_code12 == 400 and res12['code'] == "InvalidParam"):
                self.exception.add('Step12: ' + str(res12))
        else:
            self.exception.add('Step12: ' + str(self.api_error))

        print('Step13: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加MX类型记录解析结果优先级合法，域名不合法')
        payload13 = {
            "domain": domain1,
            "host": "m5",
            "type": "MX",
            "result": {"preference": 20, "data": "#@mail_.test.com"}
        }
        r13 = self.post(url=url1, json=payload13, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code13, res13 = r13
            if not (status_code13 == 400 and res13['code'] == "InvalidParam"):
                self.exception.add('Step13: ' + str(res13))
        else:
            self.exception.add('Step13: ' + str(self.api_error))

        print('Step14: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加MX类型记录解析结果优先级和域名都不合法')
        payload14 = {
            "domain": domain1,
            "host": "m6",
            "type": "MX",
            "result": {"preference": 67000, "data": "#@mail_.test.com"}
        }
        r14 = self.post(url=url1, json=payload14, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code14, res14 = r14
            if not (status_code14 == 400 and res14['code'] == "InvalidParam"):
                self.exception.add('Step14: ' + str(res14))
        else:
            self.exception.add('Step14: ' + str(self.api_error))

        print('Step15: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加MX类型记录解析结果缺少优先级')
        payload15 = {
            "domain": domain1,
            "host": "m7",
            "type": "MX",
            "result": {"data": "mail_.test.com"}
        }
        r15 = self.post(url=url1, json=payload15, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code15, res15 = r15
            if not (status_code15 == 400 and res15['code'] == "InvalidResourceResult"):
                self.exception.add('Step15: ' + str(res15))
        else:
            self.exception.add('Step15: ' + str(self.api_error))

        print('Step16: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加MX类型记录解析结果缺少优先级')
        payload16 = {
            "domain": domain1,
            "host": "m8",
            "type": "MX"
        }
        r16 = self.post(url=url1, json=payload16, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code16, res16 = r16
            if not (status_code16 == 400 and res16['code'] == "InvalidResourceResult"):
                self.exception.add('Step16: ' + str(res16))
        else:
            self.exception.add('Step16: ' + str(self.api_error))