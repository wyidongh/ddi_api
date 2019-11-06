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

    def test_add_auth_record_status_validation_check(self):

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


        domain2 = "yamu.com"
        ns_name2 = "ns." + domain2
        self.authorization_add_standard_domain(domainname=domain2, nodename=self.nodename[1], viewname='default',
                                               ns_name=ns_name2, ns_ip=self.serverip[0])


        url1 = "https://" + self.serverip[0] + ":19393/api/dns/records"

        print('Step3: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，status为0')
        payload3 = {
                    "domain": domain1,
                    "host": "d1",
                    "result": {"data": "1.1.1.1"},
                    "status": 0
                    }

        r3 = self.post(url=url1,json=payload3,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code3,res3 = r3
            if not (status_code3 == 200 and res3['code'] == "Success"):
                self.exception.add('Step3: ' + str(res3))
        else:
            self.exception.add('Step3: ' + str(self.api_error))


        print('Step4: 点击【记录管理】，查看步骤3添加的记录的状态')
        sleep(20)
        self.query(service=self.serverip[0], qname="d1." + domain1, rdtype="A")
        if  self.error is None:
            self.exception.add('Step4: 记录未禁用')


        print('Step5: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，status为1')
        payload5 = {
                    "domain": domain1,
                    "host": "d2",
                    "result": {"data": "1.1.1.1"},
                    "status": 1
                    }
        r5 = self.post(url=url1, json=payload5, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code5, res5 = r5
            if not (status_code5 == 200 and res5['code'] == "Success"):
                self.exception.add('Step5: ' + str(res5))
        else:
            self.exception.add('Step5: ' + str(self.api_error))

        sleep(20)
        print('Step6: 点击【记录管理】，查看步骤5添加的记录的状态')
        self.query(service=self.serverip[0],qname="d2." + domain1,rdtype="A")
        if not self.error is None or not '1.1.1.1' in self.short:
            self.exception.add('Step6: A类型解析错误' )

        print('Step7: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，status为2')
        payload7 = {
                    "domain": domain1,
                    "host": "d3",
                    "result": {"data": "1.1.1.1"},
                    "status": 2
                    }
        r7 = self.post(url=url1, json=payload7, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code7, res7 = r7
            if not (status_code7 == 400 and res7['code'] == "InvalidStatus"):
                self.exception.add('Step7: ' + str(res7))
        else:
            self.exception.add('Step7: ' + str(self.api_error))

        print('Step8: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，status为-1')
        payload8 = {
            "domain": domain1,
            "host": "d4",
            "result": {"data": "1.1.1.1"},
            "status": -1
        }
        r8 = self.post(url=url1, json=payload8, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code8, res8 = r8
            if not (status_code8 == 400 and res8['code'] == "InvalidStatus"):
                self.exception.add('Step8: ' + str(res8))
        else:
            self.exception.add('Step8: ' + str(self.api_error))



