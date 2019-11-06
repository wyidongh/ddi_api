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
        self.dhs_node_add_dns_node(nodename=self.nodename[1])
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


    def test_modify_auth_domain(self):
        url = "https://" + self.serverip[0] + ":19393/api/dns/zones"
        print('添加授权域test.com')
        domain = "test.com"
        ns_name = "ns." + domain
        self.authorization_add_standard_domain(domainname=domain, nodename=self.nodename[0], viewname='default',
                                               ns_name=ns_name, ns_ip=self.serverip[0])
        print('添加反向域3.2.1.in-addr.arpa')
        reverse_domain = "3.2.1"
        self.authorization_add_reverse_domain(domainname=reverse_domain, arpa_type="in-addr.arpa", nodename=self.nodename[0],
                                              ns_name=ns_name)

        sleep(3)
        print('Step1: 用GET方法调用https://192.168.6.62:19393/api/dns/zones接口，查询出所有授权域的ID，其中包括3.2.1.in-addr.arpa的id')
        r1 = self.get(url=url,auth=HTTPBasicAuth(self.api_user,self.api_password))
        id = ""
        if r1 is not None:
            status_code1 = r1[0]
            res1 = r1[1]
            for zone in res1["data"]:
                domainname = zone.get("domain")
                if domainname == reverse_domain + ".in-addr.arpa":
                    id = zone.get("id")
                    break
                else:
                    continue

            if not (status_code1 == 200 and res1["code"] == "Success" and bool(id) ):
                self.exception.add("Step1:" + str(res1))
        else:
            self.exception.add("Step1: " + self.api_error)

        # print("id;%s" % id)

        print('Step2: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5b9a258d9b63a0005b2d2d60接口，将3.2.1.in-addr.arpa的备注修改为“反向域”')
        url2 = url + "/" + str(id)
        payload = {"comment":"反向域test"}
        r2 = self.put(url=url2,json=payload,auth=HTTPBasicAuth(self.api_user,self.api_password))
        if self.api_error is  None:
            status_code2 = r2[0]
            res2 = r2[1]
            if not (status_code2 == 200 and res2["code"] == "Success"):
                self.exception.add("Step2:" + str(res2))
        else:
            self.exception.add("Step2: " + self.api_error)

        self.authorization_enter_domain_page()
        sleep(3)
        print('Step3: 点击【域管理】进入页面，查看授权域3.2.1.in-addr.arpa的备注信息')
        flag = self.isElementExist_by_xpath('//*[@id="datarows"]/tr/td[text()="反向域test"]')
        if not flag:
            self.exception.add("Step3: 未发现指定备注信息")





