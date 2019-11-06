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
        sleep(1)
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

    def test_add_dhcp_subnet_ipv4_validation_check(self):

        url = "https://" + self.serverip[0] + ":19393/api/dhcp/subnet"

        print('Step1: 用POST方法调用接口https://192.168.6.82:19393/api/dhcp/subnet，添加nodeName为“dhcp1”，ip为包含负数的策略')
        ip1 = "-192.168.1.0"
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
        if self.api_error is None:
            status_code1,res1 = r1
            if not (status_code1 == 400 and res1['code'] == "InvalidParam"):
                self.exception.add('Step1: ' + str(r1))
        else:
            self.exception.add('Step1: ' + str(self.api_error))

        print('Step2: 用POST方法调用接口https://192.168.6.82:19393/api/dhcp/subnet，添加nodeName为“dhcp”，ip为全零的策略')
        ip2 = "0.0.0.0"
        mask2 = 24
        gateway2 = "192.168.2.1"
        dns2 = "192.168.2.2"
        payload2 = {
            "nodeName": self.dhcpnode[0],
            "ip": ip2,
            "mask": mask2,
            "version": 4,
            "gateway": gateway2,
            "dns": dns2,
            "lease": 60
        }

        r2 = self.post(url=url, json=payload2, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code2, res2 = r2
            if not (status_code2 == 400 and res2['code'] == "InvalidParam"):
                self.exception.add('Step2: ' + str(r2))
        else:
            self.exception.add('Step2: ' + str(self.api_error))

        print('Step3: 用POST方法调用接口https://192.168.6.82:19393/api/dhcp/subnet，添加nodeName为“dhcp1”，ip为全255的策略')
        ip3 = "255.255.255.255"
        mask3 = 24
        gateway3 = "192.168.3.1"
        dns3 = "192.168.3.2"
        payload3 = {
            "nodeName": self.dhcpnode[0],
            "ip": ip3,
            "mask": mask3,
            "version": 4,
            "gateway": gateway3,
            "dns": dns3,
            "lease": 60
        }

        r3 = self.post(url=url, json=payload3, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code3, res3 = r3
            if not (status_code3 == 200 and res3['code'] == "Success"):
                self.exception.add('Step3: ' + str(r3))
        else:
            self.exception.add('Step3: ' + str(self.api_error))

        print('Step4: 用POST方法调用接口https://192.168.6.82:19393/api/dhcp/subnet，添加nodeName为“dhcp1”，ip为超过了255的策略')
        ip4 = "192.256.4.0"
        mask4 = 24
        gateway4 = "192.168.4.1"
        dns4 = "192.168.4.2"
        payload4 = {
            "nodeName": self.dhcpnode[0],
            "ip": ip4,
            "mask": mask4,
            "version": 4,
            "gateway": gateway4,
            "dns": dns4,
            "lease": 60
        }

        r4 = self.post(url=url, json=payload4, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code4, res4 = r4
            if not (status_code4 == 400 and res4['code'] == "InvalidParam"):
                self.exception.add('Step4: ' + str(r4))
        else:
            self.exception.add('Step4: ' + str(self.api_error))

        print('Step5: 用POST方法调用接口https://192.168.6.82:19393/api/dhcp/subnet，添加nodeName为“dhcp1”，ip为空的策略')
        ip5 = ""
        mask5 = 24
        gateway5 = "1.1.1.1"
        dns5 = "2.2.2.2"
        payload5 = {
            "nodeName": self.dhcpnode[0],
            "ip": ip5,
            "mask": mask5,
            "version": 4,
            "gateway": gateway5,
            "dns": dns5,
            "lease": 60
        }

        r5 = self.post(url=url, json=payload5, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code5, res5 = r5
            if not (status_code5 == 400 and res5['code'] == "InvalidParam"):
                self.exception.add('Step5: ' + str(r5))
        else:
            self.exception.add('Step5: ' + str(self.api_error))

        print('Step6: 用POST方法调用接口https://192.168.6.82:19393/api/dhcp/subnet，添加nodeName为“dhcp1”，ip为超过4个段的IPv4的策略')
        ip6 = "192.168.6.0.4"
        mask6 = 24
        gateway6 = "1.1.1.1"
        dns6 = "2.2.2.2"
        payload6 = {
            "nodeName": self.dhcpnode[0],
            "ip": ip6,
            "mask": mask6,
            "version": 4,
            "gateway": gateway6,
            "dns": dns6,
            "lease": 60
        }

        r6 = self.post(url=url, json=payload6, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code6, res6 = r6
            if not (status_code6 == 400 and res6['code'] == "InvalidParam"):
                self.exception.add('Step6: ' + str(r6))
        else:
            self.exception.add('Step6: ' + str(self.api_error))

        print('Step7: 用POST方法调用接口https://192.168.6.82:19393/api/dhcp/subnet，添加nodeName为“dhcp1”，ip为少于4个段的IPv4的策略')
        ip7 = "192.168.7"
        mask7 = 24
        gateway7 = "1.1.1.1"
        dns7 = "2.2.2.2"
        payload7 = {
            "nodeName": self.dhcpnode[0],
            "ip": ip7,
            "mask": mask7,
            "version": 4,
            "gateway": gateway7,
            "dns": dns7,
            "lease": 60
        }

        r7 = self.post(url=url, json=payload7, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code7, res7 = r7
            if not (status_code7 == 400 and res7['code'] == "InvalidParam"):
                self.exception.add('Step7: ' + str(r7))
        else:
            self.exception.add('Step7: ' + str(self.api_error))

        print('Step8: 用POST方法调用接口https://192.168.6.82:19393/api/dhcp/subnet，添加nodeName为“dhcp1”且ip为正确的IPv4地址的策略')
        ip8 = "192.168.8.0"
        mask8 = 24
        gateway8 = "192.168.8.1"
        dns8 = "192.168.8.2"
        payload8 = {
            "nodeName": self.dhcpnode[0],
            "ip": ip8,
            "mask": mask8,
            "version": 4,
            "gateway": gateway8,
            "dns": dns8,
            "lease": 60
        }

        r8 = self.post(url=url, json=payload8, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code8, res8 = r8
            if not (status_code8 == 200 and res8['code'] == "Success"):
                self.exception.add('Step8: ' + str(r8))
        else:
            self.exception.add('Step8: ' + str(self.api_error))

        print('Step9: 用POST方法调用接口https://192.168.6.82:19393/api/dhcp/subnet，添加nodeName为“dhcp1”且ip为正确的IPv4地址，mask为小数的策略')
        ip9 = "192.168.9.0"
        mask9 = 24.3
        gateway9 = "192.168.9.1"
        dns9 = "192.168.9.2"
        payload9 = {
            "nodeName": self.dhcpnode[0],
            "ip": ip9,
            "mask": mask9,
            "version": 4,
            "gateway": gateway9,
            "dns": dns9,
            "lease": 60
        }

        r9 = self.post(url=url, json=payload9, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code9, res9 = r9
            if not (status_code9 == 200 and res9['code'] == "Success"):
                self.exception.add('Step9: ' + str(r9))
        else:
            self.exception.add('Step9: ' + str(self.api_error))

        print('Step10: 用POST方法调用接口https://192.168.6.82:19393/api/dhcp/subnet，添加nodeName为“dhcp1”且ip为正确的IPv4地址，mask为0的策略')
        ip10 = "192.168.10.0"
        mask10 = 0
        gateway10 = "192.168.10.1"
        dns10 = "192.168.10.2"
        payload10 = {
            "nodeName": self.dhcpnode[0],
            "ip": ip10,
            "mask": mask10,
            "version": 4,
            "gateway": gateway10,
            "dns": dns10,
            "lease": 60
        }

        r10 = self.post(url=url, json=payload10, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code10, res10 = r10
            if not (status_code10 == 400 and res10['code'] == "InvalidParam"):
                self.exception.add('Step10: ' + str(r10))
        else:
            self.exception.add('Step10: ' + str(self.api_error))

        print('Step11: 用POST方法调用接口https://192.168.6.82:19393/api/dhcp/subnet，添加nodeName为“dhcp1”且ip为正确的IPv4地址，mask为负数的策略')
        ip11 = "192.168.11.0"
        mask11 = -24
        gateway11 = "192.168.11.1"
        dns11 = "192.168.11.2"
        payload11 = {
            "nodeName": self.dhcpnode[0],
            "ip": ip11,
            "mask": mask11,
            "version": 4,
            "gateway": gateway11,
            "dns": dns11,
            "lease": 60
        }

        r11 = self.post(url=url, json=payload11, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code11, res11 = r11
            if not (status_code11 == 400 and res11['code'] == "InvalidParam"):
                self.exception.add('Step11: ' + str(r11))
        else:
            self.exception.add('Step11: ' + str(self.api_error))

        print('Step12: 用POST方法调用接口https://192.168.6.82:19393/api/dhcp/subnet，添加nodeName为“dhcp1”且ip为正确的IPv4地址，mask为33的策略')
        ip12 = "192.168.12.0"
        mask12 = 33
        gateway12 = "192.168.12.1"
        dns12 = "192.168.12.2"
        payload12 = {
            "nodeName": self.dhcpnode[0],
            "ip": ip12,
            "mask": mask12,
            "version": 4,
            "gateway": gateway12,
            "dns": dns12,
            "lease": 60
        }

        r12 = self.post(url=url, json=payload12, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code12, res12 = r12
            if not (status_code12 == 400 and res12['code'] == "InvalidParam"):
                self.exception.add('Step12: ' + str(r12))
        else:
            self.exception.add('Step12: ' + str(self.api_error))

        print('Step13: 用POST方法调用接口https://192.168.6.82:19393/api/dhcp/subnet，添加nodeName为“dhcp1”且ip为正确的IPv4地址，mask为32的策略')
        ip13 = "192.168.13.0"
        mask13 = 32
        gateway13 = "192.168.13.1"
        dns13 = "192.168.13.2"
        payload13 = {
            "nodeName": self.dhcpnode[0],
            "ip": ip13,
            "mask": mask13,
            "version": 4,
            "gateway": gateway13,
            "dns": dns13,
            "lease": 60
        }

        r13 = self.post(url=url, json=payload13, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code13, res13 = r13
            if not (status_code13 == 200 and res13['code'] == "Success"):
                self.exception.add('Step13: ' + str(r13))
        else:
            self.exception.add('Step13: ' + str(self.api_error))

        print('Step14: 用POST方法调用接口https://192.168.6.82:19393/api/dhcp/subnet，添加nodeName为“dhcp1”且ip为正确的IPv4地址，mask为24的策略')
        ip14 = "192.168.14.0"
        mask14 = 24
        gateway14 = "192.168.14.1"
        dns14 = "192.168.14.2"
        payload14 = {
            "nodeName": self.dhcpnode[0],
            "ip": ip14,
            "mask": mask14,
            "version": 4,
            "gateway": gateway14,
            "dns": dns14,
            "lease": 60
        }

        r14 = self.post(url=url, json=payload14, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code14, res14 = r14
            if not (status_code14 == 200 and res14['code'] == "Success"):
                self.exception.add('Step14: ' + str(r14))
        else:
            self.exception.add('Step14: ' + str(self.api_error))

        print('Step15: 用POST方法调用接口https://192.168.6.82:19393/api/dhcp/subnet，添加nodeName为“dhcp1”且ip为正确的IPv4地址，mask为1的策略')
        ip15 = "192.168.15.0"
        mask15 = 1
        gateway15 = "192.168.15.1"
        dns15 = "192.168.15.2"
        payload15 = {
            "nodeName": self.dhcpnode[0],
            "ip": ip15,
            "mask": mask15,
            "version": 4,
            "gateway": gateway15,
            "dns": dns15,
            "lease": 60
        }

        r15 = self.post(url=url, json=payload15, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code15, res15 = r15
            if not (status_code15 == 200 and res15['code'] == "Success"):
                self.exception.add('Step15: ' + str(r15))
        else:
            self.exception.add('Step15: ' + str(self.api_error))

        print('Step16: 用POST方法调用接口https://192.168.6.82:19393/api/dhcp/subnet，添加nodeName为“dhcp1”且ip为正确的IPv4地址，mask为空的策略')
        ip16 = "192.168.16.0"
        mask16 = ""
        gateway16 = "192.168.16.1"
        dns16 = "192.168.16.2"
        payload16 = {
            "nodeName": self.dhcpnode[0],
            "ip": ip16,
            "mask": mask16,
            "version": 4,
            "gateway": gateway16,
            "dns": dns16,
            "lease": 60
        }

        r16 = self.post(url=url, json=payload16, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code16, res16 = r16
            if not (status_code16 == 400 and res16['code'] == "InvalidParam"):
                self.exception.add('Step16: ' + str(r16))
        else:
            self.exception.add('Step16: ' + str(self.api_error))
