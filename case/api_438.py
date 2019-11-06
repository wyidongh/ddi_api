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
        self.dhs_node_add_dns_node(nodename=self.nodename[0],device=self.devices)
        self.dhs_node_add_dns_node(nodename=self.nodename[1])
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


    def test_query_all_domain(self):



        url = "https://" + self.serverip[0] + ":19393/api/dns/zones"

        print('在node1下添加域test.com')
        domain = "test.com"
        ns_name = "ns." + domain
        self.authorization_add_standard_domain(domainname=domain,nodename=self.nodename[0],viewname='default',ns_name=ns_name,ns_ip=self.serverip[0])

        print('在node1下添加反向域3.2.1.in-addr.arpa')
        domain = "3.2.1"
        self.authorization_add_reverse_domain(domainname=domain,arpa_type="in-addr.arpa",nodename=self.nodename[0],ns_name=ns_name)

        print('在node2下添加域abc.com')
        domain = "abc.com"
        ns_name = "ns." + domain
        self.authorization_add_standard_domain(domainname=domain,nodename=self.nodename[1],viewname='default',ns_name=ns_name,ns_ip=self.serverip[0])

        sleep(3)

        r1 = self.get(url,auth=HTTPBasicAuth(self.api_user,self.api_password))
        if self.api_error is  None:
            status_code1 = r1[0]
            res1 = r1[1]
            if not (status_code1 == 200 and res1["code"] == "Success" and len(res1["data"]) == 2):
                self.exception.add("Step1:" + str(res1))
        else:
            self.exception.add("Step1: " + self.api_error)


