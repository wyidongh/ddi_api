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
        sleep(4)

    def tearDown(self):

        self.authorization_delete_all_domain()
        self.delete_api_user()
        print("删除所有DNS节点")
        self.dns_node_delete_all_node()
        if self.exception:
            raise Exception(self.exception)


    def test_query_auth_record(self):
        url = "https://" + self.serverip[0] + ":19393/api/dns/records"
        print('添加授权域test.com')
        domain = "yamu.com"
        ns_name = "ns." + domain
        self.authorization_add_standard_domain(domainname=domain, nodename=self.nodename[0], viewname='default',
                                               ns_name=ns_name, ns_ip=self.serverip[0])
        print('添加反向域3.2.1.in-addr.arpa')
        domain_a = "3.2.1"
        arpa_type = "in-addr.arpa"
        reverse_domain = domain_a + "." + arpa_type
        self.authorization_add_reverse_domain(domainname=domain_a, arpa_type=arpa_type, nodename=self.nodename[0],
                                              ns_name=ns_name)

        sleep(2)
        print('添加www.yamu.com的A记录为1.1.1.1')
        host1 = "www"
        res1 = "1.1.1.1"
        self.authorization_add_a_record(nodename=self.nodename[0],domain=domain,host=host1,res=res1)

        print('添加www.yamu.com的AAAA记录为11::22')
        host2 = "www"
        res2 = "11::22"
        self.authorization_add_aaaa_record(nodename=self.nodename[0],domain=domain,host=host2,res=res2)

        host3 = "4"
        res3 = "4.yamu.com"
        self.authorization_add_ptr_record(nodename=self.nodename[0],domain=reverse_domain,host=host3,res=res3)


        print('Step1: 用GET方法调用https://192.168.6.62:19393/api/dns/records接口，不加任何的querystring')
        r = self.get(url=url,auth=HTTPBasicAuth(self.api_user,self.api_password))
        if self.api_error is  None:
            status_code = r[0]
            res = r[1]
            if not (status_code == 200 and res["code"] == "Success" and len(res['data']) == 6):
                self.exception.add("Step1:" + str(res))
        else:
            self.exception.add("Step1: " + self.api_error)
