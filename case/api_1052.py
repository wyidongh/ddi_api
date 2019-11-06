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

    def test_delete_domain_with_name(self):
        print('授权管理】-【域管理】中在node1下添加域yamu.com和反向 域3.2.1.in-addr.arpa,test视图下面添加yamu.com')
        view1 = "test"
        group1 = "group1"
        self.view_add_addr_group(gname=group1, ip="192.168.6.0", mask="24")
        self.view_add_view(nodename=self.nodename[0], gname=group1, view=view1)

        domain1 = "test.com"
        ns_name1 = "ns." + domain1
        domain2 = "abc.com"
        ns_name2 = "ns." + domain2
        self.authorization_add_standard_domain(domainname=domain1, nodename=self.nodename[0], viewname='default',
                                               ns_name=ns_name1, ns_ip=self.serverip[0])

        self.authorization_add_standard_domain(domainname=domain1, nodename=self.nodename[0], viewname=view1,
                                               ns_name=ns_name1, ns_ip=self.serverip[0])

        self.authorization_add_standard_domain(domainname=domain1, nodename=self.nodename[1], viewname='default',
                                               ns_name=ns_name1, ns_ip=self.serverip[0])

        self.authorization_add_standard_domain(domainname=domain2, nodename=self.nodename[1], viewname='default',
                                               ns_name=ns_name2, ns_ip=self.serverip[0])


        domain_a = "3.2.1"
        arpa_type = "in-addr.arpa"
        reverse_domain = domain_a + "." + arpa_type
        self.authorization_add_reverse_domain(domainname=domain_a, arpa_type=arpa_type,nodename=self.nodename[0],ns_name=ns_name1,viewname=view1)

        sleep(3)
        url1 = "https://" + self.serverip[0] + ":19393/api/dns/zones/name"

        print('Step1: 在postman工具中使用DELETE方法调用https://192.168.16.109:19393/api/dns/zones/name?domain=test.com接口')
        payload1 = {
                    "domain": domain1
                    }
        r1 = self.delete(url=url1, params=payload1, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code1, res1 = r1
            if not (status_code1 == 200 and res1['code'] == "Success"):
                self.exception.add("Step1: " + str(r1))
        else:
            self.exception.add('Step1: ' + str(self.api_error))

        print('Step2: 在postman工具中使用DELETE方法调用https://192.168.16.109:19393/api/dns/zones/name?viewName=test&domain=test.com接口')
        payload2 = {
            "viewName": view1,
            "domain": domain1
        }
        r2 = self.delete(url=url1, params=payload2, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code2, res2 = r2
            if not (status_code2 == 200 and res2['code'] == "Success"):
                self.exception.add("Step2: " + str(r2))
        else:
            self.exception.add('Step2: ' + str(self.api_error))

        print('Step3: 在postman工具中使用DELETE方法调用https://192.168.16.109:19393/api/dns/zones/name?viewName=test&domain=3.2.1.in-addr.arpa接口')
        payload3 = {
            "viewName": view1,
            "domain": reverse_domain
        }
        r3 = self.delete(url=url1, params=payload3,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code3,res3 = r3
            if not (status_code3 == 200 and res3['code'] == "Success"):
                self.exception.add('Step3: ' + str(r3))
        else:
            self.exception.add('Step3: ' + str(self.api_error))

        print('Step4: 在postman工具中使用DELETE方法调用https://192.168.16.109:19393/api/dns/zones/name?nodeName=node2&domain=test.com接口')
        payload4 = {
            "nodeName": self.nodename[1],
            "domain": domain1
        }
        r4 = self.delete(url=url1,params=payload4,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code4,res4 = r4
            if not (status_code4 == 200 and res4['code'] == "Success"):
                self.exception.add("Step4: " + str(r4))
        else:
            self.exception.add('Step4: ' + str(self.api_error) )


        print('Step5: 在postman工具中使用DELETE方法调用https://192.168.16.109:19393/api/dns/zones/name?nodeName=node2&domain=ABc.com')
        payload5 = {
                    "nodeName":self.nodename[1],
                    "domain": domain2
                    }
        r5 = self.delete(url=url1,params=payload5,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code5,res5 = r5
            if not (status_code5 == 200 and res5['code'] == "Success"):
                self.exception.add('Step5: ' + str(r5))
        else:
            self.exception.add('Step5: ' + str(self.api_error))


        print('Step6: 在postman工具中使用DELETE方法调用https://192.168.16.109:19393/api/dns/zones/name?nodeName=node3&domain=abc.com接口')
        payload6 = {
                    "nodeName":"node10",
                    "domain": "abc.com"
                    }
        r6 = self.delete(url=url1, params=payload6,auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code6, res6 = r6
            if not (status_code6 == 400 and res6['code'] == "NodeNotExisted"):
                self.exception.add('Step6: ' + str(r6))
        else:
            self.exception.add('Step6: ' + str(self.api_error))


        print('Step7: 在postman工具中使用DELETE方法调用https://192.168.16.109:19393/api/dns/zones/name?viewName=test10&domain=abc.com接口')
        payload7 = {
                    "viewName":"test10",
                    "domain": "abc.com"
                    }
        r7 = self.delete(url=url1, params=payload7, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code7, res7 = r7
            if not (status_code7 == 400 and res7['code'] == "ViewNotExisted"):
                self.exception.add('Step7: ' + str(r7))
        else:
            self.exception.add('Step7: ' + str(self.api_error))


        print('Step8: 在postman工具中使用DELETE方法调用https://192.168.16.109:19393/api/dns/zones/name?domain=testaaa.com接口')
        payload8 = {
                    "domain": "testaaa.com"
                    }
        r8 = self.delete(url=url1, params=payload8, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code8, res8 = r8
            if not (status_code8 == 400 and res8['code'] == "ZoneNotExisted"):
                self.exception.add('Step8: ' + str(r8))
        else:
            self.exception.add('Step8: ' + str(self.api_error))


        # print('Step9: 在postman工具中使用DELETE方法调用https://192.168.16.109:19393/api/dns/zones/name?view=test&domain=test.com接')
        # payload9 = {
        #             "viewName": view1,
        #             "domain": domain1,
        #             "update": {
        #             "comment": "test&#x5907;&#x6CE8;"
        #             }
        #             }
        # r9 = self.put(url=url1, json=payload9, auth=(self.api_user, self.api_password))
        # if self.api_error is None:
        #     status_code9, res9 = r9
        #     if not (status_code9 == 200 and res9['code'] == "Success"):
        #         self.exception.add("Step9: " + str(r9))
        # else:
        #     self.exception.add('Step9: ' + str(self.api_error))
        #
        #
        # print('Step10: ')
        # payload10 = {
        #             "domain": domain1,
        #             "update": {
        #             "comment": "a" * 100
        #             }
        #             }
        # r10 = self.put(url=url1, json=payload10, auth=(self.api_user, self.api_password))
        # if self.api_error is None:
        #     status_code10, res10 = r10
        #     if not (status_code10 == 200 and res10['code'] == "Success"):
        #         self.exception.add('Step10: ' + str(r10))
        # else:
        #     self.exception.add('Step10: ' + str(self.api_error))
        #
        # print('Step11: ')
        # payload11 = payload10 = {
        #             "domain": domain1,
        #             "update": {
        #             "comment": "a" * 101
        #             }
        #             }
        # r11 = self.put(url=url1, json=payload11, auth=(self.api_user, self.api_password))
        # if self.api_error is None:
        #     status_code11, res11 = r11
        #     if not (status_code11 == 400 and res11['code'] == "InvalidComment"):
        #         self.exception.add('Step11: ' + str(r11))
        # else:
        #     self.exception.add('Step11: ' + str(self.api_error))
