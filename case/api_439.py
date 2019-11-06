from unittest import TestCase
from time import sleep
from selenium import webdriver
from basic.system import system
from basic.dnspage import dnspage
from basic.assist import Tools
from basic.ddi_api import ddi_api
from basic.resource import resource

class RunTest(TestCase, Tools, ddi_api, system, dnspage,resource):
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
        self.dhs_node_add_dns_node(nodename=self.nodename[0],device=self.devices[0:1])
        print('为节点%s添加api用户%s' % (self.nodename[0], self.api_user))
        self.add_api_user(self.nodename[0], self.api_user, self.api_password)
        sleep(3)

    def tearDown(self):

        self.authorization_delete_all_domain()
        self.delete_api_user()
        self.dns_node_delete_all_node()
        if self.exception:
            raise Exception(self.exception)


    def test_add_auth_domain(self):


        print('Step1: 用POST方法调用https://192.168.6.62:19393/api/dns/zones接口，添加一个名为yamu.com的授权域，post的body内容为{"domain":"yamu.com"}')
        url = "https://" + self.serverip[0] + ":19393/api/dns/zones"
        payload = {"domain":"yamu.com"}
        r1 = self.post(url,json=payload,auth=(self.api_user,self.api_password))
        if self.api_error is  None:
            status_code1 = r1[0]
            res1 = r1[1]
            if not (status_code1 == 200 and res1["code"] == "Success"):
                self.exception.add("Step1:" + str(res1))
        else:
            self.exception.add("Step1: " + self.api_error)

        sleep(2)

        print('Step2: 点击【域管理】进入页面，查看授权域列表')
        flag = self.authorization_find_specific_domain(domainname='yamu.com',nodename=self.nodename[0],viewname='default')
        if not flag:
            self.exception.add('Step2,域管理界面未发现指定授权域')

