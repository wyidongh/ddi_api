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

    def test_query_dhcp_subnet_list(self):

        url = "https://" + self.serverip[0] + ":19393/api/dhcp/subnet"

        p1 = {
            "nodeName": self.dhcpnode[0],
            "ip": "192.168.6.0",
            "mask": 24,
            "version": 4,
            "gateway": "192.168.6.1",
            "dns": "192.168.6.2",
            "lease": 60
        }
        self.post(url=url, json=p1, auth=(self.api_user, self.api_password))
        p2 = {
            "nodeName": self.dhcpnode[0],
            "ip": "192.168.3.0",
            "mask": 24,
            "version": 4,
            "gateway": "192.168.3.1",
            "dns": "192.168.3.2",
            "lease": 60
        }
        self.post(url=url, json=p2, auth=(self.api_user, self.api_password))
        p3 = {
            "nodeName": self.dhcpnode[1],
            "ip": "172.0.0.0",
            "mask": 16,
            "version": 4,
            "gateway": "172.0.0.1",
            "dns": "172.0.0.2",
            "lease": 60
        }
        self.post(url=url, json=p3, auth=(self.api_user, self.api_password))
        p4 = {
            "nodeName": self.dhcpnode[1],
            "ip": "2002::",
            "mask": 64,
            "version": 6,
            "gateway": "2002::1",
            "dns": "2002::2",
            "lease": 60
        }
        self.post(url=url, json=p4, auth=(self.api_user, self.api_password))
        p5 = {
            "nodeName": self.dhcpnode[0],
            "ip": "2001::",
            "mask": 64,
            "version": 6,
            "gateway": "2001::1",
            "dns": "2001::2",
            "lease": 60
        }
        self.post(url=url, json=p5, auth=(self.api_user, self.api_password))



        print('Step1: 用GET方法调用接口https://192.168.6.82:19393/api/dhcp/subnet返回所有的dhcp的子网列表')

        r1 = self.get(url=url,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code1,res1 = r1
            if not (status_code1 == 200 and res1['code'] == "Success" and len(res1['data']) == 5):
                self.exception.add('Step1: ' + str(r1))
        else:
            self.exception.add('Step1: ' + str(self.api_error))

        print('Step2: 用GET方法调用接口，按照节点查询https://192.168.6.82:19393/api/dhcp/subnet?nodeName=dhcp1返回所有的dhcp的子网列表')
        payload2 = {
            "nodeName": self.dhcpnode[0]
        }

        r2 = self.get(url=url, params=payload2, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code2, res2 = r2
            if status_code2 == 200 and res2['code'] == "Success" and len(res2['data']) == 3:
                for dhcp in res2['data']:
                    nodoname2 = dhcp.get('nodeName')
                    if nodoname2 != self.dhcpnode[0]:
                        self.exception.add('Step2a: ' + str(r2))
            else:
                self.exception.add('Step2b: ' + str(r2))
        else:
            self.exception.add('Step2: ' + str(self.api_error))

        print('Step3: 用GET方法调用接口，按照节点查询https://192.168.6.82:19393/api/dhcp/subnet?nodeName=dhcp2返回所有的dhcp的子网列表')
        payload3 = {
            "nodeName": self.dhcpnode[1]
        }

        r3 = self.get(url=url, params=payload3, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code3, res3 = r3
            if status_code3 == 200 and res3['code'] == "Success" and len(res3['data']) == 2:
                for dhcp in res3['data']:
                    nodoname3 = dhcp.get('nodeName')
                    print(nodoname3)
                    if nodoname3 != self.dhcpnode[1]:
                        self.exception.add('Step3a: ' + str(r3))
            else:
                self.exception.add('Step3b: ' + str(r3))
        else:
            self.exception.add('Step3: ' + str(self.api_error))

        print('Step4: 用GET方法调用接口，按照节点查询且节点不存在https://192.168.6.82:19393/api/dhcp/subnet?nodeName=dhcp3返回所有的dhcp的子网列表')
        payload4 = {
            "nodeName": "dhcp3333"
        }
        r4 = self.get(url=url, params=payload4, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code4, res4 = r4
            if not (status_code4 == 200 and res4['code'] == "Success" and len(res4['data']) == 0):
                self.exception.add('Step4: ' + str(r4))
        else:
            self.exception.add('Step4: ' + str(self.api_error))

        print('Step5: 用GET方法调用接口，按照ip段查询https://192.168.6.82:19393/api/dhcp/subnet?ip=192.168.6.0返回所有的dhcp的子网列表')
        payload5 = {
            "ip": "192.168.6.0"
        }

        r5 = self.get(url=url, params=payload5, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code5, res5 = r5
            if status_code5 == 200 and res5['code'] == "Success" and len(res5['data']) == 1:
                for dhcp in res5['data']:
                    ip5 = dhcp.get('ip')
                    if ip5 != "192.168.6.0":
                        self.exception.add('Step5: ' + str(r5))
            else:
                self.exception.add('Step5: ' + str(r5))
        else:
            self.exception.add('Step5: ' + str(self.api_error))

        print('Step6: 用GET方法调用接口，按照ip段查询且ip段不存在https://192.168.6.82:19393/api/dhcp/subnet?ip=192.168.10.0返回所有的dhcp的子网列表')
        payload6 = {
            "ip": "192.168.10.0"
        }

        r6 = self.get(url=url, params=payload6, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code6, res6 = r6
            if not(status_code6 == 200 and res6['code'] == "Success" and len(res6['data']) == 0):
                self.exception.add('Step6: ' + str(r6))
        else:
            self.exception.add('Step6: ' + str(self.api_error))

        print('Step7: 用GET方法调用接口，按照dhcp节点和ip段组合查询https://192.168.6.82:19393/api/dhcp/subnet?nodeName=dhcp2&ip=192.168.6.0返回所有的dhcp的子网列表')
        payload7 = {
            "nodeName": self.dhcpnode[1],
            "ip": "172.0.0.0"
        }

        r7 = self.get(url=url, params=payload7, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code7, res7 = r7
            if not (status_code7 == 200 and res7['code'] == "Success" and len(res7['data']) == 1):
                self.exception.add('Step7: ' + str(r7))
        else:
            self.exception.add('Step7: ' + str(self.api_error))