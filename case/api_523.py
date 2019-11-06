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

    def test_delete_specific_auth_record(self):


        print('Step1: 点击【域管理】在node1下的default视图，添加test.com')
        domain1 = "test.com"
        ns_name1 = "ns." + domain1
        self.authorization_add_standard_domain(domainname=domain1, nodename=self.nodename[0], viewname='default',
                                               ns_name=ns_name1, ns_ip=self.serverip[0])

        print('Step2: 点击【记录管理】，添加y1.test.com的A记录为1.1.1.1')
        self.authorization_add_a_record(nodename=self.nodename[0],domain=domain1,host="y1",res="1.1.1.1")


        url1 = "https://" + self.serverip[0] + ":19393/api/dns/records"

        print('Step3: 用DELETE方法调用接口https://192.168.6.62:19393/api/dns/records/5bbf0b0c8889ee7be5a92334，按照ID删除步骤2中添加的记录')
        payload = {
                    "nodeName": self.nodename[0],
                    "domain": domain1,
                    "host": "y1." + domain1
                }
        r1 = self.get(url=url1,params=payload,auth=(self.api_user,self.api_password))
        id = ""
        if self.api_error is None:
            status_code1,res1 = r1
            if status_code1 == 200 and res1['code'] == "Success" and len(res1['data']) == 1:
                id = res1['data'][0]['id']
            else:
                self.exception.add('Step3: ' + str(r1))
        else:
            self.exception.add('Step3: 获取指定记录ID失败')

        url2 = url1 + "/" + str(id)

        r2 = self.delete(url=url2,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code2,res2 = r2
            if not (status_code2 == 200 and res2['code'] == "Success"):
                self.exception.add("Step3:删除记录失败 " + str(r2))
        else:
            self.exception.add('Step3:删除记录失败 ' + str(self.api_error) )

        print('Step4: 点击【记录管理】，查看页面的记录列表')
        self.authorization_enter_record_page()
        flag = self.authorization_find_specific_record(nodename=self.nodename[0],record="y1.test.com",type="A",res="1.1.1.1")
        if flag:
            self.exception.add("Step4:页面记录任然存在,删除失败")

        print('Step5: 用DELETE方法调用接口https://192.168.6.62:19393/api/dns/records/123456，删除不存在的记录')
        url3 = url1 + "/123456"
        r5 = self.delete(url=url3,auth=(self.api_user,self.api_password))
        if self.api_error is None:
            status_code5,res5 = r5
            if not (status_code5 == 400 and res5['code'] == "RecordNotExisted"):
                self.exception.add('Step5: ' + str(r5))
        else:
            self.exception.add('Step5: ' + str(self.api_error))

