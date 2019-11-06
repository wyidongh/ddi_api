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

    def test_add_auth_record_PTR_result_validation_check(self):


        print('Step1: 点击【域管理】在node1下的default视图，添加反向域3.2.1.in-addr.arpa和a.9.8.7.6.5.0.4.0.0.0.3.0.0.0.2.0.0.0.1.0.0.0.0.0.0.0.1.2.3.4.ip6.arpa')

        domain1 = "test.com"
        ns_name1 = "ns." + domain1
        self.authorization_add_standard_domain(domainname=domain1, nodename=self.nodename[0], viewname='default',
                                               ns_name=ns_name1, ns_ip=self.serverip[0])

        domain_a = "3.2.1"
        arpa_type1 = "in-addr.arpa"
        reverse_domain1 = domain_a + "." + arpa_type1
        self.authorization_add_reverse_domain(domainname=domain_a, arpa_type=arpa_type1,
                                              nodename=self.nodename[0],
                                              ns_name=ns_name1)
        domain_b = "a.9.8.7.6.5.0.4.0.0.0.3.0.0.0.2.0.0.0.1.0.0.0.0.0.0.0.1.2.3.4"
        arpa_type2 = "ip6.arpa"
        reverse_domain2 = domain_b + "." + arpa_type2
        self.authorization_add_reverse_domain(domainname=domain_b, arpa_type=arpa_type2,
                                              nodename=self.nodename[0],
                                              ns_name=ns_name1)

        url1 = "https://" + self.serverip[0] + ":19393/api/dns/records"

        print('Step2: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加ipv4反向域的PTR类型记录解析结果正确')
        payload2 = {
                    "domain": reverse_domain1,
                    "host": "4",
                    "type": "PTR",
                    "result": {"data": "p4.test.com"}
                    }
        r2 = self.post(url=url1, json=payload2, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code2, res2 = r2
            if not (status_code2 == 200 and res2['code'] == "Success"):
                self.exception.add('Step2: ' + str(res2))
        else:
            self.exception.add('Step2: ' + str(self.api_error))



        print('Step3: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加ipv6反向域的PTR类型记录解析结果正确')
        payload3 = {
                    "domain": reverse_domain2,
                    "host": "b",
                    "type": "PTR",
                    "result": {"data": "p4.test.com"}
                    }
        r3 = self.post(url=url1, json=payload3, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code3, res3 = r3
            if not (status_code3 == 200 and res3['code'] == "Success"):
                self.exception.add('Step3: ' + str(res3))
        else:
            self.exception.add('Step3: ' + str(self.api_error))


        print('Step4: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加ipv4反向域的PTR类型记录解析结果为一级域')
        payload4 = {
                    "domain": reverse_domain1,
                    "host": "10",
                    "type": "PTR",
                    "result": {"data": "org"}
                    }
        r4 = self.post(url=url1, json=payload4, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code4, res4 = r4
            if not (status_code4 == 200 and res4['code'] == "Success"):
                self.exception.add('Step4: ' + str(res4))
        else:
            self.exception.add('Step4: ' + str(self.api_error))


        print('Step5: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加ipv4反向域的PTR类型记录解析结果为根')
        payload5 = {
                    "domain": reverse_domain1,
                    "host": "20",
                    "type": "PTR",
                    "result": {"data": "."}
                    }
        r5 = self.post(url=url1, json=payload5, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code5, res5 = r5
            if not (status_code5 == 200 and res5['code'] == "Success"):
                self.exception.add('Step5: ' + str(res5))
        else:
            self.exception.add('Step5: ' + str(self.api_error))

        print('Step6: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加ipv4反向域的PTR类型记录解析结果为空')
        payload6 = {
                    "domain": reverse_domain1,
                    "host": "30",
                    "type": "PTR",
                    "result": {"data": ""}
                    }
        r6 = self.post(url=url1, json=payload6, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code6, res6 = r6
            if not (status_code6 == 400 and res6['code'] == "InvalidParam"):
                self.exception.add('Step6: ' + str(res6))
        else:
            self.exception.add('Step6: ' + str(self.api_error))

        print('Step7: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加ipv4反向域的PTR类型记录解析结果为非法域名')
        payload7 = {
                    "domain": reverse_domain1,
                    "host": "30",
                    "type": "PTR",
                    "result": {"data": "^-_test.com"}
                    }
        r7 = self.post(url=url1, json=payload7, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code7, res7 = r7
            if not (status_code7 == 400 and res7['code'] == "InvalidParam"):
                self.exception.add('Step7: ' + str(res7))
        else:
            self.exception.add('Step7: ' + str(self.api_error))

        print('Step8: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，正向域配置')
        payload8 = {
            "domain": domain1,
            "host": "30",
            "type": "PTR",
            "result": {"data": "1.test.com"}
        }
        r8 = self.post(url=url1, json=payload7, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code8, res8 = r8
            if not (status_code8 == 400 and res8['code'] == "InvalidParam"):
                self.exception.add('Step8: ' + str(res8))
        else:
            self.exception.add('Step8: ' + str(self.api_error))