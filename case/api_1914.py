#coding:utf-8
from unittest import TestCase
from time import sleep
from selenium import webdriver
from basic.assist import Tools
from basic.system import system
from basic.ipam import ipam
from basic.ddi_api import ddi_api
from basic.resource import resource

class RunTest(TestCase, Tools, system, ipam, ddi_api, resource):
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
        print('为节点%s添加api用户%s' % (self.nodename, self.api_user))
        self.add_api_user(self.nodename[0], self.api_user, self.api_password)
        sleep(3)
    def tearDown(self):
        self.ipSegment_management_delete_all_ipSegment()
        self.delete_api_user()
        print("删除所有DNS节点")
        self.dns_node_delete_all_node()
        if self.exception:
            raise Exception(self.exception)

    def test_ipam_delete_addr_status_validation_check(self):

        ipsegment = "192.168.16.0/24"
        ip = ipsegment.split("/")[0]
        mask = ipsegment.split("/")[1]
        print('在页面【IPAM】-【ip地址段】，点击新增一个IP地址段192.168.16.0/24')
        self.ipSegment_management_add_ip_segment(ip=ip, type="IPV4", mask=mask)

        print('在页面【IPAM】-【ip段配置】-【ip段配置】，在17.0段后面点击配置按钮，为期配置网段、dns、租约等信息')
        self.ipSegment_configure_configrure_ip_segment(ipsegment=ipsegment, gateway="192.168.16.1", dns="192.168.6.2")

        sleep(4)

        url = "https://" + self.serverip[0] + ":19393/api/ipam/ipstatus/name"

        print('Step2: 在postman上面 DELETE https://192.168.16.109:19393/api/ipam/ipstatus/name?ipSegment=192.168.333.0/24&ip=192.168.333.100,删除指定的ip地址状态')
        payload2 = {"ipSegment":"192.168.333.0/24",
                   "ip":"192.168.333.108"}

        r2 = self.delete(url=url, params=payload2, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code2, res2 = r2
            if not (status_code2 == 400 and res2['code'] == "InvalidIPSegment"):
                self.exception.add("Step2: " + str(r2))
        else:
            self.exception.add('Step2: ' + str(self.api_error))


        print('Step3: 在postman上面 DELETE https://192.168.16.109:19393/api/ipam/ipstatus/name?ipSegment=192.168.15.0/24&ip=192.168.15.100,删除指定的ip地址状态' )
        payload3 = {"ipSegment": "192.168.15.0/24",
                    "ip": "192.168.15.108"}
        r3 = self.delete(url=url, params=payload3, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code3, res3 = r3
            if not (status_code3 == 400 and res3['code'] == "IPSegmentNotExist"):
                self.exception.add("Step3: " + str(r3))
        else:
            self.exception.add('Step3: ' + str(self.api_error))

        print('Step4: 在postman上面 DELETE https://192.168.16.109:19393/api/dns/ipstatus/name?ipSegment=192.168.16.0/24&ip=192.168.16.345,删除指定的ip地址状态')

        payload4 = {"ipSegment": "192.168.16.0/24",
                    "ip": "192.168.16.345"}
        r4 = self.delete(url=url, params=payload4, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code4, res4 = r4
            if not (status_code4 == 400 and res4['code'] == "InvalidIP"):
                self.exception.add("Step4: " + str(r4))
        else:
            self.exception.add('Step4: ' + str(self.api_error))

        print('Step5: 在postman上面 DELETE https://192.168.16.109:19393/api/ipam/ipstatus/name?ipSegment=192.168.16.0/24&ip=192.168.15.13,删除指定的ip地址状态')

        payload5 = {"ipSegment": "192.168.16.0/24",
                    "ip": "192.168.15.34"}
        r5 = self.delete(url=url, params=payload5, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code5, res5 = r5
            if not (status_code5 == 400 and res5['code'] == "IPNotExist"):
                self.exception.add("Step5: " + str(r5))
        else:
            self.exception.add('Step5: ' + str(self.api_error))

        print('Step6: 在postman上面 DELETE https://192.168.16.109:19393/api/ipam/ipstatus/name?ipSegment=192.168.16.0/24&ip=192.168.16.100,删除指定的ip地址状态')

        payload6 = {"ipSegment": "192.168.16.0/24",
                    "ip": "192.168.16.99"}
        r6 = self.delete(url=url, params=payload6, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code6, res6 = r6
            if not (status_code6 == 400 and res6['code'] == "SwitchInfoNotExisted"):
                self.exception.add("Step6: " + str(r6))
        else:
            self.exception.add('Step6: ' + str(self.api_error))















