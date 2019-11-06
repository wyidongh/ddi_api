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

    def test_add_auth_record_repeatability_check(self):


        print('Step1: 点击【域管理】在node1下的default视图，添加test.com')
        domain1 = "test.com"
        ns_name1 = "ns." + domain1
        self.authorization_add_standard_domain(domainname=domain1, nodename=self.nodename[0], viewname='default',
                                               ns_name=ns_name1, ns_ip=self.serverip[0])

        print('Step2: 点击【记录管理】，添加n1.test.com的AAAA记录为1111:0000::2')
        self.authorization_add_aaaa_record(nodename=self.nodename[0],domain=domain1,host="n1",res="1111:0000::2")


        url1 = "https://" + self.serverip[0] + ":19393/api/dns/records"

        print('Step3: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加AAAA记录的解析结果与步骤2相同，只是缩写格式不同')
        payload3 = {
                    "domain": domain1,
                    "host": "n1",
                    "type": "AAAA",
                    "result": {"data": "1111::2"}
                    }
        r3 = self.post(url=url1, json=payload3, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code3, res3 = r3
            if not (status_code3 == 400 and res3['code'] == "InvalidParam"):
                self.exception.add('Step3: ' + str(res3))
        else:
            self.exception.add('Step3: ' + str(self.api_error))


        print('Step4: 点击【记录管理】，添加n2.test.com的A记录为1.1.1.1，权重为1，ttl为100')
        self.authorization_add_a_record(nodename=self.nodename[0],domain=domain1,host="n2",res="1.1.1.1",ttl="100",weight="1")



        print('Step5: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加A记录的解析结果与步骤4相同，ttl值不同')
        payload5 = {
                    "domain": domain1,
                    "host": "n2",
                    "type": "A",
                    "result": {"data": "1.1.1.1"},
                    "ttl": 200
                    }
        r5 = self.post(url=url1, json=payload5, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code5, res5 = r5
            if not (status_code5 == 400 and res5['code'] == "InvalidParam"):
                self.exception.add('Step5: ' + str(res5))
        else:
            self.exception.add('Step5: ' + str(self.api_error))

        print('Step6: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加A记录的解析结果与步骤4相同，权重值不同')
        payload6 = {
                    "domain": domain1,
                    "host": "n2",
                    "type": "A",
                    "result": {"data": "1.1.1.1"},
                    "weight": 2
                    }
        r6 = self.post(url=url1, json=payload6, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code6, res6 = r6
            if not (status_code6 == 400 and res6['code'] == "InvalidParam"):
                self.exception.add('Step6: ' + str(res6))
        else:
            self.exception.add('Step6: ' + str(self.api_error))

        print('Step7: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加A记录的解析结果与步骤4完全相同')
        payload7 = {
                    "domain": domain1,
                    "host": "n2",
                    "type": "A",
                    "result": {"data": "1.1.1.1"},
                    "weight": 1,
                    "ttl": 100
                    }
        r7 = self.post(url=url1, json=payload7, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code7, res7 = r7
            if not (status_code7 == 400 and res7['code'] == "InvalidParam"):
                self.exception.add('Step7: ' + str(res7))
        else:
            self.exception.add('Step7: ' + str(self.api_error))


        print('Step8: 点击【记录管理】，添加t1.test.com的A记录为1.1.1.1')
        self.authorization_add_a_record(nodename=self.nodename[0], domain=domain1, host="t1", res="1.1.1.1")

        print('Step9: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加主机名为t1的CNAME记录')
        payload9 = {
                    "domain": domain1,
                    "host": "t1",
                    "type": "CNAME",
                    "result": {"data": "www.qq.com"}
                    }
        r9 = self.post(url=url1, json=payload9, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code9, res9 = r9
            if not (status_code9 == 400 and res9['code'] == "InvalidParam"):
                self.exception.add('Step9: ' + str(res9))
        else:
            self.exception.add('Step9: ' + str(self.api_error))

        print('Step10: 点击【记录管理】，添加t5.test.com的cname记录为www.qq.com')
        self.authorization_add_cname_record(nodename=self.nodename[0],domain=domain1,host="t5",res="www.qq.com")


        print('Step11: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加主机名为t5的非CNAME记录')
        payload11 = {
                    "domain": domain1,
                    "host": "t5",
                    "type": "AAAA",
                    "result": {"data": "11::22"}
                    }
        r11 = self.post(url=url1, json=payload11, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code11, res11 = r11
            if not (status_code11 == 400 and res11['code'] == "InvalidParam"):
                self.exception.add('Step11: ' + str(res11))
        else:
            self.exception.add('Step11: ' + str(self.api_error))

        print('Step12: 点击【记录管理】，添加t6.test.com的A类型的记录为1.1.1.1，状态为启用')
        self.authorization_add_a_record(nodename=self.nodename[0], domain=domain1, host="t6", res="1.1.1.1")

        print('Step13: 用POST方法调用接口https://192.168.6.62:19393/api/dns/records，添加和步骤12相同的记录，状态为暂停')
        payload13 = {
                    "domain": domain1,
                    "host": "t6",
                    "type": "A",
                    "result": {"data": "1.1.1.1"},
                    "status": 0
                    }
        r13 = self.post(url=url1, json=payload13, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code13, res13 = r13
            if not (status_code13 == 400 and res13['code'] == "InvalidParam"):
                self.exception.add('Step13: ' + str(res13))
        else:
            self.exception.add('Step13: ' + str(self.api_error))
