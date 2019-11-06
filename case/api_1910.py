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

    def test_ipam_edit_ip_addr_status(self):

        ipsegment = "192.168.16.0/24"
        ip = ipsegment.split("/")[0]
        mask = ipsegment.split("/")[1]
        print('在页面【IPAM】-【ip地址段】，点击新增一个IP地址段192.168.16.0/24')
        self.ipSegment_management_add_ip_segment(ip=ip, type="IPV4", mask=mask)

        print('在页面【IPAM】-【ip段配置】-【ip段配置】，在17.0段后面点击配置按钮，为期配置网段、dns、租约等信息')
        self.ipSegment_configure_configrure_ip_segment(ipsegment=ipsegment, gateway="192.168.16.1", dns="192.168.16.2")

        sleep(3)

        url = "https://" + self.serverip[0] + ":19393/api/ipam/ipstatus/name"

        print('Step2:')
        payload2 = {
                    "ipSegment": "192.168.16.0/24",
                    "ip":"192.168.16.100",
                    "update": {
                    "switchName": "swname",
                    "switchIp":"192.168.1.1",
                    "switchPort":"seo-ers-d/:df:ds",
                    "comment":"test"
                    }
                    }

        r2 = self.put(url=url, json=payload2, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code2, res2 = r2
            if not (status_code2 == 200 and res2['code'] == "Success"):
                self.exception.add("Step2: " + str(r2))
        else:
            self.exception.add('Step2: ' + str(self.api_error))
