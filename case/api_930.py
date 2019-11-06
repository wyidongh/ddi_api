#coding:utf-8
from unittest import TestCase
from time import sleep
from selenium import webdriver
from basic.assist import Tools
from basic.dhcp import dhcp
from basic.resource import resource
from basic.ipam import ipam
from basic.ddi_api import ddi_api
from basic.system import system

class RunTest(TestCase, Tools, resource, dhcp, ipam, ddi_api,system):
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
        print('添加dhcp节点')
        self.dhcp_node_add_dhcp_single_node(self.dhcpnode[0],device=self.devices[0])
        self.dhcp_node_add_dhcp_single_node(self.dhcpnode[1], device=self.devices[1])
        print('为节点%s添加api用户%s' % (self.nodename, self.api_user))
        self.add_api_user(self.nodename[0], self.api_user, self.api_password)
        sleep(3)

    def tearDown(self):
        self.ipSegment_management_delete_all_ipSegment()
        print('删除dhcp节点')
        self.dhcp_node_delete_all_node()
        print('删除api用户')
        self.delete_api_user()
        print("删除所有DNS节点")
        self.dns_node_delete_all_node()
        if self.exception:
            raise Exception(self.exception)

    def test_delete_specific_dhcp_subnet(self):

        url = "https://" + self.serverip[0] + ":19393/api/dhcp/subnet"

        print('Step1: 用POST方法调用接口https://192.168.6.82:19393/api/dhcp/subnet，添加nodeName为“dhcp1”，ip为ipv4的策略')
        ip1 = "192.168.1.0"
        mask1 = 24
        gateway1 = "192.168.1.1"
        dns1 = "192.168.1.2"
        payload1 = {
            "nodeName": self.dhcpnode[0],
            "ip": ip1,
            "mask": mask1,
            "version": 4,
            "gateway": gateway1,
            "dns": dns1,
            "lease": 60
        }

        r1 = self.post(url=url,json=payload1,auth=(self.api_user,self.api_password))
        id = ""
        if self.api_error is None:
            status_code1,res1 = r1
            if not (status_code1 == 200 and res1['code'] == "Success"):
                self.exception.add('Step1: ' + str(r1))
            id = res1['data']
        else:
            self.exception.add('Step1: ' + str(self.api_error))

        print('Step2: 用DELETE方法调用接口https://192.168.6.82:19393/api/dhcp/subnet/:id，删除步骤1中的id号的subnet')
        url2 = url + "/" + str(id)

        r2 = self.delete(url=url2,  auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code2, res2 = r2
            if not (status_code2 == 200 and res2['code'] == "Success"):
                self.exception.add('Step2: ' + str(r2))
        else:
            self.exception.add('Step2: ' + str(self.api_error))

        print('Step3: 用DELETE方法调用接口https://192.168.6.82:19393/api/dhcp/subnet/:id，删除一个不存在的id号的subnet')
        url3 = url + "/111111"
        r3 = self.delete(url=url3, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code3, res3 = r3
            if not (status_code3 == 400 and res3['code'] == "InvalidParam"):
                self.exception.add('Step3: ' + str(r3))
        else:
            self.exception.add('Step3: ' + str(self.api_error))