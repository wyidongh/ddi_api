from unittest import TestCase
from time import sleep
from selenium import webdriver
from basic.system import system
from basic.dnspage import dnspage
from basic.assist import Tools
from basic.ddi_api import ddi_api
from basic.resource import resource


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
        url1 = "https://" + self.serverip[0] + ":19393/api/dns/zones"

        print('域管理】中在node1下添加域abc-1.com和反向 域3.2.1.in-addr.arpa 在node2下添加域abc.com')
        domain1 = "abc-1.com"
        ns_name1 = "ns." + domain1
        self.authorization_add_standard_domain(domainname=domain1, nodename=self.nodename[0], viewname='default',
                                               ns_name=ns_name1, ns_ip=self.serverip[0],note="abc-1.com备注")
        print('添加反向域3.2.1.in-addr.arpa')
        reverse_domain = "3.2.1"
        self.authorization_add_reverse_domain(domainname=reverse_domain, arpa_type="in-addr.arpa",
                                              nodename=self.nodename[0],
                                              ns_name=ns_name1)
        domain2 = "abc.com"
        ns_name2 = "ns." + domain2
        self.authorization_add_standard_domain(domainname=domain2, nodename=self.nodename[1], viewname='default',
                                               ns_name=ns_name2, ns_ip=self.serverip[0])


        print('Step1: 用GET方法调用https://192.168.6.62:19393/api/dns/zones接口，查询出所有授权域的ID，其中包括abc-1.com')

        r1 = self.get(url=url1, auth=(self.api_user, self.api_password))
        id = ""
        if self.api_error is None:
            status_code1,res1 = r1
            for zone in res1["data"]:
                domainname = zone.get("domain")
                if domainname == domain1:
                    id = zone.get("id")
                    break
                else:
                    continue
            if not (status_code1 == 200 and res1["code"] == "Success" and bool(id)):
                self.exception.add("Step1:" + str(res1))
        else:
            self.exception.add("Step1: " + self.api_error)

        print('Step2: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5baddaed8889ee6bc88a43f6接口，将abc-1.com的备注修改为“”')

        url2 = url1 + "/" + str(id)
        payload2 = {
            "comment":""
        }
        r2 = self.put(url=url2,json=payload2, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code2,res2 = r2
            if not (status_code2 == 200 and res2['code'] == "Success"):
                self.exception.add("Step2:" + str(res2))
        else:
            self.exception.add("Step2:" + self.api_error)

        print('Step3: 点击【域管理】进入页面，查看授权域3.2.1.in-addr.arpa的备注信息')
        self.authorization_enter_domain_page()
        flag = self.authorization_find_specific_domain(domainname=domain1,nodename=self.nodename[0],viewname="default",note="")
        if not flag:
            self.exception.add("Step3: 页面上未查到指定备注为空的域")

        print('Step4: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5baddaed8889ee6bc88a43f6接口，将abc-1.com的备注修改为“超过100个字数”')
        payload4 = {
            "comment": 'a' * 101
        }
        r4 = self.put(url=url2, json=payload4, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code4,res4 = r4
            if not (status_code4 == 400 and res4['code'] == "InvalidParam"):
                self.exception.add("Step4:" + str(res4))
        else:
            self.exception.add("Step4:" + self.api_error)


        print('Step5: 用PUT方法调用https://192.168.6.62:19393/api/dns/zones/5bad0006接口，id对应的域不存在，将备注修改为“”')
        url3 = url1 + "/" + "5bad0006"
        payload5 = {
            "comment": ''
        }
        r5 = self.put(url=url3, json=payload5, auth=(self.api_user, self.api_password))
        if self.api_error is None:
            status_code5, res5 = r5
            if not (status_code5 == 400 and res5['code'] == "ZoneNotExisted"):
                self.exception.add("Step5:" + str(res5))
        else:
            self.exception.add("Step5:" + self.api_error)