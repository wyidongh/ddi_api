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

    def test_get_dhcp_subnet_with_ip_segment(self):

        url = "https://" + self.serverip[0] + ":19393/api/dhcp/subnet"

        print('在dhcp1节点中添加ip段192.168.1.0/24,10.0.0.0/8;在dhcp2节点中添加ip段192.168.3.0/24,1.2.0.0/16;')
        ip1 = "192.168.1.0"
        mask1 = 24
        # self.ipSegment_management_add_ip_segment(ip=ip1,type="IPV4",mask=mask1)
        ip_segment1 = ip1 + "/" + str(mask1)
        #self.ipSegment_configure_configrure_ip_segment(ipsegment=ip_segment1,gateway="192.168.1.1",dns="192.168.1.2")
        #self.business_configure_bind_segment(node=self.dhcpnode[0],segment=ip_segment1)
        p1 = {
            "nodeName": self.dhcpnode[0],
            "ip": ip1,
            "mask": mask1,
            "version": 4,
            "gateway": "192.168.1.1",
            "dns": "192.168.1.2",
            "lease": 60
        }
        self.post(url=url,json=p1,auth=(self.api_user,self.api_password))

        ip2 = "10.0.0.0"
        mask2 = "8"
        ip_segment2 = ip2 + "/" + mask2

        p2 = {
            "nodeName": self.dhcpnode[0],
            "ip": ip2,
            "mask": mask2,
            "version": 4,
            "gateway": "10.0.0.1",
            "dns": "10.10.0.2",
            "lease": 60
        }
        self.post(url=url, json=p2, auth=(self.api_user, self.api_password))


        ip3 = "192.168.3.0"
        mask3 = "24"
        ip_segment3 = ip3 + "/" + mask3
        p3 = {
            "nodeName": self.dhcpnode[1],
            "ip": ip3,
            "mask": mask3,
            "version": 4,
            "gateway": "192.168.3.1",
            "dns": "192.168.3.2",
            "lease": 60
        }
        self.post(url=url, json=p3, auth=(self.api_user, self.api_password))


        ip4 = "1.2.0.0"
        mask4 = "16"
        # self.ipSegment_management_add_ip_segment(ip=ip4, type="IPV4", mask=mask4)
        ip_segment4 = ip4 + "/" + mask4
        # self.ipSegment_configure_configrure_ip_segment(ipsegment=ip_segment4, gateway="1.2.0.1", dns="1.2.0.2")
        # self.business_configure_bind_segment(node=self.dhcpnode[1], segment=ip_segment4)

        p4 = {
            "nodeName": self.dhcpnode[1],
            "ip": ip4,
            "mask": mask4,
            "version": 4,
            "gateway": "1.2.0.1",
            "dns": "1.2.0.2",
            "lease": 60
        }
        self.post(url=url, json=p4, auth=(self.api_user, self.api_password))

        sleep(2)
        url1 = "https://" + self.serverip[0] + ":19393/api/dhcp/subnet/name"

        print('Step1: 用GET方法调用接口https://192.168.16.109:19393/api/dhcp/subnet/name?nodeName=dhcp1&ip=192.168.1.0&mask=24查询存在的指定ip段的subnet')
        payload1 = {
            "nodeName": self.dhcpnode[0],
            "ip": ip1,
            "mask": mask1
        }
        r1 = self.get(url=url1,params=payload1,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code1,res1 = r1
            if not (status_code1 == 200 and res1['code'] == "Success" and res1['data'] is not None):
                self.exception.add("Step1: " + str(r1))
        else:
            self.exception.add('Step1: ' + str(self.api_error))

        print('Step2: 用GET方法调用接口https://192.168.16.109:19393/api/dhcp/subnet/name?nodeName=dhcp1&ip=10.0.0.0&mask=8查询存在的指定ip段的subnet')
        payload2 = {
            "nodeName": self.dhcpnode[0],
            "ip": ip2,
            "mask": mask2
        }
        r2 = self.get(url=url1, params=payload2, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code2, res2 = r2
            if not (status_code2 == 200 and res2['code'] == "Success" and res2['data'] is not None):
                self.exception.add("Step2: " + str(r2))
        else:
            self.exception.add('Step2: ' + str(self.api_error))

        print('Step3: 用GET方法调用接口https://192.168.16.109:19393/api/dhcp/subnet/name?nodeName=dhcp2&ip=192.168.3.0&mask=24查询存在的指定ip段的subnet')
        payload3 = {
            "nodeName": self.dhcpnode[1],
            "ip": ip3,
            "mask": mask3
        }
        r3 = self.get(url=url1, params=payload3, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code3, res3 = r3
            if not (status_code3 == 200 and res3['code'] == "Success" and res3['data'] is not None):
                self.exception.add("Step3: " + str(r3))
        else:
            self.exception.add('Step3: ' + str(self.api_error))

        print('Step4: 用GET方法调用接口https://192.168.16.109:19393/api/dhcp/subnet/name?nodeName=dhcp2&ip=1.2.0.0&mask=16查询存在的指定ip段的subnet')
        payload4 = {
            "nodeName": self.dhcpnode[1],
            "ip": ip4,
            "mask": mask4
        }
        r4 = self.get(url=url1, params=payload4, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code4, res4 = r4
            if not (status_code4 == 200 and res4['code'] == "Success" and res4['data'] is not None):
                self.exception.add("Step4: " + str(r4))
        else:
            self.exception.add('Step4: ' + str(self.api_error))



        print('Step5: 用GET方法调用接口https://192.168.6.82:19393/api/dhcp/subnet/name?ip=192.168.1.0&mask=24查询存在的指定ip段的subnet')
        payload5 = {
            "ip": ip1,
            "mask": mask1
        }
        r5 = self.get(url=url1, params=payload5, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code5, res5 = r5
            if not (status_code5 == 400 and res5['code'] == "NodeNotExisted"):
                self.exception.add("Step5: " + str(r5))
        else:
            self.exception.add('Step5: ' + str(self.api_error))

        print('Step6: 用GET方法调用接口https://192.168.16.109:19393/api/dhcp/subnet/name?nodeName=dhcp3&ip=192.168.1.0&mask=24查询存在的指定ip段的subnet')
        payload6 = {
            "nodeName": "dhcp3",
            "ip": ip1,
            "mask": mask1
        }
        r6 = self.get(url=url1, params=payload6, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code6, res6 = r6
            if not (status_code6 == 400 and res6['code'] == "NodeNotExisted"):
                self.exception.add("Step6: " + str(r6))
        else:
            self.exception.add('Step6: ' + str(self.api_error))

        print('Step7: 用GET方法调用接口https://192.168.16.109:19393/api/dhcp/subnet/name?nodeName=dhcp1&ip=192.168.8.0&mask=24查询存在的指定ip段的subnet')
        payload7 = {
            "nodeName": self.dhcpnode[0],
            "ip": "192.168.8.0",
            "mask": "24"
        }
        r7 = self.get(url=url1, params=payload7, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code7, res7 = r7
            if not (status_code7 == 400 and res7['code'] == "SubnetNotExist"):
                self.exception.add("Step7: " + str(r7))
        else:
            self.exception.add('Step7: ' + str(self.api_error))

        print('Step8: GET方法调用接口https://192.168.16.109:19393/api/dhcp/subnet/name?nodeName=dhcp1&ip=192.168.266.0&mask=24查询存在的指定ip段的subnet')
        payload8 = {
            "nodeName": self.dhcpnode[0],
            "ip": "192.168.256.0",
            "mask": "24"
        }
        r8 = self.get(url=url1, params=payload8, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code8, res8 = r8
            if not (status_code8 == 400 and res8['code'] == "InvalidIP"):
                self.exception.add("Step8: " + str(r8))
        else:
            self.exception.add('Step8: ' + str(self.api_error))

        print('Step9: 用GET方法调用接口https://192.168.16.109:19393/api/dhcp/subnet/name?nodeName=dhcp1&ip=192.168.1.0&mask=55查询存在的指定ip段的subnet')
        payload9 = {
            "nodeName": self.dhcpnode[0],
            "ip": "192.168.1.0",
            "mask": "33"
        }
        r9 = self.get(url=url1, params=payload9, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code9, res9 = r9
            if not (status_code9 == 400 and res9['code'] == "InvalidMask"):
                self.exception.add("Step9: " + str(r9))
        else:
            self.exception.add('Step9: ' + str(self.api_error))

        print('Step10: 用GET方法调用接口https://192.168.16.109:19393/api/dhcp/subnet/name?nodeName=dhcp1&ip=192.168.1.0&mask=32查询存在的指定ip段的subnet')
        payload10 = {
            "nodeName": self.dhcpnode[0],
            "ip": "192.168.1.0",
            "mask": "32"
        }
        r10 = self.get(url=url1, params=payload10, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code10, res10 = r10
            if not (status_code10 == 400 and res10['code'] == "SubnetNotExist"):
                self.exception.add("Step10: " + str(r10))
        else:
            self.exception.add('Step10: ' + str(self.api_error))

        print('Step11: 用GET方法调用接口https://192.168.16.109:19393/api/dhcp/subnet/name?nodeName=dhcp1&ip=192.168.1.0&mask=20查询存在的指定ip段的subnet')
        payload11 = {
            "nodeName": self.dhcpnode[0],
            "ip": "192.168.1.0",
            "mask": "20"
        }
        r11 = self.get(url=url1, params=payload11, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code11, res11 = r11
            if not (status_code11 == 400 and res11['code'] == "SubnetNotExist"):
                self.exception.add("Step11: " + str(r11))
        else:
            self.exception.add('Step11: ' + str(self.api_error))

        print('Step12: 用GET方法调用接口https://192.168.16.109:19393/api/dhcp/subnet/name?nodeName=dhcp1&ip=192.168.1.0&mask=24&gateway=192.168.1.2查询存在的指定ip段的subnet')
        payload12 = {
            "nodeName": self.dhcpnode[0],
            "ip": "192.168.1.0",
            "mask": "24",
            "gateway": "192.168.1.1"
        }
        r12 = self.get(url=url1, params=payload12, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code12, res12 = r12
            if not (status_code12 == 200 and res12['code'] == "Success" and res12['data'] is not None):
                self.exception.add("Step12: " + str(r11))
        else:
            self.exception.add('Step12: ' + str(self.api_error))


        print('Step13: 用GET方法调用接口https://192.168.16.109:19393/api/dhcp/subnet/name?nodeName=dhcp1&ip=192.168.1.0&mask=24&test=test1查询存在的指定ip段的subnet')
        payload13 = {
            "nodeName": self.dhcpnode[0],
            "ip": "192.168.1.0",
            "mask": "24",
            "test": "test1"
        }
        r13 = self.get(url=url1, params=payload13, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code13, res13 = r13
            if not (status_code13 == 200 and res13['code'] == "Success" and res13['data'] is not None):
                self.exception.add("Step13: " + str(r13))
        else:
            self.exception.add('Step13: ' + str(self.api_error))






