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
        self.view_delete_all_view()
        self.view_delete_all_addr_group()
        self.delete_api_user()
        print("删除所有DNS节点")
        self.dns_node_delete_all_node()
        if self.exception:
            raise Exception(self.exception)

    def test_add_auth_records_with_optional_parameter(self):

        print('Step1: 在节点node1下添加视图v1')
        view1 = "v1"
        group1 = "group1"
        self.view_add_addr_group(gname=group1, ip="192.168.1.0", mask="24")
        self.view_add_view(nodename=self.nodename[0], gname=group1, view=view1)

        print('Step2: 点击【域管理】在node1下的default和v1视图，分别添加域test.com，在node2下添加yamu.com')
        domain1 = "test.com"
        ns_name1 = "ns." + domain1
        self.authorization_add_standard_domain(domainname=domain1, nodename=self.nodename[0], viewname='default',
                                               ns_name=ns_name1, ns_ip=self.serverip[0])

        self.authorization_add_standard_domain(domainname=domain1, nodename=self.nodename[0], viewname=view1,
                                               ns_name=ns_name1, ns_ip=self.serverip[0])

        reverse_domain = "3.2.1.in-addr.arpa"
        self.authorization_add_reverse_domain(domainname=reverse_domain[0:5], arpa_type="in-addr.arpa",
                                              nodename=self.nodename[0],
                                              ns_name=ns_name1)

        domain2 = "yamu.com"
        ns_name2 = "ns." + domain2
        self.authorization_add_standard_domain(domainname=domain2, nodename=self.nodename[1], viewname='default',
                                               ns_name=ns_name2, ns_ip=self.serverip[0])



        url1 = "https://" + self.serverip[0] + ":19393/api/dns/records"

        print('Step3: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，指定的节点名存在')
        payload3 = {
                    "nodeName": self.nodename[0],
                    "domain": domain1,
                    "host": "a1",
                    "result": {"data": "1.1.1.1"}
                    }

        r3 = self.post(url=url1,json=payload3,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code3,res3 = r3
            if not (status_code3 == 200 and res3['code'] == "Success"):
                self.exception.add('Step3: ' + str(res3))
        else:
            self.exception.add('Step3: ' + str(self.api_error))

        print('Step4: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，指定的节点名存在且不是api用户所在的默认节点')
        payload4 = {
                    "nodeName": self.nodename[1],
                    "domain": domain2,
                    "host": "a1",
                    "result": {"data": "1.1.1.1"}
                    }
        r4 = self.post(url=url1, json=payload4, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code4, res4 = r4
            if not (status_code4 == 200 and res4['code'] == "Success"):
                self.exception.add('Step4: ' + str(res4))
        else:
            self.exception.add('Step4: ' + str(self.api_error))

        print('Step5: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，指定的节点名不存在')
        payload5 = {
            "nodeName": "node3",
            "domain": domain1,
            "host": "a2",
            "result": {"data": "1.1.1.1"}
        }
        r5 = self.post(url=url1, json=payload5, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code5, res5 = r5
            if not (status_code5 == 400 and res5['code'] == "NodeNotExisted"):
                self.exception.add('Step5: ' + str(res5))
        else:
            self.exception.add('Step5: ' + str(self.api_error))

        print('Step6: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，指定的视图存在')
        payload6 = {
            "viewName": "default",
            "domain": domain1,
            "host": "a2",
            "result": {"data": "1.1.1.1"}
        }
        r6 = self.post(url=url1, json=payload6, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code6, res6 = r6
            if not (status_code6 == 200 and res6['code'] == "Success"):
                self.exception.add('Step6: ' + str(res6))
        else:
            self.exception.add('Step6: ' + str(self.api_error))

        print('Step7: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，指定的视图不存在')
        payload7 = {
            "viewName": "v123",
            "domain": domain1,
            "host": "a2",
            "result": {"data": "1.1.1.1"}
        }
        r7 = self.post(url=url1, json=payload7, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code7, res7 = r7
            if not (status_code7 == 400 and res7['code'] == "InvalidParam"):
                self.exception.add('Step7: ' + str(res7))
        else:
            self.exception.add('Step7: ' + str(self.api_error))

        print('Step8: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加A类型的记录')
        payload8 = {
            "domain": domain1,
            "type": "A",
            "host": "a3",
            "result": {"data": "1.1.1.1"}
        }
        r8 = self.post(url=url1, json=payload8, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code8, res8 = r8
            if not (status_code8 == 200 and res8['code'] == "Success"):
                self.exception.add('Step8: ' + str(res8))
        else:
            self.exception.add('Step8: ' + str(self.api_error))

        print('Step9: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加AAAA类型的记录')
        payload9 = {
            "domain": domain1,
            "type": "AAAA",
            "host": "a3",
            "result": {"data": "11::"}
        }
        r9 = self.post(url=url1, json=payload9, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code9, res9 = r9
            if not (status_code9 == 200 and res9['code'] == "Success"):
                self.exception.add('Step9: ' + str(res9))
        else:
            self.exception.add('Step9: ' + str(self.api_error))

        print('Step10: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加CNAME类型的记录')
        payload10 = {
            "domain": domain1,
            "type": "CNAME",
            "host": "a4",
            "result": {"data": "www.test.com"}
        }
        r10 = self.post(url=url1, json=payload10, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code10, res10 = r10
            if not (status_code10 == 200 and res10['code'] == "Success"):
                self.exception.add('Step10: ' + str(res10))
        else:
            self.exception.add('Step10: ' + str(self.api_error))

        print('Step11: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加NS类型的记录')
        payload11 = {
            "domain": domain1,
            "type": "NS",
            "host": "a5",
            "result": {"data": "ns.yamu.com"}
        }
        r11 = self.post(url=url1, json=payload11, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code11, res11 = r11
            if not (status_code11 == 200 and res11['code'] == "Success"):
                self.exception.add('Step11: ' + str(res11))
        else:
            self.exception.add('Step11: ' + str(self.api_error))

        print('Step12: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加NX类型的记录')
        payload12 = {
            "domain": domain1,
            "type": "MX",
            "host": "a6",
            "result": {"preference": 10,
                        "data": "mail.test.com"}
                        }
        r12 = self.post(url=url1, json=payload12, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code12, res12 = r12
            if not (status_code12 == 200 and res12['code'] == "Success"):
                self.exception.add('Step12: ' + str(res12))
        else:
            self.exception.add('Step12: ' + str(self.api_error))

        print('Step13: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，反向域添加PTR类型的记录')
        payload13 = {
            "domain": reverse_domain,
            "type": "PTR",
            "host": "4",
            "result": {"data": "4.test.com"}
        }
        r13 = self.post(url=url1, json=payload13, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code13, res13 = r13
            if not (status_code13 == 200 and res13['code'] == "Success"):
                self.exception.add('Step13: ' + str(res13))
        else:
            self.exception.add('Step13: ' + str(self.api_error))

        print('Step14: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，正向域添加PTR类型的记录')
        payload14 = {
            "domain": domain1,
            "type": "PTR",
            "host": "4",
            "result": {"data": "4.test.com"}
        }
        r14 = self.post(url=url1, json=payload14, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code14, res14 = r14
            if not (status_code14 == 400 and res14['code'] == "InvalidResourceType"):
                self.exception.add('Step14: ' + str(res14))
        else:
            self.exception.add('Step14: ' + str(self.api_error))

        print('Step15: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，反向域添加AAAA类型的记录')
        payload15 = {
            "domain": reverse_domain,
            "type": "AAAA",
            "host": "4",
            "result": {"data": "11::"}
        }
        r15 = self.post(url=url1, json=payload15, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code15, res15 = r15
            if not (status_code15 == 400 and res15['code'] == "InvalidResourceType"):
                self.exception.add('Step15: ' + str(res15))
        else:
            self.exception.add('Step15: ' + str(self.api_error))

        print('Step16: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，正向域添加接口不支持的资源类型的记录DNAME')
        payload16 = {
            "domain": domain1,
            "type": "DNAME",
            "host": "4",
            "result": {"data": "yamu.com"}
        }
        r16 = self.post(url=url1, json=payload16, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code16, res16 = r16
            if not (status_code16 == 400 and res16['code'] == "InvalidResourceType"):
                self.exception.add('Step16: ' + str(res16))
        else:
            self.exception.add('Step16: ' + str(self.api_error))