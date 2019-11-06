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
        self.dhs_node_add_dns_node(nodename=self.nodename[0],device=self.devices[0:1])
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


    def test_delete_auth_domain(self):
        url = "https://" + self.serverip[0] + ":19393/api/dns/zones"
        print('添加授权域test.com')
        domain = "test.com"
        ns_name = "ns." + domain
        self.authorization_add_standard_domain(domainname=domain, nodename=self.nodename[0], viewname='default',
                                               ns_name=ns_name, ns_ip=self.serverip[0])

        sleep(3)
        print('Step1: 用GET方法调用https://192.168.6.62:19393/api/dns/zones接口，查询出所有授权域的ID，其中包括test.com的id')
        r1 = self.get(url=url,auth=HTTPBasicAuth(self.api_user,self.api_password))
        id = ""
        if self.api_error is  None:
            status_code1 = r1[0]
            res1 = r1[1]
            for zone in res1["data"]:
                domainname = zone.get("domain")
                if domainname == domain:
                    id = zone.get("id")
                    break
                else:
                    continue

            if not (status_code1 == 200 and res1["code"] == "Success" and bool(id) ):
                self.exception.add("Step1:" + str(res1))
        else:
            self.exception.add("Step1: " + self.api_error)

        print('Step2: 用DELETE方法调用https://192.168.6.62:19393/api/dns/zones/5b9a0ceb9b63a0005b2d2a89接口，删除test.com')
        url2 = url + "/" + str(id)
        r2 = self.delete(url=url2,auth=HTTPBasicAuth(self.api_user,self.api_password))
        if self.api_error is  None:
            status_code2 = r2[0]
            res2 = r2[1]
            if not (status_code2 == 200 and res2["code"] == "Success"):
                self.exception.add("Step2:" + str(res2))
        else:
            self.exception.add("Step2: " + self.api_error)

        sleep(2)
        print('Step3: 点击【域管理】进入页面，查看授权域列表')
        flag = self.authorization_find_specific_domain(domainname=domain,nodename=self.nodename[0],viewname="default")
        if flag:
            self.exception.add("Step3: 页面添加的域未删除")



