from unittest import TestCase
from time import sleep
from selenium import webdriver
from basic.system import system
from basic.dnspage import dnspage
from basic.assist import Tools
from basic.ddi_api import ddi_api
from basic.resource import resource
from requests.auth import HTTPBasicAuth


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
        sleep(3)

    def tearDown(self):

        self.authorization_delete_all_domain()
        self.delete_api_user()
        print("删除所有DNS节点")
        self.dns_node_delete_all_node()
        if self.exception:
            raise Exception(self.exception)


    def test_add_auth_record(self):
        url = "https://" + self.serverip[0] + ":19393/api/dns/records"
        print('添加授权域yamu.com')
        domain = "yamu.com"
        ns_name = "ns." + domain
        self.authorization_add_standard_domain(domainname=domain, nodename=self.nodename[0], viewname='default',
                                               ns_name=ns_name, ns_ip=self.serverip[0])

        sleep(2)
        print('Step1: 用POST方法调用https://192.168.6.62:19393/api/dns/records接口，添加一个a.yamu.com的A记录为211.1.1.1')
        payload = {
                    "domain": "yamu.com",
                    "host":"a",
                    "type":"A",
                    "result": { "data": "211.1.1.1"}
                    }
        r = self.post(url=url,json=payload,auth=HTTPBasicAuth(self.api_user,self.api_password))
        if self.api_error is  None:
            status_code = r[0]
            res = r[1]
            if not (status_code == 200 and res["code"] == "Success"):
                self.exception.add("Step2:" + str(res))
        else:
            self.exception.add("Step2: " + self.api_error)

        print('Step2: 点击【记录管理】进入页面，查看a.yamu.com的解析结果')
        self.authorization_enter_record_page()
        sleep(1)
        flag = self.authorization_find_specific_record(nodename=self.nodename[0],record="a.yamu.com",viewname="default",type="A",res="211.1.1.1")
        if not flag:
            self.exception.add('Step2: 指定记录不存在')


