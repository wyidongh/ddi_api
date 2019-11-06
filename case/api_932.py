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
        sleep(1.5)
        self.ipSegment_management_delete_all_ipSegment()
        sleep(1)
        print('删除dhcp节点')
        self.dhcp_node_delete_all_node()
        print('删除api用户')
        self.delete_api_user()
        print("删除所有DNS节点")
        self.dns_node_delete_all_node()
        if self.exception:
            raise Exception(self.exception)

    def test_query_dhcp_subnet_with_id(self):

        url = "https://" + self.serverip[0] + ":19393/api/dhcp/subnet"
        p1 = {
            "nodeName": self.dhcpnode[0],
            "ip": "172.0.0.0",
            "mask": 16,
            "version": 4,
            "gateway": "172.0.0.1",
            "dns": "172.0.0.2",
            "lease": 60
        }
        self.post(url=url, json=p1, auth=(self.api_user, self.api_password))


        print('Step1: 用GET方法调用接口https://192.168.6.82:19393/api/dhcp/subnet/5c52648176dbe0bc75f8df54查询存在的指定id的subnet')
        payload1 = {
            "ip": "172.0.0.0"
        }
        r1 = self.get(url=url, params=payload1, auth=(self.api_user,self.api_password))
        id = ""
        if self.api_error is None:
            status_code1,res1 = r1
            if not (status_code1 == 200 and res1['code'] == "Success" and len(res1['data']) == 1):
                self.exception.add('Step1a: ' + str(r1))
            id = res1['data'][0].get('id')
        else:
            self.exception.add('Step1a: ' + str(self.api_error))

        url2 = url + "/" + id
        r2 = self.get(url=url2, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code2,res2 = r2
            if not (status_code2 == 200 and res2['code'] == "Success" and res2['data'] is not None):
                self.exception.add("Step1b: " + str(r2))
        else:
            self.exception.add('Step1b: ' + self.api_error)

        url3 = url + "/1111111"
        print('Step2: 用GET方法调用接口https://192.168.6.82:19393/api/dhcp/subnet/11111111查询不存在的指定id的subnet')
        r3 = self.get(url=url3, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code3, res3 = r3
            if not (status_code3 == 400 and res3['code'] == "InvalidParam"):
                self.exception.add('Step2: ' + str(r3))
        else:
            self.exception.add('Step2: ' + str(self.api_error))