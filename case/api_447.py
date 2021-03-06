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


    def test_delete_auth_record(self):
        url = "https://" + self.serverip[0] + ":19393/api/dns/records"
        print('添加授权域yamu.com')
        domain = "yamu.com"
        ns_name = "ns." + domain
        self.authorization_add_standard_domain(domainname=domain, nodename=self.nodename[0], viewname='default',
                                               ns_name=ns_name, ns_ip=self.serverip[0])


        print('添加a.yamu.com的A记录为211.1.1.1,备注为空')
        self.authorization_add_a_record(nodename=self.nodename[0],domain=domain,host="a",res="211.1.1.1")

        sleep(2)
        print('Step1: 先用GET方法调用https://192.168.6.62:19393/api/dns/records接口，查出a.yamu.com的id为5ba999be8889ee581b84d078')
        r1 = self.get(url=url,auth=(self.api_user,self.api_password))
        id = ""
        if self.api_error is  None:
            status_code1 = r1[0]
            res1 = r1[1]
            for zone in res1["data"]:
                domainname = zone.get("host")
                if domainname == 'a.' + domain:
                    id = zone.get("id")
                    break
                else:
                    continue
            if not (status_code1 == 200 and res1["code"] == "Success" and bool(id)):
                self.exception.add("Step1:" + str(res1))
        else:
            self.exception.add("Step1: " + self.api_error)

        print('Step2: 用DELETE方法调用https://192.168.6.62:19393/api/dns/record/5ba999be8889ee581b84d078,将a.yamu.com的A记录删除')
        url2 = url + "/" + str(id)
        r2 = self.delete(url=url2,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code2 = r2[0]
            res2 = r2[1]
            if not(status_code2 == 200 and res2['code'] == "Success"):
                self.exception.add("Step2:" + str(res2))
        else:
            self.exception.add("Step2:" + self.api_error)

        print('Step3: 点击【记录管理】，进入页面查看yamu.com的授权记录')
        self.authorization_enter_record_page()
        sleep(1)
        flag = self.authorization_find_specific_record(nodename=self.nodename[0],record="a.yamu.com",viewname="default",type="A",res="211.1.1.1")
        if flag:
            self.exception.add('Step2: 页面指定记录任然存在')


